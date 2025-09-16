class Producto:
    """Clase para representar un producto de la cafetería"""
    
    def __init__(self, id_producto, nombre, precio):
        self.id = id_producto
        self.nombre = nombre
        self.precio = precio
    
    def __str__(self):
        return f"{self.id}. {self.nombre} - ${self.precio:,.0f}"
    
    def to_dict(self):
        """Convierte el producto a diccionario para guardarlo en JSON"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un producto desde un diccionario"""
        return cls(data['id'], data['nombre'], data['precio'])
