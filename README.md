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

## Использование

1. `git clone https://github.com/xartd0/Skysmart-Answers`
2. `cd Skysmart-Answers`
3. `pip install -r requirements.txt`
4. `python3 template.py` (или `python3 live_stream_template.py`)
5. Нужно указать именно название комнаты

## Аккаунт

В конфиге уже есть аккаунт, но он может быть заблокирован, поэтому лучше впишите свой.

```
~> nano utils/config.py
auth_creds = {
    'email': 'почта',
    'password': 'пароль'
}
```


