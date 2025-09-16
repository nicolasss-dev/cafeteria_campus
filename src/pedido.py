from datetime import datetime

class ItemPedido:
    """Representa un item individual en el pedido"""
    
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad
        self.subtotal = producto.precio * cantidad
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} - ${self.subtotal:,.0f}"

class Pedido:
    """Clase para manejar un pedido completo"""
    
    def __init__(self):
        self.items = []
        self.descuento = 0
        self.tiene_descuento_estudiante = False
        self.fecha_hora = datetime.now()
    
    def agregar_item(self, producto, cantidad):
        """Agrega un producto al pedido"""
        item = ItemPedido(producto, cantidad)
        self.items.append(item)
    
    def calcular_subtotal(self):
        """Calcula el subtotal sin descuentos"""
        return sum(item.subtotal for item in self.items)
    
    def aplicar_descuento_estudiante(self):
        """Aplica descuento del 10% para estudiantes"""
        if not self.tiene_descuento_estudiante:
            subtotal = self.calcular_subtotal()
            self.descuento = subtotal * 0.1
            self.tiene_descuento_estudiante = True
    
    def calcular_total(self):
        """Calcula el total final del pedido"""
        return self.calcular_subtotal() - self.descuento
    
    def calcular_cambio(self, monto_recibido):
        """Calcula el cambio a entregar"""
        total = self.calcular_total()
        if monto_recibido >= total:
            return monto_recibido - total
        return None
    
    def mostrar_resumen(self):
        """Muestra el resumen detallado del pedido"""
        print("\n" + "="*50)
        print("           RESUMEN DEL PEDIDO")
        print("="*50)
        
        for item in self.items:
            print(f"  {item}")
        
        print("-"*50)
        subtotal = self.calcular_subtotal()
        print(f"  Subtotal: ${subtotal:,.0f}")
        
        if self.tiene_descuento_estudiante:
            print(f"  Descuento estudiante (10%): -${self.descuento:,.0f}")
        
        total = self.calcular_total()
        print(f"  TOTAL: ${total:,.0f}")
        print("="*50)
    
    def to_dict(self):
        """Convierte el pedido a diccionario para guardarlo"""
        return {
            'fecha_hora': self.fecha_hora.isoformat(),
            'items': [
                {
                    'producto': item.producto.nombre,
                    'cantidad': item.cantidad,
                    'precio_unitario': item.producto.precio,
                    'subtotal': item.subtotal
                }
                for item in self.items
            ],
            'subtotal': self.calcular_subtotal(),
            'descuento': self.descuento,
            'tiene_descuento_estudiante': self.tiene_descuento_estudiante,
            'total': self.calcular_total()
        }
