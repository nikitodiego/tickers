# tickers

Aplicación de carga, actualización y visualización de datos financieros de la API Polygon.

Para correr el script, ejecutar en consola: python app.py

El archivo functions.py es un contenedor de funciones importadas en el archivo principal. 

En cada una de ellas se explica la funcionalidad (comments).

Se modulariza el código para separar la lógica de la aplicación, de la persistencia.

Se utiliza la DB portable SQLite (tickers.db).

Como extras a la consigna, se desarrolla el manejo de errores y excepciones:

1- a nivel de aplicación (por ejemplo al ingresar opciones distintas a las del menú principal)

2- a nivel de request (http, conexión, timeout)

3- a nivel de persistencia (conexión a la base de datos, lectura y escritura).
