import time
import serial

print("INICIA")
port = "/dev/tty.HC-06-DevB"
bluetooth = serial.Serial(port, 9600)
print("Conectado")
bluetooth.flushInput()
cola = [""]
for i in range(len(cola)):
    print("Enviando" + str(cola[i]))
    bluetooth.write(b"BOOP " + str.encode(cola[i]))
    respuesta = bluetooth.readline()
    print(respuesta.decode())
    time.sleep(0.1)
bluetooth.close()
print("FINALIZADO")
