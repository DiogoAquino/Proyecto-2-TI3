#include <Servo.h>

Servo servo1;
Servo servo2;

void setup() {
  // Inicializar comunicación serial
  Serial.begin(9600);

  // Conectar los servos a los pines digitales
  servo1.attach(9);   //servo en pin 9
  servo2.attach(10);  //servo en pin 10
}

void loop() {
  // Revisar si hay datos disponibles desde el puerto serie
  if (Serial.available()) {
    // Leer la línea completa hasta el salto de línea
    String input = Serial.readStringUntil('\n');

    // Buscar la coma que separa los dos valores
    int commaIndex = input.indexOf(',');

    // Si se encontró la coma, procesar los datos
    if (commaIndex > 0) {
      // Separar y convertir a enteros los dos valores
      int angle1 = input.substring(0, commaIndex).toInt();
      int angle2 = input.substring(commaIndex + 1).toInt();

      // Limitar los ángulos entre 0 y 180
      angle1 = constrain(angle1, 0, 180);
      angle2 = constrain(angle2, 0, 180);

      // Mover los servos
      servo1.write(angle1);
      servo2.write(angle2);
    }
  }
}
