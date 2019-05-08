# -*- coding: cp1250 -*-
import tkinter as tk
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import Listbox
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext

# from tkinter import Scrollbar
Hodowcy = ['Cezary Bober', 'Julia Wieczorek', 'Mateusz Markowski', 'Alicja Dera']
Osobniki = ['KARO', 'FARO', 'DONIO', 'DEMO', 'HAPPY', 'SETO']
Gatunki = ['Psy', 'Koty']
# DEFINICJE
######################################################################################################################


# ---------------------------------------------------------------------------------------------------------------------
# Otwieranie bazy danych i zamykanie
def baseopen():  # To chyba działa
    db = filedialog.askopenfilename(initialdir="D:\Studia\Magisterka\Semestr_1\Projekty_1\IBD",
                                    title="Wybierz baze danych",
                                    filetypes=(("Bazy danych", "*.db"), ("all files", "*.*")))
    # cursor = db.cursor()
    print("widzisz to to działa")


def baseclose(db):  # to nie działa jeszcze
    db.close()
    print("widzisz to to działa")
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Gatunek
# Wygląd okna
def dodajGatunek():

    dodaj = Tk()
    dodaj.geometry("700x400+0+0")
    dodaj.title("Dodaj Nowy Gatunek")
    dodaj_label = tk.Label(dodaj)
    dodaj_label.grid()

    F1 = Frame(dodaj, borderwidth=2, relief='ridge')
    F1.grid(column=0, row=1)
    F2 = Frame(dodaj, borderwidth=2, relief='ridge')
    F2.grid(column=1, row=1)
    F3 = Frame(dodaj, borderwidth=2, relief='ridge')
    F3.grid(column=0, row=2)
    F4 = Frame(dodaj, borderwidth=2, relief='ridge')
    F4.grid(column=1, row=2)
    F5 = Frame(dodaj, borderwidth=2, relief='ridge')
    F5.grid(column=0, row=3, columnspan=2)
    F6 = Frame(dodaj, borderwidth=2, relief='ridge')
    F6.grid(column=0, row=4, columnspan=2)
    F7 = Frame(dodaj, borderwidth=2, relief='ridge')
    F7.grid(column=2, row=1, rowspan=10)
    F8 = Frame(dodaj, borderwidth=2, relief='ridge')
    F8.grid(column=2, row=0)
    F10 = Frame(dodaj, borderwidth=2, relief='ridge')  # Zamknij
    F10.grid(column=0, row=5)

    L1 = Label(F1, text="Nazwa Gatunku")
    L1.grid()
    E1 = Entry(F2, bd=5)
    E1.grid()

    wynik = scrolledtext.ScrolledText(F6, width=40, height=10)
    wynik.grid()
    # self.lista = scrolledtext.ScrolledText(self.F7, width=40, height=16)
    # self.lista.grid()

    listatree = ttk.Treeview(F7, height=16, columns=('Indeks', 'Gatunek'))
    listatree.grid()
    listatree.heading('#0', text="Index")
    listatree.heading('#1', text="Gatunek")

    def czytajgatunki():
        """ Funkcja pobiera i wyświetla dane z gatunki"""
        conn = sqlite3.connect('baza.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id_gat, gatunek FROM GATUNKI")
        gatunek = cur.fetchall()
        lista = []
        for gat in gatunek:
            gatu = (gat['id_gat'], gat['gatunek'])
            lista.append(gatu)
        conn.commit()
        cur.close()
        conn.close()
        return lista

    # Definicje przycisków
    def kliknij():
        dod = E1.get()
        Gatunki.append(dod)
        res = "Dodano gatunek: " + E1.get() + "\n"
        wynik.insert(INSERT, res)
        return

    def show():
        j = 0
        if j < len(czytajgatunki()):
            for lista in czytajgatunki():
                listatree.insert('', 0, text=lista[0], values=(lista[1]))
        j = +1
        return

    def zamknij():  # zmodyfikować i dodać do przycisku
        msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if msg == 'yes':
            dodaj.destroy
        else:
            return

    ##zmienione przez Juleczke! wczesniej bylo pod def zamknij()
    # Tworzenie przyciskow
    btn1 = Button(F5, text="Dodaj nowy gatunek", command=kliknij)
    btn2 = Button(F8, text="Wyświetl liste gatunków", command=show)
    btn4 = Button(F10, text="Zamknij", command=dodaj.destroy)

    # Ulozenie przyciskow
    btn1.grid()
    btn2.grid()
    btn4.grid()

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# edycja Gatunku
# Wygląd okna
def edytujGatunek():
    edycja = Tk()
    edycja.geometry("800x350+0+0")
    edycja.title("Edycja Gatunku")
    edycja_label = tk.Label(edycja)
    edycja_label.grid()

    F1 = Frame(edycja, borderwidth=2, relief='ridge')  # Nazwa Gatunku
    F1.grid(column=0, row=0)
    F2 = Frame(edycja, borderwidth=2, relief='ridge')  # Entry imie
    F2.grid(column=4, row=2)
    F3 = Frame(edycja, borderwidth=2, relief='ridge')  # Listbox
    F3.grid(column=0, row=2)
    F4 = Frame(edycja, borderwidth=2, relief='ridge')  # wybierz
    F4.grid(column=2, row=2)
    F5 = Frame(edycja, borderwidth=2, relief='ridge')  # Zapisz
    F5.grid(column=7, row=2)
    F6 = Frame(edycja, borderwidth=2)  # 2 strzałka
    F6.grid(column=3, row=2)
    F7 = Frame(edycja, borderwidth=2)  # 1 strzałka
    F7.grid(column=1, row=2)
    F8 = Frame(edycja, borderwidth=2)  # 3 strzałka
    F8.grid(column=6, row=2)
    F9 = Frame(edycja, borderwidth=2, relief='ridge')  # Entry nazwisko
    F9.grid(column=5, row=2)
    F10 = Frame(edycja, borderwidth=2)  # Nazwa Imie
    F10.grid(column=4, row=1)
    F11 = Frame(edycja, borderwidth=2)  # Nazwa Nazwisko
    F11.grid(column=5, row=1)
    F12 = Frame(edycja, borderwidth=2)  # Odśwież
    F12.grid(column=0, row=1)
    F13 = Frame(edycja, borderwidth=2, relief='ridge')  # Zamknij
    F13.grid(column=0, row=3)

    L1 = Label(F1, text="Gatunki")
    L1.grid()
    E1 = Entry(F2, bd=5)
    E1.grid()
    E2 = Entry(F9, bd=5)
    E2.grid()
    L2 = Label(F6, text="--->")
    L2.grid()
    L3 = Label(F7, text="--->")
    L3.grid()
    L4 = Label(F8, text="--->")
    L4.grid()
    L5 = Label(F10, text="Nazwa")
    L5.grid()
    # self.L5 = Label(self.F11, text="Nazwisko")
    # self.L5.grid()

    lista = Listbox(F3, width=40, height=16, selectmode=SINGLE)
    for imie in Gatunki:
        lista.insert(END, imie)
    lista.grid()

    # Definicje przycisków
    def wybierz():
        lista1 = int(lista.curselection()[0])  # wyświetlanie argumentów z listboxa
        dane = Gatunki[lista1]
        E1.insert(INSERT, dane[0])
        # self.E2.insert(INSERT, self.dane[1])


    def zamknij():  # zmodyfikować i dodać do przycisku
        msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if msg == 'yes':
            edycja.destroy
        else:
            return

    # znowu zmienione przez Juleczke- ta czesc byla pod def zamknij()
    # Tworzenie przyciskow
    btn1 = Button(F4, text="Wybierz", command=wybierz)
    btn2 = Button(F5, text="Zapisz zmiane")
    btn3 = Button(F12, text="Odśwież")
    btn4 = Button(F13, text="Zamknij", command=edycja.destroy)

    # Ulozenie przyciskow
    btn1.grid()
    btn2.grid()
    btn3.grid()
    btn4.grid()





    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Usuwanie gatunku
    # Wygląd okna
def usunGatunek():
    usun = Tk()
    usun.geometry("700x400+0+0")
    usun.title("Usuwanie Gatunku")
    usun_label = tk.Label(usun)
    usun_label.grid()

    F1 = Frame(usun, borderwidth=2, relief='ridge')  # Nazwa Hodowcy
    F1.grid(column=0, row=0)
    F9 = Frame(usun, borderwidth=2, relief="ridge")  # odśwież
    F9.grid(column=0, row=1)
    F2 = Frame(usun, borderwidth=2, relief='ridge')  # Entry imie
    F2.grid(column=4, row=2)
    F3 = Frame(usun, borderwidth=2, relief='ridge')  # Listbox
    F3.grid(column=0, row=2)
    F4 = Frame(usun, borderwidth=2, relief='ridge')  # wybierz
    F4.grid(column=2, row=2)
    F5 = Frame(usun, borderwidth=2, relief='ridge')  # Zapisz
    F5.grid(column=7, row=2)
    F6 = Frame(usun, borderwidth=2)  # 2 strzałka
    F6.grid(column=3, row=2)
    F7 = Frame(usun, borderwidth=2)  # 1 strzałka
    F7.grid(column=1, row=2)
    F8 = Frame(usun, borderwidth=2)  # 3 strzałka
    F8.grid(column=6, row=2)
    F10 = Frame(usun, borderwidth=2, relief='ridge')  # Zamknij
    F10.grid(column=0, row=3)

    L1 = Label(F1, text="Lista Gatunków")
    L1.grid()
    E1 = Entry(F2, bd=5)
    E1.grid()
    L2 = Label(F6, text="--->")
    L2.grid()
    L3 = Label(F7, text="--->")
    L3.grid()
    L4 = Label(F8, text="--->")
    L4.grid()

    lista = Listbox(F3, width=40, height=16, selectmode=SINGLE)
    for imie in Gatunki:
        lista.insert(END, imie)
    lista.grid()

    # Definicje przycisków
    def wybierz():
        lista1 = int(lista.curselection()[0])  # wyświetlanie argumentów z listboxa
        dane = Gatunki[lista1]


    def usuwanie():
        msg = messagebox.askquestion("Usuwanie", "Czy jesteś pewny, że chcesz usunąć tego hodowce?",
                                     icon="warning")
        if msg == 'yes':
            print("To usunie hodowce")
        else:
            print("To wróci do wyboru hodowcy")
            return


    def zamknij():  # zmodyfikować i dodać do przycisku
        msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if msg == 'yes':
            usun.destroy()
        else:
            return

    # zmienione przez Juleczke
    # Tworzenie przyciskow
    btn1 = Button(F4, text="Wybierz")
    btn2 = Button(F5, text="Usuń Gatunek", command=usuwanie)
    btn3 = Button(F9, text="Odśwież")
    btn4 = Button(F10, text="Zamknij", command=usun.destroy)

    # Ulozenie przyciskow
    btn1.grid()
    btn2.grid()
    btn3.grid()
    btn4.grid()


    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    # ---------------------------------------------------------------------------------------------------------------------
    # Dodawanie Osobnika
    # Wygląd okna
def dodajOsobnika():
    dodaj = Tk()
    dodaj.geometry("700x400+0+0")
    dodaj.title("Dodaj Nowego Osobnika")
    dodaj_label = tk.Label(dodaj)
    dodaj_label.grid()

    F1 = Frame(dodaj, borderwidth=2, relief='ridge')
    F1.grid(column=0, row=1)
    F2 = Frame(dodaj, borderwidth=2, relief='ridge')
    F2.grid(column=1, row=1)
    F11 = Frame(dodaj, borderwidth=2, relief='ridge')
    F11.grid(column=0, row=2)
    F12 = Frame(dodaj, borderwidth=2, relief='ridge')
    F12.grid(column=1, row=2)
    F3 = Frame(dodaj, borderwidth=2, relief='ridge')
    F3.grid(column=0, row=3)
    F4 = Frame(dodaj, borderwidth=2, relief='ridge')
    F4.grid(column=1, row=3)
    F5 = Frame(dodaj, borderwidth=2, relief='ridge')
    F5.grid(column=0, row=4, columnspan=2)
    F6 = Frame(dodaj, borderwidth=2, relief='ridge')
    F6.grid(column=0, row=5, columnspan=2)
    F7 = Frame(dodaj, borderwidth=2, relief='ridge')
    F7.grid(column=2, row=1, rowspan=10)
    F8 = Frame(dodaj, borderwidth=2, relief='ridge')
    F8.grid(column=2, row=0)
    F10 = Frame(dodaj, borderwidth=2, relief='ridge')  # Zamknij
    F10.grid(column=0, row=6)

    L1 = Label(F1, text="Nazwa Osobnika:")
    L1.grid()
    E1 = Entry(F2, bd=5)
    E1.grid()
    L2 = Label(F11 , text="Płeć:")
    L2.grid()
    E2 = Radiobutton(F12, text='Samiec', value=1)
    E2.grid()
    E3 = Radiobutton(F12, text='Samica', value=2)
    E3.grid()

    # self.L2 = Label(self.F3, text="Nazwisko Hodowcy")
    # self.L2.grid()
    # self.E2 = Entry(self.F4, bd=5)
    # self.E2.grid()

    wynik = scrolledtext.ScrolledText(F6, width=40, height=10)
    wynik.grid()
    listatree = ttk.Treeview(F7, height=16, columns=('Indeks', 'Nazwa', 'plec'))
    listatree.grid()
    listatree.heading('#0', text="Index")
    listatree.heading('#1', text="Nazwa")
    listatree.heading('#2', text="Płeć")

    ##zmienione przez Juleczke! wczesniej bylo pod def zamknij()

    ###
    def czytajdane():
        """Funkcja pobiera i wyświetla dane z bazy."""
        conn = sqlite3.connect('baza.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        lista = []
        cur.execute(" SELECT id_os, nazwa, plec FROM OSOBNIKI ")
        osobnicy = cur.fetchall()
        for osobnik in osobnicy:
            dane = (osobnik['id_os'], osobnik['nazwa'], osobnik['plec'])
            lista.append(dane)
        conn.commit()
        cur.close()
        conn.close()
        return lista


    ###
    # Definicje przycisków
    def kliknij():
        dod = E1.get()
        Osobniki.append(dod)
        res = "Dodano Osobnika: " + E1.get() + "\n"
        wynik.insert(INSERT, res)
        return


    def show():
        j = 0
        if j < len(czytajdane()):
            for lista in czytajdane():
                listatree.insert('', 0, text=lista[0], values=(lista[1], lista[2]))
        j = +1
        return


    def zamknij():  # zmodyfikować i dodać do przycisku
        msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if msg == 'yes':
            dodaj.destroy
        else:
            return

    # Tworzenie przyciskow
    btn1 = Button(F5, text="Dodaj nowego Osobnika", command=kliknij)
    btn2 = Button(F8, text="Wyświetl liste osobników", command=show)
    btn4 = Button(F10, text="Zamknij", command=dodaj.destroy)

    # Ulozenie przyciskow
    btn1.grid()
    btn2.grid()
    btn4.grid()


    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Edycja Osobnika
    # Wygląd okna
def edytujOsobnika():
    edycja = Tk()
    edycja.geometry("800x350+0+0")
    edycja.title("Edycja Osobnika")
    edycja_label = tk.Label(edycja)
    edycja_label.grid()

    F1 = Frame(edycja, borderwidth=2, relief='ridge')  # Nazwa Hodowcy
    F1.grid(column=0, row=0)
    F2 = Frame(edycja, borderwidth=2, relief='ridge')  # Entry imie
    F2.grid(column=4, row=2)
    F3 = Frame(edycja, borderwidth=2, relief='ridge')  # Listbox
    F3.grid(column=0, row=2)
    F4 = Frame(edycja, borderwidth=2, relief='ridge')  # wybierz
    F4.grid(column=2, row=2)
    F5 = Frame(edycja, borderwidth=2, relief='ridge')  # Zapisz
    F5.grid(column=7, row=2)
    F6 = Frame(edycja, borderwidth=2)  # 2 strzałka
    F6.grid(column=3, row=2)
    F7 = Frame(edycja, borderwidth=2)  # 1 strzałka
    F7.grid(column=1, row=2)
    F8 = Frame(edycja, borderwidth=2)  # 3 strzałka
    F8.grid(column=6, row=2)
    F9 = Frame(edycja, borderwidth=2, relief='ridge')  # Entry nazwisko
    F9.grid(column=5, row=2)
    F10 = Frame(edycja, borderwidth=2)  # Nazwa Imie
    F10.grid(column=4, row=1)
    F11 = Frame(edycja, borderwidth=2)  # Nazwa Nazwisko
    F11.grid(column=5, row=1)
    F12 = Frame(edycja, borderwidth=2)  # Odśwież
    F12.grid(column=0, row=1)
    F13 = Frame(edycja, borderwidth=2, relief='ridge')  # Zamknij
    F13.grid(column=0, row=3)

    L1 = Label(F1, text="Osobniki")
    L1.grid()
    E1 = Entry(F2, bd=5)
    E1.grid()
    # self.E2 = Entry(self.F9, bd=5)
    # self.E2.grid()
    L2 = Label(F6, text="--->")
    L2.grid()
    L3 = Label(F7, text="--->")
    L3.grid()
    L4 = Label(F8, text="--->")
    L4.grid()
    L5 = Label(F10, text="Nazwa")
    L5.grid()
    # self.L5 = Label(self.F11, text="Nazwisko")
    # self.L5.grid()

    lista = Listbox(F3, width=40, height=16, selectmode=SINGLE)
    for imie in Osobniki:
        lista.insert(END, imie)
    lista.grid()

    # znowu zmienione przez Juleczke- ta czesc byla pod def zamknij()
    # Tworzenie przyciskow
    btn1 = Button(F4, text="Wybierz", command=wybierz)
    btn2 = Button(F5, text="Zapisz zmiane")
    btn3 = Button(F12, text="Odśwież")
    btn4 = Button(F13, text="Zamknij", command=edycja.destroy)

    # Ulozenie przyciskow
    btn1.grid()
    btn2.grid()
    btn3.grid()
    btn4.grid()


    # Definicje przycisków

    def wybierz():
        lista1 = int(lista.curselection()[0])  # wyświetlanie argumentów z listboxa
        dane = Osobniki[lista1].split()
        E1.insert(INSERT, dane[0])
        # self.E2.insert(INSERT, self.dane[1])


    def zamknij():  # zmodyfikować i dodać do przycisku
        msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if msg == 'yes':
            edycja.destroy
        else:
            return


    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Usuwanie Osobnika
    # Wygląd okna
def usunOsobnika():
    usun = Tk()
    usun.geometry("700x400+0+0")
    usun.title("Usuwanie Osobnika")
    usun_label = tk.Label(usun)
    usun_label.grid()

    F1 = Frame(usun, borderwidth=2, relief='ridge')  # Nazwa Hodowcy
    F1.grid(column=0, row=0)
    F9 = Frame(usun, borderwidth=2, relief="ridge")  # odśwież
    F9.grid(column=0, row=1)
    F2 = Frame(usun, borderwidth=2, relief='ridge')  # Entry imie
    F2.grid(column=4, row=2)
    F3 = Frame(usun, borderwidth=2, relief='ridge')  # Listbox
    F3.grid(column=0, row=2)
    F4 = Frame(usun, borderwidth=2, relief='ridge')  # wybierz
    F4.grid(column=2, row=2)
    F5 = Frame(usun, borderwidth=2, relief='ridge')  # Zapisz
    F5.grid(column=7, row=2)
    F6 = Frame(usun, borderwidth=2)  # 2 strzałka
    F6.grid(column=3, row=2)
    F7 = Frame(usun, borderwidth=2)  # 1 strzałka
    F7.grid(column=1, row=2)
    F8 = Frame(usun, borderwidth=2)  # 3 strzałka
    F8.grid(column=6, row=2)
    F10 = Frame(usun, borderwidth=2, relief='ridge')  # Zamknij
    F10.grid(column=0, row=3)

    L1 = Label(F1, text="Lista Osobników")
    L1.grid()
    E1 = Entry(F2, bd=5)
    E1.grid()
    L2 = Label(F6, text="--->")
    L2.grid()
    L3 = Label(F7, text="--->")
    L3.grid()
    L4 = Label(F8, text="--->")
    L4.grid()

    lista = Listbox(F3, width=40, height=16, selectmode=SINGLE)
    for imie in Osobniki:
        lista.insert(END, imie)
    lista.grid()

    # zmienione przez Juleczke

    # Tworzenie przyciskow
    btn1 = Button(F4, text="Wybierz")
    btn2 = Button(F5, text="Usuń Osobnika", command=usuwanie)
    btn3 = Button(F9, text="Odśwież")
    btn4 = Button(F10, text="Zamknij", command=usun.destroy)

    # Ulozenie przyciskow
    btn1.grid()
    btn2.grid()
    btn3.grid()
    btn4.grid()


    # Definicje przycisków
    def wybierz():
        lista1 = int(lista.curselection()[0])  # wyświetlanie argumentów z listboxa
        dane = Osobniki[lista1].split()


    def usuwanie():
        msg = messagebox.askquestion("Usuwanie", "Czy jesteś pewny, że chcesz usunąć tego hodowce?",
                                     icon="warning")
        if msg == 'yes':
            print("To usunie hodowce")
        else:
            print("To wróci do wyboru hodowcy")
            return


    def zamknij():  # zmodyfikować i dodać do przycisku
        msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if msg == 'yes':
            usun.destroy()
        else:
            return
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Dodaj Nowego Hodowce
# To do:
''' połącz go z funkcjami spraw żeby listy się czyściły przed kolejnym wyświetleniem'''

# Wygląd okna
def dodajHodowce():
    dodaj = Tk()
    dodaj.geometry("700x400+0+0")
    dodaj.title("Dodaj Nowego Hodowce")
    dodaj_label = tk.Label(dodaj)
    dodaj_label.grid()

    F1 = Frame(dodaj, borderwidth=2, relief='ridge')
    F1.grid(column=0, row=1)
    F2 = Frame(dodaj, borderwidth=2, relief='ridge')
    F2.grid(column=1, row=1)
    F3 = Frame(dodaj, borderwidth=2, relief='ridge')
    F3.grid(column=0, row=2)
    F4 = Frame(dodaj, borderwidth=2, relief='ridge')
    F4.grid(column=1, row=2)
    F5 = Frame(dodaj, borderwidth=2, relief='ridge')
    F5.grid(column=0, row=3, columnspan=2)
    F6 = Frame(dodaj, borderwidth=2, relief='ridge')
    F6.grid(column=0, row=4, columnspan=2)
    F7 = Frame(dodaj, borderwidth=2, relief='ridge')
    F7.grid(column=2, row=1, rowspan=10)
    F8 = Frame(dodaj, borderwidth=2, relief='ridge')
    F8.grid(column=2, row=0)
    F10 = Frame(dodaj, borderwidth=2, relief='ridge')  # Zamknij
    F10.grid(column=0, row=5)

    L1 = Label(F1, text="Imię Hodowcy")
    L1.grid()
    E1 = Entry(F2, bd=5)
    E1.grid()

    L2 = Label(F3, text="Nazwisko Hodowcy")
    L2.grid()
    E2 = Entry(F4, bd=5)
    E2.grid()

    wynik = scrolledtext.ScrolledText(F6, width=40, height=10)
    wynik.grid()
    # self.lista = scrolledtext.ScrolledText(self.F7, width=40, height=16)
    # self.lista.grid()

    listatree = ttk.Treeview(F7, height=20, columns=('',''))
    listatree.grid()
    listatree.heading('#0', text="Index")
    listatree.heading('#1', text="Imie")
    listatree.heading('#2', text="Nazwisko")

    ##zmienione przez Juleczke! wczesniej bylo pod def zamknij()
    # Definicje przycisków
    def kliknij():
        dod = E1.get() + " " + E2.get()
        #Hodowcy.append(dod)

        res = "Dodano hodowce: " + E1.get() + " " + E2.get() + "\n"
        wynik.insert(INSERT, res)
        return

    def show():
        j = 0
        if j < len(czytajhodowcow()):
            for lista in czytajhodowcow():
                listatree.insert('', 0, text=lista[0], values=(lista[1], lista[2]))
        j = +1
        return

    def czytajhodowcow():
        """Funckja wczytująca wszystkich hodowców z bazy"""
        conn = sqlite3.connect('baza.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(" SELECT id_hod, imie, nazwisko FROM HODOWCY")
        hodowca = cur.fetchall()
        lista = []
        for hod in hodowca:
            hodor = (hod['id_hod'], hod['imie'], hod['nazwisko'])
            lista.append(hodor)
        conn.commit()
        cur.close()
        conn.close()
        return lista

        def zamknij():  # zmodyfikować i dodać do przycisku
            msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
            if msg == 'yes':
                dodaj.destroy
            else:
                return

        # Tworzenie przyciskow
        btn1 = Button(F5, text="Dodaj nowego Hodowce", command=kliknij)
        btn2 = Button(F8, text="Wyświetl spis hodowców", command=show)
        btn4 = Button(F10, text="Zamknij", command=dodaj.destroy)

        # Ulozenie przyciskow
        btn1.grid()
        btn2.grid()
        btn4.grid()

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Edycja Hodowcy
# To do:
''' Pozmieniaj nazwy i dostosuj wygląd okna i połącz go z funkcjami'''
# Wygląd okna

def edytujHodowce():
    edycja = Tk()
    edycja.geometry("800x350+0+0")
    edycja.title("Edycja Hodowcy")
    edycja_label = tk.Label(edycja)
    edycja_label.grid()

    F1 = Frame(edycja, borderwidth=2, relief='ridge')  # Nazwa Hodowcy
    F1.grid(column=0, row=0)
    F2 = Frame(edycja, borderwidth=2, relief='ridge')  # Entry imie
    F2.grid(column=4, row=2)
    F3 = Frame(edycja, borderwidth=2, relief='ridge')  # Listbox
    F3.grid(column=0, row=2)
    F4 = Frame(edycja, borderwidth=2, relief='ridge')  # wybierz
    F4.grid(column=2, row=2)
    F5 = Frame(edycja, borderwidth=2, relief='ridge')  # Zapisz
    F5.grid(column=7, row=2)
    F6 = Frame(edycja, borderwidth=2)  # 2 strzałka
    F6.grid(column=3, row=2)
    F7 = Frame(edycja, borderwidth=2)  # 1 strzałka
    F7.grid(column=1, row=2)
    F8 = Frame(edycja, borderwidth=2)  # 3 strzałka
    F8.grid(column=6, row=2)
    F9 = Frame(edycja, borderwidth=2, relief='ridge')  # Entry nazwisko
    F9.grid(column=5, row=2)
    F10 = Frame(edycja, borderwidth=2)  # Nazwa Imie
    F10.grid(column=4, row=1)
    F11 = Frame(edycja, borderwidth=2)  # Nazwa Nazwisko
    F11.grid(column=5, row=1)
    F12 = Frame(edycja, borderwidth=2)  # Odśwież
    F12.grid(column=0, row=1)
    F13 = Frame(edycja, borderwidth=2, relief='ridge')  # Zamknij
    F13.grid(column=0, row=3)

    L1 = Label(F1, text="HODOWCY")
    L1.grid()
    E1 = Entry(F2, bd=5)
    E1.grid()
    E2 = Entry(F9, bd=5)
    E2.grid()
    L2 = Label(F6, text="--->")
    L2.grid()
    L3 = Label(F7, text="--->")
    L3.grid()
    L4 = Label(F8, text="--->")
    L4.grid()
    L5 = Label(F10, text="Imie")
    L5.grid()
    L5 = Label(F11, text="Nazwisko")
    L5.grid()

    listatree = ttk.Treeview(F3, height=14, columns=('Indeks', 'Imie', 'Nazwisko'))
    listatree.grid()
    listatree.heading('#0', text="Index")
    listatree.heading('#1', text="Imie")
    listatree.heading('#2', text="Nazwisko")


    # znowu zmienione przez Juleczke- ta czesc byla pod def zamknij()
    # Tworzenie przyciskow
    btn1 = Button(F4, text="Wybierz", command=show)
    btn2 = Button(F5, text="Zapisz zmiane")
    btn3 = Button(F12, text="Odśwież")
    btn4 = Button(F13, text="Zamknij", command=edycja.destroy)

    # Ulozenie przyciskow
    btn1.grid()
    btn2.grid()
    btn3.grid()
    btn4.grid()


    # Definicje przycisków
    def czytajhodowcow():
        """Funckja wczytująca wszystkich hodowców z bazy"""
        conn = sqlite3.connect('baza.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(" SELECT id_hod, imie, nazwisko FROM HODOWCY")
        hodowca = cur.fetchall()
        lista = []
        for hod in hodowca:
            hodor = (hod['id_hod'], hod['imie'], hod['nazwisko'])
            lista.append(hodor)
        conn.commit()
        cur.close()
        conn.close()
        return lista

    def show():
        j = 0
        if j < len(czytajhodowcow()):
            for lista in czytajhodowcow():
                listatree.insert('', 0, text=lista[0], values=(lista[1], lista[2]))
        j = +1
        return

    '''def wybierz():
        lista1 = int(lista.curselection()[0])  # wyświetlanie argumentów z listboxa
        dane = Hodowcy[lista1].split()
        E1.insert(INSERT, dane[0])
        E2.insert(INSERT, dane[1])'''


    def zamknij():  # zmodyfikować i dodać do przycisku
        msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if msg == 'yes':
            edycja.destroy
        else:
            return
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Usuwanie Hodowcy
# Wygląd okna

def usunHodowce():
    usun = Tk()
    usun.geometry("700x400+0+0")
    usun.title("Usuwanie Hodowcy")
    usun_label = tk.Label(usun)
    usun_label.grid()

    F1 = Frame(usun, borderwidth=2, relief='ridge')  # Nazwa Hodowcy
    F1.grid(column=0, row=0)
    F9 = Frame(usun, borderwidth=2, relief="ridge")  # odśwież
    F9.grid(column=0, row=1)
    F2 = Frame(usun, borderwidth=2, relief='ridge')  # Entry imie
    F2.grid(column=4, row=2)
    F3 = Frame(usun, borderwidth=2, relief='ridge')  # Listbox
    F3.grid(column=0, row=2)
    F4 = Frame(usun, borderwidth=2, relief='ridge')  # wybierz
    F4.grid(column=2, row=2)
    F5 = Frame(usun, borderwidth=2, relief='ridge')  # Zapisz
    F5.grid(column=7, row=2)
    F6 = Frame(usun, borderwidth=2)  # 2 strzałka
    F6.grid(column=3, row=2)
    F7 = Frame(usun, borderwidth=2)  # 1 strzałka
    F7.grid(column=1, row=2)
    F8 = Frame(usun, borderwidth=2)  # 3 strzałka
    F8.grid(column=6, row=2)
    F10 = Frame(usun, borderwidth=2, relief='ridge')  # Zamknij
    F10.grid(column=0, row=3)

    L1 = Label(F1, text="Lista Hodowców")
    L1.grid()
    E1 = Entry(F2, bd=5)
    E1.grid()
    L2 = Label(F6, text="--->")
    L2.grid()
    L3 = Label(F7, text="--->")
    L3.grid()
    L4 = Label(F8, text="--->")
    L4.grid()

    lista = Listbox(F3, width=40, height=16, selectmode=SINGLE)
    for imie in Hodowcy:
        lista.insert(END, imie)
    lista.grid()

    # zmienione przez Juleczke

    # Tworzenie przyciskow
    btn1 = Button(F4, text="Wybierz")
    btn2 = Button(F5, text="Usuń Hodowce", command=usuwanie)
    btn3 = Button(F9, text="Odśwież")
    btn4 = Button(F10, text="Zamknij", command=usun.destroy)

    # Ulozenie przyciskow
    btn1.grid()
    btn2.grid()
    btn3.grid()
    btn4.grid()


    # Definicje przycisków
    def wybierz():
        lista1 = int(lista.curselection()[0])  # wyświetlanie argumentów z listboxa
        dane = Hodowcy[lista1].split()


    def usuwanie():
        msg = messagebox.askquestion("Usuwanie", "Czy jesteś pewny, że chcesz usunąć tego hodowce?",
                                     icon="warning")
        if msg == 'yes':
            print("To usunie hodowce")
        else:
            print("To wróci do wyboru hodowcy")
            return


    def zamknij():  # zmodyfikować i dodać do przycisku
        msg = messagebox.askquestion("Wyjście", "Czy jesteś pewny, że chcesz zamknąć to okno?", icon="warning")
        if msg == 'yes':
            usun.destroy()
        else:
            return
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Wyświetlanie drzewa
# Widget

def Wtree():
    tree = Tk()
    tree.geometry("700x400+0+0")
    tree.title("Drzewo rodowodowe")
    tree_label = Label(tree)
    tree_label.grid()

    F1 = Frame(tree, borderwidth=2, relief='ridge')
    F1.grid(column=0, row=0)
    F2 = Frame(tree, borderwidth=2, relief='ridge')
    F2.grid(column=0, row=1)
    F3 = Frame(tree, borderwidth=2, relief='ridge')
    F3.grid(column=1, row=1)
    F4 = Frame(tree, borderwidth=2, relief='ridge')
    F4.grid(column=2, row=1)

    L1 = Label(F1, text="Lista nazw osobników")
    L1.grid()
    L2 = Label(F3, text="Wybrano osobnika o nazwie:")
    E1 = Entry(F4, bd=5)
    E1.grid()

    show = Listbox(F2, width=60, height=40, selectmode=SINGLE)
    show.grid(column=1, row=0)

    # Definicje przyciskow

    # Tworzenie przyciskow
    btn1 = Button(tree, text="Wyszukaj")
    # Ulozenie przyciskow
    btn1.grid(column=4, row=0)

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Średni współczynnik pokrewieństwa
# Widget
def avgpokrewienstwo():
    avg = Tk()
    avg.geometry("700x400+0+0")
    avg.title("Średni wspólczynnik pokrewieństwa")
    avg_label = Label(avg)
    avg_label.grid()

    F1 = Frame(avg, borderwidth=2, relief='ridge')
    F1.grid(column=0, row=0)
    F2 = Frame(avg, borderwidth=2, relief='ridge')
    F2.grid(column=0, row=1)

    L1 = Label(F1, text="Lista Osobników")
    L1.grid()

    lista = Listbox(F2, width=40, height=16, selectmode=SINGLE)
    for nazwa in Osobniki:
        lista.insert(END, nazwa)
    lista.grid()
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Współczynnik imbredu
# Widget
def imbred():
    wsimb = Tk()
    wsimb.geometry("700x400+0+0")
    wsimb.title("Współczynnik imbredu")
    wsimb_label = Label(wsimb)
    wsimb_label.grid()
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Współczynnik pokrewieństwa
# Widget
def pokrewienstwo():
    wspok = Tk()
    wspok.geometry("700x400")
    wspok.title("Współczynnik pokrewieństwa")
    wspok_label = Label(wspok)
    wspok_label.grid()
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Współczynnik utraty przodków
# Widget
def utrata():
    wsutraty = Tk()
    wsutraty.geometry("700x400+0+0")
    wsutraty.title("Współczynnik utraty przodków")
    wsutraty_label = Label(wsutraty)
    wsutraty_label.grid()
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


#######################################################################################################################
# okno root
root = Tk()  # root widget - musi zostać stworzony przed innymi widgetami
root.geometry("1400x500+0+0")
root.title("Pracownia Informatyczna")  # tytuł naszej tabeli root
root_label = tk.Label(root)
root_label.grid()

# Menu
menu = Menu(root)
root.config(menu=menu)
filemenu = tk.Menu(menu)
# Plik
menu.add_cascade(label="Plik", menu=filemenu)
filemenu.add_command(label="Otwórz", command=baseopen)
filemenu.add_command(label="Edycja struktury")
filemenu.add_command(label="Zamknij baze", command=baseclose)
filemenu.add_separator()
filemenu.add_command(label="Zamknij program", command=root.destroy)

# Edycja
edycja = Menu(menu)
gatunek = Menu(menu)
osobnik = Menu(menu)
hodowca = Menu(menu)
menu.add_cascade(label="Edycja", menu=edycja)

edycja.add_cascade(label="Gatunek", menu=gatunek)
gatunek.add_command(label="Dodaj nowy gatunek", command=dodajGatunek)
gatunek.add_command(label="Usuń istniejący gatunek", command=usunGatunek)
gatunek.add_command(label="Edytuj istniejący gatunek", command=edytujGatunek)

edycja.add_cascade(label="Osobnik", menu=osobnik)
osobnik.add_command(label="Dodaj nowego osobnika", command=dodajOsobnika)
osobnik.add_command(label="Usuń istniejącego osobnika", command=usunOsobnika)
osobnik.add_command(label="Edytuj istniejącego osobnika", command=edytujOsobnika)

edycja.add_cascade(label="Hodowca", menu=hodowca)
hodowca.add_command(label="Dodaj nowego hodowce", command=dodajHodowce)
hodowca.add_command(label="Usuń istniejącego hodowce", command=usunHodowce)
hodowca.add_command(label="Edytuj istniejącego hodowce", command=edytujHodowce)

# Obliczenia
oblicz = Menu(menu)
menu.add_cascade(label="Współczynniki", menu=oblicz)
oblicz.add_command(label="Średni współczynnik pokrewieństwa", command=avgpokrewienstwo)
oblicz.add_command(label="Współczynnik inbredu", command=imbred)
oblicz.add_command(label="Współczynnik pokrewieństa", command=pokrewienstwo)
oblicz.add_command(label="Współczynnik utraty przodków", command=utrata)

# Wyświetlanie drzewa
tree = Menu(menu)
menu.add_cascade(label="Drzewo", menu=tree)
tree.add_command(label="Wyśwetl drzewo rodowodowe osobnika", command=Wtree)

root.mainloop()  # zamknięcie pętli
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
