# Compis2021

Gramática del proyecto implementada en el parser todavia falta probarla mas a detalle para verificar que no haya errores. 
Implementacion de las estructuras que seran:
- Tabla de variables.  
- Directorio de funciones.
- El cubo semantico.

Avance 01-05-21
Implementacion de las pilas junto con sus metodos, variables, banderas y metodos para la generacion de cuadruplos (todavia no utilizadas por el parser), ajuste de diagramas para puntos neuralgicos (no implementados todavia) ,ajustes a la gramatica y correcion de errores.

Avance 09-05-21
Correcion de la gramatica de acuerdo a los diagramas en lucidchart, punto neuralgicos para insertar variables dentro de la tabla de variables ya sea en contexto global o funcion, corregir que despues de regresar en la funcion marca como error de sintaxis

Avance 10-05-21
Cambio de sintaxis de declaracion de variables a tipo: lista_ids;, creacion de bloques de memoria, funciones para error out of bounds, nextAvail, etc.

Avance 12-05-21
generacion de cuadruplos para estatutos secuenciales, correcion cubo semantico en el nombre de tipos

Avance 15-05-21
implementacion de generacion de cuadruplos para estatutos condicionales

Avance 17-05-21
Prueba de generacion de cuadruplos con expresiones, lectura, escritura y constantes.

Avance 18-05-21
Prueba de generaciond de cuadruplos con ciclos y condiciones implementacion de algunos puntos neuralgicos para arreglos aun no utilizados por el parser para generacion de cuadruplos

Avance 19-05-21
pruebas sencillas con condicionales, ciclos y funciones. TODO funciona funcion void, pero marca error de sintaxis con los demas tipos de datos checar gramatica, en maquina virtual jala la ejecucion de las pruebas sencillas. falta implementar arreglos xd
* si se cambia de lugar la palabra reservada de lugar en la gramatica a funcion tipo id dec funciona por alguna razon
