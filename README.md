# Manual de Usuario Illya


Para este lenguaje de programacion se tienen los siguientes tipos de datos:
entero
flotante
char

La estructura del programa tiene que ser como la siguiente:

programa ID;
variables
declaracion_globales

declaracion de funciones

principal(){
Bloque de codigo
}

Donde la declaracion de variables es de la siguiente forma:
tipo_dato : ID;
tipo_dato : ID, ID;
*arreglo
tipo_dato : ID[entero];

La declaracion de funciones es de la siguiente forma:
funcion tipo ID(parametros)
variables{
Bloque de codigo
regresa(variable);
}
*Si la funcion es de tipo void no debe ir el estatuto de regresa

Una asignacion de variables es de la siguiente forma:
ID = valor;
ID[entero] = valor;

Se cuentan con los siguientes estatutos:
- SI (CONDICIONAL)
- MIENTRAS (CICLO CONDICIONAL)
- DESDE (CICLO NO CONDICIONAL)
- LLAMADA_FUNCION
- ASIGNACION
- ESCRITURA
- LECTURA
- LLAMADA_FUNCION_ESPECIAL

La asignacion de un valor a una variable es de la siguiente forma:
variable = valor;
variable[entero] = valor;

La sintaxis para escribir el valor de una variable o un letrero es la siguiente:
escribe("Hola Mundo");
*Escribir multples mensajes
escribe("hola", variableid, 1+2);

La sintaxis para leer el input del usuario y asignarlo a una variable es la siguiente:
lee(variableid);

La estructura de como se escribe un condicional es la siguiente:
si (expresion) entonces {
Bloque de codigo
} sino {
Bloque de codigo
}

*sino es opcional

La estructura de un ciclo no condicional es la siguiente:
mientras (expresion) hacer {
Bloque de codigo
}

La estructura de un ciclo condicional es la siguiente:
desde variableID = valor hasta expresion hacer {
Bloque de codigo
}

La llamada a una funcion es de la siguiente forma:
Llamada no void
variable = funcion(parametros);

llamada void
funcion(parametros);

La sintaxis de las llamadas especiales es igual que una funcion void, se cuentan con las siguientes funciones y se explican sus parametros:
- COLOR(semilla); #Recibe un valor o una expresion que tenga como resultado un valor entero o flotante que es utilizado para generar una semilla de numeros aleatorios para - generar un color
- CIRCULO(radio); #Recibe un valor o expresion que de como resultado un valor entero o flotante que es utilizado como radio para dibujar un circulo
- LINEA(tamano, direccion); #Recibe un valor o expresion que de como resultado un valor entero o flotante que es cuantos pixeles se va a desplazar la tortuga o cuantos grados va a girar y como segundo parametro la direccion hacia donde se va a mover la tortuga o girar: fd para moverla hacia adelante en la direccion que este viendo, bk para moverse hacia atras, rt para girar x grados hacia la derrecha, lt para girar x grados a la izquierda
- PENUP(); #Levanta la pluma, por lo tanto no se hacen dibujos aunque se llamen las funciones;
- PENDOWN(); #Baja la pluma para continuar dibujando, valor por defecto
- ARCO(radio_x, radio_y); #Recibe 2 expresiones o variables que den como resultado enteros o flotantes que son utilizados para dibujar un arco
- GROSOR(tamano); #Cambia el grosor de las lineas
- LIMPIAR(); #Borra todo lo que se haya dibujado
- ORDENA(ID); #Recibe como parametro el id de un arreglo para ordenarlo







