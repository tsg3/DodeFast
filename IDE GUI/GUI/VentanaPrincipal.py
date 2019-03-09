from tkinter import *
from logic.parserPrueba import *


def obtener_codigo():
    if len(current_URL) != 0:
        texto = textCommand.get("1.0", END)
        archivoCodigo = open(current_URL, "w")
        archivoCodigo.write(texto)
        archivoCodigo.close()
    else:
        printTerminal("Before saving, upload or create a program!", True)

# codeurl = C:\Users\este0\Desktop\TEC\2019 - I Semestre\Compiladores, Intérpretes y Lenguajes\DodeFast\codigosPrueba\codigo.txt

def correr_codigo():
    if len(current_URL) != 0:
        archivoCodigo = open(current_URL, "r")
        codigo = archivoCodigo.read()
        archivoCodigo.close()
        codigo = codigo.strip().replace('\n','')
        codigo = codigo.split(';')
        printTerminal("", True)
        for i in codigo:
            printTerminal(Parse_Code(i), False)
        global variables
        variables.clear()

    else:
        printTerminal("Before running, load a program!", True)


def open_file():
    ventana_secundaria = Toplevel(root)
    ventana_secundaria.title("Abrir documento existente")
    ventana_secundaria.geometry("300x100")
    Label(ventana_secundaria, text="Ingrese un URL con la ubicación del documento").place(x=20, y=10)
    url = Entry(ventana_secundaria, width=30)
    # url.insert("0","C:\Users\jorte\Documents\Compiladores e Intérpretes\DodeFast\codigosPrueba\codigo.txt")
    url.place(x=60, y=30)
    btnA = Button(ventana_secundaria, text="Abrir", command=lambda: get_url(url, ventana_secundaria))
    btnA.pack(side=BOTTOM)


def get_url(entry, ventana_secundaria):
    url = entry.get()
    url = url.strip()
    if len(url) != 0:
        global current_URL
        current_URL = url
        ventana_secundaria.destroy()
        add_code(url)


def add_code(url):
    try:
        file = open(url, "r")
        code = file.read()
        file.close()
        textCommand.config(state=NORMAL)
        textCommand.delete('1.0', END)
        textCommand.insert(END, code)
    except Exception:
        printTerminal("File doesn't exist!")


def printTerminal(code, delete):
    textTerminal.config(state=NORMAL)
    if delete:
        textTerminal.delete('1.0', END)
        textTerminal.insert(END, titleMessage + code + "\n")
    else:
        textTerminal.insert(END, code)
        textTerminal.insert(END, "\n")
        textTerminal.config(state=DISABLED)


# Ventana principal
root = Tk()
root.geometry("1280x640+5+5")
root.title("DodeFast")
root.resizable(0, 0)
root.config(bg="GRAY")

# ______________ Agregados en la ventana ___________________
# - Ventana de comandos (para escribir el código)

textCommand = Text(root, height=27, width=115, bg="white", bd=2, state=DISABLED)
textCommand.place(x=1280 - 950, y=10)
scrollText = Scrollbar(root, command=textCommand.yview)
textCommand.config(yscrollcommand=scrollText.set)
scrollText.place(in_=textCommand, relx=1, relheight=1, bordermode="outside")
scrollText.config()

# - Terminal
titleMessage = ">> DodeFast IDE\n\n"
textTerminal = Text(root, height=10, width=155, bg="white", bd=2)
textTerminal.insert(END, titleMessage)
textTerminal.config(state=DISABLED)
textTerminal.place(x=10, y=452)
scrollTerminal = Scrollbar(root, command=textTerminal.yview)
textTerminal.config(yscrollcommand=scrollTerminal.set)
scrollTerminal.place(in_=textTerminal, relx=1, relheight=1, bordermode="outside")

# - Botones

botonGuardar = Button(root, text="Guardar", command=lambda: obtener_codigo())
botonCorrer = Button(root, text="Correr", command=lambda: correr_codigo())
botonNuevo = Button(root, text="Nuevo")
botonAbrir = Button(root, text="Abrir", command=lambda: open_file())

botonGuardar.place(x=1280 - 1010, y=20)
botonCorrer.place(x=1280 - 1010, y=422)
botonAbrir.place(x=26, y=10)
botonNuevo.place(x=20, y=50)

# - Variables globales
# t = "C:\Users\jorte\Documents\Compiladores e Intérpretes\DodeFast\codigosPrueba\codigo.txt"
current_URL = ""

mainloop()
