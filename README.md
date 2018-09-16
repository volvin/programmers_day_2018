# programmers_day_2018

El problema es un rompecabezas desordenado de 20 x 20 piezas donde cada pieza tiene un color diferente en cada esquina de la figura. La solución final ordenada busca que cada pieza se alinie en colores con las cuatro piezas lindantes.
<br><br>
![Screenshot](/screenshots/challenge.png)
<br>Imágen original del problema

El algoritmo comienza buscando la primera pieza de arriba hacia abajo y de izquierda a derecha. Cuando encuentra una pieza que satisface la condición inicia otro hilo de ejecución desde ese punto de manera recursiva, esta vez para la segunda pieza. Mientras tanto, el hilo inicial sigue buscando piezas que satisfagan el primer lugar y si encuentra otra vuelve a repetir el mismo paso anterior: abre un hilo nuevo para esa pieza y sigue buscando. Este proceso de seguir buscando piezas para la misma posición se realiza porque hay muchas piezas que tienen la misma configuración de colores, pero solo algunas combinaciones llevan a un resultado final completo.
<br>A medida que avanza el programa se van descubriendo nuevas piezas y posibles combinaciones, cuando una combinación no encuentra la pieza siguiente el hilo se descarta y solo quedan activos los hilos de las combinaciones exitosas.
<br>Llegando al final cuando quedan pocas piezas el proceso se acelera y las combinaciones posibles se achican. El programa termina con dos resultados muy similares que en la combinación varían solo en las últimas piezas sin cambiar el resultado: un QR code que representa la frase: "#Developers!"
<br><br>
![Screenshot](/screenshots/resultThread-18.png)
<br>Primer resultado del algorítmo<br><br>
![Screenshot](/screenshots/resultThread-28.png)
<br>Segundo resultado del algorítmo

