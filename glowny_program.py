#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import sys


class Program():
    fname = "baza.db"
    # noinspection PyArgumentList
    def __main__(self):
        print("**********MENU**********")
        # główne menu
        print("""
            1. plik
            2. edycja
            3. oblicz""")
        self.wybor1 = input()

        if self.wybor1 == "1":
            # menu - plik
            print("""
                1. otwórz bazę danych
                2. edycja struktury bazy danych
                3. zamnknij bazę danych
                4. zamknij""")

            self.wybor2 = input()

            if self.wybor2 == "1":
                print("""
                    1. otwórz zaimplementowaną bazę danych
                    2. otwórz zewnętrzną bazę danych""")

                self.wybor3 = input()

                if "1" == self.wybor3:

                    import baza
                    if not os.path.isfile(self.fname):
                        conn = sqlite3.connect(self.fname)
                        conn.row_factory = sqlite3.Row
                        cur = conn.cursor()
                        baza.StrukturaBazyDanych.create_table()
                        baza.StrukturaBazyDanych.data_entry_genre()
                        baza.StrukturaBazyDanych.data_entry_relation()
                        baza.StrukturaBazyDanych.data_entry_breeder()
                        baza.StrukturaBazyDanych.data_entry_individual()
                        baza.StrukturaBazyDanych.data_entry_os_hod()
                    else:
                        conn = sqlite3.connect(self.fname)
                        conn.row_factory = sqlite3.Row
                        cur = conn.cursor()
                    conn.commit()
                    cur.close()
                    conn.close()

                elif self.wybor3 == "2":
                    baza = open("C:/Users/julia/Documents/bioinformatyka/semestr VIII/Pracownia_Informatyczna/04.03.2019/baza.db", "rb")
                    self.nazwaBazy = baza.name
                    print("Została otwarta baza: ", self.nazwaBazy)

            elif self.wybor2 == "2":
                print("Tutaj bedzie edycja struktury")

            elif self.wybor2 == "3":
                conn = sqlite3.connect(self.fname) # zmienic
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()

                cur.close()
                conn.close()

            elif self.wybor2 == "4":
                sys.exit()

        elif self.wybor1 == "2":
            # menu - edycja
            print("""
                1. Edycja Gatunku
                2. Edycja Osobnika
                3. Edycja Hodowcy""")

        elif self.wybor1 == "3":
            # menu - oblicz
            print("""
                1. współczynnik inbredu
                2. współczynnik utraty przodków
                3. wspołczynnik pokrewieństwa
                4. średni współczynnik pokrewieństwa""")
        else:
            print("Nie ma takiej funkcji.")


menu = Program()
menu.__main__()
