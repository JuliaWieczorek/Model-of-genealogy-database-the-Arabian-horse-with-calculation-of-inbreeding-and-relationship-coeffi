# -*- coding: cp1250 -*-

#import baza
#import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import filedialog
#from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import Listbox
from tkinter import Scrollbar

Hodowcy=['Cezary Bober', 'Julia Wieczorek', 'Mateusz Markowski', 'Alicja Dera']
# DEFINICJE
######################################################################################################################

#---------------------------------------------------------------------------------------------------------------------
# Otwieranie bazy danych i zamykanie
def baseopen(): #To chyba dzia�a
    db=filedialog.askopenfilename(initialdir = "D:\Studia\Magisterka\Semestr_1\Projekty_1\IBD",
                                  title = "Wybierz baze danych",
                                  filetypes = (("Bazy danych","*.db"),("all files","*.*")))
    #cursor = db.cursor()
    print("widzisz to to dzia�a")

def baseclose(db): # to nie dzia�a jeszcze
    db.close()
    print("widzisz to to dzia�a")
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#---------------------------------------------------------------------------------------------------------------------
#Dodaj Nowego Hodowce
#To do:
''' po��cz go z funkcjami spraw �eby listy si� czy�ci�y przed kolejnym wy�wietleniem'''
def dodajHodowce():
    # Wygl�d okna
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

    L1 = Label(F1, text="Imi� Hodowcy")
    L1.grid()
    E1 = Entry(F2, bd=5)
    E1.grid()

    L2 = Label(F3, text="Nazwisko Hodowcy")
    L2.grid()
    E2 = Entry(F4, bd=5)
    E2.grid()

    wynik = scrolledtext.ScrolledText(F6, width=40, height=10)
    wynik.grid()
    lista = scrolledtext.ScrolledText(F7, width=40, height=16)
    lista.grid()

    # Definicje przycisk�w
    def kliknij():
        dod = E1.get() + " " + E2.get()
        Hodowcy.append(dod)
      #  print(Hodowcy)
        res = "Dodano hodowce: " + E1.get() + " " + E2.get() + "\n"
        wynik.insert(INSERT, res)
        return

    def show():
        j = 0
        if j < len(Hodowcy):
            for imie in Hodowcy:
                res = imie + "\n"
                lista.insert(INSERT, res)
        j=+1
        return

    # Tworzenie przyciskow
    btn1 = Button(F5, text="Dodaj nowego Hodowce", command=kliknij)
    btn2 = Button(F8, text="Wy�wietl spis hodowc�w", command=show)

    # Ulozenie przyciskow
    btn1.grid()
    btn2.grid()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#---------------------------------------------------------------------------------------------------------------------
#Edycja Hodowcy
# To do:
''' Pozmieniaj nazwy i dostosuj wygl�d okna i po��cz go z funkcjami'''
def edytujHodowce():
    # Wygl�d okna
    edycja = Tk()
    edycja.geometry("700x400+0+0")
    edycja.title("Edycja Hodowcy")
    edycja_label = tk.Label(edycja)
    edycja_label.grid()

    F1=Frame(edycja, borderwidth=2, relief='ridge')
    F1.grid(column=0,row=0)
    F2 = Frame(edycja, borderwidth=2, relief='ridge')
    F2.grid(column=1, row=2)
    F3 = Frame(edycja, borderwidth=2, relief='ridge')
    F3.grid(column=0, row=2)
    F4 = Frame(edycja, borderwidth=2, relief='ridge')
    F4.grid(column=1, row=0)


    L1 = Label(F1, text="HODOWCY")
    L1.grid()
    E1 = Entry(F2, bd=5)
    E1.grid()

    #L1 = Label(edycja, text="Nazwisko Hodowcy")
   # L1.grid()
   # E2 = Entry(edycja, bd=5)
    #E2.grid()
    #wynik=scrolledtext.ScrolledText(F2, width=40, height=16)
    #wynik.grid()

    lista=Listbox(F3,width=40,height=16)
    for imie in Hodowcy:
        lista.insert(END, imie)
    lista.grid()



    # Definicje przycisk�w
    def kliknij():

        dod = E1.get() + " " + E2.get()
        Hodowcy.append(dod)
        print (Hodowcy)
        res = "Nowo dodany hodowca to: " + E1.get() +" "+ E2.get() + "\n"
        wynik.insert(INSERT,res)
        return

    def wybierz():
        lista1 = lista.curselection()
        E1.insert(INSERT, lista1)


    # Tworzenie przyciskow
    btn1 = Button(F4, text = "Wybierz", command=wybierz)
    #btn2 = Button(edycja, text="Edytuj")
    #btn3 = Button(edycja, text="Usu� Hodowce")

    # Ulozenie przyciskow
    btn1.grid()
    #btn2.grid( column = 1, row = 1 )
    #btn3.grid( column = 1, row = 2 )

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
#Usuwanie Hodowcy
def usunHodowce():
    #Wygl�d okna
    usun = Tk()
    usun.geometry("700x400+0+0")
    usun.title("Usuwanie Hodowcy")
    usun_label = tk.Label(usun)
    usun_label.grid()

    F1 = Frame(usun, borderwidth=2, relief='ridge')
    F1.grid(column=0, row=0)
    F2 = Frame(usun, borderwidth=2, relief='ridge')
    F2.grid(column=1, row=0)
    F3 = Frame(usun, borderwidth=2, relief='ridge')
    F3.grid(column=0, row=1)
    F4 = Frame(usun, borderwidth=2, relief='ridge')
    F4.grid(column=1, row=1)


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Wy�wietlanie drzewa
def Wtree():
    # Widget
    tree=Tk()
    tree.geometry("700x400+0+0")
    tree.title("Drzewo rodowodowe")
    tree_label = Label(tree)
    tree_label.grid()

    L1 = Label(tree, text="Nazwa Osobnika")
    L1.grid(column=2, row=0)
    E1 = Entry(tree, bd=5)
    E1.grid(column=3, row=0)

    show = scrolledtext.ScrolledText(tree, width=60, height=40)
    show.grid(column=1, row=0)

    # Definicje przyciskow

    # Tworzenie przyciskow
    btn1 = Button(tree, text="Wyszukaj")
    # Ulozenie przyciskow
    btn1.grid(column=4, row=0)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# �redni wsp�czynnik pokrewie�stwa
def avgpokrewienstwo():
    # Widget
    avg = Tk()
    avg.geometry("700x400+0+0")
    avg.title("�redni wsp�lczynnik pokrewie�stwa")
    avg_label = Label(avg)
    avg_label.grid()


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Wsp�czynnik imbredu
def imbred():
    # Widget
    wsimb= Tk()
    wsimb.geometry("700x400+0+0")
    wsimb.title("Wsp�czynnik imbredu")
    wsimb_label = Label(wsimb)
    wsimb_label.grid()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Wsp�czynnik pokrewie�stwa
def pokrewienstwo():
    # Widget
    wspok= Tk()
    wspok.geometry("700x400")
    wspok.title("Wsp�czynnik pokrewie�stwa")
    wspok_label = Label(wspok)
    wspok_label.grid()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Wsp�czynnik utraty przodk�w
def utrata():
    # Widget
    wsutraty= Tk()
    wsutraty.geometry("700x400+0+0")
    wsutraty.title("Wsp�czynnik utraty przodk�w")
    wsutraty_label = Label(wsutraty)
    wsutraty_label.grid()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#######################################################################################################################


# okno root
root = Tk() # root widget - musi zosta� stworzony przed innymi widgetami
root.geometry("1400x500+0+0")
root.title("Pracownia Informatyczna") # tytu� naszej tabeli root
root_label = tk.Label(root)
root_label.grid()

# Menu

menu = Menu(root)
root.config(menu = menu)
filemenu = tk.Menu(menu)
# Plik
menu.add_cascade(label = "Plik", menu=filemenu)
filemenu.add_command(label="Otw�rz",command=baseopen)
filemenu.add_command(label="Edycja struktury")
filemenu.add_command(label="Zamknij baze",command=baseclose)
filemenu.add_separator()
filemenu.add_command(label="Zamknij program", command = root.destroy)

# Edycja
edycja = Menu(menu)
gatunek = Menu(menu)
osobnik = Menu(menu)
hodowca = Menu(menu)
menu.add_cascade(label = "Edycja", menu=edycja)

edycja.add_cascade(label="Gatunek", menu=gatunek)
gatunek.add_command(label="Dodaj nowy gatunek")
gatunek.add_command(label="Usu� istniej�cy gatunek")
gatunek.add_command(label="Edytuj istniej�cy gatunek")

edycja.add_cascade(label="Osobnik", menu=osobnik)
osobnik.add_command(label="Dodaj nowego osobnika")
osobnik.add_command(label="Usu� istniej�cego osobnika")
osobnik.add_command(label="Edytuj istniej�cego osobnika")

edycja.add_cascade(label="Hodowca", menu = hodowca )
hodowca.add_command(label="Dodaj nowego hodowce", command=dodajHodowce)
hodowca.add_command(label="Usu� istniej�cego hodowce", command=usunHodowce)
hodowca.add_command(label="Edytuj istniej�cego hodowce",command=edytujHodowce)

# Obliczenia
oblicz = Menu(menu)
menu.add_cascade(label = "Wsp�czynniki", menu=oblicz)
oblicz.add_command(label="�redni wsp�czynnik pokrewie�stwa", command=avgpokrewienstwo)
oblicz.add_command(label="Wsp�czynnik inbredu", command=imbred)
oblicz.add_command(label="Wsp�czynnik pokrewie�sta", command=pokrewienstwo)
oblicz.add_command(label="Wsp�czynnik utraty przodk�w", command=utrata)

# Wy�wietlanie drzewa

tree = Menu(menu)
menu.add_cascade(label = "Drzewo", menu=tree)
tree.add_command(label="Wy�wetl drzewo rodowodowe osobnika",command = Wtree )


root.mainloop() # zamkni�cie p�tli
