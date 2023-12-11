import aiohttp
from user_agent import generate_user_agent
from utils import api_variables as api
from utils import config


async def get_headers():
    """---- Получаем jwt токен при входе в аккаунт skysmart ----"""
    user_agent = generate_user_agent()

    async with aiohttp.ClientSession() as session:
        async with session.post(api.url_auth, headers={'User-Agent': user_agent}, data=config.auth_creds) as resp:
            
            json_resp = await resp.json() 

            return {
                'Accept' : 'application/json, text/plain, */*',
                'Authorization': 'Bearer ' + json_resp['jwtToken'],
                'Connection' : 'keep-alive',
                'Content-Type': 'application/json',
                'User-Agent': user_agent,
            }

async def get_room(taskHash):
    """---- Получаем uuid всех заданий в тесте ----"""
    payload = "{\"taskHash\":\"" + taskHash + "\"}"
    headers = await get_headers()

    async with aiohttp.ClientSession() as session:
        async with session.post(api.url_room, headers=headers, data=payload) as resp:

            steps_raw = await resp.json() 
            await session.close()

            return steps_raw['meta']['stepUuids'] 
        

async def get_meta(taskHash):
    payload = "{\"taskHash\":\"" + taskHash + "\"}"
    headers = await get_headers()

    async with aiohttp.ClientSession() as session:
        async with session.post(api.url_room, headers=headers, data=payload) as resp:
            steps_raw = await resp.json() 
            await session.close()
            return steps_raw["title"],steps_raw["meta"]["path"]["module"]["title"]
        
            
async def get_task_html(uuid):
    """---- Получаем html по uuid каждого задания отдельно ----"""
    headers = await get_headers()

    async with aiohttp.ClientSession() as session:
        async with session.get(api.url_steps + uuid, headers=headers) as resp:

            answer_row = await resp.json()
            await session.close()

    return answer_row['content']
