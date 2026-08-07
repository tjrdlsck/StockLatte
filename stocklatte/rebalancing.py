from typing import List
from stocklatte.models import Portfolio, RebalanceAction, RebalanceResult


class MarketValueRebalancingEngine:
    """
    평가 금액(Market Value) 기준 비중 계산 & 스마트 포트폴리오 리밸런싱 엔진
    """

    def __init__(self, overweight_threshold_pct: float = 35.0, rebalance_band_pct: float = 1.0):
        """
        :param overweight_threshold_pct: 비중 쏠림 경보 감지 기준 (%)
        :param rebalance_band_pct: 리밸런싱 매매 허용 밴드 (%p). 이 값 이하의 미세한 비중 차이는 거래 비용 절감을 위해 이행하지 않음.
        """
        self.overweight_threshold_pct = overweight_threshold_pct
        self.rebalance_band_pct = rebalance_band_pct

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

        target_sum = sum(target_weights.values())
        if target_sum > 100.001:
            raise ValueError(f"목표 비중의 합계({target_sum:.1f}%)가 100%를 초과합니다.")

        current_weights = portfolio.get_current_weights()
        overweight_alerts = portfolio.detect_overweight_positions(
            threshold_pct=self.overweight_threshold_pct
        )

        pos_dict = {p.ticker: p for p in portfolio.positions}
        all_tickers = sorted(list(set(pos_dict.keys()) | set(target_weights.keys())))

        actions: List[RebalanceAction] = []

        for ticker in all_tickers:
            pos = pos_dict.get(ticker)
            target_pct = target_weights.get(ticker, 0.0)
            current_pct = current_weights.get(ticker, 0.0)
            target_market_value = round(total_val * (target_pct / 100.0), 2)
            current_market_value = pos.market_value if pos else 0.0
            price = pos.current_price if pos else 0.0

            # 비중 격차 (%p)
            weight_diff = current_pct - target_pct

            # 허용 밴드 이하의 미세 차이는 리밸런싱 이행 안함
            if abs(weight_diff) < self.rebalance_band_pct:
                continue

            diff_val = round(current_market_value - target_market_value, 2)

            if diff_val > 0:
                # 과비중 조절 매도 (TRIM_OVERWEIGHT)
                sell_amount = diff_val
                shares_to_sell = round(sell_amount / price, 2) if price > 0 else 0
                actions.append(
                    RebalanceAction(
                        ticker=ticker,
                        action_type="SELL",
                        amount=sell_amount,
                        shares=shares_to_sell,
                        target_weight=target_pct,
                        current_weight=current_pct,
                        new_weight=target_pct
                    )
                )
            elif diff_val < 0:
                # 미달 비중 채움 매수 (ADD_UNDERWEIGHT / NEW BUY)
                buy_amount = abs(diff_val)
                shares_to_buy = round(buy_amount / price, 2) if price > 0 else 0
                actions.append(
                    RebalanceAction(
                        ticker=ticker,
                        action_type="BUY",
                        amount=buy_amount,
                        shares=shares_to_buy,
                        target_weight=target_pct,
                        current_weight=current_pct,
                        new_weight=target_pct
                    )
                )

        return RebalanceResult(
            total_portfolio_value=total_val,
            target_weights=target_weights,
            actions=actions,
            overweight_alerts=overweight_alerts,
            all_positions=portfolio.positions
        )

