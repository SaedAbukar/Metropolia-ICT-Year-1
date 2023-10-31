class Publication:
    def __init__(self, name):
        self.name = name


class Book(Publication):
    def __init__(self, name, writer, pages):
        super().__init__(name)
        self.writer = writer
        self.pages = pages

    def print_info(self):
        print(f'The name of the book: {self.name}, The Writer: {self.writer}, Pages: {self.pages}.')


class Magazine(Publication):
    def __init__(self, name, chief_editor):
        super().__init__(name)
        self.chief_editor = chief_editor

    def print_info(self):
        print(f'The name of the magazine: {self.name}, The chief editor: {self.chief_editor}')


magazine = Magazine('Aku Ankka', 'Aki Hyyppä')
book = Book('Hytti n:o 6', 'Rosa Liksom', 200)

magazine.print_info()
book.print_info()
