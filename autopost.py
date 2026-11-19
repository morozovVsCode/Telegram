import json
import os
import sys
from pathlib import Path

import requests

BASE = Path(__file__).parent
posts = json.loads((BASE / "posts.json").read_text(encoding="utf-8"))
state_file = BASE / "state.json"
idx = json.loads(state_file.read_text())["next"] if state_file.exists() else 0

if idx >= len(posts):
    print("Посты закончились - добавьте новые в posts.json")
    sys.exit(1)

r = requests.post(
    f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage",
    json={
        "chat_id": os.environ["TELEGRAM_CHANNEL"],
        "text": posts[idx],
        "parse_mode": "HTML",
    },
    timeout=30,
)
r.raise_for_status()
state_file.write_text(json.dumps({"next": idx + 1}))
print(f"Опубликован пост {idx + 1} из {len(posts)}")
