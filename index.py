from tkinter import ttk
from tkinter import *
# Conectar con la base de datos
import sqlite3

class Productos:
    
    db_nombre = 'base_datos.db'
    
    
    def __init__(self,window):
        self.wind = window
        self.wind.title("Sistema de Stock")
        
        
        # TODO: CREO UN CONTENEDOR (FRAME)
        frame = LabelFrame(self.wind,   text="Registrar nuevo producto")    
        frame.grid(row=0, column=0, columnspan= 6, pady= 15)

        
        # TODO: Producto INPUT
        Label(frame, text= "Nombre: ").grid(row=1, column=0)
        self.nombre = Entry(frame)
        # Para al abrir la app el cursor este ubicado en esta posicion
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)
        
        # TODO: Categoria INPUT
        Label(frame, text= "Categoria: ").grid(row=2, column=0)
        self.categoria = Entry(frame)
        self.categoria.grid(row=2, column=1)
        
        # TODO: Stock INPUT
        Label(frame, text= "Stock: ").grid(row=3, column=0)
        self.stock = Entry(frame)
        self.stock.grid(row=3, column=1)
        
        # TODO: Descripcion INPUT
        Label(frame, text= "Descripción: ").grid(row=4, column=0)
        self.descripcion = Entry(frame)
        self.descripcion.grid(row=4, column=1)
        
        # TODO: Boton Agregar Producto
        ttk.Button(frame, text="Guardar producto", command=self.agregar_productos).grid(row=5, columnspan=2, sticky=W + E)
        
        # TODO: MENSAJE DE CONFIRMACION
        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=6,column=0, columnspan=4, sticky=W + E) # WEST TO EAST (OESTE A ESTE)
        
        
        # TODO: Tabla (Arbol de vista)
        self.tree= ttk.Treeview(height=10, columns=3)
        self.tree.grid(row=7, column=0, columnspan=4)
        self.tree.heading('#0', text="Producto", anchor= CENTER)
        # self.tree.heading('#1', text="Categoria", anchor= CENTER)
        self.tree.heading('#1', text="Stock", anchor= CENTER)
        # self.tree.heading('#3', text="Descripcion", anchor= CENTER)
        
        # TODO: BOTONES: ACTUALIZAR, ELIMINAR
        ttk.Button(text="ELIMINAR" , command=self.eliminar_productos).grid(row=8,column=0, columnspan=2, sticky= W + E)
        ttk.Button(text="EDITAR" , command=self.editar_productos).grid(row=8,column=2, columnspan=3, sticky= W + E)
        
        # TODO: LLENAR PRODUCTOS EN TABLA
        self.obtener_productos()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_nombre) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query,parameters)
            conn.commit()
        return resultado
    
    
    def obtener_productos(self):
        # Limpiando la tabla
        grabados = self.tree.get_children()
        for elemento in grabados:
            self.tree.delete(elemento)
        
        # Consultando los datos
        query = 'SELECT * FROM productos ORDER BY nombre DESC'
        db_row = self.run_query(query)
        # Rellenando los datos de la tabla
        for row in db_row:
            self.tree.insert('',0, text= row[1], values= row[3]) 
    
    
    # TODO: VALIDAR QUE LOS DATOS NO ESTEN VACIOS
    def validar_datos(self):
        return len(self.nombre.get()) != 0 and len(self.stock.get()) != 0 and len(self.categoria.get()) != 0
             
    
    
    # TODO: AGREGAR PRODUCTOS
    def agregar_productos(self):
        if self.validar_datos():
            query = 'INSERT INTO productos VALUES(NULL, ?, ?, ?, ?)'
            parameters = (self.nombre.get(),self.categoria.get(),self.stock.get(),self.descripcion.get())
            self.run_query(query, parameters)
            # print("Datos guardados correctamente") Lo reemplazo por el Label de mensaje
            self.mensaje['text'] = 'Producto {} agregado correctamente'.format(self.nombre.get())
            # De esta manera luego de agregar un producto, limpio la ventana
            self.nombre.delete(0, END)
            self.categoria.delete(0, END)
            self.stock.delete(0, END)
            self.descripcion.delete(0, END)
        else:
            self.mensaje['text'] = "Todos los campos son requeridos"
        self.obtener_productos()
        
        
    # TODO: ELIMINAR PRODUCTOS
    def eliminar_productos(self):
        #print(self.tree.item(self.tree.selection())) Muestra
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0] # Si no pongo el indice 0, no me muestra este mensaje
        except IndexError as e:
            self.mensaje['text'] = "Debe seleccionar un producto"
            return
        self.mensaje['text'] = ''
        nombre = self.tree.item(self.tree.selection())['text']
        query = ' DELETE FROM productos WHERE nombre = ?'
        self.run_query(query,(nombre,))
        self.mensaje['text'] = "Producto {} eliminado correctamente".format(nombre)
        self.obtener_productos()
        
    # TODO: EDITAR PRODUCTO
    def editar_productos(self):
        #print(self.tree.item(self.tree.selection())) #Muestra
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = "Debe seleccionar un producto"
            return
        nombre = self.tree.item(self.tree.selection())['text']
        stock_viejo = self.tree.item(self.tree.selection())['values'][0]
        # TopLevel ==> Para crear una ventana apartir de otra
        self.ventana_editar = Toplevel()
        self.ventana_editar.title = 'Editar Producto'
        
        # Antiguo nombre
        Label(self.ventana_editar, text= 'Nombre Actual: ').grid(row=0,column=1)
        Entry(self.ventana_editar, textvariable= StringVar(self.ventana_editar, value= nombre), state='readonly').grid(row=0, column=2)
        # Nuevo nombre
        Label(self.ventana_editar,text='Nombre Nuevo: ').grid(row=1, column=1)
        nombre_nuevo = Entry(self.ventana_editar)
        nombre_nuevo.grid(row=1,column=2)
        
        # Antiguo STOCK
        Label(self.ventana_editar, text= 'Stock Actual: ').grid(row=2,column=1)
        Entry(self.ventana_editar, textvariable= StringVar(self.ventana_editar, value= stock_viejo), state='readonly').grid(row=2, column=2)
        # Nuevo STOCK
        Label(self.ventana_editar,text='Stock Nuevo: ').grid(row=3, column=1)
        stock_nuevo = Entry(self.ventana_editar)
        stock_nuevo.grid(row=3,column=2)
        
        # TODO: BOTON EDITAR
        Button(self.ventana_editar, text="Actualizar" , command= lambda: self.actualizar_productos(nombre_nuevo.get(),nombre, stock_nuevo.get(), stock_viejo)).grid(row=4, column=2, sticky= W)
        
        
        # TODO: Actualizar PRODUCTOS
    def actualizar_productos(self,nombre_nuevo, nombre, stock_nuevo, stock_viejo):
        query = ' UPDATE productos set nombre = ? , stock = ? WHERE nombre = ? AND stock= ?'
        parameters = (nombre_nuevo, stock_nuevo, nombre, stock_viejo)
        self.run_query(query,parameters)
        self.ventana_editar.destroy()
        self.mensaje['text'] = "Producto {} actualizado correctamente".format(nombre)
        self.obtener_productos()
        
        
if __name__ == '__main__':
    window = Tk()
    aplicacion = Productos(window)
    window.mainloop()