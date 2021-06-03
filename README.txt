==============================================================
SIMULADOR A MIDA, by Carlos Sansón, Dídac Clària & Marcel Urpí
==============================================================



CÓMO EJECUTAR LA SIMULACIÓN:
    > python3 main.py [PARAMETROS]



OPCIONES DE EJECUCIÓN DISPONIBLES:

    - Tiempo de ejecución (NECESARIO): Define cuánto tiempo en segundos va a durar la simulación.
        Uso: "-t INT" / "--time INT"

    - Número de simulaciones: Define cuántas ejecuciones simultáneas se harán de la simulación. Las
    estadísticas resultantes mostrarán la media de todos los resultados.
        Uso: "-n INT" / "--simulations INT"

    - Seed: Define la seed de la simulación, la cuál determina la aleatoriedad de la ejecución. Dos
    ejecuciones con la misma seed tendrán el mismo resultado. Si no defines este parámetro, por defecto
    ejecutará una sola simulación.
        Uso: "-s INT" / "--seed INT"
    
    - Mostrar gráficas de las estadísticas: Si se escribe esta opción, al finalizar la simulación se
    mostrará una ventana con una gráfica de estadísticas de la simulación.
        Uso: "-g" / "--g"

    - Mostrar valores de cada ejecución individual: Si se han establecido varias ejecuciones simultáneas,
    al activar esta opción se mostrarán junto a las estadísticas los valores individuales de cada una de
    las simulaciones.
        Uso: "-v" / "--values"
    
    - Mostrar comportamiento completo de la simulación: Al activar esta opción, se imprimirá un log de todas
    las acciones que realiza cada entidad del sistema. Esta opción puede ser útil para entender el comportamiento
    de la simulación o para buscar algún problema que haya ocurrido, pero ralentiza la ejecución.
        Uso: "-d" / "--debug"

    - Mostrar lista de parámetros: Si se activa esta opción, sólo se mostrarán la lista de parámetros disponibles.
        Uso: "-h" / "--help"


EJEMPLO DE USO:
    > python3 main.py --time 57600 -n 20 --values



DEPENDENCIAS EXTERNAS:
    Para la ejecución del programa se necesita instalar estas librerías de python:
     - argparse
     - numpy
     - matplotlib
    
    Para instalar cualquier librería, ejecutar:
        > python3 -m pip install [LIBRERIA]



OTROS PARÁMETROS DE LA SIMULACIÓN:
    El resto de parámetros de la simulación están definidos en el archivo 'SimulationParameters.py'. Para modificar cualquiera
    de estos parámetros, simplemente basta con abrir el archivo con cualquier editor de texto, modificar los valores que
    aparecen y guardar los cambios. Entonces, la próxima vez que se ejecute el programa la simulación utilizará los nuevos
    parámetros modificados.



PROBLEMAS DE EJECUCIÓN DESDE WSL:
    Si se utiliza WSL para ejecutar la simulación, lo más probable es que la opción de mostrar gráficos no funcione, ya que por
    defecto, si no se ha instalado un programa externo con esta intención, WSL no tiene asignado ningún Display donde abrir
    las ventanas que contienen los gráficos.
    La mejor forma de ejecutar el programa en Windows es desde la consola PowerShell con la última versión de python 3 instalada.