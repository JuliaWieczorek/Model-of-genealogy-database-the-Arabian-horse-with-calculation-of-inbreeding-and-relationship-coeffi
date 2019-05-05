# -*- coding: cp1250 -*-
import tkinter as tk
# import baza
import baza_danych
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import Listbox
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
# from tkinter import Scrollbar
class FRONTEND(object):
    Hodowcy = ['Cezary Bober', 'Julia Wieczorek', 'Mateusz Markowski', 'Alicja Dera']
    Osobniki = ['KARO', 'FARO', 'DONIO', 'DEMO', 'HAPPY', 'SETO']
    Gatunki = ['Psy', 'Koty']
    # DEFINICJE
    ######################################################################################################################
    def __init__(self):
        # okno root
        self.root = Tk()  # root widget - musi zostać stworzony przed innymi widgetami
        self.root.geometry("1400x500+0+0")
        self.root.title("Pracownia Informatyczna")  # tytuł naszej tabeli root
        self.root_label = tk.Label(self.root)
        self.root_label.grid()

        # Menu
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu)
        # Plik
        self.menu.add_cascade(label="Plik", menu=self.filemenu)
        self.filemenu.add_command(label="Otwórz", command=self.baseopen)
        self.filemenu.add_command(label="Edycja struktury")
        self.filemenu.add_command(label="Zamknij baze", command=self.baseclose)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Zamknij program", command=self.root.destroy)

        # Edycja
        self.edycja = Menu(self.menu)
        self.gatunek = Menu(self.menu)
        self.osobnik = Menu(self.menu)
        self.hodowca = Menu(self.menu)
        self.menu.add_cascade(label="Edycja", menu=self.edycja)

        self.edycja.add_cascade(label="Gatunek", menu=self.gatunek)
        self.gatunek.add_command(label="Dodaj nowy gatunek",command=dodajGatunek)
        self.gatunek.add_command(label="Usuń istniejący gatunek",command=usunGatuenk)
        self.gatunek.add_command(label="Edytuj istniejący gatunek",command=edytujGatunek)

        self.edycja.add_cascade(label="Osobnik", menu=self.osobnik)
        self.osobnik.add_command(label="Dodaj nowego osobnika",command=dodajOsobnika)
        self.osobnik.add_command(label="Usuń istniejącego osobnika",command=usunOsobnika)
        self.osobnik.add_command(label="Edytuj istniejącego osobnika",command=edytujOsonika)

        self.edycja.add_cascade(label="Hodowca", menu=self.hodowca)
        self.hodowca.add_command(label="Dodaj nowego hodowce", command=dodajHodowce)
        self.hodowca.add_command(label="Usuń istniejącego hodowce", command=usunHodowce)
        self.hodowca.add_command(label="Edytuj istniejącego hodowce", command=edytujHodowce)

        # Obliczenia
        self.oblicz = Menu(self.menu)
        self.menu.add_cascade(label="Współczynniki", menu=self.oblicz)
        self.oblicz.add_command(label="Średni współczynnik pokrewieństwa", command=avgpokrewienstwo)
        self.oblicz.add_command(label="Współczynnik inbredu", command=imbred)
        self.oblicz.add_command(label="Współczynnik pokrewieństa", command=pokrewienstwo)
        self.oblicz.add_command(label="Współczynnik utraty przodków", command=utrata)

        # Wyświetlanie drzewa
        self.tree = Menu(self.menu)
        self.menu.add_cascade(label="Drzewo", menu=self.tree)
        self.tree.add_command(label="Wyśwetl drzewo rodowodowe osobnika", command=Wtree)

        self.root.mainloop()  # zamknięcie pętli
    # ---------------------------------------------------------------------------------------------------------------------
    # Otwieranie bazy danych i zamykanie
    def baseopen(self):  # To chyba działa
        self.db = filedialog.askopenfilename(initialdir="D:\Studia\Magisterka\Semestr_1\Projekty_1\IBD",
                                             title="Wybierz baze danych",
                                             filetypes=(("Bazy danych", "*.db"), ("all files", "*.*")))
        # cursor = db.cursor()
        print("widzisz to to działa")

    def baseclose(self, db):  # to nie działa jeszcze
        self.db.close()
        print("widzisz to to działa")
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Gatunek
class dodajGatunek(object):
    # Wygląd okna
    def __init__(self):
        self.dodaj = Tk()
        self.dodaj.geometry("700x400+0+0")
        self.dodaj.title("Dodaj Nowy Gatunek")
        self.dodaj_label = tk.Label(self.dodaj)
        self.dodaj_label.grid()

        self.F1 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F1.grid(column=0, row=1)
        self.F2 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F2.grid(column=1, row=1)
        self.F3 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F3.grid(column=0, row=2)
        self.F4 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F4.grid(column=1, row=2)
        self.F5 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F5.grid(column=0, row=3, columnspan=2)
        self.F6 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F6.grid(column=0, row=4, columnspan=2)
        self.F7 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F7.grid(column=2, row=1, rowspan=10)
        self.F8 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F8.grid(column=2, row=0)
        self.F10 = Frame(self.dodaj, borderwidth=2, relief='ridge')  # Zamknij
        self.F10.grid(column=0, row=5)

        self.L1 = Label(self.F1, text="Nazwa Gatunku")
        self.L1.grid()
        self.E1 = Entry(self.F2, bd=5)
        self.E1.grid()

        self.wynik = scrolledtext.ScrolledText(self.F6, width=40, height=10)
        self.wynik.grid()
        #self.lista = scrolledtext.ScrolledText(self.F7, width=40, height=16)
        #self.lista.grid()

        self.listatree = ttk.Treeview(self.F7, height=16, columns=('Indeks', 'Gatunek'))
        self.listatree.grid()
        self.listatree.heading('#0', text="Index")
        self.listatree.heading('#1', text="Gatunek")

        ##zmienione przez Juleczke! wczesniej bylo pod def zamknij()
        # Tworzenie przyciskow
        self.btn1 = Button(self.F5, text="Dodaj nowy gatunek", command=self.kliknij)
        self.btn2 = Button(self.F8, text="Wyświetl liste gatunków", command=self.show)
        self.btn4 = Button(self.F10, text="Zamknij", command=self.dodaj.destroy)

        # Ulozenie przyciskow
        self.btn1.grid()
        self.btn2.grid()
        self.btn4.grid()


    ###
    def czytajgatunki(self):
        """ Funkcja pobiera i wyświetla dane z gatunki"""
        self.conn = sqlite3.connect('baza.db')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT id_gat, gatunek FROM GATUNKI")
        self.gatunek = self.cur.fetchall()
        self.lista = []
        for self.gat in self.gatunek:
            gatu = (self.gat['id_gat'], self.gat['gatunek'])
            self.lista.append(gatu)
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        return self.lista
    ###

    # Definicje przycisków
    def kliknij(self):
        self.dod = self.E1.get()
        FRONTEND.Gatunki.append(self.dod)
        self.res = "Dodano gatunek: " + self.E1.get() + "\n"
        self.wynik.insert(INSERT, self.res)
        return

    #def show(self):
     #   self.j = 0
      #  if self.j < len(FRONTEND.Gatunki):
       #     for self.imie in FRONTEND.Gatunki:
        #        self.res = self.imie + "\n"
         #       self.lista.option_clear()  # działa ale nie tak jak ma
          #      self.lista.insert(INSERT, self.res)
        #self.j = +1
        #return
    ###
    def show(self):
        self.j = 0
        if self.j < len(self.czytajgatunki()):
            for self.lista in self.czytajgatunki():
                self.listatree.insert('', 0, text=self.lista[0], values=(self.lista[1]))
        self.j = +1
        return
    ###
    def zamknij(self):  # zmodyfikować i dodać do przycisku
        self.msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if self.msg == 'yes':
            self.dodaj.destroy
        else:
            return
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# edycja Gatunku
class edytujGatunek(object):
    def __init__(self):
        # Wygląd okna
        self.edycja = Tk()
        self.edycja.geometry("800x350+0+0")
        self.edycja.title("Edycja Gatunku")
        self.edycja_label = tk.Label(self.edycja)
        self.edycja_label.grid()

        self.F1 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Nazwa Gatunku
        self.F1.grid(column=0, row=0)
        self.F2 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Entry imie
        self.F2.grid(column=4, row=2)
        self.F3 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Listbox
        self.F3.grid(column=0, row=2)
        self.F4 = Frame(self.edycja, borderwidth=2, relief='ridge')  # wybierz
        self.F4.grid(column=2, row=2)
        self.F5 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Zapisz
        self.F5.grid(column=7, row=2)
        self.F6 = Frame(self.edycja, borderwidth=2)  # 2 strzałka
        self.F6.grid(column=3, row=2)
        self.F7 = Frame(self.edycja, borderwidth=2)  # 1 strzałka
        self.F7.grid(column=1, row=2)
        self.F8 = Frame(self.edycja, borderwidth=2)  # 3 strzałka
        self.F8.grid(column=6, row=2)
        self.F9 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Entry nazwisko
        self.F9.grid(column=5, row=2)
        self.F10 = Frame(self.edycja, borderwidth=2)  # Nazwa Imie
        self.F10.grid(column=4, row=1)
        self.F11 = Frame(self.edycja, borderwidth=2)  # Nazwa Nazwisko
        self.F11.grid(column=5, row=1)
        self.F12 = Frame(self.edycja, borderwidth=2)  # Odśwież
        self.F12.grid(column=0, row=1)
        self.F13 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Zamknij
        self.F13.grid(column=0, row=3)

        self.L1 = Label(self.F1, text="Gatunki")
        self.L1.grid()
        self.E1 = Entry(self.F2, bd=5)
        self.E1.grid()
        self.E2 = Entry(self.F9, bd=5)
        self.E2.grid()
        self.L2 = Label(self.F6, text="--->")
        self.L2.grid()
        self.L3 = Label(self.F7, text="--->")
        self.L3.grid()
        self.L4 = Label(self.F8, text="--->")
        self.L4.grid()
        self.L5 = Label(self.F10, text="Nazwa")
        self.L5.grid()
        # self.L5 = Label(self.F11, text="Nazwisko")
        # self.L5.grid()

        self.lista = Listbox(self.F3, width=40, height=16, selectmode=SINGLE)
        for self.imie in FRONTEND.Gatunki:
            self.lista.insert(END, self.imie)
        self.lista.grid()

        # znowu zmienione przez Juleczke- ta czesc byla pod def zamknij()
        # Tworzenie przyciskow
        self.btn1 = Button(self.F4, text="Wybierz", command=self.wybierz)
        self.btn2 = Button(self.F5, text="Zapisz zmiane")
        self.btn3 = Button(self.F12, text="Odśwież")
        self.btn4 = Button(self.F13, text="Zamknij", command=self.edycja.destroy)

        # Ulozenie przyciskow
        self.btn1.grid()
        self.btn2.grid()
        self.btn3.grid()
        self.btn4.grid()

        # Definicje przycisków
    def wybierz(self):
        self.lista1 = int(self.lista.curselection()[0])  # wyświetlanie argumentów z listboxa
        self.dane = FRONTEND.Gatunki[self.lista1]
        self.E1.insert(INSERT, self.dane[0])
        # self.E2.insert(INSERT, self.dane[1])

    def zamknij(self):  # zmodyfikować i dodać do przycisku
        self.msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if self.msg == 'yes':
            self.edycja.destroy
        else:
            return
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Usuwanie gatunku
class usunGatuenk(object):
    def __init__(self):
        # Wygląd okna
        self.usun = Tk()
        self.usun.geometry("700x400+0+0")
        self.usun.title("Usuwanie Gatunku")
        self.usun_label = tk.Label(self.usun)
        self.usun_label.grid()

        self.F1 = Frame(self.usun, borderwidth=2, relief='ridge')  # Nazwa Hodowcy
        self.F1.grid(column=0, row=0)
        self.F9 = Frame(self.usun, borderwidth=2, relief="ridge")  # odśwież
        self.F9.grid(column=0, row=1)
        self.F2 = Frame(self.usun, borderwidth=2, relief='ridge')  # Entry imie
        self.F2.grid(column=4, row=2)
        self.F3 = Frame(self.usun, borderwidth=2, relief='ridge')  # Listbox
        self.F3.grid(column=0, row=2)
        self.F4 = Frame(self.usun, borderwidth=2, relief='ridge')  # wybierz
        self.F4.grid(column=2, row=2)
        self.F5 = Frame(self.usun, borderwidth=2, relief='ridge')  # Zapisz
        self.F5.grid(column=7, row=2)
        self.F6 = Frame(self.usun, borderwidth=2)  # 2 strzałka
        self.F6.grid(column=3, row=2)
        self.F7 = Frame(self.usun, borderwidth=2)  # 1 strzałka
        self.F7.grid(column=1, row=2)
        self.F8 = Frame(self.usun, borderwidth=2)  # 3 strzałka
        self.F8.grid(column=6, row=2)
        self.F10 = Frame(self.usun, borderwidth=2, relief='ridge')  # Zamknij
        self.F10.grid(column=0, row=3)

        self.L1 = Label(self.F1, text="Lista Gatunków")
        self.L1.grid()
        self.E1 = Entry(self.F2, bd=5)
        self.E1.grid()
        self.L2 = Label(self.F6, text="--->")
        self.L2.grid()
        self.L3 = Label(self.F7, text="--->")
        self.L3.grid()
        self.L4 = Label(self.F8, text="--->")
        self.L4.grid()

        self.lista = Listbox(self.F3, width=40, height=16, selectmode=SINGLE)
        for self.imie in FRONTEND.Gatunki:
            self.lista.insert(END, self.imie)
        self.lista.grid()

        # zmienione przez Juleczke
        # Tworzenie przyciskow
        self.btn1 = Button(self.F4, text="Wybierz")
        self.btn2 = Button(self.F5, text="Usuń Gatunek", command=self.usuwanie)
        self.btn3 = Button(self.F9, text="Odśwież")
        self.btn4 = Button(self.F10, text="Zamknij", command=self.usun.destroy)

        # Ulozenie przyciskow
        self.btn1.grid()
        self.btn2.grid()
        self.btn3.grid()
        self.btn4.grid()

    # Definicje przycisków
    def wybierz(self):
        self.lista1 = int(self.lista.curselection()[0])  # wyświetlanie argumentów z listboxa
        self.dane = FRONTEND.Gatunki[self.lista1]

    def usuwanie(self):
        self.msg = messagebox.askquestion("Usuwanie", "Czy jesteś pewny, że chcesz usunąć tego hodowce?",
                                          icon="warning")
        if self.msg == 'yes':
            print("To usunie hodowce")
        else:
            print("To wróci do wyboru hodowcy")
            return

    def zamknij(self):  # zmodyfikować i dodać do przycisku
        self.msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if self.msg == 'yes':
            self.usun.destroy()
        else:
            return
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# ---------------------------------------------------------------------------------------------------------------------
# Dodawanie Osobnika
class dodajOsobnika(object):
    # Wygląd okna
    def __init__(self):
        self.dodaj = Tk()
        self.dodaj.geometry("700x400+0+0")
        self.dodaj.title("Dodaj Nowego Osobnika")
        self.dodaj_label = tk.Label(self.dodaj)
        self.dodaj_label.grid()

        self.F1 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F1.grid(column=0, row=1)
        self.F2 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F2.grid(column=1, row=1)
        self.F3 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F3.grid(column=0, row=2)
        self.F4 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F4.grid(column=1, row=2)
        self.F5 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F5.grid(column=0, row=3, columnspan=2)
        self.F6 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F6.grid(column=0, row=4, columnspan=2)
        self.F7 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F7.grid(column=2, row=1, rowspan=10)
        self.F8 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F8.grid(column=2, row=0)
        self.F10 = Frame(self.dodaj, borderwidth=2, relief='ridge')  # Zamknij
        self.F10.grid(column=0, row=5)

        self.L1 = Label(self.F1, text="Nazwa Osobnika")
        self.L1.grid()
        self.E1 = Entry(self.F2, bd=5)
        self.E1.grid()

        # self.L2 = Label(self.F3, text="Nazwisko Hodowcy")
        # self.L2.grid()
        # self.E2 = Entry(self.F4, bd=5)
        # self.E2.grid()

        self.wynik = scrolledtext.ScrolledText(self.F6, width=40, height=10)
        self.wynik.grid()
        self.listatree = ttk.Treeview (self.F7, height=16, columns=('Indeks','Nazwa','plec'))
        self.listatree.grid()
        self.listatree.heading('#0', text="Index")
        self.listatree.heading('#1', text="Nazwa")
        self.listatree.heading('#2', text="Płeć")

        ##zmienione przez Juleczke! wczesniej bylo pod def zamknij()

        # Tworzenie przyciskow
        self.btn1 = Button(self.F5, text="Dodaj nowego Osobnika", command=self.kliknij)
        self.btn2 = Button(self.F8, text="Wyświetl liste osobników", command=self.show)
        self.btn4 = Button(self.F10, text="Zamknij", command=self.dodaj.destroy)

        # Ulozenie przyciskow
        self.btn1.grid()
        self.btn2.grid()
        self.btn4.grid()

    ###
    def czytajdane(self):
        """Funkcja pobiera i wyświetla dane z bazy."""
        self.conn = sqlite3.connect('baza.db')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.lista = []
        self.cur.execute(" SELECT id_os, nazwa, plec FROM OSOBNIKI ")
        self.osobnicy = self.cur.fetchall()
        for self.osobnik in self.osobnicy:
            self.dane = (self.osobnik['id_os'], self.osobnik['nazwa'], self.osobnik['plec'])
            self.lista.append(self.dane)
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        return self.lista

    ###
    # Definicje przycisków
    def kliknij(self):
        self.dod = self.E1.get()
        FRONTEND.Osobniki.append(self.dod)
        self.res = "Dodano Osobnika: " + self.E1.get() + "\n"
        self.wynik.insert(INSERT, self.res)
        return

    def show(self):
        self.j = 0
        if self.j < len(self.czytajdane()):
            for self.lista in self.czytajdane():
                self.listatree.insert('', 0, text=self.lista[0], values=(self.lista[1], self.lista[2]))
        self.j = +1
        return

    def zamknij(self):  # zmodyfikować i dodać do przycisku
        self.msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if self.msg == 'yes':
            self.dodaj.destroy
        else:
            return


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Edycja Osobnika
class edytujOsonika(object):
    def __init__(self):
        # Wygląd okna
        self.edycja = Tk()
        self.edycja.geometry("800x350+0+0")
        self.edycja.title("Edycja Osobnika")
        self.edycja_label = tk.Label(self.edycja)
        self.edycja_label.grid()

        self.F1 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Nazwa Hodowcy
        self.F1.grid(column=0, row=0)
        self.F2 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Entry imie
        self.F2.grid(column=4, row=2)
        self.F3 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Listbox
        self.F3.grid(column=0, row=2)
        self.F4 = Frame(self.edycja, borderwidth=2, relief='ridge')  # wybierz
        self.F4.grid(column=2, row=2)
        self.F5 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Zapisz
        self.F5.grid(column=7, row=2)
        self.F6 = Frame(self.edycja, borderwidth=2)  # 2 strzałka
        self.F6.grid(column=3, row=2)
        self.F7 = Frame(self.edycja, borderwidth=2)  # 1 strzałka
        self.F7.grid(column=1, row=2)
        self.F8 = Frame(self.edycja, borderwidth=2)  # 3 strzałka
        self.F8.grid(column=6, row=2)
        self.F9 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Entry nazwisko
        self.F9.grid(column=5, row=2)
        self.F10 = Frame(self.edycja, borderwidth=2)  # Nazwa Imie
        self.F10.grid(column=4, row=1)
        self.F11 = Frame(self.edycja, borderwidth=2)  # Nazwa Nazwisko
        self.F11.grid(column=5, row=1)
        self.F12 = Frame(self.edycja, borderwidth=2)  # Odśwież
        self.F12.grid(column=0, row=1)
        self.F13 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Zamknij
        self.F13.grid(column=0, row=3)

        self.L1 = Label(self.F1, text="Osobniki")
        self.L1.grid()
        self.E1 = Entry(self.F2, bd=5)
        self.E1.grid()
        # self.E2 = Entry(self.F9, bd=5)
        # self.E2.grid()
        self.L2 = Label(self.F6, text="--->")
        self.L2.grid()
        self.L3 = Label(self.F7, text="--->")
        self.L3.grid()
        self.L4 = Label(self.F8, text="--->")
        self.L4.grid()
        self.L5 = Label(self.F10, text="Nazwa")
        self.L5.grid()
        # self.L5 = Label(self.F11, text="Nazwisko")
        # self.L5.grid()

        self.lista = Listbox(self.F3, width=40, height=16, selectmode=SINGLE)
        for self.imie in FRONTEND.Osobniki:
            self.lista.insert(END, self.imie)
        self.lista.grid()

        # znowu zmienione przez Juleczke- ta czesc byla pod def zamknij()
        # Tworzenie przyciskow
        self.btn1 = Button(self.F4, text="Wybierz", command=self.wybierz)
        self.btn2 = Button(self.F5, text="Zapisz zmiane")
        self.btn3 = Button(self.F12, text="Odśwież")
        self.btn4 = Button(self.F13, text="Zamknij", command=self.edycja.destroy)

        # Ulozenie przyciskow
        self.btn1.grid()
        self.btn2.grid()
        self.btn3.grid()
        self.btn4.grid()

        # Definicje przycisków

    def wybierz(self):
        self.lista1 = int(self.lista.curselection()[0])  # wyświetlanie argumentów z listboxa
        self.dane = FRONTEND.Osobniki[self.lista1].split()
        self.E1.insert(INSERT, self.dane[0])
        # self.E2.insert(INSERT, self.dane[1])

    def zamknij(self):  # zmodyfikować i dodać do przycisku
        self.msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if self.msg == 'yes':
            self.edycja.destroy
        else:
            return
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Usuwanie Osobnika
class usunOsobnika(object):
    def __init__(self):
        # Wygląd okna
        self.usun = Tk()
        self.usun.geometry("700x400+0+0")
        self.usun.title("Usuwanie Osobnika")
        self.usun_label = tk.Label(self.usun)
        self.usun_label.grid()

        self.F1 = Frame(self.usun, borderwidth=2, relief='ridge')  # Nazwa Hodowcy
        self.F1.grid(column=0, row=0)
        self.F9 = Frame(self.usun, borderwidth=2, relief="ridge")  # odśwież
        self.F9.grid(column=0, row=1)
        self.F2 = Frame(self.usun, borderwidth=2, relief='ridge')  # Entry imie
        self.F2.grid(column=4, row=2)
        self.F3 = Frame(self.usun, borderwidth=2, relief='ridge')  # Listbox
        self.F3.grid(column=0, row=2)
        self.F4 = Frame(self.usun, borderwidth=2, relief='ridge')  # wybierz
        self.F4.grid(column=2, row=2)
        self.F5 = Frame(self.usun, borderwidth=2, relief='ridge')  # Zapisz
        self.F5.grid(column=7, row=2)
        self.F6 = Frame(self.usun, borderwidth=2)  # 2 strzałka
        self.F6.grid(column=3, row=2)
        self.F7 = Frame(self.usun, borderwidth=2)  # 1 strzałka
        self.F7.grid(column=1, row=2)
        self.F8 = Frame(self.usun, borderwidth=2)  # 3 strzałka
        self.F8.grid(column=6, row=2)
        self.F10 = Frame(self.usun, borderwidth=2, relief='ridge')  # Zamknij
        self.F10.grid(column=0, row=3)

        self.L1 = Label(self.F1, text="Lista Osobników")
        self.L1.grid()
        self.E1 = Entry(self.F2, bd=5)
        self.E1.grid()
        self.L2 = Label(self.F6, text="--->")
        self.L2.grid()
        self.L3 = Label(self.F7, text="--->")
        self.L3.grid()
        self.L4 = Label(self.F8, text="--->")
        self.L4.grid()

        self.lista = Listbox(self.F3, width=40, height=16, selectmode=SINGLE)
        for self.imie in FRONTEND.Osobniki:
            self.lista.insert(END, self.imie)
        self.lista.grid()

        # zmienione przez Juleczke

        # Tworzenie przyciskow
        self.btn1 = Button(self.F4, text="Wybierz")
        self.btn2 = Button(self.F5, text="Usuń Osobnika", command=self.usuwanie)
        self.btn3 = Button(self.F9, text="Odśwież")
        self.btn4 = Button(self.F10, text="Zamknij", command=self.usun.destroy)

        # Ulozenie przyciskow
        self.btn1.grid()
        self.btn2.grid()
        self.btn3.grid()
        self.btn4.grid()

    # Definicje przycisków
    def wybierz(self):
        self.lista1 = int(self.lista.curselection()[0])  # wyświetlanie argumentów z listboxa
        self.dane = FRONTEND.Osobniki[self.lista1].split()

    def usuwanie(self):
        self.msg = messagebox.askquestion("Usuwanie", "Czy jesteś pewny, że chcesz usunąć tego hodowce?",
                                          icon="warning")
        if self.msg == 'yes':
            print("To usunie hodowce")
        else:
            print("To wróci do wyboru hodowcy")
            return

    def zamknij(self):  # zmodyfikować i dodać do przycisku
        self.msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if self.msg == 'yes':
            self.usun.destroy()
        else:
            return
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Dodaj Nowego Hodowce
    # To do:
    ''' połącz go z funkcjami spraw żeby listy się czyściły przed kolejnym wyświetleniem'''


class dodajHodowce(object):
    # Wygląd okna
    def __init__(self):
        self.dodaj = Tk()
        self.dodaj.geometry("700x400+0+0")
        self.dodaj.title("Dodaj Nowego Hodowce")
        self.dodaj_label = tk.Label(self.dodaj)
        self.dodaj_label.grid()

        self.F1 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F1.grid(column=0, row=1)
        self.F2 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F2.grid(column=1, row=1)
        self.F3 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F3.grid(column=0, row=2)
        self.F4 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F4.grid(column=1, row=2)
        self.F5 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F5.grid(column=0, row=3, columnspan=2)
        self.F6 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F6.grid(column=0, row=4, columnspan=2)
        self.F7 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F7.grid(column=2, row=1, rowspan=10)
        self.F8 = Frame(self.dodaj, borderwidth=2, relief='ridge')
        self.F8.grid(column=2, row=0)
        self.F10 = Frame(self.dodaj, borderwidth=2, relief='ridge')  # Zamknij
        self.F10.grid(column=0, row=5)

        self.L1 = Label(self.F1, text="Imię Hodowcy")
        self.L1.grid()
        self.E1 = Entry(self.F2, bd=5)
        self.E1.grid()

        self.L2 = Label(self.F3, text="Nazwisko Hodowcy")
        self.L2.grid()
        self.E2 = Entry(self.F4, bd=5)
        self.E2.grid()

        self.wynik = scrolledtext.ScrolledText(self.F6, width=40, height=10)
        self.wynik.grid()
        #self.lista = scrolledtext.ScrolledText(self.F7, width=40, height=16)
        #self.lista.grid()

        self.listatree = ttk.Treeview(self.F7, height=16, columns=('Indeks', 'Imie', 'Nazwisko'))
        self.listatree.grid()
        self.listatree.heading('#0', text="Index")
        self.listatree.heading('#1', text="Imie")
        self.listatree.heading('#2', text="Nazwisko")

        ##zmienione przez Juleczke! wczesniej bylo pod def zamknij()

        # Tworzenie przyciskow
        self.btn1 = Button(self.F5, text="Dodaj nowego Hodowce", command=self.kliknij)
        self.btn2 = Button(self.F8, text="Wyświetl spis hodowców", command=self.show)
        self.btn4 = Button(self.F10, text="Zamknij", command=self.dodaj.destroy)

        # Ulozenie przyciskow
        self.btn1.grid()
        self.btn2.grid()
        self.btn4.grid()

    # Definicje przycisków
    def kliknij(self):
        self.dod = self.E1.get() + " " + self.E2.get()
        FRONTEND.Hodowcy.append(self.dod)
        self.res = "Dodano hodowce: " + self.E1.get() + " " + self.E2.get() + "\n"
        self.wynik.insert(INSERT, self.res)
        return

    def show(self):
        self.j = 0
        if self.j < len(self.czytajhodowcow()):
            for self.lista in self.czytajhodowcow():
                self.listatree.insert('', 0, text=self.lista[0], values=(self.lista[1], self.lista[2]))
        self.j = +1
        return

    def czytajhodowcow(self):
        """Funckja wczytująca wszystkich hodowców z bazy"""
        self.conn = sqlite3.connect('baza.db')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.cur.execute(" SELECT id_hod, imie, nazwisko FROM HODOWCY")
        self.hodowca = self.cur.fetchall()
        self.lista = []
        for self.hod in self.hodowca:
            hodor = (self.hod['id_hod'], self.hod['imie'], self.hod['nazwisko'])
            self.lista.append(hodor)
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        return self.lista

    def zamknij(self):  # zmodyfikować i dodać do przycisku
        self.msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if self.msg == 'yes':
            self.dodaj.destroy
        else:
            return

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Edycja Hodowcy
    # To do:
    ''' Pozmieniaj nazwy i dostosuj wygląd okna i połącz go z funkcjami'''
class edytujHodowce(object):
    def __init__(self):
        # Wygląd okna
        self.edycja = Tk()
        self.edycja.geometry("800x350+0+0")
        self.edycja.title("Edycja Hodowcy")
        self.edycja_label = tk.Label(self.edycja)
        self.edycja_label.grid()

        self.F1 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Nazwa Hodowcy
        self.F1.grid(column=0, row=0)
        self.F2 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Entry imie
        self.F2.grid(column=4, row=2)
        self.F3 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Listbox
        self.F3.grid(column=0, row=2)
        self.F4 = Frame(self.edycja, borderwidth=2, relief='ridge')  # wybierz
        self.F4.grid(column=2, row=2)
        self.F5 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Zapisz
        self.F5.grid(column=7, row=2)
        self.F6 = Frame(self.edycja, borderwidth=2)  # 2 strzałka
        self.F6.grid(column=3, row=2)
        self.F7 = Frame(self.edycja, borderwidth=2)  # 1 strzałka
        self.F7.grid(column=1, row=2)
        self.F8 = Frame(self.edycja, borderwidth=2)  # 3 strzałka
        self.F8.grid(column=6, row=2)
        self.F9 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Entry nazwisko
        self.F9.grid(column=5, row=2)
        self.F10 = Frame(self.edycja, borderwidth=2)  # Nazwa Imie
        self.F10.grid(column=4, row=1)
        self.F11 = Frame(self.edycja, borderwidth=2)  # Nazwa Nazwisko
        self.F11.grid(column=5, row=1)
        self.F12 = Frame(self.edycja, borderwidth=2)  # Odśwież
        self.F12.grid(column=0, row=1)
        self.F13 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Zamknij
        self.F13.grid(column=0, row=3)

        self.L1 = Label(self.F1, text="HODOWCY")
        self.L1.grid()
        self.E1 = Entry(self.F2, bd=5)
        self.E1.grid()
        self.E2 = Entry(self.F9, bd=5)
        self.E2.grid()
        self.L2 = Label(self.F6, text="--->")
        self.L2.grid()
        self.L3 = Label(self.F7, text="--->")
        self.L3.grid()
        self.L4 = Label(self.F8, text="--->")
        self.L4.grid()
        self.L5 = Label(self.F10, text="Imie")
        self.L5.grid()
        self.L5 = Label(self.F11, text="Nazwisko")
        self.L5.grid()

        self.lista = Listbox(self.F3, width=40, height=16, selectmode=SINGLE)
        for self.imie in FRONTEND.Hodowcy:
            self.lista.insert(END, self.imie)
        self.lista.grid()

        # znowu zmienione przez Juleczke- ta czesc byla pod def zamknij()
        # Tworzenie przyciskow
        self.btn1 = Button(self.F4, text="Wybierz", command=self.wybierz)
        self.btn2 = Button(self.F5, text="Zapisz zmiane")
        self.btn3 = Button(self.F12, text="Odśwież")
        self.btn4 = Button(self.F13, text="Zamknij", command=self.edycja.destroy)

        # Ulozenie przyciskow
        self.btn1.grid()
        self.btn2.grid()
        self.btn3.grid()
        self.btn4.grid()

        # Definicje przycisków

    def wybierz(self):
        self.lista1 = int(self.lista.curselection()[0])  # wyświetlanie argumentów z listboxa
        self.dane = FRONTEND.Hodowcy[self.lista1].split()
        self.E1.insert(INSERT, self.dane[0])
        self.E2.insert(INSERT, self.dane[1])

    def zamknij(self):  # zmodyfikować i dodać do przycisku
        self.msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if self.msg == 'yes':
            self.edycja.destroy
        else:
            return
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Usuwanie Hodowcy
class usunHodowce(object):
    def __init__(self):
        # Wygląd okna
        self.usun = Tk()
        self.usun.geometry("700x400+0+0")
        self.usun.title("Usuwanie Hodowcy")
        self.usun_label = tk.Label(self.usun)
        self.usun_label.grid()

        self.F1 = Frame(self.usun, borderwidth=2, relief='ridge')  # Nazwa Hodowcy
        self.F1.grid(column=0, row=0)
        self.F9 = Frame(self.usun, borderwidth=2, relief="ridge")  # odśwież
        self.F9.grid(column=0, row=1)
        self.F2 = Frame(self.usun, borderwidth=2, relief='ridge')  # Entry imie
        self.F2.grid(column=4, row=2)
        self.F3 = Frame(self.usun, borderwidth=2, relief='ridge')  # Listbox
        self.F3.grid(column=0, row=2)
        self.F4 = Frame(self.usun, borderwidth=2, relief='ridge')  # wybierz
        self.F4.grid(column=2, row=2)
        self.F5 = Frame(self.usun, borderwidth=2, relief='ridge')  # Zapisz
        self.F5.grid(column=7, row=2)
        self.F6 = Frame(self.usun, borderwidth=2)  # 2 strzałka
        self.F6.grid(column=3, row=2)
        self.F7 = Frame(self.usun, borderwidth=2)  # 1 strzałka
        self.F7.grid(column=1, row=2)
        self.F8 = Frame(self.usun, borderwidth=2)  # 3 strzałka
        self.F8.grid(column=6, row=2)
        self.F10 = Frame(self.usun, borderwidth=2, relief='ridge')  # Zamknij
        self.F10.grid(column=0, row=3)

        self.L1 = Label(self.F1, text="Lista Hodowców")
        self.L1.grid()
        self.E1 = Entry(self.F2, bd=5)
        self.E1.grid()
        self.L2 = Label(self.F6, text="--->")
        self.L2.grid()
        self.L3 = Label(self.F7, text="--->")
        self.L3.grid()
        self.L4 = Label(self.F8, text="--->")
        self.L4.grid()

        self.lista = Listbox(self.F3, width=40, height=16, selectmode=SINGLE)
        for self.imie in FRONTEND.Hodowcy:
            self.lista.insert(END, self.imie)
        self.lista.grid()

        # zmienione przez Juleczke

        # Tworzenie przyciskow
        self.btn1 = Button(self.F4, text="Wybierz")
        self.btn2 = Button(self.F5, text="Usuń Hodowce", command=self.usuwanie)
        self.btn3 = Button(self.F9, text="Odśwież")
        self.btn4 = Button(self.F10, text="Zamknij", command=self.usun.destroy)

        # Ulozenie przyciskow
        self.btn1.grid()
        self.btn2.grid()
        self.btn3.grid()
        self.btn4.grid()

    # Definicje przycisków
    def wybierz(self):
        self.lista1 = int(self.lista.curselection()[0])  # wyświetlanie argumentów z listboxa
        self.dane = FRONTEND.Hodowcy[self.lista1].split()

    def usuwanie(self):
        self.msg = messagebox.askquestion("Usuwanie", "Czy jesteś pewny, że chcesz usunąć tego hodowce?",
                                          icon="warning")
        if self.msg == 'yes':
            print("To usunie hodowce")
        else:
            print("To wróci do wyboru hodowcy")
            return

    def zamknij(self):  # zmodyfikować i dodać do przycisku
        self.msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if self.msg == 'yes':
            self.usun.destroy()
        else:
            return
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Wyświetlanie drzewa
class Wtree(object):
    # Widget
    def __init__(self):
        self.tree = Tk()
        self.tree.geometry("700x400+0+0")
        self.tree.title("Drzewo rodowodowe")
        self.tree_label = Label(self.tree)
        self.tree_label.grid()

        self.F1 = Frame(self.tree, borderwidth=2, relief='ridge')
        self.F1.grid(column=0, row=0)
        self.F2 = Frame(self.tree, borderwidth=2, relief='ridge')
        self.F2.grid(column=0, row=1)
        self.F3 = Frame(self.tree, borderwidth=2, relief='ridge')
        self.F3.grid(column=1, row=1)
        self.F4 = Frame(self.tree, borderwidth=2, relief='ridge')
        self.F4.grid(column=2, row=1)

        self.L1 = Label(self.F1, text="Lista nazw osobników")
        self.L1.grid()
        self.L2 = Label(self.F3, text="Wybrano osobnika o nazwie:")
        self.E1 = Entry(self.F4, bd=5)
        self.E1.grid()

        self.show = Listbox(self.F2, width=60, height=40, selectmode=SINGLE)
        self.show.grid(column=1, row=0)

        # Definicje przyciskow

        # Tworzenie przyciskow
        self.btn1 = Button(self.tree, text="Wyszukaj")
        # Ulozenie przyciskow
        self.btn1.grid(column=4, row=0)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Średni współczynnik pokrewieństwa
class avgpokrewienstwo(object):
    def __init__(self):
        # Widget
        self.avg = Tk()
        self.avg.geometry("700x400+0+0")
        self.avg.title("Średni wspólczynnik pokrewieństwa")
        self.avg_label = Label(self.avg)
        self.avg_label.grid()

        self.F1 = Frame(self.avg, borderwidth=2, relief='ridge')
        self.F1.grid(column=0, row=0)
        self.F2 = Frame(self.avg, borderwidth=2, relief='ridge')
        self.F2.grid(column=0, row=1)

        self.L1 = Label(self.F1, text="Lista Osobników")
        self.L1.grid()

        self.lista = Listbox(self.F2, width=40, height=16, selectmode=SINGLE)
        for self.nazwa in FRONTEND.Osobniki:
            self.lista.insert(END, self.nazwa)
        self.lista.grid()
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Współczynnik imbredu
class imbred(object):
    def __init__(self):
        # Widget
        self.wsimb = Tk()
        self.wsimb.geometry("700x400+0+0")
        self.wsimb.title("Współczynnik imbredu")
        self.wsimb_label = Label(self.wsimb)
        self.wsimb_label.grid()
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Współczynnik pokrewieństwa
class pokrewienstwo(object):
    def __init__(self):
        # Widget
        self.wspok = Tk()
        self.wspok.geometry("700x400")
        self.wspok.title("Współczynnik pokrewieństwa")
        self.wspok_label = Label(self.wspok)
        self.wspok_label.grid()
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Współczynnik utraty przodków
class utrata(object):
    def __init__(self):
        # Widget
        self.wsutraty = Tk()
        self.wsutraty.geometry("700x400+0+0")
        self.wsutraty.title("Współczynnik utraty przodków")
        self.wsutraty_label = Label(self.wsutraty)
        self.wsutraty_label.grid()
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #######################################################################################################################


baza = FRONTEND()
