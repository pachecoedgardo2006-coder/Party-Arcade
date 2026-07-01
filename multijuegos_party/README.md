# Party Arcade Hub — Compendio de Videojuegos Multijugador Local

¡Bienvenido al **Party Arcade Hub**! Esta plataforma es una solución robusta y altamente escalable diseñada en Python y **Pygame** para actuar como un "Launcher" o "Lobby Central" de minijuegos arcade. El objetivo principal es permitir el juego simultáneo entre amigos compartiendo el mismo dispositivo (Couch Co-Op / Versus) de forma fluida y óptima.

Este proyecto surge como la evolución y refactorización estructural de un prototipo monolítico originalmente contenido en `script.py` (un juego de carrera de gravedad inversa). Para dar soporte a un ecosistema planeado de **7 modos de juego distintos**, se ha migrado a una arquitectura basada en el **Patrón Estado (State Pattern)**, el **Principio de Responsabilidad Única (SRP)** y una separación estricta de componentes.

---

## 🚀 Tecnologías y Estándares

* **Lenguaje:** Python 3.10+
* **Motor Gráfico:** Pygame 2.x
* **Entorno Recomendado:** Linux Ubuntu / Visual Studio Code
* **Estilo de Código:** Cumplimiento estricto de **PEP 8** (Constantes en `UPPER_CASE`, funciones/variables en `snake_case` y clases en `PascalCase`).

---

## 📂 Arquitectura del Proyecto (Diseño de Carpetas)

La estructura está organizada jerárquicamente para garantizar una modularización absoluta. Cada minijuego divide sus responsabilidades aislando el dominio (entidades) de su núcleo lógico y del orquestador gráfico:

```text
multijuegos_party/
│
├── main.py                     # Punto de entrada único del ciclo de vida de la aplicación
├── README.md                   # Documentación técnica del ecosistema
│
├── config/                     # Configuraciones e inicializaciones globales compartidas
│   ├── __init__.py
│   └── settings.py             # Dimensiones de ventana, FPS, paletas de colores y mapeo de controles
│
├── assets/                     # Repositorio centralizado de recursos multimedia estáticos
│   ├── audio/                  # Efectos sonoros (SFX) y bandas sonoras (.mp3, .wav)
│   ├── fonts/                  # Fuentes tipográficas vectoriales (.ttf)
│   └── sprites/                # Spritesheets, interfaces y elementos visuales (.png)
│
└── src/                        # Código fuente del ecosistema de software
    ├── __init__.py
    │
    ├── engine/                 # Núcleo operativo del motor del Launcher
    │   ├── __init__.py
    │   └── manager.py          # Clase constructor del bucle principal y swicheo de pantallas
    │
    ├── ui/                     # Componentes visuales genéricos y compartidos
    │   ├── __init__.py
    │   └── components.py       # Botones, selectores y contenedores estilizados para los menús
    │
    ├── scenes/                 # Pantallas de flujo global del sistema
    │   ├── __init__.py
    │   ├── base_scene.py       # Interfaz o clase abstracta para el polimorfismo de pantallas
    │   ├── main_menu.py        # Menú principal de bienvenida de la aplicación
    │   ├── game_select.py      # Panel de selección o "Lobby" para elegir entre los modos
    │   ├── tournament_score.py # 🏆 Tabla de posiciones intermedia del torneo por puntos
    │   └── final_results.py    # 🎉 Pantalla de resultados finales del torneo
    │
    └── modes/                  # 🚀 CONTENEDOR EXCLUSIVO PARA LOS MODOS DE JUEGO
        ├── __init__.py
        ├── base_mode.py        # Clase base que normaliza los métodos que cada juego debe implementar
        │
        ├── gravity_runner/      # 🎮 MODO 1: Carrera de Gravedad Inversa (Multijugador)
        │   ├── __init__.py
        │   ├── runner_game.py   # Orquestador principal del modo (conecta lógica y render)
        │   ├── core/            # 🧠 Lógica pura y físicas
        │   │   ├── __init__.py
        │   │   ├── particle_sys.py # Sistema de emisión de partículas para efectos visuales
        │   │   └── physics.py       # Motor de colisiones y aceleración progresiva
        │   └── domain/          # 👥 Entidades del juego
        │       ├── __init__.py
        │       ├── constants.py
        │       ├── mapa_data.py     # 🗺️ Almacenamiento y estructura de datos de los mapas
        │       ├── map_elements.py  # Definición y renderizado de los componentes del mapa
        │       ├── obstacle.py      # Entidad obstáculo
        │       └── player.py        # Entidad jugador[cite: 1]
        │
        ├── battle_snake/       # 🐍 MODO 2: Versus Snake Modularizado[cite: 1]
        │   ├── __init__.py
        │   ├── battle_snake.py # Orquestador principal del modo (interfaz con Pygame)[cite: 1]
        │   ├── core/            # 🧠 Mecánicas puras e independientes de renderizado[cite: 1]
        │   │   ├── __init__.py
        │   │   └── logic.py     # Lógica matemática: colisiones en grilla y validación de comida[cite: 1]
        │   └── domain/          # 👥 Entidades del juego (Modelado de datos)[cite: 1]
        │       ├── __init__.py
        │       ├── constants.py # Dimensiones de grilla, ticks, controles y paleta cromática local[cite: 1]
        │       ├── food.py      # Entidad comida y su algoritmo de reubicación aleatoria segura[cite: 1]
        │       └── snake.py     # Entidad serpiente (gestión de cuerpo, dirección e ID de jugador)[cite: 1]
        │
        ├── memory_grid/        # 🧠 MODO 3: Memory Grid (Tablero de Pares por Turnos)[cite: 1]
        │   ├── __init__.py
        │   ├── memory_game.py  # Orquestador principal del modo (interfaz visual y clics del mouse)[cite: 1]
        │   ├── core/            # 🧠 Mecánicas puras y control lógico de turnos[cite: 1]
        │   │   ├── __init__.py
        │   │   └── logic.py     # Lógica pura: validación de pares, mezcla aleatoria y flujo de puntaje[cite: 1]
        │   └── domain/          # 👥 Entidades del juego (Modelado de datos de la grilla)[cite: 1]
        │       ├── __init__.py
        │       ├── card.py      # Entidad tarjeta (estado atómico de visibilidad y colisiones)[cite: 1]
        │       └── constants.py # Parámetros locales: grilla 5x10, colores Neón locales y timers[cite: 1]
        │
        ├── retro_racing/       # 🏎️ MODO 4: Retro Racing (Carreras Arcade 2D)
        │   ├── __init__.py
        │   ├── racing_game.py  # Orquestador principal de la escena de carreras
        │   ├── core/            # 🧠 Núcleo de físicas de conducción
        │   │   ├── __init__.py
        │   │   └── physics.py   # Gestión de velocidad, aceleración y colisiones de los vehículos
        │   └── domain/          # 👥 Entidades del entorno de carreras
        │       ├── __init__.py
        │       ├── car.py       # Entidad coche (control de dirección, posición y render)
        │       └── constants.py # Constantes locales del juego de carreras
        │
        └── sumo_combat/                 # 🚀 MODO 5: Pelea de Sumos Top-Down (Versus)[cite: 1]
            ├── __init__.py
            ├── sumo_game.py             # Orquestador principal (conecta bucle, eventos y render)[cite: 1]
            │
            ├── core/                    # 🧠 Mecánicas puras y físicas vectoriales[cite: 1]
            │   ├── __init__.py
            │   └── physics.py           # Físicas de empuje, fricción, rebote elástico y límites de la arena[cite: 1]
            │
            └── domain/                  # 👥 Entidades y datos locales[cite: 1]
                ├── __init__.py
                ├── constants.py         # Dimensiones de la arena, masas, fuerzas y colores locales[cite: 1]
                └── wrestler.py          # Entidad del luchador (posición, velocidad, vector dirección, ID)[cite: 1]
```

- --

## 🛠️ Desglose Funcional de Módulos Centrales

### 1. Punto de Entrada (`main.py`)

Inicializa la ejecución del programa. Su único propósito es instanciar la clase contenedora de la aplicación (`GameManager`) localizada en `src.engine.manager` y lanzar el bucle principal. Se mantiene libre de lógica de juego.

### 2. Configuración Compartida (`config/settings.py`)

Almacena constantes globales del sistema como las dimensiones fijas de la ventana (`**ANCHO** = 800`, `**ALTO** = 600`), tasa de refresco (`**FPS** = 60`) y paletas cromáticas estéticas (Neón Cyberpunk). Adicionalmente, centraliza el **mapeo de entradas de teclado** para múltiples jugadores locales (ej. Controles de Jugador 1 con **WASD**/Espacio y Jugador 2 con Flechas/Enter), garantizando que todos los modos compartan la misma abstracción de periféricos.

### 3. El Motor del Launcher (`src/engine/manager.py`)

Maneja el bucle `while` nativo de Pygame, gestiona la ventana física y despacha eventos globales como el cierre abrupto de la aplicación (`pygame.**QUIT**`). Contiene una referencia dinámica a la escena activa actual, permitiendo transiciones suaves entre el menú principal, la pantalla de selección y el juego en ejecución.

### 4. Sistema de Escenas Globales (`src/scenes/`)

* **`base_scene.py`**: Define un contrato rígido mediante métodos virtuales abstractos (`manejar_eventos()`, `actualizar()`, `dibujar()`). Esto asegura que el `GameManager` pueda tratar a cualquier pantalla de forma polimórfica sin conocer sus particularidades internas.

* **`main_menu.py` y `game_select.py**`: Gestionan las pantallas iniciales del Hub utilizando los componentes interactivos definidos en `src/ui/components.py`. El selector de juego lee de forma dinámica la lista de módulos disponibles en la carpeta `modes/`.

* **`tournament_score.py` y `final_results.py**`: Administran el ciclo competitivo general mediante un sistema de torneos locales, calculando las puntuaciones y victorias globales acumuladas de los jugadores para presentarlas al terminar los encuentros.

- --

## 🛠️ Desglose Técnico de los Modos Activos

### 🎮 Modo 1: Gravity Runner (`src/modes/gravity_runner/`)

Un juego vertiginoso de carrera infinita y esquive de obstáculos con mecánicas de gravedad inversa.

* **`core/physics.py`**: Gobierna el motor de colisiones y la aceleración progresiva de la velocidad del juego.

* **`domain/mapa_data.py` & `map_elements.py**`: Abstraen la configuración estructural de las plataformas mediante matrices lógicas independientes, permitiendo la construcción organizada y lectura de las diferentes superficies del nivel.
* **`domain/player.py` & `obstacle.py**`: Modelan los atributos del jugador (velocidad, estado de salto) y los patrones dinámicos de los obstáculos. Integra un gestor de partículas (`particle_sys.py`) para renderizar efectos dinámicos en los desplazamientos.

### 🐍 Modo 2: Versus Snake (`src/modes/battle_snake/`)

El mítico arcade de la serpiente reinventado en una intensa arena competitiva local para dos jugadores simultáneos.

* **`domain/snake.py`**: Clase entidad totalmente parametrizada por `jugador_id`. Controla de forma aislada el crecimiento del cuerpo y restringe los giros no permitidos (evitando autodestrucciones por contramarcha física).

* **`domain/food.py`**: Implementa lógica inteligente de reubicación mediante `food.reubicar(cuerpos_totales)`, asegurando de forma predictiva que el alimento jamás aparezca debajo de ninguno de los jugadores.

* **`core/logic.py` (SnakeLogic)**: Concentra las reglas de negocio puras del juego. Realiza el chequeo de colisiones cruzadas (si una serpiente choca contra sí misma o contra el cuerpo del rival) de manera estricta y agnóstica a la librería gráfica.

* **`battle_snake.py`**: Actúa como el controlador principal. Capta de forma diferenciada las entradas de control (**Jugador 1: WASD** y **Jugador 2: Flechas de dirección**) y despacha de manera unificada los estados de la partida (`JUGANDO` / `GAME_OVER`).

### 🧠 Modo 3: Memory Grid (`src/modes/memory_grid/`)

Un desafío táctico de memoria visual y concentración por turnos, donde dos jugadores compiten en una grilla de 5 × 10 por encontrar la mayor cantidad de parejas de iconos.

* **`domain/card.py`**: Modela el comportamiento y el estado individual de cada una de las 50 casillas del tablero (si está oculta, volteada temporalmente o resuelta con éxito). Expone métodos matemáticos para mapear su geometría con los límites del puntero físico del ratón.

* **`domain/constants.py`**: Centraliza de manera estricta las filas, columnas, dimensiones de diseño neón y los intervalos de tiempo en milisegundos (el temporizador inicial de memorización de 4 segundos y el retraso de bloqueo por error).

* **`core/logic.py` (MemoryLogic)**: Concentra las reglas de negocio e integridad del minijuego. Ejecuta el algoritmo de mezcla aleatoria de los 25 pares de identificadores, valida si las dos tarjetas seleccionadas coinciden y gestiona de manera encapsulada el flujo estricto del cambio de turnos (P1 vs P2) según los aciertos.

* **`memory_game.py`**: Actúa como la escena operativa principal acoplada al Hub. Controla la captura de coordenadas del ratón, dibuja el tablero centrado dinámicamente según la resolución global e implementa la máquina de estados interna (`MEMORIZANDO`, `JUGANDO`, `BLOQUEADO`, `GAME_OVER`) que congela clics ilegítimos o maliciosos durante los procesos de animación.

### 🏎️ Modo 4: Retro Racing (`src/modes/retro_racing/`)

Un veloz videojuego competitivo de carreras en perspectiva cenital (top-down) con un estilo retro enfocado en los reflejos y el control de tracción.

* **`domain/car.py`**: Define las entidades mecánicas individuales de los vehículos, computando los parámetros de aceleración, frenado y control direccional asociados a cada conductor.
* **`core/physics.py`**: Rige los cálculos del entorno de carrera, determinando la desaceleración o pérdida de adherencia táctica cuando las llantas interactúan con los límites de la carretera o zonas de césped.
* **`racing_game.py`**: Funciona como el orquestador principal del nivel, coordinando el renderizado de la autopista con scroll asíncrono y mapeando simultáneamente los controles de los competidores locales.

### 🤼 Modo 5: Sumo Combat (`src/modes/sumo_combat/`)

Un intenso enfrentamiento arcade de empuje e inercias con vista cenital (top-down), donde dos luchadores compiten dentro de una arena circular de peligro por ver quién logra expulsar a su rival del ring en partidas al mejor de 3 puntos.

* **`domain/wrestler.py`**: Modela de forma atómica las propiedades físicas individuales de cada luchador (posición, vectores de velocidad e ID del jugador). Gestiona de manera aislada la captura de periféricos en tiempo real aplicando aceleraciones vectoriales normalizadas y coeficientes de fricción dinámica para evitar desplazamientos infinitos.

* **`domain/constants.py`**: Centraliza estrictamente las dimensiones del ring, los radios de colisión de las entidades, los multiplicadores de fuerza de empuje ajustados, el límite de puntuación para la victoria y el mapeo de hardware dual (Jugador 1: WASD | Jugador 2: Flechas de dirección).

* **`core/physics.py` (SumoPhysics)**: Concentra el motor matemático y físico puro del minijuego de forma agnóstica al renderizado. Implementa algoritmos de separación física inmediata ante colisiones para erradicar bugs de interpenetración y resuelve la transferencia de cantidad de movimiento elástica mediante un multiplicador de impacto elevado que eyecta a los jugadores en colisiones de alta velocidad.

* **`sumo_game.py`**: Actúa como el orquestador y controlador principal acoplado al Launcher. Maneja el ciclo de vida de la escena, la distribución de puntos por prioridad secuencial en los límites radiales de la arena circular y despliega una máquina de estados interna con fases de congelamiento y preparación para garantizar un inicio limpio y justo en cada ronda.

- --

## 🧠 Leyes y Buenas Prácticas Aplicadas

- **Bajo Acoplamiento y Alta Cohesión:** El motor del launcher no conoce las reglas, mecánicas ni sistemas de puntuación de los minijuegos. Esto evita dependencias cruzadas destructivas.

- **Erradicación de Estados Globales Mutables:** Se elimina completamente el uso de la palabra clave `global` presente en el prototipo original. El estado actual del juego, las puntuaciones y los récords se encapsulan como atributos de instancia dentro de sus respectivas clases controladoras.

- **Principio Abierto/Cerrado (**OCP**):** El sistema está **abierto para la extensión pero cerrado para la modificación**. Desarrollar nuevos modos de juego es tan simple como empaquetar nuevas carpetas bajo `src/modes/` siguiendo la interfaz de `base_mode.py`, sin necesidad de alterar una sola línea de código en el Launcher principal.

- **Inyección y Gestión Eficiente de Recursos:** Las fuentes y los assets comunes se administran centralizadamente para evitar fugas de memoria por recargas reiteradas en el bucle principal.

```

```