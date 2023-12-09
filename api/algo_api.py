import aiohttp
from .algo_errors import *
from .algo_classes import *

class AsyncSession:
    # Управление Сессией
    async def login(self, login:str, password:str):
        """
        ## Входит в ваш Аккаунт на Алгоритмике.
        - Если логин или пароль неверен вернёт ошибку.
        - Если вы уже вошли, то вернёт ошибку.
        """
        self.session = None
        self.id = None
        self.login_name = login
        self.password = password
        await self.login_algo(login_name=self.login_name, password=self.password)
    
    async def login_algo(self, login_name, password):
        if self.session is not None:
            raise AsyncAlreadyLoggedIn('Вы уже вошли в Систему! |You are already logged in!')

        self.session = aiohttp.ClientSession()

        async with self.session.post('https://learn.algoritmika.org/s/auth/api/e/student/auth', data={
            'login': login_name,
            'password': password
        }) as res:
            if res.status == 200:
                item = await res.json()
                self.id = item['item']['studentId']
            elif res.status == 400:
                raise AsyncInvalidCredentials('Логин Или пароль неверен! | Login or Password is incorrect!')
            else:
                raise AsyncUnknownException(await res.json())

    async def close(self):
        '''
        ## Закрывает сессию для активации Сессии: используйте login()
        '''
        if self.session is not None:
            await self.session.close()
            self.session = None
            self.id = None

    # Технические Хендлеры

    async def fetch(self, method, *args, **kwargs):
        if self.session is not None:
            async with method(*args, **kwargs) as res:
                if res.status == 200:
                    return await res.json()
                else:
                    raise AsyncUnknownException(await res.json())
        else:
            raise AsyncSessionClosed('Сессия закрыта, используйте метод login() для входа | Session closed, use login() method to login')

    async def post(self, *args, **kwargs):
        return await self.fetch(method=self.session.post, *args, **kwargs)

    async def get(self, *args, **kwargs):
        return await self.fetch(method=self.session.get, *args, **kwargs)

    async def delete(self, *args, **kwargs):
        return await self.fetch(method=self.session.delete, *args, **kwargs)

    # Профиль Пользователя.

    async def my_profile(self):
        '''
        ## Возвращает информацию о Аккаунте с которого вы вошли.
        '''
        data = await self.get('https://learn.algoritmika.org/api/v1/profile?expand=branch,settings,locations,permissions,avatar,referral,course')
        return SelfProfile(data['data'])
    
    async def get_profile(self, id:int):
        '''
        ## Возвращает Информацию о Пользователе по ID
        - Если ID пользователя не указано вернёт Ошибку.
        '''
        if id is None:
            raise AsyncUserIdUnspecified(f'\'id\' ID проекта не указан! | The project ID is not specified!')
        elif type(id) != int:
            raise TypeError(f'\'id\' Должно быть числом! | Must be a number! INT')
        
        data = await self.get(
            f'https://learn.algoritmika.org/api/v2/community/profile/index?expand=stats,avatars&studentId={id}'
        )
        return Profile(data['data'])
    

    # Проекты.
    async def my_projects(self, sort=SORT_LATEST):
        '''
        ## Возвращает все Проекты Пользователя.
        '''
        data = await self.get(
            f'https://learn.algoritmika.org/api/v1/projects?\
            expand=uploads,remix&sort=-{sort}&scope=student&\
            type=design,gamedesign,images,presentation,python,scratch,unity,video,vscode,website',
        )
        return [Project(i) for i in data['data']['items']]

    async def edit_project(self, id:int=None, title:str = None, description:str = None):
        '''
        ## Изменяет Проект пользователя по ID проекта.
        - Если проект не от Пользователя с Аккаунта которого вы вошли, то вернёт Ошибку.
        - Если вы ничего не указали вернёт Ошибку.
        '''
        if id is None:
            raise AsyncProjectIdUnspecified(f'\'id\' ID проекта не указан! | The project ID is not specified!')
        elif type(id) != int:
            raise TypeError(f'\'id\' Должно быть числом! | Must be a number! INT')
        data = {}
        if title is not None:
            data['title'] = str(title)
        if description is not None:
            data['description'] = str(description)

        if len(data) == 0:
            raise ValueError('Необходимо указать название и/или описание | Either title and/or description must be provided')
        await self.post(f'https://learn.algoritmika.org/api/v1/projects/update/{id}', data=data)
    

    async def get_project(self, id:int=None):
        '''
        ## Возвращает проект по ID проекта.
        - Если ID не указан Вернёт ошибку.
        '''
        if id is None:
            raise AsyncProjectIdUnspecified(f'\'id\' ID проекта не указан! | The project ID is not specified!')
        elif type(id) != int:
            raise TypeError(f'\'id\' Должно быть числом! | Must be a number! INT')
        
        data = await self.get(
            f'https://learn.algoritmika.org/api/v1/projects/info/{id}?\
            expand=uploads,remix',
        )
        return Project(data['data'])
    

    async def get_projects(self, id:int=None, page:int=1, per_page:int=50, sort=SORT_LATEST):
        '''
        ## Возвращает все проекты Пользователя.
        - Если указан ID возвращает все проекты Пользователя с Данным ID.
        - Если ID не указан возвращает все проекты Пользоавтеля под которым вы вошли в Систему.
        '''
        if id is None:
            data = await self.get(
                f'https://learn.algoritmika.org/api/v1/projects?\
                expand=uploads,remix&sort=-{sort}&scope=universe&\
                type=design,gamedesign,images,presentation,python,scratch,unity,video,vscode,website&\
                page={page}&perPage={per_page}',
            )
        elif type(id) == int:
            data = await self.get(
                f'https://learn.algoritmika.org/api/v1/projects?\
                expand=uploads,remix&sort=-{sort}&scope=universe&\
                type=design,gamedesign,images,presentation,python,scratch,unity,video,vscode,website&\
                page={page}&perPage={per_page}&studentId={id}',
            )
        else:
            raise TypeError(f'\'id\' Должно быть числом! | Must be a number! INT')

        return [Project(i) for i in data['data']['items']]


    # Реакции!
    async def place_reaction(self, id:int=None, reaction:str=None):
        '''
        ## Устонавливает на Проект с Указанным ID рекацию.\n
        - Если ID не указан Вернёт Ошибку.\n
        - Если не указана Реакция Вернёт Ошибку.
        '''
        if id is None:
            raise AsyncProjectIdUnspecified(f'\'id\' ID проекта не указан! | The project ID is not specified!')
        elif type(id) != int:
            raise TypeError(f'\'id\' Должно быть числом! | Must be a number! INT')
        
        if reaction is None:
            raise AsyncReactionUnspecified(f'\'reaction\' Реакция не указана! | The Reaction is not specified!')
        
        await self.post(
            'https://learn.algoritmika.org/api/v2/community/reaction/add',
            data={
                'ownerId': id,
                'ownerType': 'project_relation',
                'type': reaction
            }
        )
        
        
    async def remove_reaction(self, id:int=None, reaction:str=None):
        '''
        ## Удаляет с Проекта с Указанным ID рекацию.\n
        - Если ID не указан Вернёт Ошибку.\n
        - Если не указана Реакция Вернёт Ошибку.
        '''
        if id is None:
            raise AsyncProjectIdUnspecified(f'\'id\' ID проекта не указан! | The project ID is not specified!')
        elif type(id) != int:
            raise TypeError(f'\'id\' Должно быть числом! | Must be a number! INT')
        
        if reaction is None:
            raise AsyncReactionUnspecified(f'\'reaction\' Реакция не указана! | The Reaction is not specified!')
        
        await self.post(
            'https://learn.algoritmika.org/api/v2/community/reaction/remove',
            data={
                'ownerId': id,
                'ownerType': 'project_relation',
                'type': reaction
            }
        )
    

    # Комментарии! *^____^*
    async def post_comment(self, id:int=None, text:str=None, reply_to:int = None):
        '''
        ## Публикует Комментарий под проектом с Указанным ID.\n
        - Если ID не указан Вернёт Ошибку.
        '''
        if id is None:
            raise AsyncProjectIdUnspecified(f'\'id\' ID проекта не указан! | The project ID is not specified!')
        elif type(id) != int:
            raise TypeError(f'\'id\' Должно быть числом! | Must be a number! INT')
        
        if text is None:
            raise ValueError('Текст комментария не указан! | Comment text not specified!')
        
        if reply_to == None:
            data = {'message': text}
        else:
            if type(reply_to) != int:
                raise TypeError(f'\'reply_to\' Должно быть числом! | Must be a number! INT')
            data = {'message': text, 'parentCommentId': reply_to}
        
        data = await self.post(
            f'https://learn.algoritmika.org/api/v1/projects/comment/{id}',
            data=data
        )
        return Comment(data['data'])
        
        
    async def delete_comment(self, id:int=None):
        '''
        ## Удаляет Комментарий с Указанным ID.\n
        - Если ID не указан Вернёт Ошибку.
        '''
        if id is None:
            raise AsyncCommentIdUnspecified(f'\'id\' ID Комментария не указан! | The Comment ID is not specified!')
        elif type(id) != int:
            raise TypeError(f'\'id\' Должно быть числом! | Must be a number! INT')
        
        await self.delete(
            f'https://learn.algoritmika.org/api/v1/projects/comment/{id}'
        )
        
        
    async def get_comments(self, id:int=None, page:int = 1, per_page:int = 50):
        '''
        ## По умолчанию Получает все Комментарии под проектом с Указанным ID начиная с Страницы 1 до страницы 50.\n
        ### Вы также можете назначить своё Значение page и per_page\n
        - Если ID не указан Вернёт Ошибку.
        '''
        if id is None:
            raise AsyncProjectIdUnspecified(f'\'id\' ID проекта не указан! | The project ID is not specified!')
        elif type(id) != int:
            raise TypeError(f'\'id\' Должно быть числом! | Must be a number! INT')
        if type(page) != int:
            raise TypeError(f'\'page\' Должно быть числом! | Must be a number! INT')
        if type(per_page) != int:
            raise TypeError(f'\'per_page\' Должно быть числом! | Must be a number! INT')
        
        data = await self.get(
            f'https://learn.algoritmika.org/api/v1/projects/comment/{id}?\
            page={page}&perPage={per_page}&sort=-id',
        )
        comments = [Comment(i) for i in data['data']['items']]

        if comments:
            return comments
        else:
            raise AsyncCommentNotFound('Комментарии не найдены! | No comments found!')
    

    async def get_now_comment(self, id:int=None):
        page = 1
        per_page = 1
        '''
        ## Получает последний Комментарий под проектом с Указанным ID.\n
        - Если ID не указан Вернёт Ошибку.\n
        - Если Комментариев нет Вернёт Ошибку.
        '''
        if id is None:
            raise AsyncProjectIdUnspecified(f'\'id\' ID проекта не указан! | The project ID is not specified!')
        elif type(id) != int:
            raise TypeError(f'\'id\' Должно быть числом! | Must be a number! INT')
        
        data = await self.get(
            f'https://learn.algoritmika.org/api/v1/projects/comment/{id}?'
            f'page={page}&perPage={per_page}&sort=-id',
        )
        
        comments = [Comment(i) for i in data['data']['items']]
        
        if comments:
            return comments[0]
        else:
            raise AsyncCommentNotFound('Комментарии не найдены! | No comments found!')


    # Код Проекта Python
    async def get_source_code(self, id:int=None) -> str:
        '''
        ## Возвращает код вашего `python` проекта.\n
        - Если ID не указан Вернёт Ошибку.\n
        - Если проект не на `python` вернёт ошибку.
        '''
        if id is None:
            raise AsyncProjectIdUnspecified(f'\'id\' ID проекта не указан! | The project ID is not specified!')
        elif type(id) != int:
            raise TypeError(f'\'id\' Должно быть числом! | Must be a number! INT')
        
        res = await self.get(f'https://learn.algoritmika.org/api/v1/projects/info/{id}?expand=uploads')
        res = res['data']
        if res['type'] != 'python':
            raise TypeError('Проект должен быть проектом `python`. | Project should be a `python` project.')
        
        res = self.get(f"https://learn.algoritmika.org/api/v1/python/open?id={res['meta']['projectId']}")
        return res['data']['content']
    

    async def change_source_code(self, id:int = None, code:str = None):
        '''
        ## Изменяет код вашего `python` проекта.\n
        - Если ID не указан вернёт ошибку.\n
        - Если Code не указан вернёт ошибку.\n
        - Если проект не на `python` вернёт ошибку.
        '''
        if id is None:
            raise AsyncProjectIdUnspecified(f'\'id\' ID проекта не указан! | The project ID is not specified!')
        elif type(id) != int:
            raise TypeError(f'\'id\' Должно быть числом! | Must be a number! INT')
        
        if code is None:
            raise AsyncCodeUnspecified(f'\'code\' Новый код Проекта не указан! | The new Project code is not specified!')
        
        res = self.get(f'https://learn.algoritmika.org/api/v1/projects/info/{id}?expand=uploads')
        res = res['data']
        if res['type'] != 'python':
            raise TypeError('Проект должен быть проектом `python`. | Project should be a `python` project.')
        
        self.post(
            f"https://learn.algoritmika.org/api/v1/python/save?id={res['meta']['projectId']}",
            data={"content": str(code), "name": res['title']}
        )
    

    # Тренды
    async def get_trending(self, interval:str):
        '''
        ## Получает и Возвращает все Популярные проекты из Трендов за указанный период.\n
        Значение `interval` должно быть любым из следующей таблицы:
        | Переменная | Описание |
        |-----|-----|
        | `algo_api_async.TRENDS_DAY` | Тренды за день |
        | `algo_api_async.TRENDS_WEEK` | Тренды за неделю |
        | `algo_api_async.TRENDS_MONTH` | Тренды за месяц |
        '''
        data = await self.get(
            f'https://learn.algoritmika.org/api/v1/projects/trends?\
            interval={interval}&expand=remix'
        )

        return [Project(i) for i in data.json()['data']['items']]