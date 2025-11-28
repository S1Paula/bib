import sqlite3
from dataclasses import dataclass


@dataclass
class Ksiazka:
    id: int
    tytul: str
    liczba_stron: int
    gatunek: str




class Biblioteka:
    def __init__(self, nazwa_pliku: str = "bibloteka.db"):
        self.nazwa_pliku = nazwa_pliku
        self._utworz_tabele()


    def _polaczenie(self):
        conn = sqlite3.connect(self.nazwa_pliku)
        conn.row_factory = sqlite3.Row
        return conn


    def _utworz_tabele(self):
        with self._polaczenie() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS ksiazki(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           tytul    TEXT,
                           liczba_stron INTEGER,
                           gatunek  TEXT
                           )
                           """
            )
            conn.commit()

    def dodaj_ksiazke(self, tytul: str, liczba_stron: int, gatunek: str) -> None:
        with self._polaczenie() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ksiazki (tytul, liczba_stron, gatunek) VALUES (?, ?, ?)",
                (tytul, liczba_stron, gatunek)
            )
            conn.commit()

baza = Biblioteka()


baza.dodaj_ksiazke("ferdydurke", 248, "lektura")


