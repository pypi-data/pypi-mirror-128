"""
Simple Beatmap Parser
Simple meaning giving more raw data
"""

class Beatmap:
    ...

"""
from typing import Any

def str_to_valid_value(s: str) -> Any:
    if s.lstrip('-').isdecimal():
        return int(s)

    if s.lstrip('-').replace('.', '', 1).isdecimal():
        return float(s)
        
    return s

class Beatmap(dict):
    def parse(self, content: bytes) -> None:
        current_section: str = ''

        for line in content.decode().splitlines():
            if (
                'file format' in line or
                line.strip().startswith('//') or
                line == ''
            ):
                continue

            elif (
                line.startswith('[') and 
                line.endswith(']')
            ):
                decoded_line = line.lower()
                current_section = decoded_line[1:][:-1]

                if current_section in ('hitobjects', 'events', 'timingpoints'):
                    placeholder = []
                else:
                    placeholder = {}

                self[current_section] = placeholder
                continue

            elif (
                ':' in line and
                ',' not in line
            ):
                key, value = line.strip().split(':', 1)
                self[current_section][key.strip().lower()] = str_to_valid_value(value.strip())
                continue

            self[current_section].append(line)

    @classmethod
    def from_content(cls, content: bytes) -> 'Beatmap':
        bmap = cls()
        bmap.parse(content)
        return bmap

    @classmethod
    def from_file(cls, path: str) -> 'Beatmap':
        bmap = cls()
        with open(path, 'rb') as f:
            bmap.parse(f.read())
        
        return bmap
"""