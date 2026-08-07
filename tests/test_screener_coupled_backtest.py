import os
import sys
import unittest

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from stocklatte.backtest import PointInTimeBacktester, FullCycleBacktester
from stocklatte.screener import Adaptive3DCouplingScreener


class TestScreenerCoupledBacktest(unittest.TestCase):

    def test_screener_as_of_date_execution(self):
        """
        과거 시점(as_of_date)을 기준으로 라이브 스크리너(Adaptive3DCouplingScreener)가 
        정상 동작하여 레짐을 판단하고 스크리닝 결과 및 비중(score_weight_pct)을 반환하는지 테스트
        """
        screener = Adaptive3DCouplingScreener()
        ticker_universe = ["NVDA", "MSFT", "AAPL", "AMZN", "GOOGL", "META", "TSLA", "AMD"]
        
        as_of_date = "2024-01-01"
        df_result = screener.run_adaptive_screening(ticker_universe, as_of_date=as_of_date)
        
        self.assertFalse(df_result.empty, "스크리닝 결과가 비어있지 않아야 합니다.")
        self.assertIn("regime_detected", df_result.columns, "레짐 탐지 결과가 포함되어야 합니다.")
        self.assertIn("score_weight_pct", df_result.columns, "점수 비례 비중이 포함되어야 합니다.")
        self.assertIn("macro_score", df_result.columns, "적응형 매크로 스코어가 포함되어야 합니다.")
        print(f"\n[PASS] test_screener_as_of_date_execution: Detected Regime={df_result['regime_detected'].iloc[0]}")

    def test_screener_coupled_pit_backtest_execution(self):
        """
        PointInTimeBacktester에서 라이브 스크리너가 100% 동일하게 이식된 
        run_screener_coupled_pit_backtest()가 정상 수행되는지 검증
        """
        ticker_universe = ["NVDA", "MSFT", "AAPL", "AMZN", "GOOGL", "META", "TSLA", "AMD"]
        pit_backtester = PointInTimeBacktester(ticker_universe=ticker_universe)
        
        # 최근 연도(2024)에 대해 백테스트 수행
        results = pit_backtester.run_screener_coupled_pit_backtest(years=[2024], use_score_weights=True)
        
        self.assertIn("total_portfolio_return_pct", results, "총 포트폴리오 수익률 결과가 포함되어야 합니다.")
        self.assertIn("total_benchmark_return_pct", results, "총 벤치마크 수익률 결과가 포함되어야 합니다.")
        self.assertIn("portfolio_cagr_pct", results, "CAGR 결과가 포함되어야 합니다.")
        self.assertIn("yearly_quarterly_results", results, "연도별 분기 실적이 포함되어야 합니다.")
        
        yearly_res = results["yearly_quarterly_results"]
        self.assertIn(2024, yearly_res, "2024년 결과가 존재해야 합니다.")
        self.assertIn("selected_tickers_by_quarter", yearly_res[2024], "분기별 종목 선택 결과가 존재해야 합니다.")
        self.assertIn("weights_by_quarter", yearly_res[2024], "분기별 종목 비중 결과가 존재해야 합니다.")
        
        print(f"[PASS] test_screener_coupled_pit_backtest_execution: 2024 Total Return={results['total_portfolio_return_pct']}%, Benchmark={results['total_benchmark_return_pct']}%")


if __name__ == "__main__":
    unittest.main()
