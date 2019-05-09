from tkinter import *
from tkinter import ttk
import sqlite3

class Product:

    db_name = "baza.db"

    def __init__(self, wind):
        self.wind = wind
        self.wind.title('OSOBNIKI')

        frame = LabelFrame(self.wind, text = "Add new record")
        frame.grid(row = 0, column = 1)

        Label(frame, text = "Name: ").grid(row = 1, column = 1)
        self.name = Entry(frame)
        self.name.grid(row = 1, column = 2)

        Label(frame, text = "Gender: ").grid(row = 2, column = 1)
        self.gender = Entry(frame)
        self.gender.grid(row = 2, column = 2)

        Label(frame, text="Species: ").grid(row=3, column=1)
        self.species = Entry(frame)
        self.species.grid(row=3, column=2)

        Label(frame, text="Breeder: ").grid(row=4, column=1)
        self.breeder = Entry(frame)
        self.breeder.grid(row=4, column=2)

        ttk.Button(frame, text = 'Add record', command = self.adding).grid(row = 5, column = 2)
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 5, column = 0)

        self.tree = ttk.Treeview(height = 10, columns =('Name','Gender','Species'))
        self.tree.grid(row = 6, column = 0, columnspan = 3)
        self.tree.heading('#0', text = 'Name', anchor = W)
        self.tree.heading('#1', text = 'Gender', anchor = W)
        self.tree.heading('#2', text = 'Species', anchor = W)
        self.tree.heading('#3', text = 'Breeder', anchor = W)



        ttk.Button(text = 'Delete record', command = self.deleting).grid(row = 7, column = 0)
        ttk.Button(text = 'Edit record', command = self.editing).grid(row = 7, column = 1)

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
        query = 'SELECT * FROM osobniki ORDER BY id_os DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = (row[2], row[3], row[4]))

    def lenrecord(self):
        query = 'SELECT * FROM osobniki ORDER BY id_os DESC'
        db_rows = self.run_query(query)
        lista = []
        for row in db_rows:
            lista.append(row)
        return len(lista)

    def validation(self):
        return len(self.name.get()) != 0 and len(self.gender.get()) != 0 and len(self.species.get()) != 0 and len(self.breeder.get()) != 0

    def adding(self):
        if self.validation():
            l = self.lenrecord()
            query = 'INSERT INTO osobniki VALUES (?, ?, ?, ?, ?)'
            parameters = (l+1, self.name.get(), self.gender.get(), self.species.get(), self.breeder.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Record {} added'.format(self.name.get())
            self.name.delete(0, END)
            self.gender.delete(0, END)
            self.species.delete(0, END)
            self.breeder.delete(0, END)

        else:
            self.message['text'] = 'name filed or gender field is empty'
        self.viewing_record()

    def deleting(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select record!'
            return

        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM osobniki WHERE nazwa = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted.'.format(name)
        self.viewing_record()

    def editing(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select record!'
            return
        old_name = self.tree.item(self.tree.selection())['text']
        old_gender = self.tree.item(self.tree.selection())['values'][0]
        old_species = self.tree.item(self.tree.selection())['values'][1]
        old_breeder = self.tree.item(self.tree.selection())['values'][2]


        self.edit_wind = Toplevel()
        self.edit_wind.title('Editing')

        Label(self.edit_wind, text = 'Old name:').grid(row = 0, column =1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_name), state = 'readonly').grid(row = 0, column = 2)
        Label(self.edit_wind, text = 'New name:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        Label(self.edit_wind, text='Old gender:').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_gender), state='readonly').grid(row=2, column=2)
        Label(self.edit_wind, text='New gender:').grid(row=3, column=1)
        new_gender = Entry(self.edit_wind)
        new_gender.grid(row=3, column=2)

        Label(self.edit_wind, text='Old species:').grid(row=4, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_species), state='readonly').grid(row=4,
                                                                                                               column=2)
        Label(self.edit_wind, text='New species:').grid(row=5, column=1)
        new_species = Entry(self.edit_wind)
        new_species.grid(row=5, column=2)

        Label(self.edit_wind, text='Old breeder:').grid(row=6, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_breeder), state='readonly').grid(row=6,
                                                                                                               column=2)
        Label(self.edit_wind, text='New breeder:').grid(row=7, column=1)
        new_breeder = Entry(self.edit_wind)
        new_breeder.grid(row=7, column=2)

        Button(self.edit_wind, text = 'Save changes',
               command = lambda: self.edit_records(new_name.get(), old_name,
                                                   new_gender.get(), old_gender,
                                                   new_species.get(), old_species,
                                                   new_breeder.get(), old_breeder)).grid(row=8, column=2, sticky=W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, old_name, new_gender, old_gender, new_species, old_species, new_breeder, old_breeder):
        query = 'UPDATE osobniki SET nazwa = ?, plec = ?, id_gat = ?, id_hod =? WHERE nazwa = ? AND plec = ? AND id_gat = ? AND id_hod = ?'
        parameters = (new_name, new_gender, new_species, new_breeder, old_name, old_gender, old_species, old_breeder)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} changed.'.format(old_name)
        self.viewing_record()

if __name__ == '__main__':
    wind = Tk()
    application = Product(wind)
    wind.mainloop()