import enum
import typing
import aiohttp
import pydantic
import requests
from datetime import datetime

BASE_API_V1 = 'https://akatsuki.pw/api/v1'
BASE_API_PEPPY = 'https://akatsuki.pw/api'

num_to_str = {
    0: 'osu',
    1: 'taiko',
    2: 'fruits',
    3: 'mania'
}

@enum.unique
class Gamemode(enum.IntEnum):
    STD = 0
    Taiko = 1
    Ctb = 2
    Mania = 4

    @property
    def as_str(self) -> int:
        return num_to_str[int(self)] # type: ignore

@enum.unique
class Language(enum.IntEnum):
    Any = 0
    Unspecified = 1
    English = 2
    Japanese = 3
    Chinese = 4
    Instrumental = 5
    Korean = 6
    French = 7
    German = 8
    Swedish = 9
    Spanish = 10
    Italian = 11
    Russian = 12
    Polish = 13
    Other = 14

@enum.unique
class Genre(enum.IntEnum):
    Any = 0
    Unspecified = 1
    VideoGame = 2
    Anime = 3
    Rock = 4
    Pop = 5
    Other = 6
    Novelty = 7
    HipHop = 9
    Electronic = 10
    Metal = 11
    Classical = 12
    Folk = 13
    Jazz = 14

@enum.unique
class RankingStatus(enum.IntEnum):
    Loved = 4
    Qualified = 3
    Approved = 2
    Ranked = 1
    Pending = 0
    WIP = -1
    Graveyard = -2

class Beatmap(pydantic.BaseModel):
    approved: RankingStatus
    approved_date: datetime
    beatmap_id: int
    beatmapset_id: int
    bpm: int
    creator: str
    diff_approach: float
    diff_drain: float
    diff_overall: float
    diff_size: float
    difficultyrating: float
    favourite_count: int
    file_md5: str
    genre_id: Genre
    hit_length: int
    language_id: Language
    last_update: datetime
    max_combo: int
    mode: Gamemode
    passcount: int
    playcount: int
    source: str
    tags: list[str]
    title: str
    total_length: int
    version: str

    @pydantic.validator('tags', pre=True, always=True)
    def tags_match(cls, v: str) -> list[str]:
        return v.split()

class AkatsukiApi:
    def __init__(
        self, raise_errors: bool = False, 
        http_client: requests.Session = requests.Session()
    ) -> None:
        self.raise_errors = raise_errors
        self.http = http_client

    def get_beatmaps(self, params: dict, raw_json: bool = False) -> typing.Optional[typing.Union[list[Beatmap], list[dict]]]:
        resp = self.http.get(
            url = f'{BASE_API_PEPPY}/get_beatmaps',
            params = params
        )
        
        if not resp:
            if self.raise_errors:
                raise Exception('response was not found.')
            else:
                return
        
        if resp.status_code != 200:
            if self.raise_errors:
                raise Exception(f'expected 200 response code, got {resp.status}')
            else:
                return

        json = resp.json()
        if not json:
            if self.raise_errors:
                raise Exception('json is empty')
            else:
                return

        if raw_json:
            return json
        else:
            return [Beatmap(**bmap) for bmap in json]

class AsyncAkatsukiApi:
    ...

"""
class AkatsukiApi:
    def __init__(
        self, raise_errors: bool = False, 
        http_client: aiohttp.ClientSession = aiohttp.ClientSession()
    ) -> None:

        self.raise_errors = raise_errors
        self.http = http_client

    async def get_json(self, url: str, **kwargs) -> Optional[dict]:
        async with self.client.get(url, **kwargs) as resp:
            if not resp:
                if self.raise_errors:
                    raise Exception('response was not found.')
                else:
                    return
            
            if resp.status != 200:
                if self.raise_errors:
                    raise Exception(f'expected 200 response code, got {resp.status}')
                else:
                    return
            
            return await resp.json()

    async def get_beatmaps(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_PEPPY}/get_beatmaps',
            params = params
        )
    
    async def get_user_peppy(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_PEPPY}/get_user',
            params = params
        )
    
    async def get_scores(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_PEPPY}/get_scores',
            params = params
        )
    
    async def get_user_best_peppy(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_PEPPY}/get_user_best',
            params = params
        )
    
    async def get_user_recent_peppy(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_PEPPY}/get_user_recent',
            params = params
        )
    
    async def get_ping(self) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/ping'
        )
    
    async def get_surprise_me(self) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/surprise_me'
        )

    async def get_users(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users',
            params = params
        )
    
    async def get_users_full(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/full',
            params = params
        )

    async def get_users_whatid(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/whatid',
            params = params
        )
    
    async def get_users_userpage(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/userpage',
            params = params
        )

    async def get_users_lookup(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/lookup',
            params = params
        )
    
    async def get_users_achievements(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/achievements',
            params = params
        )
    
    async def get_users_most_played(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/most_played',
            params = params
        )
    
    async def get_badges(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/badges',
            params = params
        )
    
    async def get_badges_members(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/badges',
            params = params
        )
    
    async def get_scores(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/scores',
            params = params
        )
    
    async def get_user_recent(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/scores/recent',
            params = params
        )
    
    async def get_user_best(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/scores/best',
            params = params
        )
"""