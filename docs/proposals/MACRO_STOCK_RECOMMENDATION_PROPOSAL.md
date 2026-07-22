# 📈 [StockLatte] 올인원 글로벌 거시경제·정책·환율·비정형 리스크 모니터링 기반 미국 주식 추천 시스템 상세 설계서

> **작성일자:** 2026년 7월 22일 (전염병·자연재해·GDP·신용스프레드 등 올인원 확장)  
> **작성자:** 글로벌 미국 주식 수석 트레이더 & AI 시스템 아키텍트  
> **문서 목적:** 지정학/금리뿐만 아니라 **GDP 성장률, 정책 인플레이션(M2/국채발행), 전염병/자연재해, 환율, 무역제재, 신용스프레드, 공포지수(VIX/MOVE)** 등 시장을 흔드는 모든 변수를 실시간 수집하여, LLM이 전천후로 **"미국 주식 매수/매도 시나리오"**를 도출하는 완벽한 자동화 서비스 구축  

---

## 1. 🎯 프로젝트 개요 및 배경

### 1.1 배경 및 문제 정의
* **블랙 스완 & 복합 리스크 (Black Swan & Multi-Risk Factors):** 글로벌 금융 시장은 단순 금리나 전쟁 외에도 **GDP 침체, 정책성 유동성 과잉(M2/국채 발행), 전염병(Pandemic), 자연재해/이상기후(엘니뇨/태풍), 신용 위험(하이일드 스프레드), 환율 발작(엔 캐리 청산)** 등 예측 불가능한 변수에 의해 급변합니다.
* **초보 투자자의 한계:** 개인이 매주 발표되는 신규 실업수당 청구건수, PCE 물가지수, WHO 보건 경보, NOAA 기후 재해 소식, CBOE VIX 지수 등을 수집하고 주가 영향도를 계산하는 것은 불가능합니다.
* **LLM 판단력의 완전성 (Completeness of LLM Input):** 지표가 누락되면 LLM은 "잘못된 판단(Hallucination)"을 내립니다. 시장을 움직이는 6대 영역 데이터가 모두 주입되어야만 전문 수석 트레이더 수준의 날카로운 분석이 완성됩니다.
* **해결책:** 100% 무료/저비용 데이터 원천을 통해 **[성장/인플레 + 금융/신용 + 환율/무역 + 지정학 + 비정형 재난/기후 + 수급]** 데이터를 정제된 **All-in-One Context Matrix**로 구축하여 최적의 투자의사 결정을 지원합니다.

---

## 2. 🧠 전문 트레이더 관점의 6대 종합 분석 레이어 (All-in-One Multi-Layer Approach)

```mermaid
flowchart TD
    A[1. 성장/인플레/정책 (GDP, M2, PCE, 국채발행)] --> G[LLM All-in-One Context Matrix]
    B[2. 금융 변동성 & 신용위험 (VIX, MOVE, 하이일드)] --> G
    C[3. 환율 & 무역 제재 (DXY, USD/JPY, BIS 수출통제)] --> G
    D[4. 지정학 & 원자재 (GPR, 유가, 구리, 금)] --> G
    E[5. 비정형 재난 & 기후 (WHO 전염병, NOAA 이상기후)] --> G
    F[6. 기관 수급 & 고용 (CoT, 실업수당, 10Y-2Y 금리차)] --> G
    G --> H[입체적 매수 추천 & 내 포트폴리오 매도 신호 발송]
```

---

## 3. 🌐 올인원 무료 데이터 수집 파이프라인 (All-in-One Data Matrix)

비용을 100% 무료(Free Tier/공공 데이터)로 유지하면서 시장을 흔드는 모든 핵심 지표의 데이터 출처를 정리했습니다.

| 분류 | 핵심 지표 / 데이터 | 데이터 출처 (Data Source) | 비용 | 파급 효과 및 트레이더 해석 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 성장 & 정책 인플레** | **실질 GDP 성장률 (`GDPC1`)**<br>**PCE 물가지수 (`PCEPI`)**<br>**M2 통화량 / 국채 발행량** | **FRED API** (`fredapi`) | **100% 무료** | · **2분기 연속 GDP 음수:** 경기 침체(Recession) 경보<br>· **M2/국채발행 급증:** 정책성 인플레이션 재발 우려<br>· **PCE 인플레:** 미 연준 금리 향방 결정 |
| **2. 금융 변동성 & 신용** | **VIX (주가 공포지수)**<br>**MOVE (채권 공포지수)**<br>**High-Yield Credit Spread** | **Yahoo Finance** / **FRED API** (`BAMLH0A0HYM2`) | **100% 무료** | · **VIX > 30:** 시장 패닉 (바닥 매수 기회 탐색)<br>· **신용 스프레드 급등:** 부실 기업 부도 위험 및 금융 위기 시그널 |
| **3. 비정형 재난 & 기후** | **WHO 전염병 경보**<br>**NOAA 이상기후 (엘니뇨/태풍)**<br>**곡물 가격 (대두/옥수수/밀)** | **WHO RSS / NOAA Open Data / yfinance** | **100% 무료** | · **전염병 경보:** 바이오/백신주 호재, 항공/여행주 급락<br>· **이상 기후/태풍:** 농산물 폭등, 정유공장 셧다운, 보험 손해율 급증 |
| **4. 환율 & 무역 제재** | **DXY (달러) / USD/JPY (엔화)**<br>**미 BIS 제재 / CHIPS / IRA** | **yfinance / Federal Register RSS** | **100% 무료** | · **USD/JPY 급락:** 엔 캐리 청산에 따른 기술주 폭락 경보<br>· **수출 제한 제재:** 장비주 악재 vs 미 파운드리 반사이익 |
| **5. 지정학 & 원자재** | **GPR Index (지정학 리스크)**<br>**WTI 원유 / 천연가스 / 구리** | **GPR Direct CSV / yfinance** | **100% 무료** | · **Dr. Copper(구리) 상승:** 실물 경기 회복 신호<br>· **원유/가스 급등:** 에너지주 수혜, 항공/소비재 마진 악화 |
| **6. 기관 수급 & 고용** | **10Y-2Y 장단기 금리차**<br>**신규 실업수당 청구건수**<br>**CFTC CoT (기관 선물 수급)** | **FRED API** (`T10Y2Y`, `ICSA`) / **CFTC.gov** | **100% 무료** | · **장단기 금리차 역전 후 해제:** 역사적 경기 침체 임박<br>· **실업수당 청구 급증:** 고용 시장 냉각 시그널 |

---

## 4. 🤖 LLM 주입용 올인원 프롬프트 구조 (All-in-One Context Matrix Architecture)

시장 전체를 조망할 수 있는 구조화된 JSON 프롬프트를 생성하여 LLM의 분석 능력을 최대로 끌어올립니다.

### 4.1 LLM 입력 데이터 구조 예시 (JSON Schema)
```json
{
  "growth_and_inflation_policy": {
    "real_gdp_growth": "+1.4% (둔화세)",
    "pce_inflation_yoy": "2.6%",
    "m2_money_supply_trend": "상승 전환 (정책 유동성 공급)",
    "initial_jobless_claims": "242K (안정적)"
  },
  "financial_volatility_and_credit": {
    "cboe_vix": "22.5 (경계 단계)",
    "move_bond_volatility": "115.0",
    "high_yield_credit_spread": "3.85% (안정적)"
  },
  "unstructured_disasters_and_climate": {
    "who_health_alerts": "새로운 조류 독감(H5N1) 변이 인체 감염 경보 발령",
    "noaa_climate_status": "강력한 엘니뇨 지속 -> 곡물 및 천연가스 생산 차질 우려"
  },
  "fx_and_trade_policy": {
    "dxy_dollar_index": "104.2",
    "usd_jpy_rate": "151.2 (엔화 강세 압력 ⚠️)",
    "export_restrictions": "미 상무부, 대중 첨단 기술 수출 통제 대상 12개 기업 추가"
  },
  "geopolitics_and_commodities": {
    "gpr_index": "165 (높음)",
    "wti_crude": "$87.20",
    "copper_price": "$4.45",
    "corn_grain_price": "$4.80 (기후 영향으로 급등)"
  },
  "user_portfolio": [
    {"ticker": "AAL", "avg_cost": 14.50, "current_price": 11.20, "pnl_pct": "-22.76%"},
    {"ticker": "PFE", "avg_cost": 28.00, "current_price": 31.50, "pnl_pct": "+12.50%"}
  ]
}
```

---

## 5. ⚙️ 주가 상승(매수) & 포트폴리오 매도(Exit) 시나리오 엔진

### 5.1 💡 비정형 리스크/정책 기반 매수(Buy) 시나리오 예시

#### 시나리오 1: 전염병/보건 경보 발령 & 바이오 수혜 / 여행주 피하기
* **상황 조건 (IF):** WHO 글로벌 보건 경보 단계 격상 뉴스 급증.
* **입체적 분석 (WHY):** 백신/치료제 개발 바이오 기업 수주 급증, 항공/여행/소비재 진입 자제.
* **추천 종목:** **Pfizer (PFE)**, **Moderna (MRNA)**
* **매수 트리거 (WHEN TO BUY):** WHO 발표 직후 및 거래량 폭증 시.

#### 시나리오 2: 엘니뇨 기후 재해 & 비료/곡물 및 원자재 수혜
* **상황 조건 (IF):** NOAA 엘니뇨 경보 지속 AND 곡물/비료 가격 $\$4.50$ 상방 돌파.
* **입체적 분석 (WHY):** 농산물 수확량 감소로 곡물 거래사 및 비료 제조사 마진 급증.
* **추천 종목:** **Nutrien (NTR)**, **Archer-Daniels-Midland (ADM)**

---

### 5.2 🛑 사용자 포트폴리오 진단 및 매도(Sell / Exit) 추천 알고리즘

사용자가 **[보유 종목, 평균 매수가, 보유 수량]**을 입력하면, 전염병·신용스프레드·GDP 침체 등 블랙스완 요소를 포함하여 실시간 진단을 제공합니다.

#### 4대 매도 평가 레이어:

1. **비정형 재난/전염병 악재 시그널:**
   * **예시 (항공주 AAL 보유 시):** WHO 보건 경보 발령 시 $\rightarrow$ `[여행 감소 우려 - 즉시 손절/익절 매도 경고]`

2. **신용 위험 & 금융 변동성 발작 (Credit & Volatility Crisis):**
   * **예시:** 하이일드 신용 스프레드 $5.0\%$ 돌파 OR VIX 지수 $35$ 돌파 시 $\rightarrow$ `[전체 보유 종목 위험 관리 현금화 비율 확대 권고]`

3. **정책 인플레이션 & 금리 발작:**
   * **예시:** M2 통화량 폭증 및 10년물 금리 $4.8\%$ 돌파 시 $\rightarrow$ `[고P/E 성장주 차익 실현 권고]`

4. **동적 익절/손절 & 모멘텀 소멸:**
   * **수익 목표 (Take-Profit):** $+20\%$ 분할 익절.
   * **손절 (Stop-Loss):** $-7\%$ 도달 시 구조적 악재 판별 후 자동 대응 가이드 발송.

---

## 6. 📐 시스템 아키텍처 (System Architecture)

```
 [6대 다차원 데이터 원천 (100% 무료/저비용)]
 ├── FRED API (GDP, PCE, M2, 신용스프레드, 장단기 금리차, 실업수당)
 ├── Yahoo Finance (주가, 원자재, VIX, MOVE 지수, FX 환율)
 ├── WHO RSS & NOAA Open Data (전염병 보건 경보, 기후 재해)
 ├── GPR Index & NY Fed GSCPI (지정학 지수, 공급망 압력 지수)
 └── US Federal Register & Google News (무역제재, 수출통제)
        │
        ▼
 [Data Ingestion & All-in-One Context Matrix Builder]
        │
        ▼
 [AI Analysis Engine (Gemini All-in-One Context Prompt)]
 ├── 6대 레이어 리스크 종합 평가 (0~100 점수화)
 ├── 센티먼트 및 인과관계 매핑 (Bullish / Neutral / Bearish)
 └── 매수 추천 및 내 포트폴리오 매도 진단 보고서 작성
        │
        ▼
 [Rule & Trigger Engine]
 ├── If-Then 매수 시나리오 매칭
 └── 사용자 포트폴리오 매도(Sell) 시그널 진단기
        │
        ▼
 [StockLatte UI / Notification System]
 ├── 오늘의 시장 6대 종합 온도계 대시보드
 ├── 입체적 종목 추천 리포트 (매수 타이밍 + 기후/전염병/정책 리스크)
 ├── 내 포트폴리오 매도 타이밍 진단 탭
 └── 텔레그램 / Discord / 웹 푸시 알림
```

---

## 7. 🖥️ 초보자를 위한 UI/UX 화면 구성 안 (StockLatte Dashboard)

1. **오늘의 글로벌 시장 6대 종합 온도계 (Market Thermometer)**
   * `🔴 지정학 리스크: 높음 (중동 유가 변동성 ⚠️)`
   * `🔴 비정형 보건/기후: 경계 (WHO 조류 독감 경보 & 엘니뇨 곡물가 폭등 ⚠️)`
   * `🟡 환율/통화 리스크: 주의 (엔화 강세 전환 ⚠️ 엔캐리 청산 경계)`
   * `🔵 무역/통상 규제: 보통 (미 대중 반도체 추가 제재 발표)`
   * `🟢 금리/인플레: 안정 (FOMC 금리 인하 가능성 80%)`
   * `🟢 신용/변동성: 양호 (VIX 22.5 / 하이일드 스프레드 안정)`

2. **[NEW] 내 포트폴리오 매도 진단 카드 (Portfolio Sell Assistant)**
   * **입력 예시:** Ticker `AAL` (아메리칸 항공) | 평단가 `$14.50` | 현재가 `$11.20` (수익률 `-22.76%`)
   * **진단 결과:** `🔴 [비정형 보건 악재 발생 - 손절 및 매도 권고]`
   * **입체적 분석 사유:**
     1. WHO의 새로운 전염병 보건 경보 발령으로 글로벌 여객 수요 감소 직격탄 우려.
     2. 유가 $87 돌파로 항공유 정제 비용 마진 부담 가중.
     3. **추천 대응:** 반등을 기다리기보다 손절 후 방산/바이오 섹터(PFE, MRNA)로 교체 매매 권장.

---

## 8. 🛠️ 단계별 개발 로드맵 (Milestones)

### Phase 1: 6대 데이터 수집 파이프라인 구축 (1~2주)
* Python 기반 거시지표, GDP, M2, VIX, MOVE, WHO RSS, NOAA 기후, FX 파이프라인 구축 (`yfinance`, `fredapi`, `feedparser`).
* 사용자 평단가 기반 매도(Sell) 시그널 파이프라인 및 테스트 케이스 구축 (`tests/` 및 `test_results/`).

### Phase 2: AI (Gemini) All-in-One Context Matrix Prompt 연동 (2~3주)
* JSON 형태의 All-in-One Context Matrix를 Gemini Free Tier API에 전달하여 종합 진단 리포트 자동 생성.

### Phase 3: Web Dashboard & 실시간 알림 서비스 구축 (3~4주)
* HTML/Vanilla CSS/JavaScript (또는 Vite React) 기반의 6대 시장 온도계 및 포트폴리오 매도 진단 대시보드 구축.

---

## 9. 📚 참고 문헌 및 데이터 API (References)

1. **FRED (Federal Reserve Economic Data):** https://fred.stlouisfed.org/ (GDP, M2, PCE, 신용스프레드, 금리차, 실업수당 무료 API)
2. **Yahoo Finance API (`yfinance`):** https://pypi.org/project/yfinance/ (주가, 원자재, VIX, MOVE, FX 시세)
3. **WHO Disease Outbreak News:** https://www.who.int/emergencies/disease-outbreak-news (전염병 보건 경보 RSS)
4. **NOAA Climate Prediction Center:** https://www.cpc.ncep.noaa.gov/ (이상기후 및 엘니뇨/라니냐 데이터)
5. **NY Fed GSCPI:** https://www.newyorkfed.org/research/policy/gscpi (공급망 압력 지수)
6. **U.S. Federal Register (BIS Export Regulations):** https://www.federalregister.gov/ (무역 제재 관보)
7. **Geopolitical Risk (GPR) Index:** https://www.matteoiacoviello.com/gpr.htm (지정학 리스크 지수 데이터)
