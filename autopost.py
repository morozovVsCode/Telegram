import json
import os
import sys
import time
import urllib.error
import urllib.request

POSTS_FILE = "posts.json"
STATE_FILE = "state.json"
CAPTION_LIMIT = 1024


def api(token, method, payload):
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = json.dumps(payload).encode("utf-8")
    for attempt in range(5):
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            try:
                body = json.load(e)
            except Exception:
                body = {}
            if e.code == 429:
                wait = body.get("parameters", {}).get("retry_after", 10) + 1
                print(f"Лимит запросов, жду {wait} сек")
                time.sleep(wait)
                continue
            raise RuntimeError(f"{method}: HTTP {e.code} {body.get('description', '')}")
        except urllib.error.URLError as e:
            print(f"Сетевая ошибка ({e.reason}), попытка {attempt + 1}/5")
            time.sleep(5)
    raise RuntimeError(f"{method}: не удалось отправить после 5 попыток")


def send_post(token, chat_id, post):
    text, image = post["text"], post.get("image")
    if image and len(text) <= CAPTION_LIMIT:
        api(token, "sendPhoto", {"chat_id": chat_id, "photo": image,
                                 "caption": text, "parse_mode": "HTML"})
        return
    if image:
        api(token, "sendPhoto", {"chat_id": chat_id, "photo": image})
    api(token, "sendMessage", {"chat_id": chat_id, "text": text, "parse_mode": "HTML",
                               "link_preview_options": {"is_disabled": True}})


def load_state():
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            data = json.load(f)
            return int(data.get("next_index", data.get("next", 0)))
    except (FileNotFoundError, ValueError, AttributeError):
        return 0


def save_state(n):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"next_index": n}, f)


def check_images(posts):
    bad = []
    for i, p in enumerate(posts, 1):
        url = p.get("image")
        if not url:
            bad.append((i, "нет ссылки"))
            continue
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status != 200:
                    bad.append((i, f"HTTP {r.status}"))
        except urllib.error.HTTPError as e:
            bad.append((i, f"HTTP {e.code}"))
        except Exception as e:
            bad.append((i, str(e)))
    if bad:
        print(f"Не открываются картинки: {len(bad)} из {len(posts)}")
        for i, why in bad[:20]:
            print(f"  пост №{i}: {why} -> {posts[i - 1].get('image')}")
        sys.exit(1)
    print(f"Все {len(posts)} картинок доступны.")


def main():
    with open(POSTS_FILE, encoding="utf-8") as f:
        posts = json.load(f)

    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_images(posts)
        return

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID") or os.environ.get("TELEGRAM_CHANNEL")
    missing = [name for name, val in (("TELEGRAM_BOT_TOKEN", token),
                                      ("TELEGRAM_CHAT_ID", chat_id)) if not val]
    if missing:
        sys.exit("ПУСТЫЕ переменные: " + ", ".join(missing) +
                 ". Секрет не найден: проверьте имя и что он в Repository secrets.")

    per_run = int(os.environ.get("POSTS_PER_RUN", "1"))
    idx = load_state()
    if idx >= len(posts):
        print("Все посты уже опубликованы.")
        return

    for _ in range(per_run):
        if idx >= len(posts):
            break
        title = posts[idx]["text"].split("\n", 1)[0][:70]
        print(f"Публикую пост {idx + 1}/{len(posts)}: {title}")
        send_post(token, chat_id, posts[idx])
        idx += 1
        save_state(idx)
        time.sleep(2)
    print(f"Готово. Осталось постов: {len(posts) - idx}")


if __name__ == "__main__":
    main()
