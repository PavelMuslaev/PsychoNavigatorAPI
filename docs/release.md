# Запуск API и Telegram-бота

Команды ниже рассчитаны на Linux/macOS, Git и uv. Для Telegram потребуется токен своего бота от BotFather. В двух терминалах используйте соответствующие корни репозиториев как рабочие каталоги.

```sh
git clone https://github.com/PavelMuslaev/PsychoNavigatorAPI.git
git clone https://github.com/PavelMuslaev/Psycho_navigatorbot.git
uv python install 3.14
(cd PsychoNavigatorAPI && uv sync --locked --python 3.14)
(cd Psycho_navigatorbot && uv sync --locked --python 3.14)
umask 077
mkdir -p "$HOME/psychonav-data"
touch PsychoNavigatorAPI/.env Psycho_navigatorbot/.env
chmod 600 PsychoNavigatorAPI/.env Psycho_navigatorbot/.env
```

Создайте случайный сервисный секрет в менеджере паролей. В локальном файле API `.env` задайте абсолютный путь к файлу в созданном каталоге и подставьте секрет:

```dotenv
DATABASE_PATH=/absolute/path/to/psychonav-data/history.sqlite3
HISTORY_TOKEN=<общий сервисный секрет>
```

В файле бота `.env`:

```dotenv
API_BASE_URL=http://127.0.0.1:8000
BOT_TOKEN=<токен от BotFather>
HISTORY_TOKEN=<тот же сервисный секрет>
```

Путь и ключи подставляются буквально. Храните оба файла вне Git, базу и резервные копии — на постоянном диске с доступом только для обслуживающей учётной записи. На разных хостах задайте боту защищённый адрес API.

## Первый запуск

В корне API:

```sh
uv run alembic upgrade head
uv run uvicorn --app-dir src psycho_navigator.main:app --host 127.0.0.1 --port 8000
```

В корне бота:

```sh
curl --fail http://127.0.0.1:8000/health
PYTHONPATH=src uv run python -m psychonavigatorbot.main
```

В личном чате отправьте /start, пройдите BFI-2 и EPI. Откройте оба результата из «Моя история». Перезапустите оба процесса из тех же каталогов и снова откройте записи. Сверьте даты и значения шкал.

## Резервная копия и восстановление

Из корня API узнайте эффективный путь:

```sh
PYTHONPATH=src uv run python -c 'from psycho_navigator.config import Settings; print(Settings().database_path.resolve())'
```

Для копирования используйте SQLite backup API. Сохраните следующий фрагмент как локальный скрипт copy-history.py и передайте два абсолютных пути. Источник открывается только для чтения, целевой файл должен быть новым.

```python
from contextlib import closing
from pathlib import Path
import sqlite3
import sys

source, target = map(Path, sys.argv[1:])
target.touch(mode=0o600, exist_ok=False)
with closing(sqlite3.connect(source.resolve().as_uri() + "?mode=ro", uri=True)) as src:
    with closing(sqlite3.connect(target)) as dst:
        src.backup(dst)
        if dst.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
            raise RuntimeError("Повреждённая копия")
```

```sh
uv run python copy-history.py /path/history.sqlite3 /backups/history-2026-11-27.sqlite3
uv run python copy-history.py /backups/history-2026-11-27.sqlite3 /path/restored.sqlite3
```

При ошибке используйте новое имя назначения и повторите копирование после устранения причины. Проверьте восстановленную базу отдельным экземпляром API на порту 8001 с DATABASE_PATH=/path/restored.sqlite3. Для переключения остановите бот и API, укажите проверенный файл в .env API, примените миграции и запустите оба сервиса. Сохраните предыдущий файл до проверки результатов.

## Обновление

1. Остановите бот и API, сделайте резервную копию. Запишите текущие версии обоих репозиториев командой `git rev-parse HEAD`.
2. Переключите репозитории на выбранные релизные коммиты и в каждом выполните `uv sync --locked`.
3. Из корня API выполните `uv run alembic upgrade head`. Запустите API, проверьте /health, затем запустите бот и повторите проверку истории.
4. Для отката остановите процессы, верните прежние коммиты и зависимости, подключите восстановленную предрелизную базу. Изменения после момента копирования в неё не попадут.

## Если каталог работает, а история недоступна

В access log Uvicorn найдите метод, путь и статус запроса истории. В /docs можно проверить GET /users/{telegram_id}/attempts, указав HISTORY_TOKEN в Authorize и ID собственного тестового пользователя.

- **401** — проверьте наличие и совпадение HISTORY_TOKEN у процессов, затем перезапустите их.
- **500 / no such table** — сравните эффективный путь API с путём миграций. Из того же окружения выполните `uv run alembic current` и `uv run alembic heads`. Для отстающей базы примените upgrade head.
- **200 и пустой список** — проверьте Telegram ID и файл базы. При относительном пути смена рабочего каталога может подключить другую SQLite.
- **Ошибка подключения или записи** — проверьте API_BASE_URL, журнал API, существование каталога, права на файл и каталог, свободное место.
