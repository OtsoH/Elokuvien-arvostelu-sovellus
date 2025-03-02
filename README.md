# Elokuvien-arvostelu-sovellus

## Sovelluksen tilanne (lopullinen palautus)
 * Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
 * Käyttäjä pystyy luomaan haluamastaan elokuvasta arvostelun.
 * Käyttäjä pystyy muokkaamaan ja poistamaan omia arvostelujaan.
 * Käyttäjä näkee sovellukseen lisätyt arvostelut.
 * Käyttäjä pystyy etsimään arvosteluja hakusanalla.
 * Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän arvostelujen määrän sekä itse arvostelut
 * Käyttäjä pystyy määrittämään arvostelulleen kategorian sekä arvosanan
 * Muut käyttäjät voivat kommentoida toisten arvosteluja

   ## Sovelluksen asennus:
   Asenna flask:
   * $ pip install flask

   Luo tietokannan taulut ja lisää alkutiedot:
   * $ sqlite3 database.db < schema.sql
   * $ sqlite3 database.db < init.sql

   Käynnistys:
   * $ flask run
