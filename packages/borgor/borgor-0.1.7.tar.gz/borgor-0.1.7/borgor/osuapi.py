import enum
import typing
import aiohttp
import base64
import requests
import pydantic
import textwrap
from datetime import datetime

@enum.unique
class Mods(enum.IntFlag):
    NOMOD = 0
    NOFAIL = 1 << 0
    EASY = 1 << 1
    TOUCHSCREEN = 1 << 2
    HIDDEN = 1 << 3
    HARDROCK = 1 << 4
    SUDDENDEATH = 1 << 5
    DOUBLETIME = 1 << 6
    RELAX = 1 << 7
    HALFTIME = 1 << 8
    NIGHTCORE = 1 << 9
    FLASHLIGHT = 1 << 10
    AUTOPLAY = 1 << 11
    SPUNOUT = 1 << 12
    AUTOPILOT = 1 << 13
    PERFECT = 1 << 14
    KEY4 = 1 << 15
    KEY5 = 1 << 16
    KEY6 = 1 << 17
    KEY7 = 1 << 18
    KEY8 = 1 << 19
    FADEIN = 1 << 20
    RANDOM = 1 << 21
    CINEMA = 1 << 22
    TARGET = 1 << 23
    KEY9 = 1 << 24
    KEYCOOP = 1 << 25
    KEY1 = 1 << 26
    KEY3 = 1 << 27
    KEY2 = 1 << 28
    SCOREV2 = 1 << 29
    MIRROR = 1 << 30

    def __repr__(self) -> str:
        if not self:
            return 'NM'

        if self & Mods.NIGHTCORE:
            self &= ~Mods.DOUBLETIME

        return ''.join(v for k, v in mod_to_str.items() if self & k)

    @classmethod
    def from_str(cls, s: str):
        final_mods = 0
        for m in textwrap.wrap(s.lower(), 2):
            if m not in str_to_mod:
                continue
            
            final_mods += str_to_mod[m]
        
        return cls(final_mods)

str_to_mod = {
    'nm': Mods.NOMOD,
    'ez': Mods.EASY,
    'td': Mods.TOUCHSCREEN,
    'hd': Mods.HIDDEN,
    'hr': Mods.HARDROCK,
    'sd': Mods.SUDDENDEATH,
    'dt': Mods.DOUBLETIME,
    'rx': Mods.RELAX,
    'ht': Mods.HALFTIME,
    'nc': Mods.NIGHTCORE,
    'fl': Mods.FLASHLIGHT,
    'au': Mods.AUTOPLAY,
    'so': Mods.SPUNOUT,
    'ap': Mods.AUTOPILOT,
    'pf': Mods.PERFECT,
    'k1': Mods.KEY1, 
    'k2': Mods.KEY2, 
    'k3': Mods.KEY3, 
    'k4': Mods.KEY4, 
    'k5': Mods.KEY5, 
    'k6': Mods.KEY6, 
    'k7': Mods.KEY7, 
    'k8': Mods.KEY8, 
    'k9': Mods.KEY9,
    'fi': Mods.FADEIN,
    'rn': Mods.RANDOM,
    'cn': Mods.CINEMA,
    'tp': Mods.TARGET,
    'v2': Mods.SCOREV2,
    'co': Mods.KEYCOOP,
    'mi': Mods.MIRROR
}

mod_to_str = {
    Mods.NOFAIL: 'NF',
    Mods.EASY: 'EZ',
    Mods.TOUCHSCREEN: 'TD',
    Mods.HIDDEN: 'HD',
    Mods.HARDROCK: 'HR',
    Mods.SUDDENDEATH: 'SD',
    Mods.DOUBLETIME: 'DT',
    Mods.RELAX: 'RX',
    Mods.HALFTIME: 'HT',
    Mods.NIGHTCORE: 'NC',
    Mods.FLASHLIGHT: 'FL',
    Mods.AUTOPLAY: 'AU',
    Mods.SPUNOUT: 'SO',
    Mods.AUTOPILOT: 'AP',
    Mods.PERFECT: 'PF',
    Mods.KEY4: 'K4',
    Mods.KEY5: 'K5',
    Mods.KEY6: 'K6',
    Mods.KEY7: 'K7',
    Mods.KEY8: 'K8',
    Mods.FADEIN: 'FI',
    Mods.RANDOM: 'RN',
    Mods.CINEMA: 'CN',
    Mods.TARGET: 'TP',
    Mods.KEY9: 'K9',
    Mods.KEYCOOP: 'CO',
    Mods.KEY1: 'K1',
    Mods.KEY3: 'K3',
    Mods.KEY2: 'K2',
    Mods.SCOREV2: 'V2',
    Mods.MIRROR: 'MI'
}

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

@enum.unique
class ScoringType(enum.IntEnum):
    Score = 0
    Accuracy = 1
    Combo = 2
    ScoreV2 = 3

@enum.unique
class TeamType(enum.IntEnum):
    Tag = 0
    Co_op = 1
    Team_vs = 2
    Tag_Team = 3

@enum.unique
class Team(enum.IntEnum):
    Neutral = 0
    Blue = 1
    Red = 2

class Beatmap(pydantic.BaseModel):
    approved: RankingStatus
    submit_date: datetime
    approved_date: typing.Optional[datetime] = None
    last_update: datetime
    artist: str
    beatmap_id: int
    beatmapset_id: int
    bpm: int
    creator: str
    creator_id: int
    difficultyrating: float
    diff_aim: float
    diff_speed: float
    diff_size: float
    diff_overall: float
    diff_approach: float
    diff_drain: float
    hit_length: int
    source: str
    genre_id: Genre
    language_id: Language
    title: str
    total_length: int
    version: str
    file_md5: str
    mode: Gamemode
    tags: list[str]
    favourite_count: int
    rating: float
    playcount: int
    passcount: int
    packs: typing.Any # TODO: look into
    count_normal: int
    count_slider: int
    count_spinner: int
    max_combo: int
    storyboard: bool
    video: bool
    download_unavailable: bool
    audio_unavailable: bool

    @pydantic.validator('tags', pre=True, always=True)
    def tags_match(cls, v: str) -> list[str]:
        return v.split()

class Event(pydantic.BaseModel):
    display_html: str
    beatmap_id: int
    beatmapset_id: int
    date: datetime
    epicfactor: int

class User(pydantic.BaseModel):
    user_id: int
    username: str
    join_date: datetime
    count300: int
    count100: int
    count50: int
    playcount: int
    ranked_score: int
    total_score: int
    pp_rank: int
    level: float
    pp_raw: float
    accuracy: float
    count_rank_ss: int
    count_rank_ssh: int
    count_rank_s: int
    count_rank_sh: int
    count_rank_a: int
    country: str
    total_seconds_played: int
    pp_country_rank: int
    events: list[Event]

class Score(pydantic.BaseModel):
    score_id: int
    score: int
    username: str
    count300: int
    count100: int
    count50: int
    countmiss: int
    maxcombo: int
    countkatu: int
    countgeki: int
    perfect: bool
    enabled_mods: Mods
    user_id: int
    date: datetime
    rank: str
    pp: float = 0.0
    replay_available: bool

    @pydantic.validator('enabled_mods', pre=True, always=True)
    def enabled_mods_match(cls, v: str) -> Mods:
        return Mods(int(v))
    
class UserBestScore(pydantic.BaseModel):
    beatmap_id: int
    score_id: int
    score: int
    maxcombo: int
    count50: int
    count100: int
    count300: int
    countmiss: int
    countkatu: int
    countgeki: int
    perfect: bool
    enabled_mods: Mods
    user_id: int
    date: datetime
    rank: str
    pp: float = 0.0
    replay_available: bool
    
    @pydantic.validator('enabled_mods', pre=True, always=True)
    def enabled_mods_match(cls, v: str) -> Mods:
        return Mods(int(v))

class UserRecentScore(pydantic.BaseModel):
    beatmap_id: int
    score: int
    maxcombo: int
    count50: int
    count100: int
    count300: int
    countmiss: int
    countkatu: int
    countgeki: int
    perfect: bool
    enabled_mods: Mods
    user_id: int
    date: datetime
    rank: str
    
    @pydantic.validator('enabled_mods', pre=True, always=True)
    def enabled_mods_match(cls, v: str) -> Mods:
        return Mods(int(v))

class GameScore(pydantic.BaseModel):
    slot: int
    team: Team
    user_id: int
    score: int
    maxcombo: int
    rank: int
    count50: int
    count100: int
    count300: int
    countmiss: int
    countgeki: int
    countkatu: int
    perfect: bool
    passed: bool = pydantic.Field(..., alias='pass')
    enabled_mods: typing.Optional[Mods] = None

    @pydantic.validator('enabled_mods', pre=True, always=True)
    def enabled_mods_match(cls, v: typing.Optional[str]) -> typing.Optional[Mods]:
        if not v:
            return
        
        return Mods(int(v))

class Game(pydantic.BaseModel):
    game_id: int
    start_time: datetime
    end_time: typing.Optional[datetime] = None
    beatmap_id: int
    play_mode: Gamemode
    match_type: int # unsure
    scoring_type: ScoringType
    team_type: TeamType
    mods: Mods
    scores: list[GameScore]

    @pydantic.validator('mods', pre=True, always=True)
    def mods_match(cls, v: str) -> Mods:
        return Mods(int(v))

class MatchDetails(pydantic.BaseModel):
    match_id: int
    name: str
    start_time: datetime
    end_time: typing.Optional[datetime] = None

class Match(pydantic.BaseModel):
    match: MatchDetails
    games: list[Game]

class Replay(pydantic.BaseModel):
    content: bytes

    @pydantic.validator('content', pre=True, always=True)
    def replay_match(cls, v: str) -> bytes:
        return base64.b64decode(v)

BASE_API = 'https://osu.ppy.sh/api' 

class OsuApi:
    def __init__(
        self, key: str, 
        raise_errors: bool = False,
        http_client: requests.Session = requests.Session()
    ) -> None:
        self.key = key
        self.http = http_client
        self.raise_errors = raise_errors
    
    def get_beatmaps(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[list[Beatmap], list[dict]]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        resp = self.http.get(
            f'{BASE_API}/get_beatmaps',
            params = params
        )

        if not resp:
            if self.raise_errors:
                raise Exception('no response')
            else:
                return
        
        if resp.status_code != 200:
            if self.raise_errors:
                raise Exception(f'response code: {resp.status_code}')
            else:
                return
        
        json: typing.Union[list, list[dict]] = resp.json()
        if not json:
            if self.raise_errors:
                raise Exception('json is empty')
            else:
                return
        
        if raw_json:
            return json
        else:
            return [Beatmap(**bmap) for bmap in json]

    def get_user(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[User, dict]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        resp = self.http.get(
            f'{BASE_API}/get_user',
            params = params
        )

        if not resp:
            if self.raise_errors:
                raise Exception('no response')
            else:
                return
        
        if resp.status_code != 200:
            if self.raise_errors:
                raise Exception(f'response code: {resp.status_code}')
            else:
                return
        
        json: typing.Union[list, list[dict]] = resp.json()
        if not json:
            if self.raise_errors:
                raise Exception('json is empty')
            else:
                return
        
        if raw_json:
            return json[0]
        else:
            return User(**json[0])

    def get_scores(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[list[Score], list[dict]]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        resp = self.http.get(
            f'{BASE_API}/get_scores',
            params = params
        )

        if not resp:
            if self.raise_errors:
                raise Exception('no response')
            else:
                return
        
        if resp.status_code != 200:
            if self.raise_errors:
                raise Exception(f'response code: {resp.status_code}')
            else:
                return
        
        json: typing.Union[list, list[dict]] = resp.json()
        if not json:
            if self.raise_errors:
                raise Exception('json is empty')
            else:
                return
        
        if raw_json:
            return json
        else:
            return [Score(**score) for score in json]

    def get_user_best(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[list[UserBestScore], list[dict]]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        resp = self.http.get(
            f'{BASE_API}/get_user_best',
            params = params
        )

        if not resp:
            if self.raise_errors:
                raise Exception('no response')
            else:
                return
        
        if resp.status_code != 200:
            if self.raise_errors:
                raise Exception(f'response code: {resp.status_code}')
            else:
                return
        
        json: typing.Union[list, list[dict]] = resp.json()
        if not json:
            if self.raise_errors:
                raise Exception('json is empty')
            else:
                return
        
        if raw_json:
            return json
        else:
            return [UserBestScore(**score) for score in json]

    def get_user_recent(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[list[UserRecentScore], list[dict]]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        resp = self.http.get(
            f'{BASE_API}/get_user_recent',
            params = params
        )

        if not resp:
            if self.raise_errors:
                raise Exception('no response')
            else:
                return
        
        if resp.status_code != 200:
            if self.raise_errors:
                raise Exception(f'response code: {resp.status_code}')
            else:
                return
        
        json: typing.Union[list, list[dict]] = resp.json()
        if not json:
            if self.raise_errors:
                raise Exception('json is empty')
            else:
                return
        
        if raw_json:
            return json
        else:
            return [UserRecentScore(**score) for score in json]

    def get_match(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[Match, dict]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        resp = self.http.get(
            f'{BASE_API}/get_match',
            params = params
        )

        if not resp:
            if self.raise_errors:
                raise Exception('no response')
            else:
                return
        
        if resp.status_code != 200:
            if self.raise_errors:
                raise Exception(f'response code: {resp.status_code}')
            else:
                return
        
        json: typing.Optional[dict] = resp.json()
        if not json:
            if self.raise_errors:
                raise Exception('json is empty')
            else:
                return
        
        if raw_json:
            return json
        else:
            return Match(**json)

    def get_replay(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[Replay, dict]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        resp = self.http.get(
            f'{BASE_API}/get_replay',
            params = params
        )

        if not resp:
            if self.raise_errors:
                raise Exception('no response')
            else:
                return
        
        if resp.status_code != 200:
            if self.raise_errors:
                raise Exception(f'response code: {resp.status_code}')
            else:
                return
        
        json: typing.Optional[dict] = resp.json()
        if not json:
            if self.raise_errors:
                raise Exception('json is empty')
            else:
                return
        
        if raw_json:
            return json
        else:
            return Replay(**json)

class AsyncOsuApi:
    def __init__(
        self, key: str, 
        raise_errors: bool = False,
        http_client: aiohttp.ClientSession = aiohttp.ClientSession()
    ) -> None:
        self.key = key
        self.http = http_client
        self.raise_errors = raise_errors
    
    async def get_beatmaps(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[list[Beatmap], list[dict]]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        async with self.http.get(
            f'{BASE_API}/get_beatmaps',
            params = params
        ) as resp:

            if not resp:
                if self.raise_errors:
                    raise Exception('no response')
                else:
                    return
            
            if resp.status != 200:
                if self.raise_errors:
                    raise Exception(f'response code: {resp.status}')
                else:
                    return
        
            json: typing.Union[list, list[dict]] = await resp.json()
            if not json:
                if self.raise_errors:
                    raise Exception('json is empty')
                else:
                    return
            
            if raw_json:
                return json
            else:
                return [Beatmap(**bmap) for bmap in json]

    async def get_user(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[User, dict]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        async with self.http.get(
            f'{BASE_API}/get_user',
            params = params
        ) as resp:

            if not resp:
                if self.raise_errors:
                    raise Exception('no response')
                else:
                    return
            
            if resp.status != 200:
                if self.raise_errors:
                    raise Exception(f'response code: {resp.status}')
                else:
                    return
            
            json: typing.Union[list, list[dict]] = await resp.json()
            if not json:
                if self.raise_errors:
                    raise Exception('json is empty')
                else:
                    return
            
            if raw_json:
                return json[0]
            else:
                return User(**json[0])

    async def get_scores(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[list[Score], list[dict]]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        async with self.http.get(
            f'{BASE_API}/get_scores',
            params = params
        ) as resp:

            if not resp:
                if self.raise_errors:
                    raise Exception('no response')
                else:
                    return
            
            if resp.status != 200:
                if self.raise_errors:
                    raise Exception(f'response code: {resp.status}')
                else:
                    return
            
            json: typing.Union[list, list[dict]] = await resp.json()
            if not json:
                if self.raise_errors:
                    raise Exception('json is empty')
                else:
                    return
            
            if raw_json:
                return json
            else:
                return [Score(**score) for score in json]

    async def get_user_best(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[list[UserBestScore], list[dict]]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        async with self.http.get(
            f'{BASE_API}/get_user_best',
            params = params
        ) as resp:

            if not resp:
                if self.raise_errors:
                    raise Exception('no response')
                else:
                    return
            
            if resp.status != 200:
                if self.raise_errors:
                    raise Exception(f'response code: {resp.status}')
                else:
                    return
            
            json: typing.Union[list, list[dict]] = await resp.json()
            if not json:
                if self.raise_errors:
                    raise Exception('json is empty')
                else:
                    return
            
            if raw_json:
                return json
            else:
                return [UserBestScore(**score) for score in json]

    async def get_user_recent(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[list[UserRecentScore], list[dict]]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        async with self.http.get(
            f'{BASE_API}/get_user_recent',
            params = params
        ) as resp:

            if not resp:
                if self.raise_errors:
                    raise Exception('no response')
                else:
                    return

            if resp.status != 200:
                if self.raise_errors:
                    raise Exception(f'response code: {resp.status}')
                else:
                    return

            json: typing.Union[list, list[dict]] = await resp.json()
            if not json:
                if self.raise_errors:
                    raise Exception('json is empty')
                else:
                    return

            if raw_json:
                return json
            else:
                return [UserRecentScore(**score) for score in json]

    async def get_match(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[Match, dict]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        async with self.http.get(
            f'{BASE_API}/get_match',
            params = params
        ) as resp:

            if not resp:
                if self.raise_errors:
                    raise Exception('no response')
                else:
                    return
            
            if resp.status != 200:
                if self.raise_errors:
                    raise Exception(f'response code: {resp.status}')
                else:
                    return
            
            json: typing.Optional[dict] = await resp.json()
            if not json:
                if self.raise_errors:
                    raise Exception('json is empty')
                else:
                    return
            
            if raw_json:
                return json
            else:
                return Match(**json)

    async def get_replay(
        self, params: dict, 
        raw_json: bool = False
    ) -> typing.Optional[
            typing.Union[Replay, dict]
        ]:

        if 'k' not in params:
            params['k'] = self.key
        
        async with self.http.get(
            f'{BASE_API}/get_replay',
            params = params
        ) as resp:

            if not resp:
                if self.raise_errors:
                    raise Exception('no response')
                else:
                    return
            
            if resp.status != 200:
                if self.raise_errors:
                    raise Exception(f'response code: {resp.status}')
                else:
                    return
            
            json: typing.Optional[dict] = await resp.json()
            if not json:
                if self.raise_errors:
                    raise Exception('json is empty')
                else:
                    return
            
            if raw_json:
                return json
            else:
                return Replay(**json)