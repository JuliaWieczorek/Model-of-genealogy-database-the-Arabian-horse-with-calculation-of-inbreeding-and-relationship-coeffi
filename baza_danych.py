#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import planarity

# conn = sqlite3.connect('baza.db')
# conn.row_factory = sqlite3.Row
# cur = conn.cursor()


class Baza(object):

    def open(self):
        self.conn = sqlite3.connect('baza.db')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def czytajdane(self):
        """Funkcja pobiera i wyświetla dane z bazy."""
        self.lista = []
        self.cur.execute(" SELECT id_os, nazwa, plec FROM OSOBNIKI ")
        self.osobnicy = self.cur.fetchall()
        for self.osobnik in self.osobnicy:
            self.dane = (self.osobnik['id_os'], self.osobnik['nazwa'], self.osobnik['plec'])
            self.lista.append(self.dane)
        return self.lista

    def czytajrelacje(self):
        """ Funkcja pobiera i wyświetla dane z encji relacja """
        self.cur.execute(" SELECT id_os1, id_os2 FROM RELACJE ")
        self.relacja = self.cur.fetchall()
        for self.rel in self.relacja:
            print(self.rel['id_os1'], self.rel['id_os2'])
        print()

    def czytajgatunki(self):
        """ Funkcja pobiera i wyświetla dane z gatunki"""
        self.cur.execute("SELECT id_gat, gatunek FROM GATUNKI")
        self.gatunek = self.cur.fetchall()
        self.lista = []
        for self.gat in self.gatunek:
            print(self.gat['id_gat'], self.gat['gatunek'])
            self.lista.append(self.gat['gatunek'])
            print(self.lista)
        print()
        return self.lista

    def czytajhodowcow(self):
        """Funckja wczytująca wszystkich hodowców z bazy"""
        self.cur.execute(" SELECT id_hod, imie, nazwisko FROM HODOWCY")
        self.hodowca = self.cur.fetchall()
        self.lista = []
        for self.hod in self.hodowca:
            print(self.hod['id_hod'], self.hod['imie'], self.hod['nazwisko'])
            self.lista.append(self.hod['id_hod'], self.hod['imie'], self.hod['nazwisko'])
        print()
        return self.lista

    def czytajosobniki_hodocy(self):
        """Funckja wczytująca encje laczaca"""
        self.cur.execute("SELECT id_os, id_hod FROM OSOBNIKI_HODOWCY")
        self.os_hod = self.cur.fetchall()
        for self.oh in self.os_hod:
            print(self.oh['id_os'], self.oh['id_hod'])
        print()

    def relacjepoimionach(self):
        """Funkcja laczy tabele osobnik i relacja
            Wczytuje dane relacji i tlumacze id osobnikow na ich imiona"""
        self.cur.execute(
            """
            SELECT o1.nazwa as 'rodzic', o2.nazwa as 'potomek' FROM OSOBNIKI AS o1
            join RELACJE on o1.id_os==RELACJE.id_os1
            join OSOBNIKI as o2 on o2.id_os==RELACJE.id_os2
            """)
        self.relacja = self.cur.fetchall()
        for self.rel in self.relacja:
            print(self.rel['rodzic'], self.rel['potomek'])
        print()

    def wlasciciele(self):
        """Funckja wypisze właścicieli wraz z ich pupilami """
        self.cur.execute(
            """
            SELECT imie, nazwisko, nazwa from HODOWCY
            join OSOBNIKI using(id_hod)
            """)
        self.wlasciciele = self.cur.fetchall()
        for self.wl in self.wlasciciele:
            print(self.wl['imie'], self.wl['nazwisko'], self.wl['nazwa'])
        self.cur.execute(
            """
            SELECT imie, nazwisko, count(nazwa) as ilosc from HODOWCY
            join OSOBNIKI using(id_hod)
            group by imie
            """)
        self.wlasciciele = self.cur.fetchall()
        for self.wl in self.wlasciciele:
            print(self.wl['imie'], self.wl['nazwisko'], self.wl['ilosc'])
        print()

    def gatunekosobnika(self):
        """Funkcja wypisze gatunki z ktorych pochodza osobniki """
        self.cur.execute(
            """
            SELECT nazwa, gatunek from OSOBNIKI
            join GATUNKI on OSOBNIKI.id_gat == GATUNKI.id_gat
            """)
        self.gatunki = self.cur.fetchall()
        for self.gat in self.gatunki:
            print(self.gat['nazwa'], self.gat['gatunek'])
        print()

    def wpisujwgraf(self):
        """Funkcja pobiera i modyfikuje dane w forme grafu tołp """
        self.cur.execute("SELECT id_os1, id_os2 FROM RELACJE")
        self.relacja = self.cur.fetchall()
        self.graph = ()
        self.listagrafow = []
        for self.rel in self.relacja:
            graph = (self.rel['id_os1'], self.rel['id_os2'])
            self.listagrafow.append(self.graph)
        print(self.listagrafow)
        return self.listagrafow

    def wpisujwgraf_po_nazwach(self):
        """Funkcja pobiera i modyfikuje dane w forme grafu tołp """
        self.cur.execute(
            """
            SELECT o1.nazwa as 'rodzic', o2.nazwa as 'potomek' FROM OSOBNIKI AS o1
            join RELACJE on o1.id_os==RELACJE.id_os1
            join OSOBNIKI as o2 on o2.id_os==RELACJE.id_os2
            """)
        self.relacja = self.cur.fetchall()
        self.graph = ()
        self.listagrafow1 = []
        for self.rel in self.relacja:
            self.graph = (self.rel['rodzic'], self.rel['potomek'])
            self.listagrafow1.append(self.graph)
        print(self.listagrafow1)
        return self.listagrafow1

    def rysujgraf(self):
        self.b = self.wpisujwgraf_po_nazwach()
        print(planarity.is_planar(self.b))
        print(planarity.ascii(self.b))

    def czytajdane2(self):
        """Funkcja pobiera i wyświetla dane z bazy."""
        self.cur.execute("SELECT id_os, id_hod FROM OSOBNIKI")
        self.osobnicy = self.cur.fetchall()
        for self.osobnik in self.osobnicy:
            print('(', self.osobnik['id_os'], ',', self.osobnik['id_hod'], '),')
        print()

    def segregujPoPlci(self):
        """Funkcja czytaj dane segregujaca wzgledem plci."""
        print("""Wybierz:
              1. samiec
              2. samica""")
        w = input()
        print("wybrales", w)
        self.wybor = []
        self.wszystko = self.czytajdane()
        if w == "1":
            for i in self.wszystko:
                for j in i:
                    if j == 'samiec':
                        self.wybor.append(i)
        elif w == "2":
            for i in self.wszystko:
                for j in i:
                    if j == 'samica':
                        self.wybor.append(i)
        print(self.wybor)

    def id_nazwa(self, id):
        """Funkcja zamieniająca id w nazwe osobnika"""
        # self.open()
        self.id = id
        for row in self.cur.execute("SELECT nazwa FROM osobniki WHERE id_os=?", (self.id,)):
            self.nazwa = row[0]
            print(self.nazwa)
        # self.close()
        return self.nazwa

    def nazwa_id(self, nazwa):
        """Funkcja podaje id osobnika"""
        self.nazwa = nazwa
        for row in self.cur.execute("SELECT id_os FROM osobniki WHERE nazwa=?", (self.nazwa,)):
            self.id = row[0]
            print(self.id)
        return self.id

    def dodaj_gatunki(self):
        """Funkcja służąca do wpisywania danych do encji gatunki """
        print("Podaj nazwe gatunku")
        self.x = input()
        self.cur.execute("SELECT id_gat, gatunek FROM GATUNKI")
        self.gatunek = self.cur.fetchall()
        self.n = len(self.gatunek)
        self.cur.execute("INSERT INTO GATUNKI VALUES(?,?)", (self.n + 1, self.x))

    def dodaj_osobniki(self):
        print("Ile osobników chcesz dodać?")
        self.n = input()
        print("Podaj nazwe osobnika")
        self.nazwa = input()
        print("Z jakiego gatunku?")
        self.gatunek = input()
        print("samiec/ samica")
        self.plec = input()
        print("Imie hodowcy:")
        self.imie = input()
        print("Nazwisko hodowcy:")
        self.nazwisko = input()

        for self.i in self.czyt:
            if self.gatunek == self.czyt:
                self.cur.execute("SELECT id_gat FROM GATUNKI WHERE gatunek = (?)", (self.gatunek))
                self.n = self.cur.fetchall()
                print(self.n)
                break
            else:
                self.cur.execute("SELECT id_gat, gatunek FROM GATUNKI")
                self.gatunek = self.cur.fetchall()
                self.n = len(self.gatunek) + 1
                self.cur.execute("INSERT INTO GATUNKI VALUES(?,?)", (self.n, self.gatunek))
                self.czytajgatunki()
                break

        '''self.hod = czytajhodowcow()
        for self.i in self.hod:
            if 
        cur.execute("""SELECT id_hod, imie, nazwisko FROM HODOWCY """)

        cur.execute("""SELECT id_os, nazwa FROM OSOBNIKI""")
        self.osobnicy = cur.fetchall()
        self.m = len(self.osobnicy)
        cur.execute("""INSERT INTO OSOBNIKI
                    (id_os, nazwa, plec, id_gat) VALUES (?, ?, ?, ?)"""
                    , (m+1, nazwa, plec, n))#dołożyć id_hod

    '''

# jula = Baza()
# jula.czytajrelacje()
# jula.segregujPoPlci()
# jula.relacjepoimionach()
# jula.nazwa_id('CARO')
# jula.id_nazwa(2)
# jula.dodaj_osobniki()
# jula.czytajgatunki()

