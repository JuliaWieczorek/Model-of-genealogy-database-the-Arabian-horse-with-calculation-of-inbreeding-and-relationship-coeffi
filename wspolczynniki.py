# -*- coding: cp1250 -*-

import sqlite3
import math
import baza_danych

class Oblicz(object):

    def __main__(self):
        self.menu()
        self.funkcje = {'1': self.all_osobniki, '2': self.find_child1, '3': self.find_parent1, '4': self.find_grand1,
                        '5': self.find_pra1, '6': self.wspolny_przodek1, '7': self.sciezka1, '8': self.tree1,
                        '9': self.inbred1, '10': self.pokrewienstwo1, '11': self.inbred_pokr1}
        self.nazwyFunkcji = {'1': 'all_osobniki', '2': 'znajdujaca potomkow osobnika',
                             '3': 'znajdujaca rodzicow osobnika',
                             '4': 'znajdujaca dziadkow osobika',
                             '5': 'odnajdujaca dziadkow', '6': 'szukajaca wspolnych przodkow',
                             '7': 'funkcje wyznaczajaca sciezke',
                             '8': 'wyznaczajaca drzewo pokolen',
                             '9': 'obliczajaca wspolczynnik inbredu', '10': 'obliczajaca wspolczynnik pokrewienstwa',
                             '11': 'obliczajaca współczynnik inbredu'}
        self.op = input("Co wybierzesz?-> ")
        while self.op != '12':
            if self.op == '2' or self.op == '3' or self.op == '4' or self.op == '5' or self.op == '8' or \
                    self.op == '9' or self.op == '11':
                self.nzw1 = input('Wybierz osobnika: ')
            elif self.op == '7' or self.op == '10' or self.op == '6':
                self.nzw1 = input('Wybierz pierwszego konia: ')
                self.nzw2 = input('Wybierz drugiego konia: ')
            self.wybranaFkcja = self.funkcje.get(self.op, self.blad)
            self.nazwaWybranejFkcji = self.nazwyFunkcji.get(self.op, self.blad)
            print("::::wybrales funkcje {nazwa}::::\n {wynik}".format(nazwa=self.nazwaWybranejFkcji,
                                                                      wynik=self.wybranaFkcja()))
            self.menu()
            self.op = input("Co wybierzesz?-> ")

    def all_osobniki(self):
        baza_danych.Baza.open(self)
        for self.all in baza_danych.Baza.open.cur.execute('SELECT nazwa FROM osobniki'):
            print(self.all)
        baza_danych.Baza.close(self)

    def find_child(self, id1):
        self.id1 = id1
        self.list_of_child = []
        baza_danych.Baza.open(self)
        for row in baza_danych.Baza.open.cur.execute('SELECT id_os1 FROM RELACJE WHERE id_os2=?', (self.id1,)):
            self.nzw = baza_danych.Baza.id_nazwa(self, row)
            self.list_of_child.append(tuple(self.nzw))
        print('Lista dzieci osobnika:', self.list_of_child)
        if len(self.list_of_child) > 0:
            self.count_child = len(self.list_of_child)
            print('Ten osobnik ma %i dzieci' % self.count_child)
        baza_danych.Baza.close(self)

    def find_parent(self, id1):
        self.id = id1
        self.list_of_parents = []
        baza_danych.Baza.open(self)
        for self.row in baza_danych.Baza.open.cur.execute('SELECT id_os2 FROM relacje WHERE id_os1=?', (self.id)):
            self.list_of_parents.append(tuple(self.row))
        baza_danych.Baza.close(self)
        return self.list_of_parents

    def find_grand(self, id1):
        self.id1 = id1
        self.lista = []
        baza_danych.Baza.open(self)
        for self.row in baza_danych.Baza.open.cur.execute(
                'SELECT id_os2 FROM relacje WHERE id_os1 in (SELECT id_os2 FROM relacje WHERE id_os1=?)',
                [self.id1]):
            self.lista.append(self.row)
        baza_danych.Baza.close(self)
        return self.lista

    def find_pra(self, id1):
        self.id1 = id1
        self.lista = []
        baza_danych.Baza.open(self)
        for self.row in baza_danych.Baza.open.cur.execute(
                'SELECT id_os2 FROM relacje WHERE id_os1 in (SELECT id_os2 FROM relacje WHERE id_os1 in (SELECT id_os2 FROM relacje WHERE id_os1=?))',
                [self.id1]):
            self.lista.append(self.row)
        baza_danych.Baza.close(self)
        return self.lista

    def tree(self, nzw):
        self.nzw = nzw
        self.a = self.find_parent(self.nzw)
        self.b = self.find_grand(self.nzw)
        self.c = self.find_pra(self.nzw)
        self.ListTree = []
        for self.i in self.a:
            self.ListTree.append(self.i)
        for self.j in self.b:
            self.ListTree.append(self.j)
        for self.y in self.c:
            self.ListTree.append(self.y)
        return self.ListTree

    def tree2(self, nzw):  #
        self.nzw = nzw
        self.a = self.find_parent(self.nzw)
        self.b = self.find_grand(self.nzw)
        self.c = self.find_pra(self.nzw)
        self.ListTree = []
        self.ListTree.append(self.a)
        self.ListTree.append(self.b)
        self.ListTree.append(self.c)
        return self.ListTree

    def wspolny_przodek(self, nzw1, nzw2):
        self.nzw1 = nzw1
        self.nzw2 = nzw2
        self.x = self.tree(self.nzw1)
        self.y = self.tree(self.nzw2)
        self.wsp = set(self.x) & set(self.y)
        return self.wsp

    def wspolny_przodek2(self, nzw1, nzw2):  #
        self.nzw1 = nzw1
        self.nzw2 = nzw2
        self.x = self.tree2(self.nzw1)
        self.y = self.tree2(self.nzw2)
        self.wsp = [i for i in self.x if i in self.y]
        return self.wsp

    def porownanie(self, nzw1, nzw2):
        self.nzw1 = nzw1
        self.nzw2 = nzw2
        self.a = self.find_parent(self.nzw1)
        self.A = self.find_parent(self.nzw2)
        self.aa = []
        self.aa.extend(self.a)
        self.aa.extend(self.A)
        self.b = self.find_grand(self.nzw1)
        self.B = self.find_grand(self.nzw2)
        self.bb = []
        self.bb.extend(self.b)
        self.bb.extend(self.B)
        self.c = self.find_pra(self.nzw1)
        self.C = self.find_pra(self.nzw2)
        self.cc = []
        self.cc.extend(self.c)
        self.cc.extend(self.C)
        self.wspolny = []
        if (self.a == self.A) and len(self.a) == 2:
            self.wspolny.extend(self.a)
            return self.wspolny
        else:
            self.i = list(set(self.a) & set(self.A))
            self.wspolny.extend(self.i)

        if (len(self.a) > 0 or len(self.A) > 0):
            for self.i in self.aa:
                self.i = self.aa.pop(0)
                self.i = str(self.i[0])
                if (self.i == self.nzw1) or (self.i == self.nzw2):
                    self.wspolny.append(self.i)

        if not self.wspolny:
            if self.b == self.B and len(self.b) == 4:
                self.wspolny.extend(self.b)
                return self.wspolny
            elif (len(self.b) > 0 or len(self.B) > 0):
                for self.i in self.bb:
                    self.i = self.bb.pop(0)
                    self.i = str(self.i[0])
                    if (self.i == self.nzw1) or (self.i == self.nzw2):
                        self.wspolny.append(self.i)
                self.i = list(set(self.b) & set(self.B))
                for self.z in self.b:
                    if self.b.count(self.z) > 1:
                        self.wspolny.append(self.z)
                for self.z in self.B:
                    if self.B.count(self.z) > 1:
                        self.wspolny.append(self.z)
                self.wspolny.extend(self.i)

        if not self.wspolny:

            if self.c == self.C and len(self.c) == 8:
                self.wspolny.extend(self.c)
                return self.wspolny
            elif (len(self.c) > 0 or len(self.C) > 0):
                for self.i in self.cc:
                    self.i = self.cc.pop(0)
                    self.i = str(self.i[0])
                    if (self.i == self.nzw1) or (self.i == self.nzw2):
                        self.wspolny.append(self.i)
            else:
                self.i = list(set(self.c) & set(self.C))
                for self.z in self.c:
                    if self.c.count(self.z) > 1:
                        self.wspolny.append(self.i)
                for self.z in self.C:
                    if self.C.count(self.z) > 1:
                        self.wspolny.append(self.i)
                self.wspolny.extend(self.i)

        if not self.wspolny:
            self.wsp = self.wspolny_przodek(self.nzw1, self.nzw2)
            self.wspolny.extend(self.wsp)
            return self.wspolny
        return self.wspolny

    def porownanie2(self, nzw1, nzw2):
        self.nzw1 = nzw1
        self.nzw2 = nzw2
        self.a = self.find_parent(self.nzw1)
        self.A = self.find_parent(self.nzw2)
        self.b = self.find_grand(self.nzw1)
        self.B = self.find_grand(self.nzw2)
        self.c = self.find_pra(self.nzw1)
        self.C = self.find_pra(self.nzw2)
        self.wspolny = self.porownanie(self.nzw1, self.nzw2)
        self.w = 0
        if not self.wspolny:
            self.nzw1 = str(self.nzw1)
            self.nzw1 = (self.nzw1,)
            self.nzw2 = str(self.nzw2)
            self.nzw2 = (self.nzw2,)
            for self.i in self.a:
                if (self.nzw1 == self.i) or (self.nzw2 == self.i):
                    self.w += 1
            for self.i in self.A:
                if (self.nzw1 == self.i) or (self.nzw2 == self.i):
                    self.w += 1
            for self.i in self.b:
                if (self.nzw1 == self.i) or (self.nzw2 == self.i):
                    self.w += 2
            for self.i in self.B:
                if (self.nzw1 == self.i) or (self.nzw2 == self.i):
                    self.w += 2
            for self.i in self.c:
                if (self.nzw1 == self.i) or (self.nzw2 == self.i):
                    self.w += 3
            for self.i in self.C:
                if (self.nzw1 == self.i) or (self.nzw2 == self.i):
                    self.w += 3
        return self.w

    def sciezka(self, nzw1, nzw2):
        self.nzw1 = nzw1
        self.nzw2 = nzw2
        self.Y = self.wspolny_przodek(self.nzw1, self.nzw2)
        self.full = []
        for self.i in range(len(self.Y)):
            self.cos = self.Y.pop()
            self.wsp_a = 0
            self.wsp_b = 0
            self.wsp_c = 0
            self.A = self.find_parent(self.nzw1)
            self.B = self.find_parent(self.nzw2)
            self.C = self.find_grand(self.nzw1)
            self.D = self.find_grand(self.nzw2)
            self.E = self.find_pra(self.nzw1)
            self.F = self.find_pra(self.nzw2)
            for self.a in self.A:
                self.a = self.A.pop()
                if self.a == self.cos:
                    self.wsp_a += 1
                    for self.b in self.B:
                        self.b = self.B.pop()
                        if self.b == self.cos:
                            self.wsp_a += 1
                        elif self.b != self.cos:
                            break
                    for self.d in self.D:
                        self.d = self.D.pop()
                        if self.d == self.cos:
                            self.wsp_a += 2
                        elif self.d != self.cos:
                            break
                    for self.f in self.F:
                        self.f = self.F.pop()
                        if self.f == self.cos:
                            self.wsp_a += 3
                        elif self.f != self.cos:
                            break
                elif self.a != self.cos:
                    break
                self.full.append(self.wsp_a)
            for self.c in self.C:
                self.c = self.C.pop()
                if self.c == self.cos:
                    self.wsp_b += 2
                    for self.b in self.B:
                        self.b = self.B.pop()
                        if self.b == self.cos:
                            self.wsp_b += 1
                        elif self.b != self.cos:
                            break
                    for self.d in self.D:
                        self.d = self.D.pop()
                        if self.d == self.cos:
                            self.wsp_b += 2
                        elif self.d != self.cos:
                            break
                    for self.f in self.F:
                        self.f = self.F.pop()
                        if self.f == self.cos:
                            self.wsp_b += 3
                        elif self.f != self.cos:
                            break
                elif self.c != self.cos:
                    break
                self.full.append(self.wsp_b)
            for self.e in self.E:
                self.e = self.E.pop()
                if self.e == self.cos:
                    self.wsp_c += 3
                    for self.b in self.B:
                        self.b = self.B.pop()
                        if self.b == self.cos:
                            self.wsp_c += 1
                        elif self.b != self.cos:
                            break
                    for self.d in self.D:
                        self.d = self.D.pop()
                        if self.d == self.cos:
                            self.wsp_c += 2
                        elif self.d != self.cos:
                            break
                    for self.f in self.F:
                        self.f = self.F.pop()
                        if self.f == self.cos:
                            self.wsp_c += 3
                        elif self.f != self.cos:
                            break
                elif self.e != self.cos:
                    break
                self.full.append(self.wsp_c)
        self.full = self.full[0:len(self.full) / 2]
        return self.full

    def sciezka_konkretna(self, nzw1, nzw2, cos):  # zamiany!
        self.nzw1 = nzw1
        self.nzw2 = nzw2
        self.cos = cos
        if type(self.cos) == str:
            self.cos = (self.cos,)
        self.full = []
        self.wsp_a = 0
        self.wsp_b = 0
        self.wsp_b_1 = 0
        self.wsp_c = 0
        self.wsp_c_1 = 0
        self.wsp_c_2 = 0
        self.wsp_c_3 = 0
        self.wsp_c_4 = 0
        self.wsp_c_5 = 0
        self.wsp_c_6 = 0
        self.wsp_c_7 = 0
        self.wsp_c_8 = 0
        self.wsp_c_9 = 0
        self.wsp_c_10 = 0
        self.wsp_c_11 = 0
        self.wsp_c_12 = 0
        self.wsp_c_13 = 0
        self.wsp_c_14 = 0
        self.wsp_c_15 = 0
        self.wsp_d_1 = 0
        self.wsp_d_2 = 0
        self.wsp_d_3 = 0
        self.wsp_d_4 = 0
        self.wsp_d_5 = 0
        self.wsp_d_6 = 0
        self.wsp_d_7 = 0
        self.wsp_d_8 = 0
        self.wsp_d_9 = 0
        self.wsp_d_10 = 0
        self.wsp_d_11 = 0
        self.wsp_d_12 = 0
        self.wsp_d_13 = 0
        self.wsp_d_14 = 0
        self.wsp_d_15 = 0
        self.wsp_d_16 = 0
        self.la = 0
        self.lb = 0
        self.lc = 0
        self.ld = 0
        self.le = 0
        self.lf = 0
        self.A = self.find_parent(self.nzw1)
        self.B = self.find_parent(self.nzw2)
        self.C = self.find_grand(self.nzw1)
        self.D = self.find_grand(self.nzw2)
        self.E = self.find_pra(self.nzw1)
        self.F = self.find_pra(self.nzw2)
        if self.A or self.B:
            if (self.A == self.B):
                if len(self.A) == 2:
                    for self.a in range(len(self.A)):
                        self.a = self.A.pop(0)
                        self.aa = str(self.a[0])
                        if (self.a == self.cos):
                            self.wsp_a += 2
                elif len(self.A) == 1:
                    for self.a in range(len(self.A)):
                        self.a = self.A.pop(0)
                        self.a = str(self.a[0])
                        if (self.a == self.cos):
                            self.wsp_a += 1
                self.full.append(self.wsp_a)
                for self.i in range(self.full.count(0)):
                    self.full.remove(0)
                if self.full:
                    return self.full
            else:
                for self.a in range(len(self.A)):
                    for self.b in range(len(self.B)):
                        self.a = self.A.pop(0)
                        self.aa = str(self.a[0])
                        self.b = self.B.pop(0)
                        self.bb = str(self.b[0])
                        if (self.a == self.cos) and (self.b == self.cos):
                            self.wsp_a += 2
                        elif (self.a == self.cos) or (self.b == self.cos):
                            self.wsp_a += 1
                self.full.append(self.wsp_a)
            for self.i in range(self.full.count(0)):
                self.full.remove(0)
            if self.full:
                return self.full
        if not self.full:
            if self.C or self.D:
                if (self.C == self.D):
                    for self.c in range(len(self.C)):
                        self.c = self.C.pop(0)
                        self.c = str(self.c[0])
                        if (self.c == self.cos):
                            self.wsp_b += 4
                        self.full.append(self.wsp_b)
            if self.E or self.F:
                if (self.E == self.F):
                    for self.e in range(len(self.E)):
                        self.e = self.E.pop(0)
                        self.e = str(self.e[0])
                        if (self.e == self.cos):
                            self.wsp_c += 6
                        self.full.append(self.wsp_c)

        self.z = max(len(self.A), len(self.B), len(self.C), len(self.D), len(self.E), len(self.F))
        lista = [self.A, self.B, self.C, self.D, self.E, self.F]
        for self.l in self.lista:
            for self.l in self.lista:
                if len(self.l) < self.z:
                    self.l.extend([0])

        self.lista_index = []
        for self.l in self.lista:
            for self.i in self.l:
                if (self.i == self.cos):
                    self.index = self.lista.index(self.l)
                    self.lista_index.append(self.index)
        self.lista_index = list(set(self.lista_index))
        self.lista_wszystkiego = []
        self.lista_rodzicow = []
        self.lista_dziadkow = []
        self.lista_pra = []
        if len(self.lista_index) > 0:
            for self.a in range(len(self.lista_index)):
                self.i = self.lista_index.pop()
                if (self.i == 0) or (self.i == 1):
                    self.lista_rodzicow.append(self.i)
                elif (self.i == 2) or (self.i == 3):
                    self.lista_dziadkow.append(self.i)
                elif (self.i == 4) or (self.i == 5):
                    self.lista_pra.append(self.i)
            self.lista_wszystkiego.append(self.lista_rodzicow)
            self.lista_wszystkiego.append(self.lista_dziadkow)
            self.lista_wszystkiego.append(self.lista_pra)
            for self.a in range(len(self.lista_wszystkiego)):
                for self.b in self.lista_wszystkiego:
                    if not self.b:
                        self.lista_wszystkiego.remove(self.b)

            if len(self.lista_wszystkiego) == 1:
                for self.a in range(len(self.lista_wszystkiego)):
                    self.l = self.lista_wszystkiego.pop()
                    if (self.l == [0]) or (self.l == [1]) or (self.l == [0, 1]) or (self.l == [1, 0]):
                        for self.a in range(len(self.A)):
                            for self.b in range(len(self.B)):
                                self.a = self.A.pop(0)
                                self.b = self.B.pop(0)
                                if (self.a == self.cos) and (self.b == self.cos):
                                    self.wsp_a += 2
                                elif (self.a == self.cos) or (self.b == self.cos):
                                    self.wsp_a += 1
                                else:
                                    self.wsp_a += 0
                                    break
                                self.full.append(self.wsp_a)

                    elif (self.l == [2]) or (self.l == [3]) or (self.l == [2, 3]) or (self.l == [3, 2]):
                        for self.c in range(len(self.C)):
                            self.c = self.C.pop(0)
                            if (self.c == self.cos):
                                self.lc += 1
                        for self.d in range(len(self.D)):
                            self.d = self.D.pop(0)
                            if (self.d == self.cos):
                                self.ld += 1
                        if self.lc > 1 and self.ld > 1:
                            self.wsp_b += 4
                            self.wsp_b_1 += 4
                            self.full.extend([self.wsp_b, self.wsp_b_1])
                        elif self.lc > 1 or self.ld > 1:
                            self.wsp_b += 4
                            self.full.append(self.wsp_b)
                        elif self.lc == 1 and self.ld == 1:
                            self.wsp_b += 4
                            self.full.append(self.wsp_b)
                        elif self.lc == 1 or self.ld == 1:
                            self.wsp_b += 2
                            self.full.append(self.wsp_b)
                        else:
                            print('nie ma wsrod dziadkow')

                    elif (self.l == 4) or (self.l == 5) or (self.l == [4, 5]) or (self.l == [5, 4]):
                        for self.e in range(len(self.E)):
                            self.e = self.E.pop()
                            if (self.e == self.cos):
                                self.le += 1
                        for self.f in range(len(self.F)):
                            self.f = self.F.pop(0)
                            if (self.f == self.cos):
                                self.lf += 1
                        if self.le == 4 and self.lf == 4:
                            self.wsp_c += 6
                            self.wsp_c_1 += 6
                            self.wsp_c_2 += 6
                            self.wsp_c_3 += 6
                            self.wsp_c_4 += 6
                            self.wsp_c_5 += 6
                            self.wsp_c_6 += 6
                            self.wsp_c_7 += 6
                            self.wsp_c_8 += 6
                            self.wsp_c_9 += 6
                            self.wsp_c_10 += 6
                            self.wsp_c_11 += 6
                            self.wsp_c_12 += 6
                            self.wsp_c_13 += 6
                            self.wsp_c_14 += 6
                            self.wsp_c_15 += 6
                            self.full.extend([self.wsp_c, self.wsp_c_1, self.wsp_c_2, self.wsp_c_3, self.wsp_c_4,
                                              self.wsp_c_5, self.wsp_c_6, self.wsp_c_7, self.wsp_c_8, self.wsp_c_9,
                                              self.wsp_c_10, self.wsp_c_11, self.wsp_c_12, self.wsp_c_13, self.wsp_c_14,
                                              self.wsp_c_15])
                        elif (self.le == 4 and self.lf == 3) or (self.le == 3 and self.lf == 4):
                            self.wsp_c += 6
                            self.wsp_c_1 += 6
                            self.wsp_c_2 += 6
                            self.wsp_c_3 += 6
                            self.wsp_c_4 += 6
                            self.wsp_c_5 += 5
                            self.wsp_c_6 += 5
                            self.wsp_c_7 += 5
                            self.wsp_c_8 += 5
                            self.full.extend([self.wsp_c, self.wsp_c_1, self.wsp_c_2, self.wsp_c_3, self.wsp_c_4,
                                              self.wsp_c_5, self.wsp_c_6, self.wsp_c_7, self.wsp_c_8])
                        elif (self.le == 4 and self.lf == 2) or (self.le == 2 and self.lf == 4):
                            self.wsp_c += 6
                            self.wsp_c_1 += 6
                            self.wsp_c_2 += 6
                            self.wsp_c_3 += 6
                            self.wsp_c_4 += 6
                            self.wsp_c_5 += 6
                            self.wsp_c_6 += 6
                            self.wsp_c_7 += 6
                            self.full.extend([self.wsp_c, self.wsp_c_1, self.wsp_c_2, self.wsp_c_3, self.wsp_c_4,
                                              self.wsp_c_5, self.wsp_c_6, self.wsp_c_7])
                        elif (self.le == 4 and self.lf == 1) or (self.le == 1 and self.lf == 4):
                            self.wsp_c += 6
                            self.wsp_c_1 += 6
                            self.wsp_c_2 += 6
                            self.wsp_c_3 += 6
                            self.wsp_c_4 += 6
                            self.full.extend([self.wsp_c, self.wsp_c_1, self.wsp_c_2, self.wsp_c_3, self.wsp_c_4])
                        elif (self.le == 4 and self.lf == 0) or (self.le == 0 and self.lf == 4):  # inbred
                            self.wsp_c += 4
                            self.wsp_c_1 += 4
                            self.wsp_c_2 += 4
                            self.wsp_c_3 += 4
                            self.full.extend([self.wsp_c, self.wsp_c_1, self.wsp_c_2, self.wsp_c_3])
                        elif self.le == 3 and self.lf == 3:
                            self.wsp_c += 6
                            self.wsp_c_1 += 6
                            self.wsp_c_2 += 6
                            self.wsp_c_3 += 6
                            self.wsp_c_4 += 6
                            self.wsp_c_5 += 6
                            self.wsp_c_6 += 6
                            self.wsp_c_7 += 6
                            self.wsp_c_8 += 6
                            self.full.extend([self.wsp_c, self.wsp_c_1, self.wsp_c_2, self.wsp_c_3, self.wsp_c_4,
                                              self.wsp_c_5, self.wsp_c_6, self.wsp_c_7, self.wsp_c_8])
                        elif (self.le == 3 and self.lf == 2) or (self.le == 2 and self.lf == 3):
                            self.wsp_c += 6
                            self.wsp_c_1 += 6
                            self.wsp_c_2 += 6
                            self.wsp_c_3 += 6
                            self.wsp_c_4 += 6
                            self.wsp_c_5 += 6
                            self.wsp_c_6 += 6
                            self.full.extend([self.wsp_c, self.wsp_c_1, self.wsp_c_2, self.wsp_c_3, self.wsp_c_4,
                                              self.wsp_c_5, self.wsp_c_6])
                        elif (self.le == 3 and self.lf == 1) or (self.le == 1 and self.lf == 3):
                            self.wsp_c += 6
                            self.wsp_c_1 += 6
                            self.wsp_c_2 += 6
                            self.wsp_c_3 += 0
                            self.full.extend([self.wsp_c, self.wsp_c_1, self.wsp_c_2, self.wsp_c_3])
                        elif (self.le == 3 and self.lf == 0) or (self.le == 0 and self.lf == 3):  # inbred
                            self.wsp_c += 4
                            self.wsp_c_1 += 4
                            self.wsp_c_2 += 2
                            self.full.extend([self.wsp_c, self.wsp_c_1, self.wsp_c_2])
                        elif self.le == 2 and self.lf == 2:
                            self.wsp_c += 6
                            self.wsp_c_1 += 6
                            self.wsp_c_2 += 6
                            self.wsp_c_3 += 6
                            self.full.extend([self.wsp_c, self.wsp_c_1, self.wsp_c_2, self.wsp_c_3])
                        elif (self.le == 2 and self.lf == 1) or (self.le == 1 and self.lf == 2):
                            self.wsp_c += 6
                            self.wsp_c_1 += 6
                            self.wsp_c_2 += 0
                            self.full.extend([self.wsp_c, self.wsp_c_1, self.wsp_c_2])
                        elif (self.le == 2 and self.lf == 0) or (self.le == 0 and self.lf == 2):  # inbred
                            self.wsp_c += 4
                            self.wsp_c_1 += 0
                            self.full.extend([self.wsp_c, self.wsp_c_1])
                        elif self.le == 1 and self.lf == 1:
                            self.wsp_c += 6
                            self.full.append(self.wsp_c)
                        elif (self.le == 1 or self.lf == 0) or (self.le == 0 and self.lf == 1):
                            self.wsp_c += 0
                            self.full.append(self.wsp_c)
                        else:
                            print('nie ma wsrod pradziadkow')
            else:

                # rodzic i dziadek
                if (((self.lista_rodzicow == [0]) and (self.lista_dziadkow == [2]))
                        or ((self.lista_rodzicow == [1]) and (self.lista_dziadkow == [2]))
                        or ((self.lista_rodzicow == [0]) and (self.lista_dziadkow == [3]))
                        or ((self.lista_rodzicow == [1]) and (self.lista_dziadkow == [3]))
                        or ((self.lista_rodzicow == [0]) and (self.lista_dziadkow == [2, 3]))
                        or ((self.lista_rodzicow == [0]) and (self.lista_dziadkow == [3, 2]))
                        or ((self.lista_rodzicow == [1]) and (self.lista_dziadkow == [2, 3]))
                        or ((self.lista_rodzicow == [1]) and (self.lista_dziadkow == [3, 2]))
                        or ((self.lista_rodzicow == [0, 1]) and (self.lista_dziadkow == [2]))
                        or ((self.lista_rodzicow == [1, 0]) and (self.lista_dziadkow == [2]))
                        or ((self.lista_rodzicow == [0, 1]) and (self.lista_dziadkow == [3]))
                        or ((self.lista_rodzicow == [1, 0]) and (self.lista_dziadkow == [3]))
                        or ((self.lista_rodzicow == [0, 1]) and (self.lista_dziadkow == [2, 3]))
                        or ((self.lista_rodzicow == [1, 0] and (self.lista_dziadkow == [2, 3]))
                            or ((self.lista_rodzicow == [0, 1]) and (self.lista_dziadkow == [3, 2]))
                            or ((self.lista_rodzicow == [1, 0]) and (self.lista_dziadkow == [3, 2])))):

                    for self.a in range(len(self.A)):
                        self.a = self.A.pop()
                        if (self.a == self.cos):
                            self.la += 1
                    for self.b in range(len(self.B)):
                        self.b = self.B.pop(0)
                        if (self.b == self.cos):
                            self.lb += 1
                    for self.c in range(len(self.C)):
                        self.c = self.C.pop()
                        if (self.c == self.cos):
                            self.lc += 1
                    for self.d in range(len(self.D)):
                        self.d = self.D.pop(0)
                        if (self.d == self.cos):
                            self.ld += 1

                    if (self.la == 1 and self.lb == 1 and self.lc == 1 and self.ld == 1):  ##
                        self.wsp_d_1 += 4
                        self.wsp_d_2 += 3
                        self.wsp_d_3 += 3
                        self.wsp_d_4 += 2
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4])
                    elif (self.la == 1 and self.lb == 1 and self.lc == 1 and self.ld == 0) or (
                            self.la == 1 and self.lb == 1 and self.lc == 0 and self.ld == 1):  ##
                        self.wsp_d_1 += 3
                        self.wsp_d_2 += 2
                        self.full.extend([self.wsp_d_1, self.wsp_d_2])
                    elif (self.la == 1 and self.lb == 0 and self.lc == 1 and self.ld == 2) or (
                            self.la == 0 and self.lb == 1 and self.lc == 2 and self.ld == 1):  ##
                        self.wsp_d_1 += 4
                        self.wsp_d_2 += 4
                        self.wsp_d_3 += 3
                        self.wsp_d_4 += 3
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4])
                    elif (self.la == 1 and self.lb == 0 and self.lc == 1 and self.ld == 1) or (
                            self.la == 0 and self.lb == 1 and self.lc == 1 and self.ld == 1):  ##
                        self.wsp_d_1 += 4
                        self.wsp_d_2 += 3
                        self.full.extend([self.wsp_d_1, self.wsp_d_2])
                    elif (self.la == 1 and self.lb == 0 and self.lc == 0 and self.ld == 1) or (
                            self.la == 0 and self.lb == 1 and self.lc == 1 and self.ld == 0):  ##
                        self.wsp_d_1 += 3
                        self.full.append(self.wsp_d_1)
                # rodzic i pradziadek
                elif (((self.lista_rodzicow == [0]) and (self.lista_pra == [4]))
                      or ((self.lista_rodzicow == [1]) and (self.lista_pra == [4]))
                      or ((self.lista_rodzicow == [0]) and (self.lista_pra == [5]))
                      or ((self.lista_rodzicow == [1]) and (self.lista_pra == [5]))
                      or ((self.lista_rodzicow == [0]) and (self.lista_pra == [4, 5]))
                      or ((self.lista_rodzicow == [0]) and (self.lista_pra == [5, 4]))
                      or ((self.lista_rodzicow == [1]) and (self.lista_pra == [4, 5]))
                      or ((self.lista_rodzicow == [1]) and (self.lista_pra == [5, 4]))
                      or ((self.lista_rodzicow == [0, 1]) and (self.lista_pra == [4]))
                      or ((self.lista_rodzicow == [1, 0]) and (self.lista_pra == [4]))
                      or ((self.lista_rodzicow == [0, 1]) and (self.lista_pra == [5]))
                      or ((self.lista_rodzicow == [1, 0]) and (self.lista_pra == [5]))
                      or ((self.lista_rodzicow == [0, 1]) and (self.lista_pra == [4, 5]))
                      or ((self.lista_rodzicow == [1, 0]) and (self.lista_pra == [4, 5]))
                      or ((self.lista_rodzicow == [0, 1]) and (self.lista_pra == [5, 4]))
                      or ((self.lista_rodzicow == [1, 0]) and (self.lista_pra == [5, 4]))):
                    for self.a in range(len(self.A)):
                        self.a = self.A.pop()
                        if (self.a == self.cos):
                            self.la += 1
                    for self.b in range(len(self.B)):
                        self.b = self.B.pop(0)
                        if (self.b == self.cos):
                            self.lb += 1
                    for self.e in range(len(self.E)):
                        self.e = self.E.pop()
                        if (self.e == self.cos):
                            self.le += 1
                    for self.f in range(len(self.F)):
                        self.f = self.F.pop(0)
                        if (self.f == self.cos):
                            self.lf += 1

                    if self.la == 1 and self.lb == 1 and self.lc == 2 and self.ld == 2:  ##
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 6
                        self.wsp_d_3 += 4
                        self.wsp_d_4 += 6
                        self.wsp_d_5 += 6
                        self.wsp_d_6 += 4
                        self.wsp_d_7 += 4
                        self.wsp_d_8 += 4
                        self.wsp_d_9 += 2
                        self.full.extend(
                            [self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5, self.wsp_d_6,
                             self.wsp_d_7, self.wsp_d_8, self.wsp_d_9])
                    elif (self.la == 1 and self.lb == 0 and self.lc == 2 and self.ld == 4) or (
                            self.la == 0 and self.lb == 1 and self.lc == 2 and self.ld == 4):  ##
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 6
                        self.wsp_d_3 += 6
                        self.wsp_d_4 += 6

                        self.wsp_d_5 += 6
                        self.wsp_d_6 += 6
                        self.wsp_d_7 += 6
                        self.wsp_d_8 += 6

                        self.wsp_d_9 += 4
                        self.wsp_d_10 += 4
                        self.wsp_d_11 += 4
                        self.wsp_d_12 += 4
                        self.full.extend(
                            [self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5, self.wsp_d_6,
                             self.wsp_d_7, self.wsp_d_8, self.wsp_d_9, self.wsp_d_10, self.wsp_d_11, self.wsp_d_12])
                    elif (self.la == 1 and self.lb == 1 and self.lc == 1 and self.ld == 2) or (
                            self.la == 1 and self.lb == 1 and self.lc == 2 and self.ld == 1):  ##
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 6
                        self.wsp_d_3 += 4
                        self.wsp_d_4 += 4
                        self.wsp_d_5 += 4
                        self.wsp_d_6 += 2
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5,
                                          self.wsp_d_6])
                    elif (self.la == 1 and self.lb == 0 and self.lc == 1 and self.ld == 4) or (
                            self.la == 0 and self.lb == 1 and self.lc == 4 and self.ld == 1):
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 6
                        self.wsp_d_3 += 6
                        self.wsp_d_4 += 6
                        self.wsp_d_5 += 4
                        self.wsp_d_6 += 4
                        self.wsp_d_7 += 4
                        self.wsp_d_8 += 4
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5,
                                          self.wsp_d_6, self.wsp_d_7, self.wsp_d_8])
                    elif (self.la == 1 and self.lb == 1 and self.lc == 2 and self.ld == 0) or (
                            self.la == 1 and self.lb == 1 and self.lc == 0 and self.ld == 2):
                        self.wsp_d_1 += 4
                        self.wsp_d_2 += 4
                        self.wsp_d_3 += 2
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3])
                    elif (self.la == 1 and self.lb == 1 and self.lc == 1 and self.ld == 1):
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 4
                        self.wsp_d_3 += 2
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3])
                    elif (self.la == 1 and self.lb == 1 and self.lc == 1 and self.ld == 0) or (
                            self.la == 1 and self.lb == 1 and self.lc == 0 and self.ld == 1):
                        self.wsp_d_1 += 4
                        self.wsp_d_2 += 2
                        self.full.extend([self.wsp_d_1, self.wsp_d_2])
                    elif (self.la == 1 and self.lb == 0 and self.lc == 2 and self.ld == 3) or (
                            self.la == 0 and self.lb == 1 and self.lc == 3 and self.ld == 2):
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 6
                        self.wsp_d_3 += 6

                        self.wsp_d_4 += 6
                        self.wsp_d_5 += 6
                        self.wsp_d_6 += 6

                        self.wsp_d_7 += 4
                        self.wsp_d_8 += 4
                        self.wsp_d_9 += 4
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5,
                                          self.wsp_d_6, self.wsp_d_7, self.wsp_d_8, self.wsp_d_9])
                    elif (self.la == 1 and self.lb == 0 and self.lc == 2 and self.ld == 2) or (
                            self.la == 0 and self.lb == 1 and self.lc == 2 and self.ld == 2):
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 6

                        self.wsp_d_3 += 6
                        self.wsp_d_4 += 6

                        self.wsp_d_5 += 4
                        self.wsp_d_6 += 4
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5,
                                          self.wsp_d_6])
                    elif ((self.la == 1 and self.lb == 0 and self.lc == 2 and self.ld == 1) or (
                            self.la == 0 and self.lb == 1 and self.lc == 2 and self.ld == 1) or (
                                  self.la == 1 and self.lb == 0 and self.lc == 1 and self.ld == 2) or (
                                  self.la == 0 and self.lb == 1 and self.lc == 1 and self.ld == 2)):
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 6
                        self.wsp_d_3 += 4
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3])
                    elif (self.la == 0 and self.lb == 1 and self.lc == 2 and self.ld == 0) or (
                            self.la == 1 and self.lb == 0 and self.lc == 0 and self.ld == 2):
                        self.wsp_d_1 += 4
                        self.wsp_d_2 += 4
                        self.full.extend([self.wsp_d_1, self.wsp_d_2])
                    elif (self.la == 1 and self.lb == 0 and self.lc == 1 and self.ld == 3) or (
                            self.la == 0 and self.lb == 1 and self.lc == 3 and self.ld == 1):
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 6
                        self.wsp_d_3 += 6
                        self.wsp_d_4 += 4
                        self.wsp_d_5 += 4
                        self.wsp_d_6 += 4
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5,
                                          self.wsp_d_6])
                    elif (self.la == 1 and self.lb == 0 and self.lc == 0 and self.ld == 1) or (
                            self.la == 0 and self.lb == 1 and self.lc == 1 and self.ld == 0):
                        self.wsp_d_1 += 4
                        self.full.append(self.wsp_d_1)

                elif ((((self.lista_dziadkow == [2]) and (self.lista_pra == [4])) or (
                        (self.lista_dziadkow == [3]) and (self.lista_pra == [4])) or (
                               (self.lista_dziadkow == [2]) and (self.lista_pra == [5])) or (
                               (self.lista_dziadkow == [3]) and (self.lista_pra == [5])) or (
                               (self.lista_dziadkow == [2]) and (self.lista_pra == [4, 5])) or (
                               (self.lista_dziadkow == [2]) and (self.lista_pra == [5, 4])) or (
                               (self.lista_dziadkow == [3] and (self.lista_pra == [4, 5])) or (
                               (self.lista_dziadkow == [3] and (self.lista_pra == [5, 4])) or (
                               (self.lista_dziadkow == [2, 3]) and (self.lista_pra == [4])) or (
                                       (self.lista_dziadkow == [3, 2]) and (self.lista_pra == [4])) or (
                                       (self.lista_dziadkow == [2, 3]) and (self.lista_pra == [5])) or (
                                       (self.lista_dziadkow == [3, 2]) and (self.lista_pra == [5])) or (
                                       (self.lista_dziadkow == [2, 3]) and (self.lista_pra == [4, 5])) or (
                                       (self.lista_dziadkow == [3, 2] and (self.lista_pra == [4, 5])) or (
                                       (self.lista_dziadkow == [2, 3]) and (self.lista_pra == [3, 2])) or (
                                               (self.lista_dziadkow == [1, 0]) and (self.lista_pra == [5, 4]))))))):
                    for self.c in range(len(self.C)):
                        self.c = self.C.pop()
                        if (self.c == self.cos):
                            self.lc += 1
                    for self.d in range(len(self.D)):
                        self.d = self.D.pop(0)
                        if (self.d == self.cos):
                            self.ld += 1
                    for self.e in range(len(self.E)):
                        self.e = self.E.pop()
                        if (self.e == self.cos):
                            self.le += 1
                    for self.f in range(len(self.F)):
                        self.f = self.F.pop(0)
                        if (self.f == self.cos):
                            self.lf += 1
                    if ((self.lc == 2) and (self.ld == 2) and (self.le == 2) and (self.lf == 2)):
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 5
                        self.wsp_d_3 += 6
                        self.wsp_d_4 += 5

                        self.wsp_d_5 += 5
                        self.wsp_d_6 += 4
                        self.wsp_d_7 += 5
                        self.wsp_d_8 += 4

                        self.wsp_d_9 += 6
                        self.wsp_d_10 += 5
                        self.wsp_d_11 += 6
                        self.wsp_d_12 += 5

                        self.wsp_d_13 += 5
                        self.wsp_d_14 += 4
                        self.wsp_d_15 += 5
                        self.wsp_d_16 += 4
                        self.full.extend(
                            [self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5, self.wsp_d_6,
                             self.wsp_d_7, self.wsp_d_8, self.wsp_d_9, self.wsp_d_10, self.wsp_d_11, self.wsp_d_12,
                             self.wsp_d_13, self.wsp_d_14, self.wsp_d_15, self.wsp_d_16])
                    elif ((self.lc == 2) and (self.ld == 2) and (self.le == 2) and (self.lf == 1)) or (
                            (self.lc == 2) and (self.ld == 2) and (self.le == 1) and (self.lf == 2)):
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 5
                        self.wsp_d_3 += 5

                        self.wsp_d_4 += 5
                        self.wsp_d_5 += 4
                        self.wsp_d_6 += 4

                        self.wsp_d_7 += 6
                        self.wsp_d_8 += 5
                        self.wsp_d_9 += 5

                        self.wsp_d_10 += 5
                        self.wsp_d_11 += 4
                        self.wsp_d_12 += 4
                        self.full.extend(
                            [self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5, self.wsp_d_6,
                             self.wsp_d_7, self.wsp_d_8, self.wsp_d_9, self.wsp_d_10, self.wsp_d_11, self.wsp_d_12])
                    elif ((self.lc == 2) and (self.ld == 2) and (self.le == 2) and (self.lf == 0)) or (
                            (self.lc == 2) and (self.ld == 2) and (self.le == 0) and (self.lf == 2)):
                        self.wsp_d_1 += 5
                        self.wsp_d_2 += 5

                        self.wsp_d_3 += 4
                        self.wsp_d_4 += 4

                        self.wsp_d_5 += 5
                        self.wsp_d_6 += 5

                        self.wsp_d_7 += 4
                        self.wsp_d_8 += 4
                        self.full.extend(
                            [self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5, self.wsp_d_6,
                             self.wsp_d_7, self.wsp_d_8])
                    elif (((self.lc == 2) and (self.ld == 1) and (self.le == 2) and (self.lf == 3)) or (
                            (self.lc == 2) and (self.ld == 1) and (self.le == 3) and (self.lf == 2))
                          or ((self.lc == 1) and (self.ld == 2) and (self.le == 2) and (self.lf == 3)) or (
                                  (self.lc == 1) and (self.ld == 2) and (self.le == 3) and (self.lf == 2))):
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 5
                        self.wsp_d_3 += 6
                        self.wsp_d_4 += 6

                        self.wsp_d_5 += 5
                        self.wsp_d_6 += 4
                        self.wsp_d_7 += 5
                        self.wsp_d_8 += 5

                        self.wsp_d_9 += 6
                        self.wsp_d_10 += 5
                        self.wsp_d_11 += 6
                        self.wsp_d_12 += 6

                        self.wsp_d_13 += 5
                        self.wsp_d_14 += 4
                        self.wsp_d_15 += 5
                        self.wsp_d_16 += 5
                        self.full.extend(
                            [self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5, self.wsp_d_6,
                             self.wsp_d_7, self.wsp_d_8, self.wsp_d_9, self.wsp_d_10, self.wsp_d_11, self.wsp_d_12,
                             self.wsp_d_13, self.wsp_d_14, self.wsp_d_15, self.wsp_d_16])
                    elif ((self.lc == 2) and (self.ld == 1) and (self.le == 2) and (self.lf == 2)) or (
                            (self.lc == 1) and (self.ld == 2) and (self.le == 2) and (self.lf == 2)):
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 5
                        self.wsp_d_3 += 6

                        self.wsp_d_4 += 5
                        self.wsp_d_5 += 4
                        self.wsp_d_6 += 5

                        self.wsp_d_7 += 6
                        self.wsp_d_8 += 5
                        self.wsp_d_9 += 6

                        self.wsp_d_10 += 5
                        self.wsp_d_11 += 4
                        self.wsp_d_12 += 5
                        self.full.extend(
                            [self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5, self.wsp_d_6,
                             self.wsp_d_7, self.wsp_d_8, self.wsp_d_9, self.wsp_d_10, self.wsp_d_11, self.wsp_d_12])
                    elif (((self.lc == 2) and (self.ld == 1) and (self.le == 2) and (self.lf == 1)) or (
                            (self.lc == 1) and (self.ld == 2) and (self.le == 1) and (self.lf == 2))
                          or ((self.lc == 2) and (self.ld == 1) and (self.le == 1) and (self.lf == 2)) or (
                                  (self.lc == 1) and (self.ld == 2) and (self.le == 2) and (self.lf == 1))):
                        self.wsp_d_1 += 6
                        self.wsp_d_2 += 5

                        self.wsp_d_3 += 5
                        self.wsp_d_4 += 4

                        self.wsp_d_5 += 6
                        self.wsp_d_6 += 5

                        self.wsp_d_7 += 5
                        self.wsp_d_8 += 4
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5,
                                          self.wsp_d_6, self.wsp_d_7, self.wsp_d_8])
                    elif (((self.lc == 2) and (self.ld == 1) and (self.le == 2) and (self.lf == 0)) or (
                            (self.lc == 1) and (self.ld == 2) and (self.le == 0) and (self.lf == 2))
                          or ((self.lc == 2) and (self.ld == 1) and (self.le == 0) and (self.lf == 2)) or (
                                  (self.lc == 1) and (self.ld == 2) and (self.le == 2) and (self.lf == 0))):
                        self.wsp_d_1 += 5
                        self.wsp_d_2 += 4

                        self.wsp_d_3 += 5
                        self.wsp_d_4 += 4
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4])
                    elif ((self.lc == 2) and (self.ld == 1) and (self.le == 1) and (self.lf == 0)) or (
                            (self.lc == 1) and (self.ld == 2) and (self.le == 0) and (self.lf == 1)):
                        self.wsp_d_1 += 4
                        self.wsp_d_2 += 5
                        self.wsp_d_3 += 4
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3])
                    elif ((self.lc == 1) and (self.ld == 2) and (self.le == 1) and (self.lf == 0)) or (
                            (self.lc == 2) and (self.ld == 1) and (self.le == 0) and (self.lf == 1)):  ####
                        self.wsp_d_1 += 4
                        self.wsp_d_2 += 4
                        self.wsp_d_3 += 5
                        self.wsp_d_4 += 5
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4])
                    elif ((self.lc == 2) and (self.ld == 1) and (self.le == 0) and (self.lf == 1)) or (
                            (self.lc == 2) and (self.ld == 1) and (self.le == 1) and (self.lf == 0)):
                        self.wsp_d_1 += 4
                        self.wsp_d_2 += 5
                        self.wsp_d_3 += 4
                        self.wsp_d_4 += 5
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4])
                    elif ((self.lc == 2) and (self.ld == 0) and (self.le == 2) and (self.lf == 4)) or (
                            (self.lc == 0) and (self.ld == 2) and (self.le == 4) and (self.lf == 2)):
                        self.wsp_d_1 += 5
                        self.wsp_d_2 += 5
                        self.wsp_d_3 += 5
                        self.wsp_d_4 += 5

                        self.wsp_d_5 += 6
                        self.wsp_d_6 += 6
                        self.wsp_d_7 += 6
                        self.wsp_d_8 += 6

                        self.wsp_d_9 += 5
                        self.wsp_d_10 += 5
                        self.wsp_d_11 += 5
                        self.wsp_d_12 += 5

                        self.wsp_d_13 += 6
                        self.wsp_d_14 += 6
                        self.wsp_d_15 += 6
                        self.wsp_d_16 += 6
                        self.full.extend(
                            [self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5, self.wsp_d_6,
                             self.wsp_d_7, self.wsp_d_8, self.wsp_d_9, self.wsp_d_10, self.wsp_d_11, self.wsp_d_12,
                             self.wsp_d_13, self.wsp_d_14, self.wsp_d_15, self.wsp_d_16])
                    elif ((self.lc == 2) and (self.ld == 0) and (self.le == 2) and (self.lf == 3)) or (
                            (self.lc == 0) and (self.ld == 2) and (self.le == 3) and (self.lf == 2)):
                        self.wsp_d_1 += 5
                        self.wsp_d_2 += 5
                        self.wsp_d_3 += 5

                        self.wsp_d_4 += 6
                        self.wsp_d_5 += 6
                        self.wsp_d_6 += 6

                        self.wsp_d_7 += 5
                        self.wsp_d_8 += 5
                        self.wsp_d_9 += 5

                        self.wsp_d_10 += 6
                        self.wsp_d_11 += 6
                        self.wsp_d_12 += 6
                        self.full.extend(
                            [self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5, self.wsp_d_6,
                             self.wsp_d_7, self.wsp_d_8, self.wsp_d_9, self.wsp_d_10, self.wsp_d_11, self.wsp_d_12])
                    elif ((self.lc == 2) and (self.ld == 0) and (self.le == 2) and (self.lf == 2)) or (
                            (self.lc == 0) and (self.ld == 2) and (self.le == 2) and (self.lf == 2)):
                        self.wsp_d_1 += 5
                        self.wsp_d_2 += 5

                        self.wsp_d_3 += 6
                        self.wsp_d_4 += 6

                        self.wsp_d_5 += 5
                        self.wsp_d_6 += 5

                        self.wsp_d_7 += 6
                        self.wsp_d_8 += 6
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5,
                                          self.wsp_d_6, self.wsp_d_7, self.wsp_d_8])
                    elif ((self.lc == 2) and (self.ld == 0) and (self.le == 2) and (self.lf == 1)) or (
                            (self.lc == 0) and (self.ld == 2) and (self.le == 1) and (self.lf == 2)):
                        self.wsp_d_1 += 5
                        self.wsp_d_2 += 6
                        self.wsp_d_3 += 5
                        self.wsp_d_4 += 6
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4])
                    elif ((self.lc == 2) and (self.ld == 0) and (self.le == 1) and (self.lf == 2)) or (
                            (self.lc == 0) and (self.ld == 2) and (self.le == 2) and (self.lf == 1)):
                        self.wsp_d_1 += 5
                        self.wsp_d_2 += 5

                        self.wsp_d_3 += 6
                        self.wsp_d_4 += 6

                        self.wsp_d_5 += 5
                        self.wsp_d_6 += 5
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5,
                                          self.wsp_d_6])
                    elif ((self.lc == 1) and (self.ld == 0) and (self.le == 3) and (self.lf == 4)) or (
                            (self.lc == 0) and (self.ld == 1) and (self.le == 4) and (self.lf == 3)):
                        self.wsp_d_1 += 5
                        self.wsp_d_2 += 5
                        self.wsp_d_3 += 5
                        self.wsp_d_4 += 5

                        self.wsp_d_5 += 6
                        self.wsp_d_6 += 6
                        self.wsp_d_7 += 6
                        self.wsp_d_8 += 6

                        self.wsp_d_9 += 6
                        self.wsp_d_10 += 6
                        self.wsp_d_11 += 6
                        self.wsp_d_12 += 6

                        self.wsp_d_13 += 6
                        self.wsp_d_14 += 6
                        self.wsp_d_15 += 6
                        self.wsp_d_16 += 6
                        self.full.extend(
                            [self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5, self.wsp_d_6,
                             self.wsp_d_7, self.wsp_d_8, self.wsp_d_9, self.wsp_d_10, self.wsp_d_11, self.wsp_d_12,
                             self.wsp_d_13, self.wsp_d_14, self.wsp_d_15, self.wsp_d_16])
                    elif ((self.lc == 1) and (self.ld == 0) and (self.le == 3) and (self.lf == 3)) or (
                            (self.lc == 0) and (self.ld == 1) and (self.le == 3) and (self.lf == 3)):
                        self.wsp_d_1 += 5
                        self.wsp_d_2 += 5
                        self.wsp_d_3 += 5

                        self.wsp_d_4 += 6
                        self.wsp_d_5 += 6
                        self.wsp_d_6 += 6

                        self.wsp_d_7 += 6
                        self.wsp_d_8 += 6
                        self.wsp_d_9 += 6

                        self.wsp_d_10 += 6
                        self.wsp_d_11 += 6
                        self.wsp_d_12 += 6
                        self.full.extend(
                            [self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5, self.wsp_d_6,
                             self.wsp_d_7, self.wsp_d_8, self.wsp_d_9, self.wsp_d_10, self.wsp_d_11, self.wsp_d_12])
                    elif ((self.lc == 1) and (self.ld == 0) and (self.le == 2) and (self.lf == 3)) or (
                            (self.lc == 0) and (self.ld == 1) and (self.le == 3) and (self.lf == 2)):
                        self.wsp_d_1 += 5
                        self.wsp_d_2 += 5
                        self.wsp_d_3 += 5

                        self.wsp_d_4 += 6
                        self.wsp_d_5 += 6
                        self.wsp_d_6 += 6

                        self.wsp_d_7 += 6
                        self.wsp_d_8 += 6
                        self.wsp_d_9 += 6
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5,
                                          self.wsp_d_6, self.wsp_d_7, self.wsp_d_8, self.wsp_d_9])
                    elif ((self.lc == 1) and (self.ld == 0) and (self.le == 3) and (self.lf == 2)) or (
                            (self.lc == 0) and (self.ld == 1) and (self.le == 2) and (self.lf == 3)):
                        self.wsp_d_1 += 5
                        self.wsp_d_2 += 5

                        self.wsp_d_3 += 6
                        self.wsp_d_4 += 6

                        self.wsp_d_5 += 6
                        self.wsp_d_6 += 6

                        self.wsp_d_7 += 6
                        self.wsp_d_8 += 6
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4, self.wsp_d_5,
                                          self.wsp_d_6, self.wsp_d_7, self.wsp_d_8])
                    elif ((self.lc == 1) and (self.ld == 0) and (self.le == 3) and (self.lf == 1)) or (
                            (self.lc == 0) and (self.ld == 1) and (self.le == 1) and (self.lf == 3)):
                        self.wsp_d_1 += 5
                        self.wsp_d_2 += 6
                        self.wsp_d_3 += 6
                        self.wsp_d_4 += 6
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_3, self.wsp_d_4])
                    elif ((self.lc == 1) and (self.ld == 0) and (self.le == 1) and (self.lf == 3)) or (
                            (self.lc == 0) and (self.ld == 1) and (self.le == 3) and (self.lf == 1)):  #
                        self.wsp_d_1 += 5
                        self.wsp_d_2 += 5
                        self.wsp_d_3 += 5

                        self.wsp_d_4 += 6
                        self.wsp_d_5 += 6
                        self.wsp_d_6 += 6
                        self.full.extend([self.wsp_d_1, self.wsp_d_2, self.wsp_d_4, self.wsp_d_5])

        self.FULL = sum(self.full)
        self.full = self.full[0:len(self.full)]
        return self.full

    def inbred(self, nzw):
        self.nzw = nzw
        self.x = self.find_parent(self.nzw)
        if len(self.x) == 2:
            self.a1 = self.x[0]
            self.rodzic1 = str(self.a1[0])
            self.b1 = self.x[1]
            self.rodzic2 = str(self.b1[0])
        else:
            self.F = 0
            return self.F
        self.y = self.porownanie(self.rodzic1, self.rodzic2)
        if self.y:
            for self.i in range(len(self.y)):
                self.w = []
                self.ii = self.y.pop()
                self.ic = str(self.ii[0])
                self.xx = self.find_parent(self.ic)
                if len(self.xx) == 2:
                    self.a1 = self.xx[0]
                    self.rodzic11 = str(self.a1[0])
                    self.b1 = self.xx[1]
                    self.rodzic12 = str(self.b1[0])
                    self.por = self.porownanie(self.rodzic11, self.rodzic12)
                    if self.por:
                        for self.a in range(len(self.por)):
                            self.ai = self.por.pop()
                            self.sy = self.sciezka_konkretna(self.rodzic11, self.rodzic12, self.ai)
                            for self.i in range(self.sy.count(0)):
                                self.sy.remove(0)
                            self.Za = []
                            for self.j in self.sy:
                                self.w = 0.5 ** (self.j + 1)
                                self.Za.append(self.w)
                            self.Fa = sum(self.Za)
                    else:
                        self.Fa = 0
                else:
                    self.Fa = 0
            self.k = self.sciezka_konkretna(self.rodzic1, self.rodzic2, self.ii)
            for self.i in range(self.k.count(0)):
                self.k.remove(0)
            for self.i in range(len(self.k)):
                self.sz = self.k.pop()
                self.szy = (0.5 ** (self.sz + 1)) * (1 + self.Fa)
                self.w.append(self.szy)
        else:
            self.F = 0
            return self.F
        self.F = sum(self.w)
        return self.F

    def pokrewienstwo(self, nzw1, nzw2):
        self.nzw1 = nzw1
        self.nzw2 = nzw2
        self.x = self.porownanie(self.nzw1, self.nzw2)
        self.y = self.porownanie2(self.nzw1, self.nzw2)
        self.w = []
        self.FFF = []
        if self.x:
            for self.i in range(len(self.x)):
                self.w = []
                self.ii = self.x.pop()
                self.ic = str(self.ii[0])
                self.F = self.inbred(self.ic)
                self.k = self.sciezka_konkretna(self.nzw1, self.nzw2, self.ii)
                for self.i in range(self.k.count(0)):
                    self.k.remove(0)
                if len(self.k) > 0:
                    for self.i in range(len(self.k)):
                        self.sz = self.k.pop()
                        self.szy = 0.5 ** self.sz
                        self.w.append(self.szy)
                else:
                    self.szy = 0
                    self.w.append(self.szy)
                self.pi = sum(self.w)
                self.FF = ((self.pi) * (1 + self.F))
                self.FFF.append(self.FF)
        if self.y:
            self.szy = 0.5 ** self.y
            self.w.append(self.szy)
            self.pi = sum(self.w)
            self.FFF.append(self.pi)

        self.FFFF = sum(self.FFF)
        self.Fx = self.inbred(self.nzw1)
        self.Fy = self.inbred(self.nzw2)
        self.f = math.sqrt((1 + self.Fx) * (1 + self.Fy))
        self.X = (self.FFFF / self.f)
        return self.X

    def inbred_pokr(self, nzw):
        self.nzw = nzw
        self.x = self.find_parent(self.nzw)
        if len(self.x) == 2:
            self.a1 = self.x[0]
            self.rodzic1 = str(self.a1[0])
            self.b1 = self.x[1]
            self.rodzic2 = str(self.b1[0])
        else:
            self.F = 0
            return self.F
        self.r = self.pokrewienstwo(self.rodzic1, self.rodzic2)
        self.Fx = self.inbred(self.rodzic1)
        self.Fy = self.inbred(self.rodzic2)
        self.f = math.sqrt((1 + self.Fx) * (1 + self.Fy))
        self.F = (self.r / 2) * self.f
        return self.F

    def blad(self):
        return 'Error menu'

    def find_child1(self):
        return self.find_child(self.nzw1)

    def find_parent1(self):
        return self.find_parent(self.nzw1)

    def find_grand1(self):
        return self.find_grand(self.nzw1)

    def find_pra1(self):
        return self.find_pra(self.nzw1)

    def tree1(self):
        return self.tree(self.nzw1)

    def wspolny_przodek1(self):
        return self.wspolny_przodek(self.nzw1, self.nzw2)

    def sciezka1(self):
        return self.sciezka(self.nzw1, self.nzw2)

    def inbred1(self):
        return self.inbred(self.nzw1)

    def pokrewienstwo1(self):
        return self.pokrewienstwo(self.nzw1, self.nzw2)

    def inbred_pokr1(self):
        return self.inbred_pokr(self.nzw1)

    def menu(self):
        print("::MENU::\n"
              "1 - all_osobniki\n"
              "2 - find_child\n"
              "3 - find_parent\n"
              "4 - find_grand\n"
              "5 - find_pra\n"
              "6 - wspolny_przodek\n"
              "7 - sciezka\n"
              "8 - tree\n"
              "9 - współczynnik inbredu\n"
              "10 - współczynnik pokrewienstwa\n"
              "11 - współczynnik inbredu")


jula = Oblicz()
jula.__main__()
