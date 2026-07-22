from flask import Flask, render_template, request, jsonify
from stocklatte.models import Position, Portfolio
from stocklatte.rebalancing import MarketValueRebalancingEngine
from stocklatte.data_provider import StockDataProvider

app = Flask(__name__)

# 기본 데모 포트폴리오 (제안서 2.1절 예시 반영)
# Total Value: $15,000 (NVDA $7,500 [50%], MSFT $3,500 [23.3%], CAT $4,000 [26.7%])
DEFAULT_PORTFOLIO = {
    "positions": [
        {"ticker": "NVDA", "quantity": 50, "current_price": 150.0},
        {"ticker": "MSFT", "quantity": 10, "current_price": 350.0},
        {"ticker": "CAT", "quantity": 20, "current_price": 200.0}
    ],
    "cash": 0.0,
    "target_weights": {"NVDA": 30.0, "MSFT": 30.0, "CAT": 40.0}
}

# 메모리 상 저장된 현재 포트폴리오
current_portfolio_data = dict(DEFAULT_PORTFOLIO)


def _build_portfolio_object(data_dict: dict) -> Portfolio:
    positions = [
        Position(
            ticker=item["ticker"],
            quantity=float(item["quantity"]),
            current_price=float(item["current_price"])
        )
        for item in data_dict.get("positions", [])
    ]
    cash = float(data_dict.get("cash", 0.0))
    target_weights = {
        k: float(v) for k, v in data_dict.get("target_weights", {}).items()
    }
    return Portfolio(positions=positions, cash=cash, target_weights=target_weights)


@app.route("/")
def index():
    """StockLatte 메인 대시보드 페이지"""
    return render_template("index.html")


@app.route("/api/portfolio", methods=["GET", "POST"])
def portfolio_api():
    """포트폴리오 정보 조회 및 수정 API"""
    global current_portfolio_data

    if request.method == "POST":
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "잘못된 데이터 형식입니다."}), 400
        current_portfolio_data = payload
        return jsonify({"message": "포트폴리오가 성공적으로 업데이트되었습니다."})

    # GET 요청 처리
    portfolio = _build_portfolio_object(current_portfolio_data)
    weights = portfolio.get_current_weights()
    overweights = portfolio.detect_overweight_positions(threshold_pct=35.0)

    positions_detail = []
    for pos in portfolio.positions:
        positions_detail.append({
            "ticker": pos.ticker,
            "quantity": pos.quantity,
            "current_price": pos.current_price,
            "market_value": pos.market_value,
            "current_weight": weights.get(pos.ticker, 0.0),
            "target_weight": portfolio.target_weights.get(pos.ticker, 0.0)
        })

    return jsonify({
        "total_value": portfolio.total_value,
        "cash": portfolio.cash,
        "positions": positions_detail,
        "overweight_alerts": overweights
    })


@app.route("/api/rebalance", methods=["POST"])
def rebalance_api():
    """스마트 리밸런싱 산출 및 LLM JSON 프롬프트 생성 API"""
    global current_portfolio_data

    payload = request.get_json() or current_portfolio_data
    portfolio = _build_portfolio_object(payload)

    engine = MarketValueRebalancingEngine(overweight_threshold_pct=35.0)
    try:
        result = engine.calculate_rebalance(portfolio)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    actions_data = [
        {
            "ticker": act.ticker,
            "action_type": act.action_type,
            "amount": act.amount,
            "shares": act.shares,
            "target_weight": act.target_weight,
            "current_weight": act.current_weight,
            "new_weight": act.new_weight
        }
        for act in result.actions
    ]

    return jsonify({
        "total_portfolio_value": result.total_portfolio_value,
        "target_weights": result.target_weights,
        "actions": actions_data,
        "overweight_alerts": result.overweight_alerts,
        "llm_json": result.to_llm_json()
    })


@app.route("/api/reset", methods=["POST"])
def reset_api():
    """포트폴리오 초기화 API"""
    global current_portfolio_data
    current_portfolio_data = dict(DEFAULT_PORTFOLIO)
    return jsonify({"message": "기초 포트폴리오 데이터로 초기화되었습니다."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
