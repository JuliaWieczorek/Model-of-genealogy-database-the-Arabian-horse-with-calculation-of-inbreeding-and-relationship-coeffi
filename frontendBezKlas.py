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
    wsimb.geometry("1000x600+0+0")
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
        text = 'Osobnik: %(n)s\nJego współczynnik inbredu wynosi: %(wsp)f \n' % {'n': nzw1, 'wsp': wsp}
        wynik_wsimb.delete('1.0', END)
        wynik_wsimb.insert(END, text, 'p')

    def zapisywanieDoPlikuInbred():
        imie = treeO_wsimb.item(treeO_wsimb.selection())['text']
        plik = "Inbred_Osobnika_%(imie)s.txt" % {'imie': imie}
        plik1 = open(plik, 'w')
        TestNazwa = imie
        TestPlec = 'Samiec'
        TestGat = 'Pies'
        TestHod = 'Bogdan Zbychu'
        TestInbred = 0.57
        h = "Wspołczynnik Inbredu \n\nNazwa osobnika: %(NazwaI)s\nPłeć osobnika: %(PłećI)s\nGatunek osobnika: %(GatI)s\nHodowca osobnika: %(HodI)s\nWspółczynnik Inbredu wynosi: %(WspI)f" \
            % {'NazwaI': TestNazwa, 'PłećI': TestPlec, 'GatI': TestGat, 'HodI': TestHod, 'WspI': TestInbred}
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
    wspok.geometry("1000x600+0+0")
    wspok.title("Współczynnik pokrewieństwa")
    wspok_label = Label(wspok)
    wspok_label.grid()

    F1 = Frame(wspok, borderwidth=2)
    F1.grid(column=0, row=0, columnspan=2)
    F2 = Frame(wspok, borderwidth=2)
    F2.grid(column=0, row=1, columnspan=2)
    F3 = Frame(wspok, borderwidth=2)
    F3.grid(column=0, row=2, columnspan=2)

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
        text = "Osobnik pierwszy: %(n1)s\nOsobnik drugi: %(n2)s\nWspółczynnik pokrewieństwa tych osobników wynosi: %(p)f" % {'n1': nazwa, 'n2': nazwa2, 'p': wsp}
        wynik_wspok2.delete('1.0', END)
        wynik_wspok2.insert(END, text, 'p')
        wynik_wspok2.insert(END, '\n', ('p'))

    def zapisywanieDoPlikuPokre():
        imie1 = treeO_wspok1.item(treeO_wspok1.selection())['text']
        imie2 = treeO_wspok2.item(treeO_wspok2.selection())['text']
        plik = "Pokrewienstwo_Osobnika_%(imie1)s_oraz_%(imie2)s.txt" % {'imie1': imie1, 'imie2': imie2}
        plik1 = open(plik, 'w')
        pok2 = "Wspólczynnik pokrewieństwa\n\nOsobnik pierwszy: \nNazwa: %(nazwa1)s \nPłeć:\nGatunek:\nHodowca:\n\nOsobnik drugi:\n\nNazwa: %(nazwa2)s\nPłeć:\nGatunek:\nHodowca:\n\nWspółczynnik pokrewieństwa pomiędzy tymi osobnikami wynosi: {}\n" \
               % {'nazwa1': imie1, 'nazwa2': imie2}

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
    avgpok.geometry("1000x600+0+0")
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

    def id_nazwa(id):
        """Funkcja zamieniająca id w nazwe osobnika"""
        print("Start in id nazwa", id)
        id = id
        query = "SELECT nazwa FROM osobniki WHERE id_os=?"
        db_rows = run_query(query, id)
        for row in db_rows:
            nazwa = row[0]
        return nazwa

    def nazwa_id(nazwa):
        """Funkcja podaje id osobnika"""
        nazwa = nazwa
        print ("Start in nazwa_id", nazwa)
        query = "SELECT id_os FROM osobniki WHERE nazwa=?"
        db_rows = run_query(query, (nazwa,))
        print("next one in nazwa id", nazwa)
        for row in db_rows:
            id = row[0]
            print ("for in nazwa id", nazwa)
        return id

    def find_parent(nazwa):
        #nazwa = nazwa
        list_of_parents = []
        print("Start in find parent nazwa",nazwa)
        nazwa1 = nazwa_id(nazwa)
        try:
            print("try in find parent nazwa 1: ", nazwa1)
            query = 'SELECT id_os2 FROM relacje WHERE id_os1=?'
            db_rows = run_query(query, (nazwa1,))
            for row in db_rows:
                parent = id_nazwa(row)
                list_of_parents.append(parent)
        except ValueError:
            pass
        return list_of_parents

    def find_grand(nazwa):
        nazwa = nazwa
        lista = []
        nazwa1 = nazwa_id(nazwa)
        query = 'SELECT id_os2 FROM relacje WHERE id_os1 in (SELECT id_os2 FROM relacje WHERE id_os1=?)'
        db_rows = run_query(query, (nazwa1,))
        for row in db_rows:
            grand = id_nazwa(row)
            lista.append(grand)
        return lista

    def find_pra(nazwa:str):
        nazwa = nazwa
        lista = []
        nazwa1 = nazwa_id(nazwa)
        query = 'SELECT id_os2 FROM relacje WHERE id_os1 in (SELECT id_os2 FROM relacje WHERE id_os1 in (SELECT id_os2 FROM relacje WHERE id_os1=?))'
        db_rows = run_query(query, [nazwa1])
        for row in db_rows:
            pra = id_nazwa(row)
            lista.append(pra)
        return lista

    def tree():
        nazwa = treeO_avgpok.item(treeO_avgpok.selection())['text']
        a = find_parent(nazwa)
        b = find_grand(nazwa)
        c = find_pra(nazwa)
        ListTree = []
        for i in a:
            ListTree.append(i)
        for j in b:
            ListTree.append(j)
        for y in c:
            ListTree.append(y)
        return ListTree

    def wspolny_przodek(nazwa1, nazwa2):
        x = tree()
        y = tree()
        wsp = set(x) & set(y)
        return wsp

    def porownanie(nzw1, nzw2):
        nzw1 = nzw1
        nzw2 = nzw2
        a = find_parent(nzw1)
        A = find_parent(nzw2)
        aa = []
        aa.extend(a)
        aa.extend(A)
        b = find_grand(nzw1)
        B = find_grand(nzw2)
        bb = []
        bb.extend(b)
        bb.extend(B)
        c = find_pra(nzw1)
        C = find_pra(nzw2)
        cc = []
        cc.extend(c)
        cc.extend(C)
        wspolny = []
        if (a == A) and len(a) == 2:
            wspolny.extend(a)
            return wspolny
        else:
            i = list(set(a) & set(A))
            wspolny.extend(i)

        if (len(a) > 0 or len(A) > 0):
            for i in aa:
                i = aa.pop(0)
                i = str(i[0])
                if ( i == nzw1) or (i == nzw2):
                    wspolny.append(i)

        if not wspolny:
            if b == B and len(b) == 4:
                wspolny.extend(b)
                return wspolny
            elif (len(b) > 0 or len(B) > 0):
                for i in bb:
                    i = bb.pop(0)
                    i = str(i[0])
                    if (i == nzw1) or (i == nzw2):
                        wspolny.append(i)
                i = list(set(b) & set(B))
                for z in b:
                    if b.count(z) > 1:
                        wspolny.append(z)
                for z in B:
                    if B.count(z) > 1:
                        wspolny.append(z)
                wspolny.extend(i)

        if not wspolny:

            if c == C and len(c) == 8:
                wspolny.extend(c)
                return wspolny
            elif (len(c) > 0 or len(C) > 0):
                for i in cc:
                    i = cc.pop(0)
                    i = str(i[0])
                    if (i == nzw1) or (i == nzw2):
                        wspolny.append(i)
            else:
                i = list(set(c) & set(C))
                for z in c:
                    if c.count(z) > 1:
                        wspolny.append(i)
                for z in C:
                    if C.count(z) > 1:
                        wspolny.append(i)
                wspolny.extend(i)

        if not wspolny:
            wsp = wspolny_przodek(nzw1, nzw2)
            wspolny.extend(wsp)
            return wspolny
        return wspolny

    def porownanie2(nzw1, nzw2):
        nzw1 = nzw1
        nzw2 = nzw2
        a = find_parent(nzw1)
        A = find_parent(nzw2)
        b = find_grand(nzw1)
        B = find_grand(nzw2)
        c = find_pra(nzw1)
        C = find_pra(nzw2)
        wspolny = porownanie(nzw1, nzw2)
        w = 0
        if not wspolny:
            nzw1 = str(nzw1)
            nzw1 = (nzw1,)
            nzw2 = str(nzw2)
            nzw2 = (nzw2,)
            for i in a:
                if (nzw1 == i) or (nzw2 == i):
                    w += 1
            for i in A:
                if (nzw1 == i) or (nzw2 == i):
                    w += 1
            for i in b:
                if (nzw1 == i) or (nzw2 == i):
                    w += 2
            for i in B:
                if (nzw1 == i) or (nzw2 == i):
                    w += 2
            for i in c:
                if (nzw1 == i) or (nzw2 == i):
                    w += 3
            for i in C:
                if (nzw1 == i) or (nzw2 == i):
                    w += 3
        return w

    def sciezka_konkretna( nzw1, nzw2, cos):
        cos = cos
        if type(cos) == str:
            cos = (cos,)
        full = []
        wsp_a = 0
        wsp_b = 0
        wsp_b_1 = 0
        wsp_c = 0
        wsp_c_1 = 0
        wsp_c_2 = 0
        wsp_c_3 = 0
        wsp_c_4 = 0
        wsp_c_5 = 0
        wsp_c_6 = 0
        wsp_c_7 = 0
        wsp_c_8 = 0
        wsp_c_9 = 0
        wsp_c_10 = 0
        wsp_c_11 = 0
        wsp_c_12 = 0
        wsp_c_13 = 0
        wsp_c_14 = 0
        wsp_c_15 = 0
        wsp_d_1 = 0
        wsp_d_2 = 0
        wsp_d_3 = 0
        wsp_d_4 = 0
        wsp_d_5 = 0
        wsp_d_6 = 0
        wsp_d_7 = 0
        wsp_d_8 = 0
        wsp_d_9 = 0
        wsp_d_10 = 0
        wsp_d_11 = 0
        wsp_d_12 = 0
        wsp_d_13 = 0
        wsp_d_14 = 0
        wsp_d_15 = 0
        wsp_d_16 = 0
        la = 0
        lb = 0
        lc = 0
        ld = 0
        le = 0
        lf = 0
        print("before find parent", nzw1, nzw2)
        A = find_parent(nzw1) # usunąłem [0]
        B = find_parent(nzw2) # usunąłem [0]
        print("find parent", nzw1, nzw2)
        C = find_grand(nzw1) # usunąłem [0]
        D = find_grand(nzw2) # usunąłem [0]
        print("find grand", nzw1, nzw2)
        E = find_pra(nzw1) # usunąłem [0]
        Fe = find_pra(nzw2) # usunąłem [0]

        print("find_pra", nzw1, nzw2)
        if A or B:
            if (A == B):
                if len(A) == 2:
                    for a in range(len(A)):
                        #a = A.pop(0)
                        aa = str(a)
                        if (a == cos):
                            wsp_a += 2
                elif len(A) == 1:
                    for a in range(len(A)):
                        #a = A.pop(0)
                        a = str(a) #a[0]
                        if (a == cos):
                            wsp_a += 1
                full.append(wsp_a)
                for i in range(full.count(0)):
                    full.remove(0)
                if full:
                    return full
            else:
                for a in range(len(A)):
                    for b in range(len(B)):
                        #a = A.pop(0)
                        aa = str(a)
                        #b = B.pop(0)
                        bb = str(b)
                        if (a == cos) and (b == cos):
                            wsp_a += 2
                        elif (a == cos) or (b == cos):
                            wsp_a += 1
                full.append(wsp_a)
            for i in range(full.count(0)):
                full.remove(0)
            if full:
                return full
        if not full:
            if C or D:
                if (C == D):
                    for c in range(len(C)):
                        #c = C.pop(0)
                        c = str(c)
                        if (c == cos):
                            wsp_b += 4
                        full.append(wsp_b)
            if E or Fe:
                if (E == Fe):
                    for e in range(len(E)):
                        #e = E.pop(0)
                        e = str(e)
                        if (e == cos):
                            wsp_c += 6
                        full.append(wsp_c)

        z = max(len(A), len(B), len(C), len(D), len(E), len(Fe))
        lista = [A, B, C, D, E, Fe]
        for l in lista:
            for l in lista:
                if len(l) < z:
                    l.extend([0])

        lista_index = []
        for l in lista:
            for i in l:
                if (i == cos):
                    index = lista.index(l)
                    lista_index.append(index)
        lista_index = list(set(lista_index))
        lista_wszystkiego = []
        lista_rodzicow = []
        lista_dziadkow = []
        lista_pra = []
        if len(lista_index) > 0:
            for a in range(len(lista_index)):
                i = lista_index.pop()
                if (i == 0) or (i == 1):
                    lista_rodzicow.append(i)
                elif (i == 2) or (i == 3):
                    lista_dziadkow.append(i)
                elif (i == 4) or (i == 5):
                    lista_pra.append(i)
            lista_wszystkiego.append(lista_rodzicow)
            lista_wszystkiego.append(lista_dziadkow)
            lista_wszystkiego.append(lista_pra)
            for a in range(len(lista_wszystkiego)):
                for b in lista_wszystkiego:
                    if not b:
                        lista_wszystkiego.remove(b)

            if len(lista_wszystkiego) == 1:
                for a in range(len(lista_wszystkiego)):
                    l = lista_wszystkiego.pop()
                    if (l == [0]) or (l == [1]) or (l == [0, 1]) or (l == [1, 0]):
                        for a in range(len(A)):
                            for b in range(len(B)):
                                a = A.pop(0)
                                b = B.pop(0)
                                if (a == cos) and (b == cos):
                                    wsp_a += 2
                                elif (a == cos) or (b == cos):
                                    wsp_a += 1
                                else:
                                    wsp_a += 0
                                    break
                                full.append(wsp_a)

                    elif (l == [2]) or (l == [3]) or (l == [2, 3]) or (l == [3, 2]):
                        for c in range(len(C)):
                            c = C.pop(0)
                            if (c == cos):
                                lc += 1
                        for d in range(len(D)):
                            d = D.pop(0)
                            if (d == cos):
                                ld += 1
                        if lc > 1 and ld > 1:
                            wsp_b += 4
                            wsp_b_1 += 4
                            full.extend([wsp_b, wsp_b_1])
                        elif lc > 1 or ld > 1:
                            wsp_b += 4
                            full.append(wsp_b)
                        elif lc == 1 and ld == 1:
                            wsp_b += 4
                            full.append(wsp_b)
                        elif lc == 1 or ld == 1:
                            wsp_b += 2
                            full.append(wsp_b)
                        else:
                            print('nie ma wsrod dziadkow')

                    elif (l == 4) or (l == 5) or (l == [4, 5]) or (l == [5, 4]):
                        for e in range(len(E)):
                            e = E.pop()
                            if (e == cos):
                                le += 1
                        for f in range(len(Fe)):
                            f = Fe.pop(0)
                            if (f == cos):
                                lf += 1
                        if le == 4 and lf == 4:
                            wsp_c += 6
                            wsp_c_1 += 6
                            wsp_c_2 += 6
                            wsp_c_3 += 6
                            wsp_c_4 += 6
                            wsp_c_5 += 6
                            wsp_c_6 += 6
                            wsp_c_7 += 6
                            wsp_c_8 += 6
                            wsp_c_9 += 6
                            wsp_c_10 += 6
                            wsp_c_11 += 6
                            wsp_c_12 += 6
                            wsp_c_13 += 6
                            wsp_c_14 += 6
                            wsp_c_15 += 6
                            full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3, wsp_c_4,
                                              wsp_c_5, wsp_c_6, wsp_c_7, wsp_c_8, wsp_c_9,
                                              wsp_c_10, wsp_c_11, wsp_c_12, wsp_c_13, wsp_c_14,
                                              wsp_c_15])
                        elif (le == 4 and lf == 3) or (le == 3 and lf == 4):
                            wsp_c += 6
                            wsp_c_1 += 6
                            wsp_c_2 += 6
                            wsp_c_3 += 6
                            wsp_c_4 += 6
                            wsp_c_5 += 5
                            wsp_c_6 += 5
                            wsp_c_7 += 5
                            wsp_c_8 += 5
                            full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3, wsp_c_4,
                                              wsp_c_5, wsp_c_6, wsp_c_7, wsp_c_8])
                        elif (le == 4 and lf == 2) or (le == 2 and lf == 4):
                            wsp_c += 6
                            wsp_c_1 += 6
                            wsp_c_2 += 6
                            wsp_c_3 += 6
                            wsp_c_4 += 6
                            wsp_c_5 += 6
                            wsp_c_6 += 6
                            wsp_c_7 += 6
                            full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3, wsp_c_4,
                                              wsp_c_5, wsp_c_6, wsp_c_7])
                        elif (le == 4 and lf == 1) or (le == 1 and lf == 4):
                            wsp_c += 6
                            wsp_c_1 += 6
                            wsp_c_2 += 6
                            wsp_c_3 += 6
                            wsp_c_4 += 6
                            full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3, wsp_c_4])
                        elif (le == 4 and lf == 0) or (le == 0 and lf == 4):  # inbred
                            wsp_c += 4
                            wsp_c_1 += 4
                            wsp_c_2 += 4
                            wsp_c_3 += 4
                            full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3])
                        elif le == 3 and lf == 3:
                            wsp_c += 6
                            wsp_c_1 += 6
                            wsp_c_2 += 6
                            wsp_c_3 += 6
                            wsp_c_4 += 6
                            wsp_c_5 += 6
                            wsp_c_6 += 6
                            wsp_c_7 += 6
                            wsp_c_8 += 6
                            full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3, wsp_c_4,
                                              wsp_c_5, wsp_c_6, wsp_c_7, wsp_c_8])
                        elif (le == 3 and lf == 2) or (le == 2 and lf == 3):
                            wsp_c += 6
                            wsp_c_1 += 6
                            wsp_c_2 += 6
                            wsp_c_3 += 6
                            wsp_c_4 += 6
                            wsp_c_5 += 6
                            wsp_c_6 += 6
                            full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3, wsp_c_4,
                                              wsp_c_5, wsp_c_6])
                        elif (le == 3 and lf == 1) or (le == 1 and lf == 3):
                            wsp_c += 6
                            wsp_c_1 += 6
                            wsp_c_2 += 6
                            wsp_c_3 += 0
                            full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3])
                        elif (le == 3 and lf == 0) or (le == 0 and lf == 3):  # inbred
                            wsp_c += 4
                            wsp_c_1 += 4
                            wsp_c_2 += 2
                            full.extend([wsp_c, wsp_c_1, wsp_c_2])
                        elif le == 2 and lf == 2:
                            wsp_c += 6
                            wsp_c_1 += 6
                            wsp_c_2 += 6
                            wsp_c_3 += 6
                            full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3])
                        elif (le == 2 and lf == 1) or (le == 1 and lf == 2):
                            wsp_c += 6
                            wsp_c_1 += 6
                            wsp_c_2 += 0
                            full.extend([wsp_c, wsp_c_1, wsp_c_2])
                        elif (le == 2 and lf == 0) or (le == 0 and lf == 2):  # inbred
                            wsp_c += 4
                            wsp_c_1 += 0
                            full.extend([wsp_c, wsp_c_1])
                        elif le == 1 and lf == 1:
                            wsp_c += 6
                            full.append(wsp_c)
                        elif (le == 1 or lf == 0) or (le == 0 and lf == 1):
                            wsp_c += 0
                            full.append(wsp_c)
                        else:
                            print('nie ma wsrod pradziadkow')
            else:

                # rodzic i dziadek
                if (((lista_rodzicow == [0]) and (lista_dziadkow == [2]))
                        or ((lista_rodzicow == [1]) and (lista_dziadkow == [2]))
                        or ((lista_rodzicow == [0]) and (lista_dziadkow == [3]))
                        or ((lista_rodzicow == [1]) and (lista_dziadkow == [3]))
                        or ((lista_rodzicow == [0]) and (lista_dziadkow == [2, 3]))
                        or ((lista_rodzicow == [0]) and (lista_dziadkow == [3, 2]))
                        or ((lista_rodzicow == [1]) and (lista_dziadkow == [2, 3]))
                        or ((lista_rodzicow == [1]) and (lista_dziadkow == [3, 2]))
                        or ((lista_rodzicow == [0, 1]) and (lista_dziadkow == [2]))
                        or ((lista_rodzicow == [1, 0]) and (lista_dziadkow == [2]))
                        or ((lista_rodzicow == [0, 1]) and (lista_dziadkow == [3]))
                        or ((lista_rodzicow == [1, 0]) and (lista_dziadkow == [3]))
                        or ((lista_rodzicow == [0, 1]) and (lista_dziadkow == [2, 3]))
                        or ((lista_rodzicow == [1, 0] and (lista_dziadkow == [2, 3]))
                            or ((lista_rodzicow == [0, 1]) and (lista_dziadkow == [3, 2]))
                            or ((lista_rodzicow == [1, 0]) and (lista_dziadkow == [3, 2])))):

                    for a in range(len(A)):
                        a = A.pop()
                        if (a == cos):
                            la += 1
                    for b in range(len(B)):
                        b = B.pop(0)
                        if (b == cos):
                            lb += 1
                    for c in range(len(C)):
                        c = C.pop()
                        if (c == cos):
                            lc += 1
                    for d in range(len(D)):
                        d = D.pop(0)
                        if (d == cos):
                            ld += 1

                    if (la == 1 and lb == 1 and lc == 1 and ld == 1):  ##
                        wsp_d_1 += 4
                        wsp_d_2 += 3
                        wsp_d_3 += 3
                        wsp_d_4 += 2
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4])
                    elif (la == 1 and lb == 1 and lc == 1 and ld == 0) or (
                            la == 1 and lb == 1 and lc == 0 and ld == 1):  ##
                        wsp_d_1 += 3
                        wsp_d_2 += 2
                        full.extend([wsp_d_1, wsp_d_2])
                    elif (la == 1 and lb == 0 and lc == 1 and ld == 2) or (
                            la == 0 and lb == 1 and lc == 2 and ld == 1):  ##
                        wsp_d_1 += 4
                        wsp_d_2 += 4
                        wsp_d_3 += 3
                        wsp_d_4 += 3
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4])
                    elif (la == 1 and lb == 0 and lc == 1 and ld == 1) or (
                            la == 0 and lb == 1 and lc == 1 and ld == 1):  ##
                        wsp_d_1 += 4
                        wsp_d_2 += 3
                        full.extend([wsp_d_1, wsp_d_2])
                    elif (la == 1 and lb == 0 and lc == 0 and ld == 1) or (
                            la == 0 and lb == 1 and lc == 1 and ld == 0):  ##
                        wsp_d_1 += 3
                        full.append(wsp_d_1)
                # rodzic i pradziadek
                elif (((lista_rodzicow == [0]) and (lista_pra == [4]))
                      or ((lista_rodzicow == [1]) and (lista_pra == [4]))
                      or ((lista_rodzicow == [0]) and (lista_pra == [5]))
                      or ((lista_rodzicow == [1]) and (lista_pra == [5]))
                      or ((lista_rodzicow == [0]) and (lista_pra == [4, 5]))
                      or ((lista_rodzicow == [0]) and (lista_pra == [5, 4]))
                      or ((lista_rodzicow == [1]) and (lista_pra == [4, 5]))
                      or ((lista_rodzicow == [1]) and (lista_pra == [5, 4]))
                      or ((lista_rodzicow == [0, 1]) and (lista_pra == [4]))
                      or ((lista_rodzicow == [1, 0]) and (lista_pra == [4]))
                      or ((lista_rodzicow == [0, 1]) and (lista_pra == [5]))
                      or ((lista_rodzicow == [1, 0]) and (lista_pra == [5]))
                      or ((lista_rodzicow == [0, 1]) and (lista_pra == [4, 5]))
                      or ((lista_rodzicow == [1, 0]) and (lista_pra == [4, 5]))
                      or ((lista_rodzicow == [0, 1]) and (lista_pra == [5, 4]))
                      or ((lista_rodzicow == [1, 0]) and (lista_pra == [5, 4]))):
                    for a in range(len(A)):
                        a = A.pop()
                        if (a == cos):
                            la += 1
                    for b in range(len(B)):
                        b = B.pop(0)
                        if (b == cos):
                            lb += 1
                    for e in range(len(E)):
                        e = E.pop()
                        if (e == cos):
                            le += 1
                    for f in range(len(Fe)):
                        f = Fe.pop(0)
                        if (f == cos):
                            lf += 1

                    if la == 1 and lb == 1 and lc == 2 and ld == 2:  ##
                        wsp_d_1 += 6
                        wsp_d_2 += 6
                        wsp_d_3 += 4
                        wsp_d_4 += 6
                        wsp_d_5 += 6
                        wsp_d_6 += 4
                        wsp_d_7 += 4
                        wsp_d_8 += 4
                        wsp_d_9 += 2
                        full.extend(
                            [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6,
                             wsp_d_7, wsp_d_8, wsp_d_9])
                    elif (la == 1 and lb == 0 and lc == 2 and ld == 4) or (
                            la == 0 and lb == 1 and lc == 2 and ld == 4):  ##
                        wsp_d_1 += 6
                        wsp_d_2 += 6
                        wsp_d_3 += 6
                        wsp_d_4 += 6

                        wsp_d_5 += 6
                        wsp_d_6 += 6
                        wsp_d_7 += 6
                        wsp_d_8 += 6

                        wsp_d_9 += 4
                        wsp_d_10 += 4
                        wsp_d_11 += 4
                        wsp_d_12 += 4
                        full.extend(
                            [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6,
                             wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10, wsp_d_11, wsp_d_12])
                    elif (la == 1 and lb == 1 and lc == 1 and ld == 2) or (
                            la == 1 and lb == 1 and lc == 2 and ld == 1):  ##
                        wsp_d_1 += 6
                        wsp_d_2 += 6
                        wsp_d_3 += 4
                        wsp_d_4 += 4
                        wsp_d_5 += 4
                        wsp_d_6 += 2
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5,
                                          wsp_d_6])
                    elif (la == 1 and lb == 0 and lc == 1 and ld == 4) or (
                            la == 0 and lb == 1 and lc == 4 and ld == 1):
                        wsp_d_1 += 6
                        wsp_d_2 += 6
                        wsp_d_3 += 6
                        wsp_d_4 += 6
                        wsp_d_5 += 4
                        wsp_d_6 += 4
                        wsp_d_7 += 4
                        wsp_d_8 += 4
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5,
                                          wsp_d_6, wsp_d_7, wsp_d_8])
                    elif (la == 1 and lb == 1 and lc == 2 and ld == 0) or (
                            la == 1 and lb == 1 and lc == 0 and ld == 2):
                        wsp_d_1 += 4
                        wsp_d_2 += 4
                        wsp_d_3 += 2
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3])
                    elif (la == 1 and lb == 1 and lc == 1 and ld == 1):
                        wsp_d_1 += 6
                        wsp_d_2 += 4
                        wsp_d_3 += 2
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3])
                    elif (la == 1 and lb == 1 and lc == 1 and ld == 0) or (
                            la == 1 and lb == 1 and lc == 0 and ld == 1):
                        wsp_d_1 += 4
                        wsp_d_2 += 2
                        full.extend([wsp_d_1, wsp_d_2])
                    elif (la == 1 and lb == 0 and lc == 2 and ld == 3) or (
                            la == 0 and lb == 1 and lc == 3 and ld == 2):
                        wsp_d_1 += 6
                        wsp_d_2 += 6
                        wsp_d_3 += 6

                        wsp_d_4 += 6
                        wsp_d_5 += 6
                        wsp_d_6 += 6

                        wsp_d_7 += 4
                        wsp_d_8 += 4
                        wsp_d_9 += 4
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5,
                                          wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9])
                    elif (la == 1 and lb == 0 and lc == 2 and ld == 2) or (
                            la == 0 and lb == 1 and lc == 2 and ld == 2):
                        wsp_d_1 += 6
                        wsp_d_2 += 6

                        wsp_d_3 += 6
                        wsp_d_4 += 6

                        wsp_d_5 += 4
                        wsp_d_6 += 4
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5,
                                          wsp_d_6])
                    elif ((la == 1 and lb == 0 and lc == 2 and ld == 1) or (
                            la == 0 and lb == 1 and lc == 2 and ld == 1) or (
                                  la == 1 and lb == 0 and lc == 1 and ld == 2) or (
                                  la == 0 and lb == 1 and lc == 1 and ld == 2)):
                        wsp_d_1 += 6
                        wsp_d_2 += 6
                        wsp_d_3 += 4
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3])
                    elif (la == 0 and lb == 1 and lc == 2 and ld == 0) or (
                            la == 1 and lb == 0 and lc == 0 and ld == 2):
                        wsp_d_1 += 4
                        wsp_d_2 += 4
                        full.extend([wsp_d_1, wsp_d_2])
                    elif (la == 1 and lb == 0 and lc == 1 and ld == 3) or (
                            la == 0 and lb == 1 and lc == 3 and ld == 1):
                        wsp_d_1 += 6
                        wsp_d_2 += 6
                        wsp_d_3 += 6
                        wsp_d_4 += 4
                        wsp_d_5 += 4
                        wsp_d_6 += 4
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5,
                                          wsp_d_6])
                    elif (la == 1 and lb == 0 and lc == 0 and ld == 1) or (
                            la == 0 and lb == 1 and lc == 1 and ld == 0):
                        wsp_d_1 += 4
                        full.append(wsp_d_1)

                elif ((((lista_dziadkow == [2]) and (lista_pra == [4])) or (
                        (lista_dziadkow == [3]) and (lista_pra == [4])) or (
                               (lista_dziadkow == [2]) and (lista_pra == [5])) or (
                               (lista_dziadkow == [3]) and (lista_pra == [5])) or (
                               (lista_dziadkow == [2]) and (lista_pra == [4, 5])) or (
                               (lista_dziadkow == [2]) and (lista_pra == [5, 4])) or (
                               (lista_dziadkow == [3] and (lista_pra == [4, 5])) or (
                               (lista_dziadkow == [3] and (lista_pra == [5, 4])) or (
                               (lista_dziadkow == [2, 3]) and (lista_pra == [4])) or (
                                       (lista_dziadkow == [3, 2]) and (lista_pra == [4])) or (
                                       (lista_dziadkow == [2, 3]) and (lista_pra == [5])) or (
                                       (lista_dziadkow == [3, 2]) and (lista_pra == [5])) or (
                                       (lista_dziadkow == [2, 3]) and (lista_pra == [4, 5])) or (
                                       (lista_dziadkow == [3, 2] and (lista_pra == [4, 5])) or (
                                       (lista_dziadkow == [2, 3]) and (lista_pra == [3, 2])) or (
                                               (lista_dziadkow == [1, 0]) and (lista_pra == [5, 4]))))))):
                    for c in range(len(C)):
                        c = C.pop()
                        if (c == cos):
                            lc += 1
                    for d in range(len(D)):
                        d = D.pop(0)
                        if (d == cos):
                            ld += 1
                    for e in range(len(E)):
                        e = E.pop()
                        if (e == cos):
                            le += 1
                    for f in range(len(Fe)):
                        f = Fe.pop(0)
                        if (f == cos):
                            lf += 1
                    if ((lc == 2) and (ld == 2) and (le == 2) and (lf == 2)):
                        wsp_d_1 += 6
                        wsp_d_2 += 5
                        wsp_d_3 += 6
                        wsp_d_4 += 5

                        wsp_d_5 += 5
                        wsp_d_6 += 4
                        wsp_d_7 += 5
                        wsp_d_8 += 4

                        wsp_d_9 += 6
                        wsp_d_10 += 5
                        wsp_d_11 += 6
                        wsp_d_12 += 5

                        wsp_d_13 += 5
                        wsp_d_14 += 4
                        wsp_d_15 += 5
                        wsp_d_16 += 4
                        full.extend(
                            [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6,
                             wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10, wsp_d_11, wsp_d_12,
                             wsp_d_13, wsp_d_14, wsp_d_15, wsp_d_16])
                    elif ((lc == 2) and (ld == 2) and (le == 2) and (lf == 1)) or (
                            (lc == 2) and (ld == 2) and (le == 1) and (lf == 2)):
                        wsp_d_1 += 6
                        wsp_d_2 += 5
                        wsp_d_3 += 5

                        wsp_d_4 += 5
                        wsp_d_5 += 4
                        wsp_d_6 += 4

                        wsp_d_7 += 6
                        wsp_d_8 += 5
                        wsp_d_9 += 5

                        wsp_d_10 += 5
                        wsp_d_11 += 4
                        wsp_d_12 += 4
                        full.extend(
                            [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6,
                             wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10, wsp_d_11, wsp_d_12])
                    elif ((lc == 2) and (ld == 2) and (le == 2) and (lf == 0)) or (
                            (lc == 2) and (ld == 2) and (le == 0) and (lf == 2)):
                        wsp_d_1 += 5
                        wsp_d_2 += 5

                        wsp_d_3 += 4
                        wsp_d_4 += 4

                        wsp_d_5 += 5
                        wsp_d_6 += 5

                        wsp_d_7 += 4
                        wsp_d_8 += 4
                        full.extend(
                            [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6,
                             wsp_d_7, wsp_d_8])
                    elif (((lc == 2) and (ld == 1) and (le == 2) and (lf == 3)) or (
                            (lc == 2) and (ld == 1) and (le == 3) and (lf == 2))
                          or ((lc == 1) and (ld == 2) and (le == 2) and (lf == 3)) or (
                                  (lc == 1) and (ld == 2) and (le == 3) and (lf == 2))):
                        wsp_d_1 += 6
                        wsp_d_2 += 5
                        wsp_d_3 += 6
                        wsp_d_4 += 6

                        wsp_d_5 += 5
                        wsp_d_6 += 4
                        wsp_d_7 += 5
                        wsp_d_8 += 5

                        wsp_d_9 += 6
                        wsp_d_10 += 5
                        wsp_d_11 += 6
                        wsp_d_12 += 6

                        wsp_d_13 += 5
                        wsp_d_14 += 4
                        wsp_d_15 += 5
                        wsp_d_16 += 5
                        full.extend(
                            [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6,
                             wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10, wsp_d_11, wsp_d_12,
                             wsp_d_13, wsp_d_14, wsp_d_15, wsp_d_16])
                    elif ((lc == 2) and (ld == 1) and (le == 2) and (lf == 2)) or (
                            (lc == 1) and (ld == 2) and (le == 2) and (lf == 2)):
                        wsp_d_1 += 6
                        wsp_d_2 += 5
                        wsp_d_3 += 6

                        wsp_d_4 += 5
                        wsp_d_5 += 4
                        wsp_d_6 += 5

                        wsp_d_7 += 6
                        wsp_d_8 += 5
                        wsp_d_9 += 6

                        wsp_d_10 += 5
                        wsp_d_11 += 4
                        wsp_d_12 += 5
                        full.extend(
                            [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6,
                             wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10, wsp_d_11, wsp_d_12])
                    elif (((lc == 2) and (ld == 1) and (le == 2) and (lf == 1)) or (
                            (lc == 1) and (ld == 2) and (le == 1) and (lf == 2))
                          or ((lc == 2) and (ld == 1) and (le == 1) and (lf == 2)) or (
                                  (lc == 1) and (ld == 2) and (le == 2) and (lf == 1))):
                        wsp_d_1 += 6
                        wsp_d_2 += 5

                        wsp_d_3 += 5
                        wsp_d_4 += 4

                        wsp_d_5 += 6
                        wsp_d_6 += 5

                        wsp_d_7 += 5
                        wsp_d_8 += 4
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5,
                                          wsp_d_6, wsp_d_7, wsp_d_8])
                    elif (((lc == 2) and (ld == 1) and (le == 2) and (lf == 0)) or (
                            (lc == 1) and (ld == 2) and (le == 0) and (lf == 2))
                          or ((lc == 2) and (ld == 1) and (le == 0) and (lf == 2)) or (
                                  (lc == 1) and (ld == 2) and (le == 2) and (lf == 0))):
                        wsp_d_1 += 5
                        wsp_d_2 += 4

                        wsp_d_3 += 5
                        wsp_d_4 += 4
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4])
                    elif ((lc == 2) and (ld == 1) and (le == 1) and (lf == 0)) or (
                            (lc == 1) and (ld == 2) and (le == 0) and (lf == 1)):
                        wsp_d_1 += 4
                        wsp_d_2 += 5
                        wsp_d_3 += 4
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3])
                    elif ((lc == 1) and (ld == 2) and (le == 1) and (lf == 0)) or (
                            (lc == 2) and (ld == 1) and (le == 0) and (lf == 1)):  ####
                        wsp_d_1 += 4
                        wsp_d_2 += 4
                        wsp_d_3 += 5
                        wsp_d_4 += 5
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4])
                    elif ((lc == 2) and (ld == 1) and (le == 0) and (lf == 1)) or (
                            (lc == 2) and (ld == 1) and (le == 1) and (lf == 0)):
                        wsp_d_1 += 4
                        wsp_d_2 += 5
                        wsp_d_3 += 4
                        wsp_d_4 += 5
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4])
                    elif ((lc == 2) and (ld == 0) and (le == 2) and (lf == 4)) or (
                            (lc == 0) and (ld == 2) and (le == 4) and (lf == 2)):
                        wsp_d_1 += 5
                        wsp_d_2 += 5
                        wsp_d_3 += 5
                        wsp_d_4 += 5

                        wsp_d_5 += 6
                        wsp_d_6 += 6
                        wsp_d_7 += 6
                        wsp_d_8 += 6

                        wsp_d_9 += 5
                        wsp_d_10 += 5
                        wsp_d_11 += 5
                        wsp_d_12 += 5

                        wsp_d_13 += 6
                        wsp_d_14 += 6
                        wsp_d_15 += 6
                        wsp_d_16 += 6
                        full.extend(
                            [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6,
                             wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10, wsp_d_11, wsp_d_12,
                             wsp_d_13, wsp_d_14, wsp_d_15, wsp_d_16])
                    elif ((lc == 2) and (ld == 0) and (le == 2) and (lf == 3)) or (
                            (lc == 0) and (ld == 2) and (le == 3) and (lf == 2)):
                        wsp_d_1 += 5
                        wsp_d_2 += 5
                        wsp_d_3 += 5

                        wsp_d_4 += 6
                        wsp_d_5 += 6
                        wsp_d_6 += 6

                        wsp_d_7 += 5
                        wsp_d_8 += 5
                        wsp_d_9 += 5

                        wsp_d_10 += 6
                        wsp_d_11 += 6
                        wsp_d_12 += 6
                        full.extend(
                            [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6,
                             wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10, wsp_d_11, wsp_d_12])
                    elif ((lc == 2) and (ld == 0) and (le == 2) and (lf == 2)) or (
                            (lc == 0) and (ld == 2) and (le == 2) and (lf == 2)):
                        wsp_d_1 += 5
                        wsp_d_2 += 5

                        wsp_d_3 += 6
                        wsp_d_4 += 6

                        wsp_d_5 += 5
                        wsp_d_6 += 5

                        wsp_d_7 += 6
                        wsp_d_8 += 6
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5,
                                          wsp_d_6, wsp_d_7, wsp_d_8])
                    elif ((lc == 2) and (ld == 0) and (le == 2) and (lf == 1)) or (
                            (lc == 0) and (ld == 2) and (le == 1) and (lf == 2)):
                        wsp_d_1 += 5
                        wsp_d_2 += 6
                        wsp_d_3 += 5
                        wsp_d_4 += 6
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4])
                    elif ((lc == 2) and (ld == 0) and (le == 1) and (lf == 2)) or (
                            (lc == 0) and (ld == 2) and (le == 2) and (lf == 1)):
                        wsp_d_1 += 5
                        wsp_d_2 += 5

                        wsp_d_3 += 6
                        wsp_d_4 += 6

                        wsp_d_5 += 5
                        wsp_d_6 += 5
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5,
                                          wsp_d_6])
                    elif ((lc == 1) and (ld == 0) and (le == 3) and (lf == 4)) or (
                            (lc == 0) and (ld == 1) and (le == 4) and (lf == 3)):
                        wsp_d_1 += 5
                        wsp_d_2 += 5
                        wsp_d_3 += 5
                        wsp_d_4 += 5

                        wsp_d_5 += 6
                        wsp_d_6 += 6
                        wsp_d_7 += 6
                        wsp_d_8 += 6

                        wsp_d_9 += 6
                        wsp_d_10 += 6
                        wsp_d_11 += 6
                        wsp_d_12 += 6

                        wsp_d_13 += 6
                        wsp_d_14 += 6
                        wsp_d_15 += 6
                        wsp_d_16 += 6
                        full.extend(
                            [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6,
                             wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10, wsp_d_11, wsp_d_12,
                             wsp_d_13, wsp_d_14, wsp_d_15, wsp_d_16])
                    elif ((lc == 1) and (ld == 0) and (le == 3) and (lf == 3)) or (
                            (lc == 0) and (ld == 1) and (le == 3) and (lf == 3)):
                        wsp_d_1 += 5
                        wsp_d_2 += 5
                        wsp_d_3 += 5

                        wsp_d_4 += 6
                        wsp_d_5 += 6
                        wsp_d_6 += 6

                        wsp_d_7 += 6
                        wsp_d_8 += 6
                        wsp_d_9 += 6

                        wsp_d_10 += 6
                        wsp_d_11 += 6
                        wsp_d_12 += 6
                        full.extend(
                            [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6,
                             wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10, wsp_d_11, wsp_d_12])
                    elif ((lc == 1) and (ld == 0) and (le == 2) and (lf == 3)) or (
                            (lc == 0) and (ld == 1) and (le == 3) and (lf == 2)):
                        wsp_d_1 += 5
                        wsp_d_2 += 5
                        wsp_d_3 += 5

                        wsp_d_4 += 6
                        wsp_d_5 += 6
                        wsp_d_6 += 6

                        wsp_d_7 += 6
                        wsp_d_8 += 6
                        wsp_d_9 += 6
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5,
                                          wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9])
                    elif ((lc == 1) and (ld == 0) and (le == 3) and (lf == 2)) or (
                            (lc == 0) and (ld == 1) and (le == 2) and (lf == 3)):
                        wsp_d_1 += 5
                        wsp_d_2 += 5

                        wsp_d_3 += 6
                        wsp_d_4 += 6

                        wsp_d_5 += 6
                        wsp_d_6 += 6

                        wsp_d_7 += 6
                        wsp_d_8 += 6
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5,
                                          wsp_d_6, wsp_d_7, wsp_d_8])
                    elif ((lc == 1) and (ld == 0) and (le == 3) and (lf == 1)) or (
                            (lc == 0) and (ld == 1) and (le == 1) and (lf == 3)):
                        wsp_d_1 += 5
                        wsp_d_2 += 6
                        wsp_d_3 += 6
                        wsp_d_4 += 6
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4])
                    elif ((lc == 1) and (ld == 0) and (le == 1) and (lf == 3)) or (
                            (lc == 0) and (ld == 1) and (le == 3) and (lf == 1)):  #
                        wsp_d_1 += 5
                        wsp_d_2 += 5
                        wsp_d_3 += 5

                        wsp_d_4 += 6
                        wsp_d_5 += 6
                        wsp_d_6 += 6
                        full.extend([wsp_d_1, wsp_d_2, wsp_d_4, wsp_d_5])

        FULL = sum(full)
        full = full[0:len(full)]
        return full

    def inbred( nzw):
        nzw = nzw
        x = find_parent(nzw)
        if len(x) == 2:
            rodzic1 = x[0]
            rodzic2 = x[1]
        else:
            F = 0
            return F
        y = porownanie(rodzic1, rodzic2)
        if y:
            for i in range(len(y)):
                w = []
                ii = y.pop()
                ic = str(ii[0])
                xx = find_parent(ic)
                if len(xx) == 2:
                    a1 = xx[0]
                    rodzic11 = str(a1[0])
                    b1 = xx[1]
                    rodzic12 = str(b1[0])
                    por = porownanie(rodzic11, rodzic12)
                    if por:
                        for a in range(len(por)):
                            ai = por.pop()
                            sy = sciezka_konkretna(rodzic11, rodzic12, ai)
                            for i in range(sy.count(0)):
                                sy.remove(0)
                            Za = []
                            for j in sy:
                                w = 0.5 ** (j + 1)
                                Za.append(w)
                            Fa = sum(Za)
                    else:
                        Fa = 0
                else:
                    Fa = 0
            k = sciezka_konkretna(rodzic1, rodzic2, ii)
            for i in range(k.count(0)):
                k.remove(0)
            for i in range(len(k)):
                sz = k.pop()
                szy = (0.5 ** (sz + 1)) * (1 + Fa)
                w.append(szy)
        else:
            F = 0
            return F
        F = sum(w)
        return F

    def pokrewienstwo(nzw1, nzw2):
        x = porownanie(nzw1, nzw2)
        y = porownanie2(nzw1, nzw2)
        w = []
        FFF = []
        if x:
            for i in range(len(x)):
                w = []
                if len(x) > 0:
                    ic = x.pop()
                    F = inbred(ic)
                    k = sciezka_konkretna(nzw1, nzw2, ic)
                    for i in range(k.count(0)):
                        k.remove(0)
                    if len(k) > 0:
                        for i in range(len(k)):
                            sz = k.pop()
                            szy = 0.5 ** sz
                            w.append(szy)
                    else:
                        szy = 0
                        w.append(szy)
                    pi = sum(w)
                    FF = ((pi) * (1 + F))
                    FFF.append(FF)
                else:
                    X = 0
                    return 0
        if y:
            szy = 0.5 ** y
            w.append(szy)
            pi = sum(w)
            FFF.append(pi)

        FFFF = sum(FFF)
        Fx = inbred(nzw1)
        Fy = inbred(nzw2)
        f = math.sqrt((1 + Fx) * (1 + Fy))
        X = (FFFF / f)
        return X

    def sredni_wspolczynnik_pokrewienstwa():
        nazwa = treeO_avgpok.item(treeO_avgpok.selection())['text']
        all = tree()
        lista = []
        for i in all:
            RC = pokrewienstwo(nazwa, i)
            lista.append(RC)
        suma = sum(lista)
        length = len(all)
        MK = suma/length
        mk = "Osobnik: %(n)s\nŚredni współczynnik pokrewieństwa dla tego osobnika wynosi: %(p)f" % {'n': nazwa ,'p':MK}
        wynik_avgpok.delete('1.0', END)
        wynik_avgpok.insert(END, mk, ('p'))
        wynik_avgpok.insert(END, '\n', ('p'))

    def zapisywanieDoPlikuAvgPokre():
        imie = treeO_avgpok.item(treeO_avgpok.selection())['text']
        plik = "AVG_pokrewienstwa_osobnika_%(imie)s.txt" % {'imie': imie}
        plik1 = open(plik, 'w')
        pok = "Średni współczynnik pokrewieństwa \n\nOsobnik: \nNazwa: %(nazwa)s \nPłeć: {} \nGatunek:{} \nHodowca:{} \nŚredni współczynnik pokrewieństwa wynosi: tyle" \
              % {'nazwa': imie}
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
    treeview.geometry("1000x600+0+0")
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
        nazwaP2 = 'Mamuśka'
        nazwaP3 = 'Tatuśek'
        '''nazwaP4 =
        nazwaP5 =
        nazwaP6 =
        nazwaP7 =
        nazwaP8 =
        nazwaP9 =
        nazwaP10 =
        nazwaP11 =
        nazwaP12 =
        nazwaP13 =
        nazwaP14 =
        nazwaP15 =
        nazwaP16 =
        nazwaP17 =
        nazwaP18 =
        nazwaP19 =
        nazwaP20 =
        nazwaP21 =
        nazwaP22 =
        nazwaP23 =
        nazwaP24 =
        nazwaP25 =
        nazwaP26 =
        nazwaP27 =
        nazwaP28 =
        nazwaP29 =
        nazwaP30=
        nazwaP31 ='''
        P1 = Node(nazwaP1)
        P2 = Node(nazwaP2, parent=P1)
        P3 = Node(nazwaP3, parent=P1)
        P4 = Node("P4", parent=P2)
        P5 = Node("P5", parent=P2)
        P6 = Node("P6", parent=P3)
        P7 = Node("P7", parent=P3)
        P8 = Node("P8", parent=P4)
        P9 = Node("P9", parent=P4)
        P10 = Node("P10", parent=P5)
        P11 = Node("P11", parent=P5)
        P12 = Node("P12", parent=P6)
        P13 = Node("P13", parent=P6)
        P14 = Node("P14", parent=P7)
        P15 = Node("P15", parent=P7)
        P16 = Node("P16", parent=P8)
        P17 = Node("P17", parent=P8)
        P18 = Node("P18", parent=P9)
        P19 = Node("P19", parent=P9)
        P20 = Node("P20", parent=P10)
        P21 = Node("P21", parent=P10)
        P22 = Node("P22", parent=P11)
        P23 = Node("P23", parent=P11)
        P24 = Node("P24", parent=P12)
        P25 = Node("P25", parent=P12)
        P26 = Node("P26", parent=P13)
        P27 = Node("P27", parent=P13)
        P28 = Node("P28", parent=P14)
        P29 = Node("P29", parent=P14)
        P30 = Node("P30", parent=P15)
        P31 = Node("P31", parent=P15)

        for pre, fill, node in RenderTree(P1):
            print("%s%s" % (pre, node.name))
            # a=print("{1} {2}".format(pre[0]), node.name[0])
            # treeO_avgpok.insert(END, a)


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
root.title("Julia & Cezar Company")  # tytuł naszej tabeli root
#root_label = tk.Label(root)
#root_label.grid()

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

# root.mainloop()  # zamknięcie pętli
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
