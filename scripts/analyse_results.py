import requests
import re
import dataclasses
from typing import Optional
from datetime import datetime

DATETIME_FROM = datetime(2023, 1, 1)


def api_url(*, from_date: datetime):
    utc_ms = int(from_date.timestamp() * 1000)
    return f"https://lichess.org/api/games/user/Bot5551?tags=true&clocks=false&evals=false&opening=false&since={utc_ms}"


MATCHER_LOOKUP = {
    "black_player": r'\[Black "([^"]+)"]',
    "white_player": r'\[White "([^"]+)"]',
    "white_title": r'\[WhiteTitle "([^"]+)"]',
    "black_title": r'\[BlackTitle "([^"]+)"]',
    "site": r'\[Site "([^"]+)"]',
    "result": r'\[Result "([^"]+)"]',
    "date": r'\[UTCDate "([^"]+)"]',
    "time": r'\[UTCTime "([^"]+)"]',
}


def get_value_from_matcher(pattern: str, string: str) -> Optional[str]:
    match = re.search(pattern, string)
    if match:
        return match.group(1)
    else:
        return None


def datetime_from_strings(date: str, time: str):
    # Combine the date and time strings
    datetime_str = f"{date} {time}"

    # Define the format of the input strings
    datetime_format = "%Y.%m.%d %H:%M:%S"

    # Convert to a datetime object
    return datetime.strptime(datetime_str, datetime_format)


@dataclasses.dataclass
class Game:
    black_player: str
    white_player: str
    black_title: Optional[str]
    white_title: Optional[str]
    site: Optional[str]
    result: str
    timestamp: Optional[datetime]

    @staticmethod
    def from_text(game_text: str) -> Optional['Game']:
        date = get_value_from_matcher(MATCHER_LOOKUP["date"], game_text)
        time = get_value_from_matcher(MATCHER_LOOKUP["time"], game_text)
        timestamp = datetime_from_strings(date, time) if date and time else None

        return Game(
            black_player=get_value_from_matcher(MATCHER_LOOKUP["black_player"], game_text),
            white_player=get_value_from_matcher(MATCHER_LOOKUP["white_player"], game_text),
            white_title=get_value_from_matcher(MATCHER_LOOKUP["white_title"], game_text),
            black_title=get_value_from_matcher(MATCHER_LOOKUP["black_title"], game_text),
            site=get_value_from_matcher(MATCHER_LOOKUP["site"], game_text),
            result=get_value_from_matcher(MATCHER_LOOKUP["result"], game_text),
            timestamp=timestamp,
        )

    @staticmethod
    def is_valid(game_text):
        black_player = get_value_from_matcher(MATCHER_LOOKUP["black_player"], game_text)
        white_player = get_value_from_matcher(MATCHER_LOOKUP["white_player"], game_text)

        # Use existence of black and white players as a proxy for a well-formatted game
        return black_player is not None and white_player is not None

    def opponent_title(self, *, player_name: str) -> str:
        if self.white_player == player_name:
            return self.black_title
        if self.black_player == player_name:
            return self.white_title
        raise GameError("Player name not found in game", self)


class GameError(Exception):
    def __init__(self, message: str, game: Game):
        self.message = message
        self.game = game


@dataclasses.dataclass
class GameList:
    games: list[Game]
    player_name: str

    @staticmethod
    def from_pgn_text(pgn_text: str, player_name: str) -> 'GameList':
        games = [Game.from_text(g) for g in pgn_text.split('\n\n\n') if Game.is_valid(g)]
        return GameList(games, player_name)

    def __iter__(self):
        return iter(self.games)

    def get_games_against_humans(self) -> 'GameList':
        return GameList(
            [g for g in self.games if g.opponent_title(player_name=self.player_name) != "BOT"],
            self.player_name
        )


def main():
    res = requests.get(api_url(from_date=DATETIME_FROM))
    text = res.content.decode("utf-8")
    game_list = GameList.from_pgn_text(text, "Bot5551")
    human_games = game_list.get_games_against_humans()
    return human_games


if __name__ == "__main__":
    main()
