import ksiazka
import klient
import wydawnictwo
import autor

def main():
    while True:
        print("książki(a), autor(b), wydawnictwo(c), klient(d), wyjdź(e)")
        wyb = input("odp: ")
        if wyb == "a":
            ksiazka.menu()
        elif wyb == "b":
            autor.menu()
        elif wyb == "c":
            wydawnictwo.menu()
        elif wyb == "d":
            klient.menu()
        elif wyb == "e":
            break
        
main()