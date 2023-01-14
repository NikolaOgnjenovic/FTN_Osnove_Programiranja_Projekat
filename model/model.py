from datetime import datetime

let = {
    "broj_leta": str,
    "sifra_polazisnog_aerodroma": str,
    "sifra_odredisnog_aerodorma": str,
    "vreme_poletanja": str,
    "vreme_sletanja": str,
    "sletanje_sutra": bool,
    "prevoznik": str,
    "dani": str,
    "model": dict,
    "cena": float,
    "datum_pocetka_operativnosti": datetime,
    "datum_kraja_operativnosti": datetime
}

konkretan_let = {
    "sifra": int,
    "broj_leta": str,
    "datum_i_vreme_polaska": datetime,
    "datum_i_vreme_dolaska": datetime,
    "zauzetost": iter,  # bilo koja vrsta kolekcije koja je adekvatna
}

model_aviona = {
    "id": int,
    "naziv": str,
    "broj_redova": int,
    "pozicije_sedista": list  # lista stringova
}

karta = {
    "broj_karte": int,
    "putnici": iter,
    "sifra_konkretnog_leta": int,
    "status": str,
    "obrisana": bool,
    "datum_prodaje": datetime,
    "prodavac": str,
    "kupac": str,
    "sediste": str
}

korisnik = {
    'uloga': str,
    'korisnicko_ime': str,
    'lozinka': str,
    'ime': str,
    'prezime': str,
    'email': str,
    'pasos': str,
    'drzavljanstvo': str,
    'telefon': str,
    'pol': str
}

# Čuvaju se i čitaju se iz zasebnog fajla, koriste se za kreiranje elemenata sa jedinstvenim ključem
vrednosti_sifri = {
    'sifra_konkretnog_leta': int,
    'broj_karte': int
}

aerodrom = {
    'skracenica': str,
    'pun_naziv': str,
    'grad': str,
    'drzava': str
}
