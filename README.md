# Laivanuoptuspeli Q-oppimisella

Miksi Q-oppiminen? Seuraava (optimaalinen) siirto saadaan Q-taulusta. Vaikeustason mukaan tätä "häiritään" x- ja y-suunnissa logaritmisella vähentämisellä sen mukaan, kuinka monta osumaa Q-agentti on saanut pelaajan laivoihin. Näin agentti ei näytä hölmöltä pelin edetessä pidemmälle.

Vaihtoehtoisesti oltaisiin voitu käyttää Q-oppimisen sijaan käyttää tietoa siitä, mihin pelaaja on sijoittanut laivansa ja vastaavasti logaritmisesti "häiritä" optimaalista osumaa..

## Pelin käynnistäminen

Peli käynnistetään kirjoittamalla komentotulkissa

python Laivanupotus.py

- tarvitsee myös lauta.py-tiedoston ja
- Meri-ja-laivat.jpg:n

Kuva on AI:n generoima.

## Python-ympäristö

Pelin kehitystyö tehtiin Python 3.10 -ympäristössä. Lähinnä huomioitavaa on, että NumPy-kirjastolla voidaan käyttää matriiseille rot90-metodia sekä bitwise and -operaatiota. Kehitysympäristössä käytettiin NumPy:stä versiota 1.24.1. Lisäksi tarvitaan jokin PyGame-kirjaston versio.

## Toteutus

Pelin aikana käytetään kahta pelilautaa. Toinen on tarkoitettu vain AI-agentin Q-taulusta pelaamiseen. Toisella pelilaudalla on ihmispelaajan siirrot. Lautaan kopioidaan myös AI-agentin tekemät siirrot..

Pelissä on neljä vaikeustasoa, joissa AI-agentti parantaa peliään logaritmisesti seuraavan kuvan mukaisesti:

![KUVA_6_Vaikeustaso](https://github.com/tickBit/Q-Laivanupotus/assets/61118857/89ec3887-97d1-4e2a-a825-e4ab2ac92881)

## Bugit

Mielestäni kerran todistin tilannetta, jossa AI-agentin laivat olivat sijoitettuna osin päällekkäin. Jahka kerkeän, yritän selvittää mikä mahdollisesti meni pieleen..
