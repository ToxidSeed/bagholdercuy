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
* Los archivos `.env` (como `.env.development` o `.env.local`) sirven única y exclusivamente para **simular el entorno de despliegue en la computadora local** de cada desarrollador.
* **NUNCA** se deben subir a Git archivos con variables reales (ej. `.env.production`). Deben estar declarados en el `.gitignore`.

### El Archivo de Contrato (`.env.example`)
* **SIEMPRE** debe existir un archivo `.env.example` en la raíz subido al repositorio. 
* Actúa como una plantilla segura sin datos reales (ej. `VITE_API_URL=`) para que cualquier nuevo desarrollador sepa qué variables requiere el proyecto para funcionar.

### Despliegue y Producción
* Se prohíbe depender de un archivo `.env.production` físico en la computadora de un desarrollador para generar los builds de producción, ya que causa el síndrome de "en mi máquina funciona".
* Las variables reales de producción deben ser inyectadas **directamente por el pipeline de CI/CD** (ej. GitHub Actions mediante Secrets) o por el panel de la plataforma de hosting (Netlify/Vercel) al momento de ejecutar el comando de compilación (`npm run build` / `quasar build`).

### Constantes vs. Variables
* **Constantes de la App:** Reglas de negocio fijas (ej. `TIMEOUT = 30`, tamaño de paginación). Deben vivir en el código fuente (`.js`).
* **Variables de Entorno Puras:** Credenciales secretas (tokens) y URLs de dependencias externas. Pertenecen a la configuración del servidor y jamás tocan el código.

---

## 5. Reglas de Oro del Proyecto

1.  **Aislamiento del Estado:** El resto de la aplicación ni siquiera debe enterarse de que el estado de un módulo específico existe.
2.  **Mutaciones Estrictas:** El estado en un `Vue.observable` solo debe ser modificado por funciones (mutaciones) exportadas desde su mismo archivo. Cero mutaciones directas desde el componente.
3.  **Flujo Unidireccional:** Los eventos suben, los datos bajan (Props down, Events up). Los componentes "tontos" no llaman a la API.
4.  **Agnosticismo de Entorno:** El código fuente debe ser capaz de levantarse localmente sin fallar, delegando la configuración pesada al entorno que lo hospeda.


## 6. Clases e Instanciación (POO en JavaScript)

En nuestro ecosistema, las Clases actúan estrictamente como "moldes" para crear múltiples objetos independientes que requieran encapsular tanto sus propios datos (estado) como su propia lógica de negocio (métodos).

### Nomenclatura Estricta

| Elemento | Convención | Ejemplo |
| :--- | :--- | :--- |
| **Nombre de la Clase** | **`PascalCase`** (Sustantivo singular) | `class OperacionBursatil {}` |
| **Nombre del Archivo** | **`PascalCase`** | `OperacionBursatil.js` |
| **Instancia (Variable)** | **`camelCase`** | `const miOperacion = new OperacionBursatil()` |

### ¿Cuándo instanciar una Clase? (`new Clase()`)

**SÍ debes usar e instanciar una clase cuando:**
* Necesitas crear múltiples entidades independientes, donde cada una maneja su propio estado interno y ejecuta cálculos sobre sí misma.
* **Ejemplo Arquitectónico:** Si tienes una tabla con 50 operaciones distintas, cada fila debe ser instanciada (`new ContratoOpcion()`). Esto permite que el componente de Vue sea "tonto" y simplemente llame a los métodos de la instancia, delegando la lógica matemática al modelo: `{{ operacion.calcularRetorno(precioActual) }}`.

### ¿Cuándo NO usar una Clase? (Antipatrones)

Para mantener el rendimiento y la simplicidad, prohíbimos el uso de clases en los siguientes escenarios:

1. **Datos planos de API (DTOs):** Si el frontend recibe miles de registros de la base de datos que solo se van a dibujar en pantalla sin mutar ni requerir cálculos complejos, se deben mantener como objetos planos (`{}`). Iterar arreglos masivos solo para convertirlos en instancias de clase consume memoria innecesaria.
2. **Estado Global o Singletons:** Si solo existirá una instancia de los datos en toda la ejecución de la app (ej. el perfil del inversor, o el estado de un panel), **no se usan clases**. Se debe utilizar el patrón centralizado con `Vue.observable`.
3. **Colecciones de Utilidades:** No se deben crear clases vacías para agrupar funciones (ej. `class CalculadoraFinanciera`). Las utilidades puras (como fórmulas de interés compuesto o formateadores de fechas) deben exportarse como funciones sueltas desde un archivo `.js` estándar en `camelCase`.## 6. Clases e Instanciación (POO en JavaScript)

En nuestro ecosistema, las Clases actúan estrictamente como "moldes" para crear múltiples objetos independientes que requieran encapsular tanto sus propios datos (estado) como su propia lógica de negocio (métodos).

### Nomenclatura Estricta

| Elemento | Convención | Ejemplo |
| :--- | :--- | :--- |
| **Nombre de la Clase** | **`PascalCase`** (Sustantivo singular) | `class OperacionBursatil {}` |
| **Nombre del Archivo** | **`PascalCase`** | `OperacionBursatil.js` |
| **Instancia (Variable)** | **`camelCase`** | `const miOperacion = new OperacionBursatil()` |

### ¿Cuándo instanciar una Clase? (`new Clase()`)

**SÍ debes usar e instanciar una clase cuando:**
* Necesitas crear múltiples entidades independientes, donde cada una maneja su propio estado interno y ejecuta cálculos sobre sí misma.
* **Ejemplo Arquitectónico:** Si tienes una tabla con 50 operaciones distintas, cada fila debe ser instanciada (`new ContratoOpcion()`). Esto permite que el componente de Vue sea "tonto" y simplemente llame a los métodos de la instancia, delegando la lógica matemática al modelo: `{{ operacion.calcularRetorno(precioActual) }}`.

### ¿Cuándo NO usar una Clase? (Antipatrones)

Para mantener el rendimiento y la simplicidad, prohíbimos el uso de clases en los siguientes escenarios:

1. **Datos planos de API (DTOs):** Si el frontend recibe miles de registros de la base de datos que solo se van a dibujar en pantalla sin mutar ni requerir cálculos complejos, se deben mantener como objetos planos (`{}`). Iterar arreglos masivos solo para convertirlos en instancias de clase consume memoria innecesaria.
2. **Estado Global o Singletons:** Si solo existirá una instancia de los datos en toda la ejecución de la app (ej. el perfil del inversor, o el estado de un panel), **no se usan clases**. Se debe utilizar el patrón centralizado con `Vue.observable`.
3. **Colecciones de Utilidades:** No se deben crear clases vacías para agrupar funciones (ej. `class CalculadoraFinanciera`). Las utilidades puras (como fórmulas de interés compuesto o formateadores de fechas) deben exportarse como funciones sueltas desde un archivo `.js` estándar en `camelCase`.