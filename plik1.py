import sqlite3

def get_con():
   conn = sqlite3.connect("baza.sqlite")
   conn.row_factory = sqlite3.Row         
#    conn.execute("PRAGMA foreign_keys = ON")
   return conn

def utworz_tabele():
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS autorzy(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       imie    TEXT,
                       nazwisko TEXT,
                       rok_urodzenia  INTEGER
                       kraj_pochodzenia TEXT
                       )
                       """
        )
        conn.commit()

def dodaj_autora( imie: str, nazwisko: str, rok_urodzenia: str, kraj_pochodzenia: str) -> None:
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO autorzy (imie, nazwisko, rok_urodzenia, kraj_pochodzenia) VALUES (?, ?, ?)",
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

def zmodyfikuj_wszystkie_dane_po_id(id:int)->None:
    if czy_autor_istnieje(id):
        pass
    else:
        print("Nie ma takiego autora")
        return None
    with get_con() as conn:
        cursor = conn.cursor()
        print("Podaj dane")
        imie = input("nowe imie: ")
        nazwisko = input("nowe nazwisko: ")
        rok_urodzenia = int(input("nowy rok urodzenia: "))
        kraj_pochodzenia = input("nowy kraj pochodzenia: ")


        cursor.execute("""UPDATE autorzy
                        SET
                            imie = ?,
                            nazwisko = ?,
                            rok_urodzenia = ?
                            kraj_pochodzenia = ?
                        WHERE id = ?
                        """,
                        (imie,nazwisko,rok_urodzenia,kraj_pochodzenia,id))


utworz_tabele()

def menu():
    akcja = input("dodaj(d), ususn(u), zmodyfikuj(m)")
    if akcja == "d":
        imie = input("nowe imie: ")
        nazwisko = input("nowe nazwisko: ")
        rok_urodzenia = int(input("nowy rok urodzenia: "))
        kraj_pochodzenia = input("nowy kraj pochodzenia: ")
        dodaj_autora(imie, nazwisko, rok_urodzenia)
    elif akcja == "u":
        id = int(input("podaj id:"))
        usun_autor_po_id(id)
    elif akcja == "m":
        id = int(input("podaj id:"))
        zmodyfikuj_wszystkie_dane_po_id(id)

menu()