import numpy as np
import re
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def funcion_lineal(x, m=1, b=0):
    return m*x+b

def extraer_coeficientes(ecuacion):
    match = re.match(r"y\s*=\s*([+-]?\d*\.?\d*)x\s*([+-]\d*\.?\d*)?", ecuacion)
    if match:
        m = float(match.group(1)) if match.group(1) else 1.0
        b = float(match.group(2)) if match.group(2) else 0.0
        return m, b

    match = re.match(r"([+-]?\d*\.?\d*)x\s*\+\s*([+-]?\d*\.?\d*)y\s*=\s*([+-]?\d*\.?\d*)", ecuacion)
    if match:
        a = float(match.group(1))
        b = float(match.group(2))
        c = float(match.group(3))
        return a / b, c / b

    match = re.match(r"([+-]?\d*\.?\d*)y\s*-\s*([+-]?\d*\.?\d*)x\s*=\s*([+-]?\d*\.?\d*)", ecuacion)
    if match:
        b = float(match.group(1))
        a = float(match.group(2))
        d = float(match.group(3))
        return a / b, d / b

    raise ValueError("Formato de ecuación no válido")

def graficacion(ecuacion):
    x = np.linspace(-10, 10, 50)
    m, b = extraer_coeficientes(ecuacion)
    y = funcion_lineal(x, m, b)

    x_puntos = [-5.0, 0.0, 5.0]
    y_puntos = [funcion_lineal(xi, m, b) for xi in x_puntos]

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    ax.plot(x, y, '-r', label=ecuacion)
    ax.scatter(x_puntos, y_puntos, color='red', label='Puntos Intermedios')
    for xi, yi in zip(x_puntos, y_puntos):
        ax.text(xi, yi + 3, f'({xi},{yi:.2f})', ha='center')
    ax.set_title('Función Lineal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ax.legend(loc='upper left')

    global canvas_widget
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=1, column=0, columnspan=4)
    canvas.draw()

def obtener_y_graficar():
    ecuacion_usuario = entrada_ecuacion.get().lower()
    try:
        graficacion(ecuacion_usuario)
    except ValueError:
        messagebox.showerror("Error", "Formato de ecuación no válido")


def reset_grafica():
    entrada_ecuacion.delete(0, tk.END)

    global canvas_widget
    if canvas_widget:
        canvas_widget.destroy()




ventana = tk.Tk()
ventana.title("Graficador de Funciones Lineales")

label = tk.Label(ventana, text="Ingrese la ecuación:")
label.grid(row=0, column=0, padx=10, pady=10)

entrada_ecuacion = tk.Entry(ventana, width=25)
entrada_ecuacion.grid(row=0, column=1, padx=10, pady=10)

btn_graficar = tk.Button(ventana, text="Graficar", command=obtener_y_graficar)
btn_graficar.grid(row=0, column=2, padx=10, pady=10)

btn_nueva_grafica = tk.Button(ventana, text="Nueva Gráfica", command=reset_grafica)
btn_nueva_grafica.grid(row=0, column=3, padx=10, pady=10)

canvas_widget = None

ventana.mainloop()