# -*- coding: cp1250 -*-
import tkinter as tk
# import baza
import sqlite3
import math
from tkinter import *
from tkinter import ttk
from tkinter import Listbox
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from wspolczynniki import Oblicz
from anytree import Node, RenderTree

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

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Współczynnik imbredu
# Widget
def imbred():
    db_name = "baza.db"

    wsimb = Tk()
    wsimb.geometry("1010x600+0+0")
    wsimb.title("Współczynnik inbredu")
    wsimb_label = Label(wsimb)
    wsimb_label.grid()

    F1 = Frame(wsimb, borderwidth=2)
    F1.grid(column=0, row=0, columnspan=2)
    F2 = Frame(wsimb, borderwidth=2)
    F2.grid(column=0, row=1, columnspan=2)
    F3 = Frame(wsimb, borderwidth=2)
    F3.grid(column=2, row=0, columnspan=2)

    L1 = Label(F1, text="Wybierz osobnika:")
    L1.grid(column=0, row=0, columnspan=3)
    L2 = Label(F2, text="Okienko Wynikowe:")
    L2.grid(column=0, row=1, columnspan=3)

    treeO_wsimb = ttk.Treeview(F1, height=10, columns=('Name', 'Gender', 'Species', 'Breeder'))
    treeO_wsimb.grid(row=7, column=0, columnspan=3)
    treeO_wsimb.heading('#0', text='Nazwa', anchor=W)
    treeO_wsimb.heading('#1', text='Płeć', anchor=W)
    treeO_wsimb.heading('#2', text='Gatunek', anchor=W)
    treeO_wsimb.heading('#3', text='Imię Hodowcy', anchor=W)
    treeO_wsimb.heading('#4', text='Nazwisko Hodowcy', anchor=W)

    # okienko wyświetlające wynik
    wynik_wsimb = Text(F2, width=60, height=12)
    wynik_wsimb.grid()

    # Definicje do przycisków
    def run_query(query, parameters=()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def viewing_record():
        records = treeO_wsimb.get_children()
        for element in records:
            treeO_wsimb.delete(element)
        query = """SELECT nazwa, plec, gatunek, imie, nazwisko FROM osobniki
             JOIN gatunki AS g ON osobniki.id_gat = g.id_gat
             JOIN hodowcy AS h ON osobniki.id_hod = h.id_hod
             ORDER BY id_os DESC"""
        db_rows = run_query(query)
        for row in db_rows:
            treeO_wsimb.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))

    def wynikInbred():
        try:
            treeO_wsimb.item(treeO_wsimb.selection())['values'][0]
        except IndexError as e:
            return
        nzw1 = treeO_wsimb.item(treeO_wsimb.selection())['text']
        pokre = Oblicz()
        wsp = pokre.inbred(nzw1)
        text = 'Osobnik: %(n)s\nJego współczynnik inbredu wynosi: %(wsp)1.3f \n' % {'n': nzw1, 'wsp': wsp}
        wynik_wsimb.delete('1.0', END)
        wynik_wsimb.insert(END, text, 'p')

    def zapisywanieDoPlikuInbred():
        imie = treeO_wsimb.item(treeO_wsimb.selection())['text']
        plik = "Inbred_Osobnika_%(imie)s.txt" % {'imie': imie}
        plik1 = open(plik, 'w')
        obiekt = Oblicz()
        id = obiekt.nazwa_id(imie)
        queryplec = "SELECT plec FROM osobniki WHERE id_os = ?"
        db_rows_plec = run_query(queryplec, (id,))
        for plec in db_rows_plec:
            TestPlec = plec[0]
        querygatunek = """SELECT gatunek FROM osobniki 
                        JOIN gatunki AS g ON osobniki.id_gat = g.id_gat
                        WHERE id_os = ?"""
        db_rows_gatunek = run_query(querygatunek, (id,))
        for gat in db_rows_gatunek:
            TestGat = gat[0]
        queryhodowca = """SELECT imie, nazwisko FROM osobniki 
                        JOIN hodowcy AS h ON osobniki.id_hod = h.id_hod
                        WHERE id_os = ?"""
        db_rows_hodowca = run_query(queryhodowca, (id,))
        for hod in db_rows_hodowca:
            TestHodI = hod[0]
            TestHodN = hod[1]
        TestNazwa = imie
        TestInbred = 0.57
        h = "Wspołczynnik Inbredu \n\nOsobnik:\nNazwa: %(NazwaI)s\nPłeć: %(PłećI)s\nGatunek: %(GatI)s\n\nHodowca:\nImię: %(HodI)s\nNazwisko: %(HodN)s\n\nWspółczynnik Inbredu wynosi: %(WspI)1.3f" \
            % {'NazwaI': TestNazwa, 'PłećI': TestPlec, 'GatI': TestGat, 'HodI': TestHodI, 'HodN': TestHodN , 'WspI': TestInbred}
        plik1.write(h)
        plik1.close()

    # Przyciski
    B1_wsimb = Button(F1, text='Oblicz współczynnik imbredu', command=wynikInbred).grid(column=0, row=10, columnspan=3)
    B2_wsimb = Button(F2, text='Zapisz wynik do pliku tekstowego',
                      command=zapisywanieDoPlikuInbred).grid(column=0, row=4, columnspan=3)
    B3_wsimb = Button(wsimb, text='Zakończ', command=wsimb.destroy).grid(column=0, row=10, columnspan=3)

    viewing_record()

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ---------------------------------------------------------------------------------------------------------------------
# Współczynnik pokrewieństwa
# Widget
def pokrewienstwo():
    db_name = "baza.db"

    wspok = Tk()
    wspok.geometry("1500x600+0+0")
    wspok.title("Współczynnik pokrewieństwa")
    wspok_label = Label(wspok)
    wspok_label.grid()

    F1 = Frame(wspok, borderwidth=2)
    F1.grid(column=0, row=0, columnspan=2)
    F2 = Frame(wspok, borderwidth=2)
    F2.grid(column=0, row=1, columnspan=2)
    F3 = Frame(wspok, borderwidth=2)
    F3.grid(column=2, row=0, columnspan=2)

    L1 = Label(F1, text="Wybierz osobnika 1")
    L1.grid(column=0, row=0, columnspan=3)
    L2 = Label(F2, text="Wybierz osobnika 2")
    L2.grid(column=0, row=1, columnspan=3)
    L3 = Label(F3, text="Okienko Wynikowe")
    L3.grid(column=0, row=2)

    treeO_wspok1 = ttk.Treeview(F1, height=10, columns=('Name', 'Gender', 'Species', 'Breeder'))
    treeO_wspok1.grid(row=7, column=0, columnspan=3)
    treeO_wspok1.heading('#0', text='Nazwa', anchor=W)
    treeO_wspok1.heading('#1', text='Płeć', anchor=W)
    treeO_wspok1.heading('#2', text='Gatunek', anchor=W)
    treeO_wspok1.heading('#3', text='Imię Hodowcy', anchor=W)
    treeO_wspok1.heading('#4', text='Nazwisko Hodowcy', anchor=W)

    treeO_wspok2 = ttk.Treeview(F2, height=10, columns=('Name', 'Gender', 'Species', 'Breeder'))
    treeO_wspok2.grid(row=7, column=0, columnspan=3)
    treeO_wspok2.heading('#0', text='Nazwa', anchor=W)
    # treeO_wspok2.column('#0', minwidth=0, width=400)
    #treeO_wspok2.heading('#1', text='Płeć', anchor=W)
    #treeO_wspok2.heading('#2', text='Gatunek', anchor=W)
    #treeO_wspok2.heading('#3', text='Imię Hodowcy', anchor=W)
    #treeO_wspok2.heading('#4', text='Nazwisko Hodowcy', anchor=W)

    # okienko wyświetlające wynik
    wynik_wspok2 = Text(F3, width=60, height=12)
    wynik_wspok2.grid()

    # Definicje do przycisków
    def run_query(query, parameters=()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def viewing_record1():
        records = treeO_wspok1.get_children()
        for element in records:
            treeO_wspok1.delete(element)
        query = """SELECT nazwa, plec, gatunek, imie, nazwisko FROM osobniki
             JOIN gatunki AS g ON osobniki.id_gat = g.id_gat
             JOIN hodowcy AS h ON osobniki.id_hod = h.id_hod

             ORDER BY id_os DESC"""
        db_rows = run_query(query)
        for row in db_rows:
            treeO_wspok1.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))

    def tree():
        nazwa = treeO_wspok1.item(treeO_wspok1.selection())['text']
        pokre = Oblicz()
        a = pokre.find_parent(nazwa)
        b = pokre.find_grand(nazwa)
        c = pokre.find_pra(nazwa)
        ListTree = []
        for i in a:
            ListTree.append(i)
        for j in b:
            ListTree.append(j)
        for y in c:
            ListTree.append(y)
        treeO_wspok2.option_clear()
        treeO_wspok2.insert('', 0, text="------------------------------")
        for naz in ListTree:
            treeO_wspok2.insert('', 0, text=naz)

    def wynikPokre():
        try:
            nazwa = treeO_wspok1.item(treeO_wspok1.selection())['text']
            nazwa2 = treeO_wspok2.item(treeO_wspok2.selection())['text']
        except IndexError as e:
            return
        pokre = Oblicz()
        wsp = pokre.pokrewienstwo(nazwa, nazwa2)
        text = "Osobnik pierwszy: %(n1)s\nOsobnik drugi: %(n2)s\nWspółczynnik pokrewieństwa tych osobników wynosi: %(p)1.3f" % {'n1': nazwa, 'n2': nazwa2, 'p': wsp}
        wynik_wspok2.delete('1.0', END)
        wynik_wspok2.insert(END, text, 'p')
        wynik_wspok2.insert(END, '\n', ('p'))
        return wsp

    def zapisywanieDoPlikuPokre():
        imie1 = treeO_wspok1.item(treeO_wspok1.selection())['text']
        imie2 = treeO_wspok2.item(treeO_wspok2.selection())['text']
        plik = "Pokrewienstwo_Osobnika_%(imie1)s_oraz_%(imie2)s.txt" % {'imie1': imie1, 'imie2': imie2}
        plik1 = open(plik, 'w')

        obiekt = Oblicz()
        id1 = obiekt.nazwa_id(imie1)
        id2 = obiekt.nazwa_id(imie2)

        queryplec = "SELECT plec FROM osobniki WHERE id_os = ?"
        db_rows_plec1 = run_query(queryplec, (id1,))
        for j in db_rows_plec1:
            plec1 = j[0]

        db_rows_plec2 = run_query(queryplec, (id2,))
        for i in db_rows_plec2:
            plec2 = i[0]

        querygatunek = """SELECT gatunek FROM osobniki 
                                 JOIN gatunki AS g ON osobniki.id_gat = g.id_gat
                                 WHERE id_os = ?"""
        db_rows_gatunek1 = run_query(querygatunek, (id1,))
        for gat in db_rows_gatunek1:
            gat1 = gat[0]

        db_rows_gatunek2 = run_query(querygatunek, (id2,))
        for gatu in db_rows_gatunek2:
            gat2 = gatu[0]

        queryhodowca = """SELECT imie, nazwisko FROM osobniki 
                                 JOIN hodowcy AS h ON osobniki.id_hod = h.id_hod
                                 WHERE id_os = ?"""
        db_rows_hodowca1 = run_query(queryhodowca, (id1,))
        for hod1 in db_rows_hodowca1:
            hodI1 = hod1[0]
            hodN1 = hod1[1]

        db_rows_hodowca2 = run_query(queryhodowca, (id2,))
        for hod2 in db_rows_hodowca2:
            hodI2 = hod2[0]
            hodN2 = hod2[1]

        wynikipokre = wynikPokre()

        pok2 = "Wspólczynnik pokrewieństwa\n\nOsobnik pierwszy: \nNazwa: {nazwa1} \nPłeć: {plec1} \nGatunek: {gat1}\nImię hodowcy: {hodI1}\nNazwisko hodowcy: {hodN1}\n\nOsobnik drugi:\nNazwa: {nazwa2}\nPłeć: {plec2}\nGatunek: {gat2}\nImię hodowcy: {hodI2}\nNazwisko hodowcy: {hodN2}\n\nWspółczynnik pokrewieństwa pomiędzy tymi osobnikami wynosi: {wynik}\n" \
            .format(**{'nazwa1': imie1, 'plec1': plec1, 'gat1': gat1, 'hodI1': hodI1, 'hodN1': hodN1, 'nazwa2': imie2,
                       'plec2': plec2, 'gat2': gat2, 'hodI2': hodI2, 'hodN2': hodN2, 'wynik': wynikipokre})

        plik1.write(pok2)
        plik1.close()

    # Przyciski
    B1 = Button(F1, text='Wyświetl spokrewnione osobniki', command=tree).grid(column=0, row=8, columnspan=3)
    B2 = Button(F2, text='Oblicz współczynnik pokrewieństwa', command=wynikPokre).grid(column=0, row=8, columnspan=3)
    B3 = Button(F3, text='Zapisz wynik do pliku tekstowego',
                command=zapisywanieDoPlikuPokre).grid(column=0, row=4, columnspan=3)
    B4 = Button(wspok, text='Zakończ', command=wspok.destroy).grid(column=1, row=10)

    viewing_record1()
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#-----------------------------------------------------------------------------------------------------------------------
# Współczynnik pokrewieństwa
# Widget
def avgpokrewienstwa():
    db_name = "baza.db"

    avgpok = Tk()
    avgpok.geometry("1010x600+0+0")
    avgpok.title("Średni współczynnik pokrewieństwa")
    avgpok_label = Label(avgpok)
    avgpok_label.grid()

    F1 = Frame(avgpok, borderwidth=2)
    F1.grid(column=0, row=0, columnspan=2)
    #F2 = Frame(avgpok, borderwidth=2)
    #F2.grid(column=0, row=1, columnspan=2)
    F3 = Frame(avgpok, borderwidth=2)
    F3.grid(column=0, row=1, columnspan=2)

    L1 = Label(F1, text="Wybierz osobnika")
    L1.grid(column=0, row=0, columnspan=3)
    #L2 = Label(F2)
    #L2.grid(column=0, row=1, columnspan=3)
    L3 = Label(F3, text="Okienko Wynikowe")
    L3.grid(column=0, row=2)

    treeO_avgpok = ttk.Treeview(F1, height=10, columns=('Name', 'Gender', 'Species', 'Breeder'))
    treeO_avgpok.grid(row=7, column=0, columnspan=3)
    treeO_avgpok.heading('#0', text='Nazwa', anchor=W)
    treeO_avgpok.heading('#1', text='Płeć', anchor=W)
    treeO_avgpok.heading('#2', text='Gatunek', anchor=W)
    treeO_avgpok.heading('#3', text='Imię Hodowcy', anchor=W)
    treeO_avgpok.heading('#4', text='Nazwisko Hodowcy', anchor=W)

    # okienko wyświetlające wynik
    wynik_avgpok = Text(F3, width=100, height=12)
    wynik_avgpok.grid()

    # Definicje przycisków
    def run_query(query, parameters=()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def viewing_record1():
        records = treeO_avgpok.get_children()
        for element in records:
            treeO_avgpok.delete(element)
        query = """SELECT nazwa, plec, gatunek, imie, nazwisko FROM osobniki
             JOIN gatunki AS g ON osobniki.id_gat = g.id_gat
             JOIN hodowcy AS h ON osobniki.id_hod = h.id_hod

             ORDER BY id_os DESC"""
        db_rows = run_query(query)
        for row in db_rows:
            treeO_avgpok.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))

    def tree():
        nazwa = treeO_avgpok.item(treeO_avgpok.selection())['text']
        obiekt = Oblicz()
        a = obiekt.find_parent(nazwa)
        b = obiekt.find_grand(nazwa)
        c = obiekt.find_pra(nazwa)
        ListTree = []
        for i in a:
            ListTree.append(i)
        for j in b:
            ListTree.append(j)
        for y in c:
            ListTree.append(y)
        return ListTree

    def sredni_wspolczynnik_pokrewienstwa():
        nazwa = treeO_avgpok.item(treeO_avgpok.selection())['text']
        obiekt = Oblicz()
        all = tree()
        lista = []
        for i in all:
            RC = obiekt.pokrewienstwo(nazwa, i)
            lista.append(RC)
        suma = sum(lista)
        length = len(all)
        try:
            MK = suma/length
        except ZeroDivisionError:
            MK = 0
        mk = "Osobnik: %(n)s\nŚredni współczynnik pokrewieństwa dla tego osobnika wynosi: %(p)1.3f" % {'n': nazwa ,'p':MK}
        wynik_avgpok.delete('1.0', END)
        wynik_avgpok.insert(END, mk, ('p'))
        wynik_avgpok.insert(END, '\n', ('p'))
        return MK

    def zapisywanieDoPlikuAvgPokre():
        imie = treeO_avgpok.item(treeO_avgpok.selection())['text']
        plik = "AVG_pokrewienstwa_osobnika_%(imie)s.txt" % {'imie': imie}
        obiekt = Oblicz()
        id = obiekt.nazwa_id(imie)
        queryplec = "SELECT plec FROM osobniki WHERE id_os = ?"
        db_rows_plec = run_query(queryplec, (id,))
        for plec in db_rows_plec:
            TestPlec = plec[0]
        querygatunek = """SELECT gatunek FROM osobniki 
                                JOIN gatunki AS g ON osobniki.id_gat = g.id_gat
                                WHERE id_os = ?"""
        db_rows_gatunek = run_query(querygatunek, (id,))
        for gat in db_rows_gatunek:
            TestGat = gat[0]
        queryhodowca = """SELECT imie, nazwisko FROM osobniki 
                                JOIN hodowcy AS h ON osobniki.id_hod = h.id_hod
                                WHERE id_os = ?"""
        db_rows_hodowca = run_query(queryhodowca, (id,))
        for hod in db_rows_hodowca:
            TestHodI = hod[0]
            TestHodN = hod[1]
        TestNazwa = imie
        wynik = sredni_wspolczynnik_pokrewienstwa()
        plik1 = open(plik, 'w')
        pok = "Średni współczynnik pokrewieństwa \n\nOsobnik: \nNazwa: %(NazwaI)s \nPłeć: %(PłećI)s \nGatunek: %(GatI)s \n\nHodowca:\nImię: %(HodI)s \nNazwisko: %(HodN)s\n\nŚredni współczynnik pokrewieństwa wynosi: %(WspI)1.3f" \
              % {'NazwaI': TestNazwa, 'PłećI': TestPlec, 'GatI': TestGat, 'HodI': TestHodI, 'HodN': TestHodN , 'WspI': wynik}
        plik1.write(pok)
        plik1.close()

    # Przyciski
    B1 = Button(F1, text='Oblicz średni wspólczynnik pokrewieństwa',
                command=sredni_wspolczynnik_pokrewienstwa).grid(column=0, row=8, columnspan=3)
    B2 = Button(F3, text='Zapisz wynik do pliku tekstowego',
                command=zapisywanieDoPlikuAvgPokre).grid(column=0, row=4,
                                                                                              columnspan=3)
    B3 = Button(avgpok, text='Zakończ', command=avgpok.destroy).grid(column=0, row=10, columnspan=3)

    viewing_record1()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#-----------------------------------------------------------------------------------------------------------------------
# Współczynnik pokrewieństwa
# Widget
def showTree():
    db_name = "baza.db"

    treeview = Tk()
    treeview.geometry("1500x600+0+0")
    treeview.title("Drzewo genealogiczne")
    treeview_label = Label(treeview)
    treeview_label.grid()

    F1 = Frame(treeview, borderwidth=2)
    F1.grid(column=0, row=0, columnspan=2)
    F2 = Frame(treeview, borderwidth=2)
    F2.grid(column=0, row=1, columnspan=2)
    F3 = Frame(treeview, borderwidth=2)
    F3.grid(column=2, row=0, columnspan=2)

    L1 = Label(F1, text="Wybierz osobnika")
    L1.grid(column=0, row=0, columnspan=3)
    L2 = Label(F2)
    L2.grid(column=0, row=0, columnspan=3, rowspan=2)
    L3 = Label(F3)
    L3.grid(column=0, row=2, rowspan=2)

    treeO_treeshow = ttk.Treeview(F1, height=10, columns=('Name', 'Gender', 'Species', 'Breeder'))
    treeO_treeshow.grid(row=7, column=0, columnspan=3)
    treeO_treeshow.heading('#0', text='Nazwa', anchor=W)
    treeO_treeshow.heading('#1', text='Płeć', anchor=W)
    treeO_treeshow.heading('#2', text='Gatunek', anchor=W)
    treeO_treeshow.heading('#3', text='Imię Hodowcy', anchor=W)
    treeO_treeshow.heading('#4', text='Nazwisko Hodowcy', anchor=W)

    treeO_avgpok = Text(F3, width=60, height=30)
    treeO_avgpok.grid(row=7, column=0, columnspan=3)

    # Definicje przycisków
    def run_query(query, parameters=()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def viewing_record():
        records = treeO_treeshow.get_children()
        for element in records:
            treeO_treeshow.delete(element)
        query = """SELECT nazwa, plec, gatunek, imie, nazwisko FROM osobniki
             JOIN gatunki AS g ON osobniki.id_gat = g.id_gat
             JOIN hodowcy AS h ON osobniki.id_hod = h.id_hod

             ORDER BY id_os DESC"""
        db_rows = run_query(query)
        for row in db_rows:
            treeO_treeshow.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))

    def show():
        nazwaP1 = treeO_treeshow.item(treeO_treeshow.selection())['text']
        obiekt = Oblicz()
        if nazwaP1:
            name1 = obiekt.find_parent(nazwaP1)  # rodzice
            if len(name1) > 1:
                nazwaP2 = name1[0]  # matka
                nazwaP3 = name1[1]  # ojciec
                name2 = obiekt.find_parent(nazwaP2)  # dziadkowie
                name3 = obiekt.find_parent(nazwaP3)  # dziadkowie
                if len(name2) > 1:
                    nazwaP4 = name2[0]  # babcia
                    nazwaP5 = name2[1]  # dziadek
                    name4 = obiekt.find_parent(nazwaP4)  # pradziadkowie
                    name5 = obiekt.find_parent(nazwaP5)  # pradziadkowie
                    if len(name4) > 1:
                        nazwaP8 = name4[0]  # prababka
                        nazwaP9 = name4[1]  # pradziad
                        name8 = obiekt.find_parent(nazwaP8)  # prapra
                        name9 = obiekt.find_parent(nazwaP9)  # prapra
                        if len(name8) > 1:
                            nazwaP16 = name8[0]
                            nazwaP17 = name8[1]
                        elif len(name8) == 1:
                            nazwaP16 = name8[0]
                        else:
                            pass
                        if len(name9) > 1:
                            nazwaP18 = name9[0]
                            nazwaP19 = name9[1]
                        elif len(name9) == 1:
                            nazwaP18 = name9[0]
                        else:
                            pass
                    elif len(name4) == 1:
                        nazwaP8 = name4[0]  # prababka
                        name8 = obiekt.find_parent(nazwaP8)  # prapra
                        if len(name8) > 1:
                            nazwaP16 = name8[0]
                            nazwaP17 = name8[1]
                        elif len(name8) == 1:
                            nazwaP16 = name8[0]
                        else:
                            pass
                    else:
                        pass
                    if len(name5) > 1:
                        nazwaP10 = name5[0]  # prababka
                        nazwaP11 = name5[1]  # pradziad
                        name10 = obiekt.find_parent(nazwaP10)  # prapra
                        name11 = obiekt.find_parent(nazwaP11)  # prapra
                        if len(name10) > 1:
                            nazwaP20 = name10[0]
                            nazwaP21 = name10[1]
                        elif len(name10) == 1:
                            nazwaP20 = name10[0]
                        else:
                            pass
                        if len(name11) > 1:
                            nazwaP22 = name11[0]
                            nazwaP23 = name11[1]
                        elif len(name11) == 1:
                            nazwaP22 = name11[0]
                        else:
                            pass
                    elif len(name5) == 1:
                        nazwaP10 = name5[0]  # prababka
                        name10 = obiekt.find_parent(nazwaP10)  # prapra
                        if len(name10) > 1:
                            nazwaP20 = name10[0]
                            nazwaP21 = name10[1]
                        elif len(name10) == 1:
                            nazwaP20 = name10[0]
                        else:
                            pass
                    else:
                        pass
                elif len(name2) == 1:
                    nazwaP5 = name2[0]  # babcia
                    name4 = obiekt.find_parent(nazwaP4)  # pradziadkowie
                else:
                    pass
                if len(name3) > 1:
                    nazwaP6 = name3[0]  # babcia
                    nazwaP7 = name3[1]  # dziadek
                    name6 = obiekt.find_parent(nazwaP6)  # pradziadkowie
                    name7 = obiekt.find_parent(nazwaP7)  # pradziadkowie
                    if len(name6) > 1:
                        nazwaP12 = name6[0]  # prababka
                        nazwaP13 = name6[1]  # pradziad
                        name12 = obiekt.find_parent(nazwaP12)  # prapra
                        name13 = obiekt.find_parent(nazwaP13)  # prapra
                        if len(name12) > 1:
                            nazwaP24 = name12[0]
                            nazwaP25 = name12[1]
                        elif len(name12) == 1:
                            nazwaP24 = name12[0]
                        else:
                            pass
                        if len(name13) > 1:
                            nazwaP26 = name13[0]
                            nazwaP27 = name13[1]
                        elif len(name13) == 1:
                            nazwaP26 = name13[0]
                        else:
                            pass
                    elif len(name6) == 1:
                        nazwaP12 = name6[0]  # prababka
                        nazwaP12 = name6[0]  # prababka
                        name12 = obiekt.find_parent(nazwaP12)  # prapra
                        if len(name12) > 1:
                            nazwaP24 = name12[0]
                            nazwaP25 = name12[1]
                        elif len(name12) == 1:
                            nazwaP24 = name12[0]
                        else:
                            pass
                    else:
                        pass
                    if len(name7) > 1:
                        nazwaP14 = name7[0]  # prababka
                        nazwaP15 = name7[1]  # pradziad
                        name14 = obiekt.find_parent(nazwaP14)  # prapra
                        name15 = obiekt.find_parent(nazwaP15)  # prapra
                        if len(name14) > 1:
                            nazwaP28 = name14[0]
                            nazwaP29 = name14[1]
                        elif len(name14) == 1:
                            nazwaP28 = name14[0]
                        else:
                            pass
                        if len(name15) > 1:
                            nazwaP30 = name15[0]
                            nazwaP31 = name15[1]
                        elif len(name15) == 1:
                            nazwaP30 = name15[0]
                        else:
                            pass
                    elif len(name7) == 1:
                        nazwaP14 = name7[0]  # prababka
                        name14 = obiekt.find_parent(nazwaP14)  # prapra
                        if len(name14) > 1:
                            nazwaP28 = name14[0]
                            nazwaP29 = name14[1]
                        elif len(name14) == 1:
                            nazwaP28 = name14[0]
                        else:
                            pass
                    else:
                        pass
                elif len(name3) == 1:
                    nazwaP6 = name3[0]  # babcia
                    name6 = obiekt.find_parent(nazwaP6)  # pradziadkowie
                else:
                    pass
            elif len(name1) == 1:
                nazwaP2 = name1[0]  # matka
                name2 = obiekt.find_parent(nazwaP2)  # dziadkowie
                if len(name2) > 1:
                    nazwaP4 = name2[0]  # babcia
                    nazwaP5 = name2[1]  # dziadek
                    name4 = obiekt.find_parent(nazwaP4)  # pradziadkowie
                    name5 = obiekt.find_parent(nazwaP5)  # pradziadkowie
                    if len(name4) > 1:
                        nazwaP8 = name4[0]  # prababka
                        nazwaP9 = name4[1]  # pradziad
                        name8 = obiekt.find_parent(nazwaP8)  # prapra
                        name9 = obiekt.find_parent(nazwaP9)  # prapra
                        if len(name8) > 1:
                            nazwaP16 = name8[0]
                            nazwaP17 = name8[1]
                        elif len(name8) == 1:
                            nazwaP16 = name8[0]
                        else:
                            pass
                        if len(name9) > 1:
                            nazwaP18 = name9[0]
                            nazwaP19 = name9[1]
                        elif len(name9) == 1:
                            nazwaP18 = name9[0]
                        else:
                            pass
                    elif len(name4) == 1:
                        nazwaP8 = name4[0]  # prababka
                        name8 = obiekt.find_parent(nazwaP8)  # prapra
                        if len(name8) > 1:
                            nazwaP16 = name8[0]
                            nazwaP17 = name8[1]
                        elif len(name8) == 1:
                            nazwaP16 = name8[0]
                        else:
                            pass
                    else:
                        pass
                    if len(name5) > 1:
                        nazwaP10 = name5[0]  # prababka
                        nazwaP11 = name5[1]  # pradziad
                        name10 = obiekt.find_parent(nazwaP10)  # prapra
                        name11 = obiekt.find_parent(nazwaP11)  # prapra
                        if len(name10) > 1:
                            nazwaP20 = name10[0]
                            nazwaP21 = name10[1]
                        elif len(name10) == 1:
                            nazwaP20 = name10[0]
                        else:
                            pass
                        if len(name11) > 1:
                            nazwaP22 = name11[0]
                            nazwaP23 = name11[1]
                        elif len(name11) == 1:
                            nazwaP22 = name11[0]
                        else:
                            pass
                    elif len(name5) == 1:
                        nazwaP10 = name5[0]  # prababka
                        name10 = obiekt.find_parent(nazwaP10)  # prapra
                        if len(name10) > 1:
                            nazwaP20 = name10[0]
                            nazwaP21 = name10[1]
                        elif len(name10) == 1:
                            nazwaP20 = name10[0]
                        else:
                            pass
                    else:
                        pass
                elif len(name2) == 1:
                    nazwaP4 = name2[0]  # babcia
                    name4 = obiekt.find_parent(nazwaP4)  # pradziadkowie
                    if len(name4) > 1:
                        nazwaP8 = name4[0]  # prababka
                        nazwaP9 = name4[1]  # pradziad
                        name8 = obiekt.find_parent(nazwaP8)  # prapra
                        name9 = obiekt.find_parent(nazwaP9)  # prapra
                        if len(name8) > 1:
                            nazwaP16 = name8[0]
                            nazwaP17 = name8[1]
                        elif len(name8) == 1:
                            nazwaP16 = name8[0]
                        else:
                            pass
                        if len(name9) > 1:
                            nazwaP18 = name9[0]
                            nazwaP19 = name9[1]
                        elif len(name9) == 1:
                            nazwaP18 = name9[0]
                        else:
                            pass
                    elif len(name4) == 1:
                        nazwaP8 = name4[0]  # prababka
                        name8 = obiekt.find_parent(nazwaP8)  # prapra
                        if len(name8) > 1:
                            nazwaP16 = name8[0]
                            nazwaP17 = name8[1]
                        elif len(name8) == 1:
                            nazwaP16 = name8[0]
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
        try:
            P1 = Node(nazwaP1)
            P2 = Node(nazwaP2, parent=P1)
            P3 = Node(nazwaP3, parent=P1)
            P4 = Node(nazwaP4, parent=P2)
            P5 = Node(nazwaP5, parent=P2)
            P6 = Node(nazwaP6, parent=P3)
            P7 = Node(nazwaP7, parent=P3)
            P8 = Node(nazwaP8, parent=P4)
            P9 = Node(nazwaP9, parent=P4)
            P10 = Node(nazwaP10, parent=P5)
            P11 = Node(nazwaP11, parent=P5)
            P12 = Node(nazwaP12, parent=P6)
            P13 = Node(nazwaP13, parent=P6)
            P14 = Node(nazwaP14, parent=P7)
            P15 = Node(nazwaP15, parent=P7)
            P16 = Node(nazwaP16, parent=P8)
            P17 = Node(nazwaP17, parent=P8)
            P18 = Node(nazwaP18, parent=P9)
            P19 = Node(nazwaP19, parent=P9)
            P20 = Node(nazwaP20, parent=P10)
            P21 = Node(nazwaP21, parent=P10)
            P22 = Node(nazwaP22, parent=P11)
            P23 = Node(nazwaP23, parent=P11)
            P24 = Node(nazwaP24, parent=P12)
            P25 = Node(nazwaP25, parent=P12)
            P26 = Node(nazwaP26, parent=P13)
            P27 = Node(nazwaP27, parent=P13)
            P28 = Node(nazwaP28, parent=P14)
            P29 = Node(nazwaP29, parent=P14)
            P30 = Node(nazwaP30, parent=P15)
            P31 = Node(nazwaP31, parent=P15)
        except:
            'bład'
        treeO_avgpok.insert(END, '----------------------------------\n', ('p'))
        for pre, fill, node in RenderTree(P1):
            a = ("%s%s\n" % (pre, node.name))
            # a=print("{1} {2}".format(pre[0]), node.name[0])
            treeO_avgpok.insert(END, a)

    # Przyciski
    B1 = Button(F2, text='Wyświetl drzewo dla wybranego osobnika', command=show).grid(column=0, row=0,
                                                                                              columnspan=3, rowspan=2)
    #B2 = Button(F3, text='Zapisz wynik do pliku tekstowego',
    #            command=zapisywanieDoPlikuPokre("Wspolczynnik_Pokrewienstawa.txt", pok)).grid(column=0, row=4,
    #                                                                                          columnspan=3)
    B3 = Button(treeview, text='Zakończ', command=treeview.destroy).grid(column=1, row=10)

    viewing_record()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#######################################################################################################################
# okno root
root = Tk()  # root widget - musi zostać stworzony przed innymi widgetami
root.geometry("1000x600+0+0")
root.title("Heredity")  # tytuł naszej tabeli root

# Menu
menu = Menu(root)
root.config(menu=menu)
filemenu = tk.Menu(menu)

# Plik
menu.add_cascade(label="Plik", menu=filemenu)
filemenu.add_command(label="Otwórz baze", command=baseopen)
filemenu.add_command(label="Zamknij baze", command=baseclose)
filemenu.add_separator()
filemenu.add_command(label="Zamknij program", command=root.destroy)

# Obliczenia
oblicz = Menu(menu)
menu.add_cascade(label="Współczynniki", menu=oblicz)
oblicz.add_command(label="Współczynnik inbredu", command=imbred)
oblicz.add_command(label="Współczynnik pokrewieństa", command=pokrewienstwo)
oblicz.add_command(label="Średni współczynnik pokrewieństwa", command=avgpokrewienstwa)

# Drzewo
drzewo = Menu(menu)
menu.add_cascade(label= "Drzewo", menu=drzewo)
drzewo.add_command(label="Wyświetl drzewo genealogiczne", command=showTree)

# =================================ZAKLADKI==========================================
class RootApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(NoteBook)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

class NoteBook(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.notebook = ttk.Notebook()
        self.tab1 = Tab1(self.notebook)
        self.tab2 = Tab2(self.notebook)
        self.tab3 = Tab3(self.notebook)
        self.notebook.add(self.tab1, text="Hodowcy")
        self.notebook.add(self.tab2, text="Gatunki")
        self.notebook.add(self.tab3, text="Osobniki")
        self.notebook.grid()

    def switch_tab1(self, frame_class):
        new_frame = frame_class(self.notebook)
        self.tab1.destroy()
        self.tab1 = new_frame

# Zakładka 1
class Tab1(Frame):
    db_name = "baza.db"

    def __init__(self, master):
        Frame.__init__(self, master)
        self._frame = None
        self.switch_frame(Hodowcy)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

# Wygląd Zakładki 1
class Hodowcy(Frame):
    db_name = "baza.db"

    def __init__(self, master):
        Frame.__init__(self, master)

        frame = LabelFrame(self.master, text="Dodaj Hodowce")
        frame.grid(row=0, column=0, columnspan=2)

        Label(frame, text="Imię: ").grid(row=1, column=0, columnspan=2)
        self.fname = Entry(frame)
        self.fname.grid(row=1, column=2)

        Label(frame, text="Nazwisko: ").grid(row=2, column=1)
        self.sname = Entry(frame)
        self.sname.grid(row=2, column=2)

        ttk.Button(frame, text='Dodaj Hodowce', command=self.adding).grid(row=3, column=2)
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0)

        self.treeH = ttk.Treeview(master, height=10, columns=2)
        self.treeH.grid(row=4, column=0, columnspan=2)
        self.treeH.grid(row=4, column=0, columnspan=2)
        self.treeH.heading('#0', text='ID', anchor=W)
        self.treeH.heading(2, text='Imię', anchor=W)

        ttk.Button(master, text='Usuń Hodowce', command=self.deleting).grid(row=5, column=0)
        ttk.Button(master, text='Edytuj Hodowce', command=self.editing).grid(row=5, column=1)

        self.viewing_record()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def viewing_record(self):
        records = self.treeH.get_children()
        for element in records:
            self.treeH.delete(element)
        query = 'SELECT * FROM hodowcy ORDER BY id_hod DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.treeH.insert('', 0, text=row[1], values=row[2])

    def lenrecord(self):
        query = 'SELECT * FROM hodowcy ORDER BY id_hod DESC'
        db_rows = self.run_query(query)
        lista = []
        for row in db_rows:
            lista.append(row)
        return len(lista)

    def validation(self):
        return len(self.fname.get()) != 0 and len(self.sname.get()) != 0

    def adding(self):
        if self.validation():
            l = self.lenrecord()
            query = 'INSERT INTO hodowcy VALUES (?, ?, ?)'
            parameters = (l + 1, self.fname.get(), self.sname.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Rekord {} został dodany'.format(self.fname.get())
            self.fname.delete(0, END)
            self.sname.delete(0, END)
        else:
            self.message['text'] = 'Uzupełnij wszystkie pola!'
        self.viewing_record()

    def deleting(self):
        self.message['text'] = ''
        try:
            self.treeH.item(self.treeH.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Proszę, wybierz rekod!'
            return

        self.message['text'] = ''
        name = self.treeH.item(self.treeH.selection())['text']

        query1 = 'SELECT id_hod FROM hodowcy WHERE  imie = ?'  # znalezienie id hodowcy
        db_rows = self.run_query(query1, (name,))
        for row in db_rows:
            id = row

        query2 = 'DELETE FROM OSOBNIKI_HODOWCY WHERE id_hod = ?'  # usunięcie hodowcy z relacji osobniki_hodowcy
        self.run_query(query2, id)

        query3 = 'DELETE FROM OSOBNIKI WHERE id_hod = ?'  # usunięcie hodowcy z relacji osobniki
        self.run_query(query3, id)

        query = 'DELETE FROM hodowcy WHERE imie = ?'  # usuniecie hodowcy z relacji hodowcy
        self.run_query(query, (name,))

        self.message['text'] = 'Rekord {} został usunięty.'.format(name)
        self.viewing_record()

    def editing(self):
        self.message['text'] = ''
        try:
            self.treeH.item(self.treeH.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Proszę, wybierz rekord!'
            return
        old_name = self.treeH.item(self.treeH.selection())['text']
        old_second_name = self.treeH.item(self.treeH.selection())['values'][0]

        self.edit_master = Toplevel()
        self.edit_master.title('Edycja')

        Label(self.edit_master, text='Stare imię:').grid(row=0, column=1)
        Entry(self.edit_master, textvariable=StringVar(self.edit_master, value=old_name), state='readonly').grid(
            row=0, column=2)
        Label(self.edit_master, text='Nowe imię:').grid(row=1, column=1)
        new_name = Entry(self.edit_master)
        new_name.grid(row=1, column=2)

        Label(self.edit_master, text='Stare nazwisko:').grid(row=2, column=1)
        Entry(self.edit_master, textvariable=StringVar(self.edit_master, value=old_second_name),
              state='readonly').grid(row=2, column=2)
        Label(self.edit_master, text='Nowe nazwisko:').grid(row=3, column=1)
        new_second_name = Entry(self.edit_master)
        new_second_name.grid(row=3, column=2)

        Button(self.edit_master, text='Zapisz zmiany',
               command=lambda: self.edit_records(new_name.get(), old_name, new_second_name.get(),
                                                 old_second_name)).grid(row=4, column=2, sticky=W)
        self.edit_master.mainloop()

    def edit_records(self, new_name, name, new_second_name, old_second_name):
        query = 'UPDATE hodowcy SET imie = ?, nazwisko = ? WHERE imie = ? AND nazwisko = ?'
        parameters = (new_name, new_second_name, name, old_second_name)
        self.run_query(query, parameters)
        self.edit_master.destroy()
        self.message['text'] = 'Rekord {} zmieniony.'.format(name)
        self.viewing_record()

# Zakładka 2
class Tab2(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self._frame = None
        self.switch_frame(Gatunki)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

# Wygląd zakładki 2
class Gatunki(Frame):
    db_name = "baza.db"

    def __init__(self, master):
        Frame.__init__(self, master)

        frame = LabelFrame(self.master, text="Dodaj Gatunek")
        frame.grid(row=0, column=0, columnspan=2)

        Label(frame, text="Nazwa: ").grid(row=1, column=1)
        self.name = Entry(frame)
        self.name.grid(row=1, column=2)

        ttk.Button(frame, text='Dodaj Gatunek', command=self.adding).grid(row=3, column=2)
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2)

        self.treeG = ttk.Treeview(master, height=10, columns='')
        self.treeG.grid(row=4, column=0, columnspan=2)
        self.treeG.heading('#0', text='Nazwa Gatunku', anchor=W)

        ttk.Button(master, text='Usuń Gatunek', command=self.deleting).grid(row=5, column=0)
        ttk.Button(master, text='Edytuj Gatunek', command=self.editing).grid(row=5, column=1, columnspan=2)

        self.viewing_record()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def viewing_record(self):
        records = self.treeG.get_children()
        for element in records:
            self.treeG.delete(element)
        query = 'SELECT gatunek FROM gatunki ORDER BY id_gat DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.treeG.insert('', 0, text=row[0])

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
            name = self.name.get()
            lista = []
            query1 = 'SELECT gatunek FROM gatunki'
            db_rows = self.run_query(query1)
            for row in db_rows:
                lista.append(row[0])
            if name in lista:
                self.message['text'] = 'Nazwa istnieje w bazie!'
            else:
                query = 'INSERT INTO gatunki VALUES (?, ?)'
                parameters = (l + 1, name)
                self.run_query(query, parameters)
                self.message['text'] = 'Rekord {} zostął dodany.'.format(self.name.get())
                self.name.delete(0, END)
        else:
            self.message['text'] = 'Nazwa gatunku jest pusta!'
        self.viewing_record()

    def deleting(self):
        self.message['text'] = ''
        try:
            self.treeG.item(self.treeG.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Proszę, wybierz rekord.'
            return

        self.message['text'] = ''
        name = self.treeG.item(self.treeG.selection())['text']

        query1 = 'SELECT id_gat FROM gatunki WHERE  gatunek = ?'  # znalezienie id hodowcy
        db_rows = self.run_query(query1, (name,))
        for row in db_rows:
            id = row

        query3 = 'DELETE FROM OSOBNIKI WHERE id_gat = ?'  # usunięcie hodowcy z relacji osobniki
        self.run_query(query3, id)

        query = 'DELETE FROM gatunki WHERE gatunek = ?'
        self.run_query(query, (name,))
        self.message['text'] = 'Gatunek {} został usunięty.'.format(name)
        self.viewing_record()

    def editing(self):
        self.message['text'] = ''
        try:
            self.treeG.item(self.treeG.selection())['text']
        except IndexError as e:
            self.message['text'] = 'Proszę, wybierz gatunek.'
            return
        old_name = self.treeG.item(self.treeG.selection())['text']

        self.edit_master = Toplevel()
        self.edit_master.title('Edytowanie')

        Label(self.edit_master, text='Stara nazwa:').grid(row=0, column=1)
        Entry(self.edit_master, textvariable=StringVar(self.edit_master, value=old_name), state='readonly').grid(row=0,
                                                                                                            column=2)
        Label(self.edit_master, text='Nowa nazwa:').grid(row=1, column=1)
        new_name = Entry(self.edit_master)
        new_name.grid(row=1, column=2)

        Button(self.edit_master, text='Zapisz',
               command=lambda: self.edit_records(new_name.get(), old_name)).grid(row=4, column=2, sticky=W)
        self.edit_master.mainloop()

    def edit_records(self, new_name, name):
        query = 'UPDATE gatunki SET gatunek = ? WHERE gatunek = ?'
        parameters = (new_name, name)
        self.run_query(query, parameters)
        self.edit_master.destroy()
        self.message['text'] = 'Nazwa gatunku {} została zmieniona.'.format(name)
        self.viewing_record()

# Zakładka 3
class Tab3(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self._frame = None
        self.switch_frame(Osobniki)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

# Wygląd zakładki 3
class Osobniki(Frame):
    db_name = "baza.db"

    def __init__(self, master):
        Frame.__init__(self, master)

        frame = LabelFrame(self.master, text="Dodaj Osobnika")
        frame.grid(row=0, column=1)

        Label(frame, text="Nazwa: ").grid(row=1, column=1)
        self.name = Entry(frame)
        self.name.grid(row=1, column=2)

        Label(frame, text="Płeć: ").grid(row=2, column=1)
        self.gender = Entry(frame)
        self.gender.grid(row=2, column=2)

        Label(frame, text="Gatunek: ").grid(row=3, column=1)
        self.species = Entry(frame)
        self.species.grid(row=3, column=2)

        Label(frame, text="Imię Hodowcy: ").grid(row=4, column=1)
        self.fbreeder = Entry(frame)
        self.fbreeder.grid(row=4, column=2)

        Label(frame, text="Nazwisko Hodowcy: ").grid(row=5, column=1)
        self.lbreeder = Entry(frame)
        self.lbreeder.grid(row=5, column=2)

        ttk.Button(frame, text='Dodaj nowego osobnika', command=self.adding).grid(row=6, column=1, columnspan=2)
        self.message = Label(text='', fg='red')
        self.message.grid(row=6, column=0)

        self.treeO = ttk.Treeview(master, height=10, columns=('Name', 'Gender', 'Species', 'Breeder'))
        self.treeO.grid(row=7, column=0, columnspan=3)
        self.treeO.heading('#0', text='Nazwa', anchor=W)
        self.treeO.heading('#1', text='Płeć', anchor=W)
        self.treeO.heading('#2', text='Gatunek', anchor=W)
        self.treeO.heading('#3', text='Imię Hodowcy', anchor=W)
        self.treeO.heading('#4', text='Nazwisko Hodowcy', anchor=W)

        ttk.Button(master, text='Usuń osobnika z bazy', command=self.deleting).grid(row=8, column=0, columnspan=2)
        ttk.Button(master, text='Edytuj osobnika', command=self.editing).grid(row=8, column=1, columnspan=2)

        self.viewing_record()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def viewing_record(self):
        records = self.treeO.get_children()
        for element in records:
            self.treeO.delete(element)
        query = """SELECT nazwa, plec, gatunek, imie, nazwisko FROM osobniki
         JOIN gatunki AS g ON osobniki.id_gat = g.id_gat
         JOIN hodowcy AS h ON osobniki.id_hod = h.id_hod
         ORDER BY id_os DESC"""
        db_rows = self.run_query(query)
        for row in db_rows:
            self.treeO.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))

    def lenrecord(self):
        query = 'SELECT * FROM osobniki ORDER BY id_os DESC'
        db_rows = self.run_query(query)
        lista = []
        for row in db_rows:
            lista.append(row)
        return len(lista)

    def validation(self):
        return len(self.name.get()) != 0 and len(self.gender.get()) != 0 and len(self.species.get()) != 0 and len(
            self.fbreeder.get()) != 0 and len(self.lbreeder.get()) != 0

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
                    parameters = (l + 1, self.name.get(), self.gender.get(), id1, id2)
                    self.run_query(query, parameters)
                    self.message['text'] = 'Rekord {} został dodany.'.format(self.name.get())
                    self.name.delete(0, END)
                    self.gender.delete(0, END)
                    self.species.delete(0, END)
                    self.fbreeder.delete(0, END)
                    self.lbreeder.delete(0, END)
                else:
                    self.message['text'] = 'Hodowca nie istnieje'
            else:
                self.message['text'] = 'Brak takiego gatunku w bazie.'

        else:
            self.message['text'] = 'Uzupełnij wszystkie pola.'
        self.viewing_record()

    def deleting(self):
        self.message['text'] = ''
        try:
            self.treeO.item(self.treeO.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Proszę, wybierz rekord!'
            return

        self.message['text'] = ''
        name = self.treeO.item(self.treeO.selection())['text']

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
        self.run_query(query, (name,))
        self.message['text'] = 'Rekord {} został usunięty.'.format(name)
        self.viewing_record()

    def editing(self):
        self.message['text'] = ''
        try:
            self.treeO.item(self.treeO.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Proszę, wybierz rekord!'
            return
        old_name = self.treeO.item(self.treeO.selection())['text']
        old_gender = self.treeO.item(self.treeO.selection())['values'][0]
        old_species = self.treeO.item(self.treeO.selection())['values'][1]
        old_fbreeder = self.treeO.item(self.treeO.selection())['values'][2]
        old_lbreeder = self.treeO.item(self.treeO.selection())['values'][3]

        self.edit_master = Toplevel()
        self.edit_master.title('Edycja')

        Label(self.edit_master, text='Stara nazwa:').grid(row=0, column=1)
        Entry(self.edit_master, textvariable=StringVar(self.edit_master, value=old_name), state='readonly').grid(row=0,
                                                                                                            column=2)
        Label(self.edit_master, text='Nowa nazwa:').grid(row=1, column=1)
        new_name = Entry(self.edit_master)
        new_name.grid(row=1, column=2)

        Label(self.edit_master, text='Wcześniejsza płeć:').grid(row=2, column=1)
        Entry(self.edit_master, textvariable=StringVar(self.edit_master, value=old_gender), state='readonly').grid(
            row=2, column=2)
        Label(self.edit_master, text='Nowa płeć:').grid(row=3, column=1)
        new_gender = Entry(self.edit_master)
        new_gender.grid(row=3, column=2)

        Label(self.edit_master, text='Wcześniejszy gatunek:').grid(row=4, column=1)
        Entry(self.edit_master, textvariable=StringVar(self.edit_master, value=old_species), state='readonly').grid(
            row=4,
            column=2)
        Label(self.edit_master, text='Obecny gatunek:').grid(row=5, column=1)
        new_species = Entry(self.edit_master)
        new_species.grid(row=5, column=2)

        Label(self.edit_master, text='Stare imie hodowcy:').grid(row=6, column=1)
        Entry(self.edit_master, textvariable=StringVar(self.edit_master, value=old_fbreeder), state='readonly').grid(
            row=6,
            column=2)
        Label(self.edit_master, text='Nowe imie hodowcy:').grid(row=7, column=1)
        new_fbreeder = Entry(self.edit_master)
        new_fbreeder.grid(row=7, column=2)

        Label(self.edit_master, text='Stare nazwisko hodowcy:').grid(row=8, column=1)
        Entry(self.edit_master, textvariable=StringVar(self.edit_master, value=old_lbreeder), state='readonly').grid(
            row=8,
            column=2)
        Label(self.edit_master, text='Nowe nazwisko hodowcy:').grid(row=9, column=1)
        new_lbreeder = Entry(self.edit_master)
        new_lbreeder.grid(row=9, column=2)

        Button(self.edit_master, text='Zapisz zmiany',
               command=lambda: self.edit_records(new_name.get(), old_name,
                                                 new_gender.get(), old_gender,
                                                 new_species.get(), old_species,
                                                 new_fbreeder.get(), old_fbreeder,
                                                 new_lbreeder.get(), old_lbreeder)).grid(row=10, column=2, sticky=W)
        self.edit_master.mainloop()

    def edit_records(self, new_name, old_name, new_gender, old_gender, new_species, old_species, new_fbreeder,
                     old_fbreeder, new_lbreeder, old_lbreeder):
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
        parameters = (
            new_name, new_gender, new_id_species, new_id_breeder, old_name, old_gender, old_id_species, old_id_breeder)
        self.run_query(query, parameters)
        self.edit_master.destroy()
        self.message['text'] = 'Rekord {} został zmieniony.'.format(old_name)
        self.viewing_record()

# =====================KONIEC_ZAKLADEK================================================================================
if __name__ == "__main__":
    Root = RootApp()
    Root.mainloop()

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
