import aiohttp
from user_agent import generate_user_agent
from utils import api_variables as api
from utils.auth import get_token
import json


async def load_token_from_json(filename="token.json"):
    """Load the token from a JSON file."""
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data.get("token")
    except FileNotFoundError:
        print(f"Токена нет, начинаем процесс получения токена, подождите.")
        success = get_token()
        if success:
            print("Токен был успешно получен и сохранен в token.json")
            return await load_token_from_json()  # Повторный вызов функции после получения токена
    except Exception as e:
        print(f"Failed to load token: {e}")
    return None


async def get_headers():
    """Get jwt token for Skysmart account login."""
    token = await load_token_from_json()
    if token:
        user_agent = generate_user_agent()
        return {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer ' + token,
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'User-Agent': user_agent,
        }
    else:
        return None


async def get_room(taskHash, session):
    """Get uuid for all tasks in a test."""
    payload = "{\"taskHash\":\"" + taskHash + "\"}"
    headers = await get_headers()

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
    headers = await get_headers()
    payload = "{\"taskHash\":\"" + taskHash + "\"}"

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
    headers = await get_headers()

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


async def get_room_info(session, taskHash):
    """Get room info about skysmart room test."""
    headers = await get_headers()

    payload = "{\"taskHash\":\"" + taskHash + "\"}"

    try:
        async with session.post(api.url_room_preview, headers=headers, data=payload) as resp:
            if resp.status == 200:

                json_resp = await resp.json()

                return json_resp
            else:
                raise Exception(f"Room info request failed with status: {resp.status}")
    except Exception as e:
        print(f"Error during getting info about room: {e}")
        return None
