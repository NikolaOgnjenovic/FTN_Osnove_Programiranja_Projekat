from model import model
from common import utils
"""
Funkcija kreira novi rečnik za model aviona i dodaje ga u rečnik svih modela aviona.
Kao rezultat vraća rečnik svih modela aviona sa novim modelom.
"""


id_modela = -1


def kreiranje_modela_aviona(
    svi_modeli_aviona: dict,
    naziv: str = '',
    broj_redova: str = '',
    pozicije_sedista: list = []
) -> dict:
    if not naziv:
        raise Exception('Greška: naziv modela aviona prazan.')
    if not broj_redova:
        raise Exception('Greška: broj redova modela aviona nije brojna vrednost.')
    if len(pozicije_sedista) == 0:
        raise Exception('Greška: pozicije sedišta prazne.')
    global id_modela
    id_modela += 1
    svi_modeli_aviona.update({id_modela: {'naziv': naziv, 'id': id_modela, 'broj_redova': broj_redova,
                                          'pozicije_sedista': pozicije_sedista}})
    return svi_modeli_aviona


"""
Funkcija čuva sve modele aviona u fajl na zadatoj putanji sa zadatim operatorom.
"""


def sacuvaj_modele_aviona(putanja: str, separator: str, svi_aerodromi: dict):
    utils.sacuvaj_recnik(svi_aerodromi, putanja, separator, model.model_aviona.keys())


"""
Funkcija učitava sve modele aviona iz fajla na zadatoj putanji sa zadatim operatorom.
"""


def ucitaj_modele_aviona(putanja: str, separator: str) -> dict:
    return utils.ucitaj_recnik_iz_fajla(putanja, separator, model.model_aviona.keys(), 'id')
