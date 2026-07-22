# 📈 [StockLatte] 올인원 거시경제·기업CapEx·자원수급·정책·환율·비정형 리스크 모니터링 기반 미국 주식 추천 시스템 상세 설계서

> **작성일자:** 2026년 7월 22일 (전방산업 B2B 수요·기업 CapEx·건설/인프라 수주 파이프라인 확장)  
> **작성자:** 글로벌 미국 주식 수석 트레이더 & AI 시스템 아키텍트  
> **문서 목적:** 거시지표/지정학뿐만 아니라 **전방 산업 B2B 기업 수요, 빅테크 AI 설비투자(CapEx), 건설/인프라 지출(Construction Spending), 수주잔고(Backlog), 가동률(Capacity Utilization), 자원 수급, 환율, 신용스프레드** 등 기업 이윤과 주가를 결정짓는 전방-후방 밸류체인 수급 변수를 실시간 수집하여, LLM이 **"미국 주식 매수/매도 시나리오"**를 입체적으로 도출하는 완벽한 자동화 서비스 구축  

---

## 1. 🎯 프로젝트 개요 및 배경

### 1.1 배경 및 문제 정의
* **전방 산업 B2B 수요 & CapEx 밸류체인 (Downstream Demand & CapEx Chain):** 주가는 단순 뉴스가 아니라 **전방 산업의 기업 수요(B2B Demand)**에 의해 결정됩니다. 
  * *예시 1 (AI 메모리 폭등):* 빅테크(MSFT, META, GOOGL, AMZN)의 **AI 데이터센터 설비투자(CapEx) 폭증** $\rightarrow$ NVDA GPU 수요 쇄도 $\rightarrow$ HBM/메모리(MU, SK하이닉스) 수주 폭발.
  * *예시 2 (인프라/건설 폭등):* 미국 리쇼어링 공장 건설 및 인프라 법안(IIJA) 지출 폭증 $\rightarrow$ 건설 지출(Construction Spending) 급증 $\rightarrow$ 중장비(CAT, DE) 수주 및 주가 폭등.
* **초보 투자자의 한계:** 개인이 SEC 공시(10-Q/10-K)에서 빅테크 4사의 CapEx 가이던스, 미 상무부 건설 지출 통계, 미 연준 산업 가동률(Capacity Utilization), ISM 제조업 신규 수주 지수(New Orders Index)를 일일이 추적하고 연결고리를 찾는 것은 불가능합니다.
* **LLM 판단력의 완전성 (Completeness of LLM Input):** 전방 산업의 CapEx 및 수주 잔고(Backlog) 데이터가 주입되지 않으면 LLM은 실적 대폭발 종목을 놓칩니다. **[B2B CapEx/수주 + 자원수급 + 거시/금리 + 환율/무역 + 지정학 + 비정형 재난]**의 8대 레이어 체계가 필요합니다.
* **해결책:** 100% 무료 공공 API(SEC EDGAR, FRED, ISM)를 활용해 전방 산업의 B2B 수요 지표를 정제하여 **All-in-One Context Matrix**로 구축합니다.

---

## 2. 🧠 전문 트레이더 관점의 8대 종합 분석 레이어 (All-in-One Multi-Layer Approach)

```mermaid
flowchart TD
    A[1. 전방 B2B 수요 & 기업 CapEx (SEC EDGAR, 건설지출, ISM 신규수주)] --> I[LLM All-in-One Context Matrix]
    B[2. 자원 수급/생산량/수출입 (EIA, USGS, USDA, LME)] --> I
    C[3. 성장/인플레/정책 (GDP, M2, PCE, 국채발행)] --> I
    D[4. 금융 변동성 & 신용위험 (VIX, MOVE, 하이일드)] --> I
    E[5. 환율 & 무역 제재 (DXY, USD/JPY, BIS 수출통제)] --> I
    F[6. 지정학 & 원자재 (GPR, 유가, 구리, 금)] --> I
    G[7. 비정형 재난 & 기후 (WHO 전염병, NOAA 이상기후)] --> I
    H[8. 기관 수급 & 고용 (CoT, 실업수당, 10Y-2Y 금리차)] --> I
    I --> J[입체적 매수 추천 & 내 포트폴리오 매도 신호 발송]
```

---

## 3. 🌐 올인원 무료 데이터 수집 파이프라인 (All-in-One Data Matrix)

비용은 100% 무료(SEC EDGAR, FRED API 등)로 유지하면서 전방 기업 수요와 핵심 거시 지표를 정밀하게 수집합니다.

| 분류 | 핵심 지표 / 데이터 | 데이터 출처 (Data Source) | 비용 | 파급 효과 및 트레이더 해석 |
| :--- | :--- | :--- | :--- | :--- |
| **1. B2B 수요 & 기업 CapEx** | **빅테크 4사 CapEx 지출/가이던스**<br>**미국 총 건설 지출 (`TTLCONS`)**<br>**ISM 제조업 신규수주 지수**<br>**산업 가동률 (`TCU`)** | **SEC EDGAR API** (10-Q/K)<br>**FRED API** (`fredapi`)<br>**ISM / Census Bureau** | **100% 무료** | · **Big Tech CapEx 증가:** NVDA, 메모리(MU), 서버/냉각(VRT) 실적 폭증<br>· **건설 지출/가동률 > 80%:** 건설 기계(CAT), 파운드리/공장 인프라 수혜<br>· **ISM 신규 수주 > 50:** 제조업 경기 회복 및 부품 수주 폭증 |
| **2. 자원 생산 & 수출입** | **원유 생산/재고량 (EIA)**<br>**희토류/리튬 매장·생산 (USGS)**<br>**세계 곡물 수급 (USDA WASDE)** | **EIA API** / **USGS**<br>**USDA WASDE** / **LME** | **100% 무료** | · **EIA 원유 재고 감소:** 유가 상승 $\rightarrow$ 정유주(XOM) 수혜<br>· **중국 희토류 수출 규제:** MP Materials(MP) 등 대체 광산 폭등<br>· **USDA 곡물 재고 급감:** 농업/비료주(NTR, ADM) 호재 |
| **3. 자원 통상 & 제재** | **자원 수출 제한 조치**<br>**Global Trade Alert** | **GlobalTradeAlert.org**<br>**OECD Raw Materials** | **100% 무료** | · **자원 무기화 발표:** 공급망 차질 발생으로 수혜 섹터 갭상승<br>· **핵심 광물 관세:** 배터리/전기차(TSLA) 원가 부담 가중 |
| **4. 성장 & 정책 인플레** | **실질 GDP 성장률 (`GDPC1`)**<br>**PCE 물가지수 / M2 통화량** | **FRED API** (`fredapi`) | **100% 무료** | · **2분기 연속 GDP 음수:** 경기 침체 경보<br>· **M2/국채발행 급증:** 정책성 인플레이션 재발 우려 |
| **5. 금융 변동성 & 신용** | **VIX (주가 공포지수)**<br>**MOVE (채권 공포지수)**<br>**High-Yield Credit Spread** | **Yahoo Finance** / **FRED API** (`BAMLH0A0HYM2`) | **100% 무료** | · **VIX > 30:** 시장 패닉 (바닥 매수 기회 탐색)<br>· **신용 스프레드 급등:** 부실 기업 부도 위험 및 금융 위기 시그널 |
| **6. 비정형 재난 & 기후** | **WHO 전염병 경보**<br>**NOAA 이상기후 (엘니뇨/태풍)** | **WHO RSS / NOAA Open Data** | **100% 무료** | · **전염병 경보:** 바이오주 호재, 항공/여행주 급락<br>· **이상 기후/태풍:** 농산물 폭등, 정유공장 가동 중단 |
| **7. 환율 & 무역 제재** | **DXY (달러) / USD/JPY (엔화)**<br>**미 BIS 제재 / CHIPS / IRA** | **yfinance / Federal Register RSS** | **100% 무료** | · **USD/JPY 급락:** 엔 캐리 청산에 따른 기술주 폭락 경보<br>· **수출 제한 제재:** 장비주 악재 vs 미 파운드리 반사이익 |
| **8. 기관 수급 & 고용** | **10Y-2Y 장단기 금리차**<br>**신규 실업수당 청구건수**<br>**CFTC CoT (기관 선물 수급)** | **FRED API** / **CFTC.gov** | **100% 무료** | · **장단기 금리차 역전 후 해제:** 역사적 경기 침체 도래<br>· **실업수당 청구 급증:** 고용 시장 냉각 시그널 |

---

## 4. 🤖 LLM 주입용 올인원 프롬프트 구조 (All-in-One Context Matrix Architecture)

전방 B2B 수요와 CapEx 수주 밸류체인이 포함된 JSON 프롬프트를 생성하여 LLM의 분석 능력을 극대화합니다.

### 4.1 LLM 입력 데이터 구조 예시 (JSON Schema)
```json
{
  "downstream_b2b_demand_and_capex": {
    "bigtech_ai_capex_guidance": "MSFT, META, GOOGL 2026년 CapEx 전년 대비 +35% 증액 발표 (총 $200B 데이터센터 투입)",
    "us_construction_spending": "$2.15T (전년 대비 +7.8% 증가 - 비주거용 공장/데이터센터 주도)",
    "ism_manufacturing_new_orders": "53.2 (50 상회 -> 확장 국면 진입)",
    "us_capacity_utilization": "79.8% (80% 임박 -> 기업 설비 증설 모멘텀)"
  },
  "global_resource_and_commodity_supply": {
    "us_eia_crude_inventory": "-4.2M Barrels",
    "usgs_critical_minerals": "중국, 희토류 수출 통제 강화"
  },
  "growth_and_inflation_policy": {
    "real_gdp_growth": "+1.4%",
    "pce_inflation_yoy": "2.6%"
  },
  "financial_volatility_and_credit": {
    "cboe_vix": "22.5"
  },
  "user_portfolio": [
    {"ticker": "MU", "avg_cost": 95.00, "current_price": 135.00, "pnl_pct": "+42.10% (BigTech CapEx HBM 수혜)"},
    {"ticker": "CAT", "avg_cost": 310.00, "current_price": 365.00, "pnl_pct": "+17.74% (미 건설지출 수혜)"}
  ]
}
```

---

## 5. ⚙️ 주가 상승(매수) & 포트폴리오 매도(Exit) 시나리오 엔진

### 5.1 💡 B2B CapEx & 전방 수요 기반 매수(Buy) 시나리오 예시

#### 시나리오 1: 빅테크 AI CapEx 폭증 & HBM 메모리 수주 대폭발
* **상황 조건 (IF):** Big Tech(MSFT, META) 10-Q CapEx 가이던스 상향 발표 AND ISM 신규 수주 지수 > 50.
* **입체적 분석 (WHY):** 데이터센터 구축을 위한 AI 서버 칩 및 HBM/고용량 DRAM 주문 쇄도로 메모리 가격 상승 및 실적 상향.
* **추천 종목:** **Micron Technology (MU)**, **Nvidia (NVDA)**, **Vertiv (VRT - 데이터센터 냉각)**
* **매수 트리거 (WHEN TO BUY):** 빅테크 실적 발표에서 CapEx 증액 확인 직후.

#### 시나리오 2: 미국 비주거용 건설 지출 폭증 & 중장비 수주 모멘텀
* **상황 조건 (IF):** 미국 비주거용 건설 지출(`TTLCONS`) 전월 대비 +1.5% 이상 급증 AND 인프라 법안 집행.
* **입체적 분석 (WHY):** 미 국내 반도체/배터리 공장 건설 및 도로/전력망 확충으로 건설 중장비 수주 잔고(Backlog) 급증.
* **추천 종목:** **Caterpillar (CAT)**, **Deere & Company (DE)**

---

### 5.2 🛑 사용자 포트폴리오 진단 및 매도(Sell / Exit) 추천 알고리즘

사용자가 **[보유 종목, 평균 매수가, 보유 수량]**을 입력하면, 전방 B2B 기업의 CapEx 삭감, 건설 지출 감소 등 밸류체인 악재를 대입해 피크아웃(Peak-out) 매도 타점을 제시합니다.

#### 4대 매도 평가 레이어:

1. **전방 산업 CapEx 삭감 및 피크아웃 (CapEx Peak-Out Signal):**
   * **예시 (메모리 MU 보유 시):** 빅테크 기업들이 AI CapEx 속도 조절(지출 삭감) 시 $\rightarrow$ `[메모리 피크아웃 우려 - 익절/비중 축소 경고]`

2. **건설/인프라 수주 잔고 감소:**
   * **예시 (CAT 보유 시):** 미 건설 지출 둔화 및 수주 잔고 하락 시 $\rightarrow$ `[매도 진단 가이드 발송]`

3. **신용 위험 & 환율 발작 (FX & Volatility Crisis):**
   * **예시:** USD/JPY 급락(엔캐리 청산) 시 $\rightarrow$ `[기술주 위험 관리]`

4. **동적 익절/손절 & 모멘텀 소멸:**
   * **수익 목표 (Take-Profit):** $+20\%$ 분할 익절.
   * **손절 (Stop-Loss):** $-7\%$ 도달 시 원인 판별 후 자동 대응.

---

## 6. 📐 시스템 아키텍처 (System Architecture)

```
 [8대 다차원 데이터 원천 (100% 무료/저비용)]
 ├── SEC EDGAR API & FRED Construction & ISM (CapEx, B2B 신규수주, 가동률)
 ├── EIA API & USGS & USDA WASDE & LME (자원 생산/재고/수출입)
 ├── FRED API (GDP, PCE, M2, 신용스프레드, 장단기 금리차, 실업수당)
 ├── Yahoo Finance (주가, 원자재, VIX, MOVE 지수, FX 환율)
 ├── WHO RSS & NOAA Open Data (전염병 보건 경보, 기후 재해)
 ├── GPR Index & NY Fed GSCPI (지정학 지수, 공급망 압력 지수)
 └── US Federal Register & Global Trade Alert (무역제재, 자원수출통제)
        │
        ▼
 [Data Ingestion & All-in-One Context Matrix Builder]
        │
        ▼
 [AI Analysis Engine (Gemini All-in-One Context Prompt)]
 ├── 8대 레이어 B2B CapEx/거시/자원 리스크 종합 평가 (0~100 점수화)
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
 ├── 오늘의 시장 8대 종합 온도계 대시보드 (B2B CapEx 레이더 포함)
 ├── 입체적 종목 추천 리포트 (매수 타이밍 + CapEx/자원/기후 리스크)
 ├── 내 포트폴리오 매도 타이밍 진단 탭
 └── 텔레그램 / Discord / 웹 푸시 알림
```

---

## 7. 🖥️ 초보자를 위한 UI/UX 화면 구성 안 (StockLatte Dashboard)

1. **오늘의 글로벌 시장 8대 종합 온도계 (Market Thermometer)**
   * `🟢 B2B CapEx/수주: 매우 긍정 (빅테크 AI CapEx +35% 증액 & 건설지출 호조 🚀)`
   * `🔴 자원 수급/무기화: 경계 (중국 희토류 수출 규제 & EIA 원유 재고 급감 ⚠️)`
   * `🔴 지정학 리스크: 높음 (중동 분쟁 변동성 ⚠️)`
   * `🟡 환율/통화 리스크: 주의 (엔화 강세 전환 ⚠️ 엔캐리 청산 경계)`
   * `🔵 무역/통상 규제: 보통 (미 대중 반도체 추가 제재 발표)`
   * `🟢 금리/인플레: 안정 (FOMC 금리 인하 가능성 80%)`
   * `🟢 비정형 보건/기후: 양호 (전염병 경보 없음)`
   * `🟢 신용/변동성: 양호 (VIX 22.5 / 하이일드 스프레드 안정)`

2. **[NEW] 내 포트폴리오 매도 진단 카드 (Portfolio Sell Assistant)**
   * **입력 예시:** Ticker `MU` (마이론 테크놀로지) | 평단가 `$95.00` | 현재가 `$135.00` (수익률 `+42.10%`)
   * **진단 결과:** `🟢 [전방 CapEx 호조 지속 - 보유 및 트레일링 스탑 설정]`
   * **입체적 분석 사유:**
     1. Big Tech 4사의 AI 데이터센터 CapEx 가이던스가 여전히 전년 대비 +35% 이상 성장세 유지 중.
     2. HBM3E 수주 잔고가 내년까지 완전 소진(Sold-out) 상태로 피크아웃 우려 낮음.
     3. **추천 대응:** 성급한 전량 매도보다 $125.00 트레일링 스탑을 설정하고 지속 보유하여 추가 상승 수익 극대화 권장.

---

## 8. 🛠️ 단계별 개발 로드맵 (Milestones)

### Phase 1: 8대 데이터 수집 파이프라인 구축 (1~2주)
* Python 기반 B2B CapEx (SEC EDGAR API, FRED 건설지출, ISM 신규수주), 자원 수급, 거시지표 파이프라인 구축 (`yfinance`, `fredapi`, `sec-edgar-downloader`, `feedparser`).
* 사용자 평단가 기반 매도(Sell) 시그널 파이프라인 및 테스트 케이스 구축 (`tests/` 및 `test_results/`).

### Phase 2: AI (Gemini) All-in-One Context Matrix Prompt 연동 (2~3주)
* JSON 형태의 All-in-One Context Matrix를 Gemini Free Tier API에 전달하여 종합 진단 리포트 자동 생성.

### Phase 3: Web Dashboard & 실시간 알림 서비스 구축 (3~4주)
* HTML/Vanilla CSS/JavaScript (또는 Vite React) 기반의 8대 시장 온도계 및 포트폴리오 매도 진단 대시보드 구축.

---

## 9. 📚 참고 문헌 및 데이터 API (References)

1. **U.S. SEC EDGAR API:** https://www.sec.gov/edgar/sec-api-documentation (미국 상장사 10-Q/K CapEx 공시 무료 API)
2. **FRED (Federal Reserve Economic Data):** https://fred.stlouisfed.org/ (건설 지출, 가동률, GDP, M2, PCE 무료 API)
3. **ISM (Institute for Supply Management):** https://www.ismworld.org/ (ISM 제조업 신규 수주 지수)
4. **U.S. Energy Information Administration (EIA):** https://www.eia.gov/ (원유/가스 생산 및 재고 API)
5. **U.S. Geological Survey (USGS):** https://www.usgs.gov/ (희토류/리튬 자원 매장량)
6. **Yahoo Finance API (`yfinance`):** https://pypi.org/project/yfinance/ (주가, 원자재, VIX, FX 시세)
7. **WHO Disease Outbreak News:** https://www.who.int/emergencies/disease-outbreak-news (전염병 보건 경보 RSS)
8. **Geopolitical Risk (GPR) Index:** https://www.matteoiacoviello.com/gpr.htm (지정학 리스크 지수)
