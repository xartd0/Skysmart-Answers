# Ответы на тесты от платформы edu.skysmart.ru

### Работа web версии

<div align="center"> 
  <img src="https://github.com/xartd0/Skysmart-Answers-API/assets/43171120/921c5de9-d9cf-4924-8e08-3e60a6159568" alt="screenshot" />
</div>

### Нужно указывать именно название комнаты, а не ссылку

Примеры:
| Ссылка | Название комнаты |
| ------------- | ------------- |
| https://edu.skysmart.ru/student/maxevepuma | maxevepuma |
| https://edu.skysmart.ru/student/nexemiduke | nexemiduke |
| https://edu.skysmart.ru/student/luzimosoxa | luzimosoxa |
| https://edu.skysmart.ru/student/kuxikifizi | kuxikifizi |



<!-- Run Locally -->
### :running: Запуск локально

Клонируем репозиторий

```bash
  git clone https://github.com/xartd0/Skysmart-Answers
```

Заходим в его папку

```bash
  cd Skysmart-Answers
```

Ставим зависимости или запускаем install.bat

```bash
  pip3 install -r requirements.txt
```

Запуск web версии

```bash
  start.bat
```

Запуск через cmd

```bash
  python3 template.py
```



### Аккаунт
В конфиге уже есть аккаунт, но вы можете использовать свой (необязательно).

```
~> nano utils/config.py
# Данные от аккаунта
auth_creds = {
    'password': '',
    'phoneOrEmail': '' пишите почту
}
```

## Вопросы
Если у вас остались вопросы, то пишите в тг - https://t.me/xartd0
