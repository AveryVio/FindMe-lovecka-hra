Tady jsou všechny funkce a jejich vstupní parametry a vysvětlení jejich práce.

termíny:
cursor: spojení s databází (termín z psycopg)
slovník: struktura klíčů a hodnot (funkce pythonu)

# Databázové funkce

Tyto funkce používají knihovnu psycopg pro operace s postgresovou databází, všechny mají specifické obecné parametry:

> dbname (str): Jméno databáze  
> user (str): Uživatelské jméno  
> host (str): Hostující adresa  
> port (int): Číslo portu  
> table_name (str): Jméno tabullky  

Poté jsou specifické parametry, pro jendoduchost budou zkráceny na "generic_params".


## Funkce pro vytváření

create_table
>parametry: generic_params, columns(slovník)  
>vrací: True/False  

Funkce vytvoří cursor a vytvoří dotaz spojením sloupců a jejich typů. Poté ho spustí a vypíše zprávu úspěchu a vrátí True.
Když nastane chyba, vypíše chybovou zprávu a vrátí False.
## Fetchovací funkce
#### fetch_all_from_table
> parametry: generic_params  
> vrací: seznam slovníků/False  

Funkce vytvoří cursor a dotaz na získání všech sloupců, pak ho spustí. Dále extrahuje jména sloupců a spojí je s hodnotami do seznamu slovníků, to pak vrátí.
Pokud nastane chyba, vypíše chybovou zprávu a vrátí False.
#### fetch_columns_from_table
>parametry: generic_params, columns(seznam)  
>vrací: seznam slovníků/False  

Funkce vytvoří cursor a dotaz ze seznamu sloupců, pak ho spustí. Dále spojí sloupce a řady do seznamu slovníků a to vrátí
Pokud nastane chyba, vypíše chybovou zprávu a vrátí False.
#### fetch_columns_with_filter
>parametry: generic_params, columns(seznam), filter_column(text), filter_value(text)  
>vrací: seznam slovníků/prázdný seznam  

Funkce vytvoří cursor a udělá ze seznamu sloupců filtr sloupců a vytvoří dotaz, ten pak spustí. Dále vloží vrácené hodnoty do seznamu slovníků a to vrátí.
Když nastane chyba, vypíše chybovou zprávu a vrátí False.
#### entry_exists
>parametry: generic_params, column(text), value(text)  
>vrací: True/False  

Funkce vytvoří cursor a dotaz filtrující pro sloupec, ten pak spustí a vrátí True.
Když nastane chyba, vypíše chybovou zprávu a vrátí False.
## Vkládací funkce
#### insert_into_table
>parametry: generic_params, data(slovník)  
>vrací: True/False  


Funkce vytvoří cursor a spojí sloupce a řádky do dotazu, který poté spustí. Pokud nenastane chyba vrátí True.
Když nastane chyba, vypíše chybovou zprávu a vrátí False.

## Aktualizační funkce
#### update_table
>parametry: generic_params, data(slovník)  
>vrací: True/False  


Funkce vytvoří cursor a spojí sloupce a řádky do dotazu, který poté spustí. Pokud nenastane chyba vrátí True.
Když nastane chyba, vypíše chybovou zprávu a vrátí False

----

# HTTP funkce

HTTP server má několik interních funkcí pro definování odpovídání na HTTP dotazy.
Tento projekt používá pouze dvě a to GET  a POST. Obě odpovídají na specifické URI cesty a ty budou probrány odděleně.
Existuje také několik pomocných funkcí pro sjednocené odpovědi a čitelnější kód.

## Pomocné funkce

#### ExtractKeyValue
>parametry: data(slovník), key(text)
>vrací: slovník obsahující klíče a hodnoty dat

Funkce vezme parametry a vyjme hodnotu která spadá hodnotě klíče, pak je spáruje je do slovníku.

#### SendJSONResponse
>parametry: self(objekt), data(slovník)

Tato funkce vytvoří hlavičky a HTTP status, s tím pošle data jako JSON odpověď.

#### SendJSONQueryResponse
>parametry: self(objekt), response(slovník)

Tato funkce vytvoří hlavičky a HTTP status a Access Control Allow Metody, s tím pošle data jako JSON odpověď.

#### SendJSONError
>parametry: self(objekt), errorM(Exception)

Tato funkce vytvoří hlavičky a HTTP status a Access Control Allow Metody, s tím pošle chybovou zprávu jako JSON odpověď.

#### SendHTMLResponse
>parametry: self(objekt), message(text)

Tato funkce vytvoří hlavičky a HTTP status a Access Control Allow Metody, s tím pošle message jako HTML odpověď.

## do_GET
>parametry: self(obj)

#### /conntest

Pro testování jestli HTTP server funguje, bez závisení na psycopg, v podstatě hezčí ping.
#### /add_hunt

For GET dotazy, tato zpráva oznamuje ztraceným cestovatelům že tato cesta je pouze na POST.
#### /i_venture_forth_to_hunt

Funkce oddělí parametry od cesty, pokud jsou špatné, odpoví s chybovou zprávou.
Když jsou správně, oddělí klíče a hodnoty z slovníků, pak pomocí fetch_columns_with_filter() dostane data a ty pošle klientovi jako JSON soubor.
Když nastane chyba, pošle klientu chybovou zprávu.

#### /spse

Tato stránka pouze přesměruje na školní web.

## do_POST
>parametry: self(obj)

#### /add_hunt

Funkce zkontroluje jestli lov existuje v databázi pomocí entry_exists(). Když jo, tak inkrementuje sloupec count, poté pomocí update_table(), když neexistuje tak ho přidá do databáze pomocí insert_into_table(). Po vyřešení dotazu pošle uživateli potvrzení.
Když nastane chyba, pošle klientu chybovou zprávu.

#### /add_user

>[!WARNING] VAROVÁNÍ
>toto není aktuálně podporováno

Funkce načte JSON data a vloží uživatele do databáze, poté pošle uživateli potvrzení.
Když nastane chyba, pošle klientu chybovou zprávu.