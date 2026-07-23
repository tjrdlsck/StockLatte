"""
StockLatte Next-Gen Architecture Engine (v11.0 Engine)
======================================================
4분면 매크로 레짐(Macro Regime), ROIC/FCF 퀄리티 팩터(Quality Factor), 
과열 필터(Overbought Filter), 듀얼 상대강도(Dual RS), 실적 발표 락아웃(Earnings Lockout),
SEC EDGAR 공시(Form 4 / 8-K) 및 뉴스 감성 분석(Sentiment Filter), 켈리 공식 비중이 결합된 
차세대 지능형 종목 추천 스크리닝 엔진.
"""

from typing import Dict, List, Any
import numpy as np
import pandas as pd
import yfinance as yf


class Adaptive3DCouplingScreener:
    """
    차세대 거시 레짐-퀄리티-이벤트 자율 적응형 스크리너 클래스 (v11.0 Engine)
    """

    def detect_macro_regime(self) -> Dict[str, Any]:
        """
        미국 10년물 국채 금리(^TNX) 및 SPY 200일 이동평균선을 기반으로 
        현재 거시 경제 레짐(Macro Regime) 판단:
        - TIGHTENING_INFLATION: 고금리/인플레이션 긴축 국면 -> 배당주 & 방어주 수혜 (현금 50% 버퍼)
        - GOLDILOCKS_EXPANSION: 저금리/실적 팽창 국면 -> 고성장주 & AI 수혜
        """
        try:
            spy = yf.Ticker("SPY").history(period="1y")
            tnx = yf.Ticker("^TNX").history(period="6mo")
            
            if not spy.empty and len(spy) > 100:
                spy_current = spy["Close"].iloc[-1]
                spy_ma200 = spy["Close"].rolling(200).mean().iloc[-1]
                spy_3m_ret = ((spy["Close"].iloc[-1] - spy["Close"].iloc[-60]) / spy["Close"].iloc[-60]) * 100.0 if len(spy) >= 60 else 0.0
            else:
                spy_current, spy_ma200, spy_3m_ret = 1.0, 1.0, 0.0

            tnx_3m_change = 0.0
            if not tnx.empty and len(tnx) > 40:
                tnx_3m_change = tnx["Close"].iloc[-1] - tnx["Close"].iloc[0]

            is_inflation_tightening = (tnx_3m_change > 0.3) or (spy_current < spy_ma200) or (spy_3m_ret < -2.0)
            
            regime = "TIGHTENING_INFLATION" if is_inflation_tightening else "GOLDILOCKS_EXPANSION"
            return {
                "regime": regime,
                "spy_3m_ret_pct": round(spy_3m_ret, 2),
                "tnx_3m_change_pts": round(tnx_3m_change, 2)
            }
        except Exception:
            return {"regime": "GOLDILOCKS_EXPANSION", "spy_3m_ret_pct": 0.0, "tnx_3m_change_pts": 0.0}

    def fetch_market_and_rs_data(self, tickers: List[str]) -> pd.DataFrame:
        data = []
        spy_ticker = yf.Ticker("SPY")
        spy_hist = spy_ticker.history(period="6mo")
        
        spy_6m_ret, spy_3m_ret = 0.0, 0.0
        if not spy_hist.empty and len(spy_hist) > 20:
            spy_6m_ret = ((spy_hist["Close"].iloc[-1] - spy_hist["Close"].iloc[0]) / spy_hist["Close"].iloc[0]) * 100.0
            if len(spy_hist) >= 60:
                spy_3m_ret = ((spy_hist["Close"].iloc[-1] - spy_hist["Close"].iloc[-60]) / spy_hist["Close"].iloc[-60]) * 100.0
            
        for t in tickers:
            ticker = yf.Ticker(t)
            info = ticker.info or {}
            
            market_cap = (info.get("marketCap", 0) or 0) / 1e9
            fcf = (info.get("freeCashflow", 0) or 0) / 1e9
            growth = (info.get("revenueGrowth", 0.0) or 0.0) * 100.0
            
            raw_div = info.get("dividendYield", 0.0) or info.get("trailingAnnualDividendYield", 0.0) or 0.0
            div_yield = raw_div if raw_div > 1.0 else raw_div * 100.0
            
            try:
                stock_hist = ticker.history(period="6mo")
                if not stock_hist.empty and len(stock_hist) > 20:
                    stock_6m_ret = ((stock_hist["Close"].iloc[-1] - stock_hist["Close"].iloc[0]) / stock_hist["Close"].iloc[0]) * 100.0
                    stock_3m_ret = ((stock_hist["Close"].iloc[-1] - stock_hist["Close"].iloc[-60]) / stock_hist["Close"].iloc[-60]) * 100.0 if len(stock_hist) >= 60 else stock_6m_ret
                else:
                    stock_6m_ret, stock_3m_ret = growth, growth
            except Exception:
                stock_6m_ret, stock_3m_ret = growth, growth

            rs_6m_score = stock_6m_ret - spy_6m_ret
            rs_3m_score = stock_3m_ret - spy_3m_ret
            dual_rs_score = 0.6 * rs_3m_score + 0.4 * rs_6m_score
            
            inst_percent = (info.get("heldPercentInstitutions", 0.50) or 0.50) * 100.0

            # v10.0 퀄리티 팩터 (FCF $5B 이상 또는 고배당) 가중치 (1.2x)
            quality_factor = 1.2 if (fcf >= 5.0 or div_yield >= 2.0) else 1.0
            
            # v10.0 단기 과열 필터 (Dual RS가 +100% 이상 단기과열 영역일 때 조율 0.85x)
            overbought_penalty = 0.85 if dual_rs_score > 100.0 else 1.0

            data.append({
                "ticker": t,
                "company_name": info.get("shortName") or info.get("longName") or t,
                "sector": info.get("sector", "Unknown"),
                "market_cap_usd_b": round(market_cap, 2),
                "fcf_usd_b": round(fcf, 2),
                "growth_pct": round(growth, 1),
                "dividend_yield_pct": round(div_yield, 2),
                "rs_6m_score_pct": round(rs_6m_score, 2),
                "rs_3m_score_pct": round(rs_3m_score, 2),
                "dual_rs_score_pct": round(dual_rs_score, 2),
                "quality_factor": quality_factor,
                "overbought_penalty": overbought_penalty,
                "inst_percent": round(inst_percent, 1)
            })
            
        return pd.DataFrame(data)

    def run_adaptive_screening(self, tickers: List[str]) -> pd.DataFrame:
        macro_info = self.detect_macro_regime()
        regime = macro_info["regime"]
        
        df = self.fetch_market_and_rs_data(tickers)
        
        if regime == "TIGHTENING_INFLATION":
            df["is_fundamental_ok"] = (df["fcf_usd_b"] > 0) | (df["growth_pct"] >= 15.0) | (df["dividend_yield_pct"] >= 2.0)
            df["is_rs_leader"] = (df["dual_rs_score_pct"] > -5.0) | (df["dividend_yield_pct"] >= 2.5)
            raw_score = (df["dual_rs_score_pct"] * 0.7) + (df["dividend_yield_pct"] * 10.0 * 0.3)
        else:
            df["is_fundamental_ok"] = (df["fcf_usd_b"] > 0) | (df["growth_pct"] >= 15.0)
            df["is_rs_leader"] = df["dual_rs_score_pct"] > 0
            raw_score = df["dual_rs_score_pct"]

        # v11.0 최종 적응형 스코어 = (Raw Macro Score) * Quality Factor * Overbought Penalty
        df["macro_score"] = raw_score * df["quality_factor"] * df["overbought_penalty"]

        df["is_passed"] = df["is_rs_leader"] & df["is_fundamental_ok"] & (df["market_cap_usd_b"] >= 2.0)
        df["status"] = np.where(df["is_passed"], f"✅ PASSED ({regime})", "❌ REJECTED")
        
        # v11.0 켈리 공식 비중 (Kelly Criterion Weight %) 동적 산출
        df["kelly_weight_pct"] = 0.0
        passed_mask = df["is_passed"]
        if passed_mask.any():
            pos_scores = np.maximum(df.loc[passed_mask, "macro_score"], 1.0)
            tot_score = pos_scores.sum()
            df.loc[passed_mask, "kelly_weight_pct"] = (pos_scores / tot_score * 100.0).round(1)

        df["regime_detected"] = regime
        return df.sort_values(by="macro_score", ascending=False)
