"""
StockLatte Pure Data-Driven Point-in-Time Backtester
=====================================================
Look-ahead Bias(미래 데이터 참조 오염) 및 수동 성과 보정을 100% 제거한
순수 시장 데이터 기반 시계열 롤링 백테스터.
"""

from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd
import yfinance as yf
from stocklatte.screener import Adaptive3DCouplingScreener


class FullCycleBacktester:
    """
    연속 시계열 복리 백테스트 엔진 클래스
    """

    def __init__(self, start_date: str = "2022-01-01", end_date: str = "2026-01-01"):
        self.start_date = start_date
        self.end_date = end_date

    def fetch_full_4year_prices(self, tickers: List[str]) -> pd.DataFrame:
        price_dict = {}
        for t in tickers:
            try:
                hist = yf.Ticker(t).history(start=self.start_date, end=self.end_date)
                if not hist.empty and "Close" in hist.columns:
                    price_dict[t] = hist["Close"]
            except Exception:
                pass
        return pd.DataFrame(price_dict).dropna()

    def run_full_4year_backtest(self, passed_tickers: List[str], benchmark_ticker: str = "SPY", weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        all_tickers = list(set(passed_tickers + [benchmark_ticker]))
        df_prices = self.fetch_full_4year_prices(all_tickers)
        
        if df_prices.empty or len(df_prices) < 20:
            return {"error": "데이터 수집 실패 또는 보유 기간 부족", "portfolio_total_return_pct": 0.0, "benchmark_total_return_pct": 0.0}

        daily_returns = df_prices.pct_change().dropna()
        valid_portfolio_cols = [t for t in passed_tickers if t in daily_returns.columns]
        
        if not valid_portfolio_cols:
            portfolio_daily = pd.Series(0.0, index=daily_returns.index)
        elif weights and any(t in weights for t in valid_portfolio_cols):
            # weights가 주어진 경우 점수 비례 포트폴리오 가중치 적용
            w_dict = {t: weights.get(t, 0.0) for t in valid_portfolio_cols}
            w_sum = sum(w_dict.values())
            if w_sum > 0:
                normalized_weights = pd.Series({t: w / w_sum for t, w in w_dict.items()})
                portfolio_daily = (daily_returns[valid_portfolio_cols] * normalized_weights).sum(axis=1)
            else:
                portfolio_daily = daily_returns[valid_portfolio_cols].mean(axis=1)
        else:
            portfolio_daily = daily_returns[valid_portfolio_cols].mean(axis=1)
            
        benchmark_daily = daily_returns[benchmark_ticker] if benchmark_ticker in daily_returns.columns else daily_returns.iloc[:, 0]
        
        portfolio_cum = (1.0 + portfolio_daily).cumprod()
        benchmark_cum = (1.0 + benchmark_daily).cumprod()
        
        port_final = float(portfolio_cum.values[-1]) if not portfolio_cum.empty else 1.0
        bench_final = float(benchmark_cum.values[-1]) if not benchmark_cum.empty else 1.0
        
        total_days = len(portfolio_daily)
        years = float(total_days / 252.0) if total_days > 0 else 1.0
        
        port_total_ret = (port_final - 1.0) * 100.0
        bench_total_ret = (bench_final - 1.0) * 100.0
        
        port_cagr = ((port_final) ** (1.0 / max(years, 0.1)) - 1.0) * 100.0
        bench_cagr = ((bench_final) ** (1.0 / max(years, 0.1)) - 1.0) * 100.0
        
        port_peak = portfolio_cum.cummax()
        port_dd = (portfolio_cum - port_peak) / port_peak if not port_peak.empty else pd.Series(0.0, index=portfolio_cum.index)
        port_mdd = float(port_dd.min()) * 100.0 if not port_dd.empty else 0.0
        
        bench_peak = benchmark_cum.cummax()
        bench_dd = (benchmark_cum - bench_peak) / bench_peak if not bench_peak.empty else pd.Series(0.0, index=benchmark_cum.index)
        bench_mdd = float(bench_dd.min()) * 100.0 if not bench_dd.empty else 0.0
        
        rf_daily = 0.03 / 252.0
        std_val = portfolio_daily.std()
        sharpe_ratio = float(np.sqrt(252) * (portfolio_daily.mean() - rf_daily) / (std_val + 1e-6)) if std_val > 0 else 0.0
        
        ind_returns = {}
        for t in valid_portfolio_cols:
            if not df_prices[t].empty:
                sp = float(df_prices[t].iloc[0])
                ep = float(df_prices[t].iloc[-1])
                ind_returns[t] = round(((ep - sp) / sp) * 100.0, 2) if sp > 0 else 0.0
            
        sorted_ind = dict(sorted(ind_returns.items(), key=lambda x: x[1], reverse=True))

        return {
            "period_years": round(years, 2),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "portfolio_total_return_pct": round(port_total_ret, 2),
            "benchmark_total_return_pct": round(bench_total_ret, 2),
            "portfolio_cagr_pct": round(port_cagr, 2),
            "benchmark_cagr_pct": round(bench_cagr, 2),
            "total_alpha_cagr_pct": round(port_cagr - bench_cagr, 2),
            "portfolio_mdd_pct": round(port_mdd, 2),
            "benchmark_mdd_pct": round(bench_mdd, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "sorted_individual_returns": sorted_ind
        }


class PointInTimeBacktester:
    """
    Look-ahead Bias(미래 데이터 참조 편향)를 차단하고 
    수동 가상 알파 추가를 100% 제거한 순수 PIT 백테스터 클래스.
    """

    def __init__(self, ticker_universe: List[str]):
        self.ticker_universe = ticker_universe
        self.screener = Adaptive3DCouplingScreener()

    def run_screener_coupled_pit_backtest(self, years: List[int] = [2022, 2023, 2024, 2025], use_score_weights: bool = True) -> Dict[str, Any]:
        """
        Adaptive3DCouplingScreener의 스크리닝 알고리즘(레짐 판단, Dual RS, Quality Factor, 과열 페널티 등)을 
        100% 동일하게 이식하여 분기별 포인트-인-타임(Point-in-Time) 백테스트를 수행합니다.
        """
        yearly_quarterly_results = {}
        all_quarter_returns = []
        all_spy_returns = []
        
        for y in years:
            quarters = [
                (f"{y}-01-01", f"{y}-03-31"),
                (f"{y}-04-01", f"{y}-06-30"),
                (f"{y}-07-01", f"{y}-09-30"),
                (f"{y}-10-01", f"{y}-12-31")
            ]
            
            port_quarter_rets = []
            spy_quarter_rets = []
            selected_tickers_per_q = {}
            regimes_per_q = {}
            weights_per_q = {}
            
            for idx, (q_start, q_end) in enumerate(quarters, 1):
                # 1. 라이브 스크리너 로직을 as_of_date=q_start 시점으로 그대로 실행
                df_screened = self.screener.run_adaptive_screening(self.ticker_universe, as_of_date=q_start)
                
                # 통과 종목 및 비중 파악
                passed_df = df_screened[df_screened["is_passed"]] if ("is_passed" in df_screened.columns and not df_screened[df_screened["is_passed"]].empty) else df_screened.head(5)
                if passed_df.empty:
                    passed_df = df_screened.head(5)
                    
                selected_tickers = passed_df["ticker"].tolist()
                weights = dict(zip(passed_df["ticker"], passed_df["score_weight_pct"])) if (use_score_weights and "score_weight_pct" in passed_df.columns) else None
                
                q_key = f"Q{idx}"
                selected_tickers_per_q[q_key] = selected_tickers
                weights_per_q[q_key] = weights
                regimes_per_q[q_key] = df_screened["regime_detected"].iloc[0] if ("regime_detected" in df_screened.columns and not df_screened.empty) else "GOLDILOCKS_EXPANSION"
                
                # 2. 풀사이클 백테스터로 해당 분기 실적 및 포트폴리오 수익률 산출
                bt = FullCycleBacktester(start_date=q_start, end_date=q_end)
                res = bt.run_full_4year_backtest(selected_tickers, benchmark_ticker="SPY", weights=weights)
                
                port_q_ret = res.get("portfolio_total_return_pct", 0.0)
                spy_q_ret = res.get("benchmark_total_return_pct", 0.0)
                
                port_quarter_rets.append(port_q_ret)
                spy_quarter_rets.append(spy_q_ret)
                all_quarter_returns.append(port_q_ret)
                all_spy_returns.append(spy_q_ret)
                
            port_cum = 1.0
            spy_cum = 1.0
            for pr, sr in zip(port_quarter_rets, spy_quarter_rets):
                port_cum *= (1.0 + pr / 100.0)
                spy_cum *= (1.0 + sr / 100.0)
                
            port_year_total = (port_cum - 1.0) * 100.0
            spy_year_total = (spy_cum - 1.0) * 100.0
            
            yearly_quarterly_results[y] = {
                "selected_tickers_by_quarter": selected_tickers_per_q,
                "weights_by_quarter": weights_per_q,
                "regime_by_quarter": regimes_per_q,
                "portfolio_return_pct": round(port_year_total, 2),
                "benchmark_return_pct": round(spy_year_total, 2),
                "alpha_return_pct": round(port_year_total - spy_year_total, 2)
            }
            
        # 전체 통산 복리 성과 계산
        total_port_cum = 1.0
        total_spy_cum = 1.0
        for pr, sr in zip(all_quarter_returns, all_spy_returns):
            total_port_cum *= (1.0 + pr / 100.0)
            total_spy_cum *= (1.0 + sr / 100.0)
            
        total_years = len(years)
        tot_port_ret = (total_port_cum - 1.0) * 100.0
        tot_spy_ret = (total_spy_cum - 1.0) * 100.0
        
        port_cagr = ((total_port_cum) ** (1.0 / max(total_years, 0.1)) - 1.0) * 100.0
        spy_cagr = ((total_spy_cum) ** (1.0 / max(total_years, 0.1)) - 1.0) * 100.0
        
        return {
            "years_evaluated": years,
            "yearly_quarterly_results": yearly_quarterly_results,
            "total_portfolio_return_pct": round(tot_port_ret, 2),
            "total_benchmark_return_pct": round(tot_spy_ret, 2),
            "portfolio_cagr_pct": round(port_cagr, 2),
            "benchmark_cagr_pct": round(spy_cagr, 2),
            "total_alpha_cagr_pct": round(port_cagr - spy_cagr, 2)
        }

    def get_historical_prices_up_to(self, tickers: List[str], as_of_date: str, lookback_days: int = 365) -> pd.DataFrame:
        """
        as_of_date 이전 lookback_days 동안의 가격 데이터만 수집 (미래 데이터 차단)
        """
        end_dt = pd.to_datetime(as_of_date)
        start_dt = end_dt - pd.Timedelta(days=lookback_days)
        
        price_dict = {}
        for t in tickers:
            try:
                hist = yf.Ticker(t).history(start=start_dt.strftime("%Y-%m-%d"), end=end_dt.strftime("%Y-%m-%d"))
                if not hist.empty and "Close" in hist.columns:
                    price_dict[t] = hist["Close"]
            except Exception:
                pass
        return pd.DataFrame(price_dict).dropna()

    def run_point_in_time_screening(self, as_of_date: str) -> List[str]:
        """
        as_of_date 시점 이전에 존재하는 과거 historical price만으로 상대강도(RS) 스코어 산출
        """
        all_tickers = list(set(self.ticker_universe + ["SPY"]))
        df_hist = self.get_historical_prices_up_to(all_tickers, as_of_date=as_of_date, lookback_days=365)
        
        if df_hist.empty or "SPY" not in df_hist.columns:
            # 데이터 수집 실패 시 유효한 종목만 반환 (임의 하드코딩 대체 없음)
            return [t for t in self.ticker_universe if t in df_hist.columns]
            
        spy_prices = df_hist["SPY"]
        if len(spy_prices) < 20:
            return [t for t in self.ticker_universe if t in df_hist.columns]

        spy_ret_6m = ((spy_prices.iloc[-1] - spy_prices.iloc[0]) / spy_prices.iloc[0]) * 100.0
        
        passed_tickers = []
        rs_scores = {}
        
        for t in self.ticker_universe:
            if t in df_hist.columns and len(df_hist[t]) >= 20:
                stock_prices = df_hist[t]
                stock_ret_6m = ((stock_prices.iloc[-1] - stock_prices.iloc[0]) / stock_prices.iloc[0]) * 100.0
                rs_score = stock_ret_6m - spy_ret_6m
                rs_scores[t] = rs_score
                if rs_score > -5.0:
                    passed_tickers.append(t)
                    
        sorted_passed = sorted(passed_tickers, key=lambda x: rs_scores.get(x, -999.0), reverse=True)
        return sorted_passed[:10] if sorted_passed else [t for t in self.ticker_universe if t in df_hist.columns][:5]

    def run_quarterly_pit_backtest(self, years: List[int] = [2022, 2023, 2024, 2025]) -> Dict[str, Any]:
        yearly_quarterly_results = {}
        
        for y in years:
            quarters = [
                (f"{y}-01-01", f"{y}-03-31"),
                (f"{y}-04-01", f"{y}-06-30"),
                (f"{y}-07-01", f"{y}-09-30"),
                (f"{y}-10-01", f"{y}-12-31")
            ]
            
            port_quarter_rets = []
            spy_quarter_rets = []
            selected_tickers_per_q = {}
            
            for idx, (q_start, q_end) in enumerate(quarters, 1):
                pit_tickers = self.run_point_in_time_screening(as_of_date=q_start)
                selected_tickers_per_q[f"Q{idx}"] = pit_tickers
                
                bt = FullCycleBacktester(start_date=q_start, end_date=q_end)
                res = bt.run_full_4year_backtest(pit_tickers, benchmark_ticker="SPY")
                
                port_q_ret = res.get("portfolio_total_return_pct", 0.0)
                spy_q_ret = res.get("benchmark_total_return_pct", 0.0)
                
                port_quarter_rets.append(port_q_ret)
                spy_quarter_rets.append(spy_q_ret)
                
            port_cum = 1.0
            spy_cum = 1.0
            for pr, sr in zip(port_quarter_rets, spy_quarter_rets):
                port_cum *= (1.0 + pr / 100.0)
                spy_cum *= (1.0 + sr / 100.0)
                
            port_year_total = (port_cum - 1.0) * 100.0
            spy_year_total = (spy_cum - 1.0) * 100.0
            
            yearly_quarterly_results[y] = {
                "selected_tickers_by_quarter": selected_tickers_per_q,
                "portfolio_return_pct": round(port_year_total, 2),
                "benchmark_return_pct": round(spy_year_total, 2),
                "alpha_pct": round(port_year_total - spy_year_total, 2),
                "quarterly_returns": [round(r, 2) for r in port_quarter_rets]
            }
        return yearly_quarterly_results

    def run_audited_semiannual_and_annual_backtest(self, years: List[int] = [2022, 2023, 2024, 2025]) -> Dict[str, Any]:
        """
        순수 시장 주가 시계열 기반 반기/연간 롤링 백테스트 (년도별 조건식 제거)
        """
        audit_results = {}
        
        for y in years:
            semi_periods = [
                ("H1", f"{y}-01-01", f"{y}-06-30"),
                ("H2", f"{y}-07-01", f"{y}-12-31")
            ]
            
            semi_results = {}
            h_port_rets = []
            h_spy_rets = []
            
            for h_label, s_date, e_date in semi_periods:
                q_bt = self.run_quarterly_pit_backtest(years=[y])
                q_rets = q_bt[y]["quarterly_returns"]
                
                if h_label == "H1":
                    port_ret = ((1 + q_rets[0]/100.0) * (1 + q_rets[1]/100.0) - 1) * 100.0
                else:
                    port_ret = ((1 + q_rets[2]/100.0) * (1 + q_rets[3]/100.0) - 1) * 100.0
                    
                bt_h = FullCycleBacktester(start_date=s_date, end_date=e_date)
                res_h = bt_h.run_full_4year_backtest(self.ticker_universe[:10], benchmark_ticker="SPY")
                spy_ret = res_h.get("benchmark_total_return_pct", 0.0)
                
                h_port_rets.append(round(port_ret, 2))
                h_spy_rets.append(round(spy_ret, 2))
                
                semi_results[h_label] = {
                    "portfolio_return_pct": round(port_ret, 2),
                    "benchmark_return_pct": round(spy_ret, 2),
                    "alpha_pct": round(port_ret - spy_ret, 2)
                }
                
            annual_port_cum = (1 + h_port_rets[0]/100.0) * (1 + h_port_rets[1]/100.0) - 1
            annual_spy_cum = (1 + h_spy_rets[0]/100.0) * (1 + h_spy_rets[1]/100.0) - 1
            
            annual_port_ret = round(annual_port_cum * 100.0, 2)
            annual_spy_ret = round(annual_spy_cum * 100.0, 2)
            
            audit_results[y] = {
                "semi_annual": semi_results,
                "annual_portfolio_return_pct": annual_port_ret,
                "annual_benchmark_return_pct": annual_spy_ret,
                "annual_alpha_pct": round(annual_port_ret - annual_spy_ret, 2)
            }
            
        return audit_results

    def run_earnings_derisked_pit_backtest(self, years: List[int] = [2022, 2023, 2024, 2025]) -> Dict[str, Any]:
        """
        가상의 성과 추가 수치(+1.8%p 등)를 100% 제거하고 순수 데이터 백테스트 결과 반환
        """
        derisked_results = {}
        audited_base = self.run_audited_semiannual_and_annual_backtest(years=years)
        
        for y in years:
            base_year_data = audited_base[y]
            base_annual_ret = base_year_data["annual_portfolio_return_pct"]
            spy_ret = base_year_data["annual_benchmark_return_pct"]
            
            derisked_results[y] = {
                "base_portfolio_return_pct": base_annual_ret,
                "derisked_portfolio_return_pct": base_annual_ret,
                "benchmark_return_pct": spy_ret,
                "derisked_alpha_pct": round(base_annual_ret - spy_ret, 2),
                "derisked_benefit_pct": 0.0
            }
            
        return derisked_results

    def run_v11_sec_news_audited_backtest(self, years: List[int] = [2022, 2023, 2024, 2025]) -> Dict[str, Any]:
        """
        가상의 성과 보정치(+2.2%p, +1.55%p 등)를 100% 제거하고 순수 데이터 백테스트 결과 반환
        """
        v11_results = {}
        derisked_base = self.run_earnings_derisked_pit_backtest(years=years)
        
        for y in years:
            base_data = derisked_base[y]
            derisked_ret = base_data["derisked_portfolio_return_pct"]
            spy_ret = base_data["benchmark_return_pct"]
            
            v11_results[y] = {
                "base_portfolio_return_pct": derisked_ret,
                "v11_portfolio_return_pct": derisked_ret,
                "benchmark_return_pct": spy_ret,
                "v11_alpha_pct": round(derisked_ret - spy_ret, 2),
                "v11_improvement_pct": 0.0
            }
            
        return v11_results

    def run_fee_adjusted_audited_backtest(self, fee_and_slippage_pct: float = 0.20, years: List[int] = [2022, 2023, 2024, 2025]) -> Dict[str, Any]:
        """
        실제 회전율 및 거래 수수료/슬리피지 차감 백테스트
        """
        fee_adjusted_results = {}
        v11_base = self.run_v11_sec_news_audited_backtest(years=years)
        
        for y in years:
            base_data = v11_base[y]
            raw_v11_ret = base_data["v11_portfolio_return_pct"]
            spy_ret = base_data["benchmark_return_pct"]
            
            # 연간 4회 리밸런싱 비용 차감 (약 0.45%p 차감)
            annual_fee_cost = round(fee_and_slippage_pct * 2.25, 2)
            fee_adjusted_ret = round(raw_v11_ret - annual_fee_cost, 2)
            
            fee_adjusted_results[y] = {
                "raw_v11_return_pct": raw_v11_ret,
                "annual_fee_cost_pct": annual_fee_cost,
                "fee_adjusted_return_pct": fee_adjusted_ret,
                "benchmark_return_pct": spy_ret,
                "fee_adjusted_alpha_pct": round(fee_adjusted_ret - spy_ret, 2)
            }
            
        return fee_adjusted_results

    def run_kis_korean_tax_audited_backtest(self, initial_seed_krw: int = 2000000, years: List[int] = [2022, 2023, 2024, 2025]) -> Dict[str, Any]:
        """
        한국투자증권(KIS) 미국 주식 거래 수수료/환전비용(연 -0.80%p) 및 
        해외주식 양도소득세(연 250만원 공제 후 22% 단일과세) 세후 복리 백테스터.
        """
        v11_base = self.run_v11_sec_news_audited_backtest(years=years)
        current_seed = float(initial_seed_krw)
        tax_results = {}
        
        for y in years:
            base_data = v11_base[y]
            raw_v11_ret = base_data["v11_portfolio_return_pct"]
            spy_ret = base_data["benchmark_return_pct"]
            
            kis_net_ret = round(raw_v11_ret - 0.80, 2)
            
            start_balance = current_seed
            end_balance_pre_tax = start_balance * (1.0 + kis_net_ret / 100.0)
            annual_gain = end_balance_pre_tax - start_balance
            
            taxable_gain = max(0.0, annual_gain - 2500000.0)
            tax_amount = taxable_gain * 0.22
            
            end_balance_after_tax = end_balance_pre_tax - tax_amount
            current_seed = end_balance_after_tax
            
            cum_ret_after_tax = round(((end_balance_after_tax - initial_seed_krw) / initial_seed_krw) * 100.0, 2)
            
            tax_results[y] = {
                "start_balance_krw": round(start_balance),
                "kis_net_return_pct": kis_net_ret,
                "end_balance_pre_tax_krw": round(end_balance_pre_tax),
                "annual_gain_krw": round(annual_gain),
                "tax_amount_krw": round(tax_amount),
                "end_balance_after_tax_krw": round(end_balance_after_tax),
                "cum_return_after_tax_pct": cum_ret_after_tax,
                "benchmark_return_pct": spy_ret
            }
            
        return tax_results

    def run_monthly_dca_korean_tax_backtest(self, monthly_deposit_krw: int = 300000, years: List[int] = [2022, 2023, 2024, 2025]) -> Dict[str, Any]:
        """
        매월 30만 원 적립식(Monthly DCA) 불입 시 한국투자증권 수수료/환전비용 및 
        해외주식 양도소득세(연 250만 원 공제 후 22%) 세후 복리 백테스터.
        """
        v11_base = self.run_v11_sec_news_audited_backtest(years=years)
        current_balance = 0.0
        cum_deposited_krw = 0
        dca_results = {}
        
        for y in years:
            base_data = v11_base[y]
            raw_v11_ret = base_data["v11_portfolio_return_pct"]
            spy_ret = base_data["benchmark_return_pct"]
            kis_net_ret = round(raw_v11_ret - 0.80, 2)
            
            monthly_rate = (1.0 + kis_net_ret / 100.0) ** (1.0 / 12.0) - 1.0
            year_start_balance = current_balance
            
            temp_bal = year_start_balance
            for _ in range(12):
                temp_bal = (temp_bal + monthly_deposit_krw) * (1.0 + monthly_rate)
                cum_deposited_krw += monthly_deposit_krw
                
            end_balance_pre_tax = temp_bal
            annual_gain = end_balance_pre_tax - (year_start_balance + monthly_deposit_krw * 12)
            
            taxable_gain = max(0.0, annual_gain - 2500000.0)
            tax_amount = taxable_gain * 0.22
            
            end_balance_after_tax = end_balance_pre_tax - tax_amount
            current_balance = end_balance_after_tax
            
            dca_results[y] = {
                "cum_deposited_krw": cum_deposited_krw,
                "start_balance_krw": round(year_start_balance),
                "kis_net_return_pct": kis_net_ret,
                "end_balance_pre_tax_krw": round(end_balance_pre_tax),
                "annual_gain_krw": round(annual_gain),
                "tax_amount_krw": round(tax_amount),
                "end_balance_after_tax_krw": round(end_balance_after_tax),
                "after_tax_gain_krw": round(end_balance_after_tax - cum_deposited_krw),
                "cum_return_on_deposited_pct": round(((end_balance_after_tax - cum_deposited_krw) / cum_deposited_krw) * 100.0, 2) if cum_deposited_krw > 0 else 0.0,
                "benchmark_return_pct": spy_ret
            }
            
        return dca_results








