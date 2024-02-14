@echo off
echo Установка необходимых библиотек...

pip install aiohttp==3.8.1
pip install beautifulsoup4==4.11.1
pip install user_agent==0.1.10
pip install uvicorn==0.18.2
pip install fastapi==0.45.0
pip install selenium==4.17.2

echo Установка завершена!
