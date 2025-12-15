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
                       CREATE TABLE IF NOT EXISTS wydawnictwa(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nazwa    TEXT,
                       dyrektor TEXT,
                       rok_powstania  INTEGER,
                       adres    TEXT
                       )
                       """
        )
        conn.commit()

def dodaj_wydawnictwo( nazwa: str, dyrektor: str, rok_powstania: str, adres: str) -> None:
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO wydawnictwa (nazwa, dyrektor, rok_powstania, adres) VALUES (?, ?, ?, ?)",
            (nazwa, dyrektor, rok_powstania, adres)
        )
        conn.commit()

def czy_wydawnictwo_istnieje( id: int) -> bool:
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM wydawnictwa WHERE id = ?", (id,))
        return cursor.fetchone() is not None
        
def usun_wydawnictwo_po_id(id:int)->None:
    if czy_wydawnictwo_istnieje(id):
        pass
    else:
        print("Nie ma takiego wydawnictwa")
        return None
    with get_con() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM wydawnictwa WHERE id = ?", (id,))
        conn.commit()

def zmodyfikuj_dane_po_id(id: int) -> None:
    if not czy_wydawnictwo_istnieje(id):
        print("Nie ma takiego wydawnictwa")
        return

    with get_con() as conn:
        cursor = conn.cursor()

        wyb = input("nazwa(a), dyrektor(b), rok powstania(c), adres(d): ")

        if wyb == "a":
            nazwa = input("nowa nazwa: ")
            zmiana = f"nazwa = '{nazwa}'"

        elif wyb == "b":
            dyrektor = input("nowy dyrektor: ")
            zmiana = f"dyrektor = '{dyrektor}'"

        elif wyb == "c":
            rok_powstania = int(input("nowy rok powstania: "))
            zmiana = f"rok_powstania = {rok_powstania}"

        elif wyb == "d":
            adres = input("nowy adres: ")
            zmiana = f"adres = '{adres}'"

        else:
            print("Niepoprawny wybór")
            return

        sql = f"UPDATE wydawnictwa SET {zmiana} WHERE id = {id}"
        cursor.execute(sql)
        conn.commit()


utworz_tabele()

def menu():
    while True:
        print("dodaj(a), usun(b), zmodyfikuj(c), wyjdz(d)")
        akcja = input("odp: ")
        if akcja == "a":
            nazwa = input("nazwa: ")
            dyrektor = input("dyrektor: ")
            rok_powstania = int(input("rok powstania: "))
            adres = input("adres: ")
            dodaj_wydawnictwo(nazwa, dyrektor, rok_powstania, adres)
        elif akcja == "b":
            id = int(input("podaj id:"))
            usun_wydawnictwo_po_id(id)
        elif akcja == "c":
            id = int(input("podaj id:"))
            zmodyfikuj_dane_po_id(id)
        elif akcja == "d":
            break
