#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import planarity

conn = sqlite3.connect('baza.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()


class Baza(object):

    def czytajdane(self):
        """Funkcja pobiera i wyświetla dane z bazy."""
        cur.execute(" SELECT id_os, nazwa FROM OSOBNIKI ")
        self.osobnicy = cur.fetchall()
        for self.osobnik in self.osobnicy:
            print(self.osobnik['id_os'], self.osobnik['nazwa'])
        print()

    def czytajrelacje(self):
        """ Funkcja pobiera i wyświetla dane z encji relacja """
        cur.execute(" SELECT id_os1, id_os2 FROM RELACJE ")
        self.relacja = cur.fetchall()
        for self.rel in self.relacja:
            print(self.rel['id_os1'], self.rel['id_os2'])
        print()

    def czytajgatunki(self):
        """ Funkcja pobiera i wyświetla dane z gatunki"""
        cur.execute("SELECT id_gat, gatunek FROM GATUNKI")
        self.gatunek = cur.fetchall()
        self.lista = []
        for self.gat in self.gatunek:
            print(self.gat['id_gat'], self.gat['gatunek'])
            self.lista.append(self.gat['gatunek'])
            print(self.lista)
        print()
        return self.lista

    def czytajhodowcow(self):
        """Funckja wczytująca wszystkich hodowców z bazy"""
        cur.execute(" SELECT id_hod, imie, nazwisko FROM HODOWCY")
        self.hodowca = cur.fetchall()
        self.lista = []
        for self.hod in self.hodowca:
            print(self.hod['id_hod'], self.hod['imie'], self.hod['nazwisko'])
            self.lista.append(self.hod['id_hod'], self.hod['imie'], self.hod['nazwisko'])
        print()
        return self.lista

    def czytajosobniki_hodocy(self):
        """Funckja wczytująca encje laczaca"""
        cur.execute("SELECT id_os, id_hod FROM OSOBNIKI_HODOWCY")
        self.os_hod = cur.fetchall()
        for self.oh in self.os_hod:
            print(self.oh['id_os'], self.oh['id_hod'])
        print()

    def relacjepoimionach(self):
        """Funkcja laczy tabele osobnik i relacja
            Wczytuje dane relacji i tlumacze id osobnikow na ich imiona"""
        cur.execute(
            """
            SELECT o1.nazwa as 'rodzic', o2.nazwa as 'potomek' FROM OSOBNIKI AS o1
            join RELACJE on o1.id_os==RELACJE.id_os1
            join OSOBNIKI as o2 on o2.id_os==RELACJE.id_os2
            """)
        self.relacja = cur.fetchall()
        for self.rel in self.relacja:
            print(self.rel['rodzic'], self.rel['potomek'])
        print()

    def wlasciciele(self):
        """Funckja wypisze właścicieli wraz z ich pupilami """
        cur.execute(
            """
            SELECT imie, nazwisko, nazwa from HODOWCY
            join OSOBNIKI using(id_hod)
            """)
        self.wlasciciele = cur.fetchall()
        for self.wl in self.wlasciciele:
            print(self.wl['imie'], self.wl['nazwisko'], self.wl['nazwa'])
        cur.execute(
            """
            SELECT imie, nazwisko, count(nazwa) as ilosc from HODOWCY
            join OSOBNIKI using(id_hod)
            group by imie
            """)
        self.wlasciciele = cur.fetchall()
        for self.wl in self.wlasciciele:
            print(self.wl['imie'], self.wl['nazwisko'], self.wl['ilosc'])
        print()

    def gatunekosobnika(self):
        """Funkcja wypisze gatunki z ktorych pochodza osobniki """
        cur.execute(
            """
            SELECT nazwa, gatunek from OSOBNIKI
            join GATUNKI on OSOBNIKI.id_gat == GATUNKI.id_gat
            """)
        self.gatunki = cur.fetchall()
        for self.gat in self.gatunki:
            print(self.gat['nazwa'], self.gat['gatunek'])
        print()

    def wpisujwgraf(self):
        """Funkcja pobiera i modyfikuje dane w forme grafu tołp """
        cur.execute("SELECT id_os1, id_os2 FROM RELACJE")
        self.relacja = cur.fetchall()
        self.graph = ()
        self.listagrafow = []
        for self.rel in self.relacja:
            graph = (self.rel['id_os1'], self.rel['id_os2'])
            self.listagrafow.append(self.graph)
        print(self.listagrafow)
        return self.listagrafow

    def wpisujwgraf_po_nazwach(self):
        """Funkcja pobiera i modyfikuje dane w forme grafu tołp """
        cur.execute(
            """
            SELECT o1.nazwa as 'rodzic', o2.nazwa as 'potomek' FROM OSOBNIKI AS o1
            join RELACJE on o1.id_os==RELACJE.id_os1
            join OSOBNIKI as o2 on o2.id_os==RELACJE.id_os2
            """)
        self.relacja = cur.fetchall()
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

    def czytajdane(self):
        """Funkcja pobiera i wyświetla dane z bazy."""
        cur.execute("SELECT id_os, id_hod FROM OSOBNIKI")
        self.osobnicy = cur.fetchall()
        for self.osobnik in self.osobnicy:
            print('(', self.osobnik['id_os'], ',', self.osobnik['id_hod'], '),')
        print()

    def dodaj_gatunki(self):
        """Funkcja służąca do wpisywania danych do encji gatunki """
        print("Podaj nazwe gatunku")
        self.x = input()
        cur.execute("SELECT id_gat, gatunek FROM GATUNKI")
        self.gatunek = cur.fetchall()
        self.n = len(self.gatunek)
        cur.execute("INSERT INTO GATUNKI VALUES(?,?)", (self.n + 1, self.x))
        conn.commit()

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
                cur.execute("SELECT id_gat FROM GATUNKI WHERE gatunek = (?)", (self.gatunek))
                self.n = cur.fetchall()
                print(self.n)
                break
            else:
                cur.execute("SELECT id_gat, gatunek FROM GATUNKI")
                self.gatunek = cur.fetchall()
                n = len(self.gatunek) + 1
                cur.execute("INSERT INTO GATUNKI VALUES(?,?)", (self.n, self.gatunek))
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

jula = Baza()
# jula.czytajdane()
jula.czytajgatunki()

conn.commit()
cur.close()
conn.close()
