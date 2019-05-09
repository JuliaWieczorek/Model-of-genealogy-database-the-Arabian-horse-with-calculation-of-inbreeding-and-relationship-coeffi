from tkinter import *
from tkinter import ttk
import sqlite3

class Product:

    db_name = "baza.db"

    def __init__(self, wind):
        self.wind = wind
        #self.wind.title('GATUNKI')

        frame = LabelFrame(self.wind, text = "Add new record")
        frame.grid(row = 0, column = 0)

        Label(frame, text = "Name: ").grid(row = 1, column = 1)
        self.name = Entry(frame)
        self.name.grid(row = 1, column = 2)

        ttk.Button(frame, text = 'Add record', command = self.adding).grid(row = 3, column = 2)
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2)

        self.tree = ttk.Treeview(height = 10, columns ='')
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Name', anchor = W)

        ttk.Button(text = 'Delete record', command = self.deleting).grid(row = 5, column = 0)
        ttk.Button(text = 'Edit record', command = self.editing).grid(row = 5, column = 1)

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
        query = 'SELECT gatunek FROM gatunki ORDER BY id_gat DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = row[0])

    def lenrecord(self):
        query = 'SELECT * FROM gatunki ORDER BY id_gat DESC'
        db_rows = self.run_query(query)
        lista = []
        for row in db_rows:
            lista.append(row)
        return len(lista)

    def validation(self):
        return len(self.name.get()) != 0

    def adding(self):
        if self.validation():
            l = self.lenrecord()
            query = 'INSERT INTO gatunki VALUES (?, ?)'
            parameters = (l+1, self.name.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Record {} added'.format(self.name.get())
            self.name.delete(0, END)
        else:
            self.message['text'] = 'name filed or gender field is empty'
        self.viewing_record()

    def deleting(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select record!'
            return

        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM gatunki WHERE gatunek = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted.'.format(name)
        self.viewing_record()

    def editing(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'Please, select record!'
            return
        old_name = self.tree.item(self.tree.selection())['text']

        self.edit_wind = Toplevel()
        self.edit_wind.title('Editing')

        Label(self.edit_wind, text = 'Old name:').grid(row = 0, column =1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_name), state = 'readonly').grid(row = 0, column = 2)
        Label(self.edit_wind, text = 'New name:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        Button(self.edit_wind, text = 'Save changes',
               command = lambda: self.edit_records(new_name.get(), old_name)).grid(row=4, column=2, sticky=W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name):
        query = 'UPDATE gatunki SET gatunek = ? WHERE gatunek = ?'
        parameters = (new_name, name)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} changed.'.format(name)
        self.viewing_record()

if __name__ == '__main__':
    wind = Tk()
    application = Product(wind)
    wind.mainloop()