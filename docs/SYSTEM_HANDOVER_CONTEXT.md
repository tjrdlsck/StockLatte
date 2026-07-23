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
  4. **브랜치 전략**: **무시** (사용자 지시대로 현재 브랜치에서 다이렉트 수정 및 작업 반영).
  5. **테스트 및 파일 관리**:
     - `tests/`: 유닛 테스트 스크립트 보관 (Git 커밋 대상)
     - `test_results/`: 실행 결과 로그 보관 (`test_results/test_screener.log`)
     - `.gitignore`: `venv/`, `__pycache__/`, `.env`, `test_results/` 예외 처리 완료.

---

## 2. 🧠 구축된 핵심 엔진 및 파이프라인 (System Architecture)

### 2.1 v11.0 차세대 지능형 적응형 스크리너 (v11.0 Engine)
- **위치**: [stocklatte/screener.py](file:///C:/cli-develop/StockLatte/stocklatte/screener.py)
- **5대 메커니즘**:
  1. 4분면 매크로 레짐 자동 판단 (`detect_macro_regime`).
  2. ROIC/FCF 퀄리티 팩터 ($1.2\times$ 프리미엄) 적용.
  3. 단기 과열 상투 필터 ($Dual\_RS > 100\%$ 시 $0.85\times$ 페널티).
  4. 실적 발표 락아웃 & SEC Form 4/8-K & 뉴스 감성 분석 필터.
  5. 켈리 공식(Kelly Criterion) 포트폴리오 비중 % 자동 산출.

### 2.2 Point-in-Time 롤링 & 세후 복리 백테스터 (v11.0 Engine)
- **위치**: [stocklatte/backtest.py](file:///C:/cli-develop/StockLatte/stocklatte/backtest.py)
- **4년 실측 세후 성과 (2022 ~ 2025)**:
  - **원금 200만 원 일시불**: 세후 누적 수익률 **+167.70%** (세후 자산 535만 원, 세금 0원)
  - **원금 1,000만 원 일시불**: 세후 누적 수익률 **+143.19%** (세후 자산 2,431만 원, 세금 203만 원 납부 후)
  - **매월 30만 원 적립식 (DCA)**: 세후 누적 수익률 **+88.37%** (불입 원금 1,440만 원 ➡️ 세후 자산 2,712만 원)

### 2.3 전략 보고서 & 제안서
- **전략 최종 보고서**: [docs/STRATEGY_AUDIT_REPORT.md](file:///C:/cli-develop/StockLatte/docs/STRATEGY_AUDIT_REPORT.md)
- **시스템 제안서**: [docs/USA_STOCK_RECOMMENDATION_PROPOSAL.md](file:///C:/cli-develop/StockLatte/docs/USA_STOCK_RECOMMENDATION_PROPOSAL.md)

---

## 3. 🧪 작업 방식 및 테스트 실행 명령 (Execution Protocol)

```powershell
# 가상환경 파이썬 기반 pytest v11.0 통합 백테스트 실행
.\venv\Scripts\python.exe -m pytest tests/test_screener.py -v -s
```

- **테스트 파일**: [tests/test_screener.py](file:///C:/cli-develop/StockLatte/tests/test_screener.py)
- **로그 결과**: [test_results/test_screener.log](file:///C:/cli-develop/StockLatte/test_results/test_screener.log)
