# Laivanupotuspeli Q-oppimisella

Miksi Q-oppiminen? Seuraava (optimaalinen) siirto saadaan Q-taulusta. Vaikeustason mukaan tätä "häiritään" x- ja y-suunnissa. Virhe pienenee logaritmisesti sen mukaan, kuinka monta osumaa Q-agentti on saanut pelaajan laivoihin. Näin agentti ei näytä hölmöltä pelin edetessä pidemmälle.

Vaihtoehtoisesti oltaisiin voitu käyttää Q-oppimisen sijaan tietoa siitä, mihin pelaaja on sijoittanut laivansa ja vastaavasti logaritmisesti "häiritä" optimaalista osumaa..

Vielä kuva pelin tuoksinnasta:

![Peli_kaynnissa](https://github.com/tickBit/Q-Laivanupotus/assets/61118857/1772ef4c-857b-4106-9406-fd709cde23b5)

Toivottavasti houkuttelee kokeilemaan. :)

## Pelin käynnistäminen

Peli käynnistetään kirjoittamalla komentotulkissa

python Laivanupotus.py

- tarvitsee myös lauta.py-tiedoston ja
- Meri-ja-laivat.jpg:n

Kuva on AI:n generoima.

## Python-ympäristö

Pelin kehitystyö tehtiin Python 3.10 -ympäristössä. Lähinnä huomioitavaa on, että NumPy-kirjastolla voidaan käyttää matriiseille rot90-metodia sekä bitwise and -operaatiota. Kehitysympäristössä käytettiin NumPy:stä versiota 1.24.1. Lisäksi tarvitaan jokin PyGame-kirjaston versio.

## Toteutus

Pelissä käytetään satunnaissiementä ja Q-oppiminen käynnistetään grid search -periaatteella etsien optimaalinen Q-taulu..

Pelin aikana käytetään kahta pelilautaa. Toinen on tarkoitettu vain AI-agentin Q-taulusta pelaamiseen. Toisella pelilaudalla on ihmispelaajan siirrot. Lautaan kopioidaan myös AI-agentin tekemät siirrot..

Pelissä on neljä vaikeustasoa, joissa AI-agentti parantaa peliään logaritmisesti seuraavan kuvan mukaisesti:

![Vaikeustaso](https://github.com/tickBit/Q-Laivanupotus/assets/61118857/47735f65-bd25-4e96-a575-943b1f608062)

Kuvassa x- ja y-suunnassa osuman häirinnän arvo on siis satunnaisluku väliltä 0..arvo, joka on kuvassa.

## Bugit

Mielestäni kerran todistin tilannetta, jossa AI-agentin laivat olivat sijoitettuna osin päällekkäin. Jahka kerkeän, yritän selvittää mikä mahdollisesti meni pieleen..
