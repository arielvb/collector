BGG
====

File
----

Artists
.......
Search: http://boardgamegeek.com/geeksearch.php?action=search&objecttype=boardgameartist&q=Michael&B1=Go
File: http://boardgamegeek.com/boardgameartist/6565/michael-resch

Boardgame
.........
File: http://boardgamegeek.com/boardgame/106999/coney-island

Boardgame name is only a decorator, the boardgame id is 106999 for coney island

Images
......
All images:
	http://boardgamegeek.com/images/boardgame/106999/coney-island

sizes = { 'square', 'small', 'medium', 'large', 'original'} # original requires register, large is 1024x683

http://boardgamegeek.com/image/1411264/coney-island?size=medium
http://boardgamegeek.com/image/1411264/coney-island?size=square

Game Opengraph information
--------------------------
All the files have opengraph information::

{i.get("name") : i.get("content") for i in soup.find_all("meta", attrs={'name':re.compile("og:*")})}

XMLAPI
------

Boardgamegeek té una api on mostra una part de la seva informació, en el cas de la fitxa falten dades
 com la puntuació. 

XMLAPI va compleix les nostres necesitats per la cerca i per la importació de les col·lecions de l'usuari.

La informació de l'api es troba disponible a `Boardgame XML API`_.

.. _BoardGameGeek XML API: http://boardgamegeek.com/xmlapi

Referències
-----------

- BoardgameGeek http://boardgamegeek.com (2012-08)
- http://boardgamegeek.com/xmlapi (2012-11-13)
