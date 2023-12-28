# Ответы на SkySmart

### Нужно указывать именно название комнаты, а не ссылку

Примеры:
| Ссылка | Название комнаты |
| ------------- | ------------- |
| https://edu.skysmart.ru/student/maxevepuma | maxevepuma |
| https://edu.skysmart.ru/student/nexemiduke | nexemiduke |
| https://edu.skysmart.ru/student/luzimosoxa | luzimosoxa |
| https://edu.skysmart.ru/student/kuxikifizi | kuxikifizi |

## Зависимости

1. `python3`
2. `python-pip`
3. `aiohttp`
4. `beautifulsoup4`
5. `user_agent`
5. `base64`

## Использование через cmd

1. `git clone https://github.com/xartd0/Skysmart-Answers`
2. `cd Skysmart-Answers`
3. `pip install -r requirements.txt`
4. `python3 template.py`
5. Нужно указать именно название комнаты

## Использование через web (кто особо не шарит, а хочет сразу ответы, в нем есть поддержка математических символов)

1. `git clone https://github.com/xartd0/Skysmart-Answers)` или качаете через сайт
2. `cd Skysmart-Answers` или заходите через проводник
3. `install.bat` просто нажимаем (установка всех библиотек)
4. `start.bat` тут тоже (запуск сайта)

## Работа web версии
https://github.com/xartd0/Skysmart-Answers-API/assets/43171120/69cdc6e5-b05f-4432-91b9-2fc6b6c9ee67
https://github.com/xartd0/Skysmart-Answers-API/assets/43171120/eaeee4fb-e0c0-4420-997d-6915dc5967cc

## Вопросы
Если у вас остались вопросы, то пишите в тг - https://t.me/xartd0

## Аккаунт

В конфиге уже есть аккаунт, но он может быть заблокирован, поэтому лучше впишите свой.

```
~> nano utils/config.py
# Данные от аккаунта
auth_creds = {
    'password': '',
    'phoneOrEmail': '' пишите почту
}
```


