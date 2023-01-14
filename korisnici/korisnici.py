import common.konstante as konst
import common.utils as utils
from model import model

trenutno_ulogovan = {}


"""
Funkcija koja kreira novi rečnik koji predstavlja korisnika sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih korisnika proširenu novim korisnikom. Može se ponašati kao dodavanje ili ažuriranje, u zavisnosti od vrednosti
parametra azuriraj:
- azuriraj == False: kreira se novi korisnik. Vraća grešku ako korisničko ime već postoji.
- azuriraj == True: ažurira se postojeći korisnik. Vraća grešku ako korisničko ime ne postoji.

Ova funkcija proverava i validnost podataka o korisniku, koji su tipa string.

CHECKPOINT 1: Vraća string sa greškom ako podaci nisu validni (ne važi za konverziju brojeva).
ODBRANA: Baca grešku sa porukom ako podaci nisu validni.
"""


def kreiraj_korisnika(svi_korisnici: dict, azuriraj: bool, uloga: str, staro_korisnicko_ime: str | None,
                      korisnicko_ime: str, lozinka: str, ime: str, prezime: str, email: str = '', pasos: str = '',
                      drzavljanstvo: str = '', telefon: str = '', pol: str = '') -> dict:
    # Provera validne uloge
    uloge = [konst.ULOGA_KORISNIK, konst.ULOGA_ADMIN, konst.ULOGA_PRODAVAC]
    if uloga not in uloge:
        raise Exception('Greška: uloga je nepostojeća')
    # Provera validnog korisnickog imena
    if korisnicko_ime is None:
        raise Exception('Greška: korisničko ime je prazno')
    # Ako se azurira i staro ime ne postoji, greska
    if azuriraj and staro_korisnicko_ime not in svi_korisnici:
        raise Exception('Greška: korisničko ime ne postoji')
    # Ako se ime menja a vec postoji greska
    if korisnicko_ime in svi_korisnici and korisnicko_ime != staro_korisnicko_ime:
        raise Exception('Greška: korisničko ime već postoji')
    # Ako je ime prazno greska
    if ime is None or len(ime) < 1:
        raise Exception('Greška: ime je prazno')
    # Ako je prezime prazno greska
    if prezime is None or len(prezime) < 1:
        raise Exception('Greška: prezime je prazno')
    # Ako je lozinka prazna greska
    if lozinka is None or len(lozinka) < 1:
        raise Exception('Greška: lozinka je prazna')
    # Ako je email @.nesto ili @ ne postoji ili ima vise domena greska
    if len(email) > 0 and (str(email).find('@') == 0 or '@' not in str(email) or email.count('.') != 1):
        raise Exception('Greška: imejl nije validan')
    # Ako pasos nije sastavljen od brojeva ili duzine 9 greska
    if len(pasos) > 0:
        pasos = str(pasos)
        if not pasos.isnumeric() or len(pasos) != 9:
            raise Exception('Greška: pasoš nema 9 cifara')
    # Ako telefon nije broj greska
    if len(telefon) > 0:
        telefon = str(telefon)
        if not telefon.isnumeric():
            raise Exception('Greška: telefon ne sadrži samo brojeve')

    nov_korisnik = {'uloga': uloga, 'korisnicko_ime': korisnicko_ime, 'lozinka': lozinka, 'ime': ime,
                    'prezime': prezime, 'email': email, 'pasos': pasos, 'drzavljanstvo': drzavljanstvo,
                    'telefon': telefon, 'pol': pol}
    # Ako se pravi nov korisnik i ime vec postoji greska
    if not azuriraj:
        if staro_korisnicko_ime in svi_korisnici:
            raise Exception('Greška: korisničko ime već postoji')
        # Napravi novog korisnika
        svi_korisnici.update({korisnicko_ime: nov_korisnik})
    # Ako se azurira postojeci azuriraj sve[stari] i u sve[novi] stavi popovan stari
    else:
        svi_korisnici.update({staro_korisnicko_ime: nov_korisnik})
        svi_korisnici[korisnicko_ime] = svi_korisnici.pop(staro_korisnicko_ime)
    return svi_korisnici


"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
"""


def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    utils.sacuvaj_recnik(svi_korisnici, putanja, separator, model.korisnik.keys())


"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""


def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:
    return utils.ucitaj_recnik_iz_fajla(putanja, separator, model.korisnik.keys(), 'korisnicko_ime')


"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
"""


def login(svi_korisnici, korisnicko_ime, lozinka) -> dict:
    # Ako je ime pronadjeno i njegova sifra jednaka unetoj vrati korisnika, ako ne vrati gresku
    if korisnicko_ime in svi_korisnici and svi_korisnici[korisnicko_ime]['lozinka'] == lozinka:
        global trenutno_ulogovan
        trenutno_ulogovan = svi_korisnici[korisnicko_ime]
        return svi_korisnici[korisnicko_ime]
    raise Exception('Greška: login nepostojeći')
