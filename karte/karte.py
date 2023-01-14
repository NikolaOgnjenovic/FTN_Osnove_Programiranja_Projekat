from datetime import datetime
from model import model
import common.konstante as konst
import common.utils as utils

sledeci_broj_karte = 0
"""
Kupovina karte proverava da li prosleđeni konkretni let postoji i da li ima slobodnih mesta. U tom slučaju se karta 
dodaje u kolekciju svih karata. Slobodna mesta se prosleđuju posebno iako su deo konkretnog leta, zbog lakšeg 
testiranja. Baca grešku ako podaci nisu validni.
kwargs moze da prihvati prodavca kao recnik, i datum_prodaje kao datetime
recnik prodavac moze imati id i ulogu
CHECKPOINT 2: kupuje se samo za ulogovanog korisnika i bez povezanih letova.
ODBRANA: moguće je dodati saputnike i odabrati povezane letove. 
"""


def kupovina_karte(
        sve_karte: dict,
        svi_konkretni_letovi: dict,
        sifra_konkretnog_leta: int,
        putnici: list,
        slobodna_mesta: list,
        kupac: dict,
        **kwargs  # prodavac i datum prodaje
) -> (dict, dict):
    prihvatljive_uloge = [konst.ULOGA_KORISNIK, konst.ULOGA_PRODAVAC]
    if kupac.get('uloga') not in prihvatljive_uloge:
        raise Exception('Test greska')
    if sifra_konkretnog_leta not in svi_konkretni_letovi:
        raise Exception('Greška: konkretni let ne postoji')

    broj_mesta = 0
    for red in slobodna_mesta:
        if broj_mesta > len(putnici):
            break
        for mesto_zauzeto in red:
            if not mesto_zauzeto:
                broj_mesta += 1
    if broj_mesta < len(putnici):
        raise Exception('Greška: nema slobodnog mesta za sve putnike.')

    # Jedan test prosleđuje prodavca kao rečnik id, uloga: korisnik umesto kao string
    prodavac = kwargs.get('prodavac')
    if prodavac != str(prodavac) and prodavac.get('uloga') != konst.ULOGA_PRODAVAC:
        raise Exception('Greška: samo korisnik uloge prodavac može biti prodavac.')

    datum = kwargs.get('datum_prodaje')
    if datum is None:
        datum = datetime.now().date()

    # Ako se zove iz testova, koristi globalnu promenljivu
    global sledeci_broj_karte
    broj_karte = sledeci_broj_karte

    zvao_test = False
    vrednosti = {}
    try:
        # Ako se zove iz testova baciće izuzetak pa će se koristiti globalna promenljiva
        vrednosti = utils.ucitaj_recnik_iz_fajla('fajlovi/vrednosti_sifri.csv', ',', model.vrednosti_sifri.keys(),
                                                 'vrednosti_sifri')
        broj_karte = vrednosti['broj_karte']
    except FileNotFoundError:
        zvao_test = True

    karta = {
        'broj_karte': broj_karte,
        'putnici': putnici,
        'sifra_konkretnog_leta': sifra_konkretnog_leta,
        'status': konst.STATUS_NEREALIZOVANA_KARTA,
        'obrisana': False,
        'datum_prodaje': datum,
        'prodavac': kwargs['prodavac'],
        'kupac': kupac
    }
    if not zvao_test:
        vrednosti['broj_karte'] += 1
        utils.sacuvaj_vrednosti_sifri(vrednosti, 'fajlovi/vrednosti_sifri.csv', ',', model.vrednosti_sifri.keys())
    else:
        sledeci_broj_karte += 1
    sve_karte.update({karta['broj_karte']: karta})
    return karta, sve_karte


"""
Vraća sve nerealizovane karte za korisnika u listi.
"""


def pregled_nerealizovanaih_karata(korisnik: dict, sve_karte: list) -> list:
    nerealizovane_karte = []
    for karta in sve_karte:
        if korisnik in karta['putnici'] and karta['status'] == konst.STATUS_NEREALIZOVANA_KARTA:
            nerealizovane_karte.append(karta)
    return nerealizovane_karte


"""
Funkcija menja sve vrednosti karte novim vrednostima. Kao rezultat vraća rečnik sa svim kartama, 
koji sada sadrži izmenu.
"""


def izmena_karte(
        sve_karte: iter,
        svi_konkretni_letovi: iter,
        broj_karte: int,
        nova_sifra_konkretnog_leta: int = None,
        nov_datum_polaska: datetime = None,
        sediste: str = None
) -> dict:
    if broj_karte not in sve_karte:
        raise Exception('Greška: karta datog broja ne postoji')
    karta = sve_karte[broj_karte]
    if nova_sifra_konkretnog_leta is not None:
        karta['sifra_konkretnog_leta'] = nova_sifra_konkretnog_leta
    if nov_datum_polaska is not None:
        svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['datum_i_vreme_polaska'] = nov_datum_polaska
    if sediste is not None:
        karta['sediste'] = sediste
    sve_karte.update({karta['broj_karte']: karta})
    return sve_karte


"""
 Funkcija brisanja karte se ponaša drugačije u zavisnosti od korisnika:
- Prodavac: karta se označava za brisanje
- Admin/menadžer: karta se trajno briše
Kao rezultat se vraća nova kolekcija svih karata. Baca grešku ako podaci nisu validni.
"""


def brisanje_karte(korisnik: dict, sve_karte: dict, broj_karte: int) -> dict:
    if korisnik['uloga'] == konst.ULOGA_ADMIN:
        sve_karte.pop(broj_karte)
        print('Karta uspešno obrisana\n')
    elif korisnik['uloga'] == konst.ULOGA_PRODAVAC:
        sve_karte[broj_karte]['obrisana'] = True
        print('Karta uspešno obeležena za brisanje\n')
    else:
        raise Exception('Greška: korisnik ne sme da briše karte')
    return sve_karte


"""
Funkcija vraća sve karte koje se poklapaju sa svim zadatim kriterijumima. 
Kriterijum se ne primenjuje ako nije prosleđen.
"""


def pretraga_prodatih_karata(sve_karte: dict, svi_letovi: dict, svi_konkretni_letovi: dict, polaziste: str = "",
                             odrediste: str = "", datum_polaska: datetime = "", datum_dolaska: str = "",
                             korisnicko_ime_putnika: str = "") -> list:
    prodate_karte = []
    for karta in sve_karte.values():
        konkretan_let = svi_konkretni_letovi[karta['sifra_konkretnog_leta']]
        let = svi_letovi[konkretan_let['broj_leta']]
        if polaziste != '' and let['sifra_polazisnog_aerodroma'] != polaziste:
            continue
        if odrediste != '' and let['sifra_odredisnog_aerodorma'] != odrediste:
            continue
        if datum_polaska != '' and konkretan_let['datum_i_vreme_polaska'] != datum_polaska:
            continue
        if datum_dolaska != '' and konkretan_let['datum_i_vreme_dolaska'] != datum_dolaska:
            continue
        if korisnicko_ime_putnika not in karta['putnici']:
            continue
        prodate_karte.append(karta)
    return prodate_karte


"""
Funkcija koja čuva sve karte u fajl na zadatoj putanji.
"""


def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
    utils.sacuvaj_recnik(sve_karte, putanja, separator, model.karta.keys())


"""
Funkcija koja učitava sve karte iz fajla i vraća ih u rečniku.
"""


def ucitaj_karte_iz_fajla(putanja: str, separator: str) -> dict:
    return utils.ucitaj_recnik_iz_fajla(putanja, separator, model.karta.keys(), 'broj_karte')
