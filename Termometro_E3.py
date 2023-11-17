import tkinter
import serial
import time
import threading

# Comunicación serial con Arduino por el COM1 Vel baudios
arduino = serial.Serial('COM1', 9600)

time.sleep(2)

# Función para el control de LED Encender - Apagar
def encender_led():
    arduino.write(b'1')
    led_status.config(text="ON")
    led_canvas.itemconfig(led_slider, fill="yellow")

def apagar_led():
    arduino.write(b'0')
    led_status.config(text="OFF")
    led_canvas.itemconfig(led_slider, fill="black")

# Recibir y mostrar datos de la temperatura desde Arduino
def receive_temperature():
    while True:
        temperature_data = arduino.readline().decode('utf-8').strip()
        try:
            temperature = float(temperature_data)
            update_gauge(temperature)
        except ValueError:
            pass

# Actualizar el widget por medio de un valor de temperatura
def update_gauge(temperature):
    temperature_gauge.configure(from_=0, to=100, length=200, tickinterval=10, label="Temperatura (°C)")

    if temperature > 80:
        temperature_gauge.config(bg="red", fg="white")
    else:
        temperature_gauge.config(bg="light green", fg="black")

    temperature_gauge.set(temperature)

# Crear y configurar la ventana principal
root = tkinter.Tk()
root.title("TERMOMETRO EQUIPO_3")
root.geometry("320x220")

# Crear y configurar el widget gauge
temperature_gauge = tkinter.Scale(root, orient='horizontal')
temperature_gauge.pack()

# Crear y configurar el widget LED
led_canvas = tkinter.Canvas(root, width=50, height=30)
led_slider = led_canvas.create_oval(15, 15, 30, 30, fill="black")
led_canvas.pack()

# Etiqueta para mostrar el estado del LED
led_status = tkinter.Label(root, text="OFF", font=("Helvetica", 10))
led_status.pack()

# Crear y configurar los botones para el control de los LEDs
led_button_on = tkinter.Button(root, text="Encender LED", command=encender_led)
led_button_on.pack()

led_button_off = tkinter.Button(root, text="Apagar LED", command=apagar_led)
led_button_off.pack()

# Crear un hilo para ejecutar la función en paralelo con el resto del programa
receive_temperature_thread = threading.Thread(target=receive_temperature)
receive_temperature_thread.start()

root.mainloop()
