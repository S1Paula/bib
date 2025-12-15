import sqlite3
# import plik1

def get_con():
   conn = sqlite3.connect("baza.sqlite")
   conn.row_factory = sqlite3.Row         
   conn.execute("PRAGMA foreign_keys = ON")
   return conn

def utworz_tabele():
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS ksiazki(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       autor_id  INTEGER NOT NULL,
                       wydawnictwo_id   INTEGER NOT NULL,
                       wyporzyczona   INTEGER,  
                       tytul    TEXT,
                       liczba_stron INTEGER,
                       gatunek  TEXT,
                       FOREIGN KEY (autor_id)
                            REFERENCES autorzy(id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                       
                       FOREIGN KEY (wydawnictwo_id)
                            REFERENCES wydawnictwa(id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                       
                       FOREIGN KEY (wyporzyczona)
                            REFERENCES klienci(id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE

                       )
                       """
        )
        conn.commit()

def dodaj_ksiazke(autor_id: int, wydawnictwo_id: int, tytul: str, liczba_stron: int, gatunek: str) -> None:
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ksiazki (autor_id, wydawnictwo_id, tytul, liczba_stron, gatunek) VALUES (?, ?, ?, ?, ?)",
            (autor_id, wydawnictwo_id, tytul, liczba_stron, gatunek)
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

def zmodyfikuj_dane_po_id(id: int) -> None:
    if not czy_ksiazka_istnieje(id):
        print("Nie ma takiej Ksiazki")
        return

    with get_con() as conn:
        cursor = conn.cursor()

        wyb = input("tytuł(a), liczba stron(b), gatunek(c), autor(d), wydawnictwo(e), wypożycz(f): ")

        if wyb == "a":
            tytul = input("nowy tytul: ")
            zmiana = f"tytul = '{tytul}'"

        elif wyb == "b":
            liczba_stron = int(input("nowa liczba stron: "))
            zmiana = f"liczba_stron = {liczba_stron}"

        elif wyb == "c":
            gatunek = input("nowy gatunek: ")
            zmiana = f"gatunek = '{gatunek}'"

        elif wyb == "d":
            autor_id = int(input("nowe id autora: "))
            zmiana = f"autor_id = {autor_id}"

        elif wyb == "e":
            wydawnictwo_id = int(input("nowe id wydawnictwa: "))
            zmiana = f"wydawnictwo_id = {wydawnictwo_id}"

        elif wyb == "f":
            wypozyczona = int(input("id klienta: "))
            zmiana = f"wypozyczona = {wypozyczona}"

        else:
            print("Niepoprawny wybór")
            return

        sql = f"UPDATE ksiazki SET {zmiana} WHERE id = {id}"
        cursor.execute(sql)
        conn.commit()


utworz_tabele()

def menu():
    while True:
        print("dodaj(a), usun(b), zmodyfikuj(c), wyjdz(d)")
        akcja = input("odp: ")
        if akcja == "a":
            autor_id = int(input("podaj id autora: "))
            wydawnictwo_id = int(input("podaj id wydawnictwa: "))
            tytul = input("podaj tytul: ")
            licz_str = int(input("podaj liczbe stron: "))
            gatunek = input("podaj gatunek: ")
            dodaj_ksiazke(autor_id, wydawnictwo_id, tytul, licz_str, gatunek)
        elif akcja == "b":
            id = int(input("podaj id:"))
            usun_ksiazke_po_id(id)
        elif akcja == "c":
            id = int(input("podaj id:"))
            zmodyfikuj_dane_po_id(id)
        elif akcja == "d":
            break
