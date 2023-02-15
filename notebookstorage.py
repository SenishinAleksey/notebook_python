import json
import os
from datetime import datetime

from note import Note


class NotebookStorage:
    __storage = []
    __storage_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'notebook.json')

    def __init__(self):
        if os.path.exists(self.__storage_file_path):
            with open(self.__storage_file_path, 'r') as f:
                pass
                storage_dict = json.load(f)
                for note_dict in storage_dict:
                    create = datetime.strptime(note_dict['create'], Note.date_format)
                    change = datetime.strptime(note_dict['change'], Note.date_format)
                    note = Note(note_dict['id'], note_dict['title'], note_dict['strings'], create, change)
                    NotebookStorage.__storage.append(note)

    def __del__(self):
        self.save_storage()

    @classmethod
    def save_storage(cls) -> None:
        storage_dict = []
        for note in cls.__storage:
            storage_dict.append(note.to_dict())
        with open(cls.__storage_file_path, 'w') as f:
            json.dump(storage_dict, f)

    def add_note(self, note: Note) -> None:
        self.__storage.append(note)
        self.save_storage()

    def get_notes_for_page(self, page) -> dict:
        pages_count = len(self.__storage) // 10
        if len(self.__storage) % 10 != 0:
            pages_count += 1
        return {
            'page': page,
            'pages_count': pages_count,
            'notes': self.__storage[10 * (page - 1):10 * page]
        }

    def get_new_id(self) -> int:
        if len(self.__storage) == 0:
            return 1
        ids = []
        for note in self.__storage:
            ids.append(note.id)
        return max(ids) + 1

    def get_note(self, note_id) -> Note:
        for note in self.__storage:
            if note.id == note_id:
                return note
        raise Warning('Заметка не найдена')

    def del_note(self, note: Note):
        self.__storage.remove(note)
        self.save_storage()

    def get_notes_for_date(self, filter_date: datetime, page):
        filtered_notes = []
        for note in self.__storage:
            if note.create.date() == filter_date.date():
                filtered_notes.append(note)
        pages_count = len(filtered_notes) // 10
        if len(filtered_notes) % 10 != 0:
            pages_count += 1
        return {
            'page': page,
            'pages_count': pages_count,
            'notes': filtered_notes[10 * (page - 1):10 * page],
            'filter_date': filter_date.date().strftime('%Y-%m-%d')
        }
