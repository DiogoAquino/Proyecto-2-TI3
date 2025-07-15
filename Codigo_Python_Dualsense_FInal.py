import time
import serial
from pydualsense import pydualsense
import serial.serialutil

# --- Funciones de Utilidad ---
def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# --- Configuración de la comunicación serial ---
SERIAL_PORT = 'COM8' # ¡AJUSTA ESTO AL PUERTO COM DE TU ARDUINO!
BAUD_RATE = 115200

# --- Rangos y Pasos de Movimiento ---
# SERVO_MIN y SERVO_MAX se mantienen como referencia para el rango general de servos,
# pero ya no se usan para limitar activamente las posiciones.
SERVO_MIN = 0
SERVO_MAX = 180
SERVO_BUTTON_INCREMENT = 3

JOYSTICK_DEADZONE_THRESHOLD = 15

# --- Variables de Posición Actual ---
# Posiciones iniciales centradas en el rango 0-180.
pos_garra = 90       # Garra (Pin 6) - Controlada por L1/R1
pos_servo2 = 90      # Servo 2 (Pin 8) - Controlado por Triángulo/Cuadrado
pos_servo_mg995 = 90 # Servo MG995 (Pin 9) - Controlado por Círculo/X

# --- Conexión Serial con Arduino ---
ser = None
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2)
    print(f"Conexión serial establecida en {SERIAL_PORT} a {BAUD_RATE} baudios.")
except serial.SerialException as e:
    print(f"ERROR: No se pudo abrir el puerto serial {SERIAL_PORT}: {e}")
    print("Asegúrate de que Arduino esté conectado y el puerto sea correcto (COM8). Cierra el Monitor Serial del IDE de Arduino si está abierto.")
    exit()

# --- Inicialización del DualSense ---
ds = None
try:
    ds = pydualsense()
    ds.init()
    print("Mando de PS5 conectado y listo.")
    ds.light.setColorI(0, 0, 255)
except Exception as e:
    print(f"ERROR: No se pudo inicializar el mando de PS5: {e}")
    print("Asegúrate de que el mando esté encendido y conectado (USB o Bluetooth).")
    if ser:
        ser.close()
    exit()

print("\n--- Control del Brazo Robótico ---")
print("Garra: L1 (abre), R1 (cierra) [Rango completo]") # Mensaje actualizado
print("Base (Stepper): Joystick Derecho (R3) horizontal")
print("Servo 2: Triángulo (arriba), Cuadrado (abajo)")
print("Servo MG995: Círculo (una dirección), X (otra dirección)")
print("Presiona Ctrl+C para salir.")

# --- Bucle Principal de Control ---
try:
    while True:
        # --- Lectura de Entradas del DualSense ---
        
        # Garra (L1/R1)
        l1_pressed = ds.state.L1
        r1_pressed = ds.state.R1

        # Stepper (Joystick Derecho X-axis)
        rx_val = ds.state.RX

        # Servo 2 (Triángulo/Cuadrado)
        triangle_pressed = ds.state.triangle
        square_pressed = ds.state.square

        # Servo MG995 (Círculo/X)
        circle_pressed = ds.state.circle 
        cross_pressed = ds.state.cross   
        
        # --- Lógica de Control y Actualización de Posiciones ---
        
        # Control de la Garra (L1/R1)
        if l1_pressed: 
            pos_garra += SERVO_BUTTON_INCREMENT
        elif r1_pressed:
            pos_garra -= SERVO_BUTTON_INCREMENT
        # ¡Ya no hay limitación! La posición puede ir de 0 a 180
        
        # Control del Stepper (Joystick Derecho Horizontal)
        stepper_steps = 0
        if abs(rx_val) > JOYSTICK_DEADZONE_THRESHOLD:
            stepper_steps = int(map_range(rx_val, -128, 127, -50, 50))
        
        # Control del Servo 2 (Triángulo/Cuadrado)
        if triangle_pressed:
            pos_servo2 += SERVO_BUTTON_INCREMENT
        elif square_pressed:
            pos_servo2 -= SERVO_BUTTON_INCREMENT
        # ¡Ya no hay limitación!
        
        # Control del Servo MG995 (Círculo/X)
        if circle_pressed: 
            pos_servo_mg995 += SERVO_BUTTON_INCREMENT
        elif cross_pressed: 
            pos_servo_mg995 -= SERVO_BUTTON_INCREMENT
        # ¡Ya no hay limitación!

        # --- Asegurarse de que los valores no se salgan del rango de int ---
        # Si bien no hay límites en el movimiento físico, los servos solo aceptan 0-180.
        # Es una buena práctica asegurar que las variables no crezcan indefinidamente.
        pos_garra = max(0, min(180, pos_garra))
        pos_servo2 = max(0, min(180, pos_servo2))
        pos_servo_mg995 = max(0, min(180, pos_servo_mg995))


        # --- Construcción y Envío del Mensaje al Arduino ---
        data_to_send = ""
        data_to_send += f"G:{pos_garra}\n"
        data_to_send += f"S2:{pos_servo2}\n"
        data_to_send += f"M9:{pos_servo_mg995}\n"
        
        if stepper_steps != 0:
            data_to_send += f"SP:{stepper_steps}\n"
        
        # Genera el output para la consola
        print_output = f"Garra: {pos_garra} | S2: {pos_servo2} | MG995: {pos_servo_mg995}"
        if stepper_steps != 0:
            print_output += f" | Stepper: {stepper_steps}"
        print_output += f" | Enviando: {data_to_send.strip().replace('\n', ' | ')}"
        
        # --- Manejo de errores de comunicación serial ---
        try:
            ser.write(data_to_send.encode())
            # print("output " + print_output)
        except serial.serialutil.SerialException as e:
            print(f"¡ADVERTENCIA! Error al escribir al Arduino: {e}.")
            print("Intentando reconectar al puerto serial...")
            try:
                if ser.is_open:
                    ser.close()
                ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
                time.sleep(2)
                print("Puerto serial reconectado exitosamente.")
            except serial.SerialException as re_e:
                print(f"FALLO al reconectar al puerto serial: {re_e}. Asegúrate de que el Arduino esté conectado y funcional.")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nDeteniendo el control y cerrando conexiones.")
finally:
    if ds:
        ds.light.setColorI(0, 0, 0)
        ds.close()
    if ser:
        ser.close()
    print("Programa finalizado.")
