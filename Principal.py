from tkinter import *
import math as m
import sqlite3 as s
import datetime as t
import os as a

#Variables para usar gets
DatoDeComoSegano = ""
PedidorDeCuantoSeGano = 0

# Crea una base de datos junto a su conexion y cursor
RutaBaseDeDatos = a.path.join("BaseDeDatos.db")  

Conexion = s.connect("BaseDeDatos.db")
Cursor = Conexion.cursor()

#Crea una ventana y le ajusta la geometria
Ventana = Tk()
Ventana.title("Ventana principal")
Ventana.geometry("500x500")
for i in range(11):
            Ventana.grid_columnconfigure(i,weight=1)
            Ventana.grid_rowconfigure(i,weight=1)

#Configura la base de datos  y annade las tablas y columnas 
# Se cambia   EXISTS <Nombre de tabla> (<Nombre Columna> <Tipo de dato>)
def ConfiguracionBaseDatos():
    Cursor.execute('''CREATE TABLE IF NOT EXISTS Ganancias(id INTEGER PRIMARY KEY AUTOINCREMENT,Fecha Text, Forma_Ganancia TEXT,Cantidad INTEGER)''')
    Cursor.execute('''CREATE TABLE IF NOT EXISTS Gastos(id INTEGER PRIMARY KEY AUTOINCREMENT,Fecha Text, Forma_Gasto TEXT,Cantidad INTEGER)''')
    Conexion.commit()

ConfiguracionBaseDatos()


#Funcion para eliminar
def EliminarWidgets():
        for widget in Ventana.winfo_children():
            widget.destroy()   

#Home de la aplicacion
def Inicio():
    EliminarWidgets()
    BotonDeAgregargananciasDeHoy =Button(text= "Agregar ganacias" , command= lambda :VentanaDeAgregarGanancias())
    BotonDeAgregargananciasDeHoy.grid(column=0 , row =2)

Inicio()

# La interfaz del boton Agregar ganancias
def VentanaDeAgregarGanancias():
    EliminarWidgets()
    global BotonParaPasarALaSiguiente
    global EstarSeguroQueEligeComoGano
    global DatoDeComoSegano
    global PedidorDeCuantoSeGano

    s.register_adapter(t.date, lambda val: val.isoformat())

    TextoParaPedidorDeCuantoSeGano = Label(Ventana, text="Agrega la cantidad que se gano hoy con la forma anterior")
    TextoParaPedidorDeCuantoSeGano.grid(columnspan= 10, row = 2)

    PedidorDeCuantoSeGano = Entry(Ventana)
    PedidorDeCuantoSeGano.grid(columnspan=10,row = 3)

    BotonParaPasarALaSiguiente = Button(text= "Continuar", command= lambda:VentanaParaCalcularYAgregarAlBD())
    BotonParaPasarALaSiguiente.grid(column= 4, row= 5)

    # Crear el Menubutton
    menu_boton = Menubutton(Ventana, text="Toca aca y elige la opcion de como se gano", bg= "#FFCDC5")  # Texto del botón
    menu_boton.grid(column=4, row = 1)  # Ajusta pady para la posición vertical

    # Crear el menú
    menu = Menu(menu_boton, tearoff=0)
    menu.add_command(label="Cipres", command=lambda: ComoSeGano("Cipres"))  # Se cambia el nombre por las opciones que quieres dar
    menu.add_command(label="Hoja", command=lambda: ComoSeGano("Hoja"))
    menu.add_command(label="Esquinera", command=lambda: ComoSeGano("Esquinera"))
    menu.add_command(label="Suite", command=lambda: ComoSeGano("Suite"))
    menu.add_command(label="Ensueño", command=lambda: ComoSeGano("Ensueño"))
    menu.add_command(label="Gloria", command=lambda: ComoSeGano("Gloria"))
    menu.add_command(label="Villa Torre", command=lambda: ComoSeGano("Villa Torre"))
    menu.add_command(label="Chalet", command=lambda: ComoSeGano("Chalet"))
    menu.add_command(label="Zona Verde", command=lambda: ComoSeGano("Zona Verde"))

    # Asignar el menú al Menubutton
    menu_boton["menu"] = menu
    
    # Bloque la opcion de pulsar el boton sin haber elegido una opcion del  menu
    if DatoDeComoSegano == "":  
        EstarSeguroQueEligeComoGano = Label(Ventana, text= "Elige una opcion de ganancia",bg = "red")
        EstarSeguroQueEligeComoGano.grid(columnspan= 10, row= 4)
        BotonParaPasarALaSiguiente.config(state=DISABLED)

# Se obtiene los datos del menu que se van a insertar y se activa el boton
def ComoSeGano(Dato):
    
    EstarSeguroQueEligeComoGano.destroy()

    BotonParaPasarALaSiguiente.grid(column= 4, row= 4)
    DatoDeComoSegano = Dato
    BotonParaPasarALaSiguiente.config(state=NORMAL)

# Se obtienen el resto de datos 
def VentanaParaCalcularYAgregarAlBD():
    try:        
        DiaDeHoy = t.date.today()
        CuantoSeGano = PedidorDeCuantoSeGano.get()
        CuantoSeGano = float(CuantoSeGano)
        Cursor.execute("INSERT INTO Ganancias (Fecha,Forma_Ganancia,Cantidad) VALUES (?,?,?)",(DiaDeHoy,DatoDeComoSegano,CuantoSeGano)) #INTO  <Nombre tabla> (<Columnas a la que se va a agrega>)
        Conexion.commit()
        
        EliminarWidgets()
    
        Label(Ventana, text= "Se quiere seguir agregando ganancias?").grid( columnspan=10 ,row=2)
    
        Button(Ventana,text= "Si", command=lambda: VentanaDeAgregarGanancias()).grid( column= 6,row=4)
        Button(Ventana,text= "No", command=lambda: Inicio()).grid( column= 3,row=4)
    except ValueError: # Si acaso se le ocurre  poner letras
        EliminarWidgets()
        Label(Ventana, text = "Ocurrio un error no puedes poner letras en ese espacio").grid(column= 2, row= 2)
        Ventana.update()
        Ventana.after(3000, VentanaDeAgregarGanancias())
    except e: # En caso que la base de datos falle
        EliminarWidgets()
        Label(Ventana, text = "Ocurrio un error con la base de datos intente reiniciar y si no contacte con el programador").grid(column= 2, row= 2)
        Ventana.update()
        Ventana.after(3000, Inicio())
        

    

Ventana.mainloop()

