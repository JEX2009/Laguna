from tkinter import *
import math as m
import sqlite3 as s
import datetime as t
from os import path

class Aplicacion:
    def __init__(self, master):
        self.master = master
        master.title("VentanaPrincipal")
        master.geometry("500x500")
        for i in range(11):
            master.grid_columnconfigure(i, weight=1)
            master.grid_rowconfigure(i, weight=1)

        self.RutaBaseDeDatos = path.join("BaseDeDatos.db")
        self.Conexion = s.connect("BaseDeDatos.db")
        self.Cursor = self.Conexion.cursor()
        self.ConfiguracionBaseDatos()

        self.DatoDeComoSeGano = None
        self.PedidorDeCuantoSeGano = None
        self.FormaQuePago = None

        self.Inicio()

    def ConfiguracionBaseDatos(self):
        self.Cursor.execute('''CREATE TABLE IF NOT EXISTS Ganancias(id INTEGER PRIMARY KEY AUTOINCREMENT,Fecha TEXT, FormaGanancia TEXT,Cantidad INTEGER, FormaPago TEXT)''')
        self.Cursor.execute('''CREATE TABLE IF NOT EXISTS Gastos(id INTEGER PRIMARY KEY AUTOINCREMENT,Fecha TEXT, FormaGasto TEXT,Cantidad INTEGER)''')
        self.Conexion.commit()

    def EliminarWidgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def Inicio(self):
        self.EliminarWidgets()
        BotonDeAgregarGananciasDeHoy = Button(self.master, text="Agregar ganancias", command=self.VentanaDeAgregarGanancias)
        BotonDeAgregarGananciasDeHoy.grid(column=0, row=2)

        BotonAgregarCostosDeHoy = Button(self.master, text="Agregar costos", command=self.VentanaAgregarCostosDeHoy)
        BotonAgregarCostosDeHoy.grid(column = 8, row= 2)

    def VentanaDeAgregarGanancias(self):
        self.EliminarWidgets()
        
        s.register_adapter(t.date, lambda val: val.isoformat())

        TextoParaPedidorDeCuantoSeGano = Label(self.master, text="Agrega la cantidad que se gano hoy con la forma anterior")
        TextoParaPedidorDeCuantoSeGano.grid(columnspan=10, row=3)

        self.PedidorDeCuantoSeGano = Entry(self.master)
        self.PedidorDeCuantoSeGano.grid(columnspan=10, row=4)

        # Crear el Menubutton para la forma de ganancia
        menuBotonGanancia = Menubutton(self.master, text="Toca aca y elige la opcion de como se gano", bg="#FFCDC5")
        menuBotonGanancia.grid(column=4, row=1)

        # Crear el menú para la forma de ganancia
        menuGanancia = Menu(menuBotonGanancia, tearoff=0)
        opcionesGanancia = ["Cipres", "Hoja", "Esquinera", "Suite", "Ensueño", "Gloria", "Villa Torre", "Chalet", "Zona Verde"]
        for opcion in opcionesGanancia:
            menuGanancia.add_command(label=opcion, command=lambda op=opcion: self.ComoSeGano(op))
        menuBotonGanancia["menu"] = menuGanancia

        # Crear el Menubutton para la forma de pago
        menuBotonPago = Menubutton(self.master, text="Toca aca y elige la forma de como se pago", bg="#FFCDC5")
        menuBotonPago.grid(column=4, row=2)

        # Crear el menú para la forma de pago
        menuPago = Menu(menuBotonPago, tearoff=0)
        opcionesPago = ["Efectivo", "SinpeMovil", "Transferencia", "Tarjeta"]
        for opcion in opcionesPago:
            menuPago.add_command(label=opcion, command=lambda op=opcion: self.ComoSePago(op))
        menuBotonPago["menu"] = menuPago

        # Bloquear el botón de continuar hasta que se seleccionen ambas opciones
        self.BotonParaPasarALaSiguiente = Button(self.master, text="Continuar", command=self.VentanaParaCalcularYAgregarAlBD, state=DISABLED)
        self.BotonParaPasarALaSiguiente.grid(column=4, row=6)

        self.EstarSeguroQueEligeComoGano = Label(self.master, text="Elige una opcion de ganancia y como pago", bg="red")
        self.EstarSeguroQueEligeComoGano.grid(columnspan=10, row=5)

        self.DatosFormaQuePago = Label(self.master, text="")
        self.DatosFormaQuePago.grid(column=2, row=0)

        self.DatosComoSePago = Label(self.master, text="")
        self.DatosComoSePago.grid(column=4, row=0)

        self.Salida = Button(self.master, text="Volver",command=self.Inicio)
        self.Salida.grid(column=11, row= 0)

    def ComoSePago(self, Dato):
        self.FormaQuePago = Dato
        self.DatosComoSePago.config(text=self.FormaQuePago)
        self.ActivarBotonContinuar()

    def ComoSeGano(self, Dato):
        self.DatoDeComoSeGano = Dato
        self.DatosFormaQuePago.config(text=self.DatoDeComoSeGano)
        self.ActivarBotonContinuar()

    def ActivarBotonContinuar(self ):
        if self.DatoDeComoSeGano is not None and self.FormaQuePago is not None:
            self.EstarSeguroQueEligeComoGano.destroy()
            self.BotonParaPasarALaSiguiente.config(state=NORMAL)
            self.BotonParaPasarALaSiguiente.grid(column=4, row=5)

    def VentanaParaCalcularYAgregarAlBD(self):
        try:
            DiaDeHoy = t.date.today()
            CuantoSeGano = self.PedidorDeCuantoSeGano.get()
            CuantoSeGano = float(CuantoSeGano)
            if self.FormaQuePago == "Tarjeta":
                CuantoSeGano = CuantoSeGano * (1 - 13 / 100) 

            self.Cursor.execute("INSERT INTO Ganancias (Fecha,FormaGanancia,Cantidad,FormaPago) VALUES (?,?,?,?)", (DiaDeHoy, self.DatoDeComoSeGano, CuantoSeGano, self.FormaQuePago))
            self.Conexion.commit()

            self.EliminarWidgets()

            Label(self.master, text="Se quiere seguir agregando ganancias?").grid(columnspan=10, row=2)

            Button(self.master, text="Si", command=self.VentanaDeAgregarGanancias).grid(column=6, row=4)
            Button(self.master, text="No", command=self.Inicio).grid(column=3, row=4)

        except ValueError:  # Si acaso se le ocurre  poner letras
            self.EliminarWidgets()

            Label(self.master, text="Ocurrio un error no puedes poner letras o dejar en blanco el espacio de cuanto se gano").grid(column=2, row=2)
            self.master.update()

            self.master.after(3000, self.VentanaDeAgregarGanancias)
        except Exception as e:  # En caso que la base de datos falle
            self.EliminarWidgets()

            Label(self.master, text="Ocurrio un error con la base de datos intente reiniciar y si no contacte con el programador").grid(column=2, row=2)
            self.master.update()

            self.master.after(3000, self.Inicio)

    def VentanaAgregarCostosDeHoy(self):
        self.EliminarWidgets()
        Label(self.master, text= "Agrega el nombre del gasto ej: Jairo, Pequeño mundo, brenes, luz, etc.. ").grid(columnspan=10,row=1)
        self.TipoDeGasto = Entry(self.master)
        self.TipoDeGasto.grid(columnspan=10, row=2)

        Label(self.master, text= "De cuanto fue el gasto?").grid(columnspan=10, row=3)
        self.CantidadDeGasto = Entry(self.master)
        self.CantidadDeGasto.grid(columnspan= 10 ,row=4)

        self.BotonParaPasarSiguiente = Button(self.master, text="Continuar", command=self.VentanaParaAgregarGastoBD)
        self.BotonParaPasarSiguiente.grid(column=4, row=6)

        self.Salida = Button(self.master, text="Volver",command=self.Inicio)
        self.Salida.grid(column=11, row= 0)

    def VentanaParaAgregarGastoBD(self):
        try:
            
            DiaDeHoy = t.date.today().isoformat()
            self.DatoTipoDeGasto = self.TipoDeGasto.get()

            self.DatoCantidadDeGasto = self.CantidadDeGasto.get()
            self.DatoCantidadDeGasto = float(self.DatoCantidadDeGasto)
            
            self.Cursor.execute("INSERT INTO Gastos (Fecha,FormaGasto,Cantidad) VALUES (?,?,?)", (DiaDeHoy, self.DatoTipoDeGasto, self.DatoCantidadDeGasto))
            self.Conexion.commit()

            self.EliminarWidgets()

            Label(self.master, text="Se quiere seguir agregando costos?").grid(columnspan=10, row=2)

            Button(self.master, text="Si", command=self.VentanaAgregarCostosDeHoy).grid(column=6, row=4)
            Button(self.master, text="No", command=self.Inicio).grid(column=3, row=4)

        except ValueError:
            self.EliminarWidgets()

            Label(self.master, text="Ocurrio un error no puedes poner letras o dejar en blanco el espacio de cuanto se gasto").grid(column=2, row=2)
            self.master.update()

            self.master.after(3000, self.VentanaDeAgregarGanancias)
        except Exception as e:  # En caso que la base de datos falle
            print(e)
            self.EliminarWidgets()

            Label(self.master, text="Ocurrio un error con la base de datos intente reiniciar y si no contacte con el programador").grid(column=2, row=2)
            self.master.update()

            self.master.after(3000, self.Inicio)






root = Tk()
app = Aplicacion(root)
root.mainloop()