from tkinter import *
import logic.parserPrueba
import os.path
import threading

#symbols = [' ','(',')','{','}',':',';','','\n','\t',]

def obtener_codigo():
    if len(current_URL) != 0:
        texto = textCommand.get("1.0", END)
        archivoCodigo = open(current_URL, "w")
        archivoCodigo.write(texto)
        archivoCodigo.close()
    else:
        printTerminal("Before saving, upload or create a program!", True)


def correr_codigo():
    global debugger
    if len(current_URL) != 0:
        textCommand.tag_remove('line_error', '1.0', END)
        logic.parserPrueba.flag_stop = False
        logic.parserPrueba.line = 0
        archivoCodigo = open(current_URL, "r")
        # prevCode = archivoCodigo.read().strip().replace('\n', '♥♦').replace('\t', '')
        prevCode = archivoCodigo.read().replace('\t', ' ')
        archivoCodigo.close()
        printTerminal("", True)

        if debugger:
            logic.parserPrueba.flag_runnig = True
            threading.Thread(target=printingLoop).start()

        logic.parserPrueba.runParser(prevCode)
        if not debugger:
            printTerminal(logic.parserPrueba.st, False)
        logic.parserPrueba.st = ""
    else:
        printTerminal("Before running, load a program!", True)


def printingLoop():
    actualstr = ""
    while logic.parserPrueba.flag_runnig:
        if logic.parserPrueba.st != "" and logic.parserPrueba.st != actualstr:
            printTerminal(logic.parserPrueba.st.strip(), False)
            actualstr = logic.parserPrueba.st


def open_file():
    ventana_secundaria = Toplevel(root)
    ventana_secundaria.transient(root)
    ventana_secundaria.title("Abrir documento existente")
    ventana_secundaria.geometry("300x100")
    ventana_secundaria.resizable(width=False, height=False)
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
        textCommand.delete(textCommand.index("end"))

        color_words()

        current_URL = url
    except Exception:
        printTerminal("File doesn't exist!", True)

def color_words():
    global symbols
    count = 1
    for i in logic.parserPrueba.color_words:
        start_pos = '1.0'
        while True:
            start_pos = textCommand.search(i, start_pos, END)
            if start_pos:
                end_pos = textCommand.index('{}+{}c'.format(start_pos, (len(i))))
                #if (textCommand.get(start_pos+'-1c') in symbols and textCommand.get(end_pos) in symbols) or start_pos == '1.0':
                if count < 8:
                    textCommand.tag_add("reser1", start_pos, end_pos)
                elif count < 14:
                    textCommand.tag_add("reser2", start_pos, end_pos)
                elif count < 20:
                    textCommand.tag_add("reser3", start_pos, end_pos)
                elif count < 22:
                    textCommand.tag_add("reser4", start_pos, end_pos)
                else:
                    textCommand.tag_add("reser5", start_pos, end_pos)
                start_pos = end_pos
            else:
                break
        count += 1

def enter(event):
    textCommand.tag_remove('reser1', '1.0', END)
    textCommand.tag_remove('reser2', '1.0', END)
    textCommand.tag_remove('reser3', '1.0', END)
    textCommand.tag_remove('reser4', '1.0', END)
    textCommand.tag_remove('reser5', '1.0', END)
    textCommand.tag_remove('line_error', '1.0', END)
    color_words()

'''def black(event):
    try:
        sel = "%s-%s" % (textCommand.index("insert wordstart"), textCommand.index("insert wordend"))
    except Exception:
        sel = "<none>"
    if sel != "<none>":
        sel_list = sel.split('-')
        textCommand.tag_remove('reser1', sel_list[0], sel_list[1])
        textCommand.tag_remove('reser2', sel_list[0], sel_list[1])
        textCommand.tag_add("black", sel_list[0], sel_list[1])'''

def printTerminal(code, delete):
    textTerminal.config(state=NORMAL)
    error_line = code.find("en la linea")
    if error_line != -1:
        count = error_line + 12
        len_line = ''
        while code[count].isdigit():
            len_line += code[count]
            count += 1
        textCommand.tag_add("line_error",len_line+'.0',len_line+'.end')
    if delete:
        textTerminal.delete('1.0', END)
        textTerminal.insert(END, titleMessage + code.replace("☺", "").replace("☻", "") + "\n")
    else:
        textTerminal.insert(END, code.replace("☺", "").replace("☻", ""))
        textTerminal.insert(END, "\n")
        textTerminal.config(state=DISABLED)
    if code != "":
        if code[-1] == "☻":
            textTerminal.tag_add("code", str(int(textTerminal.index("end").split(".")[0]) - 4) + ".0",
                                 textTerminal.index("end"))
            textTerminal.tag_config("code", foreground="RED")
        elif "☺" in code:
            textTerminal.tag_add("code", str(int(textTerminal.index("end").split(".")[0]) - 2) + ".0",
                                 textTerminal.index("end"))
            textTerminal.tag_config("code", foreground="GREEN")


def new_file():
    ventana_secundaria = Toplevel(root)
    ventana_secundaria.title("Nuevo archivo")
    ventana_secundaria.geometry("300x150")
    ventana_secundaria.resizable(width=False, height=False)
    ventana_secundaria.transient(root)
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


def debug():
    global debugger
    global label_debug
    if debugger:
        debugger = False
        botonDebug.config(text="Debugger: OFF", bg="YELLOW")
    else:
        debugger = True
        botonDebug.config(text="Debugger: ON", bg="GREEN")


# Ventana principal

root = Tk()

# - Variables globales
current_URL = ""
file_name = StringVar()
file_name.set("")
debugger = False

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
botonCorrer = Button(root, text="Correr", bg="#66FF00", command=lambda: run_thread())
botonNuevo = Button(root, text="Nuevo", command=lambda: new_file())
botonAbrir = Button(root, text="Abrir", command=lambda: open_file())
botonDetener = Button(root, text="Detener", bg="RED", command=lambda: stop())
botonDebug = Button(root, text="Debugger: OFF", bg="YELLOW", command=lambda: debug())

botonDebug.place(x=50, y=422)
botonDetener.place(x=200, y=422)
botonGuardar.place(x=270, y=50)
botonCorrer.place(x=270, y=422)
botonAbrir.place(x=26, y=50)
botonNuevo.place(x=80, y=50)

root.bind("<Key>", enter)
root.bind("<BackSpace>", enter)
root.bind("<space>", enter)
root.bind("<Return>", enter)

textCommand.tag_config("reser1", foreground="#003a63", font='Courier 9 bold')
textCommand.tag_config("reser2", foreground="#1a8c5c", font='Courier 9')
textCommand.tag_config("reser3", foreground="#e08dc4", font='Courier 9 bold')
textCommand.tag_config("reser4", foreground="#990652", font='Courier 9 bold')
textCommand.tag_config("reser5", foreground="#ef962f", font='Courier 9 bold')
textCommand.tag_config("line_error", background="#f74b45")

mainloop()
