Segunda entrega del proyecto
============================

Se consideran foros de discusión como los de la primera entrega: en el
formato conocido y con la misma estructura. En esta entrega hay dos
objetivos: (i) analizar la estructura del agrupamiento de usuarios en
un foro de discusión y (ii) clasificar los mensajes publicados por los
usuarios en un foro de discusión.


Parte (i)
---------

Para (i) se debe construir un grafo (no dirigido) G = (V, E, w : E ->
Nats) a partir de un foro de discusión F. Los vértices V son los
nombres de los usuarios participando en F. Cada arco (u, v) en E
indica que u respondió (directa o indirectamente) un mensaje de v o
viceversa. La función de peso w sobre los arcos en E es tal que para
cualquier (u, v) en E la cantidad w(u, v) corresponde a la parte
entera del promedio de los tiempos (en segundos) entre los que
interactúan u y v. Por ejemplo, si se tiene el siguiente árbol que
representa F, en donde a y b son usuarios diferentes a u y v, y el
tiempo que transcurre entre cada comunicación directa etiqueta los
arcos

                      u
                   3/   \5
                   v     a
                  6|  2/ |2 \3
                   u  u  v   b

entonces hay 3 interacciones entre u y v: dos directas con duraciones
3 y 6, respectivamente, y una indirecta con duración 7 (5+2). El
promedio de las tres interacciones es 5.333... y su parte entera es
5. Luego, w(u, v) en el grafo G es 5.

Una vez se cuenta con el grafo, el siguiente paso es construir una
teselación de Voronoi a partir de una serie de vértices centro C,
subconjunto de G. Dados C, una teselación de Voronoi de G con respecto
a C es tal que a cada centro c en C se asocia una colección de
vértices en G que corresponde a todos aquellos vértices que están más
cerca a c que a cualquier otro centro en C. La forma de determinar los
centros C se describe a continuación:

  - Construir la distribución de grado de G.

  - Identificar la colección de grados con máxima frecuencia y tomar
    como cantidad de centros el grado más pequeño entre ellas.

  - La cantidad de centros debe ser al menos 2.

Por ejemplo, si la distribución de grados de G es:

  1 |-> 1
  2 |-> 5
  3 |-> 7
  4 |-> 4
  5 |-> 6
  6 |-> 7
  7 |-> 6
  8 |-> 2
  9 |-> 3
  
entonces aquellos grados con máxima frecuencia son 3 y 6. En este
caso, la cantidad de centros sería 3.

Una vez se ha determinado la cantidad de centros k, se pueden escoger
los centros C para la teselación de Voronoi: C es el conjunto de los k
primeros vértices en el orden descendente de usuarios ponderados por
su cantidad de participaciones en los foro (esta lista se construyó
para la primera entrega; los centros son primeros k usuarios de la
lista).


Parte (ii)
----------

Para (ii) se debe asociar a cada mensaje una pareja de números (i,j)
de la siguiente manera. Para cada mensaje T (i.e., secuencia de
palabras), dicha pareja (i, j) representa un segmento de palabras en T
tal que T[i, j) contiene todas las palabras de T bajo ciertas
condiciones que se presentan a continuación. En un mensaje T, una
palabra se define como una secuencia maximal de caracteres
alfabéticos, en mayúsculas o minúsculas. Por ejemplo, en el mensaje T
correspondiente a

  Yes sir!!!. Right away #SiR. ????right, SIR????Yes:)

las palabras son

  Yes
  sir
  Right
  away
  SiR
  right
  SIR
  Yes

Sin embargo, para el análisis, no se distinguirán diferencias entre
mayúsculas y minúsculas. Por tanto, la lista anterior se reduce a
(escribiendo todo en minúsculas)

  yes
  sir
  right
  away

Bajo este esquema, las parejas (no es una lista exhaustiva)

  0 4
  0 8
  3 8

son tales que T[0, 4), T[0, 8) y T[3, 8) contienen todas las palabras
en T. Entre estas parejas, y aquellas otras que no se muestran y
cumplen la propiedad dada, es

 0 4

la que induce la secuencia más pequeña en T que incluye todas las
palabras de T.

En caso tal de que para un texto T haya más de una pareja (i, j)
con (j-i) minimal, se debe escoger aquella pareja que tenga menor i.


Instrucciones para la entrega
-----------------------------

Para cada árbol F que representa un foro de discusión se deben generar
varias líneas de texto. Las primeras k (i.e., cantidad de centros, tal
y como se describe para la parte (i)) líneas presentan las k
Teselaciones de Voronoi en grafo construido G para la parte (i). Cada
una de estas líneas lista tiene el formato:

  <center> <vertices> <dist>

en donde

  <center> es el nombre del vértice centro

  <vertices> es la lista de nombres de los vértices en la celda de <center>

  <dist> es la suma de las distancias de <center> a cada uno de los
         vértices en <vertices>

Cada para de elementos consecutivos en una línea se separan por un
espacio sencillo. Las k líneas se presentan ascendentemente por el
nombre del centro.

Luego vienen tantas líneas como textos haya en F y en el preorden de
F, cada una con el formato:

  <comment_id> <i> <j>

en donde

  <comment_id> es el identificador del mensaje

  <i> <j> como se indica en la descripción de la parte (ii) para el mensaje
          identificado con <comment_id>

