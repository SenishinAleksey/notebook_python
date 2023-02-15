from notebookstorage import NotebookStorage
from views import Views
from note import Note
from datetime import datetime


class Notebook:

    def __init__(self):
        self.storage = NotebookStorage()
        self.notes_list()

    def notes_list(self, page=1) -> None:
        try:
            notes = self.storage.get_notes_for_page(page)
            user_answer = Views.show_notes(notes)
            if user_answer == 1:
                self.add_note()
            elif user_answer == 2:
                note_id = Views.notes_id_request()
                self.show_note(note_id, page)
            elif user_answer == 3:
                filter_date = Views.filter_date_request()
                self.filter(filter_date)
            elif user_answer == 4:
                self.notes_list(page + 1)
            elif user_answer == 5:
                self.notes_list(page - 1)
            elif user_answer == 0:
                exit()
        except Warning as mes:
            Views.show_error(mes)
            self.notes_list(page)

    def add_note(self):
        title, strings, = Views.add_note()
        note_id = self.storage.get_new_id()
        note = Note(note_id, title, strings, datetime.now(), datetime.now())
        self.storage.add_note(note)
        Views.show_success('Заметка добавлена')
        self.notes_list()


    def show_note(self, note_id, page):
        note_id = int(note_id)
        try:
            note = self.storage.get_note(note_id)
            user_answer = Views.show_note(note)
            if user_answer == 1:
                self.edit_note(note, page)
            elif user_answer == 2:
                self.del_note(note, page)
            else:
                self.notes_list(page)
        except Warning as mes:
            Views.show_error(mes)
            self.notes_list(page)

    def edit_note(self, note: Note, page):
        print('Введите новые значения или оставьте пустым, если не требуется изменять:')
        title = input(f'Заголовок [{note.title}]: ')
        if len(title):
            note.title = title
        i = 0
        new_strings = []
        for string in note.strings:
            new_string = input(f'Строка {i + 1} [{string}]: ')
            if len(new_string):
                new_strings.append(new_string)
            else:
                new_strings.append(string)
            i += 1
        note.strings = new_strings
        note.change = datetime.now()
        self.storage.save_storage()
        Views.show_success('Успешно изменено')
        self.show_note(note.id, page)

    def del_note(self, note: Note, page) -> None:
        self.storage.del_note(note)
        Views.show_success('Заметка удалена')
        self.notes_list(page)

    def filter(self, filter_date: datetime, page=1):
        try:
            notes = self.storage.get_notes_for_date(filter_date, page)
            user_answer = Views.show_filtered_notes(notes)
            if user_answer == 1:
                self.add_note()
            elif user_answer == 2:
                note_id = Views.notes_id_request()
                self.show_note(note_id, page)
            elif user_answer == 4:
                self.filter(filter_date, page + 1)
            elif user_answer == 5:
                self.filter(filter_date, page - 1)
            elif user_answer == 0:
                self.notes_list()
        except Warning as mes:
            Views.show_error(mes)
            self.notes_list()
