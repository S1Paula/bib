import sqlite3
# import plik1

def get_con():
   conn = sqlite3.connect("baza.sqlite")
   conn.row_factory = sqlite3.Row         
#    conn.execute("PRAGMA foreign_keys = ON")
   return conn

def utworz_tabele():
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS ksiazki(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       autor_id  INTEGER NOT NULL,
                       tytul    TEXT,
                       liczba_stron INTEGER,
                       gatunek  TEXT,
                       FOREIGN KEY (autor_id)
                            REFERENCES autorzy(id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE

                       )
                       """
        )
        conn.commit()

def dodaj_ksiazke(autor_id: int, tytul: str, liczba_stron: int, gatunek: str) -> None:
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ksiazki (autor_id, tytul, liczba_stron, gatunek) VALUES (?, ?, ?, ?)",
            (autor_id, tytul, liczba_stron, gatunek)
        )
        conn.commit()

def czy_ksiazka_istnieje( id: int) -> bool:
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM ksiazki WHERE id = ?", (id,))
        return cursor.fetchone() is not None
        
def usun_ksiazke_po_id(id:int)->None:
    if czy_ksiazka_istnieje(id):
        pass
    else:
        print("Nie ma takiej ksiazki")
        return None
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ksiazki WHERE id = ?", (id,))
        conn.commit()

def zmodyfikuj_wszystkie_dane_po_id(id:int)->None:
    if czy_ksiazka_istnieje(id):
        pass
    else:
        print("Nie ma takiej Ksiazki")
        return None
    with get_con() as conn:
        cursor = conn.cursor()
        print("Podaj dane")
        tytul = input("nowy tytul: ")
        liczba_stron = int(input("nowa liczba stron: "))
        gatunek = input("nowy gatunek: ")


        cursor.execute("""UPDATE ksiazki
                        SET
                            tytul = ?,
                            liczba_stron = ?,
                            gatunek = ?
                        WHERE id = ?
                        """,
                        (tytul,liczba_stron,gatunek,id))


utworz_tabele()

def menu():
    akcja = input("dodaj ksiazke(d), ususn ksiazke(u), zmodyfikuj ksiazke(m)")
    if akcja == "d":
        autor_id = int(input("podaj id autora: "))
        tytul = input("podaj tytul: ")
        licz_str = int(input("podaj liczbe stron: "))
        gatunek = input("podaj gatunek: ")
        dodaj_ksiazke(autor_id, tytul, licz_str, gatunek)
    elif akcja == "u":
        id = int(input("podaj id:"))
        usun_ksiazke_po_id(id)
    elif akcja == "m":
        id = int(input("podaj id:"))
        zmodyfikuj_wszystkie_dane_po_id(id)

menu()




# dodaj_ksiazke("xxx", 12, "adsfa")
# dodaj_ksiazke("asdf", 1356, "jytghdrw")
# dodaj_ksiazke("sretr", 345, "rsthfsw")
# dodaj_ksiazke("xxntyx", 15642, "adkjyjysfa")
# dodaj_ksiazke("ryt", 345, "ndgt")

# usun_ksiazke_po_id(1)
# zmodyfikuj_wszystkie_dane_po_id(4)




