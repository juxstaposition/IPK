#	VUT FIT Brno, Počítačové komunikace a sítě			
##	Projekt 1: HTTP resolver doménových mien
###	Autor: Daniel Miloslav Ocenas (xocena06)
###	Datum: 3.2020							
###	Popis: Server komunikujuci s protokolom HTTP, zaistujuci preklad domenovych mien

Cieľom prvého projektu v predmete IPK 2019/2020 bolo vytvoriť resolvér doménových mien HTTP požiadaviek typu GET a POST. Projekt som vytvoril v jazyku Python pomocou knižnice *socket* ako server, ktorý prijíma požiadavky na porte špecifikovanom pri spustení programu. 

Prikaz pre spustenie:
```make run PORT=number```

Pre moje riešenie musí platiť *number ∈ <2^10,2^16>* čím som obmedzil pouzitie portov pre ktoré je potrebné administrátorské povolenie. 

Server čaká na HTTP požiadavky verzie HTTP/1.1 (iná verzia nie je podporovaná) pokiaľ nie je manuálne prerušený pomocou signálu SIGINT.

