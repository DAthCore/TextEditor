import tkinter as tk
from tkinter.filedialog import askopenfile, asksaveasfilename #Módulo etiqueta, paquete FileDialog se importa las funciones de Hash Open File, ademas de la fución As Save As Filename

#FileDialog: Permite abrir una ventana de busqueda

class Editor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('DAthCore | Editor de Texto')
        #Configuración del tamaño minimo de la ventana
        self.rowconfigure(0, minsize=600, weight=1)
        #Configuracion de  la segunda columna
        self.columnconfigure(1, minsize=600, weight=1)
        #Atributo Campo de Texto
        self.campo_texto = tk.Text(self, wrap=tk.WORD)
        #Atributo del archivo
        self.archivo = None
        #Atributo para saber si ya se abrió un archivo anteriormente
        self.archivo_abierto = False
        #Craeacion de componentes
        self._crear_componentes()
        
    def _crear_componentes(self):
        frame_botones = tk.Frame(self, relief=tk.RAISED, bd=2)
        boton_abrir = tk.Button(frame_botones, text='Abrir', command=self._abrir_archivo)
        boton_guardar = tk.Button(frame_botones, text='Guardar', command=self._guardar)
        boton_guardar_como = tk.Button(frame_botones, text='Guardar Como...', command=self._guardar_como)
        #Los botones los expandimos de manera horizontal (sticky='we')
        boton_abrir.grid(row=0, column=0, sticky='we', padx=5, pady=5)
        boton_guardar.grid(row=1, column=0, sticky='we', padx=5, pady=5)
        boton_guardar_como.grid(row=2, column=0, sticky='we', padx=5, pady=5)
        #Se coloca el frame de manera vertical
        frame_botones.grid(row=0, column=0, sticky='ns')
        #Agregamos el campo de texto, se expandirá por completo por el espacio disponible
        self.campo_texto.grid(row=0, column=1, sticky='nswe')
        
    def _crear_menu(self):
        #Creamos el menu de la App
        menu_app = tk.Menu(self)
        self.config(menu = menu_app)
        #Agregamos la opciones a nuestro menú
        #Agregamos menú archivo
        menu_archivo = tk.Menu(menu_app, tearoff=False)
        menu_app.add_cascade(label='Archivo', menu=menu_archivo)
        #Agregamos la opciones del menú archivo
        menu_archivo.add_command(label='Abrir', command=self._abrir_archivo)
        menu_archivo.add_command(label='Guardar', command=self._guardar)
        menu_archivo.add_command(label='Guardar Como...', command=self._guardar_como)
        menu_archivo.add_separator()
        menu_archivo.add_command(label='Salir', command=self.quit)
    
    def _abrir_archivo(self):
        #Abrir archivo para edición (lectura-escritura)
        self.archivo_abierto = askopenfile(mode='r+') #r: Raiz o de lectura
        #Eliminar texo anterior
        self.campo_texto.delete(1.0, tk.END) #Desde línea 1 hasta el final del texto comando END
        #Revisamos si hay un archivo
        if not self.archivo_abierto:
            return
        #Abrimos el archivo en modo lectura/escritura como recurso
        with open(self.archivo_abierto.name, 'r+') as self.archivo:
            texto = self.archivo.read() #Leemos el contenido del archivo
            self.campo_texto.insert(1.0, texto) #Insertamos el contenido del archivo
            self.title(f'DAthCore * Editor Texto - {self.archivo.name}') #Modificamos el titulo de la aplicación
    
    def _guardar(self):
        #Si ya se abrió previamente un archivo, lo sobreescribimos:
        if self.archivo_abierto:
            #Salvamos el archivo (lo abrimos en modo escritura)
            with open(self.archivo_abierto.name, 'w') as self.archivo:
                #Leemos el contenido de la caja de texto
                texto = self.campo_texto.get(1.0, tk.END)
                #Escribimos el contenido al mismo archivo
                self.archivo.write(texto)
                #Cambiamos el nombre del titulo de la app
                self.title(f'DAthCore * Editor Texto -  {self.archivo.name}')
        else: #Caso contarrio que no tengamos un archivo abierto, mandamos llamar el metodo Guardar como..
            self._guardar_como()
    
    def _guardar_como(self):
        #Salavamos el archivo actual como un nuevo archivo
        self.archivo = asksaveasfilename(
            defaultextension='txt',
            filetypes=[('Archivos de Texto', '*.txt'), ('Todos los archivos', '*.*')]
        )
        if not self.archivo:
            return
        #Abrimos el archivo en modo escritura (write)
        with open(self.archivo, 'w') as archivo:
            #Leemos el contenido de la caja de texto
            texto = self.campo_texto.get(1.0, tk.END)
            #Escribimos el contenido al nuevo archivo
            archivo.write(texto)
            #Cambiamos el nombre del archivo
            self.title(f'DAthCore | Editor de Texto - {archivo.name}') 
            #Indicamos que hemos abierto un archivo
            self.archivo_abierto = archivo
        
if __name__ == '__main__':
    editor = Editor()
    editor.mainloop()