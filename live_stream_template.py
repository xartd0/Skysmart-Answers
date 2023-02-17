# Это мы тянем библиотеки
# SkySmart - answers - основная
from answer_module import SkyAnswers
# Это мы будем перезаписывать функцию GET_ANSWERS, поэтому нам надо API
import skysmart_api
# У нас асинхронный код
import asyncio
# Парсер
from bs4 import BeautifulSoup
# Это чтоб сделать оформление
import shutil
# Для нахождения id комнаты
import re

# Функция которая форматирует Input в что-то красивое


# I: generate_one('number','title','full-text',['answers-1','answers-2'])

# O:
# Задание #number - *title*
# Текст вопроса
# full-text
# 
#     Ответ: answers-1
#     Ответ: answers-2

async def generate_one(questuon_number:int, questuon_title:str, questuon_text:str='', answers: list = None) -> str:
    if answers is None:
        answers = []
    if questuon_text.strip() != '': questuon_text = 'Текст вопроса\n' + questuon_text
    generated = f'Задание #{questuon_number} - *{questuon_title}*\n{questuon_text}\n'
    for i in answers:
        generated += f'\n    Ответ: {i}'
    return generated.strip()

# Новая функция для получения ответов
async def get_answers(self):
    
    # Tasks-uuid
    tasks_uuids = await skysmart_api.get_room(self.task_hash)
    
    # А почему бы и нет
    meta = await skysmart_api.get_meta(self.task_hash)
    print( f'Название теста: {meta[0]}\nТема: {meta[1]}\n\n')
    
    # Цикл по задачам
    for tasks_count,uuid in enumerate(tasks_uuids): 
        
        # Получаем код задачи
        soup = await skysmart_api.get_task_html(uuid)

        # Получаем ответ
        answers = self.get_task_answer(BeautifulSoup(soup, 'html.parser'), tasks_count+1)

        # Выводим
        print(await generate_one(answers['task_number'],answers['question'],answers['full_q'],answers['answer']))
        print(f'\n{"-"*shutil.get_terminal_size((80, 20)).columns}\n')

    # Возвращаем ничего. Нам не нужно их возвращать, потому что мы их сразу же выводим
    return []


async def main():
    
    # Получаем ID комнаты
    task_hash = input('Укажите название комнаты: ')
    
    # А почему бы и нет?
    task_hash = re.findall(r'student/(.*)', task_hash)[0]
    
    # Создаём SkyAnswers
    answers_module = SkyAnswers(task_hash)
    
    # Перезацисываем get_answers
    answers_module.get_answers = get_answers
    
    # Выводим линию
    print(f'\n{"-"*shutil.get_terminal_size((80, 20)).columns}\n')
    
    # Вызываем новую функцию
    await answers_module.get_answers(answers_module)

# Запускаем
asyncio.run(main())
