"""
StockLatte v11.0 Next-Gen Screener & Full Audit Unit Test
=========================================================
v11.0 차세대 적응형 스크리닝 엔진 (매크로 레짐 + ROIC/FCF 퀄리티 + 과열 필터 + 듀얼 RS + 켈리 비중) 및 
Point-in-Time 미래 데이터 편향 차단 4년 시계열 롤링, 어닝 디리스킹, 
한국투자증권(KIS) 실측 수수료 및 22% 해외주식 양도소득세 세후 복리 백테스트 표준 유닛 테스트.
"""

import os
import sys
import logging
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from stocklatte.screener import Adaptive3DCouplingScreener
from stocklatte.backtest import PointInTimeBacktester


def setup_logger():
    results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test_results"))
    os.makedirs(results_dir, exist_ok=True)
    log_file_path = os.path.join(results_dir, "test_screener.log")
    
    logger = logging.getLogger("StockLatteV11Test")
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


def test_v11_screener_and_full_audit_backtest():
    logger, log_file_path = setup_logger()
    logger.info("=== StockLatte v11.0 차세대 스크리너 & 한국 세후 복리 통합 실측 백테스트 시작 ===")
    
    ticker_universe_20 = [
        "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "PLTR",
        "AMD", "AVGO", "JPM", "JNJ", "V", "PG", "COST", "WMT", "CVX",
        "XOM", "MO", "SCHD"
    ]
    
    # 1. v11.0 차세대 스크리닝 집행
    screener = Adaptive3DCouplingScreener()
    macro_info = screener.detect_macro_regime()
    logger.info(f" 🌐 감지된 현재 거시 레짐: {macro_info['regime']} (SPY 3M: {macro_info['spy_3m_ret_pct']}%)")
    
    df_results = screener.run_adaptive_screening(ticker_universe_20)
    logger.info("\n" + "="*95)
    logger.info(" [ v11.0 차세대 스크리너 상위 추천 종목 및 켈리 비중 리포트 ]")
    logger.info("="*95)
    
    for idx, row in df_results.head(8).iterrows():
        logger.info(f" [{row['ticker']:6s}] {row['company_name'][:18]:18s} | 퀄리티: {row['quality_factor']}x | Dual RS: {row['dual_rs_score_pct']:+6.2f}% | 최종점수: {row['macro_score']:+6.2f} | 켈리권장비중: {row['kelly_weight_pct']:5.1f}%")
        
    # 2. 한국투자증권 수수료 & 세후(22%) 원금 1,000만 원 백테스트 집행
    pit_backtester = PointInTimeBacktester(ticker_universe=ticker_universe_20)
    tax_10m_results = pit_backtester.run_kis_korean_tax_audited_backtest(initial_seed_krw=10000000, years=[2022, 2023, 2024, 2025])
    
    logger.info("\n" + "="*95)
    logger.info(" [ 원금 1,000만 원 시작 - 한투 수수료 & 22% 세후 복리 백테스트 리포트 ]")
    logger.info("="*95)
    for year, data in tax_10m_results.items():
        logger.info(f" 📅 [{year}년도] 기초원금: {data['start_balance_krw']:,}원 | 세후최종자산: {data['end_balance_after_tax_krw']:,}원 | 세후수익률: {data['cum_return_after_tax_pct']:+8.2f}% | 양도세: {data['tax_amount_krw']:,}원")

    # 3. 매월 30만 원 적립식(DCA) 세후 복리 백테스트 집행
    dca_results = pit_backtester.run_monthly_dca_korean_tax_backtest(monthly_deposit_krw=300000, years=[2022, 2023, 2024, 2025])
    
    logger.info("\n" + "="*95)
    logger.info(" [ 매월 30만 원 적립식 투입 - 한투 수수료 & 22% 세후 복리 백테스트 리포트 ]")
    logger.info("="*95)
    for year, data in dca_results.items():
        logger.info(f" 📅 [{year}년도] 누적불입원금: {data['cum_deposited_krw']:,}원 | 세후최종자산: {data['end_balance_after_tax_krw']:,}원 | 세후수익률: {data['cum_return_on_deposited_pct']:+8.2f}% | 양도세: {data['tax_amount_krw']:,}원")
        
    logger.info("="*95)
    
    assert len(df_results) > 0
    assert len(tax_10m_results) == 4
    assert len(dca_results) == 4
    assert os.path.exists(log_file_path)


if __name__ == "__main__":
    test_v11_screener_and_full_audit_backtest()
