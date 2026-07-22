import pytest
import json
from app import app as flask_app


@pytest.fixture
def client():
    """Flask 테스트 클라이언트 픽스처"""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


def test_index_page(client):
    """대시보드 메인 HTML 응답 검증 테스트"""
    response = client.get('/')
    assert response.status_code == 200
    assert "StockLatte" in response.get_data(as_text=True)


def test_get_portfolio_api(client):
    """포트폴리오 정보 API 조회 테스트"""
    response = client.get('/api/portfolio')
    assert response.status_code == 200
    data = response.get_json()
    assert "total_value" in data
    assert "positions" in data
    assert len(data["positions"]) >= 3
    assert data["total_value"] == 15000.0


def test_rebalance_api(client):
    """스마트 리밸런싱 API 실행 테스트"""
    response = client.post('/api/rebalance', json={})
    assert response.status_code == 200
    data = response.get_json()
    assert "actions" in data
    assert "llm_json" in data
    assert len(data["actions"]) == 3

    # NVDA 매도(SELL), MSFT 매수(BUY), CAT 매수(BUY) 액션 검증
    actions = {a["ticker"]: a for a in data["actions"]}
    assert actions["NVDA"]["action_type"] == "SELL"
    assert actions["NVDA"]["amount"] == 3000.0
    assert actions["MSFT"]["action_type"] == "BUY"
    assert actions["MSFT"]["amount"] == 1000.0
    assert actions["CAT"]["action_type"] == "BUY"
    assert actions["CAT"]["amount"] == 2000.0


def test_update_portfolio_api(client):
    """포트폴리오 포지션 업데이트 API 테스트"""
    new_data = {
        "positions": [
            {"ticker": "NVDA", "quantity": 10, "current_price": 100.0},
            {"ticker": "AAPL", "quantity": 10, "current_price": 200.0}
        ],
        "cash": 1000.0,
        "target_weights": {"NVDA": 50.0, "AAPL": 50.0}
    }
    response = client.post('/api/portfolio', json=new_data)
    assert response.status_code == 200

    # 업데이트 결과 확인
    res_get = client.get('/api/portfolio')
    data = res_get.get_json()
    assert data["total_value"] == 4000.0
    assert len(data["positions"]) == 2
