# Ответы на тесты от платформы edu.skysmart.ru

### Работа web версии

<img src="https://github.com/xartd0/Skysmart-Answers-API/assets/43171120/921c5de9-d9cf-4924-8e08-3e60a6159568" alt="screenshot" width="600" height="400"/>

### Нужно указывать именно название комнаты, а не ссылку

Примеры:
| Ссылка | Название комнаты |
| ------------- | ------------- |
| https://edu.skysmart.ru/student/maxevepuma | maxevepuma |
| https://edu.skysmart.ru/student/nexemiduke | nexemiduke |
| https://edu.skysmart.ru/student/luzimosoxa | luzimosoxa |
| https://edu.skysmart.ru/student/kuxikifizi | kuxikifizi |


### :running: Готовое решение
Данный репозиторий развернут на vercel - https://skysmart-answers.vercel.app/


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

Ставим зависимости

```bash
  pip3 install -r requirements.txt
```

Запуск web версии

```bash
  uvicorn web.main:app --port 8000
```

На фронтенде нужно поменять в запросе url на localhost:8000
В данной строке
```bash
  const response = await fetch('https://skysmart-answers.vercel.app/get_answers/', {
```

Запуск через cmd

```bash
  python template.py
```

## Вопросы
Если у вас остались вопросы, то пишите в тг - https://t.me/xartd0
