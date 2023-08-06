from dataclasses import dataclass
from typing import Optional


@dataclass
class File:
    filepath: str
    _identifier: Optional[str] = None

    @property
    def identifier(self) -> str:
        if self._identifier is None:
            return self.filepath
        return self._identifier


@dataclass
class ManuscriptFile:
    key: str
    filepath: str
