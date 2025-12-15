import sqlite3

def get_con():
   conn = sqlite3.connect("baza.sqlite")
   conn.row_factory = sqlite3.Row         
   conn.execute("PRAGMA foreign_keys = ON")
   return conn

def utworz_tabele():
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS autorzy(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       imie    TEXT,
                       nazwisko TEXT,
                       rok_urodzenia  INTEGER,
                       kraj_pochodzenia TEXT
                       )
                       """
        )
        conn.commit()

def dodaj_autora( imie: str, nazwisko: str, rok_urodzenia: str, kraj_pochodzenia: str) -> None:
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO autorzy (imie, nazwisko, rok_urodzenia, kraj_pochodzenia) VALUES (?, ?, ?, ?)",
            (imie, nazwisko, rok_urodzenia, kraj_pochodzenia)
        )
        conn.commit()

def czy_autor_istnieje( id: int) -> bool:
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM autorzy WHERE id = ?", (id,))
        return cursor.fetchone() is not None
        
def usun_autor_po_id(id:int)->None:
    if czy_autor_istnieje(id):
        pass
    else:
        print("Nie ma takiego autora")
        return None
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM autorzy WHERE id = ?", (id,))
        conn.commit()

def zmodyfikuj_dane_po_id(id: int) -> None:
    if not czy_autor_istnieje(id):
        print("Nie ma takiego autora")
        return

    with get_con() as conn:
        cursor = conn.cursor()

        wyb = input("imie(a), nazwisko(b), rok urodzenia(c), kraj pochodzenia(d): ")

        if wyb == "a":
            imie = input("nowe imie: ")
            zmiana = f"imie = '{imie}'"

        elif wyb == "b":
            nazwisko = input("nowe nazwisko: ")
            zmiana = f"nazwisko = '{nazwisko}'"

        elif wyb == "c":
            rok_urodzenia = int(input("nowy rok urodzenia: "))
            zmiana = f"rok_urodzenia = {rok_urodzenia}"

        elif wyb == "d":
            kraj_pochodzenia = input("nowy kraj pochodzenia: ")
            zmiana = f"kraj_pochodzenia = '{kraj_pochodzenia}'"

        else:
            print("Niepoprawny wybór")
            return

        sql = f"UPDATE autorzy SET {zmiana} WHERE id = {id}"
        cursor.execute(sql)
        conn.commit()


utworz_tabele()

def menu():
    while True:
        print("dodaj(a), usun(b), zmodyfikuj(c), wyjdz(d)")
        akcja = input("odp: ")
        if akcja == "a":
            imie = input("imie: ")
            nazwisko = input("nazwisko: ")
            rok_urodzenia = int(input("rok urodzenia: "))
            kraj_pochodzenia = input("kraj pochodzenia: ")
            dodaj_autora(imie, nazwisko, rok_urodzenia, kraj_pochodzenia)
        elif akcja == "b":
            id = int(input("podaj id:"))
            usun_autor_po_id(id)
        elif akcja == "c":
            id = int(input("podaj id:"))
            zmodyfikuj_dane_po_id(id)
        elif akcja == "d":
            break

