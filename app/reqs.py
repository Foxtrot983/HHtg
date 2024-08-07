from aiohttp import ClientSession
from .config import CLIENT_ID, CLIENT_SECRET, APP_ACCESS_TOKEN
from .errors import TokenError

async def async_request(method: str, url: str, headers:dict = None, data:dict=None):
    #proxy = choice(PROXIES.split(',')[:-1]) if PROXIES else None
    try:
        async with ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers, data=data) as response:
                if response.status == 403 or response.status == 400:
                    raise TokenError('токен')
                result = await response.json()
        return result
    except Exception as e:
        print(e)



async def get_user_access_token(token:str, refresh:bool=False) -> dict|bool:
    #Соответственно если refresh=True, то пойдет рефреш токена
    url = f'https://hh.ru/oauth/token'
    if refresh:
        body = {
            'refresh_token':refresh_token,
            'grant_type':'refresh_token',
        }
    else:
        body = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code':token,
            'grant_type':'authorization_code',
            #'redirect_uri': 'http://www.lisatrottest.com/oauth',
        }
    headers = {
        'OauthToken': f'Bearer {APP_ACCESS_TOKEN}',
        'HH-User-Agent':'LisatrotApp/1.0 (wladiksan@gmail.com)'
    }
    
    result = await async_request(method='POST', url=url, headers=headers, data=body)
    access_token = result.get('access_token')
    refresh_token = result.get('refresh_token')
    status = True
    if not access_token:
        status = False
        raise TokenError("Ошибка токена")
    output = {
        'status': status,
        'access_token': result.get('access_token'),
        'refresh_token': result.get('refresh_token'),
    }
    return output


async def get_resumes(access_token:str):
    url = 'https://api.hh.ru/resumes/mine'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    req = await async_request(method='get', url=url, headers=headers)
    resumes = [{'id':i.get('id'), 'name':i.get('title')} for i in req.get('items') if i.get('title')!=None]
    return resumes


async def get_vacs(access_token:str, resume_id:str):
    url = f'https://api.hh.ru/resumes/{resume_id}/similar_vacancies'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    req = await async_request(method='get', url=url, headers=headers)
    vacs = [{'name':x.get('name'), 'url':x.get('alternate_url')} for x in req.get('items')[:10]]
    return vacs