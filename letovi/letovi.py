import time
from datetime import datetime, timedelta, date

from model import model
import common.utils as utils
import common.konstante as konst


# Validira date podatke vezane za kreiranje leta. Raisuje izuzetak ako neki nije validan.
def validacija_podataka(broj_leta: str, dani: list, cena: float, model_aviona: dict, vreme_poletanja: str,
                        vreme_sletanja: str, datum_pocetka_operativnosti: datetime,
                        datum_kraja_operativnosti: datetime, sletanje_sutra: bool, sifra_polazisnog_aerodroma: str,
                        sifra_odredisnog_aerodroma: str, prevoznik: str):
    if not dani:
        raise Exception('Greška: dani su prazni')
    for dan in dani:
        if dan < konst.PONEDELJAK or dan > konst.NEDELJA:
            raise Exception('Greška: nepostojeći dan')
    if cena < 0:
        raise Exception('Greška: cena nije validna')
    if not model_aviona:
        raise Exception('Greška: model ne postoji')

    if len(vreme_sletanja) != 5:
        raise Exception('Greška: vreme sletenja nije formata 24:00')
    try:
        time.strptime(vreme_sletanja, '%H:%M')
    except ValueError:
        raise Exception('Greška: vreme sletenja nije formata 24:00')

    if len(vreme_poletanja) != 5:
        raise Exception('Greška: vreme poletanja nije formata 24:00')
    try:
        time.strptime(vreme_poletanja, '%H:%M')
    except ValueError:
        raise Exception('Greška: vreme poletanja nije formata 24:00')

    if len(broj_leta) != 4 or not broj_leta[:2].isalpha() or not broj_leta[2:4].isnumeric():
        raise Exception('Greška: broj leta nije validan')

    if datum_kraja_operativnosti < datum_pocetka_operativnosti:
        raise Exception('Greška: datum kraja operativnosti je pre datuma početka operativnosti')

    if sletanje_sutra is None:
        raise 'Greška: sletanje sutra nije validno'
    if len(sifra_polazisnog_aerodroma) != 3:
        raise 'Greška: šifra polazišnog aerodroma nije validna'
    if len(sifra_odredisnog_aerodroma) != 3:
        raise 'Greška: šifra odredišnog aerodroma nije validna'
    if prevoznik is None or prevoznik == '':
        raise 'Greška: prevoznik nije validan'


"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
Ipak vraća listu letova čiji je datum početka operativnosti posle trenutnog vremena
"""


def pregled_nerealizovanih_letova(svi_letovi: dict) -> list:
    print('Nerealizovani letovi:')
    lista = []
    for let in svi_letovi.values():
        if let['datum_pocetka_operativnosti'] > datetime.now():
            lista.append(let)
    return lista


"""
Funkcija koja omogucava pretragu leta po zadatim kriterijumima. Korisnik moze da zada jedan ili vise kriterijuma.
Povfratna vrednost je lista konkretnih letova.
"""


def pretraga_letova(svi_letovi: dict, konkretni_letovi: dict, polaziste: str = "", odrediste: str = "",
                    datum_polaska: datetime = None, datum_dolaska: datetime = None, vreme_poletanja: str = "",
                    vreme_sletanja: str = "", prevoznik: str = "") -> list:
    lista = []
    for konkretni_let in konkretni_letovi.values():
        broj_leta = konkretni_let['broj_leta']
        opsti_let = svi_letovi[broj_leta]
        if polaziste and polaziste != opsti_let['sifra_polazisnog_aerodroma']:
            continue
        if odrediste and odrediste != opsti_let['sifra_odredisnog_aerodorma']:
            continue
        if datum_polaska and datum_polaska.date() != konkretni_let['datum_i_vreme_polaska'].date():
            continue
        if datum_dolaska and datum_dolaska.date() != konkretni_let['datum_i_vreme_dolaska'].date():
            continue
        if vreme_poletanja and vreme_poletanja != opsti_let['vreme_poletanja']:
            continue
        if vreme_sletanja and vreme_sletanja != opsti_let['vreme_sletanja']:
            continue
        if prevoznik and prevoznik != opsti_let['prevoznik']:
            continue

        lista.append(konkretni_let)

    return lista


def trazenje_10_najjeftinijih_letova(svi_letovi: dict, polaziste: str = "", odrediste: str = "") -> list:
    letovi = []
    for let in svi_letovi.values():
        if polaziste != '' and polaziste != let['sifra_polazisnog_aerodroma']:
            continue
        if odrediste != '' and odrediste != let['sifra_odredisnog_aerodorma']:
            continue
        letovi.append(let)
    letovi = sorted(letovi, key=lambda l: l['cena'])
    letovi = letovi[:10]
    letovi.reverse()
    return letovi


# Kreiranje i izmena letova se razlikiju za par uslova te zovu istu funkciju - azuriraj let
def azuriraj_let(svi_letovi: dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                 vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                 dani: list, model_aviona: dict, cena: float, datum_pocetka_operativnosti: datetime,
                 datum_kraja_operativnosti: datetime) -> dict:
    validacija_podataka(broj_leta, dani, cena, model_aviona, vreme_poletanja, vreme_sletanja,
                        datum_pocetka_operativnosti, datum_kraja_operativnosti, sletanje_sutra,
                        sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma, prevoznik)

    nov_let = {'broj_leta': broj_leta, 'sifra_polazisnog_aerodroma': sifra_polazisnog_aerodroma,
               'sifra_odredisnog_aerodorma': sifra_odredisnog_aerodorma, 'vreme_poletanja': vreme_poletanja,
               'vreme_sletanja': vreme_sletanja, 'sletanje_sutra': sletanje_sutra, 'prevoznik': prevoznik,
               'dani': dani, 'model': model_aviona, 'cena': cena,
               'datum_pocetka_operativnosti': datum_pocetka_operativnosti,
               'datum_kraja_operativnosti': datum_kraja_operativnosti}
    svi_letovi.update({broj_leta: nov_let})

    return svi_letovi


"""Funkcija koja kreira novi rečnik koji predstavlja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju 
svih letova proširenu novim letom. Ova funkcija proverava i validnost podataka o letu. Paziti da kada se kreira let, 
da se kreiraju i njegovi konkretni letovi. vreme_poletanja i vreme_sletanja su u formatu hh:mm CHECKPOINT2: Baca 
grešku sa porukom ako podaci nisu validni. """


def kreiranje_letova(svi_letovi: dict, broj_leta: str, sifra_polazisnog_aerodroma: str,
                     sifra_odredisnog_aerodorma: str, vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool,
                     prevoznik: str, dani: list, model_aviona: dict, cena: float,
                     datum_pocetka_operativnosti: datetime = None, datum_kraja_operativnosti: datetime = None):
    if broj_leta in svi_letovi:
        raise 'Greška: let već postoji.'
    rezultat = azuriraj_let(svi_letovi, broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma,
                            vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model_aviona, cena,
                            datum_pocetka_operativnosti, datum_kraja_operativnosti)
    if len(rezultat) > 0:
        return svi_letovi
    return rezultat


"""
Funkcija koja menja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova sa promenjenim letom. 
Ova funkcija proverava i validnost podataka o letu.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""


def izmena_letova(svi_letovi: dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                  vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                  dani: list, model_aviona: dict, cena: float, datum_pocetka_operativnosti: datetime,
                  datum_kraja_operativnosti: datetime) -> dict:
    if broj_leta not in svi_letovi:
        raise 'Greška: let ne postoji.'
    return azuriraj_let(svi_letovi, broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma, vreme_poletanja,
                        vreme_sletanja, sletanje_sutra, prevoznik, dani, model_aviona, cena,
                        datum_pocetka_operativnosti,
                        datum_kraja_operativnosti)


"""
Funkcija koja cuva sve letove na zadatoj putanji
"""


def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    utils.sacuvaj_recnik(svi_letovi, putanja, separator, model.let.keys())


"""
Funkcija koja učitava sve letove iz fajla i vraća ih u rečniku.
"""


def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:
    return utils.ucitaj_recnik_iz_fajla(putanja, separator, model.let.keys(), 'broj_leta')


# Postavlja vrednost polja 'zauzetost' konkretnog leta na matricu broj_redova x len(pozicije_sedista) = {False}
def podesi_matricu_zauzetosti(svi_letovi: dict, konkretan_let: dict) -> list:
    matrica = []
    model_aviona = svi_letovi.get(konkretan_let['broj_leta'])['model']
    broj_redova = model_aviona['broj_redova']
    pozicije_sedista = model_aviona['pozicije_sedista']

    for i in range(0, broj_redova):
        red = []
        for j in range(0, len(pozicije_sedista)):
            red.append(False)
        matrica.append(red)

    konkretan_let['zauzetost'] = matrica
    return matrica


def matrica_zauzetosti(konkretan_let: dict) -> list:
    return konkretan_let['zauzetost']


"""
Funkcija koja zauzima sedište na datoj poziciji u redu, najkasnije 48h pre poletanja. Redovi počinju od 1. 
Vraća grešku ako se sedište ne može zauzeti iz bilo kog razloga.
"""


def checkin(karta, svi_letovi: dict, konkretni_let: dict, red: int, pozicija: str) -> (dict, dict):
    if (konkretni_let['datum_i_vreme_polaska'] - datetime.now()) < timedelta(hours=48):
        raise Exception('Greška: ne možete se checkin-ovati manje od 48 sati pre početka leta.')

    model_aviona = svi_letovi[konkretni_let['broj_leta']]['model']
    broj_redova = model_aviona['broj_redova']
    pozicije_sedista = model_aviona['pozicije_sedista']

    red -= 1  # Red je prosleđen sa početnim indeksom 1
    if red < 0 or red > broj_redova:
        raise Exception('Greška: red ne postoji u modelu aviona.')
    if pozicija not in pozicije_sedista:
        raise Exception('Greška: pozicija sedišta u modelu aviona.')

    pozicija_broj = -1
    for sediste in pozicije_sedista:
        pozicija_broj += 1
        if pozicija == sediste:
            break
    if konkretni_let['zauzetost'][red][pozicija_broj]:
        raise Exception('Greška: mesto je već zauzeto.')
    konkretni_let['zauzetost'][red][pozicija_broj] = True

    karta['sediste'] = pozicija + str(red+1)

    return konkretni_let, karta


"""
Funkcija koja vraća listu konkretni letova koji zadovoljavaju sledeće uslove:
1. Polazište im je jednako odredištu prosleđenog konkretnog leta
2. Vreme i mesto poletanja im je najviše 120 minuta nakon sletanja konkretnog leta
"""


def povezani_letovi(svi_letovi: dict, svi_konkretni_letovi: dict, konkretni_let: dict) -> list:
    sifra = konkretni_let['sifra']
    odrediste_karte = svi_letovi[svi_konkretni_letovi[sifra]['broj_leta']]['sifra_odredisnog_aerodorma']
    vreme_dolaska = svi_konkretni_letovi[sifra]['datum_i_vreme_dolaska']
    povezani_letovi_lista = []
    for konkretan_let in svi_konkretni_letovi.values():
        if svi_letovi[konkretan_let['broj_leta']]['sifra_polazisnog_aerodroma'] == odrediste_karte \
                and (timedelta(0) < (konkretan_let['datum_i_vreme_polaska'] - vreme_dolaska) < timedelta(hours=2)):
            povezani_letovi_lista.append(konkretan_let)
    return povezani_letovi_lista


"""
Funkcija koja vraća sve konkretne letove čije je vreme polaska u zadatom opsegu, +/- zadati broj fleksibilnih dana
"""


def fleksibilni_polasci(svi_letovi: dict, konkretni_letovi: dict, polaziste: str, odrediste: str,
                        datum_polaska: date, broj_fleksibilnih_dana: int, datum_dolaska: date) -> list:
    # Dodaj samo letove sa odgovarajućim polazišnim i odredišnim šiframa aerodroma
    trazeni_letovi = []
    for konkretan_let in konkretni_letovi.values():
        if konkretan_let['broj_leta'] not in svi_letovi:
            continue
        let = svi_letovi[konkretan_let['broj_leta']]
        if let['sifra_polazisnog_aerodroma'] == polaziste and let['sifra_odredisnog_aerodorma'] == odrediste:
            trazeni_letovi.append(konkretan_let)

    fleksibilnost = timedelta(days=broj_fleksibilnih_dana)

    # Ako je polazak 2022-10-10 i fleksibilnost 4 dana donja granica je 2022-10-08 a gornja 2022-10-12
    donja_granica_polaska = datum_polaska - fleksibilnost
    gornja_granica_polaska = datum_polaska + fleksibilnost

    # Isto važi i za dolazak
    donja_granica_dolaska = datum_dolaska - fleksibilnost
    gornja_granica_dolaska = datum_dolaska + fleksibilnost

    fleksibilni_letovi = []
    for konkretan_let in trazeni_letovi:
        polazak = konkretan_let['datum_i_vreme_polaska']
        dolazak = konkretan_let['datum_i_vreme_dolaska']
        if donja_granica_polaska < polazak < gornja_granica_polaska \
                and donja_granica_dolaska < dolazak < gornja_granica_dolaska:
            fleksibilni_letovi.append(konkretan_let)
    return fleksibilni_letovi
