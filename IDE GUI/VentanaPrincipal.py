from tkinter import *


def obtenerCodigo():
    texto = textCommand.get("1.0", END)

    print(texto)


# Ventana principal
root = Tk()
root.geometry("1280x640+5+5")
root.title("DodeFast")
root.resizable(0, 0)
root.config(bg="GRAY")

# ______________ Agregados en la ventana ___________________
# - Widget Entry (para escribir el código)
textCommand = Text(root, height=25, width=115, bg="white", bd=3)
textCommand.place(x=1280 - 950, y=10)
scrollText = Scrollbar(root, command=textCommand.yview)
textCommand.config(yscrollcommand=scrollText.set)
scrollText.place(in_=textCommand, relx=1, relheight=1, bordermode="outside")
scrollText.config()

# - Terminal
textTerminal = Text(root, height=10, width=155, bg="white", bd=3, state=DISABLED)
textTerminal.place(x=10, y=450)
scrollTerminal = Scrollbar(root, command=textTerminal.yview)
textTerminal.config(yscrollcommand=scrollTerminal.set)
scrollTerminal.place(in_=textTerminal, relx=1, relheight=1, bordermode="outside")

# - Botones

botonGuardar = Button(root, text="Guardar", command=lambda: obtenerCodigo())
botonCorrer = Button(root, text="Correr")
botonNuevo = Button(root, text="Nuevo")
botonAbrir = Button(root, text="Abrir")

botonGuardar.place(x=1280 - 1010, y=20)
botonCorrer.place(x=1280 - 950, y=422)
botonAbrir.place(x=26, y=10)
botonNuevo.place(x=20, y=50)

mainloop()
