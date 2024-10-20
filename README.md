
Este es un programa de escritorio desarrollado en Python que utiliza la librería Tkinter para la interfaz gráfica y SQLite para la gestión de una base de datos. El programa está diseñado para llevar un registro de ganancias, gastos y generar reportes semanales y mensuales.

## Características principales

* **Registro de ganancias:** Permite ingresar la cantidad ganada, la forma en que se ganó (categorías predefinidas) y la forma de pago.
* **Registro de gastos:** Permite ingresar el nombre del gasto y la cantidad gastada.
* **Reportes:** Genera reportes semanales y mensuales de ganancias, gastos y balance total.
* **Almacenamiento en base de datos:** Utiliza una base de datos SQLite para almacenar la información de ganancias y gastos.
* **Interfaz gráfica amigable:** Interfaz intuitiva y fácil de usar con Tkinter.

## Requisitos

* Python 3.x
* Librerías Tkinter y SQLite3 (generalmente incluidas en la instalación estándar de Python)

## Instrucciones de uso

1. **Clonar el repositorio** o descargar el código fuente.
2. **Ejecutar el archivo principal:** `python main.py` (o el nombre del archivo que contiene el código).
3. **Utilizar la interfaz gráfica:**
    * **Agregar ganancias:** Ingresar la cantidad, seleccionar la forma de ganancia y la forma de pago.
    * **Agregar gastos:** Ingresar el nombre del gasto y la cantidad.
    * **Generar reportes:** Seleccionar el tipo de reporte (semanal o mensual) y visualizar los resultados.

## Estructura del código

* **Clase `Aplicacion`:** 
    * Maneja la lógica principal de la aplicación.
    * Controla la interfaz gráfica (ventanas, botones, etiquetas).
    * Interactúa con la base de datos (conexión, consultas).
* **Funciones:**
    * `ConfiguracionBaseDatos`: Crea las tablas en la base de datos si no existen.
    * `EliminarWidgets`: Limpia la ventana actual.
    * `Inicio`: Muestra la ventana principal con las opciones iniciales.
    * `VentanaDeAgregarGanancias`: Ventana para agregar nuevas ganancias.
    * `VentanaAgregarCostosDeHoy`: Ventana para agregar nuevos gastos.
    * `VentanaSeleccionReporte`: Ventana para seleccionar el tipo de reporte.
    * `VentanaReporteSemanal`: Genera el reporte semanal.
    * `VentanaReporteMensual`: Genera el reporte mensual.
    * `MensualesPasadas`: Muestra un historial de ganancias mensuales.
    * `DivisionCapital`: (En desarrollo) Función para dividir el capital.

## Base de datos

El programa utiliza una base de datos SQLite llamada `BaseDeDatos.db`. Contiene las siguientes tablas:

* **Ganancias:** Almacena la información de las ganancias (fecha, forma de ganancia, cantidad, forma de pago).
* **Gastos:** Almacena la información de los gastos (fecha, forma de gasto, cantidad).
* **Mensual:** Almacena el balance mensual (fecha, cantidad total).

## Posibles mejoras

* **Validación de datos:** Implementar una validación más robusta para los campos de entrada.
* **Funcionalidad de división de capital:** Completar la función `DivisionCapital` para calcular la división del capital.
* **Gráficos:** Incluir gráficos en los reportes para una mejor visualización de la información.
* **Exportar reportes:** Permitir exportar los reportes en diferentes formatos (PDF, Excel).
* **Interfaz más atractiva:** Mejorar el diseño y la estética de la interfaz gráfica.
* **Autenticación de usuario:** Agregar un sistema de inicio de sesión para mayor seguridad.

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún error o tienes alguna sugerencia, por favor crea un "issue" o envía un "pull request".
