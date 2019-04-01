#-*- coding: cp1250 -*-

#import baza
#import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import Listbox
#from tkinter import Scrollbar

Hodowcy=['Cezary Bober', 'Julia Wieczorek', 'Mateusz Markowski', 'Alicja Dera']
Osobniki=['KARO','FARO','DONIO','DEMO','HAPPY','SETO']
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
    F10 = Frame(dodaj, borderwidth=2, relief='ridge')  # Zamknij
    F10.grid(column=0, row=5)

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

    def zamknij(): # zmodyfikowa� i doda� do przycisku
        msg =messagebox.askquestion("Wyj�cie","Czy jeste� pewny, �e chcesz zamkn�� to okno?", icon="warning")
        if msg == 'yes':
            dodaj.destroy
        else:
            return

    # Tworzenie przyciskow
    btn1 = Button(F5, text="Dodaj nowego Hodowce", command=kliknij)
    btn2 = Button(F8, text="Wy�wietl spis hodowc�w", command=show)
    btn4 = Button(F10, text="Zamknij", command=dodaj.destroy)


    # Ulozenie przyciskow
    btn1.grid()
    btn2.grid()
    btn4.grid()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#---------------------------------------------------------------------------------------------------------------------
#Edycja Hodowcy
# To do:
''' Pozmieniaj nazwy i dostosuj wygl�d okna i po��cz go z funkcjami'''
def edytujHodowce():
    # Wygl�d okna
    edycja = Tk()
    edycja.geometry("800x350+0+0")
    edycja.title("Edycja Hodowcy")
    edycja_label = tk.Label(edycja)
    edycja_label.grid()

    F1=Frame(edycja, borderwidth=2, relief='ridge') # Nazwa Hodowcy
    F1.grid(column=0,row=0)
    F2 = Frame(edycja, borderwidth=2, relief='ridge') # Entry imie
    F2.grid(column=4, row=2)
    F3 = Frame(edycja, borderwidth=2, relief='ridge') # Listbox
    F3.grid(column=0, row=2)
    F4 = Frame(edycja, borderwidth=2, relief='ridge') # wybierz
    F4.grid(column=2, row=2)
    F5 = Frame(edycja, borderwidth=2, relief='ridge') # Zapisz
    F5.grid(column=7, row=2)
    F6 = Frame(edycja, borderwidth=2) # 2 strza�ka
    F6.grid(column=3, row=2)
    F7 = Frame(edycja, borderwidth=2) # 1 strza�ka
    F7.grid(column=1, row=2)
    F8 = Frame(edycja, borderwidth=2) # 3 strza�ka
    F8.grid(column=6, row=2)
    F9 = Frame(edycja, borderwidth=2, relief='ridge')  # Entry nazwisko
    F9.grid(column=5, row=2)
    F10 = Frame(edycja, borderwidth=2)  # Nazwa Imie
    F10.grid(column=4, row=1)
    F11 = Frame(edycja, borderwidth=2)  # Nazwa Nazwisko
    F11.grid(column=5, row=1)
    F12 = Frame(edycja, borderwidth=2)  # Od�wie�
    F12.grid(column=0, row=1)
    F13 = Frame(edycja, borderwidth=2, relief='ridge')  # Zamknij
    F13.grid(column=0, row=3)

    L1 = Label(F1, text="HODOWCY")
    L1.grid()
    E1 = Entry(F2, bd=5)
    E1.grid()
    E2 = Entry(F9,bd=5)
    E2.grid()
    L2= Label(F6, text="--->")
    L2.grid()
    L3 = Label(F7, text="--->")
    L3.grid()
    L4 = Label(F8, text="--->")
    L4.grid()
    L5 = Label(F10, text="Imie")
    L5.grid()
    L5 = Label(F11, text="Nazwisko")
    L5.grid()

    lista=Listbox(F3,width=40,height=16, selectmode=SINGLE)
    for imie in Hodowcy:
        lista.insert(END, imie)
    lista.grid()

    # Definicje przycisk�w
    def wybierz():
        lista1 = int(lista.curselection()[0]) # wy�wietlanie argument�w z listboxa
        dane = Hodowcy[lista1].split()
        E1.insert(INSERT, dane[0])
        E2.insert(INSERT, dane[1])

    def zamknij(): # zmodyfikowa� i doda� do przycisku
        msg =messagebox.askquestion("Wyj�cie","Czy jeste� pewny, �e chcesz zamkn�� to okno?", icon="warning")
        if msg == 'yes':
            edycja.destroy
        else:
            return

    # Tworzenie przyciskow
    btn1 = Button(F4, text = "Wybierz", command=wybierz)
    btn2 = Button(F5, text="Zapisz zmiane")
    btn3 = Button(F12, text="Od�wie�")
    btn4 = Button(F13, text="Zamknij", command=edycja.destroy)


    # Ulozenie przyciskow
    btn1.grid()
    btn2.grid()
    btn3.grid()
    btn4.grid()

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

    F1 = Frame(usun, borderwidth=2, relief='ridge')  # Nazwa Hodowcy
    F1.grid(column=0, row=0)
    F9 = Frame(usun, borderwidth=2, relief="ridge") # od�wie�
    F9.grid(column=0, row=1)
    F2 = Frame(usun, borderwidth=2, relief='ridge')  # Entry imie
    F2.grid(column=4, row=2)
    F3 = Frame(usun, borderwidth=2, relief='ridge')  # Listbox
    F3.grid(column=0, row=2)
    F4 = Frame(usun, borderwidth=2, relief='ridge')  # wybierz
    F4.grid(column=2, row=2)
    F5 = Frame(usun, borderwidth=2, relief='ridge')  # Zapisz
    F5.grid(column=7, row=2)
    F6 = Frame(usun, borderwidth=2)  # 2 strza�ka
    F6.grid(column=3, row=2)
    F7 = Frame(usun, borderwidth=2)  # 1 strza�ka
    F7.grid(column=1, row=2)
    F8 = Frame(usun, borderwidth=2)  # 3 strza�ka
    F8.grid(column=6, row=2)
    F10 = Frame(usun, borderwidth=2, relief='ridge')  # Zamknij
    F10.grid(column=0,row=3)

    L1 = Label(F1, text="Lista Hodowc�w")
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

    #Definicje przycisk�w
    def wybierz():
        lista1 = int(lista.curselection()[0]) # wy�wietlanie argument�w z listboxa
        dane = Hodowcy[lista1].split()

    def usuwanie():
        msg = messagebox.askquestion("Usuwanie", "Czy jeste� pewny, �e chcesz usun�� tego hodowce?", icon="warning")
        if msg == 'yes':
            print("To usunie hodowce")
        else:
            print("To wr�ci do wyboru hodowcy")
            return


    def zamknij(): # zmodyfikowa� i doda� do przycisku
        msg =messagebox.askquestion("Wyj�cie","Czy jeste� pewny, �e chcesz zamkn�� to okno?", icon="warning")
        if msg == 'yes':
            usun.destroy()
        else:
            return

    # Tworzenie przyciskow
    btn1 = Button(F4, text="Wybierz")
    btn2 = Button(F5, text="Usu� Hodowce",command=usuwanie)
    btn3 = Button(F9, text="Od�wie�")
    btn4 = Button(F10, text="Zamknij",command=usun.destroy)

    # Ulozenie przyciskow
    btn1.grid()
    btn2.grid()
    btn3.grid()
    btn4.grid()

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

    F1 = Frame(tree, borderwidth=2, relief='ridge')
    F1.grid(column=0, row=0)
    F2 = Frame(tree, borderwidth=2, relief='ridge')
    F2.grid(column=0, row=1)
    F3 = Frame(tree, borderwidth=2, relief='ridge')
    F3.grid(column=1, row=1)
    F4 = Frame(tree, borderwidth=2, relief='ridge')
    F4.grid(column=2, row=1)

    L1 = Label(F1, text="Lista nazw osobnik�w")
    L1.grid()
    L2 = Label(F3,text="Wybrano osobnika o nazwie:")
    E1 = Entry(F4, bd=5)
    E1.grid()

    show = Listbox(F2, width=60, height=40,selectmode=SINGLE)
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

    F1 = Frame(avg, borderwidth=2, relief='ridge')
    F1.grid(column=0, row=0)
    F2 = Frame(avg, borderwidth=2, relief='ridge')
    F2.grid(column=0, row=1)

    L1 = Label(F1, text="Lista Osobnik�w")
    L1.grid()

    lista = Listbox(F2, width=40, height=16, selectmode=SINGLE)
    for nazwa in Osobniki:
        lista.insert(END, nazwa)
    lista.grid()




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
