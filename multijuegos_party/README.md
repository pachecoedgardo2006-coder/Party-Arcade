# Party Arcade Hub — Compendio de Videojuegos Multijugador Local

¡Bienvenido al **Party Arcade Hub**! Esta plataforma es una solución robusta y altamente escalable diseñada en Python y **Pygame** para actuar como un "Launcher" o "Lobby Central" de minijuegos arcade. El objetivo principal es permitir el juego simultáneo entre amigos compartiendo el mismo dispositivo (Couch Co-Op / Versus) de forma fluida y óptima.

Este proyecto surge como la evolución y refactorización estructural de un prototipo monolítico originalmente contenido en `script.py` (un juego de carrera de gravedad inversa). Para dar soporte a un ecosistema planeado de **7 modos de juego distintos**, se ha migrado a una arquitectura basada en el **Patrón Estado (State Pattern)**, el **Principio de Responsabilidad Única (SRP)** y una separación estricta de componentes.

---

## 🚀 Tecnologías y Estándares

*   **Lenguaje:** Python 3.10+
*   **Motor Gráfico:** Pygame 2.x
*   **Entorno Recomendado:** Linux Ubuntu / Visual Studio Code
*   **Estilo de Código:** Cumplimiento estricto de **PEP 8** (Constantes en `UPPER_CASE`, funciones/variables en `snake_case` y clases en `PascalCase`).

---

## 📂 Arquitectura del Proyecto (Diseño de Carpetas)

La estructura está organizada jerárquicamente para que el núcleo de la aplicación funcione de manera agnóstica a los juegos. Añadir un nuevo modo de juego no requiere modificar el lanzador ni las configuraciones básicas:

```text
multijuegos_party/
│
├── main.py                     # Punto de entrada único del ciclo de vida de la aplicación
├── README-v2.md                # Documentación técnica del ecosistema (Este archivo)
│
├── config/                     # Configuraciones e inicializaciones globales compartidas
│   ├── __init__.py
│   └── settings.py             # Dimensiones de ventana, FPS, paletas de colores y mapeo de controles (P1, P2)
│
├── assets/                     # Repositorio centralizado de recursos multimedia estáticos
│   ├── fonts/                  # Fuentes tipográficas vectoriales (.ttf)
│   ├── sprites/                # Spritesheets, interfaces y elementos visuales (.png)
│   └── audio/                  # Efectos sonoros (SFX) y bandas sonoras (.mp3, .wav)
│
└── src/                        # Código fuente del ecosistema de software
    ├── __init__.py
    │
    ├── engine/                 # Núcleo operativo del motor del Launcher
    │   ├── __init__.py
    │   └── manager.py          # Clase constructora del bucle principal y swicheo de pantallas
    │
    ├── ui/                     # Componentes visuales genéricos y compartidos
    │   ├── __init__.py
    │   └── components.py       # Botones, selectores y contenedores estilizados para los menús
    │
    ├── scenes/                 # Pantallas de flujo global del sistema
    │   ├── __init__.py
    │   ├── base_scene.py       # Interfaz o clase abstracta para el polimorfismo de pantallas
    │   ├── main_menu.py        # Menú principal de bienvenida de la aplicación
    │   └── game_select.py      # Panel de selección o "Lobby" para elegir entre los 7 modos
    │
    └── modes/                  # 🚀 CONTENEDOR EXCLUSIVO PARA LOS 7 MODOS DE JUEGO
        ├── __init__.py
        ├── base_mode.py        # Clase base que normaliza los métodos que cada juego debe implementar
        │
        ├── gravity_runner/     # MODO 1: Adaptación multijugador local del juego base de script.py
        │   ├── __init__.py
        │   ├── runner_game.py  # Controlador del estado interno, colisiones y marcador del juego
        │   └── entities.py     # Clases Jugador, Obstáculo y Partícula acopladas a este modo
        │
        ├── modo_juego_2/       # MODO 2: (Espacio reservado para el siguiente juego arcade)
        │   ├── __init__.py
        │   ├── mode_two_game.py
        │   └── entities.py
        │
        └── modo_juego_3/       # MODO 3 al 7... (Misma estructura modularizada)
            ├── __init__.py
            └── ...
```

---

## 🛠️ Desglose Funcional de Módulos Centrales

### 1. Punto de Entrada (`main.py`)
Inicializa la ejecución del programa. Su único propósito es instanciar la clase contenedora de la aplicación (`GameManager`) localizada en `src.engine.manager` y lanzar el bucle principal. Se mantiene libre de lógica de juego.

### 2. Configuración Compartida (`config/settings.py`)
Almacena constantes globales del sistema como las dimensiones fijas de la ventana (`ANCHO = 800`, `ALTO = 600`), tasa de refresco (`FPS = 60`) y paletas cromáticas estéticas (Neón Cyberpunk). Adicionalmente, centraliza el **mapeo de entradas de teclado** para múltiples jugadores locales (ej. Controles de Jugador 1 con WASD/Espacio y Jugador 2 con Flechas/Enter), garantizando que todos los modos compartan la misma abstracción de periféricos.

### 3. El Motor del Launcher (`src/engine/manager.py`)
Maneja el bucle `while` nativo de Pygame, gestiona la ventana física y despacha eventos globales como el cierre abrupto de la aplicación (`pygame.QUIT`). Contiene una referencia dinámica a la escena activa actual, permitiendo transiciones suaves entre el menú principal, la pantalla de selección y el juego en ejecución.

### 4. Sistema de Escenas Globales (`src/scenes/`)
*   **`base_scene.py`**: Define un contrato rígido mediante métodos virtuales abstractos (`manejar_eventos()`, `actualizar()`, `dibujar()`). Esto asegura que el `GameManager` pueda tratar a cualquier pantalla de forma polimórfica sin conocer sus particularidades internas.
*   **`main_menu.py` y `game_select.py`**: Gestionan las pantallas iniciales del Hub utilizando los componentes interactivos definidos en `src/ui/components.py`. El selector de juego lee de forma dinámica la lista de módulos disponibles en la carpeta `modes/`.

### 5. Arquitectura de Modos de Juego (`src/modes/`)
Cada uno de los 7 juegos se concibe como un submódulo totalmente aislado de los demás:
*   **`base_mode.py`**: Funciona de forma homóloga a `base_scene.py`, estandarizando cómo se inicializa, actualiza y renderiza un minijuego dentro del contenedor general.
*   **`gravity_runner/`**: Contiene la lógica migrada desde `script.py`. Las clases `Jugador`, `Obstaculo` y `Particula` se encapsulan en `entities.py`. El archivo `runner_game.py` toma el control de las físicas elásticas, la aceleración progresiva de la velocidad y el cálculo dinámico de frecuencias de obstáculos, adaptando el entorno para dar soporte a interacciones multijugador simultáneas en la misma pantalla.

---

## 🧠 Leyes y Buenas Prácticas Aplicadas

1.  **Bajo Acoplamiento y Alta Cohesión:** El motor del launcher no conoce las reglas, mecánicas ni sistemas de puntuación de los minijuegos. Esto evita dependencias cruzadas destructivas.
2.  **Erradicación de Estados Globales Mutables:** Se elimina completamente el uso de la palabra clave `global` presente en el prototipo original. El estado actual del juego, las puntuaciones y los récords se encapsulan como atributos de instancia dentro de sus respectivas clases controladoras.
3.  **Principio Abierto/Cerrado (OCP):** El sistema está "abierto para la extensión pero cerrado para la modificación". Desarrollar los 6 modos de juego restantes es tan simple como empaquetar nuevas carpetas bajo `src/modes/` siguiendo la interfaz de `base_mode.py`, sin necesidad de alterar una sola línea de código en el Launcher principal.
4.  **Inyección y Gestión Eficiente de Recursos:** Las fuentes y los assets comunes se administran centralizadamente para evitar fugas de memoria por recargas reiteradas en el bucle principal.