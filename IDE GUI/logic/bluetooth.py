import time
import serial

print("INICIA")
port = "COM6"
bluetooth = serial.Serial(port, 9600)
print("Conectado")
bluetooth.flushInput()
imput = ""
respuesta = "y"

while True:
    imput = input("ENVIO: ")
    if imput == 'f':
        break
    bluetooth.write(str.encode(imput))
    while respuesta.strip()[-1] != '#':
        respuesta += bluetooth.read().decode()
    print(respuesta)
    respuesta = "y"
    time.sleep(0.1)

bluetooth.close()
print("FINALIZADO")
