"""
StockLatte v10.0 Next-Gen Screener & PIT Rolling Backtest Unit Test
===================================================================
v10.0 차세대 적응형 엔진 (ROIC/FCF 퀄리티 + 과열 필터 + 듀얼 RS + 켈리 비중) 및 
Point-in-Time 미래 데이터 편향 차단 4년 시계열 롤링 백테스트 표준 유닛 테스트.
"""

import os
import sys
import logging
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from stocklatte.screener import Adaptive3DCouplingScreener
from stocklatte.backtest import FullCycleBacktester, PointInTimeBacktester


def setup_logger():
    results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test_results"))
    os.makedirs(results_dir, exist_ok=True)
    log_file_path = os.path.join(results_dir, "test_screener.log")
    
    logger = logging.getLogger("StockLatteV10Test")
    logger.setLevel(logging.INFO)
    if logger.hasHandlers():
        logger.handlers.clear()
        
    file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger, log_file_path


def test_v10_screener_and_full_audit_backtest():
    logger, log_file_path = setup_logger()
    logger.info("=== StockLatte v10.0 차세대 스크리너 & 4년 연속 시계열 통합 백테스트 시작 ===")
    
    ticker_universe_20 = [
        "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "PLTR",
        "AMD", "AVGO", "JPM", "JNJ", "V", "PG", "COST", "WMT", "CVX",
        "XOM", "MO", "SCHD"
    ]
    
    # 1. v10.0 차세대 스크리닝 집행
    screener = Adaptive3DCouplingScreener()
    macro_info = screener.detect_macro_regime()
    logger.info(f" 🌐 감지된 현재 거시 레짐: {macro_info['regime']} (SPY 3M: {macro_info['spy_3m_ret_pct']}%)")
    
    df_results = screener.run_adaptive_screening(ticker_universe_20)
    logger.info("\n" + "="*95)
    logger.info(" [ v10.0 차세대 스크리너 상위 추천 종목 및 켈리 비중 리포트 ]")
    logger.info("="*95)
    
    for idx, row in df_results.head(8).iterrows():
        logger.info(f" [{row['ticker']:6s}] {row['company_name'][:18]:18s} | 퀄리티: {row['quality_factor']}x | Dual RS: {row['dual_rs_score_pct']:+6.2f}% | 최종점수: {row['macro_score']:+6.2f} | 켈리권장비중: {row['kelly_weight_pct']:5.1f}%")
        
    # 2. Point-in-Time 롤링 백테스트 집행 (2022 ~ 2025)
    pit_backtester = PointInTimeBacktester(ticker_universe=ticker_universe_20)
    audit_results = pit_backtester.run_audited_semiannual_and_annual_backtest(years=[2022, 2023, 2024, 2025])
    
    logger.info("\n" + "="*95)
    logger.info(" [ 과거 4년(2022~2025) Point-in-Time 시계열 검증 최종 종합 리포트 ]")
    logger.info("="*95)
    
    for year, data in audit_results.items():
        logger.info(f" 📅 [{year}년도] 포트폴리오: {data['annual_portfolio_return_pct']:+8.2f}% | SPY 벤치마크: {data['annual_benchmark_return_pct']:+8.2f}% | Alpha: {data['annual_alpha_pct']:+8.2f}%p")
        
    logger.info("="*95)
    
    assert len(df_results) > 0
    assert len(audit_results) == 4
    assert os.path.exists(log_file_path)


if __name__ == "__main__":
    test_v10_screener_and_full_audit_backtest()
