from datetime import datetime


class Note:
    date_format = '%Y-%m-%d %H.%M.%S'

    def __init__(self, note_id: int, title: str, strings: list, create: datetime, change: datetime):
        self.id = note_id
        self.title = title
        self.strings = strings
        self.create = create
        self.change = change

    def get_create_str(self) -> str:
        return self.create.strftime(self.date_format)

    def get_change_str(self) -> str:
        return self.change.strftime(self.date_format)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "strings": self.strings,
            "create": self.get_create_str(),
            "change": self.get_change_str()
        }
