from datetime import datetime

from note import Note


class Views:

    @staticmethod
    def __show_menu(menu, in_line=False) -> int:
        if menu['title']:
            print(f"\033[1m{menu['title']}\033[0m")
        for num, option in menu['options'].items():
            if in_line and num != 0:
                print(f'{num} - \033[3m{option}\033[0m', end=' ')
            else:
                print(f'{num} - \033[3m{option}\033[0m')
        answer = input('Введите номер пункта меню: ')
        if answer.isdigit():
            answer = int(answer)
            if answer in menu['options']:
                return answer
        Views.show_error('такого пункта не существует')
        return Views.__show_menu(menu, in_line)

    @staticmethod
    def show_error(mes) -> None:
        print(f'\033[31mОшибка: {mes}\033[0m')

    @staticmethod
    def show_success(mes) -> None:
        print(f'\033[32mУспешно: {mes}\033[0m')

    @staticmethod
    def show_notes(notes) -> int:
        print(f"\033[1mЗаметки\033[0m")
        Views.show_notes_list(notes['notes'])
        menu = {
            'title': '',
            'options':
                {
                    1: 'Добавить'
                }
        }
        if notes['notes']:
            menu['options'][2] = 'Просмотр заметки'
            menu['options'][3] = 'Фильтр по дате'
        if notes['page'] < notes['pages_count']:
            menu['options'][4] = 'След. стр.'
        if notes['page'] > 1:
            menu['options'][5] = 'Пред. стр.'
        menu['options'][0] = 'Выход'
        return Views.__show_menu(menu, in_line=True)

    @staticmethod
    def show_notes_list(notes) -> None:
        print('-' * 40)
        if not notes:
            print('Список пуст')
        for note in notes:
            print(f'{note.id}: {note.title}  {note.get_create_str()}')
        print('-' * 40)

    @staticmethod
    def add_note() -> tuple:
        title = input('Заголовок: ')
        strings = []
        while True:
            string = input('Введите строку: ')
            strings.append(string)
            menu = {
                'title': '',
                'options':
                    {
                        1: 'Добавить еще строку',
                        0: 'Закончить'
                    }
            }
            answer = Views.__show_menu(menu, True)
            if answer == 0:
                break
        return title, strings

    @staticmethod
    def notes_id_request() -> int:
        answer = input('Введите ИД заметки: ')
        if answer.isdigit():
            return int(answer)
        Views.show_error('ожидается число')
        return Views.notes_id_request()

    @staticmethod
    def show_note(note: Note):
        print(f"\033[1m{note.title}\033[0m")
        print('-' * 40)
        print(f'ИД: {note.id}')
        print(f'Создана: {note.get_create_str()}')
        print(f'Изменена: {note.get_create_str()}')
        for string in note.strings:
            print(string)
        print('-' * 40)
        menu = {
            'title': '',
            'options':
                {
                    1: 'Изменить',
                    2: 'Удалить',
                    0: 'Вернуться в список'
                }
        }
        return Views.__show_menu(menu, in_line=True)

    @staticmethod
    def filter_date_request() -> datetime:
        date = input('Введите дату в формате ГГГГ-ММ-ДД: ')
        try:
            return datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            Views.show_error('Не верный формат даты')
            return Views.filter_date_request()

    @staticmethod
    def show_filtered_notes(notes):
        print(f"\033[1mЗаметки за {notes['filter_date']}\033[0m")
        Views.show_notes_list(notes['notes'])
        menu = {
            'title': '',
            'options':
                {
                    1: 'Добавить'
                }
        }
        if notes['notes']:
            menu['options'][2] = 'Просмотр заметки'
        if notes['page'] < notes['pages_count']:
            menu['options'][4] = 'След. стр.'
        if notes['page'] > 1:
            menu['options'][5] = 'Пред. стр.'
        menu['options'][0] = 'Сбросить фильтр'
        return Views.__show_menu(menu, in_line=True)
