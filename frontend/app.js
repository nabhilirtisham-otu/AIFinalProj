// Game state
let board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
];
let currentPlayer = "X";
let gameActive = true;
let winnerInfo = null;
let gameMode = "ai";
let selectedDifficulty = "medium";
let useAlphaBeta = true;
let moveHistory = [];

// Win patterns (index 0-8)
const winPatterns = [
    [0,1,2], [3,4,5], [6,7,8],
    [0,3,6], [1,4,7], [2,5,8],
    [0,4,8], [2,4,6]
];

const API_URL = "http://127.0.0.1:5000/make-move";

// Helper: flatten board for win detection
function getFlatBoard() {
    let flat = [];
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            flat.push(board[i][j]);
        }
    }
    return flat;
}

// Check win/draw from current board
function checkGameStatus() {
    const flat = getFlatBoard();
    for (let pattern of winPatterns) {
        const [a,b,c] = pattern;
        if (flat[a] && flat[a] === flat[b] && flat[a] === flat[c]) {
            return { winner: flat[a], winCombo: pattern };
        }
    }
    const isFull = flat.every(cell => cell !== "");
    if (isFull) return { isDraw: true };
    return null;
}

// Update game state after move
function updateGameEnd() {
    const status = checkGameStatus();
    if (status) {
        if (status.winner) {
            gameActive = false;
            winnerInfo = { winner: status.winner, winCombo: status.winCombo };
            renderBoard();
            updateTurnDisplay();
            return true;
        } else if (status.isDraw) {
            gameActive = false;
            winnerInfo = null;
            renderBoard();
            updateTurnDisplay();
            return true;
        }
    }
    return false;
}

// Render board UI
function renderBoard() {
    const cells = document.querySelectorAll(".cell");
    for (let i = 0; i < cells.length; i++) {
        const row = Math.floor(i / 3);
        const col = i % 3;
        const val = board[row][col];
        cells[i].textContent = val;
        cells[i].classList.remove("win");
        if (val === "X") cells[i].style.color = "#2c3e50";
        else if (val === "O") cells[i].style.color = "#e67e22";
    }
    if (winnerInfo && winnerInfo.winCombo) {
        const cells = document.querySelectorAll(".cell");
        winnerInfo.winCombo.forEach(idx => {
            if (cells[idx]) cells[idx].classList.add("win");
        });
    }
    updateClickability();
}

function updateClickability() {
    const cells = document.querySelectorAll(".cell");
    for (let i = 0; i < cells.length; i++) {
        const row = Math.floor(i / 3);
        const col = i % 3;
        const occupied = board[row][col] !== "";
        if (!gameActive || winnerInfo) {
            cells[i].classList.add("disabled");
        } else if (gameMode === "ai" && currentPlayer === "O" && gameActive) {
            cells[i].classList.add("disabled");
        } else if (occupied) {
            cells[i].classList.add("disabled");
        } else {
            cells[i].classList.remove("disabled");
        }
    }
}

function updateTurnDisplay() {
    const turnDiv = document.getElementById("turnStatus");
    if (!gameActive) {
        if (winnerInfo && winnerInfo.winner) {
            turnDiv.innerHTML = winnerInfo.winner + " wins!";
        } else if (getFlatBoard().every(cell => cell !== "")) {
            turnDiv.innerHTML = "Draw! Game over.";
        } else {
            turnDiv.innerHTML = "Game over";
        }
        return;
    }
    if (gameMode === "2player") {
        turnDiv.innerHTML = "Player " + currentPlayer + "'s turn";
    } else {
        if (currentPlayer === "X") {
            turnDiv.innerHTML = "Your turn (X)";
        } else {
            turnDiv.innerHTML = "AI thinking...";
        }
    }
}

// Apply move and switch turn
function applyMove(row, col, player) {
    if (!gameActive) return false;
    if (board[row][col] !== "") return false;
    if (player !== currentPlayer) return false;

    board[row][col] = player;
    moveHistory.push([row, col]);
    renderBoard();

    const ended = updateGameEnd();
    if (ended) {
        updateTurnDisplay();
        return true;
    }

    currentPlayer = currentPlayer === "X" ? "O" : "X";
    updateTurnDisplay();
    renderBoard();
    updateClickability();
    return true;
}

// Reset game
function fullReset() {
    board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ];
    currentPlayer = "X";
    gameActive = true;
    winnerInfo = null;
    moveHistory = [];
    renderBoard();
    updateTurnDisplay();
    updateClickability();
    
    // Clear analytics
    document.getElementById("summaryArea").innerHTML = "—";
    document.getElementById("metricsArea").innerHTML = "—";
    document.getElementById("moveBreakdownArea").innerHTML = "—";
    document.getElementById("explanationArea").innerHTML = "—";
    document.getElementById("pruningArea").innerHTML = "—";
}

// Render analytics from backend response
function renderAnalytics(analysis) {
    if (!analysis) return;

    // Summary
    const summary = analysis.summary || {};
    let summaryHtml = '<div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px;">';
    summaryHtml += '<span><strong>Result:</strong> ' + (summary.result || "—") + '</span>';
    summaryHtml += '<span><strong>Difficulty:</strong> ' + (summary.difficulty || selectedDifficulty) + '</span>';
    summaryHtml += '<span><strong>Alpha-Beta:</strong> ' + (summary.alphaBeta ? "ON" : "OFF") + '</span>';
    summaryHtml += '<span><strong>Moves:</strong> ' + (summary.totalMoves !== undefined ? summary.totalMoves : moveHistory.length) + '</span>';
    summaryHtml += '</div>';
    document.getElementById("summaryArea").innerHTML = summaryHtml;

    // Metrics
    const metrics = analysis.metrics || {};
    if (metrics.nodesExplored !== undefined) {
        document.getElementById("metricsArea").innerHTML = `
            <div class="metric">
                <span>Nodes Explored</span>
                <span class="metric-value">${metrics.nodesExplored || 0}</span>
            </div>
            <div class="metric">
                <span>Nodes Pruned</span>
                <span class="metric-value">${metrics.nodesPruned || 0}</span>
            </div>
            <div class="metric">
                <span>Time (ms)</span>
                <span class="metric-value">${metrics.timeMs || 0}</span>
            </div>
            <div class="metric">
                <span>Depth Limit</span>
                <span class="metric-value">${metrics.depthLimit || 0}</span>
            </div>
        `;
    } else {
        document.getElementById("metricsArea").innerHTML = '<div style="color: #999; text-align: center; grid-column: span 2;">No data yet</div>';
    }

    // Move breakdown
    const moves = analysis.moveBreakdown || [];
    if (moves.length === 0) {
        document.getElementById("moveBreakdownArea").innerHTML = '<div style="color: #999; text-align: center; padding: 12px;">—</div>';
    } else {
        let movesHtml = "";
        moves.slice(0, 6).forEach(m => {
            const moveStr = m.move ? "(" + m.move[0] + ", " + m.move[1] + ")" : "—";
            const scoreStr = m.score !== undefined ? m.score.toFixed(2) : m.score;
            movesHtml += `
                <div class="move-item">
                    <span><strong>${moveStr}</strong>  score: ${scoreStr}</span>
                    ${m.isBest ? '<span class="best-badge">BEST</span>' : '<span style="font-size: 11px;">rank #' + m.rank + '</span>'}
                </div>
            `;
        });
        document.getElementById("moveBreakdownArea").innerHTML = movesHtml;
    }

    // Explanation
    const explanation = analysis.explanation || "AI decision explanation not available";
    document.getElementById("explanationArea").innerHTML = explanation;

    // Pruning insight
    const pruning = analysis.pruningInsight || "Pruning insight will appear here.";
    document.getElementById("pruningArea").innerHTML = pruning;
}

// Check backend health
async function checkBackendHealth() {
    try {
        const response = await fetch("http://127.0.0.1:5000/health", {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });
        if (response.ok) {
            document.getElementById("apiHint").innerHTML = "Backend connected on port 5000";
            document.getElementById("apiHint").style.color = "#2e7d32";
            return true;
        } else {
            document.getElementById("apiHint").innerHTML = "Backend error - check server";
            document.getElementById("apiHint").style.color = "#d32f2f";
            return false;
        }
    } catch (err) {
        document.getElementById("apiHint").innerHTML = "Backend not running on port 5000";
        document.getElementById("apiHint").style.color = "#d32f2f";
        return false;
    }
}

// Call AI backend
async function requestAIMove() {
    if (gameMode !== "ai") return;
    if (!gameActive) return;
    if (currentPlayer !== "O") return;

    updateClickability();
    
    const boardPayload = board.map(row => [...row]);
    const moveHistoryPayload = moveHistory.map(m => [m[0], m[1]]);

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                board: boardPayload,
                difficulty: selectedDifficulty,
                alphaBeta: useAlphaBeta,
                moveHistory: moveHistoryPayload
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            const aiData = result.data;
            const analysis = result.analysis;
            const move = aiData.move;
            
            if (move && move.length === 2 && board[move[0]][move[1]] === "") {
                applyMove(move[0], move[1], "O");
                updateClickability();
            }
            
            if (analysis) {
                renderAnalytics(analysis);
            }
            
            document.getElementById("apiHint").innerHTML = "Backend connected";
            document.getElementById("apiHint").style.color = "#2e7d32";
        } else {
            console.error("AI error:", result.error);
            document.getElementById("apiHint").innerHTML = "Backend error: " + (result.error || "unknown");
            document.getElementById("apiHint").style.color = "#d32f2f";
        }
    } catch (err) {
        console.error("Fetch failed:", err);
        document.getElementById("apiHint").innerHTML = "Cannot reach backend on port 5000";
        document.getElementById("apiHint").style.color = "#d32f2f";
    }
}

// Handle cell click
function handleCellClick(row, col) {
    if (!gameActive) return;
    if (winnerInfo) return;
    if (board[row][col] !== "") return;

    if (gameMode === "2player") {
        applyMove(row, col, currentPlayer);
    } else if (gameMode === "ai") {
        if (currentPlayer === "X") {
            const success = applyMove(row, col, "X");
            if (success && gameActive && currentPlayer === "O") {
                setTimeout(function() { requestAIMove(); }, 80);
            }
            updateClickability();
        }
    }
}

// Build board DOM
function buildBoard() {
    const boardContainer = document.getElementById("board");
    boardContainer.innerHTML = "";
    for (let i = 0; i < 9; i++) {
        const row = Math.floor(i / 3);
        const col = i % 3;
        const cell = document.createElement("div");
        cell.classList.add("cell");
        cell.addEventListener("click", (function(r, c) {
            return function() { handleCellClick(r, c); };
        })(row, col));
        boardContainer.appendChild(cell);
    }
    renderBoard();
}

// Event listeners for UI controls
function setupEventListeners() {
    // Mode buttons
    const modeBtns = document.querySelectorAll(".mode-btn");
    modeBtns.forEach(function(btn) {
        btn.addEventListener("click", function() {
            modeBtns.forEach(function(b) { b.classList.remove("active"); });
            btn.classList.add("active");
            gameMode = btn.getAttribute("data-mode");
            fullReset();
        });
    });

    // Difficulty select
    const diffSelect = document.getElementById("difficultySelect");
    diffSelect.addEventListener("change", function(e) {
        selectedDifficulty = e.target.value;
    });

    // Alpha-beta toggle
    const abToggle = document.getElementById("alphaBetaToggle");
    abToggle.addEventListener("change", function(e) {
        useAlphaBeta = e.target.checked;
    });

    // Reset button
    const resetBtn = document.getElementById("resetBtn");
    resetBtn.addEventListener("click", function() {
        fullReset();
    });

    // New game button
    const newGameBtn = document.getElementById("newGameBtn");
    newGameBtn.addEventListener("click", function() {
        fullReset();
    });
}

// Initialize
function init() {
    buildBoard();
    setupEventListeners();
    fullReset();
    checkBackendHealth();
}

// Start the app when DOM is ready
document.addEventListener("DOMContentLoaded", init);
