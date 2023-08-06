#!/usr/bin/env python3
import pathlib
from dataclasses import dataclass


class RepoOrganizer:
    pass


@dataclass
class Repo:
    url: str
    path: str or pathlib.Path
    project: str or None
    group: str or None

    def clone(self):
        pass

    def register(self):
        pass
