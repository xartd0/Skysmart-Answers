import requests
import json
from bs4 import BeautifulSoup
import base64
from  more_itertools import unique_everseen
from colorama import init, Fore
init(autoreset=True)

auth_token = 'YOUR TOKEN'
results =[]

def answerparse(taskHash):
    url = f"https://api-edu.skysmart.ru/api/v1/task/start"
    payload = "{\"taskHash\":\"" + taskHash + "\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_token

    }
    response = requests.request("POST", url, headers=headers, data=payload)
    roomhashjson = response.json()
    roomHash = roomhashjson['roomHash']
    url = "https://api-edu.skysmart.ru/api/v1/lesson/join"
    payload = "{\"roomHash\":\"" + roomHash + "\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_token
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    steps_raw = response.json()
    try:
        teacherinfo = steps_raw['taskMeta']['teacher']
        subject = steps_raw['taskMeta']['subject']
        titletest = steps_raw['taskMeta']['path']['module']['lesson']
        moduletitle = steps_raw['taskMeta']['path']['module']
    except:
        pass
    checkradom = steps_raw['taskStudentMeta']['steps']
    random = False
    for uuid in checkradom:
        url = "https://api-edu.skysmart.ru/api/v1/content/step/load?stepUuid=" + uuid['stepUuid']
        headers = {
        'Authorization': auth_token
        }
        response = requests.request("GET", url, headers=headers)
        answer_row = response.json()
        soup = BeautifulSoup(answer_row['content'], 'html.parser')
        anstitle = soup.find('vim-instruction')
        anstitlerow = '📝Вопрос:' + (anstitle.text.replace('\n', ' ')).replace('\r',' ')
        results.append(anstitlerow)
        for i in soup.find_all('vim-test-item', attrs={'correct': 'true'}):
            results.append(i.text)
        for i in soup.find_all('vim-input-answers'):
            j = i.find('vim-input-item')
            results.append(j.text)
        for i in soup.find_all('vim-select-item', attrs={'correct': 'true'}):
            results.append(i.text)
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
        for i in soup.find_all('vim-groups-item'):
            arow = i['text']
            a = base64.b64decode(arow) 
            results.append(f"{a.decode('utf-8')}")   
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
        if uuid['isRandom']:
            random = True
            return random
    if random:
        print('В тесте есть рандомные задания!')

                
print("Введите комнату")
taskHash = input()
answerparse(taskHash)
i = 0
for item in results:
    if 'Вопрос' in item:
        i = i + 1
        print(Fore.CYAN + str(i),Fore.MAGENTA + str(item))
    else:
        print(Fore.GREEN + str(item))



