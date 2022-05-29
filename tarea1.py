import cx_Oracle
import csv


#create connection to Oracle
print("Conexión a base de datos:")
connection = cx_Oracle.connect(user = input("Usuario: "),
                password = input("Clave: "),
                dsn = input("dsn (ip:port/db_name): "))
cursor = connection.cursor()


"""FUNCIONES DE CREACIÓN E INSERT DE TABLAS:"""

############################################################################################################################
# create_juegos_table()
#----------------------------------------------------------
# sin parametros.
#----------------------------------------------------------
# Función recursiva que crea la tabla JUEGOS en la base de datos
# si es que no existe, si existe la borra y crea una nueva.
# Por lo que cada vez que se llame la función, se recrea la tabla.
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def create_juegos_table():
    try:
        cursor.execute (
            """ 
                CREATE TABLE JUEGOS (
                    rank INTEGER PRIMARY KEY NOT NULL,
                    name VARCHAR(200) NOT NULL,
                    platform VARCHAR2(7) NOT NULL,
                    year INT NOT NULL,
                    genre VARCHAR(15) NOT NULL,
                    publisher VARCHAR2(40) NOT NULL,
                    na_sale NUMERIC(6,3)NOT NULL,
                    eu_sale NUMERIC(6,3)NOT NULL,
                    jp_sale NUMERIC(6,3)NOT NULL,
                    other_sale NUMERIC(6,3) NOT NULL,
                    global_sale NUMERIC(6,3) NOT NULL
                )
                
            """
        )
    except:
        cursor.execute("DROP TABLE JUEGOS")
        create_juegos_table()
    return


############################################################################################################################
# create_biblioteca_table()
#----------------------------------------------------------
# sin parametros.
#----------------------------------------------------------
# Función recursiva que crea la tabla Biblioteca en la base de datos
# si es que no existe, si existe la borra y crea una nueva.
# Por lo que cada vez que se llame la función, se recrea la tabla.
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def create_biblioteca_table():
    try:
        cursor.execute (
                """ 
                    CREATE TABLE BIBLIOTECA (
                        id INTEGER PRIMARY KEY,
                        rank INTEGER NOT NULL,
                        name VARCHAR(200) NOT NULL,
                        platform VARCHAR2(7) NOT NULL,
                        year INT NOT NULL,
                        genre VARCHAR(15) NOT NULL,
                        publisher VARCHAR2(40) NOT NULL,
                        rating SMALLINT NOT NULL
                    )
                """
            )
        cursor.execute ("""CREATE VIEW BIBLIOTECA_VIEW AS SELECT * FROM BIBLIOTECA""")

    except:
        cursor.execute("DROP TABLE BIBLIOTECA")
        cursor.execute("DROP VIEW BIBLIOTECA_VIEW")
        create_biblioteca_table()
    return


############################################################################################################################
# create_basurero_table()
#----------------------------------------------------------
# sin parametros.
#----------------------------------------------------------
# Función recursiva que crea la tabla Basurero en la base de datos
# si es que no existe, si existe la borra y crea una nueva.
# Por lo que cada vez que se llame la función, se recrea la tabla.
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def create_basurero_table():
    try:
        cursor.execute (
                """ 
                    CREATE TABLE BASURERO (
                        id INTEGER PRIMARY KEY,
                        rank INTEGER NOT NULL,
                        name VARCHAR(200) NOT NULL,
                        platform VARCHAR2(7) NOT NULL,
                        action VARCHAR(30) NOT NULL
                    )
                """
            )
    except:
        cursor.execute("DROP TABLE BASURERO")
        create_biblioteca_table()
    return


############################################################################################################################
# show_basurero()
#----------------------------------------------------------
# sin parametros.
#----------------------------------------------------------
# Función que imprime el contenido de la tabla Basurero.
# Si no hay nada en la tabla, imprime un mensaje.
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def show_basurero():
    cursor.execute("""SELECT * FROM BASURERO""")
    row = cursor.fetchone()
    if row == None:
        print("No hay nada en el basurero :(")
    else:
        cursor.execute("""SELECT * FROM BASURERO""")
        rows = cursor.fetchall()
        print("\n")
        print("NOMBRE\tPLATAFORMA\tACTION")
        print("\n") 
        for row in rows:
            print(row[2],row[3],row[4])
        print("\n")
    return


############################################################################################################################
# insert_juegos_data()
#----------------------------------------------------------
# sin parametros.
#----------------------------------------------------------
# Función que crea llamas las funciones anteriores para crear
# las tablas y luego inserta los datos de los juegos en la tabla JUEGOS.
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def insert_juegos_data():
    create_juegos_table()
    create_biblioteca_table()
    create_basurero_table()

    with open('juegos.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for line in reader: 
            line["Year"] = int(line["Year"]) if line["Year"].isnumeric() else 0
            cursor.execute (
                """
                    INSERT INTO JUEGOS (rank, name, platform, year, genre, publisher, na_sale, eu_sale, jp_sale, other_sale, global_sale)
                    VALUES (:0, :1, :2, :3, :4, :5, :6, :7, :8, :9, :10)
                """,
                (int(line['Rank']), line['Name'], line['Platform'], line['Year'], line['Genre'], 
                line['Publisher'], float(line['NA_Sales']), float(line['EU_Sales']), 
                float(line['JP_Sales']), float(line['Other_Sales']), float(line['Global_Sales']))
            )
        print("CSV Cargado :) \n")
    
    cursor.execute("""
    CREATE TRIGGER transacciones_trigger
    AFTER INSERT OR DELETE ON BIBLIOTECA
    FOR EACH ROW
    BEGIN
        IF DELETING THEN
            INSERT INTO BASURERO
            (Id,Rank,Name,Platform,Action) 
            VALUES 
            (:old.Id,:old.Rank,:old.Name,:old.Platform,'Eliminado');
        END IF;
    END;
    """)

    return



"""FUNCIONES DE CONSULTA:"""


############################################################################################################################
# show_biblioteca()
#----------------------------------------------------------
# sin parametros.
#----------------------------------------------------------
# Función que imprime el contenido de la tabla Biblioteca.
# Si no hay nada en la tabla, imprime un mensaje.
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def show_biblioteca():
    cursor.execute("SELECT * FROM BIBLIOTECA")
    row = cursor.fetchone()
    if row == None:
        print("No hay nada en la biblioteca :(")
    else:
        cursor.execute("""SELECT * FROM BIBLIOTECA_VIEW""")
        rows = cursor.fetchall()
        print("\n")
        print("NOMBRE\tPLATAFORMA\tRATING")
        print("\n") 
        for row in rows:
            print(row[2], "\t", row[3], "\t", row[7])
        print("\n")
    return


############################################################################################################################
# buy_game(name)
#----------------------------------------------------------
# str name
#----------------------------------------------------------
# Función que recibe el nombre de un juego, lo busca en la tabla JUEGOS
# y lo inserta en la tabla Biblioteca. Si el juego no existe, imprime un mensaje.
# Ademas pide el rating del juego.
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def buy_game(name):
    cursor.execute("""SELECT * FROM JUEGOS
                    WHERE name = :name
                    """,
                    name = name,)
    row = cursor.fetchone()
    if row is not None:
        cursor.execute("""SELECT * FROM BIBLIOTECA WHERE name = :name""",name=name)
        row2 = cursor.fetchone()
        if row2 is None:
            while True:
                print("Califica el juego:")
                ra = int(input("1-5: "))
                if ra > 5 or ra < 1:
                    print("No es una calificación valida \n")
                else:
                    False
                    break
            cursor.execute("""
                            INSERT INTO BIBLIOTECA (id, rank, name, platform, year, genre, publisher, rating)
                            VALUES (:id, :rank, :name, :platform, :year, :genre, :publisher, :rating)
                            """,
                            id = row[0],
                            rank = row[0],
                            name = row[1],
                            platform = row[2],
                            year = row[3],
                            genre = row[4],
                            publisher = row[5],
                            rating = ra
                            )


            print("Juego comprado y agregado a tu biblioteca :) \n")
        else:
            print("Ya tienes este juego en tu biblioteca")

    else:
        print("No existe ese juego")
    return



############################################################################################################################
# ranking_games_total()
#----------------------------------------------------------
# sin parametros.
#----------------------------------------------------------
# Función que imprime el ranking de los 5 juegos en la tabla JUEGOS
# ordenados por el total de ventas.
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def ranking_games_total():
    cursor.execute("""SELECT * FROM JUEGOS ORDER BY global_sale DESC""")
    count = 0
    while count < 5:
        row = cursor.fetchone()
        print(".-",row[1] , ":", row[10] , "Millones")
        count += 1
    return



############################################################################################################################
# ranking_games_genre(generos)
#----------------------------------------------------------
# int generos
#----------------------------------------------------------
# Función recibe un genero e imprime el ranking de los 5 juegos
# en la tabla JUEGOS ordenados por el total de ventas, de ese genero.
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def ranking_games_genre(generos):

    cursor.execute('''
                    SELECT * FROM JUEGOS
                    WHERE genre = :generos
                    ORDER BY global_sale DESC
                    ''',generos=generos)
    count = 0
    a = 0
    while count < 5:
        row = cursor.fetchone()
        if row is not None:
            print(".-",row[1] , ":", row[10] , "Millones")
            a = 1
        count += 1
    if a == 0:
        print("No hay juegos de ese genero")
    return



############################################################################################################################
# delete_game(name)
#----------------------------------------------------------
# str name
#----------------------------------------------------------
# Función que recibe el nombre de un juego, lo busca en la tabla Biblioteca
# y lo elimina. Si el juego no existe, imprime un mensaje.
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def delete_game(name):
    cursor.execute("""SELECT * FROM BIBLIOTECA WHERE name = :name""",name=name)
    row = cursor.fetchone()
    if row is not None:
        cursor.execute("""DELETE FROM BIBLIOTECA WHERE name = :name""",name=name)
        print("Juego eliminado de tu biblioteca :) \n")
    else:
        print("No existe ese juego en tu biblioteca")

    connection.commit()
    return



############################################################################################################################
# update_game(name)
#----------------------------------------------------------
# str name
#----------------------------------------------------------
# Función que recibe el nombre de un juego, lo busca en la tabla Biblioteca
# y actualiza su rating. Si el juego no existe, imprime un mensaje.
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def update_game(name):
    cursor.execute("""SELECT * FROM BIBLIOTECA WHERE name = :name""",name=name)
    row = cursor.fetchone()
    if row is not None:
        while True:
            print("Nueva calificación del juego:")
            ra = int(input("1-5: "))
            if ra > 5 or ra < 1:
                print("No es una calificación valida \n")
            else:
                False
                break
        cursor.execute("""
                        UPDATE BIBLIOTECA SET rating = :rating
                        WHERE name = :name
                        """,
                        rating = ra,
                        name = name
                        )
        connection.commit()
        print("Juego actualizado :) \n")
    else:
        print("No existe ese juego en tu biblioteca")
    connection.commit()
    return



############################################################################################################################
# search_game(name,n)
#----------------------------------------------------------
# str name
# int n
#----------------------------------------------------------
# Función que recibe el nombre de un juego, y una variable n.
# Si n = 1, busca en la tabla JUEGOS.
# Si n = 2, busca en la tabla Biblioteca.
# Y finalmente imprime el todos los datos del juego.
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def search_game(name,n):
    #tienda
    if n == 1:
        cursor.execute('''
                        SELECT * FROM JUEGOS
                        WHERE name = :name
                        ''',name=name)
        row = cursor.fetchone()
        if row is not None:
            print("Ranking:",row[0])
            print("Nombre:",row[1])
            print("Plataforma:",row[2])
            print("Año:",row[3])
            print("Genero:",row[4])
            print("Compañía:",row[5])
            print("Ventas en USA (Millones):",row[6])
            print("Ventas en Europa (Millones)",row[7])
            print("Ventas en Japón (Millones)",row[8])
            print("Ventas en otros países (Millones)",row[9])
            print("Ventas globales (Millones)",row[10])
        else:
            print("No hay juegos de ese nombre")

    #biblioteca
    elif n == 2:
        cursor.execute('''
                        SELECT * FROM BIBLIOTECA
                        WHERE name = :name
                        ''',name=name)
        row = cursor.fetchone()
        if row is not None:
            print("Ranking:",row[0])
            print("Nombre:",row[2])
            print("Plataforma:",row[3])
            print("Año:",row[4])
            print("Genero:",row[5])
            print("Compañía:",row[6])
            print("Rating:",row[7])
        else:
            print("No hay juegos de ese nombre")
    else:
        print("Entrada incorrecta")
    return



############################################################################################################################
# search_game_platform(platform,n)
#----------------------------------------------------------
# str platform
# int n
#----------------------------------------------------------
# Función que recibe el nombre de la plataforma, y una variable n.
# Donde busca en la tabla JUEGOS, y imprime el n nombres de los juegos. 
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def search_game_platform(platform,n):

    cursor.execute('''
                    SELECT * FROM JUEGOS
                    WHERE PLATFORM = :platform
                    ORDER BY global_sale DESC
                    ''',platform=platform)
    count = 0
    a = 0
    while count < n:
        row = cursor.fetchone()
        if row is not None:
            print(".-",row[1])
            a = 1
        count += 1
    if a == 0:
        print("No hay juegos de ese genero")
    return



############################################################################################################################
# clean_biblioteca()
#----------------------------------------------------------
# sin parametros
#----------------------------------------------------------
# Función que limpia y reinicia la tabla Biblioteca. 
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def clean_biblioteca():
    cursor.execute("DELETE FROM BIBLIOTECA")
    create_biblioteca_table()
    return


############################################################################################################################
# menu()
#----------------------------------------------------------
# sin parametros
#----------------------------------------------------------
# Función que llama a las funciones de la interfaz.
# Según la opción seleccionada, se llama a la función correspondiente.
# Permite interactuar con el usuario.
#----------------------------------------------------------
# retorno vació.
############################################################################################################################
def menu():
    print("\n ¡¡ Bienvenido a USM Games !!\n")
    print("Cargando CSV... \n")
    insert_juegos_data()

    flag = True

    while flag:
        print("1.- Mostrar mi Biblioteca")
        print("2.- Comprar juego (según nombre)")
        print("3.- Ranking Top 5 Ventas Totales")
        print("4.- Ranking Top 5 Ventas por Género")
        print("5.- Eliminar juego de Biblioteca")
        print("6.- Actualizar calificación de juego")
        print("7.- Buscar juego por nombre (Tienda o Biblioteca)")
        print("8.- Buscar juego por plataforma en Tienda")
        print("9.- Limpiar Biblioteca")
        print("10.- Salir")

        opcion = int(input("\nIngrese una opción: "))

        match opcion:
            case 1:
                
                print("\nMi Biblioteca: \n")
                show_biblioteca()
                print("\n")
                print("\nBasurero")
                show_basurero()
                print("\n")
                opcion = str(input("\nPresione Enter para volver al menú: "))                
                print("\n")
        
            case 2:

                print("\nComprar juego: \n")
                name = input("Ingrese el nombre del juego: ")
                print("\n")
                buy_game(name)
                opcion = str(input("\nPresione Enter para volver al menú: "))
                print("\n")
        
            case 3:

                print("\nRanking Top 5 Ventas Totales: \n")
                ranking_games_total()
                opcion = str(input("\nPresione Enter para volver al menú: "))
                print("\n")

            case 4:

                print("\nRanking Top 5 Ventas por Género: \n")
                genero = input("Ingrese el género del juego: ")
                print("\n")
                ranking_games_genre(genero)
                opcion = str(input("\nPresione Enter para volver al menú: "))
                print("\n")

            case 5:

                print("\nEliminar juego de Biblioteca: \n")
                show_biblioteca()
                print("\n")
                name = input("Ingrese el nombre del juego: ")
                print("\n")
                delete_game(name)
                opcion = str(input("\nPresione Enter para volver al menú: "))
                print("\n")

            case 6:

                print("\nActualizar calificación de juego: \n")
                show_biblioteca()
                print("\n")
                name = input("Ingrese el nombre del juego: ")
                print("\n")
                update_game(name)
                opcion = str(input("\nPresione Enter para volver al menú: "))
                print("\n")

            case 7:

                print("\nBuscar juego por nombre (Tienda o Biblioteca):\n")
                print("1.- Tienda")
                print("2.- Biblioteca")
                opcion = int(input("\nIngrese una opción: "))
                print("\n")
                if opcion == 2:
                    show_biblioteca()
                    print("\n")
                name = str(input("Ingrese el nombre del juego: "))
                print("\n")
                search_game(name,opcion)
                opcion = str(input("\nPresione Enter para volver al menú: "))
                print("\n")

            case 8:
                
                print("\nBuscar juego por plataforma en Tienda: \n")
                plataforma = input("Ingrese la plataforma del juego: ")
                n = int(input("Ingrese la cantidad de juegos a mostrar: "))
                print("\n")
                search_game_platform(plataforma,n)
                opcion = str(input("\nPresione Enter para volver al menú: "))
                print("\n")

            case 9:

                print("\nLimpiar Biblioteca: \n")
                show_biblioteca()
                print("\n")
                print("Se borrará toda su Biblioteca, ¿Desea continuar? \n")
                print(" 1.- Si")
                print(" 2.- No")
                opcion = int(input("\nIngrese una opción: "))
                if opcion == 1:
                    clean_biblioteca()
                    print("\nBiblioteca limpia :)")
                    opcion = str(input("\nPresione Enter para volver al menú: "))
                    print("\n")
                
            case 10:

                print("\nSalir")
                clean_biblioteca()
                flag = False

    return


menu()
cursor.close() 
connection.close()