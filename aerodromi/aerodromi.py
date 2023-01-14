from common import utils
from model import model

"""
Funkcija kreira rečnik za novi aerodrom i dodaje ga u rečnik svih aerodroma.
Kao rezultat vraća rečnik svih aerodroma sa novim aerodromom.
"""


def kreiranje_aerodroma(
    svi_aerodromi: dict,
    skracenica: str = '',
    pun_naziv: str = '',
    grad: str = '',
    drzava: str = ''
) -> dict:
    if not skracenica:
        raise Exception('Greška: skraćenica prazna')
    if not pun_naziv:
        raise Exception('Greška: pun naziv prazan')
    if not grad:
        raise Exception('Greška: grad prazan')
    if not drzava:
        raise Exception('Greška: država prazna')

    svi_aerodromi.update({pun_naziv: {'skracenica': skracenica,
                                      'pun_naziv': pun_naziv,
                                      'grad': grad,
                                      'drzava': drzava}})
    return svi_aerodromi


"""
Funkcija koja čuva aerodrome u fajl.
"""


def sacuvaj_aerodrome(putanja: str, separator: str, svi_aerodromi: dict):
    utils.sacuvaj_recnik(svi_aerodromi, putanja, separator, model.aerodrom.keys())


"""
Funkcija koja učitava aerodrome iz fajla.
"""


def ucitaj_aerodrom(putanja: str, separator: str) -> dict:
    return utils.ucitaj_recnik_iz_fajla(putanja, separator, model.aerodrom.keys(), 'skracenica')
