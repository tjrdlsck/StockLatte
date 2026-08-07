import pytest
import json
import os
from stocklatte.models import Position, Portfolio
from stocklatte.rebalancing import MarketValueRebalancingEngine
from stocklatte.data_provider import StockDataProvider


def test_market_value_weight_calculation():
    """평가 금액 기반 비중 산출 수식을 검증하는 테스트입니다."""
    # NVDA 10주 @ $100 = $1,000
    # MSFT 10주 @ $200 = $2,000
    # 현금 = $1,000, 총 자산 = $4,000
    p1 = Position(ticker="NVDA", quantity=10, current_price=100.0)
    p2 = Position(ticker="MSFT", quantity=10, current_price=200.0)
    
    portfolio = Portfolio(
        positions=[p1, p2],
        cash=1000.0,
        target_weights={"NVDA": 50.0, "MSFT": 50.0}
    )

    assert p1.market_value == 1000.0
    assert p2.market_value == 2000.0
    assert portfolio.total_positions_value == 3000.0
    assert portfolio.total_value == 4000.0

    weights = portfolio.get_current_weights()
    # NVDA 비중: 1000 / 4000 = 25.0%
    # MSFT 비중: 2000 / 4000 = 50.0%
    assert weights["NVDA"] == 25.0
    assert weights["MSFT"] == 50.0


def test_proposal_example_rebalancing():
    """
    기획서(MACRO_STOCK_RECOMMENDATION_PROPOSAL.md) 2.1절 수치 예시 시나리오 검증:
    - NVDA: $7,500 (50% 쏠림) -> $3,000 차익 실현 (SELL)
    - MSFT: $3,500 (23.3%) -> $1,000 추가 매수 (BUY)
    - CAT: $4,000 (26.7%) -> $2,000 추가 매수 (BUY)
    - 총 자산: $15,000, 목표 비중: NVDA 30%, MSFT 30%, CAT 40%
    """
    # NVDA 50주 @ $150 = $7,500
    # MSFT 10주 @ $350 = $3,500
    # CAT 20주 @ $200 = $4,000
    nvda = Position(ticker="NVDA", quantity=50, current_price=150.0)
    msft = Position(ticker="MSFT", quantity=10, current_price=350.0)
    cat = Position(ticker="CAT", quantity=20, current_price=200.0)

    portfolio = Portfolio(
        positions=[nvda, msft, cat],
        cash=0.0,
        target_weights={"NVDA": 30.0, "MSFT": 30.0, "CAT": 40.0}
    )

    assert portfolio.total_value == 15000.0

    engine = MarketValueRebalancingEngine(overweight_threshold_pct=35.0)
    result = engine.calculate_rebalance(portfolio)

    # 1. 비중 쏠림 경경 검증 (NVDA 50% >= 35.0%)
    assert len(result.overweight_alerts) == 1
    assert result.overweight_alerts[0]["ticker"] == "NVDA"
    assert result.overweight_alerts[0]["current_weight"] == 50.0

    # 2. 리밸런싱 실행 액션 검증
    actions_by_ticker = {a.ticker: a for a in result.actions}
    
    # NVDA: 차익 실현 $3,000 (약 20주 @ $150)
    nvda_action = actions_by_ticker["NVDA"]
    assert nvda_action.action_type == "SELL"
    assert nvda_action.amount == 3000.0
    assert nvda_action.shares == 20.0  # 3000 / 150 = 20

    # MSFT: 추가 매수 $1,000
    msft_action = actions_by_ticker["MSFT"]
    assert msft_action.action_type == "BUY"
    assert msft_action.amount == 1000.0

    # CAT: 추가 매수 $2,000
    cat_action = actions_by_ticker["CAT"]
    assert cat_action.action_type == "BUY"
    assert cat_action.amount == 2000.0


def test_llm_json_generation():
    """LLM 주입용 JSON 컨텍스트 변환 검증 테스트"""
    nvda = Position(ticker="NVDA", quantity=50, current_price=150.0)
    msft = Position(ticker="MSFT", quantity=10, current_price=350.0)
    cat = Position(ticker="CAT", quantity=20, current_price=200.0)

    portfolio = Portfolio(
        positions=[nvda, msft, cat],
        cash=0.0,
        target_weights={"NVDA": 30.0, "MSFT": 30.0, "CAT": 40.0}
    )

    engine = MarketValueRebalancingEngine(overweight_threshold_pct=35.0)
    result = engine.calculate_rebalance(portfolio)

    json_str = result.to_llm_json()
    json_obj = json.loads(json_str)

    assert "market_value_rebalancing_input" in json_obj
    assert "llm_rebalancing_execution_plan" in json_obj
    assert json_obj["llm_rebalancing_execution_plan"]["action"] == "EXECUTE_MARKET_VALUE_REBALANCING"


def test_stock_data_provider_mock():
    """Mock 데이터 수집기를 활용한 주가 수집 검증 테스트"""
    provider = StockDataProvider(mock_prices={"NVDA": 150.0, "MSFT": 350.0})
    prices = provider.fetch_current_prices(["NVDA", "MSFT"])
    assert prices["NVDA"] == 150.0
    assert prices["MSFT"] == 350.0


def test_new_ticker_buy_action():
    """피드백 7번 검증: 현재 미보유 신규 종목(target_weights에만 지정)에 대한 BUY 주문 정상 생성 여부 테스트"""
    aapl = Position(ticker="AAPL", quantity=100, current_price=100.0) # $10,000 (100%)
    portfolio = Portfolio(
        positions=[aapl],
        cash=0.0,
        target_weights={"AAPL": 60.0, "NVDA": 40.0} # NVDA는 현재 보유 0개
    )
    engine = MarketValueRebalancingEngine(rebalance_band_pct=0.5)
    result = engine.calculate_rebalance(portfolio)
    
    actions_map = {a.ticker: a for a in result.actions}
    assert "NVDA" in actions_map
    assert actions_map["NVDA"].action_type == "BUY"
    assert actions_map["NVDA"].amount == 4000.0 # 40% of 10,000


def test_rebalance_band_filter():
    """피드백 9번 검증: 미세 비중 차이(허용 밴드 이하)에 대해 거래 비용 절감을 위해 HOLD 처리하는지 테스트"""
    aapl = Position(ticker="AAPL", quantity=50, current_price=100.0) # $5,000 (50.5%)
    msft = Position(ticker="MSFT", quantity=49, current_price=100.0) # $4,900 (49.5%)
    portfolio = Portfolio(
        positions=[aapl, msft],
        cash=0.0,
        target_weights={"AAPL": 50.0, "MSFT": 50.0}
    )
    # 0.5% 차이는 rebalance_band_pct = 1.0%p 설정 시 거래 생성되지 않음
    engine = MarketValueRebalancingEngine(rebalance_band_pct=1.0)
    result = engine.calculate_rebalance(portfolio)
    assert len(result.actions) == 0


def test_target_weight_validation():
    """피드백 7번 검증: 목표 비중 합계 100% 초과 시 예외 발생 테스트"""
    aapl = Position(ticker="AAPL", quantity=10, current_price=100.0)
    portfolio = Portfolio(
        positions=[aapl],
        cash=0.0,
        target_weights={"AAPL": 70.0, "MSFT": 50.0} # 합계 120%
    )
    engine = MarketValueRebalancingEngine()
    with pytest.raises(ValueError, match="100%를 초과"):
        engine.calculate_rebalance(portfolio)

