from typing import Dict, List, Optional
import yfinance as yf


class StockDataProvider:
    """
    미국 주식 실시간 주가 및 평가 금액 데이터를 수집하는 Data Provider
    """

    def __init__(self, mock_prices: Optional[Dict[str, float]] = None):
        """
        :param mock_prices: 네트워크 연결 없이 테스트 시 사용할 티커별 주가 딕셔너리
        """
        self.mock_prices = mock_prices or {}

    def fetch_current_prices(self, tickers: List[str]) -> Dict[str, float]:
        """
        주어진 티커 목록의 현재가($)를 조회합니다.
        
        :param tickers: 티커 리스트 (예: ['NVDA', 'MSFT', 'CAT'])
        :return: {티커: 현재가} 딕셔너리
        """
        prices = {}
        for ticker in tickers:
            if ticker in self.mock_prices:
                prices[ticker] = self.mock_prices[ticker]
                continue

            try:
                stock = yf.Ticker(ticker)
                # fast_info 또는 history를 통한 현재가 파싱
                info_price = getattr(stock.fast_info, 'last_price', None)
                if info_price is not None:
                    prices[ticker] = round(float(info_price), 2)
                else:
                    hist = stock.history(period="1d")
                    if not hist.empty:
                        prices[ticker] = round(float(hist['Close'].iloc[-1]), 2)
                    else:
                        prices[ticker] = 0.0
            except Exception:
                # 오프라인 또는 오류 발생 시 0.0 처리
                prices[ticker] = 0.0

        return prices
