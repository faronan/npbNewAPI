from dataclasses import dataclass


@dataclass(frozen=True)
class Team:
    value: str


@dataclass(frozen=True)
class Date:
    value: str


@dataclass
class Record:
    person: str
    texts: list

    def to_dict(self):
        texts_to_dict = {str(key): val for key, val in zip(
            list(range(len(self.texts))), self.texts)}
        dest = {
            u'person': self.person,
            u'texts': texts_to_dict,
        }
        return dest


@ dataclass
class Content:
    is_no_game: bool
    record: Record

    def to_dict(self):
        dest = {
            u'is_no_game': self.is_no_game,
            u'record': self.record.to_dict(),
        }
        return dest


@ dataclass
class Result:
    team: Team
    date: Date
    content: Content

    def to_dict(self):
        dest = {
            u'team': self.team,
            u'date': self.date,
            u'content': self.content.to_dict(),
        }
        return dest
