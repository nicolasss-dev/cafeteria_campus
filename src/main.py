#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Cafetería Campus
Desarrollado para el curso de Ingeniería de Requisitos
"""

from cafeteria import SistemaCafeteria

def main():
    """Función principal del programa"""
    try:
        sistema = SistemaCafeteria()
        sistema.ejecutar()
    except Exception as e:
        print(f"Error crítico: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
