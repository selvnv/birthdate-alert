### Утилита для создания уведомлений о днях рождениях в Telegram

#### Установка и настройка

> Конфиги и файл базы данных по умолчанию хранятся в каталоге проекта

```bash
# Клонировать репозиторий
git clone https://github.com/selvnv/birthdate-alert.git

# Перейти в каталог проекта
cd birthdate-alert/

# Создать конфигурационный файл приложения
vim conf/app.yaml
```

Содержимое конфигурационного файла заполнить по следующему шаблону
```yaml
sqlite:
  schema_path: "schema/01-initdb.sql"
  db_path: "db/birthday_info"

telegram:
  token: <INSERT_YOUR_TOKEN>
  chat_id: <INSERT_YOUR_CHAT_ID>

app:
  notification_template: "templates/alert_template.html"
```
- `sqlite.schema_path` файл с запросами, инициализирующими базу данных (создание таблицы, с которой умеет работать программа)
- `sqlite.db_path` путь по которому будет располагаться файл базы данных `sqlite`
- `telegram.token` токен телеграм бота, от имени которого будут отправляться уведомления
- `telegram.chat_id` идентификатор чата, в который будут отправляться уведомления
- `app.notification_template` путь к шаблону уведомления `jinja2`

Настройки можно менять под себя. Для работы достаточно указать `telegram.token` и `telegram.chat_id`

> Этап со сборкой пакета из исходников можно пропустить, используя уже собранный пакет из релиза

```bash
curl -L -O https://github.com/selvnv/birthdate-alert/releases/download/v0.1.0/birthday_alert-0.1.0-py3-none-any.whl
```

Приложение работает как CLI-утилита. Необходимо собрать из исходников и установить пакет
```bash
# Для сборки пакета я использую утилиту uv
# Настройки сборщика находятся в файле pyproject.toml
# Сейчас в проекте используется стандартный setuptools
uv build
# ...
# Successfully built dist/birthday_alert-0.1.0.tar.gz
# Successfully built dist/birthday_alert-0.1.0-py3-none-any.whl

# Создание и активация виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка пакета в виртуальное окружение
pip install dist/birthday_alert-0.1.0-py3-none-any.whl

# Удаление артефактов сборки
rm -r birthday_alert.egg-info/ dist/

# Инициализация базы данных приложения
birth init
```

Настройка уведомлений

```bash
# Создать скрипт для запуска уведомлений
cat > run_birth_alert.sh << 'EOF'
#!/bin/bash
cd /home/<YOUR_USERNAME>/birthdate-alert
source venv/bin/activate
birth alert
EOF

# Сделать файл скрипта исполняемым
chmod u+x run_birth_alert.sh

# Настроить запуск скрипта по кроне
crontab -e
```

Формат кроны
```text
┌───────────────────── минуты (0 - 59)
│ ┌─────────────────── часы (0 - 23)
│ │ ┌───────────────── дни месяца (1 - 31)
│ │ │ ┌─────────────── месяцы (1 - 12)
│ │ │ │ ┌───────────── дни недели (0 - 6, 0 = воскресенье)
│ │ │ │ │
* * * * * команда
```

Пример кроны
```bash
# Каждый день в 9 утра выполняется скрипт /home/osboxes/birthdate-alert/run_birth_alert.sh
# Вывод команды и ошибки перенаправляются в /home/osboxes/birthdate-alert/logs/cron.log
0 9 * * * /home/osboxes/birthdate-alert/run_birth_alert.sh >> /home/osboxes/birthdate-alert/logs/cron.log 2>&1
```

