#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import baza_danych

conn = sqlite3.connect('baza.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()


def dodaj_osobnika(self):
    print("Podaj nazwe gatunku")
    self.x = input()
    self.gatunki = baza_danych.Baza.czytajgatunki()
    if self.x in self.gatunki:
        print('Zaznacz z listy gatunków')
    else:
        cur.execute(
            """SELECT id_gat, gatunek FROM GATUNKI""")
        self.gatunek = cur.fetchall()
        self.n = len(self.gatunek)
        cur.execute("INSERT INTO GATUNKI VALUES(?,?)", (self.n + 1, self.x))

jula = baza_danych.Baza()
jula.czytajdane()

conn.commit()
cur.close()
conn.close()
