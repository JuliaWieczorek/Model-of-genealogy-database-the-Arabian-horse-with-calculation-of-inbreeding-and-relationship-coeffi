import baza_danych
import sqlite3

class Zmienne(object):

    conn = sqlite3.connect('baza.db')
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()
    def __init__(self):
        __all__ = [self.hodowcy, self.osobniki, self.gatunki]

    def hodowcy(self):
        return baza_danych.Baza.czytajhodowcow(self)

    def osobniki(self):
        return baza_danych.Baza.czytajdane(self)

    def gatunki(self):
        return baza_danych.Baza.czytajgatunki(self)

jula = Zmienne()
jula.hodowcy()