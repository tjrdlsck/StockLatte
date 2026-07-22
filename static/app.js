document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const totalPortfolioValueEl = document.getElementById("total-portfolio-value");
    const totalCashValueEl = document.getElementById("total-cash-value");
    const alertCardContainer = document.getElementById("alert-card-container");
    const alertStatusText = document.getElementById("alert-status-text");
    const alertSubtext = document.getElementById("alert-subtext");

    const positionsListEl = document.getElementById("positions-list");
    const rebalanceGuideContainer = document.getElementById("rebalance-guide-container");
    const jsonOutputContent = document.getElementById("json-output-content");

    const btnOpenModal = document.getElementById("btn-open-modal");
    const btnCloseModal = document.getElementById("btn-close-modal");
    const btnCancelModal = document.getElementById("btn-cancel-modal");
    const btnResetData = document.getElementById("btn-reset-data");
    const btnCopyJson = document.getElementById("btn-copy-json");
    const editModal = document.getElementById("edit-modal");
    const portfolioForm = document.getElementById("portfolio-form");
    const modalPositionsRows = document.getElementById("modal-positions-rows");
    const btnAddPositionRow = document.getElementById("btn-add-position-row");

    let currentPortfolio = null;

    // Fetch and render full dashboard
    async function loadDashboard() {
        try {
            const resPort = await fetch("/api/portfolio");
            const dataPort = await resPort.json();

            const resRebal = await fetch("/api/rebalance", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({})
            });
            const dataRebal = await resRebal.json();

            currentPortfolio = dataPort;
            renderSummary(dataPort);
            renderPositions(dataPort.positions);
            renderRebalanceGuide(dataRebal);
            renderLlmJson(dataRebal.llm_json);
        } catch (err) {
            console.error("대시보드 데이터를 로드하는 중 오류가 발생했습니다:", err);
        }
    }

    // Render Summary Section
    function renderSummary(data) {
        totalPortfolioValueEl.textContent = `$${data.total_value.toLocaleString("en-US", { minimumFractionDigits: 2 })}`;
        totalCashValueEl.textContent = `$${data.cash.toLocaleString("en-US", { minimumFractionDigits: 2 })}`;

        if (data.overweight_alerts && data.overweight_alerts.length > 0) {
            alertCardContainer.classList.add("has-alert");
            const alerts = data.overweight_alerts.map(a => `${a.ticker} (${a.current_weight.toFixed(1)}%)`).join(", ");
            alertStatusText.textContent = `⚠️ 비중 쏠림: ${alerts}`;
            alertSubtext.textContent = "목표 대비 과도하게 비중이 쏠렸습니다. 차익 실현 리밸런싱 권장";
        } else {
            alertCardContainer.classList.remove("has-alert");
            alertStatusText.textContent = "✅ 이상 없음 (정상)";
            alertSubtext.textContent = "종목별 자산 배분이 안전 범위 내에 유지되고 있습니다.";
        }
    }

    // Render Positions List
    function renderPositions(positions) {
        positionsListEl.innerHTML = "";

        positions.forEach(pos => {
            const isOverweight = pos.current_weight >= 35.0 || (pos.current_weight - pos.target_weight >= 10.0);
            
            const item = document.createElement("div");
            item.className = "position-item";

            item.innerHTML = `
                <div class="pos-top">
                    <div>
                        <span class="ticker-name">${pos.ticker}</span>
                        ${isOverweight ? '<span class="badge badge-info" style="margin-left: 8px; background: rgba(244, 63, 94, 0.2); color: #f43f5e; border-color: rgba(244, 63, 94, 0.4);">⚠️ 쏠림</span>' : ''}
                    </div>
                    <div class="pos-value-box">
                        <div class="pos-market-value">$${pos.market_value.toLocaleString("en-US", { minimumFractionDigits: 2 })}</div>
                        <div class="pos-price-qty">${pos.quantity}주 @ $${pos.current_price.toFixed(2)}</div>
                    </div>
                </div>
                <div class="progress-container">
                    <div class="progress-info">
                        <span>현재 비중: <strong>${pos.current_weight.toFixed(1)}%</strong></span>
                        <span>목표 비중: ${pos.target_weight.toFixed(1)}%</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill ${isOverweight ? 'overweight' : ''}" style="width: ${Math.min(pos.current_weight, 100)}%;"></div>
                    </div>
                </div>
            `;
            positionsListEl.appendChild(item);
        });
    }

    // Render Rebalancing Guide
    function renderRebalanceGuide(rebalData) {
        rebalanceGuideContainer.innerHTML = "";

        const actions = rebalData.actions || [];
        const sellActions = actions.filter(a => a.action_type === "SELL");
        const buyActions = actions.filter(a => a.action_type === "BUY");

        if (actions.length === 0) {
            rebalanceGuideContainer.innerHTML = `
                <div class="guide-card">
                    <div class="guide-step-title">🎉 리밸런싱 불필요</div>
                    <div class="guide-action-text">현재 모든 종목이 목표 비중에 완벽히 일치합니다.</div>
                </div>
            `;
            return;
        }

        // Sell High Card
        if (sellActions.length > 0) {
            const sellCard = document.createElement("div");
            sellCard.className = "guide-card sell-high";
            let sellHtml = `<div class="guide-step-title sell">📉 1단계: 차익 실현 (Sell High)</div>`;
            sellActions.forEach(act => {
                sellHtml += `
                    <div class="guide-action-text" style="margin-bottom: 4px;">
                        • <strong>${act.ticker}</strong> 주식 $${act.amount.toLocaleString("en-US", { minimumFractionDigits: 2 })}치 (약 ${act.shares}주) 차익 실현 
                        ➔ 비중 ${act.new_weight}%로 재정렬
                    </div>
                `;
            });
            sellCard.innerHTML = sellHtml;
            rebalanceGuideContainer.appendChild(sellCard);
        }

        // Buy Low Card
        if (buyActions.length > 0) {
            const buyCard = document.createElement("div");
            buyCard.className = "guide-card buy-low";
            let buyHtml = `<div class="guide-step-title buy">📈 2단계: 저점 재투자 (Buy Low)</div>`;
            buyActions.forEach(act => {
                buyHtml += `
                    <div class="guide-action-text" style="margin-bottom: 4px;">
                        • 차익 실현금으로 <strong>${act.ticker}</strong> $${act.amount.toLocaleString("en-US", { minimumFractionDigits: 2 })}치 추가 매수 (약 ${act.shares}주)
                    </div>
                `;
            });
            buyHtml += `<div class="card-subtext" style="margin-top: 8px;">➔ 확정 이익으로 저평가 코어 우량주 분산 재투자 완벽 완료!</div>`;
            buyCard.innerHTML = buyHtml;
            rebalanceGuideContainer.appendChild(buyCard);
        }
    }

    // Render LLM JSON
    function renderLlmJson(jsonStr) {
        jsonOutputContent.textContent = jsonStr;
    }

    // Copy JSON to Clipboard
    btnCopyJson.addEventListener("click", () => {
        const jsonText = jsonOutputContent.textContent;
        navigator.clipboard.writeText(jsonText).then(() => {
            alert("LLM 주입용 JSON 프롬프트가 클립보드에 복사되었습니다! 📋");
        }).catch(err => {
            console.error("클립보드 복사 실패:", err);
        });
    });

    // Reset Data
    btnResetData.addEventListener("click", async () => {
        if (confirm("기초 예시 시나리오 데이터로 포트폴리오를 초기화하시겠습니까?")) {
            await fetch("/api/reset", { method: "POST" });
            loadDashboard();
        }
    });

    // Modal Control
    function openModal() {
        if (!currentPortfolio) return;

        document.getElementById("input-cash").value = currentPortfolio.cash;
        modalPositionsRows.innerHTML = "";

        currentPortfolio.positions.forEach(pos => {
            addModalPositionRow(pos.ticker, pos.quantity, pos.current_price, pos.target_weight);
        });

        editModal.classList.add("active");
        editModal.setAttribute("aria-hidden", "false");
    }

    function closeModal() {
        editModal.classList.remove("active");
        editModal.setAttribute("aria-hidden", "true");
    }

    function addModalPositionRow(ticker = "", qty = 0, price = 0, targetWeight = 0) {
        const row = document.createElement("div");
        row.className = "modal-position-row";
        row.innerHTML = `
            <input type="text" placeholder="티커 (예: NVDA)" class="pos-ticker" value="${ticker}" required>
            <input type="number" step="0.1" placeholder="수량" class="pos-qty" value="${qty}" required>
            <input type="number" step="0.01" placeholder="현재가 ($)" class="pos-price" value="${price}" required>
            <input type="number" step="0.1" placeholder="목표비중 (%)" class="pos-target" value="${targetWeight}" required>
            <button type="button" class="btn btn-sm btn-secondary btn-remove-row" style="color: #f43f5e;">&times;</button>
        `;

        row.querySelector(".btn-remove-row").addEventListener("click", () => {
            row.remove();
        });

        modalPositionsRows.appendChild(row);
    }

    btnOpenModal.addEventListener("click", openModal);
    btnCloseModal.addEventListener("click", closeModal);
    btnCancelModal.addEventListener("click", closeModal);
    btnAddPositionRow.addEventListener("click", () => addModalPositionRow());

    // Submit Portfolio Form
    portfolioForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const cash = parseFloat(document.getElementById("input-cash").value) || 0.0;
        const rows = modalPositionsRows.querySelectorAll(".modal-position-row");

        const positions = [];
        const targetWeights = {};

        rows.forEach(r => {
            const ticker = r.querySelector(".pos-ticker").value.trim().toUpperCase();
            const qty = parseFloat(r.querySelector(".pos-qty").value) || 0;
            const price = parseFloat(r.querySelector(".pos-price").value) || 0;
            const target = parseFloat(r.querySelector(".pos-target").value) || 0;

            if (ticker) {
                positions.push({ ticker, quantity: qty, current_price: price });
                targetWeights[ticker] = target;
            }
        });

        const newPortfolioData = {
            positions,
            cash,
            target_weights: targetWeights
        };

        await fetch("/api/portfolio", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newPortfolioData)
        });

        closeModal();
        loadDashboard();
    });

    // Initial Load
    loadDashboard();
});
