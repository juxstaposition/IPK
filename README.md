#	VUT FIT Brno, Počítačové komunikace a sítě			
##	Projekt 1: HTTP resolvér doménových mien
###	Autor: Daniel Miloslav Očenáš (xocena06)
###	Dátum: 3.2020							
###	Popis: Server komunikujúci s protokolom HTTP, zaistujúci preklad doménovych mien

Cieľom prvého projektu v predmete IPK 2019/2020 bolo vytvoriť resolvér doménových mien HTTP požiadaviek typu GET a POST. Projekt som vytvoril v jazyku Python pomocou knižnice *socket* ako server, ktorý prijíma požiadavky na porte špecifikovanom pri spustení programu. 

Prikaz pre spustenie:
```make run PORT=number```

Pre moje riešenie musí platiť *number ∈ <2^10,2^16>* čím som obmedzil pouzitie portov pre ktoré je potrebné administrátorské povolenie. 

Server čaká na HTTP požiadavky verzie HTTP/1.1 (iná verzia nie je podporovaná) až pokým nie je manuálne prerušený pomocou signálu SIGINT.

Funkcia *parseData* je použitá na kontrolu tela požiadavky po synktaktickej stránke,
a vracia upravenú štruktúru dát.

Funkcia *sendResponse(conn, params)* použitá na odoslanie odpovedi zo servru.
Príjíma výstup funkcie parseData, ktoré priamo odosiela v odpovedi. 
V tejto funkcí sú do odpovedi pridané hlavičky: Typ odpovede s návrátovým kódom, Content-Type, Content-Length, Connection a Date 

Pre kontrolu parametru name v tele požiadavky používam funkcie *chceckUrl* a *chechIpAdress*, ktoré skontrolujú platný formát 
