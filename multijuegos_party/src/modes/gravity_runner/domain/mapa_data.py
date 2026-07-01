NIVEL_1 = {
    "distancia_meta": 5500,  # Un nivel bastante largo y de resistencia pura
    "plataformas": [
        # --- ZONA 1: Introducción Rítmica (Falsa seguridad) ---
        {"x": 600, "y": 320, "ancho": 150, "alto": 30},   # Plataforma 0
        {"x": 900, "y": 180, "ancho": 150, "alto": 30},   # Plataforma 1
        
        # --- ZONA 2: Escalera de Micro-plataformas (Precisión Milimétrica) ---
        # El ancho es de solo 60px (casi el tamaño del cubo). Hay que cambiar la gravedad al tocar cada una.
        {"x": 1300, "y": 380, "ancho": 60, "alto": 25},   # Plataforma 2
        {"x": 1500, "y": 150, "ancho": 60, "alto": 25},   # Plataforma 3
        {"x": 1700, "y": 380, "ancho": 60, "alto": 25},   # Plataforma 4
        {"x": 1900, "y": 150, "ancho": 60, "alto": 25},   # Plataforma 5

        # --- ZONA 3: El Laberinto de Pasillos Estrechos (Efecto Claustrofobia) ---
        # Una serie de bloques flotantes intermedios largos donde debes ir por el centro exacto
        {"x": 2300, "y": 270, "ancho": 400, "alto": 35},  # Plataforma 6
        {"x": 2850, "y": 180, "ancho": 300, "alto": 30},  # Plataforma 7
        {"x": 2850, "y": 360, "ancho": 300, "alto": 30},  # Plataforma 8

        # --- ZONA 4: El Zig-Zag del Pánico (Transiciones veloces) ---
        {"x": 3400, "y": 350, "ancho": 80, "alto": 25},   # Plataforma 9
        {"x": 3600, "y": 180, "ancho": 80, "alto": 25},   # Plataforma 10
        {"x": 3800, "y": 350, "ancho": 80, "alto": 25},   # Plataforma 11
        {"x": 4000, "y": 180, "ancho": 80, "alto": 25},   # Plataforma 12

        # --- ZONA 5: Pasarela Final de Resistencia ---
        {"x": 4400, "y": 260, "ancho": 600, "alto": 30},  # Plataforma 13
    ],
    "pinchos": [
        # --- Obstáculos Zona 1 ---
        {"x": 670, "y": "plataforma", "index_plat": 0},
        {"x": 970, "y": "plataforma", "index_plat": 1},
        {"x": 1100, "y": "suelo"},

        # --- Obstáculos Zona 2 (Pinchos trampa en los límites globales) ---
        # Mientras saltas entre micro-plataformas, el suelo y techo se llenan de pinchos para que no te dejes caer
        {"x": 1300, "y": "suelo"}, {"x": 1300, "y": "techo"},
        {"x": 1500, "y": "suelo"}, {"x": 1500, "y": "techo"},
        {"x": 1700, "y": "suelo"}, {"x": 1700, "y": "techo"},
        {"x": 1900, "y": "suelo"}, {"x": 1900, "y": "techo"},

        # --- Obstáculos Zona 3 (El Sándwich) ---
        # Bloqueamos el suelo y el techo. Obligatorio mantenerse en la plataforma central (index 6).
        {"x": 2300, "y": "suelo"}, {"x": 2300, "y": "techo"},
        {"x": 2450, "y": "suelo"}, {"x": 2450, "y": "techo"},
        # ¡Sorpresa! Un pincho en medio de la misma plataforma larga
        {"x": 2500, "y": "plataforma", "index_plat": 6},
        {"x": 2650, "y": "suelo"}, {"x": 2650, "y": "techo"},

        # Doble Pasillo: Pinchos arriba y abajo que te obligan a elegir si ir por el techo o por el suelo
        {"x": 2850, "y": "suelo"}, {"x": 2850, "y": "techo"},
        {"x": 2950, "y": "plataforma", "index_plat": 7}, # Pincho en la plataforma de arriba
        {"x": 3050, "y": "plataforma", "index_plat": 8}, # Pincho en la plataforma de abajo
        {"x": 3140, "y": "suelo"}, {"x": 3140, "y": "techo"},

        # --- Obstáculos Zona 4 (Zig-Zag con pinchos rozando) ---
        {"x": 3410, "y": "plataforma", "index_plat": 9},
        {"x": 3610, "y": "plataforma", "index_plat": 10},
        {"x": 3810, "y": "plataforma", "index_plat": 11},
        {"x": 4010, "y": "plataforma", "index_plat": 12},

        # --- Obstáculos Zona 5 (El Sprint Infernal) ---
        # Una lluvia de pinchos alternados en la plataforma final (index 13)
        {"x": 4450, "y": "plataforma", "index_plat": 13},
        {"x": 4550, "y": "suelo"},
        {"x": 4650, "y": "techo"},
        {"x": 4750, "y": "plataforma", "index_plat": 13},
        {"x": 4900, "y": "suelo"},
        {"x": 4930, "y": "suelo"}, # ¡Pincho doble en el suelo base!

        # --- Trampa antes de la meta (X: 5500) ---
        # Un pincho triple final en el suelo y un techo bajo que requiere cambiar la gravedad en el último milisegundo
        {"x": 5200, "y": "suelo"},
        {"x": 5232, "y": "suelo"},
        {"x": 5264, "y": "suelo"},
        {"x": 5350, "y": "techo"},
    ]
}