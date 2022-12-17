# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import base64
import re 
import asyncio
import aiohttp
from user_agent import generate_user_agent

url_room = 'https://api-edu.skysmart.ru/api/v1/task/preview'
url_auth = 'https://api-edu.skysmart.ru/api/v1/auth/auth'
url_steps = 'https://api-edu.skysmart.ru/api/v1/content/step/load?stepUuid='

auth_creds = {
    'email': 'asd3fgsdfgs3dfgsdfg@gmail.com',
    'password': 'i6D92r2gUmwvWJu'
}

async def auth():

    async with aiohttp.ClientSession() as session:
        async with session.post(url_auth, headers={'User-Agent': generate_user_agent()}, data=auth_creds) as resp:
            
            json_resp = await resp.json() 

            return {
                'Accept' : 'application/json, text/plain, */*',
                'Authorization': 'Bearer ' + json_resp['jwtToken'],
                'Connection' : 'keep-alive',
                'Content-Type': 'application/json',
                'User-Agent': generate_user_agent(),
            }

async def get_room(taskHash):
    url = url_room
    payload = "{\"taskHash\":\"" + taskHash + "\"}"
    headers = await auth()
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as resp:
            steps_raw = await resp.json() 
            await session.close()
            return steps_raw['meta']['stepUuids'] # все uuid заданий
            
async def get_json_html(uuid):
    url = url_steps + uuid
    headers = await auth()
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            answer_row = await resp.json()
            await session.close()
    return BeautifulSoup(answer_row['content'], 'html.parser')


async def answerparse(taskHash):
    x = 0
    results = []
    # ---- получение uuid заданий в тесте ----#
    
    # ---- тут получаем html в json ----#
    allsteps = await get_room(taskHash)
    random = False # проверка на рандомные задания
    for uuid in allsteps:
        x = x + 1
        soup = await get_json_html(uuid)
        try:
            anstitlerow = f'№{x}📝Вопрос: ' + (soup.find('vim-instruction').text.replace('\n', ' ')).replace('\r',' ')
            results.append(anstitlerow)
        except:
            try:
                anstitlerow = f'№{x}📝Вопрос: ' + (soup.find('vim-content-section-title').text.replace('\n', ' ')).replace('\r',' ')
                results.append(anstitlerow)
            except:
                try:
                    anstitlerow = f'№{x}📝Вопрос: ' + (soup.find('vim-text').text.replace('\n', ' ')).replace('\r',' ')
                    results.append(anstitlerow)
                except:
                    anstitlerow = f'№{x}📝Вопрос'
                    results.append(anstitlerow)
        # а тут много циклов,каждый цикл это разные типы заданий,знаю стремно,но мне лень переделывать
        if random:
            results.append('Это задание рандомное! Ответы могут не совпадать!')
        for i in soup.find_all('vim-test-item', attrs={'correct': 'true'}):
            results.append(await ochistka(i.text))
        for i in soup.find_all('vim-order-sentence-verify-item'):
            results.append(await ochistka(i.text))
        for i in soup.find_all('vim-input-answers'):            
            j = i.find('vim-input-item')
            results.append(await ochistka(j.text))
        for i in soup.find_all('vim-select-item', attrs={'correct': 'true'}):
            results.append(await ochistka(i.text))
        for i in soup.find_all('vim-test-image-item', attrs={'correct': 'true'}):
            results.append(f'{i.text} - Верный')
        for i in soup.find_all('math-input'):
            j = i.find('math-input-answer')
            results.append(await ochistka(j.text))
        for i in soup.find_all('vim-dnd-text-drop'):
            for f in soup.find_all('vim-dnd-text-drag'):
                if i['drag-ids'] == f['answer-id']:
                    results.append(f'{await ochistka(f.text)}')
        for i in soup.find_all('vim-dnd-group-drag'):
            for f in soup.find_all('vim-dnd-group-item'):
                if i['answer-id'] in f['drag-ids']:
                    results.append(f'{await ochistka(f.text)} - {await ochistka(i.text)}')
        for i in soup.find_all('vim-groups-row'):
            for l in i.find_all('vim-groups-item'):
                try:
                    a = base64.b64decode(l['text']) 
                    results.append(f"{await ochistka(a.decode('utf-8'))}")   
                except:
                    pass
        for i in soup.find_all('vim-strike-out-item', attrs={'striked': 'true'}):
            results.append(i.text)
        for i in soup.find_all('vim-dnd-image-set-drag'):
            for f in soup.find_all('vim-dnd-image-set-drop'):
                if i['answer-id'] in f['drag-ids']:
                    image = await ochistka(f['image'])
                    text = await ochistka(i.text)
                    results.append(f'{image} - {text}')
        for i in soup.find_all('vim-dnd-image-drag'):
            for f in soup.find_all('vim-dnd-image-drop'):
                if i['answer-id'] in f['drag-ids']:
                    results.append(f'{f.text} - {i.text}')
    
    for answer in results:
        print(answer)

async def ochistka(string):
    string = string.replace('\n', '')
    string = '→ ' + string
    fraction = re.compile("dfrac{(.*?)}{(.*?)}")
    square_root = re.compile("sqrt{(.*?)}")
    power = re.compile("(.*?)\^(.*)")
    bol = re.compile("gt")
    men = re.compile("lt")
    pm = re.compile('pm')
    perp = re.compile('perp')
    menrav = re.compile('le')
    bolrav = re.compile('ge')
    syst = re.compile('begin{cases}')
    systend = re.compile('end{cases}')
    him = re.compile('mathrm{(.*?)}')
    dot = re.compile('cdot')
    strel = re.compile('rarr')
    pi = re.compile('pi')
    besk = re.compile('infty')
    for i in him.findall(string):
        string = string.replace("\mathrm{" + str(i) + "}", str(i))
    for i in fraction.findall(string):
        string = string.replace("\dfrac{" + str(i[0]) + "}{" + str(i[1]) + "}", str(i[0]) + "/" + str(i[1]))

    for i in square_root.findall(string):
        string = string.replace("\sqrt{" + str(i) + "}", "корень из " + str(i))

    for i in power.findall(string):
        string = string.replace(str(i[0]) + "^" + str(i[1]), str(i[0]) + " ^ " + str(i[1]))

    for i in bol.findall(string):
        string = string.replace("\gt", ">")
    for i in men.findall(string):
        string = string.replace("\lt", "<")
    for i in pm.findall(string):
        string = string.replace("\pm", "±")
    for i in perp.findall(string):
        string = string.replace("\perp", "⊥")
    for i in menrav.findall(string):
        string = string.replace("\le", "≤")
    for i in bolrav.findall(string):
        string = string.replace("\ge", "≥")
    for i in syst.findall(string):
        string = string.replace(r"\begin{cases}", "{")
    for i in systend.findall(string):
        string = string.replace("\end{cases}", "}")
    for i in dot.findall(string):
        string = string.replace(r"\cdot", " ⋅")
    for i in strel.findall(string):
        string = string.replace(r"\rarr", " →")
    for i in pi.findall(string):
        string = string.replace(r"\pi", "π")
    for i in besk.findall(string):
        string = string.replace(r"\infty", "∞")
    return string



taskhash = input('Напишите название комнаты: ')
asyncio.run(answerparse(taskhash))

