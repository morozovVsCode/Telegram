import json
import os
import sys
from pathlib import Path

import requests

BASE = Path(__file__).parent
POSTS_FILE = BASE / "posts.json"
STATE_FILE = BASE / "state.json"

posts = json.loads(POSTS_FILE.read_text(encoding="utf-8"))
state = json.loads(STATE_FILE.read_text(encoding="utf-8")) if STATE_FILE.exists() else {"next": 0}
idx = int(state.get("next", 0))

if idx >= len(posts):
    print("Очередь публикаций закончилась.")
    sys.exit(0)

token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ["TELEGRAM_CHANNEL"]
api = f"https://api.telegram.org/bot{token}/"

def telegram(method, payload, timeout=90):
    response = requests.post(api + method, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data}")
    return data

item = posts[idx]
if isinstance(item, str):
    # Совместимость со старым форматом: массив строк.
    telegram("sendMessage", {
        "chat_id": chat_id,
        "text": item,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    })
else:
    text = item.get("text", "")
    image = item.get("image")
    if image:
        # Отправляем изображение отдельным сообщением: Telegram ограничивает
        # подпись к фото 1024 символами, а статьи могут быть длиннее.
        telegram("sendPhoto", {
            "chat_id": chat_id,
            "photo": image,
        })
    if text:
        # Текстовое сообщение Telegram допускает до 4096 символов.
        if len(text) > 4096:
            raise ValueError(f"Пост {idx + 1} длиннее лимита Telegram (4096 символов).")
        telegram("sendMessage", {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        })

# Обновляем указатель только после успешной отправки.
STATE_FILE.write_text(
    json.dumps({"next": idx + 1}, ensure_ascii=False),
    encoding="utf-8",
)
print(f"Успешно опубликована запись {idx + 1} из {len(posts)}")
