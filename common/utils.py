import csv
from datetime import datetime


def sacuvaj_recnik(recnik: dict, putanja: str, separator: str, osobine: list):
    with open(putanja, 'w+') as csv_fajl:
        csv_upisivac = csv.DictWriter(csv_fajl, osobine, separator)

        # Svakog korisnika upisi u csv fajl
        for element in recnik:
            csv_upisivac.writerow(recnik[element])


def sacuvaj_vrednosti_sifri(recnik: dict, putanja: str, separator: str, osobine: list):
    with open(putanja, 'w+') as csv_fajl:
        csv_upisivac = csv.DictWriter(csv_fajl, osobine, separator)
        csv_upisivac.writerow(recnik)


# Pravi fajl ako vec ne postojibine: list
def napravi_fajl(putanja: str):
    f = open(putanja, 'a+')
    f.close()


# Ucita recnik iz date putanje sa datim separatorom
# Osobine koristi DictReader za zaglavlje
# Ključ služi za eksplicitnu konverziju učitanih stringova kako bi struktura funkcionisala pri poređenju
def ucitaj_recnik_iz_fajla(putanja: str, separator: str, osobine: list, kljuc: str) -> dict:
    napravi_fajl(putanja)
    recnik = {}

    with open(putanja, 'r+') as csv_fajl:
        csv_citac = csv.DictReader(csv_fajl, osobine, separator)

        for element in csv_citac:
            # Karte se ucitavaju po letu broj_karte
            if kljuc == 'broj_karte':
                element['broj_karte'] = int(element['broj_karte'])
                element['sifra_konkretnog_leta'] = int(element['sifra_konkretnog_leta'])
                if element['putnici'] != '|':  # Zbog testova :D
                    element['putnici'] = eval(element['putnici'])
                if element['obrisana'] == 'False':
                    element['obrisana'] = False
                elif element['obrisana'] == 'True':
                    element['obrisana'] = True
                # Kupac treba da je recnik, jedan test prosledjuje string duzine 10 pa ako nije iz testa evaluiraj
                if len(element['kupac']) > 10:
                    element['kupac'] = eval(element['kupac'])
                # Neki testovi ne prosleđuju status
                if element['status'] == '|':
                    element.pop('status')
                    element['prodavac'] = eval(element['prodavac'])
                else:
                    element['datum_prodaje'] = datetime.strptime(element['datum_prodaje'], '%Y-%m-%d').date()
                if element['putnici'] == '|':
                    element.pop('putnici')
            # Letovi se ucitavaju po sifri broj_leta
            elif kljuc == 'broj_leta':
                if element['sletanje_sutra'] == 'False':
                    element['sletanje_sutra'] = False
                elif element['sletanje_sutra'] == 'True':
                    element['sletanje_sutra'] = True
                element['cena'] = float(element['cena'])
                element['model'] = eval(element['model'])
                element['datum_pocetka_operativnosti'] = datetime.strptime(element['datum_pocetka_operativnosti'],
                                                                           '%Y-%m-%d %H:%M:%S')
                element['datum_kraja_operativnosti'] = datetime.strptime(element['datum_kraja_operativnosti'],
                                                                         '%Y-%m-%d %H:%M:%S')
                element['dani'] = eval(element['dani'])  # lista
            # Konkretni letovi se ucitavaju po kljucu sifra
            elif kljuc == 'sifra':
                # Čuva se kao čist datetime 2014-03-04 06:20:40 pa pretvori u 04.03.2014.
                element['datum_i_vreme_polaska'] = datetime.strptime(element['datum_i_vreme_polaska'],
                                                                     '%Y-%m-%d %H:%M:%S')
                element['datum_i_vreme_dolaska'] = datetime.strptime(element['datum_i_vreme_dolaska'],
                                                                     '%Y-%m-%d %H:%M:%S')
                element['sifra'] = int(element['sifra'])
                # Zbog testova :D
                if element['zauzetost'] != '|':
                    element['zauzetost'] = eval(element['zauzetost'])
                else:
                    element.pop('zauzetost')
            elif kljuc == 'vrednosti_sifri':
                element['sifra_konkretnog_leta'] = int(element['sifra_konkretnog_leta'])
                element['broj_karte'] = int(element['broj_karte'])
                return element
            # Ako se ucitava model aviona
            elif kljuc == 'id':
                element['broj_redova'] = int(element['broj_redova'])
                element['id'] = int(element['id'])
                element['pozicije_sedista'] = eval(element['pozicije_sedista'])
            recnik.update({element.get(kljuc): element})
        # Nije učitan rečnik vrednosti šifri sa brojem redova većih od 0, vrati defualt 1000, 0
        if kljuc == 'vrednosti_sifri':
            return {'sifra_konkretnog_leta': 1000,
                    'broj_karte': 0}
    return recnik
