# 🔄 Quick Handover Guide for Next Session

다음 세션에서 AI가 기억을 리셋하더라도 본 프로젝트의 전체 맥락, 사용자 규칙, 엔진 아키텍처, 작업 방식을 즉시 복원할 수 있도록 작성된 요약 문서입니다.

상세 핸드오버 문서: [docs/SYSTEM_HANDOVER_CONTEXT.md](file:///C:/cli-develop/StockLatte/docs/SYSTEM_HANDOVER_CONTEXT.md)  
상세 시스템 제안서: [docs/USA_STOCK_RECOMMENDATION_PROPOSAL.md](file:///C:/cli-develop/StockLatte/docs/USA_STOCK_RECOMMENDATION_PROPOSAL.md)  
최종 전략 검증 보고서: [docs/STRATEGY_AUDIT_REPORT.md](file:///C:/cli-develop/StockLatte/docs/STRATEGY_AUDIT_REPORT.md)

---

## ⚡ 1줄 요약 복원 패키지

- **프로젝트**: StockLatte Auto-Pilot (미국 주식 자동 모니터링 & 추천 시스템)
- **핵심 알고리즘 (v11.0 Engine)**: 4분면 매크로 레짐, 상대적 FCF Margin/성장률 퀄리티 팩터(1.2x), 단기 과열 필터(0.85x), 듀얼 RS, 점수 비례 포트폴리오 비중 산출 엔진 ([stocklatte/screener.py](file:///C:/cli-develop/StockLatte/stocklatte/screener.py))
- **스마트 리밸런싱 엔진**: 신규 매수 티커 포함 full universe 순회, 허용 밴드(rebalance_band_pct) 적용, 비중 쏠림 경보 및 LLM JSON 변환 ([stocklatte/rebalancing.py](file:///C:/cli-develop/StockLatte/stocklatte/rebalancing.py))
- **백테스트 엔진**: 수동 알파/가상 성과 가산치 100% 제거, Look-ahead Bias 차단 Point-in-Time 롤링, 한국투자증권 수수료/환전비용 & 22% 해외주식 양도소득세 세후 복리 백테스터 ([stocklatte/backtest.py](file:///C:/cli-develop/StockLatte/stocklatte/backtest.py))
- **사용자 규칙**:
  1. 한국어 + CS/AI 교수 페르소나 (체계적, 전문적, 기술 용어 영문 괄호 병기, LaTeX 수식 사용).
  2. 테스트 규칙: `tests/`에 테스트 코드 작성, `test_results/test_screener.log`에 로그 저장.
- **실행 명령**:
  `.\venv\Scripts\python.exe -m pytest tests/test_screener.py -v -s`

