# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
import base64
from fpdf import FPDF
import re 
import asyncio
import aiohttp

auth_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2NDM0NzM2NDMsImV4cCI6MTY0NjA2NTY0Mywicm9sZXMiOlsiUk9MRV9FRFVfU0tZU01BUlRfU1RVREVOVF9VU0FHRSJdLCJ1c2VySWQiOjQ4NDEwMDExLCJlbWFpbCI6ImZqc2RqbWZqc25kZmpuQGdtYWlsLmNvbSIsIm5hbWUiOiLQkdC-0LPQtNCw0L0iLCJzdXJuYW1lIjoi0JLQsNC70LDQutCw0YEiLCJpZGVudGl0eSI6InRhbml4YXRpcmUifQ.q9b_1Iy-V6s5zFQGPsHS39apjRBZP_mvxI-s_jhHmt9geEcHAgvNHPOEV9isEgIx9V1cFodYe5O3y3_UZNP0EA54ItBd0S5XmLnH4n3efEIXtfSCqf0j4Edf8hmWgjLAkg46zfqz7E2gv-tD-uBFGz76QtebIyQgV3tSTRNTUdHRTp3pRDyP1wlV4RpAvwoNtOPNJe4inFEpjiQVDeWM7YkP1D1CGpPadrvc72CVfKL5PjKcAz67KBLcgSeg9OIbBCapJ2HZEi6ExOwYzuMFQf2hTSbMvGVVi7Ay0uouNGCCgeTx5WuyYqclugjg8p6-kdPdwM3YnD6ymRU7xZWyZjU77CFjRv9PR_TY_UrdAiE6oanNXNgSUB2uT9vesOmBUGImjhIHY0roZZTyK0n5Ca87M4V--0Gzg0eaMIVRBk5wrd6pdA4sNFg73KYLJ-KDyZCX6u9SHjMWRsrQRjeDOfLlCU-Jx2DHiL4LUxMbJD3mnc8WBR43WLjEg0eQIgFQhoFg-_8xD_BgEhRKBud_4bnWiTHWCrXW9r9Y_oRC-WBIYijzcqiK4Oj6dAxILKhml_mLbSqsxiPwQqjDS58fQUjTuKhFEiKqI1JbYtIVGkDh9mq1L7fl-c6xpsIBYh7pRsJcztQNzrSDpMcOe4oZBe5Vp89apo7bDKFwmGbBtqg'


async def answerparse(taskHash):
    x = 0
    results = []
    # ---- получение uuid заданий в тесте ----#
    url = f"https://api-edu.skysmart.ru/api/v1/task/start"
    payload = "{\"taskHash\":\"" + taskHash + "\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_token

    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as resp:
            roomhashjson = await resp.json() 
            roomHash = roomhashjson['roomHash'] # код рума 
            await session.close()
    
    # ---- тут получаем html в json ----#
    url = "https://api-edu.skysmart.ru/api/v1/lesson/join"
    payload = "{\"roomHash\":\"" + roomHash + "\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_token
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as resp:
            steps_raw = await resp.json()
            await session.close()
    
    
    checkradom = steps_raw['taskStudentMeta']['steps'] # все uuid заданий
    random = False # проверка на рандомные задания
    for uuid in checkradom:
        x = x + 1
        url = "https://api-edu.skysmart.ru/api/v1/content/step/load?stepUuid=" + uuid['stepUuid']
        headers = {
        'Authorization': auth_token
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                answer_row = await resp.json()
                await session.close()
        soup = BeautifulSoup(answer_row['content'], 'html.parser')
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


async def syntaxgood(results):
    results = ' '.join(results)
    r = re.compile("sqrt{(.*?)}")
    bol = re.compile("gt")
    men = re.compile("lt")
    for i in r.findall(results):
        results = results.replace("\sqrt{" + str(i) + "}", "√" + str(i))
    for i in bol.findall(results):
        results = results.replace("\gt", ">")
    for i in men.findall(results):
        results = results.replace("\lt", "<")
    results = results.split(' ')
    
    return results

#\gt > \lt 
