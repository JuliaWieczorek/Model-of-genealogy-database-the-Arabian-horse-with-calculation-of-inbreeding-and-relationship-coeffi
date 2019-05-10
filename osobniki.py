from tkinter import *
from tkinter import ttk
import sqlite3

class Product:

    db_name = "baza.db"

    def __init__(self, root):
        self.root = root
        self.root.title('OSOBNIKI')

        frame = LabelFrame(self.root, text = "Dodaj nowy rekord")
        frame.grid(row = 0, column = 1)

        Label(frame, text = "Nazwa: ").grid(row = 1, column = 1)
        self.name = Entry(frame)
        self.name.grid(row = 1, column = 2)

        Label(frame, text = "Płeć: ").grid(row = 2, column = 1)
        self.gender = Entry(frame)
        self.gender.grid(row = 2, column = 2)

        Label(frame, text="Gatunek: ").grid(row=3, column=1)
        self.species = Entry(frame)
        self.species.grid(row=3, column=2)

        Label(frame, text="Imię hodowcy: ").grid(row=4, column=1)
        self.fbreeder = Entry(frame)
        self.fbreeder.grid(row=4, column=2)

        Label(frame, text="Nazwisko hodowcy: ").grid(row=5, column=1)
        self.lbreeder = Entry(frame)
        self.lbreeder.grid(row=5, column=2)

        ttk.Button(frame, text = 'Dodaj', command = self.adding).grid(row = 6, column = 2)
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 6, column = 0)

        self.tree = ttk.Treeview(height = 10, columns =('Name','Gender','Species', 'Breeder'))
        self.tree.grid(row = 7, column = 0, columnspan = 3)
        self.tree.heading('#0', text = 'Nazwa', anchor = W)
        self.tree.heading('#1', text = 'Płeć', anchor = W)
        self.tree.heading('#2', text = 'Gatunek', anchor = W)
        self.tree.heading('#3', text = 'Imię hodowcy', anchor = W)
        self.tree.heading('#4', text = 'Nazwisko hodowcy', anchor=W)



        ttk.Button(text = 'Usuń', command = self.deleting).grid(row = 8, column = 0)
        ttk.Button(text = 'Edytuj', command = self.editing).grid(row = 8, column = 1)

        self.viewing_record()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def viewing_record(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = """SELECT nazwa, plec, gatunek, imie, nazwisko FROM osobniki
         JOIN gatunki AS g ON osobniki.id_gat = g.id_gat
         JOIN hodowcy AS h ON osobniki.id_hod = h.id_hod
         
         ORDER BY id_os DESC"""
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = row[0], values = (row[1], row[2], row[3], row[4]))

    def lenrecord(self):
        query = 'SELECT * FROM osobniki ORDER BY id_os DESC'
        db_rows = self.run_query(query)
        lista = []
        for row in db_rows:
            lista.append(row)
        return len(lista)

    def validation(self):
        return len(self.name.get()) != 0 and len(self.gender.get()) != 0 and len(self.species.get()) != 0 and len(self.fbreeder.get()) != 0 and len(self.lbreeder.get()) != 0

    def adding(self):
        if self.validation():
            lista = []
            id1 = 0
            gatunek = self.species.get()
            query1 = 'SELECT id_gat FROM gatunki WHERE  gatunek = ?'  # znalezienie id gatunku
            db_rows = self.run_query(query1, (gatunek,))
            for row1 in db_rows:
                id1 = row1[0]
                lista.append(id1)

            if id1 in lista:
                imie = self.fbreeder.get()
                nazwisko = self.lbreeder.get()
                query2 = 'SELECT id_hod FROM hodowcy WHERE  imie = ? AND nazwisko = ?'  # znalezienie id gatunku
                parameters = (imie, nazwisko)
                lista1 = []
                id2 = 0
                db_rows = self.run_query(query2, parameters)
                for row2 in db_rows:
                    id2 = row2[0]
                    lista1.append(id2)

                if id2 in lista1:
                    l = self.lenrecord()
                    query = 'INSERT INTO osobniki VALUES (?, ?, ?, ?, ?)'
                    parameters = (l+1, self.name.get(), self.gender.get(), id1, id2)
                    self.run_query(query, parameters)
                    self.message['text'] = 'Rekord {} został dodany'.format(self.name.get())
                    self.name.delete(0, END)
                    self.gender.delete(0, END)
                    self.species.delete(0, END)
                    self.fbreeder.delete(0, END)
                    self.lbreeder.delete(0, END)
                else:
                    self.message['text'] = 'Brak hodowcy w systemie'
            else:
                self.message['text'] = 'Brak gatunku w systemie'
        else:
            self.message['text'] = 'Uzupełnij pola!'
        self.viewing_record()

    def deleting(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Proszę, wybierz rekord!'
            return

        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']

        query1 = 'SELECT id_os FROM osobniki WHERE  nazwa = ?'  # znalezienie id hodowcy
        db_rows = self.run_query(query1, (name,))
        for row in db_rows:
            id = row
            id1 = row[0]

        query2 = 'DELETE FROM OSOBNIKI_HODOWCY WHERE id_os = ?'  # usunięcie hodowcy z relacji osobniki_hodowcy
        self.run_query(query2, id)

        query3 = 'DELETE FROM relacje WHERE id_os1 = ? OR id_os2 = ?'  # usunięcie hodowcy z relacji osobniki_hodowcy
        parameters = (id1, id1)
        self.run_query(query3, parameters)

        query = 'DELETE FROM osobniki WHERE nazwa = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Rekord {} został usunięty.'.format(name)
        self.viewing_record()

    def editing(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Proszę, wybierz rekord!'
            return
        old_name = self.tree.item(self.tree.selection())['text']
        old_gender = self.tree.item(self.tree.selection())['values'][0]
        old_species = self.tree.item(self.tree.selection())['values'][1]
        old_fbreeder = self.tree.item(self.tree.selection())['values'][2]
        old_lbreeder = self.tree.item(self.tree.selection())['values'][3]


        self.edit_root = Toplevel()
        self.edit_root.title('Editing')

        Label(self.edit_root, text = 'Stara nazwa:').grid(row = 0, column =1)
        Entry(self.edit_root, textvariable = StringVar(self.edit_root, value = old_name), state = 'readonly').grid(row = 0, column = 2)
        Label(self.edit_root, text = 'Nowa nazwa:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_root)
        new_name.grid(row = 1, column = 2)

        Label(self.edit_root, text='Stara płeć:').grid(row=2, column=1)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=old_gender), state='readonly').grid(row=2, column=2)
        Label(self.edit_root, text='Nowa płeć:').grid(row=3, column=1)
        new_gender = Entry(self.edit_root)
        new_gender.grid(row=3, column=2)

        Label(self.edit_root, text='Stary gatunek:').grid(row=4, column=1)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=old_species), state='readonly').grid(row=4,
                                                                                                               column=2)
        Label(self.edit_root, text='Nowy gatunek:').grid(row=5, column=1)
        new_species = Entry(self.edit_root)
        new_species.grid(row=5, column=2)

        Label(self.edit_root, text='Stare imię hodowcy:').grid(row=6, column=1)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=old_fbreeder), state='readonly').grid(row=6,
                                                                                                               column=2)
        Label(self.edit_root, text='Nowe imię hodowcy:').grid(row=7, column=1)
        new_fbreeder = Entry(self.edit_root)
        new_fbreeder.grid(row=7, column=2)

        Label(self.edit_root, text='Stare nazwisko hodowcy:').grid(row=8, column=1)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=old_lbreeder), state='readonly').grid(row=8,
                                                                                                                column=2)
        Label(self.edit_root, text='Nowe nazwisko hodowcy:').grid(row=9, column=1)
        new_lbreeder = Entry(self.edit_root)
        new_lbreeder.grid(row=9, column=2)

        Button(self.edit_root, text = 'Zapisz zmiany',
               command = lambda: self.edit_records(new_name.get(), old_name,
                                                   new_gender.get(), old_gender,
                                                   new_species.get(), old_species,
                                                   new_fbreeder.get(), old_fbreeder,
                                                   new_lbreeder.get(), old_lbreeder)).grid(row=10, column=2, sticky=W)
        self.edit_root.mainloop()

    def edit_records(self, new_name, old_name, new_gender, old_gender, new_species, old_species, new_fbreeder, old_fbreeder, new_lbreeder, old_lbreeder):

        query1 = 'SELECT id_gat FROM gatunki WHERE  gatunek = ?'
        db_rows = self.run_query(query1, (old_species,))
        for row in db_rows:
            old_id_species = row[0]

        query1 = 'SELECT id_gat FROM gatunki WHERE  gatunek = ?'
        db_rows = self.run_query(query1, (new_species,))
        for row in db_rows:
            new_id_species = row[0]

        query1 = 'SELECT id_hod FROM hodowcy WHERE  imie = ? AND nazwisko = ?'
        parameters = (old_fbreeder, old_lbreeder)
        db_rows = self.run_query(query1, parameters)
        for row in db_rows:
            old_id_breeder = row[0]

        query1 = 'SELECT id_hod FROM hodowcy WHERE  imie = ? AND nazwisko = ?'
        parameters = (new_fbreeder, new_lbreeder)
        db_rows = self.run_query(query1, parameters)
        for row in db_rows:
            new_id_breeder = row[0]

        query = 'UPDATE osobniki SET nazwa = ?, plec = ?, id_gat = ?, id_hod =? WHERE nazwa = ? AND plec = ? AND id_gat = ? AND id_hod = ?'
        parameters = (new_name, new_gender, new_id_species, new_id_breeder, old_name, old_gender, old_id_species, old_id_breeder)
        self.run_query(query, parameters)
        self.edit_root.destroy()
        self.message['text'] = 'Rekord {} został zmieniony.'.format(old_name)
        self.viewing_record()

if __name__ == '__main__':
    root = Tk()
    application = Product(root)
    root.mainloop()