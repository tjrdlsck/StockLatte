# 📈 [StockLatte] 글로벌 거시경제·통상정책·환율 및 지정학 모니터링 기반 미국 주식 추천 시스템 상세 설계서

> **작성일자:** 2026년 7월 22일 (다차원 통상·환율·무역 제재 파이프라인 확장)  
> **작성자:** 글로벌 미국 주식 수석 트레이더 & AI 시스템 아키텍트  
> **문서 목적:** 전쟁 등 지정학적 리스크뿐만 아니라 **무역 제재, 수출 제한, 환율 변동성(엔캐리/위안화), 통상 정책, 공급망 병목** 등 다차원 글로벌 경제 지표를 실시간 수집하여, LLM이 입체적이고 정밀한 **"미국 주식 매수/매도 시나리오"**를 도출하는 가성비 최고의 자동화 서비스 구축  

---

## 1. 🎯 프로젝트 개요 및 배경

### 1.1 배경 및 문제 정의
* **복합적 거시 리스크 (Multi-Dimensional Macro Risks):** 글로벌 주식 시장은 단순히 '전쟁(지정학)'이나 '금리' 하나만으로 움직이지 않습니다. **미·중 무역 제재(수출 제한), 인플레이션 감축법(IRA)/반도체법(CHIPS Act), 환율 변동(엔 캐리 트레이드 청산, 달러 강세), 공급망 병목** 등이 복합적으로 작용합니다.
* **경제 지식 진입 장벽:** 일반 투자자는 "미국의 반도체 수출 제한(BIS 제재)이 인텔, ASML, NVDA 중 어디에 호재이고 어디에 악재인가?", "엔화 강세(엔 캐리 언와인딩)가 왜 미국 기술주 폭락을 일으키는가?"와 같은 **복잡한 정책·환율·지정학 인과관계**를 분석하기 어렵습니다.
* **LLM 판단력 극대화의 필요성:** LLM(대형 언어 모델)에게 단순 뉴스 기사만 입력하면 차원 낮은 답변이 나옵니다. **[금리+환율+무역제재/정책+지정학+원자재+공급망]** 데이터가 정제된 다차원 데이터 매트릭스(Context Matrix)로 제공되어야만 전문 트레이더 수준의 날카로운 분석이 가능합니다.
* **해결책:** 무료/저비용 고품질 API를 활용하여 **환율, 무역제재, 지정학, 거시지표, 공급망** 데이터를 입체적으로 자동 수집·정제하고, 사용자 포트폴리오 평단가와 연동하여 **"정밀 매수 추천 + 포트폴리오 매도(익절·손절) 가이드"**를 제공합니다.

---

## 2. 🧠 전문 트레이더 관점의 5대 핵심 분석 레이어 (Top-Down Multi-Layer Approach)

```mermaid
flowchart TD
    A[1. 거시경제/금리/환율 (FX & Rates)] --> F[LLM 다차원 Context Matrix Engine]
    B[2. 지정학/전쟁 리스크 (Geopolitics)] --> F
    C[3. 무역 제재/수출 제한/통상 정책 (Trade & Policy)] --> F
    D[4. 공급망 & 원자재 지수 (Supply Chain & Commodities)] --> F
    E[5. 사용자 보유 포트폴리오 (Ticker & 평단가)] --> F
    F --> G[입체적 매수 추천 & 매도 타이밍 신호 발송]
```

---

## 3. 🌐 다차원 고품질 데이터 수집 파이프라인 (Data Source Matrix)

비용은 100% 무료 또는 저비용 티어로 유지하면서, LLM의 판단 정확도를 극대화하기 위해 모니터링 범위를 **환율, 무역 통상, 공급망 지수**까지 대폭 확장했습니다.

| 분류 | 핵심 지표 / 데이터 | 데이터 출처 (Data Source) | 비용 | 파급 효과 및 트레이더 해석 |
| :--- | :--- | :--- | :--- | :--- |
| **환율 & 통화 (FX)** | **DXY (달러 인덱스)<br>USD/JPY (엔/달러)<br>USD/CNY (위안/달러)** | **Yahoo Finance** (`yfinance`) / **FRED API** | **100% 무료** | · **엔화 강세:** 엔 캐리 트레이드 청산 시 기술주 글로벌 매도세 경보<br>· **달러 강세:** 다국적 기업(Big Tech) 해외 매출 평가절하 우려<br>· **위안화 약세:** 중국 경기 둔화 및 대중 수출 기업 부담 |
| **무역 제재 & 수출 제한** | **미 BIS 제재 뉴스<br>CHIPS Act / IRA 정책<br>대중국 기술 수출 규제** | **US Federal Register RSS<br>Google News RSS** | **100% 무료** | · **반도체 장비 수출 제한:** ASML, AMAT 단기 악재 vs 미 파운드리(INTEL) 반사이익<br>· **희토류/배터리 수출 통제:** 전기차(TSLA), 2차전지 공급망 타격 |
| **공급망 & 물류** | **GSCPI (글로벌 공급망 압력 지수)<br>BDI (발틱 운임 지수)** | **NY Fed Open Data<br>Investing.com Scraping** | **100% 무료** | · **공급망 압력 증가:** 유통/제조업체 마진 압박 및 물가 재상승<br>· **해운 운임 폭등:** 공급망 차질로 재고 비용 증가 |
| **거시경제 & 금리** | **미 기준금리 (FEDFUNDS)<br>10년물 국채금리 (DGS10)<br>CPI / PPI / NFP** | **FRED API** (`fredapi`) | **100% 무료** | · **10년물 금리 상승:** 성장주/Big Tech 밸류에이션 부담<br>· **CPI 하락:** 연준 금리 인하 기대감 상승 (Risk-On) |
| **지정학 & 원자재** | **GPR Index (지정학 지수)<br>WTI 원유 / 천연가스 / 구리** | **GPR Direct CSV / yfinance** | **100% 무료** | · **구리(Dr. Copper) 상승:** 글로벌 경기 회복 시그널<br>· **원유/가스 급등:** 정유주(XOM) 수혜, 항공/소비재 악재 |

---

## 4. 🤖 LLM 주입용 다차원 프롬프트 구조 (LLM Context Matrix Architecture)

LLM이 트레이더처럼 고차원적 판단을 내릴 수 있도록 뉴스 한 줄이 아닌 **종합 상태 매트릭스**를 JSON 형태로 구성하여 Prompt로 제공합니다.

### 4.1 LLM 입력 데이터 구조 예시 (JSON Schema)
```json
{
  "macro_environment": {
    "us_10y_yield": "4.25% (하락세)",
    "dxy_dollar_index": "104.2 (약세 전환)",
    "usd_jpy_rate": "152.5 (엔화 강세 전환 ⚠️ 엔캐리 청산 경계)",
    "gscpi_supply_chain_index": "+0.45 (공급망 원활)"
  },
  "policy_and_trade_news": [
    "미 상무부, 대중국 첨단 AI 반도체 및 HBM 수출 제한 규제 강화 발표",
    "EU, 중국산 전기차 추가 상계관세 최종 확정"
  ],
  "geopolitics_and_commodities": {
    "gpr_index": "145 (중동 긴장 상태)",
    "wti_crude_oil": "$86.50 (상승세)",
    "copper_price": "$4.50 (상승세)"
  },
  "user_portfolio": [
    {"ticker": "NVDA", "avg_cost": 115.0, "current_price": 135.0, "pnl_pct": "+17.39%"},
    {"ticker": "ASML", "avg_cost": 920.0, "current_price": 850.0, "pnl_pct": "-7.61%"}
  ]
}
```

---

## 5. ⚙️ 주가 상승(매수) & 포트폴리오 매도(Exit) 시나리오 엔진

### 5.1 💡 다차원 매수(Buy) 시나리오 예시

#### 시나리오 1: 미·중 반도체 수출 제한 강화 & 미 국내 생산 수혜
* **상황 조건 (IF):** 미 상무부 대중 반도체 수출 규제 강화 발표 AND 미 국내 반도체 보조금(CHIPS Act) 집행.
* **입체적 분석 (WHY):** 중국 비중이 높은 설계/장비사(ASML)는 단기 차질을 겪으나, 미국 내 파운드리 및 반도체 장비 제조업체는 정책적 지원과 수주 독점으로 하방 지지 형성.
* **추천 종목:** **Intel (INTEL)**, **Applied Materials (AMAT)**
* **매수 트리거 (WHEN TO BUY):** 관련 정책 세부안 발표 및 10년물 국채 금리 안정화 시.

#### 시나리오 2: 엔화 강세 전환(엔 캐리 언와인딩) & 원자재/안전자산 부각
* **상황 조건 (IF):** 일본 은행(BOJ) 금리 인상으로 USD/JPY 급락(엔화 강세) AND DXY 달러 인덱스 약세.
* **입체적 분석 (WHY):** 엔 캐리 트레이드 자금이 회수되면서 고평가된 Big Tech 성장주는 단기 조정 조성을 받는 반면, 달러 약세로 인해 원자재/금(Gold) 가격 상승.
* **추천 종목:** **SPDR Gold Shares (GLD)**, **Freeport-McMoRan (FCX - 구리)**

---

### 5.2 🛑 사용자 포트폴리오 진단 및 매도(Sell / Exit) 추천 알고리즘

사용자가 **[보유 종목, 평균 매수가, 보유 수량]**을 입력하면, 환율/정책/지정학 리스크를 입체적으로 대입하여 대응 전략을 제시합니다.

#### 매도 평가 3대 다차원 레이어:

1. **정책 및 통상 악재 전환 (Policy/Trade Risk Signal):**
   * **예시 (ASML/NVDA 보유 시):** 대중 수출 제한 규제 기습 발표 시 $\rightarrow$ `[단기 비중 축소 / 손절 고려 경고]`
   * **예시 (전기차 보유 시):** IRA 보조금 폐지/축소 법안 발의 시 $\rightarrow$ `[매도 진단 보고서 제공]`

2. **환율 및 글로벌 유동성 경보 (FX & Liquidity Alarm):**
   * **엔 캐리 언와인딩 경보:** USD/JPY 일간 2% 이상 하락 시 $\rightarrow$ 보유 중인 고P/E 기술주에 대해 `[트레일링 스탑 타이트 설정]` 권고.

3. **동적 익절/손절 & 모멘텀 소멸:**
   * **수익 목표 (Take-Profit):** 평단가 대비 $+20\%$ 달성 시 분할 매도(50%) 안내.
   * **손절 (Stop-Loss):** 평단가 대비 $-7\%$ 도달 시 원인 분석(일시적 악재 vs 구조적 악재)과 함께 대응책 발송.

---

## 6. 📐 시스템 아키텍처 (System Architecture)

```
 [다차원 데이터 원천 (100% 무료/저비용)]
 ├── FRED API (금리, CPI, 환율, 고용)
 ├── Yahoo Finance (주가, 원자재, DXY, USD/JPY, USD/CNY)
 ├── GPR Index & GSCPI (지정학 & 뉴욕연준 공급망 지수)
 ├── US Federal Register & Google News RSS (무역제재, 수출제한)
 └── Economic & Policy Calendar
        │
        ▼
 [Data Ingestion & Multi-Dimensional Matrix Builder]
        │
        ▼
 [AI Analysis Engine (Gemini Context Matrix Prompt)]
 ├── 다차원 거시/지정학/정책 리스크 종합 평가 (0~100 점수화)
 ├── 센티먼트 및 인과관계 매핑 (Bullish / Neutral / Bearish)
 └── 매수 및 매도 진단 보고서 자동 작성
        │
        ▼
 [Rule & Trigger Engine]
 ├── If-Then 매수 시나리오 매칭
 └── 사용자 포트폴리오 매도(Sell) 시그널 진단기
        │
        ▼
 [StockLatte UI / Notification System]
 ├── 오늘의 시장 온도계 대시보드 (금리/지정학/환율/통상 4대 레이더)
 ├── 입체적 종목 추천 리포트 (매수 타이밍 + 정책/환율 리스크)
 ├── 내 포트폴리오 매도 타이밍 진단 탭
 └── 텔레그램 / Discord / 웹 푸시 알림
```

---

## 7. 🖥️ 초보자를 위한 UI/UX 화면 구성 안 (StockLatte Dashboard)

1. **오늘의 글로벌 시장 4대 종합 온도계 (Market Thermometer)**
   * `🔴 지정학 리스크: 높음 (중동 유가 변동성 ⚠️)`
   * `🟡 환율/통화 리스크: 주의 (엔화 강세 전환 ⚠️ 엔캐리 청산 경계)`
   * `🔵 무역/통상 규제: 보통 (미 대중 반도체 추가 제재 발표)`
   * `🟢 금리/인플레: 안정 (FOMC 금리 인하 가능성 80%)`
   * `오늘의 추천 키워드: #반도체정책 #구리 #안전자산`

2. **[NEW] 내 포트폴리오 매도 진단 카드 (Portfolio Sell Assistant)**
   * **입력 예시:** Ticker `ASML` | 평단가 `$920.00` | 현재가 `$850.00` (수익률 `-7.61%`)
   * **진단 결과:** `🔴 [구조적 정책 악재 - 손절/비중 축소 고려]`
   * **입체적 분석 사유:**
     1. 미 상무부의 대중국 DUV 노광장비 수출 통제 규제 강화 확정.
     2. ASML 중국 매출 비중(약 40%) 감소에 따른 내년 EPS 하향 조정 불가피.
     3. **추천 대응:** 단순 반등 대기보다 손절 라인(-7% 상회)에 따라 비중 50% 감축 후 미 국내 생산 반도체(INTEL, AMAT)로 교체 매매 권장.

---

## 8. 🛠️ 단계별 개발 로드맵 (Milestones)

### Phase 1: 다차원 데이터 수집 & 포트폴리오 엔진 구축 (1~2주)
* Python 기반 거시 지표, 환율(DXY, USD/JPY, USD/CNY), 무역제재 뉴스, GSCPI 파이프라인 구축 (`yfinance`, `fredapi`, `feedparser`).
* 사용자 평단가 기반 매도(Sell) 시그널 파이프라인 및 테스트 케이스 구축 (`tests/` 및 `test_results/`).

### Phase 2: AI (Gemini) 다차원 Context Matrix Prompt 연동 (2~3주)
* JSON 형태의 Multi-Dimensional Context Matrix를 Gemini Free Tier API에 전달하여 수석 트레이더 수준의 종합 진단 리포트 자동 생성.

### Phase 3: Web Dashboard & 실시간 알림 서비스 구축 (3~4주)
* HTML/Vanilla CSS/JavaScript (또는 Vite React) 기반의 4대 시장 온도계 및 포트폴리오 매도 진단 대시보드 구축.

---

## 9. 📚 참고 문헌 및 데이터 API (References)

1. **FRED (Federal Reserve Economic Data):** https://fred.stlouisfed.org/ (미국 금리, 인플레이션, 환율 데이터)
2. **Yahoo Finance API (`yfinance`):** https://pypi.org/project/yfinance/ (주가, 원자재, FX 시세)
3. **NY Fed GSCPI (Global Supply Chain Pressure Index):** https://www.newyorkfed.org/research/policy/gscpi (공급망 압력 지수)
4. **U.S. Federal Register (BIS Export Regulations):** https://www.federalregister.gov/ (미국 무역 제재/수출 통제 관보)
5. **Geopolitical Risk (GPR) Index:** https://www.matteoiacoviello.com/gpr.htm (지정학 리스크 지수 데이터)
