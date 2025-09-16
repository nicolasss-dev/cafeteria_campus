import json
import os
from datetime import datetime

def cargar_productos():
    """Carga los productos desde el archivo JSON"""
    try:
        with open('data/productos.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        # Si no existe el archivo, crear productos por defecto
        productos_default = [
            {"id": 1, "nombre": "Café Americano", "precio": 3000},
            {"id": 2, "nombre": "Sandwich de Jamón", "precio": 8000},
            {"id": 3, "nombre": "Empanada", "precio": 2500},
            {"id": 4, "nombre": "Jugo Natural", "precio": 4000},
            {"id": 5, "nombre": "Croissant", "precio": 3500}
        ]
        guardar_productos(productos_default)
        return productos_default

def guardar_productos(productos):
    """Guarda los productos en el archivo JSON"""
    os.makedirs('data', exist_ok=True)
    with open('data/productos.json', 'w', encoding='utf-8') as file:
        json.dump(productos, file, indent=2, ensure_ascii=False)

def guardar_venta(pedido):
    """Guarda una venta en el archivo correspondiente al día"""
    fecha_str = pedido.fecha_hora.strftime('%Y-%m-%d')
    directorio = 'data/ventas'
    os.makedirs(directorio, exist_ok=True)
    
    archivo_ventas = f"{directorio}/ventas_{fecha_str}.json"
    
    # Cargar ventas existentes del día
    ventas = []
    if os.path.exists(archivo_ventas):
        try:
            with open(archivo_ventas, 'r', encoding='utf-8') as file:
                ventas = json.load(file)
        except:
            ventas = []
    
    # Agregar nueva venta
    ventas.append(pedido.to_dict())
    
    # Guardar ventas actualizadas
    with open(archivo_ventas, 'w', encoding='utf-8') as file:
        json.dump(ventas, file, indent=2, ensure_ascii=False)

def cargar_ventas_dia(fecha_str):
    """Carga las ventas de un día específico"""
    archivo_ventas = f"data/ventas/ventas_{fecha_str}.json"
    if os.path.exists(archivo_ventas):
        try:
            with open(archivo_ventas, 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            return []
    return []

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\nPresiona Enter para continuar...")

def validar_numero_entero(mensaje):
    """Valida que el input sea un número entero"""
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print("❌ Por favor ingresa un número válido.")

def validar_numero_float(mensaje):
    """Valida que el input sea un número decimal"""
    while True:
        try:
            valor = float(input(mensaje))
            return valor
        except ValueError:
            print("❌ Por favor ingresa un número válido.")
