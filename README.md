# 📊 Food (Calories, Proteins, Fats, Carbs) Tracking Bot

## 🤖 О боте
Телеграм-бот для анализа пищевой ценности продуктов по:
- Текстовому описанию
- Голосовому сообщению
- Фотографии
  
Результаты можно сохранить в дневник питания с возможностью просмотра статистики.

## ⚙️ Технологии
- **Aiogram** - Разработка бота
- **AI**: Mistral AI (API) для анализа текста
- **ASR**: Vosk для распознавания речи
- **DB**: Sqlalchemy(SQLite) + Alembic для миграций
- **Media**: FFmpeg для обработки аудио

## 🚀 Установка

### Windows
```powershell
# 1. Установите Chocolatey (если нет)
Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 2. Установите FFmpeg
choco install ffmpeg -y

# 3. Создайте виртуальное окружение
python -m venv venv
.\venv\Scripts\activate

# 4. Установите зависимости
pip install -r requirements.txt
```

### Linux/macOS
```bash
# 1. Установите FFmpeg
# Ubuntu/Debian
sudo apt install ffmpeg
# macOS
brew install ffmpeg

# 2. Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 3. Установите зависимости
pip install -r requirements.txt
```

## ⚙️ Конфигурация (.env)
```ini
BOT_TOKEN=your_telegram_bot_token
DB_PATH=sqlite+aiosqlite:///database/users.db
MISTRAL_API_KEY=your_mistral_api_key
ADMIN_ID=your_telegram_id
```

## 🏃‍♂️ Запуск
```bash
# Применение миграций
alembic upgrade head

# Запуск бота
python main.py
```
