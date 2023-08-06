import time
import json
from pathlib import Path
from collections import UserDict
from multiprocessing import Process

class JsonFile(UserDict):
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.last_updated: float = time.time()

        if not self.path.exists():
            self.path.write_bytes(b"{}")
            super().__new__(UserDict)
        else:
            data = json.loads(self.path.read_bytes() or b"{}")
            super().__init__(**data)

        self.process = Process(target=self.update_file)
        self.process.start()

    def update_file(self) -> None:
        while time.sleep(2) or True:
            self.path.write_text(json.dumps(dict(self), indent=len(self)))
            self.last_updated = time.time()

    def stop(self) -> None:
        self.process.terminate()
        self.path.write_text(json.dumps(dict(self), indent=len(self)))

def string_to_key(s: str) -> str:
    """
    Makes a string into a valid key
    meant for things like 
    ```py
    self.__dict__[string_to_key(str)] = value
    ```
    """
    new_str = ''
    for i, char in enumerate(s):
        if i == 0:
            new_str += char.lower()
        elif char == 'I' and s[i+1] == 'D':
            new_str += '_i'
        elif char == 'D' and s[i-1] == 'I':
            new_str += 'd'
        elif char == 'H' and s[i+1] == 'P':
            new_str += '_h'
        elif char == 'P' and s[i-1] == 'H':
            new_str += 'p'
        elif char.isupper():
            new_str += f'_{char.lower()}'
        else:
            new_str += char
    
    return new_str

def isdecimal(s: str) -> bool:
    s = s.replace('.', '', 1)
    if '.' in s:
        return False
    
    return s.isdecimal()