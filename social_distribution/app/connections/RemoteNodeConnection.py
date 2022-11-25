from .teams import *
import os


class RemoteNodeConnection():
    teams = {
        "https://c404-team8.herokuapp.com/api/": {"num": 8, "conn": Team8Connection},
        "https://social-distribution-14degrees2.herokuapp.com/api/": {"num": 15, "conn": Team15Connection}
    }

    def __init__(self, url: str):
        base_url = url.split("authors")[0]
        username = os.environ.get(
            "TEAM_" + str(self.teams[base_url]["num"]) + "_USERNAME")
        password = os.environ.get(
            "TEAM_" + str(self.teams[base_url]["num"]) + "_PASSWORD")
        self.conn = self.teams[base_url]["conn"](username, password, base_url)
