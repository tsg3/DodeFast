import time
import serial

def send(comandos):
    try:
        port = "COM12"
        bluetooth = serial.Serial(port, 9600)
        print("Conectado")
        bluetooth.flushInput()

        for i in comandos:
            j = 0
            while j < 3:
                bluetooth.write(str.encode(i[j*2:(j*2)+2]))
                respuesta = "y"
                while respuesta.strip()[-1] != '#':
                    respuesta += bluetooth.read().decode()
                time.sleep(0.5)
                print(respuesta, i)
                j += 1
        bluetooth.close()
        print("FINALIZADO")
    except serial.serialutil.SerialException:
        print('Error')
