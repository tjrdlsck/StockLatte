# 📈 [StockLatte] 올인원 거시경제·재무제표·CapEx·자원수급·정책·환율·비정형 리스크 모니터링 기반 미국 주식 추천 시스템 상세 설계서

> **작성일자:** 2026년 7월 22일 (기업 재무제표·펀더멘털·밸류에이션 파이프라인 최종 완비)  
> **작성자:** 글로벌 미국 주식 수석 트레이더 & AI 시스템 아키텍트  
> **문서 목적:** 거시지표/지정학/CapEx뿐만 아니라 **개별 기업 재무제표(손익계산서, 재무상태표, 현금흐름표), 잉여현금흐름(FCF), 부채비율, 밸류에이션(PER/PBR/PSR), 전방 B2B 수요, 자원 수급, 환율, 신용스프레드** 등 기업 펀더멘털과 주가를 결정짓는 모든 지표를 실시간 수집하여, LLM이 **"미국 주식 매수/매도 시나리오"**를 입체적으로 도출하는 완벽한 올인원 자동화 서비스 구축  

---

## 1. 🎯 프로젝트 개요 및 배경

### 1.1 배경 및 문제 정의
* **기업 재무제표 및 펀더멘털의 필수성 (Financial Statements & Fundamental Analysis):** 아무리 거시경제 호재나 AI/지정학 테마가 불어오더라도, **부채비율이 과도하여 파산 위험이 있거나, 잉여현금흐름(FCF)이 적자이거나, P/E(PER) 밸류에이션이 극단적 과열 상태인 기업**을 매수하면 대형 손실로 이어집니다.
* **초보 투자자의 한계:** 개인이 SEC 공시(10-Q/10-K) 및 재무제표 3대 항목(손익계산서, 재무상태표, 현금흐름표)을 해석하고, PER/PBR/FCF/영업이익률을 거시 지표와 결합하여 적정 주가를 판단하는 것은 매우 어렵습니다.
* **LLM 판단력의 완전성 (Completeness of LLM Input):** 개별 기업의 **재무 펀더멘털 건전성(부채비율 < 100%, FCF 양수, 영업이익률 개선)** 데이터가 주입되어야만 LLM이 부실주를 스크리닝하고 안전하고 확실한 우량주만을 추천할 수 있습니다.
* **해결책:** 100% 무료 데이터 원천(`yfinance`, `SEC EDGAR API`)을 활용해 재무제표 및 밸류에이션 지표를 정제하여 **All-in-One Context Matrix**로 구축합니다.

---

## 2. 🧠 전문 트레이더 관점의 9대 종합 분석 레이어 (All-in-One Multi-Layer Approach)

```mermaid
flowchart TD
    A[1. 개별 기업 재무제표 & 펀더멘털 (yfinance, SEC EDGAR: PER, FCF, 부채비율)] --> J[LLM All-in-One Context Matrix]
    B[2. 전방 B2B 수요 & 기업 CapEx (SEC EDGAR, 건설지출, ISM 신규수주)] --> J
    C[3. 자원 수급/생산량/수출입 (EIA, USGS, USDA, LME)] --> J
    D[4. 성장/인플레/정책 (GDP, M2, PCE, 국채발행)] --> J
    E[5. 금융 변동성 & 신용위험 (VIX, MOVE, 하이일드)] --> J
    F[6. 환율 & 무역 제재 (DXY, USD/JPY, BIS 수출통제)] --> J
    G[7. 지정학 & 원자재 (GPR, 유가, 구리, 금)] --> J
    H[8. 비정형 재난 & 기후 (WHO 전염병, NOAA 이상기후)] --> J
    I[9. 기관 수급 & 고용 (CoT, 실업수당, 10Y-2Y 금리차)] --> J
    J --> K[입체적 매수 추천 & 내 포트폴리오 매도 신호 발송]
```

---

## 3. 🌐 올인원 무료 데이터 수집 파이프라인 (All-in-One Data Matrix)

비용은 100% 무료(`yfinance`, `SEC EDGAR API` 등)로 유지하면서 개별 기업의 재무제표와 9대 종합 거시 지표를 정밀하게 수집합니다.

| 분류 | 핵심 지표 / 데이터 | 데이터 출처 (Data Source) | 비용 | 파급 효과 및 트레이더 해석 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 기업 재무제표 & 밸류** | **손익계산서 (매출/영업이익/EPS)**<br>**재무상태표 (부채비율/현금성자산)**<br>**현금흐름표 (잉여현금흐름 FCF)**<br>**PER / PBR / PSR / 배당수익률** | **Yahoo Finance API** (`yfinance`)<br>**SEC EDGAR API** (10-Q/K) | **100% 무료** | · **부채비율 > 200%:** 고금리 시기 부실 위험 스크리닝 제외<br>· **FCF(잉여현금흐름) 양수 & 급증:** 자사주 매입/배당 증액 모멘텀<br>· **PER 역사적 하단:** 저평가 바닥 매수 기회 |
| **2. B2B 수요 & CapEx** | **빅테크 4사 CapEx 지출/가이던스**<br>**미국 총 건설 지출 (`TTLCONS`)**<br>**ISM 제조업 신규수주 지수** | **SEC EDGAR API** (10-Q/K)<br>**FRED API** (`fredapi`) | **100% 무료** | · **Big Tech CapEx 증가:** NVDA, 메모리(MU), 서버/냉각(VRT) 수혜<br>· **건설 지출/가동률 > 80%:** 건설 기계(CAT), 파운드리 인프라 수혜 |
| **3. 자원 생산 & 수출입** | **원유 생산/재고량 (EIA)**<br>**희토류/리튬 매장·생산 (USGS)**<br>**세계 곡물 수급 (USDA WASDE)** | **EIA API** / **USGS**<br>**USDA WASDE** / **LME** | **100% 무료** | · **EIA 원유 재고 감소:** 유가 상승 $\rightarrow$ 정유주(XOM) 수혜<br>· **중국 희토류 수출 규제:** MP Materials(MP) 등 대체 광산 폭등 |
| **4. 자원 통상 & 제재** | **자원 수출 제한 조치**<br>**Global Trade Alert** | **GlobalTradeAlert.org**<br>**OECD Raw Materials** | **100% 무료** | · **자원 무기화 발표:** 공급망 차질 발생으로 수혜 섹터 갭상승<br>· **핵심 광물 관세:** 배터리/전기차(TSLA) 원가 부담 가중 |
| **5. 성장 & 정책 인플레** | **실질 GDP 성장률 (`GDPC1`)**<br>**PCE 물가지수 / M2 통화량** | **FRED API** (`fredapi`) | **100% 무료** | · **2분기 연속 GDP 음수:** 경기 침체 경보<br>· **M2/국채발행 급증:** 정책성 인플레이션 재발 우려 |
| **6. 금융 변동성 & 신용** | **VIX (주가 공포지수)**<br>**MOVE (채권 공포지수)**<br>**High-Yield Credit Spread** | **Yahoo Finance** / **FRED API** (`BAMLH0A0HYM2`) | **100% 무료** | · **VIX > 30:** 시장 패닉 (바닥 매수 기회 탐색)<br>· **신용 스프레드 급등:** 부실 기업 부도 위험 및 금융 위기 시그널 |
| **7. 비정형 재난 & 기후** | **WHO 전염병 경보**<br>**NOAA 이상기후 (엘니뇨/태풍)** | **WHO RSS / NOAA Open Data** | **100% 무료** | · **전염병 경보:** 바이오주 호재, 항공/여행주 급락<br>· **이상 기후/태풍:** 농산물 폭등, 정유공장 가동 중단 |
| **8. 환율 & 무역 제재** | **DXY (달러) / USD/JPY (엔화)**<br>**미 BIS 제재 / CHIPS / IRA** | **yfinance / Federal Register RSS** | **100% 무료** | · **USD/JPY 급락:** 엔 캐리 청산에 따른 기술주 폭락 경보<br>· **수출 제한 제재:** 장비주 악재 vs 미 파운드리 반사이익 |
| **9. 기관 수급 & 고용** | **10Y-2Y 장단기 금리차**<br>**신규 실업수당 청구건수**<br>**CFTC CoT (기관 선물 수급)** | **FRED API** / **CFTC.gov** | **100% 무료** | · **장단기 금리차 역전 후 해제:** 역사적 경기 침체 도래<br>· **실업수당 청구 급증:** 고용 시장 냉각 시그널 |

---

## 4. 🤖 LLM 주입용 올인원 프롬프트 구조 (All-in-One Context Matrix Architecture)

개별 기업 재무제표 펀더멘털과 거시 환경이 결합된 JSON 프롬프트를 생성하여 LLM이 우량주 선별 및 밸류에이션 평가를 내리도록 합니다.

### 4.1 LLM 입력 데이터 구조 예시 (JSON Schema)
```json
{
  "company_financial_fundamentals": {
    "ticker": "MU",
    "income_statement": {
      "revenue_growth_yoy": "+82.5% (매출 폭발적 증가)",
      "operating_margin": "24.2% (영업이익률 급반등)",
      "eps_surprise": "+14.8% (시장 예상치 대폭 상회)"
    },
    "balance_sheet": {
      "debt_to_equity": "38.5% (우수한 재무 건전성)",
      "cash_and_equivalents": "$10.5B"
    },
    "cash_flow_statement": {
      "free_cash_flow_fcf": "+$3.2B (잉여현금흐름 대폭 흑자)",
      "operating_cash_flow": "+$4.8B"
    },
    "valuation_multiples": {
      "forward_pe": "14.2x (역사적 평균 대비 저평가)",
      "peg_ratio": "0.68 (성장성 대비 극저평가)"
    }
  },
  "downstream_b2b_demand_and_capex": {
    "bigtech_ai_capex_guidance": "MSFT, META, GOOGL 2026년 CapEx 전년 대비 +35% 증액 발표"
  },
  "user_portfolio": [
    {"ticker": "MU", "avg_cost": 95.00, "current_price": 135.00, "pnl_pct": "+42.10% (재무건전성 & CapEx 호조 - 보유 추천)"}
  ]
}
```

---

## 5. ⚙️ 주가 상승(매수) & 포트폴리오 매도(Exit) 시나리오 엔진

### 5.1 💡 재무 펀더멘털 & 밸류에이션 기반 매수(Buy) 시나리오 예시

#### 시나리오 1: 잉여현금흐름(FCF) 흑자 전환 & F-PE 15배 이하 턴어라운드
* **상황 조건 (IF):** 영업이익률 흑자 전환 AND 잉여현금흐름(FCF) 양수 돌파 AND 선행 PER(Forward P/E) < 15배.
* **입체적 분석 (WHY):** 재무구조 악화 우려가 해소되고 실적 턴어라운드가 확인되어 밸류에이션 재평가(Re-rating) 진행.
* **추천 종목:** **Micron Technology (MU)**, **Western Digital (WDC)**

---

### 5.2 🛑 사용자 포트폴리오 진단 및 매도(Sell / Exit) 추천 알고리즘

사용자가 **[보유 종목, 평균 매수가, 보유 수량]**을 입력하면, 재무제표 훼손(부채비율 급증, FCF 적자 전환, PER 극단적 과열)을 평가해 손절/익절 타이밍을 제시합니다.

#### 5대 매도 평가 레이어:

1. **재무제표 훼손 경보 (Financial Deterioration Signal):**
   * **예시:** 잉여현금흐름(FCF) 적자 전환 OR 부채비율 200% 초과 $\rightarrow$ `[재무 건전성 악화 - 손절/비중 축소 권고]`

2. **밸류에이션 극단적 과열 (Overvaluation Signal):**
   * **예시:** PSR/PER이 역사적 고점 상단 3표준편차 오버슈팅 시 $\rightarrow$ `[차익 실현 분할 매도 권고]`

3. **전방 산업 CapEx 삭감 및 피크아웃:**
   * **예시:** 빅테크 CapEx 지출 삭감 발표 시 $\rightarrow$ `[익절 권고]`

4. **신용 위험 & 환율 발작:**
   * **예시:** USD/JPY 급락(엔캐리 청산) 시 $\rightarrow$ `[위험 관리]`

5. **동적 익절/손절:**
   * **수익 목표 (+20%) / 손절 라인 (-7%).**

---

## 6. 📐 시스템 아키텍처 (System Architecture)

```
 [9대 다차원 데이터 원천 (100% 무료/저비용)]
 ├── Yahoo Finance & SEC EDGAR (재무제표 3대 항목, FCF, PER/PBR, 부채비율)
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
 ├── 9대 레이어 재무제표/CapEx/거시/자원 리스크 종합 평가 (0~100 점수화)
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
 ├── 오늘의 시장 9대 종합 온도계 대시보드 (재무 펀더멘털 레이더 포함)
 ├── 입체적 종목 추천 리포트 (매수 타이밍 + 재무/CapEx/자원/기후 리스크)
 ├── 내 포트폴리오 매도 타이밍 진단 탭
 └── 텔레그램 / Discord / 웹 푸시 알림
```

---

## 7. 🖥️ 초보자를 위한 UI/UX 화면 구성 안 (StockLatte Dashboard)

1. **오늘의 글로벌 시장 9대 종합 온도계 (Market Thermometer)**
   * `🟢 재무 펀더멘털: 우수 (추천 종목 평균 FCF 흑자 & 부채비율 40% 미만 💎)`
   * `🟢 B2B CapEx/수주: 매우 긍정 (빅테크 AI CapEx +35% 증액 & 건설지출 호조 🚀)`
   * `🔴 자원 수급/무기화: 경계 (중국 희토류 수출 규제 & EIA 원유 재고 급감 ⚠️)`
   * `🔴 지정학 리스크: 높음 (중동 분쟁 변동성 ⚠️)`
   * `🟡 환율/통화 리스크: 주의 (엔화 강세 전환 ⚠️ 엔캐리 청산 경계)`
   * `🔵 무역/통상 규제: 보통 (미 대중 반도체 추가 제재 발표)`
   * `🟢 금리/인플레: 안정 (FOMC 금리 인하 가능성 80%)`
   * `🟢 비정형 보건/기후: 양호 (전염병 경보 없음)`
   * `🟢 신용/변동성: 양호 (VIX 22.5 / 하이일드 스프레드 안정)`

---

## 8. 🛠️ 단계별 개발 로드맵 (Milestones)

### Phase 1: 9대 데이터 수집 파이프라인 구축 (1~2주)
* Python 기반 기업 재무제표 (`yfinance`, `SEC EDGAR API`), B2B CapEx, 자원 수급, 거시지표 파이프라인 구축 (`yfinance`, `fredapi`, `sec-edgar-downloader`, `feedparser`).
* 사용자 평단가 기반 매도(Sell) 시그널 파이프라인 및 테스트 케이스 구축 (`tests/` 및 `test_results/`).

### Phase 2: AI (Gemini) All-in-One Context Matrix Prompt 연동 (2~3주)
* JSON 형태의 All-in-One Context Matrix를 Gemini Free Tier API에 전달하여 종합 진단 리포트 자동 생성.

### Phase 3: Web Dashboard & 실시간 알림 서비스 구축 (3~4주)
* HTML/Vanilla CSS/JavaScript (또는 Vite React) 기반의 9대 시장 온도계 및 포트폴리오 매도 진단 대시보드 구축.

---

## 9. 📚 참고 문헌 및 데이터 API (References)

1. **Yahoo Finance API (`yfinance`):** https://pypi.org/project/yfinance/ (재무제표 3대 항목, PER/PBR, FCF, 주가 시세 100% 무료)
2. **U.S. SEC EDGAR API:** https://www.sec.gov/edgar/sec-api-documentation (미 상장사 공식 10-Q/K 재무제표 공시 API)
3. **FRED (Federal Reserve Economic Data):** https://fred.stlouisfed.org/ (건설 지출, 가동률, GDP, M2, PCE 무료 API)
4. **U.S. Energy Information Administration (EIA):** https://www.eia.gov/ (원유/가스 생산 및 재고 API)
5. **U.S. Geological Survey (USGS):** https://www.usgs.gov/ (희토류/리튬 자원 매장량)
6. **WHO Disease Outbreak News:** https://www.who.int/emergencies/disease-outbreak-news (전염병 보건 경보 RSS)
7. **Geopolitical Risk (GPR) Index:** https://www.matteoiacoviello.com/gpr.htm (지정학 리스크 지수)
