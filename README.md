===========================
Brazo Robot con Arduino UNO
Controlado por DualSense
===========================

Autor: Diogo Aquino  
Carrera: Ingeniería en Informática - UCU  
Proyecto de Taller de Introducción a la Ingeniería

------------------------------------
DESCRIPCIÓN GENERAL DEL PROYECTO
------------------------------------

Este código controla un brazo robótico de 4 ejes utilizando un Arduino UNO.
Los movimientos del brazo se controlan mediante un joystick DualSense (PlayStation 5),
cuyas señales se leen desde un script en Python y se envían por puerto serie al Arduino.

--------------------
ARCHIVOS DEL PROYECTO
--------------------

1) brazo_robot.ino --> Código principal para Arduino. Controla los servomotores.
2) control_dualsense.py --> Script en Python que lee el DualSense y manda comandos al Arduino.
3) readme.txt --> Este archivo con las instrucciones.

----------------------
CÓMO FUNCIONA EL CÓDIGO
----------------------

En Arduino:

- Usa la librería Servo.h para controlar 4 servomotores (uno por eje del brazo).
- Espera recibir comandos por el puerto serie (USB).
- Cada comando representa una orden de movimiento para un servo específico.
  Por ejemplo:
     "X90" --> Mueve el servo X a 90 grados.
     "Y45" --> Mueve el servo Y a 45 grados.
- Los servos están conectados a los pines digitales (ej: 9, 10, 11, 12).

En Python:

- Usa pydualsense para leer el estado del joystick.
- Traduce movimientos del joystick izquierdo/derecho en valores de ángulo.
- Manda esos valores al Arduino por puerto COM usando pyserial.

-------------------------
CONEXIONES DEL HARDWARE
-------------------------

- Servo 1 (base): Pin 9
- Servo 2 (hombro): Pin 10
- Servo 3 (codo): Pin 11
- Servo 4 (muñeca o pinza): Pin 12
- GND y VCC de los servos conectados a fuente externa.
- GND común entre Arduino y fuente externa.

--------------------------
CÓMO USAR EL PROYECTO
--------------------------

1. Conectar el Arduino UNO a la PC por USB.
2. Cargar el código "brazo_robot.ino" con el Arduino IDE.
3. Ejecutar el script Python "control_dualsense.py".
4. Mover los joysticks para controlar el brazo.
   - Joystick izquierdo: mueve base y hombro.
   - Joystick derecho: mueve codo y muñeca.

---------------------
VERSIONES FUTURAS
---------------------

- Añadir más ejes y pinza funcional.
- Implementar control inalámbrico por Bluetooth.
- Incorporar sensores de feedback o cámara.
- Traducir el código a una interfaz con GUI.

¡Gracias por revisar este proyecto!
