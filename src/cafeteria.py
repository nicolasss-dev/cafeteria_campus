from datetime import datetime
from producto import Producto
from pedido import Pedido
from utils import *

class SistemaCafeteria:
    """Sistema principal de la cafetería"""
    
    def __init__(self):
        self.productos = []
        self.cargar_productos()
        self.autenticado = False
    
    def cargar_productos(self):
        """Carga productos desde archivo"""
        data = cargar_productos()
        self.productos = [Producto.from_dict(p) for p in data]
    
    def guardar_productos(self):
        """Guarda productos en archivo"""
        data = [p.to_dict() for p in self.productos]
        guardar_productos(data)
    
    def autenticar_admin(self):
        """Autentica al administrador"""
        if self.autenticado:
            return True
        
        print("\n🔐 Acceso de Administrador")
        print("-" * 30)
        password = input("Ingresa la clave de administrador: ")
        
        # Clave por defecto: "123"
        if password == "123":
            self.autenticado = True
            print("✅ Autenticación exitosa")
            return True
        else:
            print("❌ Clave incorrecta")
            return False
    
    def mostrar_menu_productos(self):
        """Muestra el menú de productos disponibles"""
        print("\n🍽️  MENÚ DE PRODUCTOS")
        print("="*40)
        for producto in self.productos:
            print(f"  {producto}")
        print("="*40)
    
    def buscar_producto_por_id(self, id_producto):
        """Busca un producto por su ID"""
        for producto in self.productos:
            if producto.id == id_producto:
                return producto
        return None
    
    def procesar_pedido(self):
        """Proceso principal para tomar un pedido (máx. 4 pasos)"""
        print("\n🛒 NUEVO PEDIDO")
        print("="*50)
        
        pedido = Pedido()
        
        # PASO 1: Mostrar menú
        self.mostrar_menu_productos()
        
        # PASO 2: Agregar productos
        while True:
            try:
                id_producto = validar_numero_entero("\n📝 Ingresa el número del producto (0 para terminar): ")
                
                if id_producto == 0:
                    break
                
                producto = self.buscar_producto_por_id(id_producto)
                if not producto:
                    print("❌ Producto no encontrado. Intenta de nuevo.")
                    continue
                
                cantidad = validar_numero_entero(f"📦 Cantidad de {producto.nombre}: ")
                if cantidad <= 0:
                    print("❌ La cantidad debe ser mayor a 0.")
                    continue
                
                pedido.agregar_item(producto, cantidad)
                print(f"✅ {cantidad}x {producto.nombre} agregado al pedido")
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        if not pedido.items:
            print("❌ No se agregaron productos al pedido.")
            return
        
        # PASO 3: Aplicar descuento (opcional)
        descuento = input("\n🎓 ¿Tienes carné estudiantil? (s/n): ").lower()
        if descuento == 's':
            carne = input("📄 Ingresa tu número de carné: ")
            if carne.strip():  # Validación básica
                pedido.aplicar_descuento_estudiante()
                print("✅ Descuento del 10% aplicado")
        
        # PASO 4: Mostrar resumen y finalizar
        pedido.mostrar_resumen()
        
        # Proceso de pago
        total = pedido.calcular_total()
        monto_recibido = validar_numero_float(f"\n💰 Total a pagar: ${total:,.0f}\n💵 Monto recibido: $")
        
        cambio = pedido.calcular_cambio(monto_recibido)
        if cambio is None:
            print("❌ Monto insuficiente.")
            return
        elif cambio > 0:
            print(f"💸 Cambio a entregar: ${cambio:,.0f}")
        else:
            print("✅ Pago exacto.")
        
        # Guardar venta
        guardar_venta(pedido)
        print("✅ Venta registrada exitosamente")
        
        pausar()
    
    def gestionar_productos(self):
        """Gestión de productos (requiere autenticación)"""
        if not self.autenticar_admin():
            return
        
        while True:
            limpiar_pantalla()
            print("\n⚙️  GESTIÓN DE PRODUCTOS")
            print("="*40)
            print("1. Ver productos")
            print("2. Agregar producto")
            print("3. Modificar producto")
            print("4. Eliminar producto")
            print("0. Volver al menú principal")
            print("="*40)
            
            opcion = validar_numero_entero("Selecciona una opción: ")
            
            if opcion == 1:
                self.mostrar_menu_productos()
                pausar()
            elif opcion == 2:
                self.agregar_producto()
            elif opcion == 3:
                self.modificar_producto()
            elif opcion == 4:
                self.eliminar_producto()
            elif opcion == 0:
                break
            else:
                print("❌ Opción no válida")
                pausar()
    
    def agregar_producto(self):
        """Agregar un nuevo producto"""
        print("\n➕ AGREGAR PRODUCTO")
        print("-" * 30)
        
        # Generar nuevo ID
        nuevo_id = max([p.id for p in self.productos], default=0) + 1
        
        nombre = input("Nombre del producto: ").strip()
        if not nombre:
            print("❌ El nombre no puede estar vacío")
            pausar()
            return
        
        precio = validar_numero_float("Precio del producto: $")
        if precio <= 0:
            print("❌ El precio debe ser mayor a 0")
            pausar()
            return
        
        nuevo_producto = Producto(nuevo_id, nombre, precio)
        self.productos.append(nuevo_producto)
        self.guardar_productos()
        
        print(f"✅ Producto '{nombre}' agregado exitosamente")
        pausar()
    
    def modificar_producto(self):
        """Modificar un producto existente"""
        print("\n✏️  MODIFICAR PRODUCTO")
        print("-" * 30)
        
        self.mostrar_menu_productos()
        id_producto = validar_numero_entero("\nIngresa el ID del producto a modificar: ")
        
        producto = self.buscar_producto_por_id(id_producto)
        if not producto:
            print("❌ Producto no encontrado")
            pausar()
            return
        
        print(f"\nProducto actual: {producto}")
        nuevo_nombre = input(f"Nuevo nombre (actual: {producto.nombre}): ").strip()
        if nuevo_nombre:
            producto.nombre = nuevo_nombre
        
        nuevo_precio_str = input(f"Nuevo precio (actual: ${producto.precio}): ").strip()
        if nuevo_precio_str:
            try:
                nuevo_precio = float(nuevo_precio_str)
                if nuevo_precio > 0:
                    producto.precio = nuevo_precio
                else:
                    print("❌ El precio debe ser mayor a 0")
            except ValueError:
                print("❌ Precio no válido")
        
        self.guardar_productos()
        print("✅ Producto modificado exitosamente")
        pausar()
    
    def eliminar_producto(self):
        """Eliminar un producto"""
        print("\n🗑️  ELIMINAR PRODUCTO")
        print("-" * 30)
        
        self.mostrar_menu_productos()
        id_producto = validar_numero_entero("\nIngresa el ID del producto a eliminar: ")
        
        producto = self.buscar_producto_por_id(id_producto)
        if not producto:
            print("❌ Producto no encontrado")
            pausar()
            return
        
        confirmacion = input(f"¿Confirmas eliminar '{producto.nombre}'? (s/n): ").lower()
        if confirmacion == 's':
            self.productos.remove(producto)
            self.guardar_productos()
            print("✅ Producto eliminado exitosamente")
        else:
            print("❌ Eliminación cancelada")
        
        pausar()
    
    def ver_historial_ventas(self):
        """Ver historial de ventas por día"""
        if not self.autenticar_admin():
            return
        
        print("\n📊 HISTORIAL DE VENTAS")
        print("-" * 30)
        
        fecha_str = input("Ingresa la fecha (YYYY-MM-DD) o Enter para hoy: ").strip()
        if not fecha_str:
            fecha_str = datetime.now().strftime('%Y-%m-%d')
        
        ventas = cargar_ventas_dia(fecha_str)
        
        if not ventas:
            print(f"❌ No hay ventas registradas para {fecha_str}")
            pausar()
            return
        
        print(f"\n📅 Ventas del {fecha_str}")
        print("="*50)
        
        total_dia = 0
        for i, venta in enumerate(ventas, 1):
            hora = venta['fecha_hora'].split('T')[1][:8]
            print(f"\n🧾 Venta #{i} - {hora}")
            print("-" * 25)
            for item in venta['items']:
                print(f"  {item['cantidad']}x {item['producto']} - ${item['subtotal']:,.0f}")
            
            if venta['tiene_descuento_estudiante']:
                print(f"  Descuento: -${venta['descuento']:,.0f}")
            
            print(f"  Total: ${venta['total']:,.0f}")
            total_dia += venta['total']
        
        print("="*50)
        print(f"💰 TOTAL DEL DÍA: ${total_dia:,.0f}")
        print(f"📦 VENTAS REALIZADAS: {len(ventas)}")
        print("="*50)
        
        pausar()
    
    def ejecutar(self):
        """Método principal que ejecuta el sistema"""
        while True:
            limpiar_pantalla()
            print("☕" * 20)
            print("    SISTEMA CAFETERÍA CAMPUS")
            print("☕" * 20)
            print("\n📋 MENÚ PRINCIPAL")
            print("="*40)
            print("1. 🛒 Nuevo Pedido")
            print("2. ⚙️  Gestionar Productos")
            print("3. 📊 Ver Historial de Ventas")
            print("0. 🚪 Salir")
            print("="*40)
            
            try:
                opcion = validar_numero_entero("Selecciona una opción: ")
                
                if opcion == 1:
                    self.procesar_pedido()
                elif opcion == 2:
                    self.gestionar_productos()
                elif opcion == 3:
                    self.ver_historial_ventas()
                elif opcion == 0:
                    print("\n👋 ¡Gracias por usar el Sistema Cafetería Campus!")
                    break
                else:
                    print("❌ Opción no válida. Intenta de nuevo.")
                    pausar()
                    
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                pausar()
