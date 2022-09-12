import sqlite3
from sqlite3 import Error
import requests
import json
import datetime
import matplotlib.pyplot as plt


#Crea la DB tomando como parámetro el nombre del archivo con extensión .db. En este caso ya fue creada.
def create_database(db_file):
    con = None
    try:
        con = sqlite3.connect(db_file)
        print(f"DB {db_file} created.")
    except Error as e:
        print(e)
    con.close()
    
#Crea la tabla en la DB tickers.db, tomando como parámetro el nombre de la misma(ticker), con los siguientes campos:
#clave primaria, fecha en formato unix almacenada como int, y el valor de cierre del activo en cuestión.
def create_table(name):
    # Creamos una conexión con la base de datos
    try:
        con = sqlite3.connect('tickers.db')
        cursor = con.cursor()
        res = cursor.execute(f'''
        CREATE TABLE {name} (
        ticker_id INTEGER PRIMARY KEY,
        date INTEGER NOT NULL,
        value FLOAT NOT NULL);
        ''')
        print(f"Table {name} created.")
    except Error as e:
        print(e)
    con.close()

#Borra la información en la tabla tomada como parámetro.
def delete_data(ticker):
    try:
        con = sqlite3.connect("tickers.db")
        print('database connected..')
        cs = con.cursor()
        sql_date = f'''DELETE FROM {ticker};'''
        query= cs.execute(sql_date)
        con.commit()
        print(f"Ticker {ticker} deleted.")
    except Exception as e:
        print(e)
    con.close()

#Función que toma como parámetro el nombre de una tabla(ticker). Si ya existe, borra los datos.
#Si no, crea una nueva tabla.
def validate_table(table):
    list=[] 
    try:
        con = sqlite3.connect("tickers.db")
        print('database connected..')
        cs = con.cursor()
        sql_base = ''' SELECT name FROM sqlite_master WHERE type='table';'''
        recs = cs.execute(sql_base)
        for rec in recs:
            list.append(rec[0])
    except Error as e:
        print(e)
    con.close()
    if table in list:
        print("Tabla existente, actualizando...")
        delete_data(table)
    else: 
        print("Creando nueva tabla...")
        create_table(table)


#Toma como parámetros el ticker y las dos fechas. Intenta hacer el request, capturando primero los errores http, conexión, timeout. 
#Para probar estos errores, intenté por ejemplo correr la app sin conexión a internet, o escribiendo un endpoint erróneo.
#Si pasa el try/except y se conecta a la API, luego tratamos los errores internos, como el 404, fechas no válidas, etc.
#Finalmente si el request es válido y arroja resultados, la función retorna el diccionario deserializado.
def request(ticker,start,end):
    try:
       json_file = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}?adjusted=true&sort=asc&limit=120&apiKey=xq8hXRh0WMbU0GDDu8MNQubBsEzyo1uw")    
    except requests.exceptions.HTTPError as errh:
        return ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        return ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        return ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        return ("OOps: Something Else",err)
    if json_file.status_code==404:
        return "Error 404. Ingrese datos válidos."
    deserial = json.loads(json_file.text)
    if deserial["status"]=="ERROR":
        return deserial["error"]
    elif deserial["status"]=="OK" and int(deserial["queryCount"])==0:
        return "Ingrese datos válidos para el request."
    elif deserial["status"]=="OK" and int(deserial["queryCount"])>0:
        return deserial
    

#Toma como parámetro el diccionario y carga id, fecha y valor en la DB.
def update_data(deserial):
    try:
        con = sqlite3.connect("tickers.db")
        print('database connected..')
        cs = con.cursor()
        j = 0
        for i in deserial["results"]:
            sql_base = ''' 
            INSERT INTO '{ticker}' (ticker_id, date, value)
            VALUES ('{j}', '{fecha}','{valor}');
            '''
            cs.execute(sql_base.format(ticker=deserial["ticker"],j=j, fecha=i["t"], valor=i["c"]))
            con.commit()
            j += 1
        print("Ticker updated.")
    except Error as e:
        print(e)
    con.close()

#Recorre las tablas y presenta en consola nombre y rango de fechas almacenadas.
def resumen():
    list = []  # lista de tablas
    list2 = []  # lista de datos por tabla
    try:
        con = sqlite3.connect("tickers.db")
        print('database connected..')
        cs = con.cursor()

        sql_base = ''' 
            SELECT name FROM sqlite_master WHERE type='table';
            '''
        recs = cs.execute(sql_base)
        for rec in recs:
            list.append(rec[0])
        for i in list:
            query = '''SELECT date FROM '{table}' ORDER BY date ASC;'''
            dates = cs.execute(query.format(table=i))
            for date in dates:
                list2.append(date[0])
            if len(list2) > 0:
                print(i, str(datetime.datetime.fromtimestamp(list2[0]/1000))[:-9], str(datetime.datetime.fromtimestamp(list2[-1]/1000))[:-9])
            else:
                print(i, "lista vacía")
            list2 = []
    except Error as e:
        print(e)
    con.close()

#Toma como parámetro el ticker(nombre de la tabla) y grafica el valor de cierre en función de la fecha.
def plot(table):
    list = []  # lista de fechas
    list2 = []  # lista de valores
    try:
        con = sqlite3.connect("tickers.db")
        print('database connected..')
        cs = con.cursor()
        query = '''SELECT date,value FROM '{table}' ORDER BY date ASC;'''
        data = cs.execute(query.format(table=table))
        for i in data:
            list.append(str(datetime.datetime.fromtimestamp(i[0]/1000)))
            list2.append(i[1])
    except Error as e:
        print(e)
    con.close()

    dates = [datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in list]

    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    ax.set(title=f"{table}")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    ax.plot(dates, list2, linewidth=2, color="red")
    return plt.show()
