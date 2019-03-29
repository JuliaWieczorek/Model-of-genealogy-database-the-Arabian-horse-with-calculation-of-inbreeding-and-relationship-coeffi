# -*- coding: cp1250 -*-

import sqlite3
import math

conn = sqlite3.connect('baza.db')
cur = conn.cursor()


def all_osobniki():
    for all in cur.execute('SELECT nazwa FROM osobniki'):
        print(all)


def find_child(nzw1):
    list_of_child = []
    for row in cur.execute('SELECT id_os1 FROM RELACJE WHERE id_os2=?', [nzw1]):
        list_of_child.append(tuple(row))
    print('Lista dzieci osobnika:', list_of_child)
    if len(list_of_child) > 0:
        count_child = len(list_of_child)
        print('Ten osobnik ma %i dzieci' % count_child)


def find_parent(nzw1):
    list_of_parents = []
    for row in cur.execute('SELECT id_os2 FROM relacje WHERE id_os1=?', [nzw1]):
        list_of_parents.append(tuple(row))
    return list_of_parents


def find_grand(nzw1):
    lista = []
    for row in cur.execute('SELECT id_os2 FROM relacje WHERE id_os1 in (SELECT id_os2 FROM relacje WHERE id_os1=?)',
                           [nzw1]):
        lista.append(row)
    return lista


def find_pra(nzw1):
    lista = []
    for row in cur.execute(
            'SELECT id_os2 FROM relacje WHERE id_os1 in (SELECT id_os2 FROM relacje WHERE id_os1 in (SELECT id_os2 FROM relacje WHERE id_os1=?))',
            [nzw1]):
        lista.append(row)
    return lista


def tree(nzw):
    a = find_parent(nzw)
    b = find_grand(nzw)
    c = find_pra(nzw)
    ListTree = []
    for i in a:
        ListTree.append(i)
    for j in b:
        ListTree.append(j)
    for y in c:
        ListTree.append(y)
    return ListTree


def tree2(nzw):  #
    a = find_parent(nzw)
    b = find_grand(nzw)
    c = find_pra(nzw)
    ListTree = []
    ListTree.append(a)
    ListTree.append(b)
    ListTree.append(c)
    return ListTree


def wspolny_przodek(nzw1, nzw2):
    x = tree(nzw1)
    y = tree(nzw2)
    wsp = set(x) & set(y)
    return wsp


def wspolny_przodek2(nzw1, nzw2):  #
    x = tree2(nzw1)
    y = tree2(nzw2)
    wsp = [i for i in x if i in y]
    return wsp


def porownanie(nzw1, nzw2):
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
            if (i == nzw1) or (i == nzw2):
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


def sciezka(nzw1, nzw2):
    Y = wspolny_przodek(nzw1, nzw2)
    full = []
    for i in range(len(Y)):
        cos = Y.pop()
        wsp_a = 0
        wsp_b = 0
        wsp_c = 0
        A = find_parent(nzw1)
        B = find_parent(nzw2)
        C = find_grand(nzw1)
        D = find_grand(nzw2)
        E = find_pra(nzw1)
        F = find_pra(nzw2)
        for a in A:
            a = A.pop()
            if a == cos:
                wsp_a += 1
                for b in B:
                    b = B.pop()
                    if b == cos:
                        wsp_a += 1
                    elif b != cos:
                        break
                for d in D:
                    d = D.pop()
                    if d == cos:
                        wsp_a += 2
                    elif d != cos:
                        break
                for f in F:
                    f = F.pop()
                    if f == cos:
                        wsp_a += 3
                    elif f != cos:
                        break
            elif a != cos:
                break
            full.append(wsp_a)
        for c in C:
            c = C.pop()
            if c == cos:
                wsp_b += 2
                for b in B:
                    b = B.pop()
                    if b == cos:
                        wsp_b += 1
                    elif b != cos:
                        break
                for d in D:
                    d = D.pop()
                    if d == cos:
                        wsp_b += 2
                    elif d != cos:
                        break
                for f in F:
                    f = F.pop()
                    if f == cos:
                        wsp_b += 3
                    elif f != cos:
                        break
            elif c != cos:
                break
            full.append(wsp_b)
        for e in E:
            e = E.pop()
            if e == cos:
                wsp_c += 3
                for b in B:
                    b = B.pop()
                    if b == cos:
                        wsp_c += 1
                    elif b != cos:
                        break
                for d in D:
                    d = D.pop()
                    if d == cos:
                        wsp_c += 2
                    elif d != cos:
                        break
                for f in F:
                    f = F.pop()
                    if f == cos:
                        wsp_c += 3
                    elif f != cos:
                        break
            elif e != cos:
                break
            full.append(wsp_c)
    full = full[0:len(full) / 2]
    return full


def sciezka_konkretna(nzw1, nzw2, cos):
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
    A = find_parent(nzw1)
    B = find_parent(nzw2)
    C = find_grand(nzw1)
    D = find_grand(nzw2)
    E = find_pra(nzw1)
    F = find_pra(nzw2)
    if A or B:
        if (A == B):
            if len(A) == 2:
                for a in range(len(A)):
                    a = A.pop(0)
                    aa = str(a[0])
                    if (a == cos):
                        wsp_a += 2
            elif len(A) == 1:
                for a in range(len(A)):
                    a = A.pop(0)
                    a = str(a[0])
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
                    a = A.pop(0)
                    aa = str(a[0])
                    b = B.pop(0)
                    bb = str(b[0])
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
                    c = C.pop(0)
                    c = str(c[0])
                    if (c == cos):
                        wsp_b += 4
                    full.append(wsp_b)
        if E or F:
            if (E == F):
                for e in range(len(E)):
                    e = E.pop(0)
                    e = str(e[0])
                    if (e == cos):
                        wsp_c += 6
                    full.append(wsp_c)

    z = max(len(A), len(B), len(C), len(D), len(E), len(F))
    lista = [A, B, C, D, E, F]
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
                lista_dziadkow
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
                    for f in range(len(F)):
                        f = F.pop(0)
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
                        full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3, wsp_c_4, wsp_c_5,
                                     wsp_c_6, wsp_c_7, wsp_c_8, wsp_c_9, wsp_c_10, wsp_c_11,
                                     wsp_c_12, wsp_c_13, wsp_c_14, wsp_c_15])
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
                        full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3, wsp_c_4, wsp_c_5,
                                     wsp_c_6, wsp_c_7, wsp_c_8])
                    elif (le == 4 and lf == 2) or (le == 2 and lf == 4):
                        wsp_c += 6
                        wsp_c_1 += 6
                        wsp_c_2 += 6
                        wsp_c_3 += 6
                        wsp_c_4 += 6
                        wsp_c_5 += 6
                        wsp_c_6 += 6
                        wsp_c_7 += 6
                        full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3, wsp_c_4, wsp_c_5,
                                     wsp_c_6, wsp_c_7])
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
                        full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3, wsp_c_4, wsp_c_5,
                                     wsp_c_6, wsp_c_7, wsp_c_8])
                    elif (le == 3 and lf == 2) or (le == 2 and lf == 3):
                        wsp_c += 6
                        wsp_c_1 += 6
                        wsp_c_2 += 6
                        wsp_c_3 += 6
                        wsp_c_4 += 6
                        wsp_c_5 += 6
                        wsp_c_6 += 6
                        full.extend([wsp_c, wsp_c_1, wsp_c_2, wsp_c_3, wsp_c_4, wsp_c_5,
                                     wsp_c_6])
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
                elif (la == 1 and lb == 1 and lc == 1 and ld == 0) or (la == 1 and lb == 1 and lc == 0 and ld == 1):  ##
                    wsp_d_1 += 3
                    wsp_d_2 += 2
                    full.extend([wsp_d_1, wsp_d_2])
                elif (la == 1 and lb == 0 and lc == 1 and ld == 2) or (la == 0 and lb == 1 and lc == 2 and ld == 1):  ##
                    wsp_d_1 += 4
                    wsp_d_2 += 4
                    wsp_d_3 += 3
                    wsp_d_4 += 3
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4])
                elif (la == 1 and lb == 0 and lc == 1 and ld == 1) or (la == 0 and lb == 1 and lc == 1 and ld == 1):  ##
                    wsp_d_1 += 4
                    wsp_d_2 += 3
                    full.extend([wsp_d_1, wsp_d_2])
                elif (la == 1 and lb == 0 and lc == 0 and ld == 1) or (la == 0 and lb == 1 and lc == 1 and ld == 0):  ##
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
                for f in range(len(F)):
                    f = F.pop(0)
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
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9])
                elif (la == 1 and lb == 0 and lc == 2 and ld == 4) or (la == 0 and lb == 1 and lc == 2 and ld == 4):  ##
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
                        [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10,
                         wsp_d_11, wsp_d_12])
                elif (la == 1 and lb == 1 and lc == 1 and ld == 2) or (la == 1 and lb == 1 and lc == 2 and ld == 1):  ##
                    wsp_d_1 += 6
                    wsp_d_2 += 6
                    wsp_d_3 += 4
                    wsp_d_4 += 4
                    wsp_d_5 += 4
                    wsp_d_6 += 2
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6])
                elif (la == 1 and lb == 0 and lc == 1 and ld == 4) or (la == 0 and lb == 1 and lc == 4 and ld == 1):
                    wsp_d_1 += 6
                    wsp_d_2 += 6
                    wsp_d_3 += 6
                    wsp_d_4 += 6
                    wsp_d_5 += 4
                    wsp_d_6 += 4
                    wsp_d_7 += 4
                    wsp_d_8 += 4
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8])
                elif (la == 1 and lb == 1 and lc == 2 and ld == 0) or (la == 1 and lb == 1 and lc == 0 and ld == 2):
                    wsp_d_1 += 4
                    wsp_d_2 += 4
                    wsp_d_3 += 2
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3])
                elif (la == 1 and lb == 1 and lc == 1 and ld == 1):
                    wsp_d_1 += 6
                    wsp_d_2 += 4
                    wsp_d_3 += 2
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3])
                elif (la == 1 and lb == 1 and lc == 1 and ld == 0) or (la == 1 and lb == 1 and lc == 0 and ld == 1):
                    wsp_d_1 += 4
                    wsp_d_2 += 2
                    full.extend([wsp_d_1, wsp_d_2])
                elif (la == 1 and lb == 0 and lc == 2 and ld == 3) or (la == 0 and lb == 1 and lc == 3 and ld == 2):
                    wsp_d_1 += 6
                    wsp_d_2 += 6
                    wsp_d_3 += 6

                    wsp_d_4 += 6
                    wsp_d_5 += 6
                    wsp_d_6 += 6

                    wsp_d_7 += 4
                    wsp_d_8 += 4
                    wsp_d_9 += 4
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9])
                elif (la == 1 and lb == 0 and lc == 2 and ld == 2) or (la == 0 and lb == 1 and lc == 2 and ld == 2):
                    wsp_d_1 += 6
                    wsp_d_2 += 6

                    wsp_d_3 += 6
                    wsp_d_4 += 6

                    wsp_d_5 += 4
                    wsp_d_6 += 4
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6])
                elif ((la == 1 and lb == 0 and lc == 2 and ld == 1) or (la == 0 and lb == 1 and lc == 2 and ld == 1) or
                      (la == 1 and lb == 0 and lc == 1 and ld == 2) or (la == 0 and lb == 1 and lc == 1 and ld == 2)):
                    wsp_d_1 += 6
                    wsp_d_2 += 6
                    wsp_d_3 += 4
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3])
                elif (la == 0 and lb == 1 and lc == 2 and ld == 0) or (la == 1 and lb == 0 and lc == 0 and ld == 2):
                    wsp_d_1 += 4
                    wsp_d_2 += 4
                    full.extend([wsp_d_1, wsp_d_2])
                elif (la == 1 and lb == 0 and lc == 1 and ld == 3) or (la == 0 and lb == 1 and lc == 3 and ld == 1):
                    wsp_d_1 += 6
                    wsp_d_2 += 6
                    wsp_d_3 += 6
                    wsp_d_4 += 4
                    wsp_d_5 += 4
                    wsp_d_6 += 4
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6])
                elif (la == 1 and lb == 0 and lc == 0 and ld == 1) or (la == 0 and lb == 1 and lc == 1 and ld == 0):
                    wsp_d_1 += 4
                    full.append(wsp_d_1)

            elif ((((lista_dziadkow == [2]) and (lista_pra == [4]))
                   or ((lista_dziadkow == [3]) and (lista_pra == [4]))
                   or ((lista_dziadkow == [2]) and (lista_pra == [5]))
                   or ((lista_dziadkow == [3]) and (lista_pra == [5]))
                   or ((lista_dziadkow == [2]) and (lista_pra == [4, 5]))
                   or ((lista_dziadkow == [2]) and (lista_pra == [5, 4]))
                   or ((lista_dziadkow == [3] and (lista_pra == [4, 5]))
                       or ((lista_dziadkow == [3] and (lista_pra == [5, 4]))
                           or ((lista_dziadkow == [2, 3]) and (lista_pra == [4]))
                           or ((lista_dziadkow == [3, 2]) and (lista_pra == [4]))
                           or ((lista_dziadkow == [2, 3]) and (lista_pra == [5]))
                           or ((lista_dziadkow == [3, 2]) and (lista_pra == [5]))
                           or ((lista_dziadkow == [2, 3]) and (lista_pra == [4, 5]))
                           or ((lista_dziadkow == [3, 2] and (lista_pra == [4, 5]))
                               or ((lista_dziadkow == [2, 3]) and (lista_pra == [3, 2]))
                               or ((lista_dziadkow == [1, 0]) and (lista_pra == [5, 4]))))))):
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
                for f in range(len(F)):
                    f = F.pop(0)
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
                        [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10,
                         wsp_d_11, wsp_d_12,
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
                        [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10,
                         wsp_d_11, wsp_d_12])
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
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8])
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
                        [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10,
                         wsp_d_11, wsp_d_12,
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
                        [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10,
                         wsp_d_11, wsp_d_12])
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
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8])
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
                        [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10,
                         wsp_d_11, wsp_d_12,
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
                        [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10,
                         wsp_d_11, wsp_d_12])
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
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8])
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
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6])
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
                        [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10,
                         wsp_d_11, wsp_d_12,
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
                        [wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9, wsp_d_10,
                         wsp_d_11, wsp_d_12])
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
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8, wsp_d_9])
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
                    full.extend([wsp_d_1, wsp_d_2, wsp_d_3, wsp_d_4, wsp_d_5, wsp_d_6, wsp_d_7, wsp_d_8])
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


def inbred(nzw):
    x = find_parent(nzw)
    if len(x) == 2:
        a1 = x[0]
        rodzic1 = str(a1[0])
        b1 = x[1]
        rodzic2 = str(b1[0])
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
            ii = x.pop()
            ic = str(ii[0])
            F = inbred(ic)
            k = sciezka_konkretna(nzw1, nzw2, ii)
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


def inbred_pokr(nzw):
    x = find_parent(nzw)
    if len(x) == 2:
        a1 = x[0]
        rodzic1 = str(a1[0])
        b1 = x[1]
        rodzic2 = str(b1[0])
    else:
        F = 0
        return F
    r = pokrewienstwo(rodzic1, rodzic2)
    Fx = inbred(rodzic1)
    Fy = inbred(rodzic2)
    f = math.sqrt((1 + Fx) * (1 + Fy))
    F = (r / 2) * f
    return F


def blad():
    return 'Error menu'


def find_child1():
    return find_child(nzw1)


def find_parent1():
    return find_parent(nzw1)


def find_grand1():
    return find_grand(nzw1)


def find_pra1():
    return find_pra(nzw1)


def tree1():
    return tree(nzw1)


def wspolny_przodek1():
    return wspolny_przodek(nzw1, nzw2)


def sciezka1():
    return sciezka(nzw1, nzw2)


def inbred1():
    return inbred(nzw1)


def pokrewienstwo1():
    return pokrewienstwo(nzw1, nzw2)


def inbred_pokr1():
    return inbred_pokr(nzw1)


def menu():
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


menu()
funkcje = {'1': all_osobniki, '2': find_child1, '3': find_parent1, '4': find_grand1,
           '5': find_pra1, '6': wspolny_przodek1, '7': sciezka1, '8': tree1,
           '9': inbred1, '10': pokrewienstwo1, '11': inbred_pokr1}
nazwyFunkcji = {'1': 'all_osobniki', '2': 'znajdujaca potomkow osobnika', '3': 'znajdujaca rodzicow osobnika',
                '4': 'znajdujaca dziadkow osobika',
                '5': 'odnajdujaca dziadkow', '6': 'szukajaca wspolnych przodkow', '7': 'funkcje wyznaczajaca sciezke',
                '8': 'wyznaczajaca drzewo pokolen',
                '9': 'obliczajaca wspolczynnik inbredu', '10': 'obliczajaca wspolczynnik pokrewienstwa',
                '11': 'obliczajaca współczynnik inbredu'}
op = input("Co wybierzesz?-> ")
while op != '12':
    if op == '2' or op == '3' or op == '4' or op == '5' or op == '8' or op == '9' or op == '11':
        nzw1 = input('Wybierz osobnika: ')
    elif op == '7' or op == '10' or op == '6':
        nzw1 = input('Wybierz pierwszego konia: ')
        nzw2 = input('Wybierz drugiego konia: ')
    wybranaFkcja = funkcje.get(op, blad)
    nazwaWybranejFkcji = nazwyFunkcji.get(op, blad)
    print("::::wybrales funkcje {nazwa}::::\n {wynik}".format(nazwa=nazwaWybranejFkcji, wynik=wybranaFkcja()))
    menu()
    op = input("Co wybierzesz?-> ")
