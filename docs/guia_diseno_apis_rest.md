# Guía de Especificaciones y Buenas Prácticas para el Diseño de APIs RESTful

Este documento establece los estándares de arquitectura, diseño de URLs, manejo de métodos HTTP, serialización y patrones de datos para el desarrollo de APIs RESTful en la aplicación.

---

## 1. Arquitectura de Capas y Flujo de Datos

Toda petición debe seguir un flujo unidireccional y desacoplado entre capas:

$$\text{Controlador (HTTP)} \longrightarrow \text{Servicio (Negocio)} \longrightarrow \text{Reader / Repositorio (BD)} \longrightarrow \text{Modelo}$$

### Responsabilidades por Capa:

1. **Controlador (`Resource` / View):**
   * Gestiona únicamente la capa de transporte HTTP.
   * Recibe la petición, extrae parámetros (`request.args`, `request.get_json()`) y llama a la capa de servicio.
   * Retorna el código de estado HTTP (`200`, `201`, `400`, `404`, `500`) y la respuesta serializada.
   * **No contiene lógica de negocio ni consultas a la base de datos.**

2. **Servicio (`Service`):**
   * Contiene toda la lógica de negocio, reglas de validación complejas, permisos y orquestación de operaciones.
   * **Recomendación:** Debe existir incluso para operaciones de lectura (`GET`) si hay reglas de negocio, filtrados por usuario o transformaciones.

3. **Reader / Repositorio (`Reader` / `Repository`):**
   * Encapsula el acceso a la base de datos (SQLAlchemy / ORM).
   * Contiene los `JOIN`s, filtros y consultas optimizadas.

---

## 2. Convención de URLs y Métodos HTTP

Las URLs deben representar **recursos del negocio en plural (sustantivos)**, evitando verbos en la ruta (ej: `/api/ibkr-contracts` en lugar de `/api/getContracts`).

### 📌 Tabla de Convención de Métodos

| Método HTTP | Ruta | Descripción | Idempotente |
| :--- | :--- | :--- | :---: |
| **`GET`** | `/api/v2/ibkr/contracts` | Obtener lista de contratos (soporta query params). | ✅ Sí |
| **`POST`** | `/api/v2/ibkr/contracts` | Crear o cargar contratos. | ❌ No |
| **`GET`** | `/api/v2/ibkr/contracts/<id>` | Obtener un contrato por su ID. | ✅ Sí |
| **`PUT`** | `/api/v2/ibkr/contracts/<id>` | **Reemplazo total** del contrato (envía todos los campos). | ✅ Sí |
| **`PATCH`** | `/api/v2/ibkr/contracts/<id>` | **Edición parcial** (modifica solo los campos enviados). | ⚠️ Sí |
| **`DELETE`** | `/api/v2/ibkr/contracts/<id>` | Eliminar contrato por ID. | ✅ Sí |

### Separación de Controladores (Colección vs. Detalle)
Se recomienda separar las rutas en dos clases de controladores:
```python
# 1. Colección
api.add_resource(IbkrContractsListController, '/api/v2/ibkr/contracts')

# 2. Recurso Individual
api.add_resource(IbkrContractDetailController, '/api/v2/ibkr/contracts/<int:contract_id>')
```

---

## 3. Serialización, Validación y Seguridad

### Uso de Marshmallow vs. `dict` directos

* **Entidades del Dominio (Obligatorio Marshmallow):**
  Para devolver o recibir recursos (`User`, `Contract`), se **debe** utilizar un `Schema` de Marshmallow.
  * **Filtro de Seguridad (Whitelist):** Previene la exposición accidental de campos sensibles (hashes de contraseña, tokens internos).
  * **Consistencia:** Formatea fechas en ISO-8601 y garantiza tipos de datos.

* **Respuestas de Control (Permitido `dict` / `jsonify`):**
  Para mensajes de confirmación simples, pings de salud o errores genéricos:
  ```python
  return jsonify({"message": "Recurso eliminado correctamente"}), 200
  ```

---

## 4. Filtros, Búsquedas y Consultas Complejas

Las URLs representan recursos, no la estructura física de las tablas SQL. Si una consulta requiere `JOIN`s en la base de datos, el endpoint de la API sigue siendo el mismo.

### 4.1. Filtros con Query Parameters (`GET`)
Para búsquedas y filtrados estándar:
```http
GET /api/ibkr-contracts?exchange=NASDAQ&currency=USD&status=ACTIVE
```
*En el backend, el Servicio/Reader añade los `JOIN`s y `.filter()` dinámicamente según los parámetros presentes.*

### 4.2. Sub-recursos (Relaciones Padre-Hijo)
Si un recurso depende directamente de un padre:
```http
GET /api/accounts/123/contracts
```

### 4.3. Búsqueda Avanzada (`POST /search`)
Si la búsqueda requiere enviar filtros complejos (arrays de IDs, rangos múltiples de fechas o JSONs anidados):
```http
POST /api/ibkr-contracts/search
```

### 4.4. Carga de Catálogos para el Frontend (`/lookups`)
Para optimizar el rendimiento del cliente y llenar múltiples `<select>` en una sola petición HTTP:
```http
GET /api/lookups?types=exchanges,currencies,asset_types
```

---

## 5. Múltiples Formularios que Crean en la Misma Tabla

Cuando el frontend tiene **varios formularios distintos** con diferentes validaciones que guardan en la misma tabla de la BD, se aplican las siguientes estrategias:

1. **Sub-rutas por Tipo/Intención (Recomendada):**
   ```http
   POST /api/ibkr-contracts/stocks     --> (Formulario de Acciones)
   POST /api/ibkr-contracts/options    --> (Formulario de Opciones)
   POST /api/ibkr-contracts/sync-exchange --> (Importación Masiva)
   ```
   *Cada ruta usa su propio Marshmallow Schema de validación, pero el Servicio inserta en la misma tabla.*

2. **Campo Discriminador en un solo Endpoint:**
   `POST /api/ibkr-contracts` enviando `"contract_type": "STOCK"` en el JSON para seleccionar el esquema de validación dinámicamente.

3. **Wizard por Etapas:**
   Crear en estado `DRAFT` con `POST` y actualizar los siguientes formularios secuencialmente con `PATCH /api/ibkr-contracts/<id>/step-2`.

---

## 6. Enriquecimiento de Datos y Rendimiento (Eager Loading)

Al devolver un recurso enriquecido con datos de tablas secundarias o catálogos:

1. **Marshmallow (`fields.Nested`):** Anida la información del catálogo en el JSON de respuesta.
2. **SQLAlchemy (`joinedload` / `selectinload`):** **MANDATORIO** en la capa de datos para evitar el problema de rendimiento N+1 queries.

```python
# Ejemplo de consulta optimizada en el Servicio/Reader
from sqlalchemy.orm import joinedload

def get_enriched_contracts():
    return db.session.query(IbkrContract)\
        .options(joinedload(IbkrContract.exchange))\
        .options(joinedload(IbkrContract.currency))\
        .all()
```

---

## 7. Estructura Estándar de Respuestas HTTP

### Respuesta Exitosa (`200 OK` / `201 Created`):
```json
{
  "success": true,
  "message": "Operación realizada con éxito.",
  "data": { ... }
}
```

### Respuesta de Error (`400 Bad Request` / `404 Not Found` / `500 Internal Error`):
```json
{
  "success": false,
  "message": "Descripción clara del error.",
  "errors": [ ... ]
}
```
*Centraliza el manejo de excepciones usando `@app.errorhandler(AppException)` para mantener los controladores limpios de bloques `try/except` repetitivos.*
