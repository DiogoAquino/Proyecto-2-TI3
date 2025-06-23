#include <Servo.h>

Servo miServo;  // Crea un objeto tipo Servo

void setup() {
  miServo.attach(9);  // Conecta el servo al pin digital 9
}

void loop() {
  // Gira de 0° a 180°
  for (int angulo = 0; angulo <= 180; angulo++) {
    miServo.write(angulo);  // Mueve a la posición del ángulo
    delay(15);              // Espera 15 ms para que se mueva
  }

  // Vuelve de 180° a 0°
  for (int angulo = 180; angulo >= 0; angulo--) {
    miServo.write(angulo);
    delay(15);
  }
}
