from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json


@dataclass
class Position:
    """개별 종목 포지션 정보 데이터 클래스"""
    ticker: str
    quantity: float
    current_price: float

    @property
    def market_value(self) -> float:
        """현재 평가 금액 (보유 수량 * 현재 주가)"""
        return round(self.quantity * self.current_price, 2)


@dataclass
class Portfolio:
    """포트폴리오 정보 데이터 클래스"""
    positions: List[Position]
    cash: float = 0.0
    target_weights: Dict[str, float] = field(default_factory=dict)

    @property
    def total_positions_value(self) -> float:
        """주식 포지션의 총 평가 금액"""
        return round(sum(p.market_value for p in self.positions), 2)

    @property
    def total_value(self) -> float:
        """포트폴리오 총 평가 자산 (주식 평가액 + 현금)"""
        return round(self.total_positions_value + self.cash, 2)

    def get_current_weights(self) -> Dict[str, float]:
        """종목별 현재 비중(%) 산출 (현재 평가 금액 / 포트폴리오 총 평가 금액 * 100)"""
        tot = self.total_value
        if tot <= 0:
            return {p.ticker: 0.0 for p in self.positions}
        return {
            p.ticker: round((p.market_value / tot) * 100, 2)
            for p in self.positions
        }

    def detect_overweight_positions(self, threshold_pct: float = 35.0) -> List[Dict[str, float]]:
        """
        비중 쏠림 경보 감지
        :param threshold_pct: 쏠림으로 판단할 임계 비중(%) 또는 목표 비중과의 격차 기준
        :return: 쏠림이 발생한 종목 정보 리스트
        """
        weights = self.get_current_weights()
        overweighted = []
        for ticker, weight in weights.items():
            target = self.target_weights.get(ticker, 0.0)
            # 특정 절대 비중 초과 또는 목표 비중 대비 10%p 이상 초과 쏠림 시 경보
            if weight >= threshold_pct or (target > 0 and weight - target >= 10.0):
                overweighted.append({
                    "ticker": ticker,
                    "current_weight": weight,
                    "target_weight": target,
                    "market_value": next(p.market_value for p in self.positions if p.ticker == ticker)
                })
        return overweighted


@dataclass
class RebalanceAction:
    """리밸런싱 매수/매도 실행 조치 데이터 클래스"""
    ticker: str
    action_type: str  # "SELL" (차익 실현) or "BUY" (저점 매수)
    amount: float     # 조치 대상 금액 ($)
    shares: float     # 예상 주식 수량
    target_weight: float
    current_weight: float
    new_weight: float


@dataclass
class RebalanceResult:
    """스마트 리밸런싱 최종 산출 결과 데이터 클래스"""
    total_portfolio_value: float
    target_weights: Dict[str, float]
    actions: List[RebalanceAction]
    overweight_alerts: List[Dict[str, float]]
    all_positions: Optional[List[Position]] = None

    def to_llm_json(self) -> str:
        """LLM 주입용 리밸런싱 산출 결과 JSON 포맷 변환 (전체 포지션 및 경고 분리)"""
        trim_actions = [a for a in self.actions if a.action_type == "SELL"]
        add_actions = [a for a in self.actions if a.action_type == "BUY"]

        step1_desc = []
        for act in trim_actions:
            step1_desc.append(
                f"{act.ticker} 주식 중 ${act.amount:,.2f}치(약 {act.shares:.1f}주)를 비중 조절 매도하여 "
                f"{act.ticker} 비중을 {act.new_weight:.1f}%로 조정하십시오."
            )

        step2_desc = []
        for act in add_actions:
            step2_desc.append(
                f"{act.ticker} ${act.amount:,.2f}치 추가 매수"
            )

        step1_str = " 및 ".join(step1_desc) if step1_desc else "비중 매도 조치 대상 없음"
        step2_str = "비중 조절 현금으로 " + ", ".join(step2_desc) + "하여 목표 비중을 완충하십시오." if step2_desc else "추가 매수 조치 대상 없음"

        positions_list = []
        if self.all_positions:
            tot = self.total_portfolio_value
            for pos in self.all_positions:
                cur_w = round((pos.market_value / tot * 100.0), 1) if tot > 0 else 0.0
                positions_list.append({
                    "ticker": pos.ticker,
                    "current_market_value": f"${pos.market_value:,.2f}",
                    "current_weight": f"{cur_w:.1f}%"
                })
        else:
            for alert in self.overweight_alerts:
                positions_list.append({
                    "ticker": alert["ticker"],
                    "current_market_value": f"${alert['market_value']:,.2f}",
                    "current_weight": f"{alert['current_weight']:.1f}%"
                })

        output_data = {
            "market_value_rebalancing_input": {
                "total_portfolio_value": f"${self.total_portfolio_value:,.2f}",
                "target_weights": {k: f"{v:.1f}%" for k, v in self.target_weights.items()},
                "current_positions": positions_list,
                "overweight_alerts": self.overweight_alerts
            },
            "llm_rebalancing_execution_plan": {
                "action": "EXECUTE_MARKET_VALUE_REBALANCING",
                "step1_trim_overweight": step1_str,
                "step2_add_underweight": step2_str
            }
        }
        return json.dumps(output_data, ensure_ascii=False, indent=2)

