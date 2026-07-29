# ESPECIFICACIÓN DE LA ARQUITECTURA Y PAQUETES (BAGHOLDER CUY)
Este archivo sirve como especificación técnica y mapa de referencia de la arquitectura del proyecto `Bagholder Cuy`. Su propósito es documentar detalladamente cada paquete, sus responsabilidades, dependencias y patrones de diseño implementados para servir de insumo directo (contexto) en prompts para Modelos de Lenguaje (LLMs).

---

## 1. Resumen de la Arquitectura Global
El proyecto `Bagholder Cuy` es una plataforma web de control de portafolios de inversión, cálculo de rentabilidades (P&L realizado) mediante el algoritmo FIFO, y sincronización con Interactive Brokers (IBKR).

La solución se divide en dos componentes principales:
1. **Backend (Python / Flask)**: API REST estructurada bajo un patrón modular similar a DDD (Domain-Driven Design) y CQRS simple (separando lecturas vía `reader` de escrituras/orquestaciones vía `service`/`model/bussiness`). Utiliza SQLAlchemy como ORM conectado a MySQL.
2. **Frontend (Javascript / Vue 2 + Quasar v1)**: Interfaz de usuario interactiva y responsiva con gráficos avanzados de rentabilidad, importadores de datos y paneles de gestión de transacciones.

  ```mermaid
  graph TD
      subgraph Frontend ["Vue.js App - view/client"]
          UI["Componentes/Páginas Quasar"] --> Vuex["Store de Estado"]
          Vuex --> Axios["Clientes API HTTP"]
      end

      subgraph Backend ["Flask API"]
          Axios --> EntryAPI["app.py / EntryAPI"]
          EntryAPI --> Router["routes/router.py"]
          Router --> Controller["controller/"]
          
          subgraph Presentacion ["Capa de Presentación / Validación"]
              Controller --> Parser["parser/"]
              Controller --> Schemas["schemas/"]
          end

          subgraph Aplicacion ["Capa de Aplicación y Lógica"]
              Controller --> Service["service/"]
              Service --> Processor["processor/"]
              Service --> Reader["reader/"]
          end

          subgraph Dominio ["Capa de Dominio y Datos"]
              Service --> Business["model/bussiness/"]
              Business --> Model["model/ - SQLAlchemy ORM"]
              Reader --> Model
              Model --> MySQL[("Base de Datos MySQL")]
          end
          
          subgraph Integraciones ["Integraciones Externas"]
              Service --> API_Client["api/"]
              API_Client --> ExtAPI["APIs Financieras: Alphavantage, Tiingo, IBKR, etc."]
          end
      end
  ```

---

## 2. Mapa y Catálogo de Paquetes del Backend
El backend está organizado en paquetes altamente especializados en la raíz del proyecto. A continuación se detalla cada uno de ellos:

### 2.1. `app.py` & `main.py`
* **Responsabilidad**: Son los puntos de entrada (bootstrap) de la aplicación Flask.
* **Patrón de Diseño**:
  * **Carga Dinámica (Legacy)**: En `app.py`, la clase `EntryAPI` actúa como un despachador dinámico genérico para solicitudes HTTP POST y GET. Recibe los parámetros `module_name`, `class_name` y `method_name` desde la URL, importa dinámicamente el controlador correspondiente en `controller/` y ejecuta el método solicitado.
  * **Rutas Modernas (V2 API)**: Utiliza `routes.router.init_routes` para inicializar Blueprints estándar en Flask para módulos modernos (`controller.transaccion`, `controller.reportes`, `controller.SerieManager`).
  * **JWT**: Valida tokens de acceso descodificados a través de la clave secreta `AUTH_SECRET_KEY`.

---

### 2.2. `api/`
* **Responsabilidad**: Contiene los clientes HTTP que interactúan con APIs de mercado y proveedores de datos financieros externos.
* **Archivos Clave**:
  * [Alphavantage.py](file:///home/alone/projects/bagholdercuy/api/Alphavantage.py): Cliente de datos históricos y cotizaciones de Alphavantage.
  * [Tiingo.py](file:///home/alone/projects/bagholdercuy/api/Tiingo.py): Integración con Tiingo API.
  * [fmp.py](file:///home/alone/projects/bagholdercuy/api/fmp.py): Cliente para Financial Modeling Prep.
  * [iexcloud.py](file:///home/alone/projects/bagholdercuy/api/iexcloud.py): Integración con IEX Cloud.
  * [marketdata.py](file:///home/alone/projects/bagholdercuy/api/marketdata.py) & [marketstack.py](file:///home/alone/projects/bagholdercuy/api/marketstack.py): Lectores de cotizaciones bursátiles.
  * [massive.py](file:///home/alone/projects/bagholdercuy/api/massive.py): Consumo de datos masivos.

---

### 2.3. `boot/`
* **Responsabilidad**: Contiene los scripts de inicialización que deben correr durante el arranque del contexto de la aplicación.
* **Archivos Clave**:
  * [loader.py](file:///home/alone/projects/bagholdercuy/boot/loader.py): Inicializa las constantes del sistema importando y ejecutando el paquete `constants`.

---

### 2.4. `common/`
* **Responsabilidad**: Componentes de soporte transversales (cross-cutting concerns) y utilidades compartidas.
* **Archivos Clave**:
  * [AppException.py](file:///home/alone/projects/bagholdercuy/common/AppException.py): Excepción personalizada para errores controlados de negocio.
  * [Database.py](file:///home/alone/projects/bagholdercuy/common/Database.py): Wrapper de conexión y manejo manual de transacciones SQL nativas.
  * [Response.py](file:///home/alone/projects/bagholdercuy/common/Response.py): Formateador estandarizado de respuestas API JSON (`success`, `data`, `msg`, `code`).
  * [logger.py](file:///home/alone/projects/bagholdercuy/common/logger.py): Configuración centralizada de logging para el sistema.
  * [auth.py](file:///home/alone/projects/bagholdercuy/common/auth.py): Utilidades de firma y chequeo de tokens JWT.
  * [converter.py](file:///home/alone/projects/bagholdercuy/common/converter.py) & [Formatter.py](file:///home/alone/projects/bagholdercuy/common/Formatter.py): Conversión de tipos y formateo de datos.

---

### 2.5. `config/`
* **Responsabilidad**: Gestión de la configuración global de la aplicación.
* **Archivos Clave**:
  * [config.py](file:///home/alone/projects/bagholdercuy/config/config.py): Construye la URI de conexión de SQLAlchemy MySQL a partir de variables de entorno (`.env`) y expone las clases `Config`, `DevelopmentConfig` y `ProductionConfig`.
  * [extensions.py](file:///home/alone/projects/bagholdercuy/config/extensions.py): Instancia central del ORM `db = SQLAlchemy()`.
  * [constants.py](file:///home/alone/projects/bagholdercuy/config/constants.py): Constantes de configuración globales del servidor backend.

---

### 2.6. `constants/`
* **Responsabilidad**: Define constantes y enums lógicos que mapean a catálogos en la base de datos o estados fijos del negocio.
* **Archivos Clave**:
  * [__init__.py](file:///home/alone/projects/bagholdercuy/constants/__init__.py): Mecanismo de registro automático (`register_init`) para cargar catálogos dinámicamente al iniciar.
  * [tipo_transaccion.py](file:///home/alone/projects/bagholdercuy/constants/tipo_transaccion.py): Constantes para Compras (`C`) y Ventas (`V`).
  * [instrumento_financiero.py](file:///home/alone/projects/bagholdercuy/constants/instrumento_financiero.py): Tipos de activos (Acciones, Opciones Financieras, Efectivo).
  * [evento_origen.py](file:///home/alone/projects/bagholdercuy/constants/evento_origen.py): Orígenes de datos (IBKR, Manual, Dividendos).
  * [indicador_apcierre.py](file:///home/alone/projects/bagholdercuy/constants/indicador_apcierre.py): Indicador de Apertura (`A`), Cierre (`C`), o Ninguno (`N`).

---

### 2.7. `controller/`
* **Responsabilidad**: Controladores controladores de la API. Capturan las peticiones HTTP, validan tokens JWT heredando de `Base`, formatean respuestas y delegan la lógica pesada a `service` o `reader`.
* **Archivos Clave**:
  * [base.py](file:///home/alone/projects/bagholdercuy/controller/base.py): Clase base `Base` que exige `AUTH_REQUIRED = True` y realiza la validación automática de tokens JWT de sesión.
  * [transaccion.py](file:///home/alone/projects/bagholdercuy/controller/transaccion.py): Endpoint del libro diario de transacciones bursátiles.
  * [fundsmanager.py](file:///home/alone/projects/bagholdercuy/controller/fundsmanager.py): Controlador para ingresos/retiros de efectivo y conversión de divisas.
  * [holdings.py](file:///home/alone/projects/bagholdercuy/controller/holdings.py): Gestión de portafolio actual de activos abiertos.
  * [contrato_opcion.py](file:///home/alone/projects/bagholdercuy/controller/contrato_opcion.py): Control de opciones financieras.
  * [reportes.py](file:///home/alone/projects/bagholdercuy/controller/reportes.py): Consultas agregadas de rendimiento y gráficos históricos.

---

### 2.8. `domain/`
* **Responsabilidad**: Contiene objetos de valor o lógica pura de dominio, sin acoplamiento a base de datos o dependencias externas.
* **Archivos Clave**:
  * [contratoopcion.py](file:///home/alone/projects/bagholdercuy/domain/contratoopcion.py): Estructura lógica y cálculo de propiedades del contrato de opción financiero.
  * [anyo.py](file:///home/alone/projects/bagholdercuy/domain/anyo.py), [mes.py](file:///home/alone/projects/bagholdercuy/domain/mes.py), [semana.py](file:///home/alone/projects/bagholdercuy/domain/semana.py), [fecha.py](file:///home/alone/projects/bagholdercuy/domain/fecha.py): Entidades para estructurar períodos calendarios temporales y rentabilidades agrupadas en el dominio.

---

### 2.9. `model/`
* **Responsabilidad**: Declaración de los modelos ORM de SQLAlchemy que representan las tablas físicas de la base de datos MySQL. Adicionalmente, posee lógica de manipulación interna de datos.
* **Archivos Clave**:
  * [transaccion.py](file:///home/alone/projects/bagholdercuy/model/transaccion.py): Mapeo de `tb_transaccion` (Libro de transacciones).
  * [transaccion_saldo.py](file:///home/alone/projects/bagholdercuy/model/transaccion_saldo.py): Mapeo de `tb_transaccion_saldo` (Lotes vivos / inventario de activos).
  * [movimiento_saldo.py](file:///home/alone/projects/bagholdercuy/model/movimiento_saldo.py): Mapeo de `tb_movimiento_saldo` (Historial de aplicaciones FIFO y P&L realizado).
  * [cuenta.py](file:///home/alone/projects/bagholdercuy/model/cuenta.py): Modelo de cuenta corriente/bursátil de usuario.
  * **Subpaquete `model/bussiness/`**: Lógica transaccional aplicada y procesos contables.
    * [transaccion.py](file:///home/alone/projects/bagholdercuy/model/bussiness/transaccion.py): Gestor principal del flujo de emparejamiento de transacciones.
    * [deposito_handler.py](file:///home/alone/projects/bagholdercuy/model/bussiness/deposito_handler.py), [retiro.py](file:///home/alone/projects/bagholdercuy/model/bussiness/retiro.py): Lógica contable de entradas/salidas de efectivo.
    * [mov_fondos.py](file:///home/alone/projects/bagholdercuy/model/bussiness/mov_fondos.py): Flujos históricos de fondos en la cuenta.

---

### 2.10. `parser/`
* **Responsabilidad**: Capa encargada de mapear o traducir las entidades del sistema y respuestas complejas a diccionarios planos estructurados (JSON DTOs) consumibles por el cliente Vue.js.
* **Archivos Clave**:
  * [base.py](file:///home/alone/projects/bagholdercuy/parser/base.py): Base para mapeadores automáticos.
  * [operacion.py](file:///home/alone/projects/bagholdercuy/parser/operacion.py): Parser de estructuras de trading complejas.
  * [cuenta.py](file:///home/alone/projects/bagholdercuy/parser/cuenta.py), [usuario.py](file:///home/alone/projects/bagholdercuy/parser/usuario.py): Formateadores de entidades administrativas.

---

### 2.11. `processor/`
* **Responsabilidad**: Capa de procesamiento numérico y de agregación. Ejecuta cálculos fuera de la base de datos que requieren transformaciones secuenciales o agregaciones matemáticas complejas.
* **Deprecado**: Para nuevos desarrollos no usar.
* **Archivos Clave**:
  * [variaciondiaria.py](file:///home/alone/projects/bagholdercuy/processor/variaciondiaria.py), [variacionsemanal.py](file:///home/alone/projects/bagholdercuy/processor/variacionsemanal.py), [variacionmensual.py](file:///home/alone/projects/bagholdercuy/processor/variacionmensual.py): Procesadores de cálculo de rendimiento acumulado y variación porcentual temporal.
  * [transaccion.py](file:///home/alone/projects/bagholdercuy/processor/transaccion.py): Motor para el recálculo general de transacciones.

---

### 2.12. `proxy/`
* **Responsabilidad**: Proxies de conexión o comunicación con servicios externos secundarios o disparadores de alertas configuradas.
* **Archivos Clave**:
  * [configuracionalerta.py](file:///home/alone/projects/bagholdercuy/proxy/configuracionalerta.py): Proxificación de disparadores de alertas de mercado.

---

### 2.13. `reader/`
* **Responsabilidad**: Capa de acceso a datos de solo lectura (Read-Only queries). Implementa el patrón CQRS abstrayendo las consultas de SQLAlchemy del resto del sistema. **Regla general**: Ningún archivo en `reader/` debe modificar (`INSERT`, `UPDATE`, `DELETE`) registros en la base de datos.
* **Archivos Clave**:
  * [transaccion.py](file:///home/alone/projects/bagholdercuy/reader/transaccion.py): Centraliza consultas del libro diario, cálculos de rentabilidades históricas agregadas anuales/mensuales/diarias y posiciones abiertas agrupadas.
  * [operacion.py](file:///home/alone/projects/bagholdercuy/reader/operacion.py): Consultas optimizadas de trades.
  * [posicion.py](file:///home/alone/projects/bagholdercuy/reader/posicion.py): Estado actual del portafolio.
  * [seriediaria.py](file:///home/alone/projects/bagholdercuy/reader/seriediaria.py), [seriemensual.py](file:///home/alone/projects/bagholdercuy/reader/seriemensual.py): Lectores de series históricas de precios de activos.

---

### 2.14. `routes/`
* **Responsabilidad**: Define el enrutamiento de Flask para los controladores API modernos (API V2).
* **Archivos Clave**:
  * [router.py](file:///home/alone/projects/bagholdercuy/routes/router.py): Registra las rutas asociándolas a los controladores habilitados (`controller.transaccion`, `controller.reportes`, `controller.SerieManager`) usando el prefijo `/{BAGHOLDER_APPNAME}/api/v2`.

---

### 2.15. `schemas/`
* **Responsabilidad**: Define esquemas de validación y de deserialización/serialización (ej. Marshmallow / Pydantic) para garantizar la sanidad estructural de las peticiones que recibe la API.
* **Archivos Clave**:
  * [alphavantage_schema.py](file:///home/alone/projects/bagholdercuy/schemas/alphavantage_schema.py): Esquemas para los payloads de cotizaciones.
  * [posicion_schema.py](file:///home/alone/projects/bagholdercuy/schemas/posicion_schema.py), [orden_schema.py](file:///home/alone/projects/bagholdercuy/schemas/orden_schema.py): Validación de portafolio y órdenes pendientes.

---

### 2.16. `service/`
* **Responsabilidad**: Capa de servicios y casos de uso del negocio. Orquesta la interacción de lectores (`reader`), cálculos (`processor`) y modelos de negocio para ejecutar flujos complejos de escritura en base de datos.
* **Archivos Clave**:
  * [transaccion.py](file:///home/alone/projects/bagholdercuy/service/transaccion.py): Implementa `TransaccionService` y las clases `CompraGeneric` / `VentaGeneric`. Es el núcleo del algoritmo FIFO:
    * **Compra**: Busca lotes negativos previos (cortos) para cerrarlos, calcula el P&L realizado e inserta en `tb_movimiento_saldo`. Si sobra inventario, crea un lote positivo en `tb_transaccion_saldo`.
    * **Venta**: Busca lotes positivos previos (compras) en orden cronológico, los consume aplicando FIFO, genera la ganancia/pérdida realizada en `tb_movimiento_saldo` y crea lotes negativos si es venta en corto.
  * [serie_service.py](file:///home/alone/projects/bagholdercuy/service/serie_service.py): Mantenimiento de series temporales de precios.
  * [stocksplit.py](file:///home/alone/projects/bagholdercuy/service/stocksplit.py): Proceso de aplicación de splits de acciones en el portafolio, ajustando la cantidad e importe unitario de las transacciones históricas conservando la integridad de P&L.

---

### 2.17. `structure/`
* **Responsabilidad**: Contenedores de datos estructurados (tipo Data Transfer Objects o estructuras internas) usados para empaquetar variables que viajan entre los servicios del backend.
* **Archivos Clave**:
  * [series_structure.py](file:///home/alone/projects/bagholdercuy/structure/series_structure.py) & [inputfiles.py](file:///home/alone/projects/bagholdercuy/structure/inputfiles.py).

---

### 2.18. `utils/`
* **Responsabilidad**: Módulos utilitarios generales no relacionados directamente con la lógica financiera sino con el soporte operativo (manipulación de fechas, cálculos lógicos de calendario).
* **Archivos Clave**:
  * [calendario.py](file:///home/alone/projects/bagholdercuy/utils/calendario.py): Cálculos de semanas bursátiles y días hábiles.

---

## 3. Estructura del Frontend (`view/client`)
El frontend es una Single Page Application (SPA) construida en JavaScript utilizando **Vue 2**, integrada con la suite de componentes visuales **Quasar Framework (v1)**.

### Estructura de Directorios Clave (`view/client/src/`)
* **`main.js`**: Archivo de entrada de Vue. Instancia los plugins Quasar, Vue Router y Vuex.
* **`routes.js`**: Definición central de rutas de la aplicación ([routes.js](file:///home/alone/projects/bagholdercuy/view/client/src/routes.js)). Posee un guard (`router.beforeEach`) que valida la expiración del token JWT mediante una llamada al backend (`/auth/LoginController/validar_token`) antes de permitir el acceso a las vistas principales.
* **`store/`**: Estado global manejado con Vuex.
* **`api/`**: Contiene la abstracción de llamadas AJAX (usando Axios) al backend de Flask.
* **`components/`**: Componentes reutilizables clasificados por contexto de negocio (Holdings, Funds, Split, Serie, Informes).
* **`pages/`**: Páginas principales de vistas compuestas. Destacan:
  * `ibkr-configuration/`: Paneles para configurar el endpoint de Interactive Brokers y mapear contratos financieros sincronizados.

---

## 4. Patrones de Diseño Clave a Recordar
Al proponer cambios de código o crear nuevos módulos para este sistema, respeta los siguientes principios arquitectónicos:

1. **Patrón FIFO y Lotes en BD**:
   * Las transacciones físicas se registran en `tb_transaccion`.
   * El inventario remanente de transacciones abiertas (lotes FIFO activos) se almacena en `tb_transaccion_saldo` (`ctd_saldo` e `imp_saldo`).
   * Los neteos históricos (aplicaciones FIFO y ganancias realizadas) se registran en `tb_movimiento_saldo`.
   * **Siempre** utiliza `TransaccionService` para registrar operaciones de compra o venta para asegurar la integridad de este algoritmo.

2. **Capa Reader vs Service (CQRS)**:
   * Si la operación es **lectura** (gráfico, reportes, listado), crea la query en un método dentro del paquete `reader/` correspondiente y devuélvelo en el controller.
   * Si la operación es **escritura** (inserción, actualización, lógica de negocio compleja), impleméntalo a través de un servicio en `service/` o un handler de negocio en `model/bussiness/`.

3. **Formateo y Validación**:
   * Los datos crudos recibidos desde la request HTTP deben ser validados por un esquema en `schemas/`.
   * Los objetos del ORM devueltos al cliente deben ser estructurados por un transformador en `parser/` para homogeneizar tipos de datos, fechas y números con decimales.

---
