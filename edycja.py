#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import baza_danych

conn = sqlite3.connect('baza.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()


class Edycja(object):

    def dodaj_osobnika(self):
        print("Wybierz wsród:")
        self.x = input()
        self.wybor1 = baza_danych.Baza.segregujPoPlci()
        self.nazwa1 = input()
        cur.execute("SELECT id_os from OSOBNIKI WHERE nazwa=self.nazwa1")
        self.id1 = cur.fetchone()
        cur.execute(
            "SELECT gatunek from OSOBNIKI WHERE nazwa=self.nazwa1 join GATUNKI on OSOBNIK.id_gat = GATUNKI.id_gat")
        self.gatunek1 = cur.fetchone()
        cur.execute(
            "SELECT id_hod FROM OSOBNIKI WHERE nazwa=self.nazwa1 join HODOWCY on OSOBNIKI.id_hod=HODOWCY.id.hod")
        self.hodowca1 = cur.fetchone()

        print("Wybierz wśród:")
        self.y = input()
        self.wybor2 = baza_danych.Baza.segregujPoPlci()
        self.nazwa2 = input()
        cur.execute("SELECT id_os from OSOBNIKI WHERE nazwa=self.nazwa2")
        self.id2 = cur.fetchone()
        cur.execute("""SELECT gatunek from OSOBNIKI WHERE nazwa=self.nazwa2
                    join GATUNKI on OSOBNIK.id_gat = GATUNKI.id_gat""")
        self.gatunek2 = cur.fetchone()
        cur.execute("""SELECT id_hod FROM OSOBNIKI WHERE nazwa=self.nazwa2 
                    join HODOWCY on OSOBNIKI.id_hod=HODOWCY.id.hod""")
        self.hodowca2 = cur.fetchone()

        print("Wpisza nazwe osobnika:")
        self.nazwa = input()
        print("""Wybierz płeć osobnika:
                1. samiec
                2. samica""")
        self.plec = input()
        cur.execute("""SELECT id_gat, gatunek FROM OSOBNIKI""")
        self.osobniki = cur.fetchall()
        self.n = len(self.osobniki) + 1
        cur.execute("INSERT INTO OSOBNIKI(id_os, nazwa, plec, id_gat, id_hod)VALUES(?, ?, ?, ?, ?)",
                    (self.n, self.nazwa, self.plec, self.gatunek1, self.hodowca1))
        cur.execute("INSERT INTO RELACJE(id_os1, id_os2) VALUES (?, ?)", (self.n, self.id1))
        cur.execute("INSERT INTO RELACJE(id_os1, id_os2) VALUES (?, ?)", (self.n, self.id2))
        cur.execute("INSERT INTO OSOBNIKI_HODOWCY(id_os, id_hod) VALUES (?, ?)", (self.n, self.hodowca1))

jula = Edycja()
jula.dodaj_osobnika()

conn.commit()
cur.close()
conn.close()
