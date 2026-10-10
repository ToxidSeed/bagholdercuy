# Guía de Arquitectura: Controladores (`controller.md`)

Este documento establece las convenciones y estándares obligatorios para la creación y estructuración de los controladores en el proyecto.

---

## 1. Nomenclatura de Módulos
* Cada módulo dentro del paquete debe seguir estrictamente la siguiente estructura de nombres:
  * `{dominio}_controller.py`
  * *Ejemplo:* Si el dominio es cliente, el archivo será `cliente_controller.py`.

---

## 2. Definición de Clases y Herencia
* Las clases que se encarguen de exponer endpoints dentro del módulo deben:
  * Llevar el sufijo **`Controller`**.
  * Heredar de la clase base **`Resource`** (proveniente del framework de API, ej. Flask-RESTful).
  * *Ejemplo:* `class ClienteController(Resource):`

---

## 3. Validación de Datos de Entrada (Pydantic)
* Toda la validación de los datos de entrada (payloads, parámetros de consulta, etc.) debe realizarse obligatoriamente utilizando **Pydantic**.
* Los esquemas de validación correspondientes deben ubicarse en el directorio o paquete **`schemas`**.

---

## 4. Serialización y Contratos de Salida (Marshmallow)
* Las respuestas que representen conjuntos de datos o registros (por ejemplo, la información detallada de un cliente o una lista de clientes) deben encapsularse mediante contratos de salida utilizando **Marshmallow**.
* Los esquemas de serialización de salida deben ubicarse estrictamente en la ruta: **`schemas/responses`**.

---

## 5. Estándar de Respuestas HTTP
* Al heredar de `Resource`, los métodos HTTP (`get`, `post`, `put`, `delete`, etc.) deben retornar respuestas estandarizadas.
* El formato de retorno debe ajustarse a las convenciones del framework (por ejemplo, retornar un diccionario/objeto serializado convertido a JSON junto con su código de estado HTTP correspondiente).
* *Ejemplo:* 
  ```python
  return response_data, 200  # O 400 para errores de validación, 404 si no existe, etc.