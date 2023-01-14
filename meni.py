from sys import exit
from datetime import datetime, timedelta

from common import konstante as konst
from korisnici import korisnici
from izvestaji import izvestaji
from karte import karte
from konkretni_letovi import konkretni_letovi
from letovi import letovi
from model_aviona import model_aviona
from aerodromi import aerodromi

svi_korisnici = {}
svi_letovi = {}
svi_konkretni_letovi = {}
trenutno_ulogovan_korisnik = {}
sve_karte = {}
svi_avioni = {}
svi_aerodromi = {}


def ucitaj_sve_recnike():
    global svi_korisnici
    svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla('fajlovi/korisnici.csv', ',')

    global svi_letovi
    svi_letovi = letovi.ucitaj_letove_iz_fajla('fajlovi/letovi.csv', ',')

    global svi_konkretni_letovi
    svi_konkretni_letovi = konkretni_letovi.ucitaj_konkretan_let('fajlovi/konkretni_letovi.csv', ',')

    global sve_karte
    sve_karte = karte.ucitaj_karte_iz_fajla('fajlovi/karte.csv', ',')

    global svi_aerodromi
    svi_aerodromi = aerodromi.ucitaj_aerodrom('fajlovi/aerodromi.csv', ',')

    global svi_avioni
    svi_avioni = aerodromi.ucitaj_aerodrom('fajlovi/avioni.csv', ',')


def ispisi_karte(lista_karata: list):
    if len(lista_karata) == 0:
        print('Nažalost, ne postoje odgovarajuće karte.\n')
        zajednicki_meni()
        return

    print('|Broj karte          |Šifra leta          |Datum prodaje       |Kupac               |Putnici')
    for karta in lista_karata:
        imena_putnika = ''
        for putnik in karta['putnici']:
            imena_putnika += putnik['ime'] + ' ' + putnik['prezime'] + '    '
        datum_prodaje = datetime.strftime(karta['datum_prodaje'], '%d.%m.%Y.')
        vrednosti_ispisa = [karta['broj_karte'], karta['sifra_konkretnog_leta'], datum_prodaje,
                            karta['kupac']['korisnicko_ime'], imena_putnika]
        poruka = ''
        for vrednost in vrednosti_ispisa:
            poruka += '|' + str(vrednost) + ' ' * (20 - len(str(vrednost)))
        print(poruka)


def ispisi_letove(lista_letova: list):
    if len(lista_letova) == 0:
        print('Nažalost, ne postoje odgovarajući letovi.\n')
        return

    print('|Broj leta                 |Šifra polazišnog aerodroma|Šifra dolazišnog aerodroma|Vreme poletanja          '
          ' |Vreme sletanja            |Prevoznik                 |Cena')
    for let in lista_letova:
        vrednosti_ispisa = [let['broj_leta'], let['sifra_polazisnog_aerodroma'], let['sifra_odredisnog_aerodorma'],
                            let['vreme_poletanja'], let['vreme_sletanja'], let['prevoznik'], let['cena']]
        poruka = ''
        for vrednost in vrednosti_ispisa:
            poruka += '|' + str(vrednost) + ' ' * (26 - len(str(vrednost)))
        print(poruka)


def ispisi_konkretne_letove(lista_konkretnih_letova: list):
    if len(lista_konkretnih_letova) == 0:
        print('Nažalost, ne postoje odgovarajući konkretni letovi.\n')
        zajednicki_meni()
        return
    print('|Broj leta                 |Šifra konkretnog leta     |Polazak                   |Dolazak                  '
          ' |Cena')
    for konkretan_let in lista_konkretnih_letova:
        datum_i_vreme_polaska = datetime.strftime(konkretan_let['datum_i_vreme_polaska'], '%d.%m.%Y. %H:%M')
        datum_i_vreme_dolaska = datetime.strftime(konkretan_let['datum_i_vreme_dolaska'], '%d.%m.%Y. %H:%M')
        vrednosti_ispisa = [konkretan_let['broj_leta'], konkretan_let['sifra'], datum_i_vreme_polaska,
                            datum_i_vreme_dolaska, svi_letovi[konkretan_let['broj_leta']]['cena']]
        poruka = ''
        for vrednost in vrednosti_ispisa:
            poruka += '|' + str(vrednost) + ' ' * (26 - len(str(vrednost)))
        print(poruka)


def azuriraj_podatke():
    try:
        global svi_korisnici
        global trenutno_ulogovan_korisnik

        # Promenjen korisnik uzima podatke od trenutno ulogovanog
        promenjen_korisnik = {
            'korisničko ime': trenutno_ulogovan_korisnik.get('korisnicko_ime'),
            'lozinku': trenutno_ulogovan_korisnik.get('lozinka'),
            'ime': trenutno_ulogovan_korisnik.get('ime'),
            'prezime': trenutno_ulogovan_korisnik.get('prezime'),
            'email': trenutno_ulogovan_korisnik.get('email'),
            'broj pasoša': trenutno_ulogovan_korisnik.get('pasos'),
            'državljanstvo': trenutno_ulogovan_korisnik.get('drzavljanstvo'),
            'broj telefona': trenutno_ulogovan_korisnik.get('telefon'),
            'pol': trenutno_ulogovan_korisnik.get('pol')
        }

        # Ispiši sve ključeve i unesi ih
        for osobina in promenjen_korisnik.keys():
            unos = input(f'Unesite {osobina} ili enter ako ne želite da promenite ovu stavku\n')
            # Ako nije unet prazan string promeni vrednost u promenjenom korisniku
            if len(unos) > 0:
                promenjen_korisnik[osobina] = unos

        # Ažuriraj korisnika starog korisničkog imena jednakom korisničkom imenu trenutno ulogovanog
        svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici, True, trenutno_ulogovan_korisnik.get('uloga'),
                                                    trenutno_ulogovan_korisnik.get('korisnicko_ime'),
                                                    # Staro korisnicko ime
                                                    promenjen_korisnik.get('korisničko ime'),  # Novo korisnicko ime
                                                    promenjen_korisnik.get('lozinku'), promenjen_korisnik.get('ime'),
                                                    promenjen_korisnik.get('prezime'), promenjen_korisnik.get('email'),
                                                    promenjen_korisnik.get('broj pasoša'),
                                                    promenjen_korisnik.get('državljanstvo'),
                                                    promenjen_korisnik.get('broj telefona'),
                                                    promenjen_korisnik.get('pol'))
        korisnici.sacuvaj_korisnike('fajlovi/korisnici.csv', ',', svi_korisnici)

        # Ažuriraj podatke trenutno ulogovanog korisnika
        trenutno_ulogovan_korisnik = promenjen_korisnik
        print('Uspešno ste izmenili podatke Vašeg profila.\n')
    except Exception as ex:
        print(ex)


def pregled_nerealizovanih_letova():
    ispisi_letove(letovi.pregled_nerealizovanih_letova(svi_letovi))


# Ispisuje listu pretraženih konkretnih letova
def pretraga_konkretnih_letova():
    kraj_poruke = ' ili enter ako ne želite da pretražujete po ovoj stavci.\n'
    polaziste = input('Unesite troslovnu šifru polazišnog aerodroma' + kraj_poruke)
    if polaziste and not polaziste.isalpha() or len(polaziste) != 3:
        print('Greška: šifra polazišnog aerodroma mora biti sastavljena od slova.')
        zajednicki_meni()
    odrediste = input('Unesite šifru odredišnog aerodroma' + kraj_poruke)
    if odrediste and not odrediste.isalpha():
        print('Greška: šifra odredišnog aerodroma mora biti sastavljena od slova')
        zajednicki_meni()
    datum_polaska = input(
        'Unesite datum polaska formata dd.mm.yyyy.' + kraj_poruke)
    if datum_polaska:
        try:
            datum_polaska = datetime.strptime(datum_polaska, '%d.%m.%Y.')
        except ValueError:
            print('Greška: neispravan format datuma polaska.')
            zajednicki_meni()
    datum_dolaska = input(
        'Unesite datum dolaska formata dd.mm.yyyy.' + kraj_poruke)
    if datum_dolaska:
        try:
            datum_dolaska = datetime.strptime(datum_dolaska, '%d.%m.%Y.')
        except ValueError:
            print('Greška: neispravan format datuma dolaska.')
            zajednicki_meni()
    vreme_poletanja = input('Unesite vreme poletanja formata hh:mm' + kraj_poruke)
    vreme_sletanja = input('Unesite vreme sletanja formata hh:mm' + kraj_poruke)
    ime_prevoznika = input('Unesite ime prevoznika' + kraj_poruke)
    try:
        lista_pretrazenih_letova = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste, odrediste,
                                                          datum_polaska, datum_dolaska, vreme_poletanja, vreme_sletanja,
                                                          ime_prevoznika)
        print('\nLetovi koji ispunjavaju unete kriterijume pretrage:\n')
        ispisi_konkretne_letove(lista_pretrazenih_letova)
    except Exception as ex:
        print(ex)


def prikaz_10_najjeftinijih():
    ispisi_letove(list(svi_letovi.values()))
    polaziste = input(f'Unesite troslovnu šifru polazišnog aerodroma.\n')
    if not polaziste.isalpha():
        print('Greška: šifra polazišnog aerodroma mora biti sastavljena od slova.')
        zajednicki_meni()
    odrediste = input(f'Unesite troslovnu šifru odredišnog aerodroma.\n')
    if not odrediste.isalpha():
        print('Greška: šifra odredišnog aerodroma mora biti sastavljena od slova.')
        zajednicki_meni()

    najjeftiniji_letovi = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, polaziste, odrediste)
    ispisi_letove(najjeftiniji_letovi)


def fleksibilni_polasci():
    print(f'Svi letovi:')
    ispisi_letove(list(svi_letovi.values()))
    if len(svi_letovi) > 0:
        # Unos troslovnih šifri polazištnog i odredišnog aerodroma
        polaziste = input(f'Unesite troslovnu šifru polazišnog aerodroma.\n')
        if not polaziste.isalpha() or len(polaziste) != 3:
            print('Greška: šifra polazišnog aerodroma mora biti sastavljena od slova.')
            zajednicki_meni()
        odrediste = input(f'Unesite troslovnu šifru odredišnog aerodroma.\n')
        if not odrediste.isalpha() or len(polaziste) != 3:
            print('Greška: šifra odredišnog aerodroma mora biti sastavljena od slova.')
            zajednicki_meni()

        # Unos i konverzija datuma polaska u date
        datum_polaska = input('Unesite datum polaska formata dd.mm.yyyy.\n')
        try:
            datum_polaska = datetime.strptime(datum_polaska, '%d.%m.%Y.')
        except ValueError:
            print('Greška: neispravan format datuma polaska.')
            zajednicki_meni()

        # Unos i konverzija broja fleksibilnih dana u int
        broj_fleksibilnih_dana = input('Unesite broj dana gore/dole oko polaska.\n')
        if not broj_fleksibilnih_dana.isnumeric():
            print('Greška: niste uneli dan kao brojnu vrednost.')
            zajednicki_meni()
        broj_fleksibilnih_dana = int(broj_fleksibilnih_dana)

        # Unos i konverzija datuma dolaska u date
        datum_dolaska = input('Unesite datum dolaska formata dd.mm.yyyy.\n')
        try:
            datum_dolaska = datetime.strptime(datum_dolaska, '%d.%m.%Y.')
        except ValueError:
            print('Greška: neispravan format datuma dolaska.')
            zajednicki_meni()

        fleksibilni_letovi = letovi.fleksibilni_polasci(svi_letovi, svi_konkretni_letovi, polaziste, odrediste,
                                                        datum_polaska, broj_fleksibilnih_dana, datum_dolaska)

        print('Svi fleksibilni letovi:')
        ispisi_konkretne_letove(fleksibilni_letovi)


def kupovina_karte_sifra(dati_konkretni_letovi: dict) -> int:
    sifra = input('Unesite šifru konkretnog leta.\n')
    if not sifra.isnumeric():
        print('Greška: šifra konkretnog leta mora biti numerička.')
        zajednicki_meni()
    if int(sifra) not in dati_konkretni_letovi.keys():
        print('Greška: šifra konkretnog leta ne postoji.')
        zajednicki_meni()
    return int(sifra)


def kupovina_karte_dalje(dati_konkretni_letovi: dict, sifra: int, korisnik: dict, korisnicko_ime_prodavca: str):
    kupuje_dalje = input('Unesite DA ako želite da kupite kartu za povezan let.\n')
    if kupuje_dalje == 'DA':
        odrediste_karte = svi_letovi[dati_konkretni_letovi[sifra]['broj_leta']]['sifra_odredisnog_aerodorma']
        vreme_dolaska = dati_konkretni_letovi[sifra]['datum_i_vreme_dolaska']

        # Povezani letovi su svi letovi čije je polazište odredište datog konkretnog leta
        # čije je vreme poletanja manje od 2 sata nakon vremena sletanja datog konkretnog leta
        povezani_letovi = {}

        for konkretan_let in dati_konkretni_letovi.values():
            if svi_letovi[konkretan_let['broj_leta']]['sifra_polazisnog_aerodroma'] == odrediste_karte \
                    and (timedelta(0) < (konkretan_let['datum_i_vreme_polaska'] - vreme_dolaska) < timedelta(hours=2)):
                povezani_letovi.update({konkretan_let['sifra']: konkretan_let})

        kupoprodaja_karte(povezani_letovi, korisnik, korisnicko_ime_prodavca)


# Vraća rečnik saputnika
def kupovina_saputniku() -> dict:
    # Ako se karta kupuje saputniku, unesi ime i prezime saputnika (PDF)
    kupuje_saputniku = input('Unesite DA ako kartu kupujete i za saputnika.\n')
    if kupuje_saputniku == 'DA':
        ime = input('Unesite ime saputnika.\n')
        prezime = input('Unesite prezime saputnika.\n')
        saputnik = {'ime': ime, 'prezime': prezime}
        # Ako saputnik ima profil, preuzmi sve ostale podatke o saputniku
        for korisnik in svi_korisnici.values():
            if korisnik['prezime'] == prezime and korisnik['ime'] == ime:
                saputnik = korisnik
                break

        return saputnik
    return {}


# Kupovina i prodaja su iste osim što se razlikuje prodavac
def kupoprodaja_karte(dati_konkretni_letovi: dict, korisnik: dict, korisnicko_ime_prodavca: str):
    ispisi_konkretne_letove(list(dati_konkretni_letovi.values()))
    sifra = kupovina_karte_sifra(dati_konkretni_letovi)

    # Kartu je moguće kupiti drugoj osobi umesto sebi
    kupuje_drugom = input('Unesite DA ako kartu kupujete drugoj osobi.\n')
    if kupuje_drugom == 'DA':
        ime = input('Unesite ime druge osobe.\n')
        prezime = input('Unesite prezime druge osobe.\n')
        tudji_korisnik = []
        for korisnik in svi_korisnici.values():
            if korisnik['prezime'] == prezime and korisnik['ime'] == ime:
                tudji_korisnik = korisnik
                break
        if not tudji_korisnik:
            tudji_korisnik = korisnici.kreiraj_korisnika({}, False, konst.ULOGA_KORISNIK, None, 'privremeni', 'lozinka',
                                                         ime, prezime, '', '', '', '', '')['privremeni']
        putnici = [tudji_korisnik]
    # Stavi korisnika u putnike ako se karta ne kupuje drugoj osobi
    else:
        putnici = [korisnik]

    saputnik = kupovina_saputniku()
    if saputnik != {}:
        putnici.append(saputnik)

    matrica = letovi.matrica_zauzetosti((dati_konkretni_letovi[sifra]))

    try:
        global sve_karte
        karta, sve_karte = karte.kupovina_karte(sve_karte, dati_konkretni_letovi, sifra, putnici, matrica,
                                                trenutno_ulogovan_korisnik, prodavac=korisnicko_ime_prodavca)
        karte.sacuvaj_karte(sve_karte, 'fajlovi/karte.csv', ',')

        # Prodavac je Sistem ako korisnik kupuje kartu
        if korisnicko_ime_prodavca == 'Sistem':
            print('Karta je uspešno kupljena.\n')
        else:
            print('Karta je uspešno prodata.\n')

        kupovina_karte_dalje(dati_konkretni_letovi, sifra, korisnik, korisnicko_ime_prodavca)
    except Exception as ex:
        print(ex)
        zajednicki_meni()


def kupovina_karte(dati_konkretni_letovi: dict):
    kupoprodaja_karte(dati_konkretni_letovi, trenutno_ulogovan_korisnik, 'Sistem')


def prikaz_nerealizovanih_karata():
    nerealizovane_karte = karte.pregled_nerealizovanaih_karata(trenutno_ulogovan_korisnik, list(sve_karte.values()))
    print('Vaše nerealizovane karte:\n')
    ispisi_karte(nerealizovane_karte)


# Napravi korisnika pri prodaji karte korisniku koji se ne čuva se u fajlu korisnici.csv
def napravi_privremenog_korisnika(ime: str, prezime: str, telefon: str, email: str):
    try:
        korisnici.kreiraj_korisnika(svi_korisnici, False, konst.ULOGA_KORISNIK, None, 'privremeni', 'lozinka', ime,
                                    prezime, email, '', '', telefon, '')
    except Exception as ex:
        print(ex)
        zajednicki_meni()


def prodaja_karte(dati_konkretni_letovi: dict):
    ime = input('Unesite ime kupca\n')
    prezime = input('Unesite prezime kupca\n')
    kupac_postoji = False

    # Da li kupac postoji po prezimenu i imenu u svim korisnicima?
    kupac = {}
    for korisnik in svi_korisnici.values():
        if korisnik['prezime'] == prezime and korisnik['ime'] == ime:
            kupac_postoji = True
            kupac = korisnik
            break
    telefon = ''
    email = ''
    # Ako ne postoji unesi i telefon i email (PDF)
    if not kupac_postoji:
        telefon = input('Unesite telefon kupca\n')
        email = input('Unesite email kupca\n')
        kupac = {
            'telefon': telefon,
            'email': email,
            'ime': ime,
            'prezime': prezime,
            'uloga': konst.ULOGA_KORISNIK
        }
    napravi_privremenog_korisnika(ime, prezime, telefon, email)

    kupoprodaja_karte(dati_konkretni_letovi, kupac, trenutno_ulogovan_korisnik['korisnicko_ime'])


def checkinuj(karta: dict, broj_karte: int):
    konkretan_let = svi_konkretni_letovi[karta['sifra_konkretnog_leta']]
    pozicije_sedista = svi_letovi[konkretan_let['broj_leta']]['model']['pozicije_sedista']
    matrica_zauzetosti = letovi.matrica_zauzetosti(konkretan_let)

    print('Sedišta (x - zauzeto)\n')
    for i in range(0, len(matrica_zauzetosti)):
        red_prikaz = ''
        for j in range(0, len(matrica_zauzetosti[0])):
            if matrica_zauzetosti[i][j]:
                red_prikaz += 'X '
            else:
                red_prikaz += pozicije_sedista[j] + ' '
        poruka = str(i + 1) + '. red: ' + red_prikaz
        print(poruka)

    broj_reda = input('Unesite broj reda:\n')
    try:
        broj_reda = int(broj_reda)
    except ValueError:
        print('Greška: broj reda nije brojna vrednost.\n')
        zajednicki_meni()
        return
    pozicija = input('Unesite slovo slobodne pozicije.\n')
    try:
        svi_konkretni_letovi[karta['sifra_konkretnog_leta']], sve_karte[broj_karte] = letovi.checkin(karta, svi_letovi,
                                                                                                     konkretan_let,
                                                                                                     broj_reda,
                                                                                                     pozicija)
        print('Prijava na let uspešno obavljena.\n')
        karte.sacuvaj_karte(sve_karte, 'fajlovi/karte.csv', ',')
        konkretni_letovi.sacuvaj_kokretan_let('fajlovi/konkretni_letovi.csv', ',', svi_konkretni_letovi)
    except Exception as ex:
        print(ex)


def izmena_karte():
    global sve_karte

    trazene_karte = list(sve_karte.values())
    pretrazuje = input('Unesite DA ako želite da pretražujete karte po nekim parametrima\n')
    if pretrazuje == 'DA':
        trazene_karte = pretraga_karata(False)
    ispisi_karte(trazene_karte)

    broj_karte = input('Unesite broj karte\n')

    if (not broj_karte.isnumeric()) or (int(broj_karte) not in sve_karte.keys()):
        print('Greška: broj karte nije validan.\n')
        zajednicki_meni()

    karta = sve_karte[int(broj_karte)]

    unos = input(f'Unesite šifru konkretnog leta ili enter ako ne želite da promenite ovu stavku\n')
    if len(unos) > 0:
        if not unos.isnumeric() or int(unos) not in svi_konkretni_letovi.keys():
            print('Greška: konkretan let unete šifre ne postoji.\n')
            zajednicki_meni()
        karta['sifra_konkretnog_leta'] = int(unos)

    unos = input(f'Unesite DA ako želite da promenite šifru sedišta\n')
    if unos == 'DA':
        # Ako postoji prethodno uneto sedište, postavi to sedište u matrici zauzetosti na False
        if karta['sediste'][:-1].isnumeric():
            red = int(karta['sediste'][:-1])-1
            pozicija = ord(karta['sediste']) - ord('A')
            svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['zauzetost'][red][pozicija] = False
            checkinuj(karta, karta['broj_karte'])

    sve_karte.update({karta['broj_karte']: karta})
    karte.sacuvaj_karte(sve_karte, 'fajlovi/karte.csv', ',')
    print('Uspešno ste izmenili kartu\n')


def brisanje_karte():
    global sve_karte

    # Prodavac obeležava karte za brisanje
    if trenutno_ulogovan_korisnik['uloga'] == konst.ULOGA_PRODAVAC:
        trazene_karte = list(sve_karte.values())
        pretrazuje = input('Unesite DA ako želite da pretražujete karte po nekim parametrima\n')
        if pretrazuje == 'DA':
            trazene_karte = pretraga_karata(False)
        ispisi_karte(trazene_karte)

        broj_karte = input('Unesite broj karte koju obeležavate za brisanje\n')
        brisi_kartu(broj_karte)
    # Admin briše karte obeležene za brisanje
    elif trenutno_ulogovan_korisnik['uloga'] == konst.ULOGA_ADMIN:
        print('Brojevi karata koje su obeležene za brisanje:\n')
        obelezene_karte = []
        for karta in sve_karte.values():
            if karta['obrisana']:
                obelezene_karte.append(karta)
        ispisi_karte(obelezene_karte)
        broj_karte = input('Unesite broj karte koju želite da izbrišete\n')
        brisi_kartu(broj_karte)


def brisi_kartu(broj_karte: str):
    global sve_karte
    if not broj_karte.isnumeric() or int(broj_karte) not in sve_karte.keys():
        print('Greška: broj karte nije validan.\n')
        zajednicki_meni()
    sve_karte = karte.brisanje_karte(trenutno_ulogovan_korisnik, sve_karte, int(broj_karte))
    karte.sacuvaj_karte(sve_karte, 'fajlovi/karte.csv', ',')


# Ispis i unos vezan za pretragu karte, vraća listu pretraženih karata
# pretrazuje_ime biće True kada je funkcija pozvana iz prodate_karte() jer se nudi opcija pretrage po putnicima
def pretraga_karata(pretrazuje_ime: bool) -> list:
    polaziste = input('Unesite kod polazišnog aerodroma karte ili enter ako ne želite da vršite pretragu po njemu\n')
    odrediste = input('Unesite kod odredišnog aerodroma karte ili enter ako ne želite da vršite pretragu po njemu\n')

    datum_polaska = input('Unesite datum polaska (dd.mm.yyyyy.) ili enter ako ne želite da vršite pretragu po njemu\n')
    if datum_polaska:
        try:
            datum_polaska = datetime.strptime(datum_polaska, '%d.%m.%Y.').date()
        except ValueError:
            print('Greška: pogrešan format datuma polaska.\n')
    datum_dolaska = input('Unesite datum dolaska ili enter ako ne želite da vršite pretragu po njemu\n')
    if datum_dolaska:
        try:
            datum_dolaska = datetime.strptime(datum_dolaska, '%d.%m.%Y.').date()
        except ValueError:
            print('Greška: pogrešan format datuma dolaska.\n')

    ime = ''
    prezime = ''
    if pretrazuje_ime:
        ime = input('Unesite ime osobe čije karte pretražujete ili enter ako ne pretražujete karte po osobi\n')
        if ime:
            prezime = input('Unesite prezime osobe čije karte pretražujete\n')
        else:
            prezime = ''

    trazene_karte = []
    for karta in sve_karte.values():
        konkretan_let = svi_konkretni_letovi[karta['sifra_konkretnog_leta']]
        let = svi_letovi[konkretan_let['broj_leta']]
        if polaziste and polaziste != let['sifra_polazisnog_aerodroma']:
            continue
        if odrediste and odrediste != let['sifra_odredisnog_aerodorma']:
            continue
        if datum_polaska and datum_polaska != konkretan_let['datum_i_vreme_polaska'].date():
            continue
        if datum_dolaska and datum_dolaska != konkretan_let['datum_i_vreme_dolaska'].date():
            continue
        if pretrazuje_ime and ime and prezime:
            putnik_pronadjen = False
            for putnik in karta['putnici']:
                if putnik['prezime'] != prezime or putnik['ime'] != ime:
                    putnik_pronadjen = True
                    break
            if not putnik_pronadjen:
                continue
        trazene_karte.append(karta)

    return trazene_karte


def prodate_karte():
    ispisi_karte(pretraga_karata(True))


# Sačuva letove i pravi konkretne letove vezane za njega
def sacuvaj_letove_napravi_konkretne_(let: dict):
    letovi.sacuvaj_letove('fajlovi/letovi.csv', ',', svi_letovi)

    global svi_konkretni_letovi

    # Podesi matricu zauzetosti novih konkretnih letova
    novi_konkretni_letovi = konkretni_letovi.kreiranje_konkretnog_leta({}, let)
    for konkretan_let in novi_konkretni_letovi.values():
        letovi.podesi_matricu_zauzetosti(svi_letovi, konkretan_let)

    # Dodaj nove konkretne letove u sve konkretne letove
    for konkretan_let in novi_konkretni_letovi.values():
        svi_konkretni_letovi.update({konkretan_let['sifra']: konkretan_let})
    konkretni_letovi.sacuvaj_kokretan_let('fajlovi/konkretni_letovi.csv', ',', svi_konkretni_letovi)


# Dopušta korisniku da unese sve podatke vezane za let i obrađuje ih zavisno od argumenta kreiranje
def unos_leta(kreiranje: bool):
    global svi_letovi
    global svi_konkretni_letovi

    broj_leta = input('Unesite broj leta formata XX00\n')
    if not kreiranje:
        if broj_leta not in svi_letovi:
            print(f'Greška: let broja {broj_leta} ne postoji.\n')
            zajednicki_meni()

    # Ako je se let ne kreira (već menja), na kraj svake poruke obavesti korisnika kako da ne menja polje
    poruka_kraj = '\n'
    if not kreiranje:
        poruka_kraj = ' ili enter ako ne želite da promenite ovu stavku\n'

    # Upis vrednosti za svako polje u letu
    sifra_polazisnog = input('Unesite šifru polazišnog aerodroma formata XXX' + poruka_kraj)
    sifra_odredisnog = input('Unesite šifru odredišnog aerodroma formata XXX' + poruka_kraj)
    vreme_poletanja = input('Unesite vreme poletanja formata HH:MM' + poruka_kraj)
    vreme_sletanja = input('Unesite vreme sletanja HH:MM' + poruka_kraj)
    sletanje_sutra = input('Unesite DA ako let sleće sutra' + poruka_kraj)
    if sletanje_sutra == 'DA':
        sletanje_sutra = True
    else:
        sletanje_sutra = False

    naziv_prevoznika = input('Unesite naziv prevoznika' + poruka_kraj)

    dani = input('Unesite dane kojima se vrši let (0 ponedeljak, 6 nedelja)' + poruka_kraj)
    dani_lista = []
    for dan in dani:
        if dan not in '0123456':
            return 'Greška: dani nisu u rasponu [0,6].\n'
        dani_lista.append(int(dan))

    id_modela = input('Unesite ID modela aviona' + poruka_kraj)
    naziv = input('Unesite naziv modela aviona' + poruka_kraj)
    broj_redova = input('Unesite broj redova aviona' + poruka_kraj)
    if broj_redova:
        if not broj_redova.isnumeric():
            print('Greška: broj redova nije brojna vrednost.\n')
            zajednicki_meni()
        else:
            broj_redova = int(broj_redova)
    pozicije_sedista = list(input('Unesite pozicije sedista (ABCDEF)' + poruka_kraj))

    avion = {
        'id': id_modela,
        'naziv': naziv,
        'broj_redova': broj_redova,
        'pozicije_sedista': pozicije_sedista
    }

    try:
        cena = input('Unesite cenu leta' + poruka_kraj)
        if cena != '':
            cena = float(cena)

        # Unesi datum početka operativnosti kao string i konvertuj ga ako se let pravi ili (menja i nije unet enter)
        datum_pocetka = input('Unesite datum početka operativnosti leta formata dd.mm.yyyy.' + poruka_kraj)
        if kreiranje or (not kreiranje and datum_pocetka != ''):
            datum_pocetka = datetime.strptime(datum_pocetka, '%d.%m.%Y.')

        # Unesi datum kraja operativnosti kao string i konvertuj ga ako se let pravi ili (menja i nije unet enter)
        datum_kraja = input('Unesite datum kraja operativnosti leta formata dd.mm.yyyy.' + poruka_kraj)
        if kreiranje or (not kreiranje and datum_pocetka != ''):
            datum_kraja = datetime.strptime(datum_kraja, '%d.%m.%Y.')

        # Napravi let, sve njegove konkretne letove, podesi im matrice zauzetosti i sačuvaj let i konkretne u fajlovima
        if kreiranje:
            svi_letovi = letovi.kreiranje_letova(svi_letovi, broj_leta, sifra_polazisnog, sifra_odredisnog,
                                                 vreme_poletanja, vreme_sletanja, sletanje_sutra, naziv_prevoznika,
                                                 dani_lista, avion, cena, datum_pocetka, datum_kraja)
            sacuvaj_letove_napravi_konkretne_(svi_letovi[broj_leta])
        else:
            # Proveri da li su unete vrednosti prazne. Ako jesu, postavi ih na neizmenjene vrednosti iz traženog leta
            let = svi_letovi[broj_leta]
            if sifra_polazisnog == '':
                sifra_polazisnog = let['sifra_polazisnog_aerodroma']
            if sifra_odredisnog == '':
                sifra_odredisnog = let['sifra_odredisnog_aerodorma']
            if vreme_poletanja == '':
                vreme_poletanja = let['vreme_poletanja']
            if vreme_sletanja == '':
                vreme_sletanja = let['vreme_sletanja']
            if sletanje_sutra == '':
                sletanje_sutra = let['sletanje_sutra']
            if naziv_prevoznika == '':
                naziv_prevoznika = let['prevoznik']
            if dani == '':
                dani_lista = let['dani']

            # Model učitanog leta
            model = let['model']
            # Ako je korisnik nije promenio neku od vrednosti postavi ih na vrednost iz postojećeg leta
            for key, val in avion.items():
                if val == '':
                    avion[key] = model[key]
            if not avion['pozicije_sedista']:
                avion['pozicije_sedista'] = let['model']['pozicije_sedista']
            if cena == '':
                cena = let['cena']
            if datum_pocetka == '':
                datum_pocetka = let['datum_pocetka_operativnosti']
            if datum_kraja == '':
                datum_kraja = let['datum_kraja_operativnosti']

            svi_letovi = letovi.izmena_letova(svi_letovi, broj_leta, sifra_polazisnog, sifra_odredisnog,
                                              vreme_poletanja, vreme_sletanja, sletanje_sutra, naziv_prevoznika,
                                              dani_lista, avion, cena, datum_pocetka, datum_kraja)
            sacuvaj_letove_napravi_konkretne_(svi_letovi[broj_leta])

            print('Let uspešno izmenjen.\n')
    except Exception as ex:
        print(ex)
        zajednicki_meni()


def kreiranje_leta():
    unos_leta(True)


def izmena_leta():
    ispisi_letove(list(svi_letovi.values()))
    unos_leta(False)


def registracija_prodavca():
    korisnicko_ime = input('Unesite korisničko ime prodavca:\n')
    lozinka = input('Unesite lozinku prodavca:\n')
    ime = input('Unesite ime prodavca:\n')
    prezime = input('Unesite prezime prodavca:\n')
    email = input('Unesite email prodavca:\n')
    pasos = input('Unesite broj pasoša prodavca:\n')
    drzavljanstvo = input('Unesite državljanstvo prodavca:\n')
    telefon = input('Unesite broj telefona prodavca:\n')
    pol = input('Unesite pol prodavca:\n')

    try:
        global svi_korisnici
        svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici, False, konst.ULOGA_PRODAVAC, None, korisnicko_ime,
                                                    lozinka, ime, prezime, email, pasos, drzavljanstvo, telefon, pol)
        korisnici.sacuvaj_korisnike('fajlovi/korisnici.csv', ',', svi_korisnici)
        print(f'Prodavac {korisnicko_ime} uspešno registrovan.')
    except Exception as ex:
        print(ex)
        zajednicki_meni()


def izvestaj_dan_prodaje():
    dan = input('Unesite dan prodaje formata dd.mm.yyyy.:\n')
    try:
        dan = datetime.strptime(dan, '%d.%m.%Y.').date()
        izvestaj = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje(sve_karte, dan)
        ispisi_karte(izvestaj)
    except ValueError:
        print('Greška: pogrešno unet format dana.')
        izvestaji_opcije()


def izvestaj_dan_polaska():
    dan = input('Unesite dan polaska formata dd.mm.yyyy.:\n')
    try:
        dan = datetime.strptime(dan, '%d.%m.%Y.').date()
        izvestaj = izvestaji.izvestaj_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni_letovi, dan)
        ispisi_karte(izvestaj)
    except ValueError:
        print('Greška: pogrešno unet format dana.\n')
        izvestaji_opcije()


def izvestaj_dan_prodaje_prodavac():
    dan = input('Unesite dan prodaje formata dd.mm.yyyy.:\n')
    try:
        dan = datetime.strptime(dan, '%d.%m.%Y.').date()
    except ValueError:
        print('Greška: pogrešan format dana prodaje.')
        izvestaji_opcije()
    prodavac = input('Unesite korisničko ime prodavca:\n')
    izvestaj = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte, dan, prodavac)
    ispisi_karte(izvestaj)


def izvestaj_ubc_dan_prodaje():
    dan = input('Unesite dan prodaje formata dd.mm.yyyy.:\n')
    try:
        dan = datetime.strptime(dan, '%d.%m.%Y.').date()
        broj, cena = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(sve_karte, svi_konkretni_letovi, svi_letovi,
                                                                           dan)
        print(f'Broj prodatih karata: {broj}\nUkupna cena prodatih karata: {cena}\n')
    except ValueError:
        print('Greška: pogrešno unet format dana.\n')
        izvestaji_opcije()


def izvestaj_ubc_dan_polaska():
    dan = input('Unesite dan polaska formata dd.mm.yyyy.:\n')
    try:
        dan = datetime.strptime(dan, '%d.%m.%Y.').date()
        broj, cena = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni_letovi, svi_letovi,
                                                                           dan)
        print(f'Broj prodatih karata: {broj}\nUkupna cena prodatih karata: {cena}\n')
    except ValueError:
        print('Greška: pogrešno unet format dana.\n')
        izvestaji_opcije()


def izvestaj_ubc_dan_prodaje_prodavac():
    dan = input('Unesite dan prodaje formata dd.mm.yyyy.:\n')
    prodavac = input('Unesite korisničko ime prodavca:\n')
    try:
        dan = datetime.strptime(dan, '%d.%m.%Y.').date()
        broj, cena = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte, svi_konkretni_letovi,
                                                                                      svi_letovi, dan, prodavac)
        print(f'Broj prodatih karata: {broj}\nUkupna cena prodatih karata: {cena}\n')
    except ValueError:
        print('Greška: pogrešno unet format dana.\n')
        izvestaji_opcije()


def izvestaj_ubc_30_dana_prodavci():
    try:
        izvestaj = izvestaji.izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte, svi_konkretni_letovi,
                                                                                svi_letovi)
        print('Izveštaj ukupnog broja i cene prodatih karata u poslednjih 30 dana po prodavcima:\n')
        for element in izvestaj.values():
            broj = element[0]
            cena = element[1]
            prodavac = element[2]
            print(f'Prodavac: {prodavac}\nBroj prodatih karata: {broj}\nUkupna cena prodatih karata: {cena}\n')
    except Exception as ex:
        print(ex)
        izvestaji_opcije()


def izvestaji_opcije():
    izvestaji_meni = {
        '1': izvestaj_dan_prodaje,
        '2': izvestaj_dan_polaska,
        '3': izvestaj_dan_prodaje_prodavac,
        '4': izvestaj_ubc_dan_prodaje,
        '5': izvestaj_ubc_dan_polaska,
        '6': izvestaj_ubc_dan_prodaje_prodavac,
        '7': izvestaj_ubc_30_dana_prodavci,
        'x': zajednicki_meni
    }

    poruka = '1. Izveštaj svih prodatih karata za uneti dan prodaje\n' \
             '2. Izveštaj svih prodatih karata za uneti dan polaska\n' \
             '3. Izveštaj svih prodatih karata za uneti dan prodaje i prodavca\n' \
             '4. Ukupan broj i cena prodatih karata za izabrani dan prodaje\n' \
             '5. Ukupan broj i cena prodatih karata za izabrani dan polaska\n' \
             '6. Ukupan broj i cena prodatih karata za izabrani dan prodaje i prodavca\n' \
             '7. Ukupan broj i cena prodatih karata u poslednjih 30 dana po prodavcima\n' \
             'x. Povratak na meni\n'

    while True:
        print('\nIzaberite jednu od sledećih opcija:')
        print(poruka)

        unos = input('>>')

        if unos in izvestaji_meni:
            izvestaji_meni[unos]()
            if unos == 'x':
                return
        else:
            print('Odabrali ste nepostojeću opciju.')


def kreiraj_avion():
    naziv = input('Unesite naziv modela aviona:\n')
    broj_redova = input('Unesite broj redova aviona:\n')
    if not broj_redova.isnumeric():
        print('Broj redova nije brojna vrednost.\n')
        zajednicki_meni()
        return
    pozicije_sedista = list(input('Unesite pozicije sedišta aviona:\n'))
    try:
        global svi_avioni
        svi_avioni = model_aviona.kreiranje_modela_aviona(svi_avioni, naziv, broj_redova, pozicije_sedista)
        model_aviona.sacuvaj_modele_aviona('fajlovi/avioni.csv', ',', svi_avioni)
        print('Model aviona uspešno sačuvan.\n')
    except Exception as ex:
        print(ex)


def kreiraj_aerodrom():
    naziv = input('Unesite pun naziv aerodroma:\n')
    skracenica = input('Unesite troslovnu skraćenicu aerodroma:\n')
    if len(skracenica) != 3 or not skracenica.isalpha():
        print('Skraćenica aerodroma nije validna.\n')
        zajednicki_meni()
        return
    grad = input('Unesite grad u kom se arerodrom nalazi:\n')
    drzava = input('Unesite državu u kojoj se aerodrom nalazi:\n')
    try:
        global svi_aerodromi
        svi_aerodromi = aerodromi.kreiranje_aerodroma(svi_aerodromi, naziv, skracenica, grad, drzava)
        aerodromi.sacuvaj_aerodrome('fajlovi/aerodromi.csv', ',', svi_aerodromi)
        print('Model aerodroma uspešno sačuvan.\n')
    except Exception as ex:
        print(ex)


def checkin():
    # Ime i prezime će se koristiti ako prodavac checkinuje osobu
    ime = ''
    prezime = ''
    if trenutno_ulogovan_korisnik['uloga'] == konst.ULOGA_PRODAVAC:
        ime = input('Unesite ime osobe koju prijavljujete na let\n')
        prezime = input('Unesite prezime osobe koju prijavljujete na let\n')

    # Prođi kroz sve karte:
    # 1) ako prodavac checkinuje: proveri da li je osoba putnik u karata, ako jeste dodaj je u rečnik karata za checkin
    # 2) ako korisnik checkinuje: proveri da li je kupac karte, ako jeste dodaj je u rečnik karata za checkin
    karte_za_checkin = {}
    for karta in sve_karte.values():
        odgovarajuca_karta = False
        if prezime and ime:
            for putnik in karta['putnici']:
                if prezime == putnik['prezime'] and ime == putnik['ime']:
                    odgovarajuca_karta = True
                    break
        elif trenutno_ulogovan_korisnik['prezime'] == karta['kupac']['prezime'] \
                and trenutno_ulogovan_korisnik['ime'] == karta['kupac']['ime']:
            odgovarajuca_karta = True

        if odgovarajuca_karta:
            karte_za_checkin.update({karta['broj_karte']: karta})

    ispisi_karte(list(karte_za_checkin.values()))

    # Unesi broj karte i proveri da li je u listi karata za checkin
    broj_karte = input('Unesite broj karte\n')
    try:
        broj_karte = int(broj_karte)
    except ValueError:
        print('Greška: broj karte nije brojna vrednost.\n')
        zajednicki_meni()
        return
    if broj_karte not in karte_za_checkin:
        poruka = 'Greška: niste kupac karte sa unetim brojem.\n'
        if trenutno_ulogovan_korisnik['uloga'] == konst.ULOGA_PRODAVAC:
            poruka = 'Greška: uneti korisnik nije putnik u karata sa unetim brojem.\n'
        print(poruka)
        zajednicki_meni()

    karta = karte_za_checkin[broj_karte]
    checkinuj(karta, broj_karte)

    if len(karta['putnici']) > 1:
        checkinuj_drugog = input('Unesite DA ako checkinujete saputnika.\n')
        if checkinuj_drugog == 'DA':
            checkinuj(karta, broj_karte)


# Meni koji prikazuje opcije koje su dostupne korisniku svim registrovanim i neregistrovanim korisnicima
def zajednicki_meni():
    # Opcije za neregistrovane (i registrovane)
    meni_recnik = {
        '1': pregled_nerealizovanih_letova,
        '2': pretraga_konkretnih_letova,
        '3': prikaz_10_najjeftinijih,
        '4': fleksibilni_polasci,
        'x': dobrodoslica
    }

    ulogovan = trenutno_ulogovan_korisnik != {}

    poruka = '1. Pregled nerealizovanih letova\n' \
             '2. Pretraga konkretnih letova\n' \
             '3. Prikaz 10 najjeftinijih letova\n' \
             '4. Fleksibilni polasci\n'
    if ulogovan:
        # Opcije za korisnike
        if trenutno_ulogovan_korisnik['uloga'] == konst.ULOGA_KORISNIK:
            meni_recnik.update({'5': kupovina_karte})
            poruka += '5. Kupovina karte\n'

            meni_recnik.update({'6': checkin})
            poruka += '6. Prijava na let\n'

            meni_recnik.update({'7': azuriraj_podatke})
            poruka += '7. Izmena profila\n'

            meni_recnik.update({'8': prikaz_nerealizovanih_karata})
            poruka += '8. Prikaz nerealizovanih karata\n'
        # Opcije za prodavce
        elif trenutno_ulogovan_korisnik['uloga'] == konst.ULOGA_PRODAVAC:
            meni_recnik.update({'5': prodaja_karte})
            poruka += '5. Prodaja karte\n'

            meni_recnik.update({'6': checkin})
            poruka += '6. Prijava na let\n'

            meni_recnik.update({'7': izmena_karte})
            poruka += '7. Izmena karte\n'

            meni_recnik.update({'8': brisanje_karte})
            poruka += '8. Brisanje karte\n'

            meni_recnik.update({'9': prodate_karte})
            poruka += '9. Pretraga prodatih karata\n'
        # Opcije za admine
        elif trenutno_ulogovan_korisnik['uloga'] == konst.ULOGA_ADMIN:
            meni_recnik.update({'5': kreiranje_leta})
            poruka += '5. Kreiranje letova\n'

            meni_recnik.update({'6': izmena_leta})
            poruka += '6. Izmena letova\n'

            meni_recnik.update({'7': brisanje_karte})
            poruka += '7. Brisanje karte\n'

            meni_recnik.update({'8': prodate_karte})
            poruka += '8. Pretraga prodatih karata\n'

            meni_recnik.update({'9': registracija_prodavca})
            poruka += '9. Registracija prodavca\n'

            meni_recnik.update({'10': izvestaji_opcije})
            poruka += '10. Izvestaji\n'

            meni_recnik.update({'11': kreiraj_aerodrom})
            poruka += '11. Kreiranje areodroma\n'

            meni_recnik.update({'12': kreiraj_avion})
            poruka += '12. Kreiranje modela aviona\n'
    poruka += 'x. Nazad\n'

    while True:
        print('\nIzaberite jednu od sledećih opcija:')
        print(poruka)

        unos = input('>>')

        if unos in meni_recnik:
            if trenutno_ulogovan_korisnik and trenutno_ulogovan_korisnik['uloga'] != konst.ULOGA_ADMIN and unos == '5':
                meni_recnik[unos](svi_konkretni_letovi)
            else:
                meni_recnik[unos]()
            if unos == 'x':
                return
        else:
            print('Odabrali ste nepostojeću opciju.')


def ulogovanje():
    korisnicko_ime = input('Unesite Vaše korisničko ime.\n')
    lozinka = input('Unesite Vašu lozinku.\n')

    try:
        global trenutno_ulogovan_korisnik
        trenutno_ulogovan_korisnik = korisnici.login(svi_korisnici, korisnicko_ime, lozinka)
        zajednicki_meni()
    except Exception as ex:
        print(ex)
        dobrodoslica()


def izlogovanje():
    global trenutno_ulogovan_korisnik
    trenutno_ulogovan_korisnik = {}
    dobrodoslica()


def registracija():
    global svi_korisnici
    korisnicko_ime = input('Unesite Vaše korisničko ime.\n')
    lozinka = input('Unesite Vašu lozinku.\n')
    ime = input('Unesite Vaše ime.\n')
    prezime = input('Unesite Vaše prezime.\n')
    telefon = input('Unesite broj telefona (samo cifre).\n')
    email = input('Unesite email.\n')

    try:
        # Kreiraj korisnika
        svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici, False, konst.ULOGA_KORISNIK, None, korisnicko_ime,
                                                    lozinka, ime, prezime, email, '', '', telefon, '')
        # Sačuvaj rečnik svih korisnika u fajlu
        korisnici.sacuvaj_korisnike('fajlovi/korisnici.csv', ',', svi_korisnici)

        # Promeni globalnu promenljivog trenutno ulogovanog korisnika
        global trenutno_ulogovan_korisnik
        trenutno_ulogovan_korisnik = svi_korisnici.get(korisnicko_ime)
        zajednicki_meni()
    except Exception as ex:
        print(ex)


def izlaz():
    print('Hvala Vam što koristite program Air SV51/2022.\n')
    exit()


def dobrodoslica():
    ucitaj_sve_recnike()
    meni_recnik = {}

    ulogovan = trenutno_ulogovan_korisnik != {}

    # Postavljanje opcija menija dobrodošlice: 1. Ulogovanje / izlogovanje 2. Glavni meni 3. Registracija, 4. Izlaz

    meni_recnik.update({'1': ulogovanje})
    poruka = '1. Ulogovanje\n'

    if ulogovan:
        meni_recnik.update({'1': izlogovanje})
        poruka = '1. Izlogovanje\n'

    meni_recnik.update({'2': zajednicki_meni})
    poruka += '2. Glavni meni\n'

    if not ulogovan:
        meni_recnik.update({'3': registracija})
        poruka += '3. Registracija\n'

    poruka += 'x. Izlaz\n'
    meni_recnik.update({'x': izlaz})

    while True:
        print('=' * 30)
        print('\nDobro došli u program Air SV51/2022.\n')
        print('=' * 30)
        print('Izaberite jednu od sledećih opcija:')
        print(poruka)

        unos = input('>>')

        if unos in meni_recnik:
            meni_recnik[unos]()
        else:
            print('Odabrali ste nepostojeću opciju.')
