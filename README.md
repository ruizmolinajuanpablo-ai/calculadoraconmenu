MENÚ DE HERRAMIENTAS · PySide6
===============================

Descripción
-----------
Aplicación de escritorio con siete herramientas útiles, escritas en Python
con PySide6 (Qt). Todo va dentro de una única ventana con pestañas y un menú
superior ("Herramientas") que permite cambiar de herramienta, copiar el resultado
y reiniciarla. El diseño sigue el mismo tema oscuro que la Calculadora 2.0
(fondo degradado azul petróleo, acentos turquesa y coral).

Cada herramienta es independiente, pero comparten una misma interfaz: todas
tienen un método para devolver su resultado (resultado()) y otro para reiniciarse
(reiniciar()). Por eso el menú "Copiar resultado" y "Reiniciar herramienta"
funcionan siempre con la pestaña activa, sin importar qué herramienta esté
abierta.

Herramientas incluidas
----------------------
1. Notas
   - Calcula la media ponderada de parciales y examen final.
   - Indica qué nota necesitas en el examen final para sacar un 5 (o el
     aprobado que quieras interpretar).
   - Avisa cuando los pesos no suman 100 % y cuando no es posible alcanzar
     el aprobado con los pesos actuales.

2. Bases
   - Conversor entre decimal, binario, octal y hexadecimal.
   - Al escribir en cualquier campo, los otros tres se actualizan solos.
   - Acepta números negativos y valida la entrada para cada base.

3. Porcentajes
   - Descuento, IVA (21 %), aumento, propina y "X es el % de Y".
   - Muestra cuánto se añade o se ahorra y el precio final de forma clara.
   - Calcula qué porcentaje representa una cantidad sobre un total.

4. Unidades
   - Longitud, masa, tiempo, datos, volumen, área y temperatura.
   - Permite intercambiar origen y destino con un solo clic.
   - Las temperaturas usan Kelvin internamente para evitar errores de
     conversión.

5. Contraseñas
   - Generador de contraseñas con el módulo `secrets` (aleatoriedad segura
     del sistema, no con generador predecible).
   - Se asegura de incluir al menos un carácter de cada tipo marcado
     (mayúsculas, minúsculas, números y símbolos).
   - Longitud entre 6 y 64 caracteres.

6. Texto
   - Cuenta palabras, caracteres (con y sin espacios), líneas y párrafos.
   - Estima el tiempo de lectura aproximado (200 palabras por minuto).
   - Permite limpiar el texto o cargar un ejemplo de prueba.

7. Suma
   - Suma una lista de números separada por +, espacios, saltos de línea o ; 
   - El punto o la coma se interpretan como decimal (se prioriza el uso
     decimal correcto). Admite notación científica (1e3).
   - Hasta 12 números por cálculo, con validación de cada valor.

Requisitos
----------
Necesitas un Python con PySide6 instalado. PySide6 **no tiene versión para
Python 3.14**, por eso en este equipo se usa el Python 3.9.6 del sistema
(`/usr/bin/python3`), que es el único que lo tiene instalado:

  /usr/bin/python3 -m pip install --user PySide6      Instalar (una sola vez)
  /usr/bin/python3 -c "import PySide6; print('OK')"   Comprobar

En este Mac hay dos intérpretes:

  /usr/bin/python3        3.9.6    PySide6 6.9.3  → CORRECTO
  /usr/local/bin/python3  3.14.4   sin PySide6   → NO sirve

Por este motivo el archivo tiene shebang `#!/usr/bin/python3` y las
instrucciones de ejecución usan siempre `/usr/bin/python3`.

Cómo ejecutarlo en este Mac
---------------------------
1) Doble clic en `Herramientas.app` (forma más cómoda). Usa el mismo icono
   que la Calculadora 2.0.
2) Visual Studio Code: abre la carpeta, elige `Herramientas · PySide6` en el
   desplegable de Depuración y pulsa F5.
3) Terminal:
     /usr/bin/python3 "herramientas.py"
4) Desde la propia carpeta (shebang + permiso de ejecución):
     "./herramientas.py"

Opciones del programa
---------------------
  --captura              Guarda un PNG por cada herramienta y no abre la ventana.
  --captura ruta_base    Usa esa base para los nombres de archivo.
  --help                 Muestra la ayuda.

Sin argumentos, abre la ventana en un equipo con pantalla.

Menú y atajos de teclado
------------------------
Menú `Herramientas`:
  Ctrl+1  → Notas
  Ctrl+2  → Bases
  Ctrl+3  → Porcentajes
  Ctrl+4  → Unidades
  Ctrl+5  → Contraseñas
  Ctrl+6  → Texto
  Ctrl+7  → Suma

Otras acciones:
  Ctrl+Mayús+C  → Copiar resultado (de la herramienta activa)
  Ctrl+R        → Reiniciar herramienta (vuelve a su estado inicial)
  F1            → Guía rápida
  Ctrl+C/Ctrl+V → Copiar y pegar en campos de texto

Cómo ejecutarlo en otros dispositivos
------------------------------------
El archivo se puede copiar tal cual. Solo cambia el intérprete y la forma
de instalar PySide6.

macOS (otro equipo)
  /usr/bin/python3 -m pip install --user PySide6
  /usr/bin/python3 "herramientas.py"

Windows
  py -m pip install PySide6
  py "herramientas.py"
  Para que no aparezca la consola: lanzar con `pythonw.exe` (acceso directo).
  Si los acentos salen raros: `chcp 65001` y ejecutar con `py -X utf8 ...`

Linux
  sudo apt install python3 python3-pip
  pip install PySide6  (o --break-system-packages según la distribución)
  python3 "herramientas.py"
  Si Qt no carga el plugin de pantalla (xcb): instalar las librerías mínimas:
     sudo apt install libgl1 libegl1 libxkbcommon-x11-0 libxcb-cursor0 \
                      libxcb-icccm4 libxcb-keysyms1 libxcb-shape0 \
                      libdbus-1-3 libfontconfig1
  En servidores sin monitor, el programa detecta que no hay pantalla y
  guarda automáticamente un PNG por herramienta con `--captura`.

Replit (plantilla GUI)
  pip install PySide6
  python herramientas.py

Google Colab / JupyterLite
  %pip install PySide6
  !python "herramientas.py" --captura herramientas
  from IPython.display import Image, display
  for i in [1,2,3,4,5,6,7]:
      display(Image(f"herramientas-{i}-*.png"))  (o los nombres exactos)

Android (Pydroid 3)
  Permite instalar PySide6 desde Pip en Ajustes.

Visual Studio Code
------------------
`.vscode/launch.json` incluye tres configuraciones:
  2.0 · PySide6              → /usr/bin/python3  (calculadora grafica 2.0.py)
  Herramientas · PySide6     → /usr/bin/python3  (herramientas.py)
  1.0 · Tkinter              → /usr/local/bin/python3  (pract2_calc.py)

La configuración `.vscode/settings.json` fija `/usr/bin/python3` como
intérprete por defecto del proyecto. Si el botón ▶ no funciona la primera vez,
elige el intérprete manualmente con `Cmd+Shift+P → Python: Select Interpreter →
/usr/bin/python3`.

Sugerencias para que funcione bien
----------------------------------
1) Usa siempre `/usr/bin/python3` en este equipo. Compruébalo:
     /usr/bin/python3 -c "import PySide6, sys; print(PySide6.__version__, sys.version.split()[0])"

2) En macOS, la app `Herramientas.app` lee el código de la carpeta cuando
   tiene permiso, y recurre a la copia de `Contents/Resources/` si no puede
   leerlo (por privacidad con ~/Desktop). Si editas el archivo, edita el de
   la carpeta, no la copia interna.

3) Guarda los archivos en UTF-8. Contienen tildes, eñes y caracteres
   tipográficos (× ÷ −). Si los guardas con otra codificación pueden aparecer
   caracteres raros.

4) El modo sin pantalla funciona automáticamente: si no hay DISPLAY/WAYLAND
   o `QT_QPA_PLATFORM=offscreen`, genera PNGs en lugar de abrir ventana.
   Úsalo en servidores o cuadernos online con `--captura`.

5) Comprobación rápida (valida que todo está bien):
     /usr/bin/python3 "herramientas.py" --captura /tmp/prueba_herr
   Debe crear 7 PNGs sin errores.

Problemas frecuentes y solución
-------------------------------
- `ModuleNotFoundError: No module named 'PySide6'`
  → Estás usando el intérprete equivocado (suele ser 3.14). Usa `/usr/bin/python3`.

- `qt.qpa.plugin: Could not load the Qt platform plugin xcb` (Linux)
  → Faltan librerías del sistema. Instala el paquete indicado en Linux.

- Ventana en blanco o no aparece
  → Comprueba que se ejecuta con Python que tenga PySide6 (no con doble clic
    sobre .py si el Finder lo abre en editor). En Linux puede faltar xcb.

- La app tarda en abrir por primera vez
  → Qt carga fuentes y plugins; es normal en macOS. Las siguientes veces
    abre mucho más rápido.

Archivos del proyecto
---------------------
  herramientas.py              Código fuente del menú de herramientas (PySide6)
  Herramientas.app              Aplicación de macOS para abrir con doble clic
  calculadora grafica 2.0.py   Calculadora 2.0 (PySide6)
  Calculadora 2.0.app          App de la calculadora 2.0
  .vscode/                     Configuración de VS Code (intérprete y launch)
  README_Herramientas.txt      Este documento
  README 2.0.txt               Documentación de la Calculadora 2.0
  Practica 1/                  Versión 1 con Tkinter (pract2_calc.py + app)

Notas técnicas
--------------
- Las contraseñas usan `secrets.SystemRandom()` y `secrets.choice`, no
  `random`. Garantiza al menos un carácter de cada conjunto seleccionado.
- Todas las conversiones de expresión/números se validan (no se usa `eval`).
- Las temperaturas convierten a Kelvin para evitar errores de precisión.
- El tema se aplica con `QApplication.setStyleSheet` y `Fusion` para que
  quede igual en macOS, Windows y Linux.
- Modo `offscreen` de Qt: dibuja la interfaz sin pantalla y permite generar
  capturas en servidores o cuadernos sin monitor.
