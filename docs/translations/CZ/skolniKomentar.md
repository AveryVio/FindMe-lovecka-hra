# Zohlednění částí návrhů

## Server

Vybral jsem hostovat server na kontejneru Dockeru, aby se choval stejně na všech zařízeních. Jelikož existují dvě služby, použil jsem Docker Compose, aby jsem mohl jednodušeji ovládat běh obou.  
Jako databázi jsem vybral Postgres, pro jeho popularitu a tím pádem podporu a kompatibilitu. Nejsou použity žádné speciální typy dat, protože to by ztížilo práci s daty.  
Pro vytváření API pro aplikaci jsem použil python a vytvořil skript pro pracování s databází a komunikaci s klienty. Skript používá interní Python http serverovou knihovnu a posílá a dostává data ve formátu JSON pomocí knihovny. Tyto dvě jsem vybral pro jejich výtečnou dokumentaci oproti ostatním, co jsem našel. Pro práci s databází jsem vybral knihovnu psycopg, jelikož to je obecně doporučené řešení.  

## Firmware

Pro vývoj firmwaru jsem vypral MPLAB X IDE na doporučení učitelů.
Pro měnění Bluetooth ID zařízení potřebuji externí program, protože používání shellových příkazů z Makefily projektu způsobovalo nepředvídatelné chování. (někdy nahrazení textu selhalo) Pro to jsem vybral Python, protože už je využívaný v projektu a je na všech populárních platformách. V samotném skriptu požívám nástroj sed, který je v základu na Linuxu a Macu. Ne na Windows, ale je jednoduché ho stáhnou přes Winget.

# Project structure comments

## Server

Server používá jednu Postgres tabulku na ukládání lovů. Tabulka má interní id, ale každá řádka má huntid, které je vypočítáno klientem z ID checkpointů.
API skript používá JSON soubor pro POSTování lovů, místo url parametrů, protože to zabraňuje posílání nesprávných dat od klienta, protože Javascript má svojí knihovnu pro operace s JSON soubory. To není použito při použití GET, kde url parametry jsou použité, protože je jednodušší je zpracovat. Jsou však jednodušší poslat nesprávné, což není zde problematické, protože se tím neporuší data v databázi.

## Firmware

/* firmware není dokončený*/