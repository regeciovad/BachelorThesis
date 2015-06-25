===========================
Bakalářská práce
===========================
Repositář pro moji bakalářskou práci.

Požadavky
============
Pro projekt Alan jsou zapotřebí tyto balíčky:
* python3
* python3-devel
* pip
* django >= 1.8

Instalace
============

* Instalujte všechny požadavky
* Získejte projekt pomocí příkazu:
```
    git clone https://github.com/regeciovad/BachelorThesis.git
    cd BachelorThesis
```
* Nastavte databázi

    `python3 manage.py migrate`

* Nahrajte data do databáze

    `python3 populate_alan.py`

* Nastavte administrátorský účet

    `python3 manage.py createsuperuser`
    * Enter username, email address and password (twice)
    
* Spusťte server

    `python3 manage.py runserver`
    
* Otevřete webový prohlížeč na adrese: http://127.0.0.1:8000/

URL adresy
=============

Projekt Alan má hierarchickou strukturu:

* http://127.0.0.1:8000/ - Stránka o projektu
* http://127.0.0.1:8000/admin/ - Administrátorská stránka
* http://127.0.0.1:8000/alan/ - Projekt

Dokumentace
=============

Oficiální dokumentace pro Django: [zde](https://docs.djangoproject.com/en/1.8/)
