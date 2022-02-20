# tsoha-keskustelusovellus
Tietokantasovellus-kurssin harjoitustyö

## Kuvaus

Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

## Sovelluksen testaaminen

Sovellusta voi testat Herokussa menemällä osoitteeseen https://tsoha-keskustelu-app.herokuapp.com/. Testaaminen kannattaa aloittaa luomalla uusi käyttäjätunnus. Käyttäjätunnuksen luomiseen pääsee menemällä etusivun alimman rivin viimeisessä sanassa olevaan linkkiin.

## Sovelluksen nykyinen tilanne lyhyesti
Valtaosa tavoiteltavista toiminnallisuuksista on implementoitu. Viimeistä palautusta varten on tarkoitus keskittyä enemmän käytettävyyteen (kuten navigointiin), ulkoasuun, syötteiden validointiin ja koodin sisäiseen laatuun.

## Nykyisiä ominaisuuksia

Sovelluksen ominaisuudet tällä hetkellä:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- Käyttäjä voi muokata lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

## Tavoiteltavia ominaisuuksia

Sovelluksen tavoiteltavia ominaisuuksia:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

## Tunnettuja ongelmia tällä hetkellä
- Salaiset alueet eivät ole kunnolla piilotettu, eli esimerkiksi hakutoiminnolla voidaan päästä käsiksi salattujen alueiden ketjuihin.