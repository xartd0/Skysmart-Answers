# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
import base64
import re 
import asyncio
import aiohttp


async def auth():
    url = "https://api-edu.skysmart.ru/api/v2/auth/auth/student"
    session_data = {"phoneOrEmail":"сюда почту или телефон","password":"пароль"}
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json; charset=UTF-8"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data = json.dumps(session_data)) as resp:
            data = await resp.read()
            hashrate = json.loads(data)
            await session.close()
            return 'Bearer ' + hashrate['jwtToken']

async def get_steps(roomHash):
    url = "https://api-edu.skysmart.ru/api/v1/lesson/join"
    payload = "{\"roomHash\":\"" + roomHash + "\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': await auth()
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as resp:
            steps_raw = await resp.json()
            await session.close()
    
    return steps_raw['taskStudentMeta']['steps'] # все uuid заданий


async def get_room(taskHash):
    url = f"https://api-edu.skysmart.ru/api/v1/task/start"
    payload = "{\"taskHash\":\"" + taskHash + "\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': await auth()

    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as resp:
            roomhashjson = await resp.json() 
            await session.close()
            return roomhashjson['roomHash'] # код рума 
            
async def get_json_html(uuid):
    url = "https://api-edu.skysmart.ru/api/v1/content/step/load?stepUuid=" + uuid['stepUuid']
    headers = {
    'Authorization': await auth()
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            answer_row = await resp.json()
            await session.close()
    return BeautifulSoup(answer_row['content'], 'html.parser')


async def answerparse(taskHash):
    x = 0
    results = []
    # ---- получение uuid заданий в тесте ----#
    roomHash = await get_room(taskHash)
    
    # ---- тут получаем html в json ----#
    allsteps = await get_steps(roomHash)
    random = False # проверка на рандомные задания
    for uuid in allsteps:
        x = x + 1
        soup = await get_json_html(uuid)
        try:
            anstitlerow = f'№{x}📝Вопрос: ' + (soup.find('vim-instruction').text.replace('\n', ' ')).replace('\r',' ')
            results.append(anstitlerow)
        except:
            anstitlerow = f'№{x}📝Вопрос: ' + (soup.find('vim-content-section-title').text.replace('\n', ' ')).replace('\r',' ')
            results.append(anstitlerow)
        # ledotetote
        # а тут много циклов,каждый цикл это разные типы заданий,знаю стремно,но мне лень переделывать
        if uuid['isRandom']:
            random = True
        if random:
            results.append('Это задание рандомное! Ответы могут не совпадать!')
        for i in soup.find_all('vim-test-item', attrs={'correct': 'true'}):
            results.append(i.text)
        for i in soup.find_all('vim-input-answers'):            
            j = i.find('vim-input-item')
            results.append(j.text)
        for i in soup.find_all('vim-select-item', attrs={'correct': 'true'}):
            results.append(i.text.replace('\n', ' '))
        for i in soup.find_all('vim-test-image-item', attrs={'correct': 'true'}):
            results.append(f'{i.text} - Верный')
        for i in soup.find_all('math-input'):
            j = i.find('math-input-answer')
            results.append(j.text)
        for i in soup.find_all('vim-dnd-text-drop'):
            for f in soup.find_all('vim-dnd-text-drag'):
                if i['drag-ids'] == f['answer-id']:
                    results.append(f'{f.text}')
        for i in soup.find_all('vim-dnd-group-drag'):
            for f in soup.find_all('vim-dnd-group-item'):
                if i['answer-id'] in f['drag-ids']:
                    results.append(f'{f.text} - {i.text}')
        for i in soup.find_all('vim-groups-row'):
            for l in i.find_all('vim-groups-item'):
                try:
                    a = base64.b64decode(l['text']) 
                    results.append(f"{a.decode('utf-8')}")   
                except:
                    pass
        for i in soup.find_all('vim-strike-out-item', attrs={'striked': 'true'}):
            results.append(i.text)
        for i in soup.find_all('vim-dnd-image-set-drag'):
            for f in soup.find_all('vim-dnd-image-set-drop'):
                if i['answer-id'] in f['drag-ids']:
                    results.append(f'{f["image"]} - {i.text}')
        for i in soup.find_all('vim-dnd-image-drag'):
            for f in soup.find_all('vim-dnd-image-drop'):
                if i['answer-id'] in f['drag-ids']:
                    results.append(f'{f.text} - {i.text}')
    return results


# Тут будет очистка всех странных знаков и тд
async def ochistka(string):
    string = string.replace('\n', '')
    string = '├ ' + string
    fraction = re.compile("dfrac{(.*?)}{(.*?)}")
    square_root = re.compile("sqrt{(.*?)}")
    power = re.compile("(.*?)\^(.*)")
    bol = re.compile("gt")
    men = re.compile("lt")
    pm = re.compile('pm')
    perp = re.compile('perp')
    drob = re.compile('dfrac')
    for i in fraction.findall(string):
        string = string.replace("\dfrac{" + str(i[0]) + "}{" + str(i[1]) + "}", str(i[0]) + "/" + str(i[1]))
    for i in square_root.findall(string):
        string = string.replace("\sqrt{" + str(i) + "}", "корень из " + str(i))
    for i in power.findall(string):
        string = string.replace(str(i[0]) + "^" + str(i[1]), str(i[0]) + " в степени " + str(i[1]))
    for i in bol.findall(string):
        string = string.replace("\gt", ">")
    for i in men.findall(string):
        string = string.replace("\lt", "<")
    for i in pm.findall(string):
        string = string.replace("\pm", "±")
    for i in perp.findall(string):
        string = string.replace("\perp", "⊥")
    return string

# Самый простой вывод ответов
taskHash = input('Введите комнату: ')
results = asyncio.run(answerparse(taskHash))
for i in results:
    print(i)
#\gt > \lt 
