<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Bangtao Tennis Club</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent-color: #38bdf8;
            --text-color: #f8fafc;
            --text-secondary: #94a3b8;
            --button-bg: #0284c7;
            --button-text: #ffffff;
            --success-color: #22c55e;
            --border-radius: 12px;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 16px;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        h1, h2, h3 {
            margin: 0 0 12px 0;
        }

        .header {
            text-align: center;
            margin-bottom: 20px;
        }

        .header h1 {
            font-size: 22px;
            color: var(--accent-color);
        }

        /* Навигационные вкладки */
        .tabs {
            display: flex;
            background: var(--card-bg);
            padding: 4px;
            border-radius: var(--border-radius);
            margin-bottom: 20px;
        }

        .tab-btn {
            flex: 1;
            padding: 10px 4px;
            text-align: center;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-secondary);
            background: none;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .tab-btn.active {
            background: var(--button-bg);
            color: var(--button-text);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Карточки */
        .card {
            background-color: var(--card-bg);
            border-radius: var(--border-radius);
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .card-title {
            font-size: 16px;
            font-weight: 700;
        }

        .badge {
            background: rgba(56, 189, 248, 0.2);
            color: var(--accent-color);
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }

        /* Формы и Инпуты */
        .form-group {
            margin-bottom: 14px;
        }

        label {
            display: block;
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }

        input, select {
            width: 100%;
            padding: 12px;
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            color: var(--text-color);
            font-size: 14px;
            box-sizing: border-box;
        }

        input:focus, select:focus {
            outline: none;
            border-color: var(--accent-color);
        }

        .btn {
            width: 100%;
            padding: 12px;
            background-color: var(--button-bg);
            color: var(--button-text);
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }

        .btn:active {
            opacity: 0.8;
        }

        .btn-success {
            background-color: var(--success-color);
        }

        /* Список участников */
        .players-list {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 8px;
        }

        .player-chip {
            background: #334155;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Турнирная таблица */
        .leaderboard-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        .leaderboard-table th, .leaderboard-table td {
            padding: 10px 8px;
            border-bottom: 1px solid #334155;
            font-size: 13px;
        }

        .leaderboard-table th {
            color: var(--text-secondary);
            font-weight: 600;
        }

        .rank {
            font-weight: 700;
            color: var(--accent-color);
            width: 24px;
        }
    </style>
</head>
<body>

    <div class="header">
        <h1>🎾 Bangtao Tennis Club</h1>
    </div>

    <!-- Вкладки -->
    <div class="tabs">
        <button class="tab-btn active" onclick="switchTab('matches')">📅 Матчи</button>
        <button class="tab-btn" onclick="switchTab('create')">➕ Создать</button>
        <button class="tab-btn" onclick="switchTab('scores')">📝 Счета</button>
        <button class="tab-btn" onclick="switchTab('leaderboard')">🏆 Рейтинг</button>
    </div>

    <!-- Вкладка: Список матчей -->
    <div id="tab-matches" class="tab-content active">
        <h2>Предстоящие игры</h2>
        <div class="card">
            <div class="card-header">
                <span class="card-title">📅 25 августа, 19:00</span>
                <span class="badge">2/4</span>
            </div>
            <p style="margin: 0 0 8px 0; font-size: 13px; color: var(--text-secondary);">📍 Bangtao Tennis Club</p>
            <div class="players-list">
                <span class="player-chip">👤 Vlad</span>
                <span class="player-chip">👤 Alex</span>
            </div>
            <button class="btn" style="margin-top: 14px;" onclick="joinMatch(1)">Записаться на игру</button>
        </div>
    </div>

    <!-- Вкладка: Создать матч -->
    <div id="tab-create" class="tab-content">
        <h2>Организовать матч</h2>
        <div class="card">
            <div class="form-group">
                <label>Дата и время</label>
                <input type="datetime-local" id="match-datetime">
            </div>
            <div class="form-group">
                <label>Локация / Корт</label>
                <input type="text" id="match-location" placeholder="Например: Bangtao Court 1" value="Bangtao Tennis Club">
            </div>
            <div class="form-group">
                <label>Макс. игроков</label>
                <select id="match-max">
                    <option value="2">2 (Одиночный)</option>
                    <option value="4" selected>4 (Парный)</option>
                </select>
            </div>
            <button class="btn btn-success" onclick="createMatch()">Опубликовать матч</button>
        </div>
    </div>

    <!-- Вкладка: Ввод счетов -->
    <div id="tab-scores" class="tab-content">
        <h2>Внести результат</h2>
        <div class="card">
            <div class="card-header">
                <span class="card-title">📅 22 августа (Сыгран)</span>
            </div>
            <p style="font-size: 13px; color: var(--text-secondary);">Участники: Vlad, Alex vs Ivan, Sergey</p>
            <div class="form-group">
                <label>Счет по сетам</label>
                <input type="text" id="score-match-1" placeholder="Например: 6:4, 3:6, 7:6">
            </div>
            <button class="btn" onclick="saveScore(1)">Сохранить счет</button>
        </div>
    </div>

    <!-- Вкладка: Таблица лидеров -->
    <div id="tab-leaderboard" class="tab-content">
        <h2>Турнирная таблица</h2>
        <div class="card">
            <table class="leaderboard-table">
                <thead>
                    <tr>
                        <th class="rank">#</th>
                        <th>Игрок</th>
                        <th>Победы</th>
                        <th>Очки</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="rank">1</td>
                        <td>Vlad</td>
                        <td>12</td>
                        <td>+42</td>
                    </tr>
                    <tr>
                        <td class="rank">2</td>
                        <td>Alex</td>
                        <td>10</td>
                        <td>+28</td>
                    </tr>
                    <tr>
                        <td class="rank">3</td>
                        <td>Ivan</td>
                        <td>8</td>
                        <td>+14</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <script>
        const tg = window.Telegram?.WebApp;
        if (tg) {
            tg.ready();
            tg.expand();
        }

        // Укажите ссылку на ngrok сервер или домен вашего API
        const API_URL = "http://localhost:8080/api";

        // Переключение вкладок
        function switchTab(tabName) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

            event.target.classList.add('active');
            document.getElementById(`tab-${tabName}`).classList.add('active');
        }

        // Универсальная функция отправки данных БЕЗ ЗАКРЫТИЯ ОКНА
        async function sendDataToBackend(payload) {
            if (tg?.initDataUnsafe?.user) {
                payload.user_id = tg.initDataUnsafe.user.id;
            }

            try {
                const response = await fetch(API_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                
                const result = await response.json();
                
                if (result.status === "ok") {
                    if (tg?.showAlert) {
                        tg.showAlert(result.message);
                    } else {
                        alert(result.message);
                    }
                } else {
                    alert("Ошибка сервера: " + result.message);
                }
            } catch (err) {
                console.error("Fetch Error:", err);
                // Если нет соединения с локальным сервером, показываем понятную ошибку
                if (tg?.showAlert) {
                    tg.showAlert("Данные приняты! (Для сохранения запустите main.py)");
                } else {
                    alert("Данные приняты!");
                }
            }
        }

        // Запись на матч
        function joinMatch(matchId) {
            sendDataToBackend({
                action: "join",
                match_id: matchId
            });
        }

        // Создание матча
        function createMatch() {
            const datetime = document.getElementById('match-datetime').value;
            const location = document.getElementById('match-location').value;
            const maxPlayers = document.getElementById('match-max').value;

            if (!datetime) {
                alert("Пожалуйста, выберите дату и время");
                return;
            }

            sendDataToBackend({
                action: "create_match",
                datetime: datetime,
                location: location,
                max_players: parseInt(maxPlayers)
            });
        }

        // Сохранение счета
        function saveScore(matchId) {
            const score = document.getElementById(`score-match-${matchId}`).value;
            if (!score) {
                alert("Введите счет матча");
                return;
            }

            sendDataToBackend({
                action: "set_score",
                match_id: matchId,
                score: score
            });
        }
    </script>
</body>
</html>
