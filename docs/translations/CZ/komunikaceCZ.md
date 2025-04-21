Server komunikuje s klientem pomocí HTTP/HTTPS pro získávání dat a posílání jich do databáze.
Pro komunikaci se používají jenom POST a GET funkce HTTP. Používají se cesty v URI adrese pro rozpoznání těchto funkcí

# GET

Když server dostane prosbu o data, jedna z těchto cest rozhodne jak je vyřešena, některé prodě pošlou statická data, a proto jsem je spojil do jedné sekce.

## Static pages (/conntest, /add_hunt, /spse)

Stránky conntest a add_hunt pošlou statické HTML, conntest obsahuje zprávu že server je funkční a add_hunt říká že tato cesta je pouze pro přidávání dat.
Stránka spse přesměruje uživatele na stránku SPŠE Plzeň.

## i_venture_forth_to_hunt

Tato cesta je použitá pro získávání dat z databáze s filtrem na základě hashe lovu.
Jako URI parametry klient použije páry klíče a hodnot, kde klíč je vždy "f" a hodnota je hashe lovu podle kterého se bude filtrovat. Klient může použít jakýkoli počet párů.
Server odpoví  s hashí a a počtem kolikrát byl splněn.
Doporučený parametr pro klienta na použití je "t", který vrátí nejvíce splněné lovy. Uživatel může specifikovat počet kolik jich chce, ale server maximálně vrátí počet lovů v databázi.
Server odpoví seznamem hashí lovů a počtem jejich splnění.

# POST

Když server dostane prosby o uložení dat, tělo prosby obsahuje JSON s daty, jehož interpretace záleží na cestě.

## /add_hunt

Když  uživatel přidává lov, JSON obsahuje hodnoty sloupců a řádky s hodnotami pro lov. Když je lov poprvé zaznamenán, tak je přidán jako nový řádek, když ne tak se inkrementruje hodnota count v databázi. Po vyřešení server pošle potvrzení klientovi.

## /add_user

>[!WARNING] Varování
>toto není aktuálně podporováno

Když  uživatel přidává uživatele, JSON obsahuje hodnoty sloupců a řádky s hodnotami pro uživatele.  Když server dostane prosbu, přidá jí do databáze a pošle potvrzení klientovi.
