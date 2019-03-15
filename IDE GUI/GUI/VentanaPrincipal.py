from tkinter import *
import logic.parserPrueba
import os.path
import threading
import time
import re


def obtener_codigo():
    if len(current_URL) != 0:
        texto = textCommand.get("1.0", END)
        archivoCodigo = open(current_URL, "w")
        archivoCodigo.write(texto)
        archivoCodigo.close()
    else:
        printTerminal("Before saving, upload or create a program!", True)


def separate_code(code):
    openbrace = 0
    pos = []
    repita = []
    mientras = []
    i = 0
    n = len(code)
    while i < n:
        digit = code.find('REPITA', i)
        if not (digit in repita) and digit != -1:
            repita.append(digit)
        digit = code.find('MIENTRAS', i)
        if not (digit in mientras) and digit != -1:
            mientras.append(digit)
        i += 1
    if len(repita) != len(mientras):
        return "Wrong balance between REPITA's and MIENTRAS's"
    i = 0
    n = len(repita)
    while i < n:
        if repita[i] > mientras[i]:
            return "Wrong distribution of REPITA's and MIENTRAS's"
        i += 1
    w = 0
    inside_while = False

    haga = []
    findesde = []
    y = 0
    u = len(code)
    while y < u:
        digit = code.find('HAGA', y)
        if not (digit in haga) and digit != -1:
            haga.append(digit)
        digit = code.find('FINDESDE', y)
        if not (digit in findesde) and digit != -1:
            findesde.append(digit)
        y += 1
    if len(haga) != len(findesde):
        return "Wrong balance between HAGA's and FINDESDE's"
    o = 0
    p = len(haga)
    while o < p:
        if haga[o] > findesde[o]:
            return "Wrong distribution of HAGA's and FINDESDE's"
        o += 1
    l = 0
    inside_do = False

    x = 0
    for i in code:
        if w < n:
            if x > repita[w]:
                inside_while = True
            if x > mientras[w]:
                inside_while = False
                w += 1
        if l < p:
            if x > haga[l]:
                inside_do = True
            if x > findesde[l]:
                inside_do = False
                l += 1
        if i == '{':
            openbrace += 1
        elif i == '}':
            openbrace -= 1
        elif i == ';' and openbrace == 0 and inside_while == False and inside_do == False:
            pos.append(x)
        x += 1
    lista = []
    n = len(pos)
    y = 0
    while y < n:
        if y == 0:
            lista.append(code[:pos[y]])
        else:
            lista.append(code[pos[y - 1] + 1:pos[y]])
        y += 1
    lista.append(code[pos[-1] + 1:])
    if openbrace == 0:
        return lista
    else:
        return "--> Bad distribution of brackets!"

def get_code(code):
    if code.count("INICIO") == 1 and code.count("FINAL") == 1:
        if code.index('INICIO:') < code.index('FINAL;'):
            count1 = code.index("INICIO")
            for i in range(count1):
                if code[i] != " " or code[i] != "\n":
                    print(code[i])
                    print(code[i+1])
                    return "error"
            count2 = code.index("FINAL;")
            tr = code[(count1+7):count2]
            return tr
        else:
            return "error"
    else:
        return "error"


def correr_codigo():
    if len(current_URL) != 0:
        logic.parserPrueba.line = 0
        archivoCodigo = open(current_URL, "r")
        prevCode = archivoCodigo.read()
        archivoCodigo.close()
        codigo = get_code(prevCode)
        if codigo == "error":
            printTerminal("Error INICIO-FINAL", True)
            return
        printTerminal("", True)
        codigo = codigo.strip().replace('\n', '').replace('\t', '')
        codigo = separate_code(codigo)
        if type(codigo) == str:
            printTerminal(codigo, False)
        else:
            for i in codigo:
                time.sleep(0.05)
                print(i)
                result = logic.parserPrueba.Parse_Code(i)
                if len(result[0]) > 0:
                    printTerminal(result[0], False)
                if result[1]:
                    break
            logic.parserPrueba.variables.clear()

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
        ventana_secundaria.destroy()
        add_code(url)
        fill_info()


def add_code(url):
    global current_URL
    try:
        file = open(url, "r")
        code = file.read()
        file.close()
        textCommand.config(state=NORMAL)
        textCommand.delete('1.0', END)
        textCommand.insert(END, code)
        current_URL = url
    except Exception:
        printTerminal("File doesn't exist!", True)


def printTerminal(code, delete):
    textTerminal.config(state=NORMAL)
    if delete:
        textTerminal.delete('1.0', END)
        textTerminal.insert(END, titleMessage + code + "\n")
    else:
        textTerminal.insert(END, code)
        textTerminal.insert(END, "\n")
        textTerminal.config(state=DISABLED)


def new_file():
    ventana_secundaria = Toplevel(root)
    ventana_secundaria.title("Nuevo archivo")
    ventana_secundaria.geometry("300x150")
    Label(ventana_secundaria, text="Ingrese un URL de la carpeta").place(x=20, y=10)
    url = Entry(ventana_secundaria, width=30)
    url.place(x=60, y=30)
    Label(ventana_secundaria, text="Ingrese el nombre del nuevo archivo").place(x=20, y=50)
    name = Entry(ventana_secundaria, width=30)
    name.place(x=60, y=70)
    btnA = Button(ventana_secundaria, text="Crear nuevo",
                  command=lambda: create_new_file(url, name, ventana_secundaria))
    btnA.pack(side=BOTTOM)


def create_new_file(url, name, ventana_sec):
    url = url.get()
    name = name.get()
    global current_URL
    if len(name) != 0 and len(url) != 0:
        if os.path.isdir(url):
            url += "\\" + name + ".txt"
            file = open(url, "w")
            file.close()
            textCommand.config(state=NORMAL)
            textCommand.delete('1.0', END)
            current_URL = url
            ventana_sec.destroy()
            fill_info()
        else:
            Label(ventana_sec, text="Ubicación inválida", fg="RED").place(x=20, y=90)
    else:
        Label(ventana_sec, text="Todos los espacios deben llenarse", fg="RED").place(x=20, y=110)


def fill_info():
    global currentURL
    global file_name
    cont = 1
    lista = current_URL.split("\\")
    file_name.set(lista[len(lista) - 1])
    lista = lista[0:(len(lista) - 1)]
    url = ""
    textInfo.config(state=NORMAL)
    textInfo.delete('1.0', END)
    textInfo.insert(END, "Current folder: \n-> ")

    for i in lista:
        url += i + "\\"
    textInfo.insert(END, url + "\n\n")
    lista = []
    textInfo.insert(END, "Files on folder:\n\n")
    for base, dirs, files in os.walk(url):
        lista += files
        lista += dirs
    for file in lista:
        textInfo.insert(END, str(cont) + ") " + str(file) + "\n")
        cont += 1
    textInfo.config(state=DISABLED)


def run_thread():
    thread = threading.Thread(target=correr_codigo)
    thread.start()


def stop():
    logic.parserPrueba.flag_stop = True


# Ventana principal

root = Tk()

# - Variables globales
current_URL = ""
file_name = StringVar()
file_name.set("")

# - Principal

root.geometry("1280x640+5+5")
root.title("DodeFast")
root.resizable(0, 0)
root.config(bg="GRAY")
Label(root, text="DODEFAST IDE", font=("Times", 20), fg="white", bg="GRAY").place(x=26, y=10)
Label(root, textvariable=file_name, fg="white", bg="GRAY").place(x=1280 - 950, y=10)

# ______________ Agregados en la ventana ___________________
# - Ventana de comandos (para escribir el código)

textCommand = Text(root, height=25, width=115, bg="white", bd=2, state=DISABLED)
textCommand.place(x=1280 - 950, y=30)
scrollText = Scrollbar(root, command=textCommand.yview)
textCommand.config(yscrollcommand=scrollText.set)
scrollText.place(in_=textCommand, relx=1, relheight=1, bordermode="outside")

# - Ventana de información

textInfo = Text(root, height=20, width=35, bg="white", bd=2, state=DISABLED)
textInfo.place(x=10, y=90)
scrollInfo = Scrollbar(root, command=textInfo.yview)
textInfo.config(yscrollcommand=scrollInfo.set)
scrollInfo.place(in_=textInfo, relx=1, relheight=1, bordermode="outside")

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
botonCorrer = Button(root, text="Correr", command=lambda: run_thread())
botonNuevo = Button(root, text="Nuevo", command=lambda: new_file())
botonAbrir = Button(root, text="Abrir", command=lambda: open_file())
botonDetener = Button(root, text="Detener", command=lambda: stop())

botonDetener.place(x=200, y=422)
botonGuardar.place(x=270, y=50)
botonCorrer.place(x=270, y=422)
botonAbrir.place(x=26, y=50)
botonNuevo.place(x=80, y=50)

mainloop()
