# server

Server běží na kontejnerech pomocí Docker Compose, aktuálně používáme dva kontejnery, jeden pro databázi a jeden pro API vytvořené pomocí Pythonu. Vysvětlení funkcí v API je [zde](API-funkce-vysvetleniCZ.md).


## Databáze

Tento projekt používá Postgres jako databázi, která jak bylo dříve zmíněno existuje na odděleném kontejneru od API. Jeho proměnné prostředí jsou stanoveny v souboru Docker Compose, kde je  jméno databáze a uživatel. Prozatím není implementovaná zabezpečení, ale v budoucnu budou přidaná.

Rozložení tabulek v databázi není finální, ale prozatím je takovéto:
//todo
TableWhale - testovací tabulka (pro startovací testy sama sebe)

| sloupec | id                    | number  | name |
| ------- | --------------------- | ------- | ---- |
| typ     | BIGSERIAL PRIMARY KEY | INTEGER | TEXT |
TableHunts - primární tabulka pro ukládání čísel lovů

| sloupec | id                    | huntid | count   |
| ------- | --------------------- | ------ | ------- |
| typ     | BIGSERIAL PRIMARY KEY | TEXT   | INTEGER |
>huntid ukládá identifikační hashi pro každý lov, ale id je jedinečný identifikátor v databázi (to je opatření pro zastavení chyb v budoucu), count ukládá počet kolikrát byl lov dokončen, začínající na 1

TableUsers - musí být vyvinut (bude pro ukládání uživatelů a možná i systém účtů)

| soupec | id                    | userid |
| ------ | --------------------- | ------ |
| typ    | BIGSERIAL PRIMARY KEY | TEXT   |
>huntid ukládá identifikační hashi pro každého uživatele, ale id je jedinečný identifikátor v databázi (to je opatření pro zastavení chyb v budoucu)


## API

API je z Pythonu, používající standartní knihovny a [psycopg3](https://psycopg.org/) pro komunikace s databází a hostování http/https serveru.

Server komunikuje přímo s klientem přes http/https, formát komunikace je probrán [zde](komunikaceCZ.md).  Komunikace mezi API a databází probíhá přes vnitřní síť, ale to je mimo rozsah této dokumentace, můžete zjistit více v [dokumentace psycopg3](https://www.psycopg.org/psycopg3/docs/).

----
# firmware
