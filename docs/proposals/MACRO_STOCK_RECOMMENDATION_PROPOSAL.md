# 📈 [StockLatte] 올인원 글로벌 거시경제·자원수급·정책·환율·비정형 리스크 모니터링 기반 미국 주식 추천 시스템 상세 설계서

> **작성일자:** 2026년 7월 22일 (글로벌 자원 생산량/재고/수출입 수급 파이프라인 최종 확장)  
> **작성자:** 글로벌 미국 주식 수석 트레이더 & AI 시스템 아키텍트  
> **문서 목적:** 지정학/금리/GDP뿐만 아니라 **각국 자원 생산량·재고량·수출입(원유, 천연가스, 희토류, 리튬, 곡물), 자원 무기화/수출제한, 전염병/자연재해, 환율, 신용스프레드, 공포지수(VIX/MOVE)** 등 시장을 흔드는 모든 자원 및 거시 변수를 실시간 수집하여, LLM이 전천후로 **"미국 주식 매수/매도 시나리오"**를 도출하는 완벽한 자동화 서비스 구축  

---

## 1. 🎯 프로젝트 개요 및 배경

### 1.1 배경 및 문제 정의
* **자원 무기화 & 공급망 파동 (Resource Nationalism & Commodity Shock):** 오늘날의 세계 경제는 특정 국가의 **자원 생산량 감산(OPEC+ 원유 감산), 핵심 자원 수출 제한(중국의 희토류/갈륨/제르마늄 수출 통제), 농산물 수출 금지(인도의 쌀/밀 수출 중단)** 등에 의해 개별 종목 주가가 수십 퍼센트씩 폭등/폭락합니다.
* **초보 투자자의 한계:** 개인이 미 에너지청(EIA)의 주간 원유 재고 발표, 미 지질조사국(USGS)의 광물 생산 통계, 미 농무부(USDA)의 곡물 수급 보고서(WASDE), LME 금속 재고량 등을 매일 확인하고 주가 영향도를 계산하는 것은 불가능합니다.
* **LLM 판단력의 완전성 (Completeness of LLM Input):** 지표가 누락되면 LLM은 "잘못된 판단(Hallucination)"을 내립니다. **자원 수급(생산/재고/수출입)** 데이터가 추가되어야만 원자재, 에너지, 배터리, 반도체 소재, 농업 섹터에 대한 트레이더 수준의 입체적 분석이 완성됩니다.
* **해결책:** 100% 무료/저비용 데이터 원천을 통해 **[자원 수급/생산/수출입 + 성장/인플레 + 금융/신용 + 환율/무역 + 지정학 + 비정형 재난/기후 + 수급]** 데이터를 정제된 **All-in-One Context Matrix**로 구축하여 최적의 투자의사 결정을 지원합니다.

---

## 2. 🧠 전문 트레이더 관점의 7대 종합 분석 레이어 (All-in-One Multi-Layer Approach)

```mermaid
flowchart TD
    A[1. 자원 수급/생산량/수출입 (EIA, USGS, USDA, LME)] --> H[LLM All-in-One Context Matrix]
    B[2. 성장/인플레/정책 (GDP, M2, PCE, 국채발행)] --> H
    C[3. 금융 변동성 & 신용위험 (VIX, MOVE, 하이일드)] --> H
    D[4. 환율 & 무역 제재 (DXY, USD/JPY, BIS 수출통제)] --> H
    E[5. 지정학 & 원자재 (GPR, 유가, 구리, 금)] --> H
    F[6. 비정형 재난 & 기후 (WHO 전염병, NOAA 이상기후)] --> H
    G[7. 기관 수급 & 고용 (CoT, 실업수당, 10Y-2Y 금리차)] --> H
    H --> I[입체적 매수 추천 & 내 포트폴리오 매도 신호 발송]
```

---

## 3. 🌐 올인원 무료 데이터 수집 파이프라인 (All-in-One Data Matrix)

비용을 100% 무료(Free Tier/공공 데이터)로 유지하면서 시장을 흔드는 자원 수급 지표 및 핵심 거시 지표의 데이터 출처를 정리했습니다.

| 분류 | 핵심 지표 / 데이터 | 데이터 출처 (Data Source) | 비용 | 파급 효과 및 트레이더 해석 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 자원 생산 & 수출입** | **국가별 원유 생산/재고량**<br>**희토류/리튬/니켈 매장·생산량**<br>**세계 곡물 수급/재고 (WASDE)**<br>**LME 금속 재고량** | **EIA API** (`eia.gov`) / **USGS**<br>**USDA WASDE** / **LME Data** | **100% 무료** | · **EIA 원유 재고 감소:** 유가 상승 $\rightarrow$ 정유주(XOM, CVX) 수혜<br>· **중국 희토류 수출 규제:** MP Materials(MP) 등 대체 광산 폭등<br>· **USDA 곡물 재고 급감:** 농업/비료주(NTR, ADM) 호재 |
| **2. 자원 통상 & 제재** | **자원 수출 제한 조치**<br>**Global Trade Alert** | **GlobalTradeAlert.org**<br>**OECD Raw Materials** | **100% 무료** | · **자원 무기화 발표:** 공급망 차질 발생으로 수혜 섹터 갭상승<br>· **핵심 광물 관세:** 배터리/전기차(TSLA) 원가 부담 가중 |
| **3. 성장 & 정책 인플레** | **실질 GDP 성장률 (`GDPC1`)**<br>**PCE 물가지수 / M2 통화량** | **FRED API** (`fredapi`) | **100% 무료** | · **2분기 연속 GDP 음수:** 경기 침체 경보<br>· **M2/국채발행 급증:** 정책성 인플레이션 재발 우려 |
| **4. 금융 변동성 & 신용** | **VIX (주가 공포지수)**<br>**MOVE (채권 공포지수)**<br>**High-Yield Credit Spread** | **Yahoo Finance** / **FRED API** (`BAMLH0A0HYM2`) | **100% 무료** | · **VIX > 30:** 시장 패닉 (바닥 매수 기회 탐색)<br>· **신용 스프레드 급등:** 부실 기업 부도 위험 및 금융 위기 시그널 |
| **5. 비정형 재난 & 기후** | **WHO 전염병 경보**<br>**NOAA 이상기후 (엘니뇨/태풍)** | **WHO RSS / NOAA Open Data** | **100% 무료** | · **전염병 경보:** 바이오주 호재, 항공/여행주 급락<br>· **이상 기후/태풍:** 농산물 폭등, 정유공장 가동 중단 |
| **6. 환율 & 무역 제재** | **DXY (달러) / USD/JPY (엔화)**<br>**미 BIS 제재 / CHIPS / IRA** | **yfinance / Federal Register RSS** | **100% 무료** | · **USD/JPY 급락:** 엔 캐리 청산에 따른 기술주 폭락 경보<br>· **수출 제한 제재:** 장비주 악재 vs 미 파운드리 반사이익 |
| **7. 기관 수급 & 고용** | **10Y-2Y 장단기 금리차**<br>**신규 실업수당 청구건수**<br>**CFTC CoT (기관 선물 수급)** | **FRED API** / **CFTC.gov** | **100% 무료** | · **장단기 금리차 역전 후 해제:** 역사적 경기 침체 도래<br>· **실업수당 청구 급증:** 고용 시장 냉각 시그널 |

---

## 4. 🤖 LLM 주입용 올인원 프롬프트 구조 (All-in-One Context Matrix Architecture)

자원 수급과 글로벌 거시 환경을 종합 판단할 수 있는 구조화된 JSON 프롬프트를 생성하여 LLM의 분석 능력을 최대로 끌어올립니다.

### 4.1 LLM 입력 데이터 구조 예시 (JSON Schema)
```json
{
  "global_resource_and_commodity_supply": {
    "us_eia_crude_inventory": "-4.2M Barrels (예상치 상회하는 재고 급감 ⚠️)",
    "opec_production_status": "일산 220만 바렐 자율 감산 연장 확정",
    "usgs_critical_minerals": "중국, 희토류 및 갈륨/제르마늄 수출 허가제 강화 (수출 제한)",
    "usda_grain_inventory": "세계 밀 재고량 5년래 최저치 경신 (공급 부족)"
  },
  "growth_and_inflation_policy": {
    "real_gdp_growth": "+1.4% (둔화세)",
    "pce_inflation_yoy": "2.6%",
    "m2_money_supply_trend": "상승 전환"
  },
  "financial_volatility_and_credit": {
    "cboe_vix": "22.5 (경계 단계)",
    "high_yield_credit_spread": "3.85% (안정적)"
  },
  "unstructured_disasters_and_climate": {
    "who_health_alerts": "안정적",
    "noaa_climate_status": "강력한 엘니뇨 지속 -> 곡물 생산 차질 우려"
  },
  "fx_and_trade_policy": {
    "dxy_dollar_index": "104.2",
    "usd_jpy_rate": "151.2 (엔화 강세 압력 ⚠️)"
  },
  "user_portfolio": [
    {"ticker": "MP", "avg_cost": 15.20, "current_price": 19.80, "pnl_pct": "+30.26%"},
    {"ticker": "XOM", "avg_cost": 110.00, "current_price": 118.50, "pnl_pct": "+7.73%"}
  ]
}
```

---

## 5. ⚙️ 주가 상승(매수) & 포트폴리오 매도(Exit) 시나리오 엔진

### 5.1 💡 자원 수급/무기화 기반 매수(Buy) 시나리오 예시

#### 시나리오 1: 중국 희토류 수출 통제 & 서방권 대체 광산 부각
* **상황 조건 (IF):** 중국 상무부 희토류 및 핵심 광물 수출 통제 공표 AND 미 지질조사국(USGS) 서방 광산 희토류 재고 부족 확인.
* **입체적 분석 (WHY):** 전기차 모터 및 첨단 무기에 필수적인 희토류 수급난 우려로 미국 내 유일한 희토류 채굴/분리 기업 독점 수혜.
* **추천 종목:** **MP Materials (MP)**, **Lynas Rare Earths (LYSCF)**
* **매수 트리거 (WHEN TO BUY):** 중국 수출 통제 발표 직후 주가 갭상승 초기.

#### 시나리오 2: EIA 원유 재고 급감 & OPEC+ 감산 연장
* **상황 조건 (IF):** EIA 주간 원유 재고 400만 바렐 이상 감소 AND OPEC+ 감산 연장 합의.
* **입체적 분석 (WHY):** 유가 $90 상방 돌파 및 정유사 잉여현금흐름(FCF) 폭증.
* **추천 종목:** **Exxon Mobil (XOM)**, **Occidental Petroleum (OXY)**

---

### 5.2 🛑 사용자 포트폴리오 진단 및 매도(Sell / Exit) 추천 알고리즘

사용자가 **[보유 종목, 평균 매수가, 보유 수량]**을 입력하면, 자원 재고 급증·OPEC 감산 해제 등 자원 수급 반전 악재를 대입하여 대응책을 제시합니다.

#### 4대 매도 평가 레이어:

1. **자원 수급 반전 악재 시그널 (Commodity Supply Shift):**
   * **예시 (에너지주 XOM 보유 시):** OPEC+의 기습 증산 합의 또는 EIA 원유 재고 폭증 시 $\rightarrow$ `[유가 하락 우려 - 익절/비중 축소 경고]`

2. **비정형 재난/전염병/기후 악재 시그널:**
   * **예시 (항공주 보유 시):** WHO 보건 경보 발령 시 $\rightarrow$ `[매도 경고]`

3. **신용 위험 & 환율 발작 (FX & Volatility Crisis):**
   * **예시:** USD/JPY 급락(엔캐리 청산) 시 $\rightarrow$ `[기술주 위험 관리]`

4. **동적 익절/손절 & 모멘텀 소멸:**
   * **수익 목표 (Take-Profit):** $+20\%$ 분할 익절.
   * **손절 (Stop-Loss):** $-7\%$ 도달 시 원인 판별 후 자동 가이드 발송.

---

## 6. 📐 시스템 아키텍처 (System Architecture)

```
 [7대 다차원 데이터 원천 (100% 무료/저비용)]
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
 ├── 7대 레이어 자원/거시 리스크 종합 평가 (0~100 점수화)
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
 ├── 오늘의 시장 7대 종합 온도계 대시보드 (자원수급 레이더 포함)
 ├── 입체적 종목 추천 리포트 (매수 타이밍 + 자원/정책/기후 리스크)
 ├── 내 포트폴리오 매도 타이밍 진단 탭
 └── 텔레그램 / Discord / 웹 푸시 알림
```

---

## 7. 🖥️ 초보자를 위한 UI/UX 화면 구성 안 (StockLatte Dashboard)

1. **오늘의 글로벌 시장 7대 종합 온도계 (Market Thermometer)**
   * `🔴 자원 수급/무기화: 경계 (중국 희토류 수출 규제 & EIA 원유 재고 급감 ⚠️)`
   * `🔴 지정학 리스크: 높음 (중동 분쟁 변동성 ⚠️)`
   * `🟡 환율/통화 리스크: 주의 (엔화 강세 전환 ⚠️ 엔캐리 청산 경계)`
   * `🔵 무역/통상 규제: 보통 (미 대중 반도체 추가 제재 발표)`
   * `🟢 금리/인플레: 안정 (FOMC 금리 인하 가능성 80%)`
   * `🟢 비정형 보건/기후: 양호 (전염병 경보 없음)`
   * `🟢 신용/변동성: 양호 (VIX 22.5 / 하이일드 스프레드 안정)`

2. **[NEW] 내 포트폴리오 매도 진단 카드 (Portfolio Sell Assistant)**
   * **입력 예시:** Ticker `MP` (MP 마테리얼즈) | 평단가 `$15.20` | 현재가 `$19.80` (수익률 `+30.26%`)
   * **진단 결과:** `🟢 [목표 수익 달성 - 50% 분할 익절 권장]`
   * **입체적 분석 사유:**
     1. 중국 희토류 수출 규제 이슈로 주가 $+30\%$ 폭등 완료.
     2. 목표 수익률(+20%)을 크게 상회하였으며 단기 차익 실현 물량 출회 가능성 고조.
     3. **추천 대응:** 현 시점에서 보유 수량의 50%를 익절하여 이익을 확정하고, 잔여 수량은 트레일링 스탑 $18.50 설정 권장.

---

## 8. 🛠️ 단계별 개발 로드맵 (Milestones)

### Phase 1: 7대 데이터 수집 파이프라인 구축 (1~2주)
* Python 기반 자원 수급 (EIA, USGS, USDA, LME), 거시지표, GDP, M2, VIX, WHO, FX 파이프라인 구축 (`yfinance`, `fredapi`, `feedparser`).
* 사용자 평단가 기반 매도(Sell) 시그널 파이프라인 및 테스트 케이스 구축 (`tests/` 및 `test_results/`).

### Phase 2: AI (Gemini) All-in-One Context Matrix Prompt 연동 (2~3주)
* JSON 형태의 All-in-One Context Matrix를 Gemini Free Tier API에 전달하여 종합 진단 리포트 자동 생성.

### Phase 3: Web Dashboard & 실시간 알림 서비스 구축 (3~4주)
* HTML/Vanilla CSS/JavaScript (또는 Vite React) 기반의 7대 시장 온도계 및 포트폴리오 매도 진단 대시보드 구축.

---

## 9. 📚 참고 문헌 및 데이터 API (References)

1. **U.S. Energy Information Administration (EIA):** https://www.eia.gov/ (원유/가스 생산, 재고, 수출입 무료 API)
2. **U.S. Geological Survey (USGS):** https://www.usgs.gov/ (희토류/리튬/핵심 광물 생산량 및 매장량 통계)
3. **USDA WASDE (World Agricultural Supply and Demand Estimates):** https://www.usda.gov/ (세계 곡물 수급 및 재고 보고서)
4. **Global Trade Alert:** https://www.globaltradealert.org/ (전 세계 자원 수출 제한 및 무역 제재 데이터)
5. **FRED (Federal Reserve Economic Data):** https://fred.stlouisfed.org/ (GDP, M2, PCE, 신용스프레드, 금리차, 실업수당 무료 API)
6. **Yahoo Finance API (`yfinance`):** https://pypi.org/project/yfinance/ (주가, 원자재, VIX, MOVE, FX 시세)
7. **WHO Disease Outbreak News:** https://www.who.int/emergencies/disease-outbreak-news (전염병 보건 경보 RSS)
8. **Geopolitical Risk (GPR) Index:** https://www.matteoiacoviello.com/gpr.htm (지정학 리스크 지수 데이터)
