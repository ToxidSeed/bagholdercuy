# Lineamientos de Nomenclatura, Arquitectura y Entornos

Este documento define las reglas estándar para nombrar, organizar archivos y gestionar la configuración en el proyecto, asegurando escalabilidad, modularidad y seguridad.

---

## 1. Estructura de Carpetas (Arquitectura)

Nuestra arquitectura se basa en el principio de **Colocación (Colocation)**: el archivo debe vivir lo más cerca posible de los componentes que lo van a usar.

### Jerarquía de Módulo o Característica (Recomendado)
Agrupa los archivos por funcionalidad o pantalla, no por tipo técnico.
* **Carpetas:** Deben nombrarse estrictamente en **`kebab-case`** (todo en minúsculas y separado por guiones, ej. `panel-control/`). Esto evita bugs de compilación entre sistemas operativos (Windows vs Linux) y hace match automático con las URLs.
* **Archivos de estado (`.js`):** Deben vivir exactamente en la misma carpeta que agrupa a los componentes que lo consumen.
* **Ventaja:** Si se elimina una característica, al borrar su carpeta nos llevamos sus vistas, componentes y su estado asociado, evitando código "zombie".

### Jerarquía Global (`src/global/` o `src/store/`)
* **Uso estricto:** Solo para información transversal a toda la aplicación (ej. permisos del usuario logueado).

---

## 2. Nomenclatura de Archivos JavaScript

### Archivos de Estado Centralizado (`Vue.observable`)
Creamos un solo archivo que represente el "estado" de esa pantalla o módulo.
* **Convención:** **`camelCase`** con sufijo `State` o prefijo `estado`.
* **Ejemplos válidos:** `dashboardState.js`, `estadoFiltros.js`.
* **Lo que NO va aquí:** Variables puramente visuales que solo le importan a un componente (ej. el texto de un input antes de hacer clic en buscar). Eso se queda en el `data()` del componente.

### Archivos de Utilidades Puras
* **Convención:** **`camelCase`**.
* **Ejemplos válidos:** `dateFormatter.js`, `calculadoraFinanciera.js`.

### Composables (Vue 2.7 o Plugin Composition API)
* **Convención:** **`camelCase`** empezando estrictamente con el prefijo `use`.
* **Ejemplo válido:** `useTableData.js`.

---

## 3. Nomenclatura de Componentes (`.vue`)

Utilizaremos el estándar de **`PascalCase`**, dividiendo responsabilidades según el flujo de datos unidireccional.

| Tipo de Componente | Convención | Responsabilidad | Ejemplo |
| :--- | :--- | :--- | :--- |
| **Páginas (Smart)** | Prefijo `Pagina` o sufijo `View`. | Director de orquesta. Hace las llamadas a la API y pasa datos hacia abajo mediante props. | `PaginaPrincipal.vue` |
| **Componentes (Dumb)** | Nombre descriptivo de su interfaz. | Interfaz gráfica. Reciben datos (props) y emiten eventos hacia arriba. | `FilterTable.vue` |

---

## 4. Gestión de Variables de Entorno y Configuración

Aplicaremos la arquitectura donde el código dicta *cómo* funciona la app, pero la infraestructura dicta *con qué* se conecta.

### El Principio del Simulador Local
* Los archivos `.env` (como