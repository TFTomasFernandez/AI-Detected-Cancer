import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import tensorflow as tf
import numpy as np
import MySQLdb
import csv
from datetime import datetime

# Cargar el modelo automáticamente al iniciar la aplicación
def cargar_modelo():
    global model
    model = tf.keras.models.load_model('modelo_cancer_piel.h5')
    messagebox.showinfo("Información", "Modelo cargado exitosamente")

# Función para preprocesar la imagen
def preprocesar_imagen(imagen_path):
    imagen = tf.keras.preprocessing.image.load_img(imagen_path, target_size=(128, 128))
    imagen_array = tf.keras.preprocessing.image.img_to_array(imagen)
    imagen_array = np.expand_dims(imagen_array, axis=0)
    imagen_array /= 255.0
    return imagen_array

def guardar_en_db(nombre, dni, fecha, prediccion, imagen_path):
    try:
        # Establecer la conexión a la base de datos
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="predicciones")
        cursor = db.cursor()
        
        # Comando SQL para insertar los datos en la tabla 'predicciones'
        sql = "INSERT INTO predicciones (nombre, dni, fecha, prediccion, imagen_path) VALUES (%s, %s, %s, %s, %s)"
        
        # Ejecutar el comando SQL con los valores correspondientes
        cursor.execute(sql, (nombre, dni, fecha, prediccion, imagen_path))
        
        # Confirmar los cambios en la base de datos
        db.commit()
        
    except MySQLdb.OperationalError as e:
        # Error relacionado con la conexión a la base de datos
        messagebox.showerror("Error", f"Error de conexión a la base de datos: {str(e)}")
    except MySQLdb.IntegrityError as e:
        # Error relacionado con la integridad de los datos
        messagebox.showerror("Error", f"Error de integridad de los datos: {str(e)}")
    except MySQLdb.Error as e:
        # Otros errores de MySQLdb
        messagebox.showerror("Error", f"Error al guardar en la base de datos: {str(e)}")
    except Exception as e:
        # Otros errores generales
        messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    finally:
        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        db.close()

# Función para seleccionar la imagen
def seleccionar_imagen():
    global imagen_path, imagen_tk
    imagen_path = filedialog.askopenfilename()
    
    if imagen_path:
        # Cargar y mostrar la imagen seleccionada en el Label
        imagen = Image.open(imagen_path)
        imagen = imagen.resize((250, 250), Image.LANCZOS)  # Ajustar tamaño de la imagen
        imagen_tk = ImageTk.PhotoImage(imagen)
        
        label_imagen.config(image=imagen_tk)
        label_imagen.image = imagen_tk  # Guardar referencia a la imagen para que no sea recolectada por el GC
        
        messagebox.showinfo("Información", "Imagen seleccionada correctamente")

# Función para hacer la predicción
def predecir():
    nombre = entry_nombre.get()
    dni = entry_dni.get()
    fecha = entry_fecha.get()
    
    if not nombre or not dni or not fecha:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    
    if not imagen_path:
        messagebox.showerror("Error", "Debe seleccionar una imagen")
        return
    
    imagen_array = preprocesar_imagen(imagen_path)
    prediccion = model.predict(imagen_array)
    porcentaje = prediccion[0][0] * 100
    if prediccion[0][0] > 0.5:
        resultado = f"La imagen tiene una probabilidad de {prediccion[0][0] * 100:.2f}% de ser maligna."
    else:
        resultado = f"La imagen tiene una probabilidad de {(1 - prediccion[0][0]) * 100:.2f}% de ser benigna."

    
    messagebox.showinfo("Resultado", resultado)
    
    # Guardar en base de datos
    guardar_en_db(nombre, dni, fecha, resultado, imagen_path)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Predicción de Cáncer de Piel")
root.geometry("600x800")  # Ajustar el tamaño de la ventana

# Usar ttk para widgets más modernos y bien proporcionados
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 14, "bold"), foreground="black", background="lightgray")
style.configure("TButton", font=("Helvetica", 14, "bold"), foreground="black", background="gray")
style.configure("TEntry", font=("Helvetica", 14))
style.configure("TFrame", background="lightgray")

# Crear un frame ajustado al tamaño de la ventana
frame = ttk.Frame(root, padding="20 20 20 20")
frame.grid(row=0, column=0, sticky="nsew")  # Expande el frame para cubrir todo el espacio

# Ajustar las proporciones de las columnas y filas del frame
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Nombre Completo
ttk.Label(frame, text="Nombre Completo:").grid(row=0, column=0, padx=10, pady=10, sticky="ew")
entry_nombre = ttk.Entry(frame, width=30)
entry_nombre.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# DNI
ttk.Label(frame, text="DNI:").grid(row=2, column=0, padx=10, pady=10, sticky="ew")
entry_dni = ttk.Entry(frame, width=30)
entry_dni.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

# Fecha de la Imagen
ttk.Label(frame, text="Fecha de la Imagen:").grid(row=4, column=0, padx=10, pady=10, sticky="ew")
entry_fecha = DateEntry(frame, date_pattern='yyyy-mm-dd', width=27)
entry_fecha.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

# Botón para seleccionar la imagen
btn_seleccionar_imagen = ttk.Button(frame, text="Seleccionar Imagen", command=seleccionar_imagen)
btn_seleccionar_imagen.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

# Label para mostrar la imagen
label_imagen = ttk.Label(frame)
label_imagen.grid(row=7, column=0, padx=10, pady=10)

# Botón para predecir
btn_predecir = ttk.Button(frame, text="Predecir", command=predecir)
btn_predecir.grid(row=8, column=0, padx=10, pady=20, sticky="ew")

# Ajustar las proporciones de las columnas para que se expanda correctamente
frame.grid_columnconfigure(0, weight=1)

# Cargar el modelo al iniciar la aplicación
cargar_modelo()

root.mainloop()
