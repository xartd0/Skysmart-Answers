import aiohttp
from user_agent import generate_user_agent
from utils import api_variables as api
from utils import config

async def get_headers(session):
    """Get jwt token for Skysmart account login."""
    user_agent = generate_user_agent()

    return {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': 'Bearer ' + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MDc3MjgwODIsImV4cCI6MTcxMDMyMDA4Miwicm9sZXMiOlsiUk9MRV9FRFVfU0tZU01BUlRfU1RVREVOVF9VU0FHRSJdLCJhdXRoVXNlcklkIjpudWxsLCJ1c2VySWQiOjg1NTY2NDY3LCJpZGVudGl0eSI6InhvZG9iZXZlbWEifQ.RIhsOczwutlD5797b-Zk973ObMVy76axkTX0NAmsUtBNkvO1v6FRzc0EFTlryNFDj4SlfIyA_5qo_cNRLxYHKRmq6DxfLAnzB4jw-RU18DWjB9r6VR1ayDjEsS9yn1WsJf6u9rqdtLld2AchbNxuaRunULJPNm23tNJU9ejLQxea87bBZsUOmywyoQeiau0F-mGOGfOZjPYcoA7Hg_g755EVR0c-W--uEClC0w4adYj59NY5wL-tnBOQsdgU-7_2MV3p3IoXUdcDtVaPTA0nz0ymTrI1eaTElcXuZuGQkjQuwoQsjLVTNEKQJYjlAGr-JyIMh-i4cjY7ETA8uCZMho-cNFvMybU-63SBr57nvyiFLyx1X6QADCgJHBrrh_-Q6UQDbmPAekDsPv9-JrAiuEvOvGBPt3vGwZZpiFHl6d3HH5BkcP2FB8R5wJLZwNOyKHALlJv9r2ww1KFUPDssm2ZJtHZ9_r2YtJ00yqcBsPbhMIMQSHN04xEyODVK_oiNau9vabp24klHcUFT2fCKfDqXYHYwC1sv_BNf8V3kEzPTGC1EvSQMuMz11huWmmg_JKmNdVZM78E3_79ZMJKY4mSO_NB4-ExpnGtB-ETbZ_uIQJfuD6Fy2BtAGzZFpzNivLYyPOFemke4Gn2V3ro23xaSFQ7iT00FF3SyrMOhaAE',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'User-Agent': user_agent,
    }

    # try:
    #     async with session.post(api.url_auth, headers={'User-Agent': user_agent}, data=config.auth_creds) as resp:
    #         if resp.status == 200:
    #             json_resp = await resp.json()
    #             return {
    #                 'Accept': 'application/json, text/plain, */*',
    #                 'Authorization': 'Bearer ' + json_resp['jwtToken'],
    #                 'Connection': 'keep-alive',
    #                 'Content-Type': 'application/json',
    #                 'User-Agent': user_agent,
    #             }
    #         else:
    #             raise Exception(f"Auth request failed with status: {resp.status}")
    # except Exception as e:
    #     print(f"Error during authentication: {e}")
    #     return None

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
    headers = await get_headers(session)
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


async def get_room_info(session, taskHash):
    """Get room info about skysmart room test."""
    headers = await get_headers(session)

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
