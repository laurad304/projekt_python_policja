from tkinter import *
from tkinter import ttk, messagebox
from bs4 import BeautifulSoup
import requests
import tkintermapview
import random

class Koordynaty:
    def __init__(self, szerokosc=None, dlugosc=None):
        self.szerokosc = szerokosc or self.losuj_koordynaty_pl()[0]
        self.dlugosc = dlugosc or self.losuj_koordynaty_pl()[1]

    def losuj_koordynaty_pl(self):
        szerokosc = round(random.uniform(49.0, 54.8), 6)
        dlugosc = round(random.uniform(14.1, 24.1), 6)
        return szerokosc, dlugosc

    def __str__(self):
        return f"({self.szerokosc}, {self.dlugosc})"

def get_coordinates(location: str) -> Koordynaty:
    adres_url: str = f'https://pl.wikipedia.org/wiki/{location}'
    try:
        response = requests.get(adres_url)
        response.raise_for_status()
        response_html = BeautifulSoup(response.text, 'html.parser')

        latitude_elements = response_html.select('.latitude')
        longitude_elements = response_html.select('.longitude')

        if len(latitude_elements) < 2 or len(longitude_elements) < 2:
            messagebox.showwarning("Ostrzeżenie",
                                   f"Nie znaleziono współrzędnych dla {location}. Użyto domyślnych współrzędnych.")
            return Koordynaty(52.23, 21.00)

        latitude = float(latitude_elements[1].text.replace(',', '.'))
        longitude = float(longitude_elements[1].text.replace(',', '.'))
        return Koordynaty(latitude, longitude)
    except (requests.RequestException, ValueError, IndexError) as e:
        messagebox.showwarning("Ostrzeżenie",
                               f"Nie udało się pobrać współrzędnych dla {location}: {e}. Użyto domyślnych współrzędnych.")
        return Koordynaty(52.23, 21.00)

class JednostkaPolicji:
    def __init__(self, nazwa, miejscowosc):
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc
        self.koordynaty = get_coordinates(miejscowosc)
        self.policjanci = []

class Policjant:
    def __init__(self, imie, nazwisko, miejscowosc, jednostka):
        self.imie = imie
        self.nazwisko = nazwisko
        self.miejscowosc = miejscowosc
        self.jednostka = jednostka
        self.koordynaty = get_coordinates(miejscowosc)
        self.incydenty = []

class Incydent:
    def __init__(self, numer, opis, data, miejsce, status, policjant):
        self.numer = numer
        self.opis = opis
        self.data = data
        self.miejsce = miejsce
        self.status = status
        self.policjant = policjant
        self.koordynaty = get_coordinates(miejsce)

# Przykładowe jednostki policji
jednostka1 = JednostkaPolicji("Komenda Główna Policji", "Warszawa")
jednostka2 = JednostkaPolicji("Komenda Miejska Policji", "Kraków")

# Przykładowi policjanci
policjant1 = Policjant("Anna", "Kowalska", "Warszawa", jednostka1)
policjant2 = Policjant("Jan", "Nowak", "Kraków", jednostka2)

# Dodaj policjantów do jednostek
jednostka1.policjanci.append(policjant1)
jednostka2.policjanci.append(policjant2)

# Przykładowe incydenty
incydent1 = Incydent("INC001", "Kradzież w centrum handlowym", "2025-06-01", "Warszawa", "Otwarte", policjant1)
incydent2 = Incydent("INC002", "Włamanie do mieszkania", "2025-06-05", "Kraków", "Zamknięte", policjant2)

# Przypisz incydenty do policjantów
policjant1.incydenty.append(incydent1)
policjant2.incydenty.append(incydent2)

# Wypisz informacje
print(f"Jednostka: {jednostka1.nazwa}, Lokalizacja: {jednostka1.miejscowosc}, Koordynaty: {jednostka1.koordynaty}")
print(f"Policjant: {policjant1.imie} {policjant1.nazwisko}, Lokalizacja: {policjant1.miejscowosc}, Koordynaty: {policjant1.koordynaty}")
print(f"Incydent: {incydent1.numer}, Opis: {incydent1.opis}, Status: {incydent1.status}, Koordynaty: {incydent1.koordynaty}")
