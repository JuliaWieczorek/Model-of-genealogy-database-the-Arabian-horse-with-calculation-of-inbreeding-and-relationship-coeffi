# -*- coding: cp1250 -*-

import tkinter as tk
# import baza
# import sqlite3
from tkinter import *
from tkinter import Listbox
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext


# from tkinter import Scrollbar

class FRONTEND(object):
    Hodowcy = ['Cezary Bober', 'Julia Wieczorek', 'Mateusz Markowski', 'Alicja Dera']
    Osobniki = ['KARO', 'FARO', 'DONIO', 'DEMO', 'HAPPY', 'SETO']

    # DEFINICJE
    ######################################################################################################################

    # ---------------------------------------------------------------------------------------------------------------------
    # Otwieranie bazy danych i zamykanie
    def baseopen(self):  # To chyba dzia�a
        self.db = filedialog.askopenfilename(initialdir="D:\Studia\Magisterka\Semestr_1\Projekty_1\IBD",
                                        title="Wybierz baze danych",
                                        filetypes=(("Bazy danych", "*.db"), ("all files", "*.*")))
        # cursor = db.cursor()
        print("widzisz to to dzia�a")

    def baseclose(self, db):  # to nie dzia�a jeszcze
        self.db.close()
        print("widzisz to to dzia�a")

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Dodaj Nowego Hodowce
    # To do:
    ''' po��cz go z funkcjami spraw �eby listy si� czy�ci�y przed kolejnym wy�wietleniem'''

    def dodajHodowce(self):
        # Wygl�d okna
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

        self.L1 = Label(self.F1, text="Imi� Hodowcy")
        self.L1.grid()
        self.E1 = Entry(self.F2, bd=5)
        self.E1.grid()

        self.L2 = Label(self.F3, text="Nazwisko Hodowcy")
        self.L2.grid()
        self.E2 = Entry(self.F4, bd=5)
        self.E2.grid()

        self.wynik = scrolledtext.ScrolledText(self.F6, width=40, height=10)
        self.wynik.grid()
        self.lista = scrolledtext.ScrolledText(self.F7, width=40, height=16)
        self.lista.grid()

        # Definicje przycisk�w
        def kliknij(self):
            self.dod = self.E1.get() + " " + self.E2.get()
            self.Hodowcy.append(self.dod)
            self.res = "Dodano hodowce: " + self.E1.get() + " " + self.E2.get() + "\n"
            self.wynik.insert(INSERT, self.res)
            return

        def show(self):
            self.j = 0
            if self.j < len(self.Hodowcy):
                for self.imie in self.Hodowcy:
                    self.res = self.imie + "\n"
                    self.lista.delete('0.0', END) # dzia�a ale nie tak jak ma
                    self.lista.insert(INSERT, self.res)
            self.j = +1
            return

        def zamknij(self):  # zmodyfikowa� i doda� do przycisku
            self.msg = messagebox.askquestion("Wyj�cie", "Czy jeste� pewny, �e chcesz zamkn�� to okno?", icon="warning")
            if self.msg == 'yes':
                self.dodaj.destroy
            else:
                return

        # Tworzenie przyciskow
        self.btn1 = Button(self.F5, text="Dodaj nowego Hodowce", command=kliknij)
        self.btn2 = Button(self.F8, text="Wy�wietl spis hodowc�w", command=show)
        self.btn4 = Button(self.F10, text="Zamknij", command=self.dodaj.destroy)

        # Ulozenie przyciskow
        self.btn1.grid()
        self.btn2.grid()
        self.btn4.grid()

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Edycja Hodowcy
    # To do:
    ''' Pozmieniaj nazwy i dostosuj wygl�d okna i po��cz go z funkcjami'''

    def edytujHodowce(self):
        # Wygl�d okna
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
        self.F6 = Frame(self.edycja, borderwidth=2)  # 2 strza�ka
        self.F6.grid(column=3, row=2)
        self.F7 = Frame(self.edycja, borderwidth=2)  # 1 strza�ka
        self.F7.grid(column=1, row=2)
        self.F8 = Frame(self.edycja, borderwidth=2)  # 3 strza�ka
        self.F8.grid(column=6, row=2)
        self.F9 = Frame(self.edycja, borderwidth=2, relief='ridge')  # Entry nazwisko
        self.F9.grid(column=5, row=2)
        self.F10 = Frame(self.edycja, borderwidth=2)  # Nazwa Imie
        self.F10.grid(column=4, row=1)
        self.F11 = Frame(self.edycja, borderwidth=2)  # Nazwa Nazwisko
        self.F11.grid(column=5, row=1)
        self.F12 = Frame(self.edycja, borderwidth=2)  # Od�wie�
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
        for self.imie in self.Hodowcy:
            self.lista.insert(END, self.imie)
        self.lista.grid()

        # Definicje przycisk�w
        def wybierz(self):
            self.lista1 = int(self.lista.curselection()[0])  # wy�wietlanie argument�w z listboxa
            self.dane = self.Hodowcy[self.lista1].split()
            self.E1.insert(INSERT, self.dane[0])
            self.E2.insert(INSERT, self.dane[1])

        def zamknij(self):  # zmodyfikowa� i doda� do przycisku
            self.msg = messagebox.askquestion("Wyj�cie", "Czy jeste� pewny, �e chcesz zamkn�� to okno?", icon="warning")
            if self.msg == 'yes':
                self.edycja.destroy
            else:
                return

        # Tworzenie przyciskow
        self.btn1 = Button(self.F4, text="Wybierz", command=wybierz)
        self.btn2 = Button(self.F5, text="Zapisz zmiane")
        self.btn3 = Button(self.F12, text="Od�wie�")
        self.btn4 = Button(self.F13, text="Zamknij", command=self.edycja.destroy)

        # Ulozenie przyciskow
        self.btn1.grid()
        self.btn2.grid()
        self.btn3.grid()
        self.btn4.grid()

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Usuwanie Hodowcy
    def usunHodowce(self):
        # Wygl�d okna
        self.usun = Tk()
        self.usun.geometry("700x400+0+0")
        self.usun.title("Usuwanie Hodowcy")
        self.usun_label = tk.Label(self.usun)
        self.usun_label.grid()

        self.F1 = Frame(self.usun, borderwidth=2, relief='ridge')  # Nazwa Hodowcy
        self.F1.grid(column=0, row=0)
        self.F9 = Frame(self.usun, borderwidth=2, relief="ridge")  # od�wie�
        self.F9.grid(column=0, row=1)
        self.F2 = Frame(self.usun, borderwidth=2, relief='ridge')  # Entry imie
        self.F2.grid(column=4, row=2)
        self.F3 = Frame(self.usun, borderwidth=2, relief='ridge')  # Listbox
        self.F3.grid(column=0, row=2)
        self.F4 = Frame(self.usun, borderwidth=2, relief='ridge')  # wybierz
        self.F4.grid(column=2, row=2)
        self.F5 = Frame(self.usun, borderwidth=2, relief='ridge')  # Zapisz
        self.F5.grid(column=7, row=2)
        self.F6 = Frame(self.usun, borderwidth=2)  # 2 strza�ka
        self.F6.grid(column=3, row=2)
        self.F7 = Frame(self.usun, borderwidth=2)  # 1 strza�ka
        self.F7.grid(column=1, row=2)
        self.F8 = Frame(self.usun, borderwidth=2)  # 3 strza�ka
        self.F8.grid(column=6, row=2)
        self.F10 = Frame(self.usun, borderwidth=2, relief='ridge')  # Zamknij
        self.F10.grid(column=0, row=3)

        self.L1 = Label(self.F1, text="Lista Hodowc�w")
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
        for self.imie in self.Hodowcy:
            self.lista.insert(END, self.imie)
        self.lista.grid()

        # Definicje przycisk�w
        def wybierz(self):
            self.lista1 = int(self.lista.curselection()[0])  # wy�wietlanie argument�w z listboxa
            self.dane = self.Hodowcy[self.lista1].split()

        def usuwanie(self):
            self.msg = messagebox.askquestion("Usuwanie", "Czy jeste� pewny, �e chcesz usun�� tego hodowce?", icon="warning")
            if self.msg == 'yes':
                print("To usunie hodowce")
            else:
                print("To wr�ci do wyboru hodowcy")
                return

        def zamknij(self):  # zmodyfikowa� i doda� do przycisku
            self.msg = messagebox.askquestion("Wyj�cie", "Czy jeste� pewny, �e chcesz zamkn�� to okno?", icon="warning")
            if self.msg == 'yes':
                self.usun.destroy()
            else:
                return

        # Tworzenie przyciskow
        self.btn1 = Button(self.F4, text="Wybierz")
        self.btn2 = Button(self.F5, text="Usu� Hodowce", command=usuwanie)
        self.btn3 = Button(self.F9, text="Od�wie�")
        self.btn4 = Button(self.F10, text="Zamknij", command=self.usun.destroy)

        # Ulozenie przyciskow
        self.btn1.grid()
        self.btn2.grid()
        self.btn3.grid()
        self.btn4.grid()

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Wy�wietlanie drzewa
    def Wtree(self):
        # Widget
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

        self.L1 = Label(self.F1, text="Lista nazw osobnik�w")
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
    # �redni wsp�czynnik pokrewie�stwa
    def avgpokrewienstwo(self):
        # Widget
        self.avg = Tk()
        self.avg.geometry("700x400+0+0")
        self.avg.title("�redni wsp�lczynnik pokrewie�stwa")
        self.avg_label = Label(self.avg)
        self.avg_label.grid()

        self.F1 = Frame(self.avg, borderwidth=2, relief='ridge')
        self.F1.grid(column=0, row=0)
        self.F2 = Frame(self.avg, borderwidth=2, relief='ridge')
        self.F2.grid(column=0, row=1)

        self.L1 = Label(self.F1, text="Lista Osobnik�w")
        self.L1.grid()

        self.lista = Listbox(self.F2, width=40, height=16, selectmode=SINGLE)
        for self.nazwa in self.Osobniki:
            self.lista.insert(END, self.nazwa)
        self.lista.grid()

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Wsp�czynnik imbredu
    def imbred(self):
        # Widget
        self.wsimb = Tk()
        self.wsimb.geometry("700x400+0+0")
        self.wsimb.title("Wsp�czynnik imbredu")
        self.wsimb_label = Label(self.wsimb)
        self.wsimb_label.grid()

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Wsp�czynnik pokrewie�stwa
    def pokrewienstwo(self):
        # Widget
        self.wspok = Tk()
        self.wspok.geometry("700x400")
        self.wspok.title("Wsp�czynnik pokrewie�stwa")
        self.wspok_label = Label(self.wspok)
        self.wspok_label.grid()

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ---------------------------------------------------------------------------------------------------------------------
    # Wsp�czynnik utraty przodk�w
    def utrata(self):
        # Widget
        self.wsutraty = Tk()
        self.wsutraty.geometry("700x400+0+0")
        self.wsutraty.title("Wsp�czynnik utraty przodk�w")
        self.wsutraty_label = Label(self.wsutraty)
        self.wsutraty_label.grid()

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #######################################################################################################################
    def __init__(self):
        # okno root
        self.root = Tk()  # root widget - musi zosta� stworzony przed innymi widgetami
        self.root.geometry("1400x500+0+0")
        self.root.title("Pracownia Informatyczna")  # tytu� naszej tabeli root
        self.root_label = tk.Label(self.root)
        self.root_label.grid()

        # Menu
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu)
        # Plik
        self.menu.add_cascade(label="Plik", menu=self.filemenu)
        self.filemenu.add_command(label="Otw�rz", command=self.baseopen)
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
        self.gatunek.add_command(label="Dodaj nowy gatunek")
        self.gatunek.add_command(label="Usu� istniej�cy gatunek")
        self.gatunek.add_command(label="Edytuj istniej�cy gatunek")

        self.edycja.add_cascade(label="Osobnik", menu=self.osobnik)
        self.osobnik.add_command(label="Dodaj nowego osobnika")
        self.osobnik.add_command(label="Usu� istniej�cego osobnika")
        self.osobnik.add_command(label="Edytuj istniej�cego osobnika")

        self.edycja.add_cascade(label="Hodowca", menu=self.hodowca)
        self.hodowca.add_command(label="Dodaj nowego hodowce", command=self.dodajHodowce)
        self.hodowca.add_command(label="Usu� istniej�cego hodowce", command=self.usunHodowce)
        self.hodowca.add_command(label="Edytuj istniej�cego hodowce", command=self.edytujHodowce)

        # Obliczenia
        self.oblicz = Menu(self.menu)
        self.menu.add_cascade(label="Wsp�czynniki", menu=self.oblicz)
        self.oblicz.add_command(label="�redni wsp�czynnik pokrewie�stwa", command=self.avgpokrewienstwo)
        self.oblicz.add_command(label="Wsp�czynnik inbredu", command=self.imbred)
        self.oblicz.add_command(label="Wsp�czynnik pokrewie�sta", command=self.pokrewienstwo)
        self.oblicz.add_command(label="Wsp�czynnik utraty przodk�w", command=self.utrata)

        # Wy�wietlanie drzewa
        self.tree = Menu(self.menu)
        self.menu.add_cascade(label="Drzewo", menu=self.tree)
        self.tree.add_command(label="Wy�wetl drzewo rodowodowe osobnika", command=self.Wtree)

        self.root.mainloop()  # zamkni�cie p�tli

baza=FRONTEND()