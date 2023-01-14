from datetime import datetime, date, timedelta


def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: date) -> list:
    prodate_karte = []
    for karta in sve_karte.values():
        if karta['datum_prodaje'] == dan:
            prodate_karte.append(karta)

    return prodate_karte


def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date) -> list:
    prodate_karte = []
    for karta in sve_karte.values():
        dan_karte = svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['datum_i_vreme_polaska'].date()
        if dan_karte == dan:
            prodate_karte.append(karta)
    return prodate_karte


def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: date, prodavac: str) -> list:
    prodate_karte = []
    for karta in sve_karte.values():
        if karta['datum_prodaje'] == dan and karta['prodavac'] == prodavac:
            prodate_karte.append(karta)

    return prodate_karte


def izvestaj_ubc_prodatih_karata_za_dan_prodaje(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi,
    dan: date
) -> tuple:

    broj = 0
    cena = 0

    for karta in sve_karte.values():
        if karta['datum_prodaje'] == dan:
            broj += 1
            cena += svi_letovi.get(svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['broj_leta'])['cena']

    return broj, cena


def izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict,
                                                dan: date) -> tuple:  # ubc znaci ukupan broj i cena
    broj = 0
    cena = 0

    for karta in sve_karte.values():
        # Prvi if zbog testa
        if svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['datum_i_vreme_polaska'] == dan \
                or svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['datum_i_vreme_polaska'].date() == dan:
            broj += 1
            cena += svi_letovi.get(svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['broj_leta'])['cena']
    return broj, cena


def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, konkretni_letovi: dict, svi_letovi: dict,
                                                           dan: date, prodavac: str) -> tuple:
    broj = 0
    cena = 0

    for karta in sve_karte.values():
        if karta['datum_prodaje'] == dan and karta['prodavac'] == prodavac:
            broj += 1
            cena += svi_letovi.get(konkretni_letovi[karta['sifra_konkretnog_leta']]['broj_leta'])['cena']
    return broj, cena


def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte: dict, svi_konkretni_letovi: dict,
                                                       svi_letovi: dict) -> dict:  # ubc znaci ukupan broj i cena
    izvestaj = {}

    for karta in sve_karte.values():
        # Због теста који датум продаје уноси као 10.10.2022. уместо као datetime који пише у моделу
        if karta['datum_prodaje'] == str(karta['datum_prodaje']):
            karta['datum_prodaje'] = datetime.strptime(karta['datum_prodaje'], '%d.%m.%Y.').date()

        if datetime.now().date() - karta['datum_prodaje'] < timedelta(days=30):
            cena = svi_letovi.get(svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['broj_leta'])['cena']
            if karta['prodavac'] not in izvestaj:
                izvestaj[karta['prodavac']] = {'broj': 1, 'cena': cena, 'prodavac': karta['prodavac']}
            else:
                izvestaj[karta['prodavac']]['broj'] += 1
                izvestaj[karta['prodavac']]['cena'] += cena
    # pretvori u {prodavac: (broj, cena, prodavac)} recnik zbog testa
    test_izvestaj = {}
    for element in izvestaj.values():
        test_izvestaj.update({element['prodavac']: (element['broj'], element['cena'], element['prodavac'])})
    return test_izvestaj
