import aiohttp
from user_agent import generate_user_agent
from utils import api_variables as api
from utils import config

async def get_headers(session):
    """Get jwt token for Skysmart account login."""
    user_agent = generate_user_agent()

    try:
        async with session.post(api.url_auth, headers={'User-Agent': user_agent}, data=config.auth_creds) as resp:
            if resp.status == 200:
                json_resp = await resp.json()
                return {
                    'Accept': 'application/json, text/plain, */*',
                    'Authorization': 'Bearer ' + json_resp['jwtToken'],
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/json',
                    'User-Agent': user_agent,
                }
            else:
                raise Exception(f"Auth request failed with status: {resp.status}")
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

async def get_room(taskHash, session):
    """Get uuid for all tasks in a test."""
    payload = "{\"taskHash\":\"" + taskHash + "\"}"
    headers = await get_headers(session)

    if headers is not None:
        try:
            async with session.post(api.url_room, headers=headers, data=payload) as resp:
                if resp.status == 200:
                    steps_raw = await resp.json()
                    return steps_raw['meta']['stepUuids']
                else:
                    raise Exception(f"Room request failed with status: {resp.status}")
        except Exception as e:
            print(f"Error during getting room: {e}")

async def get_meta(taskHash, session):
    """Get metadata for a task."""
    payload = "{\"taskHash\":\"" + taskHash + "\"}"
    headers = await get_headers(session)

    if headers is not None:
        try:
            async with session.post(api.url_room, headers=headers, data=payload) as resp:
                if resp.status == 200:
                    steps_raw = await resp.json()
                    return steps_raw["title"], steps_raw["meta"]["path"]["module"]["title"]
                else:
                    raise Exception(f"Meta request failed with status: {resp.status}")
        except Exception as e:
            print(f"Error during getting meta: {e}")

async def get_task_html(uuid, session):
    """Get HTML for a task by uuid."""
    headers = await get_headers(session)

    if headers is not None:
        try:
            async with session.get(api.url_steps + uuid, headers=headers) as resp:
                if resp.status == 200:
                    answer_row = await resp.json()
                    return answer_row['content']
                else:
                    raise Exception(f"Task HTML request failed with status: {resp.status}")
        except Exception as e:
            print(f"Error during getting task HTML: {e}")
