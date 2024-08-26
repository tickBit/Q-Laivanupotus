# Laivanupotuspeli Q-oppimisella

Repossa on kaksi eri peliä laivanupotuksesta Q-oppimisella.

Laivanupotus.py (johon liittyy lauta.py) on peli, jossa Q-agentille opetetaan peli optimaalisesti aluksi kokonaan. Pelissä on neljä vaikeusastetta, joissa AI-agentti parantaa peliään logaritmisesti seuraavan kuvan mukaisesti:

![Vaikeustaso](https://github.com/tickBit/Q-Laivanupotus/assets/61118857/47735f65-bd25-4e96-a575-943b1f608062)

Kuvassa x- ja y-suunnassa osuman häirinnän arvo osumasta on siis satunnaisluku väliltä 0..arvo, joka on kuvassa.

Toinen peli on Laivanupotus_oppiva.py, jossa Q-agentti oppii pelin aikana pikkuhiljaa pelaamaan..

## Pelin käynnistäminen

Peli käynnistetään kirjoittamalla komentotulkissa

python Laivanupotus.py

tai

python Laivanupotus_oppiva.py

- tarvitaan vastaavasti myös lauta.py- tai lauta_oppiva.py-tiedoston ja
- Meri-ja-laivat.jpg

Kuva on AI:n generoima.

## Python-ympäristö

Pelin kehitystyö tehtiin Python 3.11 -ympäristössä. Lähinnä huomioitavaa on, että NumPy-kirjastolla voidaan käyttää matriiseille rot90-metodia sekä bitwise and -operaatiota. Kehitysympäristössä käytettiin NumPy:stä versiota 1.24.1. Lisäksi tarvitaan jokin PyGame-kirjaston versio.

## Kuva pelistä

Kuva pelin tuoksinnasta:

![Peli_kaynnissa](https://github.com/tickBit/Q-Laivanupotus/assets/61118857/1772ef4c-857b-4106-9406-fd709cde23b5)

Toivottavasti houkuttelee kokeilemaan. :)

## Bugit

Mielestäni kerran todistin tilannetta, jossa AI-agentin laivat olivat sijoitettuna osin päällekkäin. Jahka kerkeän, yritän selvittää mikä mahdollisesti meni pieleen..
