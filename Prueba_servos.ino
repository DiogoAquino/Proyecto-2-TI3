#include <Servo.h>

Servo servo1;  
Servo servo2; 
Servo servo3;  

void setup() {
  servo1.attach(9);    // servo1 al pin digital 9
  servo2.attach(10);   // servo2 al pin digital 10
  servo3.attach(11);   // servo3 al pin digital 11
}

void loop() {
  // Mueve los servos de 0° a 180°
  for (int pos = 0; pos <= 180; pos += 1) {
    servo1.write(pos);
    servo2.write(180 - pos);  // movimiento inverso en el segundo servo
    servo3.write(pos);        // mismo movimiento que servo1
    delay(15);
  }

  // Mueve los servos de 180° a 0°
  for (int pos = 180; pos >= 0; pos -= 1) {
    servo1.write(pos);
    servo2.write(180 - pos);  // movimiento inverso
    servo3.write(pos);        // mismo movimiento que servo1
    delay(15);
  }
}
