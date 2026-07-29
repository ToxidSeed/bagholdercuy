# Proveedores de Datos de Mercados - Módulos Base

Este paquete define los módulos y las clases base necesarias para la integración de distintos proveedores de datos de mercado en el sistema (por ejemplo, IBKR, Massive, etc.).

## Propósito

El objetivo de este directorio es actuar como una capa de abstracción común. Al centralizar las interfaces y clases base en este paquete, nos aseguramos de que todos los proveedores de datos implementen la misma firma de métodos y comportamiento estándar, facilitando la mantenibilidad y la escalabilidad del sistema ante la adición de nuevas fuentes de datos.

## Componentes del Paquete

*   **[series_loader_base.py](file:///home/alone/sources/bagholdercuy/service/markets_data_providers/base/series_loader_base.py):** Define la clase e interfaz base para la carga y actualización de series de datos históricos o en tiempo real.
*   **[__init__.py](file:///home/alone/sources/bagholdercuy/service/markets_data_providers/base/__init__.py):** Inicializador del paquete de Python.

## Guía de Uso para Nuevos Proveedores

Para crear un nuevo proveedor de datos de mercado:
1. Cree un nuevo subpaquete dentro de `service/markets_data_providers/`.
2. Importe las clases base definidas en este directorio (e.g., de `series_loader_base.py`).
3. Implemente los métodos abstractos requeridos por la clase base para interactuar con la API o servicio específico del nuevo proveedor.