from tkinter import *
import math as m
import sqlite3 as s
import datetime as t
from os import path

# Clase principal de la aplicación
class Aplicacion:
    def __init__(self, master):
        # Configuración inicial de la ventana principal
        self.master = master
        master.title("VentanaPrincipal")
        master.geometry("500x500")
        
        # Configuración del grid para el layout de la ventana
        for i in range(11):
            master.grid_columnconfigure(i, weight=1)
            master.grid_rowconfigure(i, weight=1)

        # Ruta a la base de datos SQLite
        self.RutaBaseDeDatos = path.join("BaseDeDatos.db")
        # Conexión a la base de datos
        self.Conexion = s.connect("BaseDeDatos.db")
        self.Cursor = self.Conexion.cursor()
        
        # Crear las tablas necesarias en la base de datos si no existen
        self.ConfiguracionBaseDatos()

        # Variables para almacenar información sobre ganancias y pagos
        self.DatoDeComoSeGano = None
        self.PedidorDeCuantoSeGano = None
        self.FormaQuePago = None

        # Llamar a la función de inicio
        self.Inicio()

    # Configuración inicial de la base de datos
    def ConfiguracionBaseDatos(self):
        # Crear la tabla de Ganancias si no existe
        self.Cursor.execute('''CREATE TABLE IF NOT EXISTS Ganancias(id INTEGER PRIMARY KEY AUTOINCREMENT,Fecha TEXT, FormaGanancia TEXT,Cantidad INTEGER, FormaPago TEXT)''')
        # Crear la tabla de Gastos si no existe
        self.Cursor.execute('''CREATE TABLE IF NOT EXISTS Gastos(id INTEGER PRIMARY KEY AUTOINCREMENT,Fecha TEXT, FormaGasto TEXT,Cantidad INTEGER)''')
        self.Conexion.commit()

    # Elimina todos los widgets de la ventana
    def EliminarWidgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    # Ventana principal con opciones iniciales
    def Inicio(self):
        self.EliminarWidgets()
        
        # Botón para agregar ganancias
        BotonDeAgregarGananciasDeHoy = Button(self.master, text="Agregar ganancias", command=self.VentanaDeAgregarGanancias)
        BotonDeAgregarGananciasDeHoy.grid(column=2, row=2)

        # Botón para agregar costos
        BotonAgregarCostosDeHoy = Button(self.master, text="Agregar costos", command=self.VentanaAgregarCostosDeHoy)
        BotonAgregarCostosDeHoy.grid(column=8, row=2)

        # Botón para hacer un reporte
        BotonHacerReporte = Button(self.master, text="Hacer reporte", command=self.VentanaSeleccionReporte)
        BotonHacerReporte.grid(column=2, row=6)

        

    # Ventana para agregar ganancias del día
    def VentanaDeAgregarGanancias(self):
        self.EliminarWidgets()
        
        # Registrar un adaptador para trabajar con fechas en SQLite
        s.register_adapter(t.date, lambda val: val.isoformat())

        # Texto explicativo
        TextoParaPedidorDeCuantoSeGano = Label(self.master, text="Agrega la cantidad que se ganó hoy con la forma anterior")
        TextoParaPedidorDeCuantoSeGano.grid(columnspan=10, row=3)

        # Campo para ingresar la cantidad ganada
        self.PedidorDeCuantoSeGano = Entry(self.master)
        self.PedidorDeCuantoSeGano.grid(columnspan=10, row=4)

        # Menubutton para seleccionar cómo se ganó
        menuBotonGanancia = Menubutton(self.master, text="Toca acá y elige cómo se ganó", bg="#FFCDC5")
        menuBotonGanancia.grid(column=4, row=1)
        
        # Crear el menú con las opciones de cómo se ganó
        menuGanancia = Menu(menuBotonGanancia, tearoff=0)
        self.opcionesGanancia = ["Cipres", "Hoja", "Esquinera", "Suite", "Ensueño", "Gloria", "Villa Torre", "Chalet", "Zona Verde"]
        for opcion in self.opcionesGanancia:
            menuGanancia.add_command(label=opcion, command=lambda op=opcion: self.ComoSeGano(op))
        menuBotonGanancia["menu"] = menuGanancia

        # Menubutton para seleccionar cómo se pagó
        menuBotonPago = Menubutton(self.master, text="Toca acá y elige cómo se pagó", bg="#FFCDC5")
        menuBotonPago.grid(column=4, row=2)

        # Crear el menú con las opciones de formas de pago
        menuPago = Menu(menuBotonPago, tearoff=0)
        opcionesPago = ["Efectivo", "SinpeMovil", "Transferencia", "Tarjeta"]
        for opcion in opcionesPago:
            menuPago.add_command(label=opcion, command=lambda op=opcion: self.ComoSePago(op))
        menuBotonPago["menu"] = menuPago

        # Botón para continuar, desactivado hasta que se seleccionen opciones
        self.BotonParaPasarALaSiguiente = Button(self.master, text="Continuar", command=self.VentanaParaCalcularYAgregarAlBD, state=DISABLED)
        self.BotonParaPasarALaSiguiente.grid(column=4, row=6)

        # Texto que indica seleccionar opciones
        self.EstarSeguroQueEligeComoGano = Label(self.master, text="Elige una opción de ganancia y cómo pagó", bg="red")
        self.EstarSeguroQueEligeComoGano.grid(columnspan=10, row=5)

        # Etiquetas que muestran las opciones seleccionadas
        self.DatosFormaQuePago = Label(self.master, text="")
        self.DatosFormaQuePago.grid(column=2, row=0)

        self.DatosComoSePago = Label(self.master, text="")
        self.DatosComoSePago.grid(column=4, row=0)

        # Botón para volver al inicio
        self.Salida = Button(self.master, text="Volver", command=self.Inicio)
        self.Salida.grid(column=11, row=0)

    # Función que almacena la forma en que se pagó
    def ComoSePago(self, Dato):
        self.FormaQuePago = Dato
        self.DatosComoSePago.config(text=self.FormaQuePago)
        self.ActivarBotonContinuar()

    # Función que almacena la forma en que se ganó
    def ComoSeGano(self, Dato):
        self.DatoDeComoSeGano = Dato
        self.DatosFormaQuePago.config(text=self.DatoDeComoSeGano)
        self.ActivarBotonContinuar()

    # Habilita el botón de continuar cuando ambas opciones (cómo se ganó y cómo se pagó) están seleccionadas
    def ActivarBotonContinuar(self):
        if self.DatoDeComoSeGano is not None and self.FormaQuePago is not None:
            self.EstarSeguroQueEligeComoGano.destroy()
            self.BotonParaPasarALaSiguiente.config(state=NORMAL)
            self.BotonParaPasarALaSiguiente.grid(column=4, row=5)

    # Ventana para calcular y agregar la ganancia a la base de datos
    def VentanaParaCalcularYAgregarAlBD(self):
        try:
            # Obtener la fecha actual y la cantidad ganada
            DiaDeHoy = t.date.today()
            DiaDeHoy = DiaDeHoy.strftime("%d/%m/%Y")
            CuantoSeGano = self.PedidorDeCuantoSeGano.get()
            CuantoSeGano = float(CuantoSeGano)
            
            # Aplicar descuento si se pagó con tarjeta
            if self.FormaQuePago == "Tarjeta":
                CuantoSeGano = CuantoSeGano * (1 - 13 / 100)

            # Insertar el registro en la base de datos
            self.Cursor.execute("INSERT INTO Ganancias (Fecha, FormaGanancia, Cantidad, FormaPago) VALUES (?, ?, ?, ?)", 
                                (DiaDeHoy, self.DatoDeComoSeGano, CuantoSeGano, self.FormaQuePago))
            self.Conexion.commit()

            # Mensaje de confirmación y opción de agregar más ganancias
            self.EliminarWidgets()
            Label(self.master, text="¿Deseas seguir agregando ganancias?").grid(columnspan=10, row=2)
            Button(self.master, text="Sí", command=self.VentanaDeAgregarGanancias).grid(column=6, row=4)
            Button(self.master, text="No", command=self.Inicio).grid(column=3, row=4)

        except ValueError:
            # Manejar errores si se ingresan datos no válidos
            self.EliminarWidgets()
            Label(self.master, text="Error: No puedes ingresar letras o dejar el campo vacío.").grid(column=2, row=2)
            self.master.update()
            self.master.after(3000, self.VentanaDeAgregarGanancias)

        except Exception as e:
            # Manejar errores relacionados con la base de datos
            self.EliminarWidgets()
            Label(self.master, text="Error con la base de datos. Reinicie la aplicación o contacte al programador.").grid(column=2, row=2)
            self.master.update()
            self.master.after(3000, self.Inicio)

    # Ventana para agregar costos del día
    def VentanaAgregarCostosDeHoy(self):
        self.EliminarWidgets()
        
        # Entrada para el nombre o tipo de gasto
        Label(self.master, text="Agrega el nombre del gasto ej: Jairo, Pequeño mundo, Brenes, luz, etc.").grid(columnspan=10, row=1)
        self.TipoDeGasto = Entry(self.master)
        self.TipoDeGasto.grid(columnspan=10, row=2)

        # Entrada para la cantidad gastada
        Label(self.master, text="¿De cuánto fue el gasto?").grid(columnspan=10, row=3)
        self.CantidadDeGasto = Entry(self.master)
        self.CantidadDeGasto.grid(columnspan=10, row=4)

        # Botón para continuar
        self.BotonParaPasarSiguiente = Button(self.master, text="Continuar", command=self.VentanaParaAgregarGastoBD)
        self.BotonParaPasarSiguiente.grid(column=4, row=6)

        # Botón para volver al menú principal
        self.Salida = Button(self.master, text="Volver", command=self.Inicio)
        self.Salida.grid(column=11, row=0)

    # Función para agregar el gasto a la base de datos
    def VentanaParaAgregarGastoBD(self):
        try:
            # Obtener la fecha de hoy y formatearla
            DiaDeHoy = t.date.today()
            DiaDeHoy = DiaDeHoy.strftime("%d/%m/%Y")
            
            # Obtener y formatear el tipo de gasto y la cantidad gastada
            self.DatoTipoDeGasto = self.TipoDeGasto.get()
            self.DatoTipoDeGasto = self.DatoTipoDeGasto.capitalize()  # Capitalizar la primera letra

            self.DatoCantidadDeGasto = self.CantidadDeGasto.get()
            self.DatoCantidadDeGasto = float(self.DatoCantidadDeGasto)  # Convertir a float para guardar en la base de datos
            
            # Insertar los datos en la tabla Gastos
            self.Cursor.execute("INSERT INTO Gastos (Fecha, FormaGasto, Cantidad) VALUES (?, ?, ?)", (DiaDeHoy, self.DatoTipoDeGasto, self.DatoCantidadDeGasto))
            self.Conexion.commit()

            # Limpiar la pantalla después de agregar el gasto
            self.EliminarWidgets()

            # Mensaje para preguntar si se quiere agregar más costos
            Label(self.master, text="¿Se quiere seguir agregando costos?").grid(columnspan=10, row=2)

            # Botones para seguir agregando o volver al menú principal
            Button(self.master, text="Sí", command=self.VentanaAgregarCostosDeHoy).grid(column=6, row=4)
            Button(self.master, text="No", command=self.Inicio).grid(column=3, row=4)

        except ValueError:
            # Manejo de error si se ingresan letras en la cantidad de gasto
            self.EliminarWidgets()
            Label(self.master, text="Error: No puedes ingresar letras o dejar en blanco el campo de cantidad de gasto").grid(column=2, row=2)
            self.master.update()
            self.master.after(3000, self.VentanaAgregarCostosDeHoy)  # Volver a la ventana de agregar costos tras 3 segundos

        except Exception as e:
            # Manejo de error general, como problemas con la base de datos
            print(e)  # Mostrar el error en la consola
            self.EliminarWidgets()
            Label(self.master, text="Ocurrió un error con la base de datos. Intente reiniciar la aplicación o contacte al programador").grid(column=2, row=2)
            self.master.update()
            self.master.after(3000, self.Inicio)  # Volver al menú principal tras 3 segundos

    # Ventana para seleccionar el tipo de reporte
    def VentanaSeleccionReporte(self):
        self.EliminarWidgets()

        # Botón para generar un reporte semanal
        BotonReporteSemanal = Button(self.master, text="Reporte Semanal", command=self.VentanaReporteSemanal)
        BotonReporteSemanal.grid(column=2, row=2)

        # Botón para generar un reporte mensual
        BotonReporteMensual = Button(self.master, text="Reporte Mensual", command=self.VentanaReporteMensual)
        BotonReporteMensual.grid(column=8, row=2)

        self.Salida = Button(self.master, text="Volver", command=self.Inicio)
        self.Salida.grid(column=11, row=0)
        
    # Generar un reporte semanal de ganancias
    def VentanaReporteSemanal(self):
        self.EliminarWidgets()

        # Obtener la fecha actual y el inicio de la semana
        self.Hoy = t.datetime.now()
        self.InicoSemana = self.Hoy - t.timedelta(days=self.Hoy.weekday())  # Calcular el lunes de la semana actual
        self.Hoy = self.Hoy.strftime("%d/%m/%Y")
        self.InicoSemana = self.InicoSemana.strftime("%d/%m/%Y")

        # Diccionario para almacenar las ganancias por categoría
        Diccionario = dict.fromkeys(["Cipres", "Hoja", "Esquinera", "Suite", "Ensueño", "Gloria", "Villa Torre", "Chalet", "Zona Verde"], 0)

        # Consultar la base de datos para obtener las ganancias de la semana
        self.Cursor.execute(f"SELECT FormaGanancia, Cantidad FROM Ganancias WHERE Fecha BETWEEN '{self.InicoSemana}' AND '{self.Hoy}'")
        Resultados = self.Cursor.fetchall()

        # Sumar las ganancias de cada categoría
        for i in Resultados:
            Clave = i[0]  # Tipo de ganancia
            Valor = i[1]  # Monto de ganancia
            Valor = Diccionario.get(Clave) + Valor
            Diccionario[Clave] = Valor

        # Mostrar los resultados en la interfaz
        Fila = 0
        self.TotalDeGanancias = []
        for i in Diccionario:
            self.TotalDeGanancias.append(Diccionario.get(i))
            Label(self.master, text=f"Con {i} se ganó {Diccionario.get(i)}").grid(columnspan=10, row=Fila)
            Fila += 1
        # Mostrar el total de ganancias de la semana
        Label(self.master, text=f"Desde {self.InicoSemana} hasta el {self.Hoy} se ganó en total {sum(self.TotalDeGanancias)}").grid(columnspan=10, row=Fila)

        # Botón para mostrar los costos semanales
        BotonParaMostrarCostos = Button(self.master, text="Mostrar costos", command=self.VentanaReporteSemanalCostos)
        BotonParaMostrarCostos.grid(column=11, row=Fila)

    # Mostrar el reporte semanal de costos
    def VentanaReporteSemanalCostos(self):
        self.EliminarWidgets()

        # Diccionario para almacenar los gastos por categoría
        Diccionario = {}

        # Consultar la base de datos para obtener los costos de la semana
        self.Cursor.execute(f"SELECT FormaGasto, Cantidad FROM Gastos WHERE Fecha BETWEEN '{self.InicoSemana}' AND '{self.Hoy}'")
        Resultados = self.Cursor.fetchall()

        # Sumar los costos de cada categoría
        for i in Resultados:
            Clave = i[0]  # Tipo de gasto
            Valor = i[1]  # Monto del gasto
            if Clave in Diccionario:
                Valor = Diccionario.get(Clave) + Valor
            Diccionario[Clave] = Valor

        # Mostrar los costos en la interfaz
        Fila = 0
        self.TotalDeGastos = []
        for i in Diccionario:
            self.TotalDeGastos.append(Diccionario.get(i))
            Label(self.master, text=f"En {i} se gastó {Diccionario.get(i)}").grid(columnspan=10, row=Fila)
            Fila += 1

        # Mostrar el total de gastos de la semana
        Label(self.master, text=f"Desde {self.InicoSemana} hasta el {self.Hoy} se gastó en total {sum(self.TotalDeGastos)}").grid(columnspan=10, row=Fila)

        # Botón para mostrar el balance total (ganancias - costos)
        BotonParaMostrarTotales = Button(self.master, text="Mostrar total", command=self.VentanaReporteSemanalTotal)
        BotonParaMostrarTotales.grid(column=11, row=Fila)

    # Mostrar el balance semanal total (ganancias - costos)
    def VentanaReporteSemanalTotal(self):
        self.EliminarWidgets()

        # Calcular el balance general
        TotalGeneral = sum(self.TotalDeGanancias) - sum(self.TotalDeGastos)

        # Mostrar el balance final en la interfaz
        Label(self.master, text=f"Desde {self.InicoSemana} hasta el {self.Hoy} se obtuvo un total de {TotalGeneral}").grid(columnspan=10, row=5)

        # Botón para salir y volver al menú principal
        Salir = Button(self.master, text="Salir", command=self.Inicio)
        Salir.grid(column=11, row=0)

    # Generar un reporte mensual de ganancias
    def VentanaReporteMensual(self):
        self.EliminarWidgets()

        # Obtener la fecha actual y el inicio del mes
        self.PrimerDiaMes = t.datetime.now()
        # Calcular el primer día del mes anterior
        self.PrimerDiaMesPasado = t.date(self.PrimerDiaMes.year, self.PrimerDiaMes.month, 1) - t.timedelta(days=1)
        self.PrimerDiaMesPasado = self.PrimerDiaMesPasado.replace(day=1)

        # Formatear las fechas
        self.PrimerDiaMes = self.PrimerDiaMes.strftime("%d/%m/%Y")
        self.PrimerDiaMesPasado = self.PrimerDiaMesPasado.strftime("%d/%m/%Y")

        # Diccionario para almacenar las ganancias por categoría
        Diccionario = dict.fromkeys(["Cipres", "Hoja", "Esquinera", "Suite", "Ensueño", "Gloria", "Villa Torre", "Chalet", "Zona Verde"], 0)

        # Consultar la base de datos para obtener las ganancias de la semana
        self.Cursor.execute(f"SELECT FormaGanancia, Cantidad FROM Ganancias WHERE Fecha BETWEEN '{self.PrimerDiaMesPasado}' AND '{self.PrimerDiaMes}'")
        Resultados = self.Cursor.fetchall()

        # Sumar las ganancias de cada categoría
        for i in Resultados:
            Clave = i[0]  # Tipo de ganancia
            Valor = i[1]  # Monto de ganancia
            Valor = Diccionario.get(Clave) + Valor
            Diccionario[Clave] = Valor

        # Mostrar los resultados en la interfaz
        Fila = 0
        self.TotalDeGananciasMensual = []
        for i in Diccionario:
            self.TotalDeGananciasMensual.append(Diccionario.get(i))
            Label(self.master, text=f"Con {i} se ganó {Diccionario.get(i)}").grid(columnspan=10, row=Fila)
            Fila += 1
        # Mostrar el total de ganancias de la semana
        Label(self.master, text=f"Desde {self.InicoSemana} hasta el {self.Hoy} se ganó en total {sum(self.TotalDeGananciasMensual)}").grid(columnspan=10, row=Fila)

        # Botón para mostrar los costos semanales
        BotonParaMostrarCostos = Button(self.master, text="Mostrar costos", command=self.VentanaReporteMensualCostos)
        BotonParaMostrarCostos.grid(column=11, row=Fila)

    # Mostrar el reporte mensual de costos
    def VentanaReporteMensualCostos(self):
        self.EliminarWidgets()

        # Diccionario para almacenar los gastos por categoría
        Diccionario = {}

        # Consultar la base de datos para obtener los costos de la semana
        self.Cursor.execute(f"SELECT FormaGasto, Cantidad FROM Gastos WHERE Fecha BETWEEN '{self.PrimerDiaMesPasado}' AND '{self.PrimerDiaMes}'")
        Resultados = self.Cursor.fetchall()

        # Sumar los costos de cada categoría
        for i in Resultados:
            Clave = i[0]  # Tipo de gasto
            Valor = i[1]  # Monto del gasto
            if Clave in Diccionario:
                Valor = Diccionario.get(Clave) + Valor
            Diccionario[Clave] = Valor

        # Mostrar los costos en la interfaz
        Fila = 0
        self.TotalDeGastosMensual = []
        for i in Diccionario:
            self.TotalDeGastos.append(Diccionario.get(i))
            Label(self.master, text=f"En {i} se gastó {Diccionario.get(i)}").grid(columnspan=10, row=Fila)
            Fila += 1

        # Mostrar el total de gastos de la semana
        Label(self.master, text=f"Desde {self.InicoSemana} hasta el {self.Hoy} se gastó en total {sum(self.TotalDeGastosMensual)}").grid(columnspan=10, row=Fila)

        # Botón para mostrar el balance total (ganancias - costos)
        BotonParaMostrarTotales = Button(self.master, text="Mostrar total", command=self.VentanaReporteMensualTotal)
        BotonParaMostrarTotales.grid(column=11, row=Fila)

    # Mostrar el balance mensual total (ganancias - costos)
    def VentanaReporteMensualTotal(self):
        self.EliminarWidgets()

        # Calcular el balance general
        TotalGeneral = sum(self.TotalDeGananciasMensual) - sum(self.TotalDeGastosMensual)

        # Mostrar el balance final en la interfaz
        Label(self.master, text=f"Desde {self.PrimerDiaMesPasado} hasta el {self.PrimerDiaMes} se obtuvo un total de {TotalGeneral}").grid(columnspan=10, row=5)

        # Botón para salir y volver al menú principal
        Salir = Button(self.master, text="Salir", command=self.Inicio)
        Salir.grid(column=11, row=0)






root = Tk()
app = Aplicacion(root)
root.mainloop()