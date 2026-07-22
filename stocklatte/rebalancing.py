from typing import List
from stocklatte.models import Portfolio, RebalanceAction, RebalanceResult


class MarketValueRebalancingEngine:
    """
    평가 금액(Market Value) 기준 비중 계산 & Sell High, Buy Low 스마트 리밸런싱 엔진
    """

    def __init__(self, overweight_threshold_pct: float = 35.0):
        """
        :param overweight_threshold_pct: 비중 쏠림 경보 감지 기준 (%)
        """
        self.overweight_threshold_pct = overweight_threshold_pct

    def calculate_rebalance(self, portfolio: Portfolio) -> RebalanceResult:
        """
        포트폴리오의 평가 금액 기준 비중 이탈을 계산하여 스마트 리밸런싱 가이드를 산출합니다.

        :param portfolio: Portfolio 객체
        :return: RebalanceResult 객체
        """
        total_val = portfolio.total_value
        if total_val <= 0:
            raise ValueError("포트폴리오 총 평가 자산이 0 이하입니다.")

        target_weights = portfolio.target_weights
        if not target_weights:
            raise ValueError("포트폴리오에 설정된 목표 비중(target_weights)이 없습니다.")

        current_weights = portfolio.get_current_weights()
        overweight_alerts = portfolio.detect_overweight_positions(
            threshold_pct=self.overweight_threshold_pct
        )

        actions: List[RebalanceAction] = []

        for pos in portfolio.positions:
            ticker = pos.ticker
            target_pct = target_weights.get(ticker, 0.0)
            target_market_value = round(total_val * (target_pct / 100.0), 2)
            current_market_value = pos.market_value
            diff = round(current_market_value - target_market_value, 2)

            if diff > 0.01:
                # 차익 실현 (Sell High): 현재 평가액이 목표 평가액보다 큼
                sell_amount = diff
                shares_to_sell = round(sell_amount / pos.current_price, 2) if pos.current_price > 0 else 0
                actions.append(
                    RebalanceAction(
                        ticker=ticker,
                        action_type="SELL",
                        amount=sell_amount,
                        shares=shares_to_sell,
                        target_weight=target_pct,
                        current_weight=current_weights.get(ticker, 0.0),
                        new_weight=target_pct
                    )
                )
            elif diff < -0.01:
                # 저점 매수 (Buy Low): 현재 평가액이 목표 평가액보다 작음
                buy_amount = abs(diff)
                shares_to_buy = round(buy_amount / pos.current_price, 2) if pos.current_price > 0 else 0
                actions.append(
                    RebalanceAction(
                        ticker=ticker,
                        action_type="BUY",
                        amount=buy_amount,
                        shares=shares_to_buy,
                        target_weight=target_pct,
                        current_weight=current_weights.get(ticker, 0.0),
                        new_weight=target_pct
                    )
                )

        return RebalanceResult(
            total_portfolio_value=total_val,
            target_weights=target_weights,
            actions=actions,
            overweight_alerts=overweight_alerts
        )
