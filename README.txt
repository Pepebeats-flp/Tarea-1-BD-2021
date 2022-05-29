
Tarea 1 Bases de Datos
José Pinto
Rut: 20922898-K
Rol: 202073559-K

Aclaraciones:

    * En la Tarea se utilizó Python 3.10.4 
    para poder implementar match.

    * Se utilizó Oracle 18c XE Server.

    * El mismo tarea.py pide los datos de conexión a la base de datos.

    * Al momento de mostrar la biblioteca, también se imprime un apartado
    llamado basurero que muestra los juegos que fueron borrados de la biblioteca
    y que se registran mediante el trigger.

    * Cada vez que se corra el programa, se crean las tablas
    nuevamente y se reinician los datos. Esto lo hice ya que
    cada vez que se corría el código, se creaban problemas
    ya que las tablas se llamaban igual y tenía que cambiar en todo
    momento los nombres de las nuevas tablas. Esto lo aclaro, por que
    es obvio que la idea de un programa así, es que los datos queden
    guardados y puedan ser utilizados luego de que el programa se cierre.

    * En el enunciado no se especifica que atributos deben
    imprimir en el menu, por lo que ocupé el nombre del juego,
    en algunos casos acompañado de las ventas globales y 
    en otro caso con la consola y el ranking local.

    * En el enunciado tampoco se especifica que hacer al momento de comprar
    un juego que esté en muchas plataformas, por lo que yo tomé el primer juego
    que encuentre con ese nombre.