# 🔄 StockLatte System Context Handover Document (상태 복원 핸드오버 문서)
> **Purpose**: 대화 세션 리셋 후에도 이전의 작업 맥락, 엔진 구조, 실행 방식, 사용자 규칙을 토큰 최적화 상태로 100% 복원하기 위한 가이드.

---

## 1. 📌 프로젝트 개요 및 핵심 원칙 (Project Core)
- **프로젝트명**: StockLatte Auto-Pilot (미국 주식 자동 모니터링 & 매매 추천 시스템)
- **주요 목표**: 게으른 투자자를 위한 최소 개입 미국 주식 매도 타이밍 포착 및 올웨더 종목 추천
- **사용자 필수 규칙 (User Rules & Preferences)**:
  1. **언어/페르소나**: 한국어(Korean), CS/AI 최고 전문가 & 교수 톤 (체계적, 깊이 있는 강의 스타일).
  2. **기술 용어**: 처음 등장 시 영문 괄호 병기 (예: 상대강도 지수 `Relative Strength, RS`).
  3. **수식 표기**: LaTeX 사용 ($...$ 또는 $$...$$).
  4. **테스트 및 파일 관리**:
     - `tests/`: 유닛 테스트 스크립트 보관 (Git 커밋 대상)
     - `test_results/`: 실행 결과 로그 보관 (`test_results/test_screener.log`)
     - `.gitignore`: `venv/`, `__pycache__/`, `.env`, `test_results/` 예외 처리 완료.

---

## 2. 🧠 구축된 핵심 엔진 및 파이프라인 (System Architecture)

### 2.1 v11.0 차세대 지능형 적응형 스크리너 (v11.0 Engine)
- **위치**: [stocklatte/screener.py](file:///C:/cli-develop/StockLatte/stocklatte/screener.py)
- **핵심 메커니즘**:
  1. 4분면 매크로 레짐 판단 (`detect_macro_regime`).
  2. 상대적 FCF Margin ($10\%$ 이상) & 성장성 기반 퀄리티 팩터 ($1.2\times$ 가중치) 적용.
  3. 단기 과열 상투 필터 ($Dual\_RS > 100\%$ 시 $0.85\times$ 페널티).
  4. 점수 비례 포트폴리오 비중 (`score_weight_pct`) 산출 엔진.

### 2.2 스마트 평가 금액 리밸런싱 엔진
- **위치**: [stocklatte/rebalancing.py](file:///C:/cli-develop/StockLatte/stocklatte/rebalancing.py)
- **주요 개선**:
  - 목표 비중(Target Weights) 및 현재 포지션 전체 유니버스 순회로 신규 매수(`BUY`) 종목 완벽 처리.
  - 리밸런싱 허용 밴드(`rebalance_band_pct: 1.0%p`) 적용으로 미세 비중 변화로 인한 불필요한 고비용 거래 차단.
  - LLM 주입용 JSON 컨텍스트 변환 시 전체 보유 종목과 경고 종목을 명확히 분리하여 전달.

### 2.3 무편향 Point-in-Time 롤링 & 세후 복리 백테스터 (Backtester)
- **위치**: [stocklatte/backtest.py](file:///C:/cli-develop/StockLatte/stocklatte/backtest.py)
- **주요 개선**:
  - **가상 성과 가산치(+2.2%p 등) 및 연도별 조건문 하드코딩 100% 제거**: 과거 실측 시세 데이터를 기반으로 순수 계산.
  - Look-ahead Bias 차단 Point-in-Time 롤링 백테스팅.
  - 한국투자증권 수수료/환전비용 및 해외주식 22% 양도소득세 세후 복리 평가.

---

## 3. 🧪 작업 방식 및 테스트 실행 명령 (Execution Protocol)

```powershell
# 가상환경 파이썬 기반 pytest 통합 테스트 실행
.\venv\Scripts\python.exe -m pytest tests/test_screener.py -v -s
```

- **테스트 파일**: [tests/test_screener.py](file:///C:/cli-develop/StockLatte/tests/test_screener.py)
- **로그 결과**: [test_results/test_screener.log](file:///C:/cli-develop/StockLatte/test_results/test_screener.log)

