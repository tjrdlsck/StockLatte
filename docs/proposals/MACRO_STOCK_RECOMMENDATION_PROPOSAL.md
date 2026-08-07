# 📈 [StockLatte] 중장기 우량주 자산배분 & 거시적 리밸런싱 관리 기반 미국 주식 시스템 상세 설계서

> **작성일자:** 2026년 7월 22일 (현재 평가 금액 기반 스마트 리밸런싱 메커니즘 최종 완비)  
> **작성자:** 글로벌 미국 주식 수석 트레이더 & AI 시스템 아키텍트  
> **문서 목적:** 잦은 단타 매매를 배제하고, **현재 평가 금액(Current Market Value) 기준**으로 싸게 사서 대폭등한 우량주의 이익금 일부를 차익 실현(Sell High)하여 상대적으로 저평가된 다른 섹터 1등 우량주를 저점 매수(Buy Low)하는 **자동 포트폴리오 스마트 리밸런싱 계산 엔진**을 탑재한 미국 주식 자산관리 서비스 구축  

---

## 1. 🎯 프로젝트 개요 및 평가 금액 기반 리밸런싱 원리

### 1.1 "평가 금액 기반 비중 산출 & Sell High, Buy Low 리밸런싱" 원리
* **비중 계산 방식 (Market Value Based Weighting):** 포트폴리오 비중은 최초 매수가(평단가)가 아닌 **'현재 평가 금액 (보유 수량 $\times$ 현재 주가)'**을 기준으로 계산됩니다.
  $$\text{종목별 비중 (\%)} = \left( \frac{\text{개별 종목 현재 평가 금액}}{\text{포트폴리오 총 평가 금액}} \right) \times 100$$
* **"싸게 샀던 주식이 폭등하면 리밸런싱을 한다"의 핵심 원리:**
  - 싸게 산 우량주(예: Nvidia)가 2~3배 폭등하여 계좌 비중의 40~50% 이상을 차지하게 되면, 특정 종목에 리스크가 과도하게 쏠립니다.
  - 이때 리밸런싱은 **원금은 그대로 둔 채 폭등한 이익금 일부만 차익 실현(Sell High)**하여, 상대적으로 덜 오르거나 저평가된 타 섹터 1등 우량주를 추가 매수(Buy Low)함으로써 **이익을 확정 짓고 계좌 전체의 복리 안전판을 강화**하는 것입니다.

---

## 2. 🏛️ 스마트 리밸런싱 작동 메커니즘 (Market Value Rebalancing Engine)

```mermaid
flowchart TD
    A[초기 포트폴리오: NVDA 30% | MSFT 30% | CAT 40%] --> B[NVDA 대폭등! 평가 금액 쏠림 발생: NVDA 비중 50% ⚠️]
    B --> C[스마트 리밸런싱 계산 엔진 작동]
    C --> D[NVDA 폭등 이익금 중 일부 차익 실현: Sell High]
    D --> E[차익 실현 현금으로 저평가 우량주 MSFT/CAT 추가 매수: Buy Low]
    E --> F[목표 비중 재정렬 완료 & 확정 이익 복리 재투자 확정]
```

---

### 2.1 실전 리밸런싱 수치 예시 (Step-by-Step Example)

| 구 분 | 계좌 초기 투자 상태 | 6개월 후 NVDA 폭등 상태 | 리밸런싱 실행 후 최종 상태 |
| :--- | :--- | :--- | :--- |
| **Nvidia (NVDA)** | $\$3,000$ (비중 $30\%$) | **$\$7,500$ (비중 $50\%$ ⚠️ 쏠림)** | **$\$4,500$ (비중 $30\%$)** $\rightarrow$ 이익금 $\$3,000$ 차익 실현 |
| **Microsoft (MSFT)** | $\$3,000$ (비중 $30\%$) | $\$3,500$ (비중 $23\%$) | **$\$4,500$ (비중 $30\%$)** $\rightarrow$ 저평가 우량주 $\$1,000$ 추가 매수 |
| **Caterpillar (CAT)** | $\$4,000$ (비중 $40\%$) | $\$4,000$ (비중 $27\%$) | **$\$6,000$ (비중 $40\%$)** $\rightarrow$ 인프라 우량주 $\$2,000$ 추가 매수 |
| **총 평가 자산** | **$\$10,000$** | **$\$15,000$ (수익률 $+50\%$)** | **$\$15,000$ (안전한 자산 배분 완료)** |

---

## 3. 🤖 LLM 주입용 평가 금액 리밸런싱 계산 프롬프트

현재 평가 금액과 비중 쏠림을 감지하여 LLM이 구체적인 매도/매수 수량을 안내하는 JSON 구조입니다.

```json
{
  "market_value_rebalancing_input": {
    "total_portfolio_value": "$15,000",
    "target_weights": {"NVDA": "30%", "MSFT": "30%", "CAT": "40%"},
    "current_positions": [
      {"ticker": "NVDA", "current_market_value": "$7,500", "current_weight": "50.0% (과도 쏠림 ⚠️)"},
      {"ticker": "MSFT", "current_market_value": "$3,500", "current_weight": "23.3%"},
      {"ticker": "CAT", "current_market_value": "$4,000", "current_weight": "26.7%"}
    ]
  },
  "llm_rebalancing_execution_plan": {
    "action": "EXECUTE_MARKET_VALUE_REBALANCING",
    "step1_sell_high": "NVDA 주식 중 $3,000치(약 22주)를 차익 실현하여 NVDA 평가 금액을 $4,500(30%)로 맞추십시오.",
    "step2_buy_low": "차익 실현한 $3,000로 MSFT $1,000치 추가 매수, CAT $2,000치 추가 매수하여 목표 비중(30:30:40)을 완성하십시오."
  }
}
```

---

## 4. 🌐 올인원 무료 데이터 수집 파이프라인 (All-in-One Data Matrix)

| 분류 | 핵심 지표 / 데이터 | 데이터 출처 (Data Source) | 비용 | 중장기 리밸런싱 활용 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 평가 금액 & 비중** | **실시간 주가 $\times$ 보유 수량** | **yfinance API** | **100% 무료** | · 실시간 평가 금액 계산 및 종목별 비중 쏠림(> 35%) 감지 |
| **2. 기관 매매 & 13F** | **SEC Form 13F 공시** | **SEC EDGAR API** | **100% 무료** | · 3개월 분기 리밸런싱 시 기관 매수 1등주 확인 |
| **3. B2B CapEx & 실적** | **빅테크 CapEx / 10-Q 실적** | **SEC EDGAR API** | **100% 무료** | · 수혜 우량주의 FCF 흑자 유지 검증 |
| **4. 거시/금리/환율** | **미 기준금리, CPI, VIX** | **FRED API / yfinance** | **100% 무료** | · 거시 국면 전환 시 목표 비중 비율(Target Weight) 조정 |

---

## 5. 🖥️ 초보자를 위한 UI/UX 화면 구성 안 (StockLatte Dashboard)

1. **내 포트폴리오 실시간 평가 금액 & 비중 쏠림 대시보드**
   * `총 평가 자산: $15,000 (초기 대비 +$5,000 수익 달성 🚀)`
   * `⚠️ 비중 쏠림 경보: NVDA 비중이 50%로 과도하게 높아졌습니다.`

2. **[NEW] 1초 자동 리밸런싱 가이드 (One-Click Rebalancing Guide)**
   * `1. NVDA 이익금 $3,000 팔기 (Sell High)`
   * `2. MSFT $1,000 사기 + CAT $2,000 사기 (Buy Low)`
   * `➔ 확정 이익으로 저평가 우량주 분산 완료!`

---

## 6. 🛠️ 단계별 개발 로드맵 (Milestones)

### Phase 1: 평가 금액 기반 비중 계산기 & 쏠림 감지 로직 구축 (1주)
* `yfinance` 주가 연동 기반 보유 수량 $\times$ 현재가 평가 금액 자동 계산 및 비중 쏠림 경고 알고리즘 구축.

### Phase 2: AI (Gemini) 리밸런싱 매도/매수 가이드 Prompt 연동 (2주)
* 이익 실현 수량과 재투자 종목 및 수량을 자동으로 계산해 주는 Prompt 연동.

### Phase 3: Web Dashboard 구축 (3~4주)
* HTML/Vanilla CSS/JavaScript 기반 포트폴리오 평가 금액 & 리밸런싱 대시보드 구축.

---

## 7. 📚 참고 문헌 및 데이터 API (References)

1. **Yahoo Finance API (`yfinance`):** https://pypi.org/project/yfinance/ (실시간 주가 및 평가 금액 파싱 100% 무료)
2. **U.S. SEC EDGAR 13F API:** https://www.sec.gov/edgar/sec-api-documentation (기관 분기 매매 파싱)
3. **FRED (Federal Reserve Economic Data):** https://fred.stlouisfed.org/ (거시 지표 무료 API)
