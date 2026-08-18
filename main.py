<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Теннисный Клуб</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--tg-theme-bg-color, #f4f4f5);
            color: var(--tg-theme-text-color, #18181b);
            margin: 0;
            padding: 16px;
            box-sizing: border-box;
        }
        .card {
            background: var(--tg-theme-secondary-bg-color, #ffffff);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        h2 {
            margin-top: 0;
            font-size: 18px;
            color: var(--tg-theme-text-color, #18181b);
        }
        .form-group {
            margin-bottom: 12px;
        }
        label {
            display: block;
            font-size: 12px;
            color: var(--tg-theme-hint-color, #71717a);
            margin-bottom: 4px;
        }
        input, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #e4e4e7;
            border-radius: 8px;
            box-sizing: border-box;
            background: var(--tg-theme-bg-color, #ffffff);
            color: var(--tg-theme-text-color, #18181b);
            font-size: 14px;
        }
        button {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            background-color: var(--tg-theme-button-color, #2563eb);
            color: var(--tg-theme-button-text-color, #ffffff);
            font-weight: 600;
            cursor: pointer;
            font-size: 14px;
            transition: opacity 0.2s;
        }
        button:active {
            opacity: 0.8;
        }
        .status-msg {
            margin-top: 10px;
            font-size: 13px;
            text-align: center;
            display: none;
        }
        .success { color: #16a34a; }
        .error { color: #dc2626; }
    </style>
</head>
<body>

    <div class="card">
        <h2>🎾 Создать матч</h2>
        <div class="form-group">
            <label>Дата и время</label>
            <input type="datetime-local" id="matchDate">
        </div>
        <div class="form-group">
            <label>Локация / Корт</label>
            <input type="text" id="matchLocation" placeholder="например, Корт №1">
        </div>
        <div class="form-group">
            <label>Макс. участников</label>
            <input type="number" id="maxPlayers" value="4" min="2" max="10">
        </div>
        <button onclick="createMatch()">Опубликовать матч</button>
        <div id="createStatus" class="status-msg"></div>
    </div>

    <div class="card">
        <h2>📝 Внести счет</h2>
        <div class="form-group">
            <label>ID матча</label>
            <input type="number" id="scoreMatchId" placeholder="ID матча">
        </div>
        <div class="form-group">
            <label>Итоговый счет</label>
            <input type="text" id="scoreValue" placeholder="6:4, 3:6, 10:8">
        </div>
        <button onclick="submitScore()">Сохранить результат</button>
        <div id="scoreStatus" class="status-msg"></div>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();

        // Публичный URL туннеля ngrok
        const API_URL = "https://pastel-founding-sly.ngrok-free.dev/api";

        async function sendRequest(endpoint, data, statusElId) {
            const statusEl = document.getElementById(statusElId);
            statusEl.style.display = 'block';
            statusEl.className = 'status-msg';
            statusEl.innerText = 'Отправка...';

            const payload = {
                ...data,
                initData: tg.initData,
                user: tg.initDataUnsafe?.user || {}
            };

            try {
                const response = await fetch(`${API_URL}/${endpoint}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();

                if (response.ok && result.status === 'ok') {
                    statusEl.innerText = 'Успешно сохранено!';
                    statusEl.classList.add('success');
                    if (tg.HapticFeedback) {
                        tg.HapticFeedback.notificationOccurred('success');
                    }
                } else {
                    throw new Error(result.message || 'Ошибка сервера');
                }
            } catch (err) {
                statusEl.innerText = `Ошибка: ${err.message}`;
                statusEl.classList.add('error');
                if (tg.HapticFeedback) {
                    tg.HapticFeedback.notificationOccurred('error');
                }
            }
        }

        function createMatch() {
            const date = document.getElementById('matchDate').value;
            const location = document.getElementById('matchLocation').value;
            const maxPlayers = document.getElementById('maxPlayers').value;

            if (!date || !location) {
                alert('Пожалуйста, заполните дату и локацию');
                return;
            }

            sendRequest('create-match', { date, location, maxPlayers }, 'createStatus');
        }

        function submitScore() {
            const matchId = document.getElementById('scoreMatchId').value;
            const score = document.getElementById('scoreValue').value;

            if (!matchId || !score) {
                alert('Заполните ID матча и счет');
                return;
            }

            sendRequest('submit-score', { matchId, score }, 'scoreStatus');
        }
    </script>
</body>
</html>
