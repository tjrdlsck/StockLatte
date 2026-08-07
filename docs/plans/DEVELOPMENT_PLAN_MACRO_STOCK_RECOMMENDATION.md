# 📋 [StockLatte] 중장기 우량주 거시적 스마트 리밸런싱 시스템 상세 개발 계획서

> **작성일자:** 2026년 7월 22일  
> **작성자:** StockLatte 개발 팀  
> **관련 제안서:** [MACRO_STOCK_RECOMMENDATION_PROPOSAL.md](../proposals/MACRO_STOCK_RECOMMENDATION_PROPOSAL.md)  
> **목적:** 중장기 우량주 자산배분 포트폴리오의 평가 금액(Market Value) 기준 비중 산출, 비중 쏠림 감지, Sell High & Buy Low 스마트 리밸런싱 계산 엔진 및 LLM 프롬프트 주입 모듈 구현계획

---

## 1. 🎯 프로젝트 목표 및 시스템 개요

본 개발 계획서는 단타 매매를 배제하고, **현재 평가 금액(Current Market Value)**을 기준으로 주식 비중을 산출하여 폭등한 우량주의 이익금 일부를 차익 실현(Sell High)하고 저평가된 우량주를 저점 매수(Buy Low)하는 **자동 포트폴리오 스마트 리밸런싱 계산 엔진**의 구현을 목적으로 합니다.

### 1.1 핵심 기능 요구사항
1. **평가 금액 기반 비중 계산 엔진 (Market Value Calculation Engine):**
   - 개별 종목 평가 금액: $\text{Current Market Value} = \text{보유 수량} \times \text{현재 주가}$
   - 포트폴리오 총 평가 금액: $\text{Total Portfolio Value} = \sum (\text{개별 종목 평가 금액}) + \text{보유 현금}$
   - 종목별 비중 수식:
     $$\text{Weight}_i (\%) = \left( \frac{\text{Market Value}_i}{\text{Total Portfolio Value}} \right) \times 100$$
2. **비중 쏠림 경보 (Overweight Shift Alert Sensor):**
   - 목표 비중 대비 이탈율 감지 또는 특정 종목 비중 임계값(기본 35% 이상) 초과 시 경고 시그널 발생.
3. **스마트 리밸런싱 실행 플랜 산출 (Sell High & Buy Low Optimizer):**
   - 폭등 종목의 이익금 차익 실현 목표 금액 계산:
     $$\text{Sell Amount}_i = \text{Current Market Value}_i - (\text{Total Portfolio Value} \times \text{Target Weight}_i)$$
   - 저평가 종목의 추가 매수 목표 금액 계산:
     $$\text{Buy Amount}_j = (\text{Total Portfolio Value} \times \text{Target Weight}_j) - \text{Current Market Value}_j$$
4. **LLM Context JSON Generator:**
   - Gemini / Claude 등 메인 LLM에 주입 가능한 표준화된 JSON 리밸런싱 실행 프롬프트 데이터 생성.
5. **데이터 파이프라인 연동 (`yfinance`):**
   - 실시간 또는 지연 주가 수집 및 오프라인/테스트 모킹 지원.

---

## 2. 🏛️ 시스템 아키텍처 및 모듈 구조

```
StockLatte/
├── stocklatte/                    # 메인 소스코드 패키지
│   ├── __init__.py
│   ├── models.py                  # 포지션, 포트폴리오, 리밸런싱 결과 데이터 클래스
│   ├── rebalancing.py             # 스마트 리밸런싱 계산 엔진 핵심 로직
│   └── data_provider.py           # yfinance 주가 수집 및 데이터 제공 모듈
├── docs/
│   ├── proposals/
│   │   └── MACRO_STOCK_RECOMMENDATION_PROPOSAL.md
│   └── plans/
│       └── DEVELOPMENT_PLAN_MACRO_STOCK_RECOMMENDATION.md
├── tests/
│   ├── test_environment.py
│   └── test_rebalancing.py        # 스마트 리밸런싱 검증 테스트
├── .gitignore
├── .ignore
└── requirements.txt
```

---

## 3. 📊 상세 데이터 모델 및 수학적 알고리즘 설계

### 3.1 데이터 모델 구조 (`models.py`)

* **`Position`**: 개별 주식 포지션 데이터 클래스 (티커, 수량, 현재가, 평가금액, 현재비중)
* **`Portfolio`**: 전체 포트폴리오 데이터 클래스 (포지션 목록, 보유 현금, 총 평가 자산, 목표 비중 Dict)
* **`RebalanceAction`**: 리밸런싱 작업 정보 클래스 (작업 구분 `SELL`/`BUY`, 티커, 금액, 예상 수량)
* **`RebalanceResult`**: 리밸런싱 최종 결과 및 LLM 프롬프트 JSON 변환 인터페이스

### 3.2 리밸런싱 계산 알고리즘

수식에 따른 리밸런싱 계산 절차:

1. 총 자산 평가액 계산:
   $$V_{\text{total}} = \sum_{i=1}^{N} (S_i \times P_i) + C$$
   *(단, $S_i$는 보유 수량, $P_i$는 현재 주가, $C$는 보유 현금)*

2. 각 종목 $i$의 목표 평가액($V_{\text{target}, i}$) 계산:
   $$V_{\text{target}, i} = V_{\text{total}} \times W_{\text{target}, i}$$

3. 조정 금액 $\Delta V_i$ 산출:
   $$\Delta V_i = V_{\text{target}, i} - V_{\text{current}, i}$$
   - $\Delta V_i < 0$: $\lvert \Delta V_i \rvert$ 만큼 차익 실현 (Sell High)
   - $\Delta V_i > 0$: $\Delta V_i$ 만큼 추가 매수 (Buy Low)

---

## 4. 🗓️ 단계별 개발 마일스톤 (Milestones)

| 단계 | 작업 내용 | 상세 설명 | 완료 기준 |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **모듈 구조 및 데이터 클래스 정의** | `stocklatte/models.py` 구현 | 데이터 클래스 및 JSON 직렬화 지원 |
| **Phase 2** | **스마트 리밸런싱 엔진 구현** | `stocklatte/rebalancing.py` 구현 | 비중 산출, 쏠림 감지, 매도/매수 금액 계산 |
| **Phase 3** | **주가 데이터 수집기 연동** | `stocklatte/data_provider.py` 구현 | yfinance 연동 및 테스트용 오프라인 Mock 데이터 지원 |
| **Phase 4** | **단위 테스트 & 검증** | `tests/test_rebalancing.py` 구현 | 예시 시나리오(NVDA/MSFT/CAT) 100% 매칭 검증 |
| **Phase 5** | **검증 및 커밋/푸시** | 기존 코드 비교, pytest 테스트 및 푸시 | CI/CD 준비 완료 및 `feat/#3` 푸시 |

---

## 5. 🧪 테스트 및 검증 전략

1. **단위 테스트 (`tests/test_rebalancing.py`):**
   - 제안서 2.1절의 수치 예시 검증:
     - 초기: NVDA $3,000(30%), MSFT $3,000(30%), CAT $4,000(40%) [총 $10,000]
     - 6개월 후 NVDA 폭등: NVDA $7,500(50%), MSFT $3,500(23.3%), CAT $4,000(26.7%) [총 $15,000]
     - 쏠림 감지: NVDA 50% 쏠림 경보 확인
     - 리밸런싱 산출: NVDA $3,000 매도, MSFT $1,000 매수, CAT $2,000 매수 결과 정확히 검증
   - 단주 처리 및 현금 포함 포트폴리오 리밸런싱 정밀도 검증
2. **LLM Context JSON 검증:**
   - JSON 포맷 일치 및 예외 처리 검증
3. **규칙 준수 검증:**
   - `.gitignore` (`test_results/`, `venv/` 등) 적용 여부 확인
   - 최소한의 코드 수정으로 최고 효율성 확보

---

## 6. 📚 참고 문헌 (References)
- [StockLatte 거시적 주식 추천 제안서](../proposals/MACRO_STOCK_RECOMMENDATION_PROPOSAL.md)
- [yfinance API Documentation](https://pypi.org/project/yfinance/)
