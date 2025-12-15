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
                       CREATE TABLE IF NOT EXISTS klienci(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       imie    TEXT,
                       nazwisko TEXT,
                       rok_urodzenia  INTEGER,
                       email    TEXT,
                       telefon INTEGER
                       )
                       """
        )
        conn.commit()

def dodaj_klienta( imie: str, nazwisko: str, rok_urodzenia: str, email: str, telefon: int) -> None:
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO klienci (imie, nazwisko, rok_urodzenia, email, telefon) VALUES (?, ?, ?, ?, ?)",
            (imie, nazwisko, rok_urodzenia, email, telefon)
        )
        conn.commit()

def czy_klient_istnieje( id: int) -> bool:
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM klienci WHERE id = ?", (id,))
        return cursor.fetchone() is not None
        
def usun_klienta_po_id(id:int)->None:
    if czy_klient_istnieje(id):
        pass
    else:
        print("Nie ma takiego klienta")
        return None
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM klienci WHERE id = ?", (id,))
        conn.commit()

def zmodyfikuj_dane_po_id(id: int) -> None:
    if not czy_klient_istnieje(id):
        print("Nie ma takiego klienta")
        return

    with get_con() as conn:
        cursor = conn.cursor()

        wyb = input("imie(a), nazwisko(b), rok urodzenia(c), email(d), telefon(e): ")

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
            email = input("nowy email: ")
            zmiana = f"email = '{email}'"

        elif wyb == "c":
            telefon = int(input("nowy telefon: "))
            zmiana = f"telefon = {telefon}"

        else:
            print("Niepoprawny wybór")
            return

        sql = f"UPDATE klienci SET {zmiana} WHERE id = {id}"
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
            email = input("email: ")
            telefon = int(input("telefon: "))
            dodaj_klienta(imie, nazwisko, rok_urodzenia, email, telefon)
        elif akcja == "b":
            id = int(input("podaj id:"))
            usun_klienta_po_id(id)
        elif akcja == "c":
            id = int(input("podaj id:"))
            zmodyfikuj_dane_po_id(id)
        elif akcja == "d":
            break

