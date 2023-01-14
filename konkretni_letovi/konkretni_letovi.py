from datetime import datetime, timedelta
from common import utils
from model import model

# Šifre počinju od 1000
sledeca_sifra = 1000


# Vraća datetime oblik razlike pocetnog i krajnjeg datuma
def razlika_datuma(pocetak: datetime, kraj: datetime) -> datetime:
    for n in range(int((pocetak - kraj).days)):
        yield pocetak + timedelta(n)


def kreiranje_konkretnog_leta(svi_konkretni_letovi: dict, let: dict):
    datum_pocetka_operativnosti = let['datum_pocetka_operativnosti']
    datum_kraja_operativnosti = let['datum_kraja_operativnosti']
    sat_poletanja = let['vreme_poletanja'][:2]
    minut_poletanja = let['vreme_poletanja'][3:5]
    sat_dolaska = let['vreme_sletanja'][:2]
    minut_dolaska = let['vreme_sletanja'][3:5]

    global sledeca_sifra

    vrednosti = {}

    zvao_test = False
    try:
        # Ako se zove iz testova baciće izuzetak pa će se koristiti globalna promenljiva
        vrednosti = utils.ucitaj_recnik_iz_fajla('fajlovi/vrednosti_sifri.csv', ',', model.vrednosti_sifri.keys(),
                                                 'vrednosti_sifri')
    except FileNotFoundError:
        zvao_test = True

    razlika_nedelja = timedelta(days=7)
    # Za svaki dan tokom kog se let realizuje
    for dan in let['dani']:
        # Razlika u danima = (dan početka realizovanja + dan realizacije) % 7
        razlika = (datum_pocetka_operativnosti.weekday() + int(dan)) % 7

        # Razliku u danima dodaj na datum početka operativnosti i počni odatle iteraciju
        trenutni_datum = datum_pocetka_operativnosti + timedelta(days=razlika)

        # Iteriraj do datuma kraja operativnosti
        while trenutni_datum < datum_kraja_operativnosti:
            if zvao_test:
                sifra_konkretnog_leta = sledeca_sifra
            else:
                sifra_konkretnog_leta = vrednosti['sifra_konkretnog_leta']
            konkretan_let = {
                'sifra': sifra_konkretnog_leta,
                'broj_leta': let['broj_leta'],
                # U trenutni datum dodaj sat i minut poletanja i dolaska koristeći replace()
                'datum_i_vreme_polaska': trenutni_datum.replace(hour=int(sat_poletanja), minute=int(minut_poletanja)),
                'datum_i_vreme_dolaska': trenutni_datum.replace(hour=int(sat_dolaska), minute=int(minut_dolaska))
            }

            if zvao_test:
                sledeca_sifra += 1
            else:
                vrednosti['sifra_konkretnog_leta'] += 1
                sifra_konkretnog_leta += 1
            svi_konkretni_letovi.update({konkretan_let['sifra']: konkretan_let})
            # Trenutni datum povećaj za nedelju dana
            trenutni_datum += razlika_nedelja

    if not zvao_test:
        utils.sacuvaj_vrednosti_sifri(vrednosti, 'fajlovi/vrednosti_sifri.csv', ',', model.vrednosti_sifri.keys())

    return svi_konkretni_letovi


def sacuvaj_kokretan_let(putanja: str, separator: str, svi_konkretni_letovi: dict):
    utils.sacuvaj_recnik(svi_konkretni_letovi, putanja, separator, model.konkretan_let.keys())


def ucitaj_konkretan_let(putanja: str, separator: str) -> dict:
    return utils.ucitaj_recnik_iz_fajla(putanja, separator, model.konkretan_let.keys(), 'sifra')
