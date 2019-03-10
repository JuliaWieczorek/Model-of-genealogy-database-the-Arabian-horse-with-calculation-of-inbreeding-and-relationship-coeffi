# -*- coding: cp1250 -*-

import sqlite3


conn = sqlite3.connect('baza.db')
conn.execute("PRAGMA foreign_keys = 1")
cur = conn.cursor()

# rows = conn.execute('pragma foreign_keys')
# for row in rows:
#    print(row)

class StrukturaBazyDanych():

    def __init__(self):
        __all__ = [self.drop(), self.create_table(), self.data_entry_genre(),
                   self.data_entry_individual(), self.data_entry_os_hod(),
                   self.data_entry_breeder(), self.data_entry_relation()]

    def drop(self):
        cur.execute("""DROP TABLE  GATUNKI""")
        cur.execute("""DROP TABLE  OSOBNIKI""")
        cur.execute("""DROP TABLE  RELACJE""")
        cur.execute("""DROP TABLE  OSOBNIKI_HODOWCY""")
        cur.execute("""DROP TABLE  HODOWCY""")
        conn.commit()


    def create_table(self):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS GATUNKI (
        id_gat int NOT NULL,
        gatunek varchar(255),
        PRIMARY KEY (id_gat));""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS OSOBNIKI (
        id_os int(10) NOT NULL,
        nazwa varchar(255),
        plec varchar(255) NOT NULL,
        id_gat int NOT NULL,
        id_hod int,
        PRIMARY KEY (id_os),
        FOREIGN KEY (id_hod) REFERENCES HODOWCY(id_hod));""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS RELACJE (
        id_os1 int,
        id_os2 int,
        PRIMARY KEY (id_os1, id_os2)); """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS HODOWCY (
        id_hod int NOT NULL,
        imie varchar(255),
        nazwisko varchar(255),
        PRIMARY KEY (id_hod))""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS OSOBNIKI_HODOWCY (
        id_os int NOT NULL,
        id_hod int NOT NULL,
        FOREIGN KEY (id_os) REFERENCES OSOBNIKI(id_os),
        FOREIGN KEY (id_hod) REFERENCES HODOWCY(id_hod))""")


    def data_entry_genre(self):
        """ Wpisuje dane do encji GATUNKI """
        cur.execute("INSERT INTO GATUNKI VALUES(1,'psy')")
        cur.execute("INSERT INTO GATUNKI VALUES(2,'koty')")
        conn.commit()


    def data_entry_relation(self):
        """Wpisuje dane do relacji"""
        self.relacje = [(106, 122), (107, 122), (108, 123), (109, 123), (110, 124), (111, 124), (112, 125), (113, 125),
                   (114, 118), (115, 118), (116, 119),
                   (117, 119), (120, 127), (121, 127), (122, 128), (123, 128), (124, 129), (125, 129), (118, 126),
                   (119, 126), (126, 126), (127, 130), (149, 107),
                   (149, 135), (150, 136), (150, 137), (86, 138), (86, 139), (87, 140), (87, 141), (152, 142), (152, 143),
                   (153, 121), (153, 144), (138, 145),
                   (138, 146), (154, 147), (154, 148), (96, 149), (96, 150), (97, 86), (97, 87), (157, 152), (157, 153),
                   (114, 138), (114, 154), (158, 96),
                   (158, 97), (159, 157), (159, 114)]
        cur.executemany("INSERT INTO RELACJE(id_os1, id_os2) VALUES (?, ?)", self.relacje)
        conn.commit()


    def data_entry_breeder(self):
        """Wpisuje informacje o hodowcy"""
        cur.execute("INSERT INTO HODOWCY VALUES(1, 'Jan', 'Kowalski')")
        cur.execute("INSERT INTO HODOWCY VALUES(2, 'Robert', 'Nowak')")
        cur.execute("INSERT INTO HODOWCY VALUES(3, 'Maria', 'Anna')")
        conn.commit()


    def data_entry_individual(self):
        """Wpisuje informacje o osobnikach"""
        self.osobniki = [(1, 'KARO', 'samiec', 2, 1), (2, 'KONY', 'samica', 2, 2), (3, 'FERRO', 'samiec', 2, 3),
                    (4, 'GLORIA', 'samica', 2, 3), (5, 'ARNO', 'samiec', 2, 1),
                    (6, 'ELISA', 'samica', 2, 3), (7, 'BERRY', 'samiec', 2, 3), (8, 'BESSI', 'samica', 2, 1),
                    (9, 'ZIK 64544', 'samiec', 2, 3), (10, 'CEDA 64706', 'samica', 2, 2),
                    (11, 'BATT', 'samiec', 2, 1), (12, 'BETY', 'samica', 2, 2), (13, 'CARO', 'samiec', 2, 3),
                    (14, 'ISA', 'samica', 2, 1), (15, 'BAZI', 'samiec', 2, 1),
                    (16, 'DISTEL', 'samica', 2, 3), (17, 'CEKIN 05838', 'samiec', 2, 1), (18, 'ALI', 'samica', 2, 2),
                    (19, 'GUSTEL', 'samiec', 2, 3), (20, 'EMMA', 'samica', 2, 1),
                    (21, 'KARON', 'samiec', 2, 1), (22, 'G E Fido', 'samiec', 2, 2), (23, 'ANJA', 'samica', 2, 3),
                    (24, 'A F Gorky', 'samiec', 2, 2), (25, 'ALF', 'samiec', 2, 1),
                    (26, 'HELLA 15036', 'samica', 2, 2), (27, 'MERKO', 'samiec', 2, 3), (28, 'BIRKA', 'samica', 2, 3),
                    (29, 'JACKEL', 'samiec', 2, 2), (30, 'ELLA', 'samica', 2, 1),
                    (31, 'BELLO', 'samiec', 2, 1), (32, 'KUNDL', 'samica', 2, 2), (33, 'ARKO', 'samiec', 2, 3),
                    (34, 'ADA', 'samica', 2, 3), (35, 'DAGO', 'samiec', 2, 2),
                    (36, 'BELLA', 'samica', 2, 1), (37, 'DUNAO', 'samiec', 2, 2), (38, 'BETI', 'samica', 2, 3),
                    (39, 'ALDO', 'samiec', 2, 3), (40, 'JASNA 60003', 'samica', 2, 2),
                    (41, 'HEIFER 41581', 'samiec', 2, 1), (42, 'BONITA 41541', 'samica', 2, 2),
                    (43, 'ANDERL', 'samiec', 2, 3), (44, 'CHECKY', 'samica', 2, 1), (45, 'HARALD', 'samiec', 2, 2),
                    (46, 'DOSSI', 'samiec', 2, 3), (47, 'BOSKO 60034', 'samica', 2, 1),
                    (48, 'BISTRA 60088', 'samiec', 2, 2), (49, 'BALDER', 'samica', 2, 3), (50, 'AGDA', 'samiec', 2, 1),
                    (51, 'GSELL', 'samica', 2, 2), (52, 'BORA', 'samiec', 2, 3), (53, 'FRENDE', 'samica', 2, 3),
                    (54, 'IDUN', 'samiec', 2, 2), (55, 'CYKLON', 'samica', 2, 1),
                    (56, 'BENNO', 'samiec', 2, 1), (57, 'DOLF', 'samiec', 2, 1), (58, 'BURSCH', 'samiec', 2, 1),
                    (59, 'CENO', 'samiec', 2, 2), (60, 'CORA', 'samica', 2, 2),
                    (61, 'HASAN', 'samiec', 2, 2), (62, 'AINAVALMIS 4427U', 'samica', 2, 3), (63, 'NDERL', 'samiec', 2, 3),
                    (64, 'ANDY 18523E', 'samiec', 2, 3), (65, 'BADCIBI 19356V', 'samica', 2, 2),
                    (66, 'PAN', 'samiec', 2, 2), (67, 'WEGA', 'samica', 2, 2), (68, 'ULJAS 5533K', 'samiec', 2, 1),
                    (69, 'MINKA', 'samiec', 2, 1), (70, 'GENESIS', 'samica', 2, 1),
                    (71, 'EGO', 'samiec', 2, 2), (72, 'CAMELIA', 'samica', 2, 2), (73, 'XEROCH 14172', 'samiec', 2, 2),
                    (74, 'SAGA', 'samica', 2, 1), (75, 'HEKLA', 'samica', 2, 1),
                    (76, 'GLEN', 'samiec', 2, 1), (77, 'AXA', 'samica', 2, 2), (78, 'CESAR', 'samiec', 2, 2),
                    (79, 'ELA', 'samica', 2, 3), (80, 'GERO', 'samiec', 2, 1),
                    (81, 'ASTA', 'samica', 2, 3), (82, 'ZAK', 'samiec', 2, 2), (83, 'ELZA', 'samica', 2, 1),
                    (84, 'KARISSO', 'samiec', 2, 2), (85, 'SAMBA', 'samica', 2, 3),
                    (86, 'AKIL', 'samiec', 2, 1), (87, 'TEQUILLA', 'samica', 2, 2), (88, 'CIT', 'samiec', 2, 2),
                    (89, 'GINESS', 'samica', 2, 3), (90, 'BRAVO', 'samiec', 2, 1),
                    (91, 'CZIKA', 'samica', 2, 2), (92, 'ARGO', 'samiec', 2, 1), (93, 'AFRA', 'samica', 2, 2),
                    (94, 'IROS', 'samiec', 2, 3), (95, 'FANNY', 'samica', 2, 1),
                    (96, 'SKY', 'samiec', 2, 2), (97, 'KAZBACH BEZA', 'samica', 2, 2), (98, 'CHOCOLATE', 'samiec', 2, 3),
                    (99, 'KIRA', 'samica', 2, 1),
                    (100, 'ASTOR', 'samiec', 2, 2), (101, 'JETTY', 'samica', 2, 3), (102, 'WYCIOR', 'samiec', 2, 1),
                    (103, 'LUFA', 'samica', 2, 2), (104, 'VOR', 'samiec', 2, 3), (105, 'FLINTA', 'samica', 2, 2),
                    (106, 'KLIF', 'samiec', 2, 1), (107, 'DONI', 'samiec', 3, 2), (108, 'SONIA', 'samica', 3, 2),
                    (109, 'AGAT', 'samiec', 3, 1), (110, 'FIGLARA', 'samica', 3, 1),
                    (111, 'GERO', 'samiec', 3, 2), (112, 'GINESS', 'samica', 3, 1), (113, 'ARO', 'samiec', 3, 3),
                    (114, 'FANTA', 'samica', 3, 3), (115, 'AGIN', 'samiec', 3, 3),
                    (116, 'HELDA', 'samica', 3, 2), (117, 'DAG', 'samiec', 3, 1), (118, 'CITA', 'samica', 3, 1),
                    (119, 'BRUNO', 'samiec', 3, 1), (120, 'CINDY', 'samica', 3, 2),
                    (121, 'AMIGO', 'samiec', 3, 2), (122, 'GORA', 'samica', 3, 3), (123, 'KAMON', 'samiec', 3, 1),
                    (124, 'BREGA', 'samica', 3, 2), (125, 'VILLAIN', 'samiec', 3, 3),
                    (126, 'OLZA', 'samica', 3, 2), (127, 'FLOX', 'samiec', 3, 2), (128, 'ARIKA', 'samica', 3, 1),
                    (129, 'ARS', 'samiec', 3, 2), (130, 'HUBA', 'samica', 3, 2),
                    (131, 'ZARIA', 'samica', 3, 1), (132, 'AKRON', 'samiec', 3, 1), (133, 'ZULA', 'samica', 3, 2),
                    (134, 'DEMO', 'samica', 3, 2), (135, 'ALBA', 'samica', 3, 2),
                    (136, 'BRAVO', 'samiec', 3, 1), (137, 'ZAMA', 'samica', 3, 2), (138, 'DON', 'samiec', 3, 3),
                    (139, 'FARSA', 'samica', 3, 3), (140, 'ALAN', 'samiec', 3, 1),
                    (141, 'FAMA', 'samica', 3, 2), (142, 'CIRO', 'samiec', 3, 1), (143, 'AFRA', 'samica', 3, 2),
                    (144, 'MAŁGA', 'samica', 3, 1), (145, 'KIM', 'samiec', 3, 2),
                    (146, 'AJKA', 'samica', 3, 1), (147, 'ARES', 'samiec', 3, 2), (148, 'FIONA', 'samica', 3, 2),
                    (149, 'KARISSO', 'samiec', 3, 1), (150, 'SAMBA', 'samica', 3, 1),
                    (151, 'TEQUILLA', 'samica', 3, 1), (152, 'BURY', 'samiec', 3, 2), (153, 'BETA', 'samica', 3, 2),
                    (154, 'CERA', 'samica', 3, 1), (155, 'SKY', 'samiec', 3, 1),
                    (156, 'BEZA', 'samica', 3, 1), (157, 'SZNAPS', 'samiec', 3, 2), (158, 'INTER', 'samiec', 3, 2),
                    (159, 'DAMA', 'samica', 3, 2), (160, 'DAMA', 'samiec', 3, 3)]
        cur.executemany("""INSERT INTO OSOBNIKI(id_os, nazwa, plec, id_gat, id_hod) VALUES (?, ?, ?, ?, ?)""", self.osobniki)
        conn.commit()


    def data_entry_os_hod(self):
        self.os_hod = [(1, 1), (2, 2), (3, 3), (4, 3), (5, 1), (6, 3), (7, 3), (8, 1), (9, 3), (10, 2), (11, 1), (12, 2),
                  (13, 3), (14, 1),
                  (15, 1), (16, 3), (17, 1), (18, 2), (19, 3), (20, 1), (21, 1), (22, 2), (23, 3), (24, 2), (25, 1),
                  (26, 2), (27, 3),
                  (28, 3), (29, 2), (30, 1), (31, 1), (32, 2), (33, 3), (34, 3), (35, 2), (36, 1), (37, 2), (38, 3),
                  (39, 3), (40, 2),
                  (41, 1), (42, 2), (43, 3), (44, 1), (45, 2), (46, 3), (47, 1), (48, 2), (49, 3), (50, 1), (51, 2),
                  (52, 3), (53, 3),
                  (54, 2), (55, 1), (56, 1), (57, 1), (58, 1), (59, 2), (60, 2), (61, 2), (62, 3), (63, 3), (64, 3),
                  (65, 2), (66, 2),
                  (67, 2), (68, 1), (69, 1), (70, 1), (71, 2), (72, 2), (73, 2), (74, 1), (75, 1), (76, 1), (77, 2),
                  (78, 2), (79, 3),
                  (80, 1), (81, 3), (82, 2), (83, 1), (84, 2), (85, 3), (86, 1), (87, 2), (88, 2), (89, 3), (90, 1),
                  (91, 2), (92, 1),
                  (93, 2), (94, 3), (95, 1), (96, 2), (97, 2), (98, 3), (99, 1), (100, 2), (101, 3), (102, 1), (103, 2),
                  (104, 3),
                  (105, 2), (106, 1), (107, 2), (108, 2), (109, 1), (110, 1), (111, 2), (112, 1), (113, 3), (114, 3),
                  (115, 3), (116, 2),
                  (117, 1), (118, 1), (119, 1), (120, 2), (121, 2), (122, 3), (123, 1), (124, 2), (125, 3), (126, 2),
                  (127, 2), (128, 1),
                  (129, 2), (130, 2), (131, 1), (132, 1), (133, 2), (134, 2), (135, 2), (136, 1), (137, 2), (138, 3),
                  (139, 3), (140, 1),
                  (141, 2), (142, 1), (143, 2), (144, 1), (145, 2), (146, 1), (147, 2), (148, 2), (149, 1), (150, 1),
                  (151, 1), (152, 2),
                  (153, 2), (154, 1), (155, 1), (156, 1), (157, 2), (158, 2), (159, 2), (160, 3)]
        cur.executemany("""INSERT INTO OSOBNIKI_HODOWCY(id_os, id_hod) VALUES (?, ?)""", self.os_hod)
        conn.commit()


# drop()
# create_table()
# data_entry_genre()
# data_entry_relation()
# data_entry_breeder()
# data_entry_individual()
# data_entry_os_hod()

cur.close()
conn.close()

