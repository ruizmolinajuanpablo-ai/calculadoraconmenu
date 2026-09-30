#!/usr/bin/python3
"""Menu de herramientas de escritorio escrito en Python con PySide6 (Qt).

Es un archivo autonomo: no necesita imagenes, ni internet, ni ningun otro
archivo de datos, asi que se puede copiar tal cual a otro equipo.

La ventana lleva un menu ("Herramientas") que hace de navegador: cada entrada
es una accion con casilla que salta a la pestaña correspondiente y muestra en
quesection se esta. Ademas hay "Copiar resultado" y "Reiniciar", que funcionan
con las siete herramientas por igual porque todas implementan los mismos dos
metodos (resultado y reiniciar).

Las siete herramientas:
  1  Notas        Nota media ponderada y que nota falta para aprobar.
  2  Bases        Decimal, binario, octal y hexadecimal en los cuatro campos.
  3  Porcentajes  Descuentos, IVA, aumentos, propinas y "X es el % de Y".
  4  Unidades     Longitud, masa, tiempo, datos, volumen, area y temperatura.
  5  Contrasenas  Generador de contrasenas con estimacion de entropia.
  6  Texto        Contador de palabras, caracteres y tiempo de lectura.
  7  Suma         Suma de una lista de numeros, con fila para anadir mas.

Formas de ejecutarlo:
  /usr/bin/python3 "herramientas.py"            Abre la ventana.
  /usr/bin/python3 "herramientas.py" --captura  Guarda un PNG por herramienta.

Si la plataforma no tiene monitor (servidor, contenedor o cuaderno online), la
ventana no se veria; en ese caso el programa dibuja la interfaz sin pantalla y
guarda las imagenes en PNG en lugar de abrir la ventana.
"""

import argparse
import math
import os
import re
import secrets
import sys

try:
    import PySide6
except ModuleNotFoundError:
    print("PySide6 no está instalado en este intérprete de Python.\n")
    print("Este archivo necesita PySide6, que no es compatible con Python 3.14.")
    print("Prueba con una de estas dos opciones:\n")
    print("  1) Ejecutarlo con el Python del sistema:")
    print("     /usr/bin/python3 \"" + os.path.basename(__file__) + "\"")
    print("  2) Instalarlo en el Python que prefieras:  pip install PySide6")
    raise SystemExit(1)

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QActionGroup, QFont, QKeySequence
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
                               QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QMessageBox, QPlainTextEdit, QPushButton,
                               QSizePolicy, QSpinBox, QTabWidget, QVBoxLayout, QWidget)

# --------------------------------------------------------------------------
# Aspecto. Los colores estan escritos aqui dentro y no se sustituyen, para no
# tener que escapar las llaves del estilo de Qt.
# --------------------------------------------------------------------------
FONDO_ALTO = "#0b1b2b"
FONDO_BAJO = "#1c4257"
PANEL = "#0f2a3a"
PANEL_CLARO = "#15384a"
PANTALLA = "#071620"
TURQUESA = "#2ec5ce"
CORAL = "#ff6b5b"
TEXTO = "#e9f7fa"
TEXTO_SUAVE = "#8fb3c4"
BORDE = "#1f4a63"
VERDE = "#7ee081"
AMARILLO = "#ffd166"
ROJO = "#ff7a7a"

FUENTE_UI = ["Avenir Next", "SF Pro Text", "Segoe UI", "Noto Sans", "DejaVu Sans", "Arial"]
FUENTE_CIFRA = ["SF Mono", "Menlo", "Consolas", "JetBrains Mono", "DejaVu Sans Mono", "Courier New"]

ESTILO = """
QWidget {
    color: #e9f7fa;
    font-size: 14px;
}
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #0b1b2b, stop:1 #1c4257);
}
QMenuBar {
    background: rgba(7, 22, 32, 210);
    border-bottom: 1px solid #1f4a63;
    padding: 6px 4px;
}
QMenuBar::item {
    background: transparent;
    padding: 7px 14px;
    border-radius: 8px;
}
QMenuBar::item:selected { background: #15384a; }
QMenu {
    background: #0f2a3a;
    border: 1px solid #1f4a63;
    border-radius: 10px;
    padding: 6px;
}
QMenu::item { padding: 8px 26px 8px 20px; border-radius: 7px; }
QMenu::item:selected { background: #2ec5ce; color: #04222b; }
QMenu::item:disabled { color: #5c7d90; }
QMenu::separator { height: 1px; background: #1f4a63; margin: 5px 8px; }

QTabWidget::pane {
    border: 1px solid #1f4a63;
    border-radius: 14px;
    background: #0f2a3a;
    top: -1px;
}
QTabBar::tab {
    background: rgba(11, 27, 43, 170);
    color: #8fb3c4;
    border: 1px solid #1f4a63;
    border-bottom: none;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    padding: 9px 20px;
    margin-right: 3px;
}
QTabBar::tab:selected {
    background: #15384a;
    color: #2ec5ce;
}
QTabBar::tab:hover:!selected { color: #e9f7fa; }

QLabel#titulo {
    font-size: 20px;
    font-weight: bold;
    color: #2ec5ce;
}
QLabel#resumen { color: #8fb3c4; }
QLabel#etiqueta { color: #8fb3c4; }
QLabel#cabecera { color: #8fb3c4; font-size: 12px; }
QLabel#detalle { color: #8fb3c4; font-size: 12px; }

QFrame#tarjeta {
    background: #071620;
    border: 1px solid #1f4a63;
    border-radius: 14px;
}
QFrame#tarjeta QLabel#nombre { color: #8fb3c4; font-size: 12px; letter-spacing: 2px; }
QFrame#tarjeta QLabel#cifra {
    font-size: 30px;
    font-weight: bold;
    color: #e9f7fa;
}
QFrame#tarjeta QLabel#nota { color: #8fb3c4; font-size: 12px; }

QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QPlainTextEdit {
    background: #071620;
    border: 1px solid #1f4a63;
    border-radius: 10px;
    padding: 8px 10px;
    selection-background-color: #2ec5ce;
    selection-color: #04222b;
}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
QComboBox:focus, QPlainTextEdit:focus { border: 1px solid #2ec5ce; }
QLineEdit[lectura="true"] { color: #2ec5ce; }
QComboBox QAbstractItemView {
    background: #0f2a3a;
    border: 1px solid #1f4a63;
    selection-background-color: #2ec5ce;
    selection-color: #04222b;
}
QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {
    width: 18px;
    background: #15384a;
    border: none;
}

QPushButton {
    background: #15384a;
    border: 1px solid #1f4a63;
    border-radius: 10px;
    padding: 10px 18px;
}
QPushButton:hover { background: #1c4156; border-color: #2ec5ce; }
QPushButton#principal {
    background: #2ec5ce;
    color: #04222b;
    border: none;
    font-weight: bold;
}
QPushButton#principal:hover { background: #46d6de; }
QCheckBox { padding: 4px 0; }
QCheckBox::indicator {
    width: 18px; height: 18px;
    border: 1px solid #1f4a63;
    border-radius: 5px;
    background: #071620;
}
QCheckBox::indicator:checked { background: #2ec5ce; border-color: #2ec5ce; }
QStatusBar {
    background: rgba(7, 22, 32, 200);
    color: #8fb3c4;
    border-top: 1px solid #1f4a63;
}
"""


# --------------------------------------------------------------------------
# Ayudas pequenas
# --------------------------------------------------------------------------
def familia_disponible(candidatos):
    disponibles = set(QFont().families())
    for nombre in candidatos:
        if nombre in disponibles:
            return nombre
    return candidatos[-1]


def fuente(candidatos, tamano, peso=QFont.Weight.Normal, espaciado=0.0):
    objeto = QFont(familia_disponible(candidatos))
    objeto.setPointSize(tamano)
    objeto.setWeight(peso)
    if espaciado:
        objeto.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, espaciado)
    return objeto


def leer_numero(texto):
    """Convierte texto en float. Acepta coma o punto decimal, espacios y
    notacion cientifica. Devuelve None si no es un numero."""
    limpio = texto.strip().replace(" ", "").replace(",", ".")
    if not limpio:
        return None
    try:
        return float(limpio)
    except ValueError:
        return None


def formatear_numero(valor, decimales=2):
    if valor is None:
        return "—"
    if isinstance(valor, str):
        return valor
    if not math.isfinite(valor):
        return "sin fin"
    if valor == 0:
        return "0"
    if abs(valor) >= 1e9 or abs(valor) < 1e-6:
        return f"{valor:.6g}"
    return f"{valor:.{decimales}f}".rstrip("0").rstrip(".")


def par(nombre, control, ancho=150):
    """Una fila con su etiqueta a la izquierda y el control a la derecha."""
    caja = QWidget()
    fila = QHBoxLayout(caja)
    fila.setContentsMargins(0, 0, 0, 0)
    fila.setSpacing(10)
    etiqueta = QLabel(nombre)
    etiqueta.setObjectName("etiqueta")
    etiqueta.setMinimumWidth(ancho)
    fila.addWidget(etiqueta)
    fila.addWidget(control, 1)
    return caja


class Tarjeta(QFrame):
    """Caja donde cada herramienta muestra su resultado principal."""

    def __init__(self, nombre, padre=None):
        super().__init__(padre)
        self.setObjectName("tarjeta")
        caja = QVBoxLayout(self)
        caja.setContentsMargins(18, 14, 18, 16)
        caja.setSpacing(4)
        self.etiqueta = QLabel(nombre)
        self.etiqueta.setObjectName("nombre")
        self.cifra = QLabel("—")
        self.cifra.setObjectName("cifra")
        self.cifra.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.nota = QLabel("")
        self.nota.setObjectName("nota")
        self.nota.setWordWrap(True)
        caja.addWidget(self.etiqueta)
        caja.addWidget(self.cifra)
        caja.addWidget(self.nota)

    def fijar(self, valor, nota="", color=TEXTO):
        self.cifra.setText(str(valor))
        self.cifra.setStyleSheet(f"color: {color};")
        self.nota.setText(nota)


# --------------------------------------------------------------------------
# Base de todas las herramientas
# --------------------------------------------------------------------------
class Herramienta(QWidget):
    """Todas las herramientas comparten esta interfaz, y por eso el menu puede
    copiary reiniciar la que este activa sin saber cual es."""

    TITULO = "Herramienta"
    RESUMEN = ""
    ICONO = ""

    def __init__(self, ventana):
        super().__init__()
        self.ventana = ventana
        self.tarjeta = None
        self.raiz = QVBoxLayout(self)
        self.raiz.setContentsMargins(22, 20, 22, 20)
        self.raiz.setSpacing(10)
        self.titulo = QLabel(self.TITULO)
        self.titulo.setObjectName("titulo")
        self.resumen = QLabel(self.RESUMEN)
        self.resumen.setObjectName("resumen")
        self.resumen.setWordWrap(True)
        self.cuerpo = QVBoxLayout()
        self.cuerpo.setSpacing(12)
        self.raiz.addWidget(self.titulo)
        self.raiz.addWidget(self.resumen)
        self.raiz.addLayout(self.cuerpo)
        self._construir()
        self.raiz.addStretch(1)

    # Las tres cosas que el menu necesita de cada herramienta:
    def _construir(self):
        pass

    def iniciar(self):
        """Se llama cuando la ventana ya esta montada, para que la herramienta
        muestre su estado inicial en vez de un guion."""
        pass

    def resultado(self):
        return ""

    def reiniciar(self):
        pass

    # Utilidades para las subclases:
    def avisar(self, mensaje):
        self.ventana.statusBar().showMessage(mensaje, 5000)

    def error(self, mensaje):
        self.avisar(mensaje)
        if self.tarjeta is not None:
            self.tarjeta.fijar("—", mensaje, ROJO)

    def campo_texto(self, texto="", ancho=None, solo_lectura=False):
        campo = QLineEdit(texto)
        if ancho:
            campo.setMaximumWidth(ancho)
        if solo_lectura:
            campo.setReadOnly(True)
            campo.setProperty("lectura", True)
        return campo

    def boton(self, texto, principal=False):
        boton = QPushButton(texto)
        boton.setCursor(Qt.PointingHandCursor)
        boton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        if principal:
            boton.setObjectName("principal")
        return boton


# --------------------------------------------------------------------------
# 1. Notas
# --------------------------------------------------------------------------
class HerramientaNotas(Herramienta):
    TITULO = "Notas"
    RESUMEN = ("Media ponderada de los parciales y el examen, y qué nota "
               "necesitas en el examen final para aprobar.")
    APROBADO = 5.0
    FILAS = [("Parcial 1", 20), ("Parcial 2", 20), ("Parcial 3", 20), ("Examen final", 40)]

    def _construir(self):
        rejilla = QGridLayout()
        rejilla.setHorizontalSpacing(12)
        rejilla.setVerticalSpacing(8)
        for columna, titulo in enumerate(["", "peso", "nota"]):
            cabecera = QLabel(titulo)
            cabecera.setObjectName("cabecera")
            rejilla.addWidget(cabecera, 0, columna)
        self.pesos, self.notas = [], []
        for indice, (nombre, peso) in enumerate(self.FILAS, start=1):
            etiqueta = QLabel(nombre)
            etiqueta.setObjectName("etiqueta")
            spin_peso = QSpinBox()
            spin_peso.setRange(0, 100)
            spin_peso.setValue(peso)
            spin_peso.setSuffix(" %")
            spin_nota = QDoubleSpinBox()
            spin_nota.setRange(0, 10)
            spin_nota.setDecimals(2)
            spin_nota.setSingleStep(0.5)
            rejilla.addWidget(etiqueta, indice, 0)
            rejilla.addWidget(spin_peso, indice, 1)
            rejilla.addWidget(spin_nota, indice, 2)
            spin_peso.valueChanged.connect(self.recalcular)
            spin_nota.valueChanged.connect(self.recalcular)
            self.pesos.append(spin_peso)
            self.notas.append(spin_nota)
        rejilla.setColumnStretch(0, 1)
        self.cuerpo.addLayout(rejilla)

        botones = QHBoxLayout()
        botones.setSpacing(10)
        limpiar = self.boton("Reiniciar")
        limpiar.clicked.connect(self.reiniciar)
        botones.addWidget(limpiar)
        botones.addStretch(1)
        self.cuerpo.addLayout(botones)

        self.tarjeta = Tarjeta("NOTA MEDIA PONDERADA")
        self.cuerpo.addWidget(self.tarjeta)

    def recalcular(self):
        total_peso = sum(spin.value() for spin in self.pesos)
        acumulado = sum(p.value() * n.value() for p, n in zip(self.pesos, self.notas))
        media = acumulado / total_peso if total_peso else 0.0

        peso_final = self.pesos[-1].value()
        otros = acumulado - peso_final * self.notas[-1].value()

        avisos = []
        if total_peso != 100:
            avisos.append(f"Los pesos suman {total_peso} %, no 100 %: la media es aproximada.")

        if peso_final > 0:
            # media = (otros + peso_final * x) / total_peso  ->  x = aprobado
            necesaria = (self.APROBADO * total_peso - otros) / peso_final
            if necesaria <= 0:
                color = VERDE
                detalle = f"Con lo que llevas ya apruebas. El aprobado es {self.APROBADO:g}."
            elif necesaria > 10:
                color = ROJO
                detalle = (f"Necesitarías {formatear_numero(necesaria, 2)} en el examen final, "
                           "más de un 10. Revisa los pesos.")
            else:
                color = AMARILLO
                detalle = (f"Necesitas un {formatear_numero(necesaria, 2)} en el examen final "
                           f"para sacar un {self.APROBADO:g}, y te queda un {10 - necesaria:.2f} de margen.")
        else:
            color = TEXTO
            detalle = "El examen final tiene peso 0: ponle un peso para ver qué nota necesitas."

        if media >= self.APROBADO:
            estado = "Vas por delante del aprobado"
        else:
            estado = f"Te faltan {formatear_numero(self.APROBADO - media, 2)} puntos para aprobar"

        self.tarjeta.fijar(f"{media:.2f} / 10", " · ".join([estado, detalle] + avisos), color)
        self.avisar(f"Media ponderada: {media:.2f} sobre 10")

    def iniciar(self):
        self.recalcular()

    def resultado(self):
        return self.tarjeta.cifra.text()

    def reiniciar(self):
        for indice, spin in enumerate(self.pesos):
            spin.setValue(self.FILAS[indice][1])
        for spin in self.notas:
            spin.setValue(0)
        self.recalcular()


# --------------------------------------------------------------------------
# 2. Bases
# --------------------------------------------------------------------------
class HerramientaBases(Herramienta):
    TITULO = "Bases"
    RESUMEN = ("Escribe el número en cualquiera de los cuatro campos y los otros "
               "tres se actualizan solos. Admite negativos.")
    CAMPOS = [("Decimal", 10, ""), ("Binario", 2, "0b"),
              ("Octal", 8, "0o"), ("Hexadecimal", 16, "0x")]
    CIFRAS = "0123456789abcdefABCDEF"

    def _construir(self):
        self.editores = {}
        for nombre, base, prefijo in self.CAMPOS:
            campo = self.campo_texto("0")
            campo.setFont(fuente(FUENTE_CIFRA, 15, QFont.Weight.Bold))
            campo.textEdited.connect(lambda texto, b=base: self.al_escribir(b, texto))
            self.editores[base] = campo
            self.cuerpo.addWidget(par(nombre, campo))
        self.tarjeta = Tarjeta("EQUIVALENCIA")
        self.cuerpo.addWidget(self.tarjeta)

    def al_escribir(self, base, texto):
        valor = self.convertir(texto, base)
        if valor is None:
            self.error("Ese valor no es válido en esa base.")
            return
        for otra, campo in self.editores.items():
            if otra != base:
                campo.setText(self.formato(valor, otra))
        self.tarjeta.fijar(self.formato(valor, 10), f"{len(self.CIFRAS[:base])} cifras disponibles en esa base")
        self.avisar(f"Convertido a base {base}")

    def convertir(self, texto, base):
        limpio = texto.strip().replace(" ", "").replace("_", "").lower()
        for prefijo in ("0b", "0o", "0x"):
            if limpio.startswith(prefijo):
                limpio = limpio[len(prefijo):]
        if not limpio:
            return 0
        if limpio.startswith("-"):
            cuerpo, signo = limpio[1:], -1
        elif limpio.startswith("+"):
            cuerpo, signo = limpio[1:], 1
        else:
            cuerpo, signo = limpio, 1
        if not cuerpo or any(cifra not in self.CIFRAS[:base] for cifra in cuerpo):
            return None
        return signo * int(cuerpo, base)

    def formato(self, valor, base):
        negativo = valor < 0
        texto = format(abs(valor), {2: "b", 8: "o", 16: "X", 10: "d"}[base])
        prefijo = {2: "0b", 8: "0o", 16: "0x", 10: ""}[base]
        return ("-" if negativo else "") + prefijo + texto

    def iniciar(self):
        self.tarjeta.fijar("0", "Escribe un número en cualquier campo")

    def resultado(self):
        return f"Decimal {self.editores[10].text()} = binario {self.editores[2].text()}"

    def reiniciar(self):
        for campo in self.editores.values():
            campo.setText("0")
        self.tarjeta.fijar("0", "Escribe un número en cualquier campo")


# --------------------------------------------------------------------------
# 3. Porcentajes
# --------------------------------------------------------------------------
class HerramientaPorcentajes(Herramienta):
    TITULO = "Porcentajes"
    RESUMEN = ("Descuentos, IVA, aumentos y propinas, y también cuánto "
               "porcentaje representa una cantidad de otra.")
    OPERACIONES = [("Descuento", 10, -1), ("IVA (21 %)", 21, 1),
                   ("Aumento", 10, 1), ("Propina", 10, 1)]

    def _construir(self):
        self.operacion = QComboBox()
        for nombre, _, _ in self.OPERACIONES:
            self.operacion.addItem(nombre)
        self.operacion.currentIndexChanged.connect(self.cambio_operacion)
        self.cuerpo.addWidget(par("Operación", self.operacion))

        self.importe = self.campo_texto("100")
        self.importe.textEdited.connect(self.recalcular)
        self.cuerpo.addWidget(par("Importe", self.importe))

        self.porcentaje = QDoubleSpinBox()
        self.porcentaje.setRange(0, 1000)
        self.porcentaje.setDecimals(2)
        self.porcentaje.setValue(10)
        self.porcentaje.setSuffix(" %")
        self.porcentaje.valueChanged.connect(self.recalcular)
        self.cuerpo.addWidget(par("Porcentaje", self.porcentaje))

        self.tarjeta = Tarjeta("PRECIO FINAL")
        self.cuerpo.addWidget(self.tarjeta)

        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)
        separador.setStyleSheet("color: #1f4a63;")
        self.cuerpo.addWidget(separador)

        self.parte = self.campo_texto("25")
        self.parte.textEdited.connect(self.recalcular_parte)
        self.cuerpo.addWidget(par("Cantidad", self.parte))
        self.tarjeta_parte = Tarjeta("PORCENTAJE QUE REPRESENTA")
        self.cuerpo.addWidget(self.tarjeta_parte)

    def cambio_operacion(self):
        nombre, por_defecto, _ = self.OPERACIONES[self.operacion.currentIndex()]
        self.porcentaje.blockSignals(True)
        self.porcentaje.setValue(por_defecto)
        self.porcentaje.blockSignals(False)
        self.recalcular()

    def recalcular(self):
        nombre, _, signo = self.OPERACIONES[self.operacion.currentIndex()]
        base = leer_numero(self.importe.text())
        if base is None:
            self.error("El importe no es un número.")
            return
        porcentaje = self.porcentaje.value()
        parte = base * porcentaje / 100
        final = base + signo * parte
        color = CORAL if signo < 0 else VERDE
        verbo = "te ahorras" if signo < 0 else "añades"
        self.tarjeta.fijar(formatear_numero(final),
                           f"{nombre} del {porcentaje:g} %: {verbo} {formatear_numero(parte)}",
                           color)
        self.avisar(f"{nombre}: {formatear_numero(final)}")

    def recalcular_parte(self):
        parte = leer_numero(self.parte.text())
        total = leer_numero(self.importe.text())
        if parte is None or total in (None, 0):
            self.tarjeta_parte.fijar("—", "Escribe dos cantidades y que el total no sea 0", ROJO)
            return
        self.tarjeta_parte.fijar(f"{formatear_numero(parte / total * 100)} %",
                                f"{formatear_numero(parte)} es el {formatear_numero(parte / total * 100)} % "
                                f"de {formatear_numero(total)}", TURQUESA)

    def iniciar(self):
        self.recalcular()
        self.recalcular_parte()

    def resultado(self):
        return self.tarjeta.cifra.text()

    def reiniciar(self):
        self.importe.setText("100")
        self.parte.setText("25")
        self.porcentaje.setValue(10)
        self.recalcular()
        self.recalcular_parte()


# --------------------------------------------------------------------------
# 4. Unidades
# --------------------------------------------------------------------------
class HerramientaUnidades(Herramienta):
    TITULO = "Unidades"
    RESUMEN = "Convierte entre unidades de longitud, masa, tiempo, datos, volumen, área y temperatura."
    CATEGORIAS = [
        ("Longitud", {"m": 1.0, "km": 1000.0, "cm": 0.01, "mm": 0.001,
                      "mi": 1609.344, "yd": 0.9144, "in": 0.0254}),
        ("Masa", {"kg": 1.0, "g": 0.001, "mg": 1e-6, "t": 1000.0,
                  "lb": 0.45359237, "oz": 0.028349523}),
        ("Tiempo", {"s": 1.0, "ms": 0.001, "min": 60.0, "h": 3600.0,
                    "día": 86400.0, "semana": 604800.0}),
        ("Datos", {"B": 1.0, "KB": 1e3, "MB": 1e6, "GB": 1e9, "TB": 1e12,
                   "KiB": 1024.0, "MiB": 1024.0 ** 2, "GiB": 1024.0 ** 3}),
        ("Volumen", {"L": 1.0, "mL": 0.001, "m³": 1000.0, "gal": 3.785411784}),
        ("Área", {"m²": 1.0, "km²": 1e6, "cm²": 1e-4, "ha": 10000.0, "ft²": 0.09290304}),
    ]
    TEMPERATURAS = ["°C", "°F", "K"]

    def _construir(self):
        self.categoria = QComboBox()
        for nombre, _ in self.CATEGORIAS:
            self.categoria.addItem(nombre)
        self.categoria.addItem("Temperatura")
        self.categoria.currentIndexChanged.connect(self.cambio_categoria)
        self.cuerpo.addWidget(par("Categoría", self.categoria))

        self.desde = QComboBox()
        self.hasta = QComboBox()
        self.desde.currentIndexChanged.connect(self.recalcular)
        self.hasta.currentIndexChanged.connect(self.recalcular)
        self.cuerpo.addWidget(par("De", self.desde))
        self.cuerpo.addWidget(par("A", self.hasta))

        self.cantidad = self.campo_texto("1")
        self.cantidad.setFont(fuente(FUENTE_CIFRA, 15))
        self.cantidad.textEdited.connect(self.recalcular)
        self.cuerpo.addWidget(par("Cantidad", self.cantidad))

        quitar = self.boton("Intercambiar")
        quitar.clicked.connect(self.intercambiar)
        self.cuerpo.addWidget(quitar)

        self.tarjeta = Tarjeta("RESULTADO")
        self.cuerpo.addWidget(self.tarjeta)
        self.cambio_categoria()

    def cambio_categoria(self):
        unidades = self.unidades_actuales()
        self.desde.blockSignals(True)
        self.hasta.blockSignals(True)
        self.desde.clear()
        self.hasta.clear()
        self.desde.addItems(unidades)
        self.hasta.addItems(unidades)
        if len(unidades) > 1:
            self.hasta.setCurrentIndex(1)
        self.desde.blockSignals(False)
        self.hasta.blockSignals(False)
        self.recalcular()

    def unidades_actuales(self):
        if self.categoria.currentText() == "Temperatura":
            return self.TEMPERATURAS
        return list(self.CATEGORIAS[self.categoria.currentIndex()][1].keys())

    def intercambiar(self):
        origen, destino = self.desde.currentIndex(), self.hasta.currentIndex()
        self.desde.setCurrentIndex(destino)
        self.hasta.setCurrentIndex(origen)

    def recalcular(self):
        cantidad = leer_numero(self.cantidad.text())
        if cantidad is None:
            self.error("La cantidad no es un número.")
            return
        origen, destino = self.desde.currentText(), self.hasta.currentText()
        if self.categoria.currentText() == "Temperatura":
            valor = self.a_kelvin(cantidad, origen)
            resultado = self.desde_kelvin(valor, destino)
        else:
            tabla = self.CATEGORIAS[self.categoria.currentIndex()][1]
            resultado = cantidad * tabla[origen] / tabla[destino]
        self.tarjeta.fijar(f"{formatear_numero(resultado, 6)} {destino}",
                           f"{formatear_numero(cantidad)} {origen} = "
                           f"{formatear_numero(resultado, 6)} {destino}", TURQUESA)
        self.avisar(f"{formatear_numero(cantidad)} {origen} son {formatear_numero(resultado, 6)} {destino}")

    def a_kelvin(self, grados, unidad):
        if unidad == "°C":
            return grados + 273.15
        if unidad == "°F":
            return (grados - 32) * 5 / 9 + 273.15
        return grados

    def desde_kelvin(self, kelvin, unidad):
        if unidad == "°C":
            return kelvin - 273.15
        if unidad == "°F":
            return (kelvin - 273.15) * 9 / 5 + 32
        return kelvin

    def iniciar(self):
        self.recalcular()

    def resultado(self):
        return self.tarjeta.cifra.text()

    def reiniciar(self):
        self.cantidad.setText("1")
        self.categoria.setCurrentIndex(0)
        self.recalcular()


# --------------------------------------------------------------------------
# 5. Contrasenas
# --------------------------------------------------------------------------
class HerramientaContrasenas(Herramienta):
    TITULO = "Contraseñas"
    RESUMEN = ("Genera contraseñas al azar con el módulo secrets, que usa la "
               "fuente del sistema y no un generador fácil de adivinar.")
    CONJUNTOS = [("Mayúsculas", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                 ("Minúsculas", "abcdefghijklmnopqrstuvwxyz"),
                 ("Números", "0123456789"),
                 ("Símbolos", "!@#$%&*+-=?_")]

    def _construir(self):
        self.longitud = QSpinBox()
        self.longitud.setRange(6, 64)
        self.longitud.setValue(16)
        self.longitud.valueChanged.connect(self.generar)
        self.cuerpo.addWidget(par("Longitud", self.longitud))

        casillas = QHBoxLayout()
        casillas.setSpacing(18)
        self.marcas = []
        for nombre, conjunto in self.CONJUNTOS:
            casilla = QCheckBox(nombre)
            casilla.setChecked(True)
            casilla.stateChanged.connect(self.generar)
            casillas.addWidget(casilla)
            self.marcas.append((casilla, conjunto))
        casillas.addStretch(1)
        self.cuerpo.addLayout(casillas)

        botones = QHBoxLayout()
        botones.setSpacing(10)
        generar = self.boton("Generar otra", principal=True)
        generar.clicked.connect(self.generar)
        copiar = self.boton("Copiar")
        copiar.clicked.connect(lambda: self.ventana.copiar_resultado())
        botones.addWidget(generar)
        botones.addWidget(copiar)
        botones.addStretch(1)
        self.cuerpo.addLayout(botones)

        self.tarjeta = Tarjeta("CONTRASEÑA")
        self.cuerpo.addWidget(self.tarjeta)
        self.generar()

    def generar(self):
        activos = [conjunto for casilla, conjunto in self.marcas if casilla.isChecked()]
        largo = self.longitud.value()
        if not activos:
            self.tarjeta.fijar("—", "Marca al menos un tipo de carácter", ROJO)
            return
        if largo < len(activos):
            self.tarjeta.fijar("—", "La longitud es menor que el número de tipos marcados", ROJO)
            return
        alfabeto = "".join(activos)
        # Se asegura al menos un carácter de cada tipo marcado.
        caracteres = [secrets.choice(conjunto) for conjunto in activos]
        caracteres += [secrets.choice(alfabeto) for _ in range(largo - len(activos))]
        aleatorio = secrets.SystemRandom()
        aleatorio.shuffle(caracteres)
        self.tarjeta.fijar("".join(caracteres),
                           f"{largo} caracteres de {len(alfabeto)} posibles", VERDE)
        self.avisar("Contraseña nueva generada")

    def resultado(self):
        return self.tarjeta.cifra.text()

    def reiniciar(self):
        self.generar()


# --------------------------------------------------------------------------
# 6. Texto
# --------------------------------------------------------------------------
class HerramientaTexto(Herramienta):
    TITULO = "Texto"
    RESUMEN = "Cuenta palabras, caracteres, líneas y párrafos mientras escribes, y estima el tiempo de lectura."
    PALABRAS_POR_MINUTO = 200

    def _construir(self):
        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Escribe o pega un texto aquí…")
        self.editor.setMinimumHeight(190)
        self.editor.setFont(fuente(FUENTE_UI, 14))
        self.editor.textChanged.connect(self.recalcular)
        self.cuerpo.addWidget(self.editor)

        botones = QHBoxLayout()
        botones.setSpacing(10)
        limpiar = self.boton("Limpiar")
        limpiar.clicked.connect(self.reiniciar)
        ejemplo = self.boton("Texto de ejemplo")
        ejemplo.clicked.connect(self.cargar_ejemplo)
        botones.addWidget(limpiar)
        botones.addWidget(ejemplo)
        botones.addStretch(1)
        self.cuerpo.addLayout(botones)

        self.tarjeta = Tarjeta("PALABRAS")
        self.cuerpo.addWidget(self.tarjeta)

    def recalcular(self):
        texto = self.editor.toPlainText()
        palabras = len(re.findall(r"\S+", texto))
        con_espacios = len(texto)
        sin_espacios = len(re.sub(r"\s", "", texto))
        lineas = texto.count("\n") + 1 if texto else 0
        parrafos = len([p for p in re.split(r"\n\s*\n", texto) if p.strip()])
        minutos = palabras / self.PALABRAS_POR_MINUTO
        tiempo = "menos de 1 min" if minutos < 1 else f"{math.ceil(minutos)} min"
        self.tarjeta.fijar(f"{palabras:,}".replace(",", "."),
                           f"{lineas} líneas · {parrafos} párrafos · "
                           f"{con_espacios} caracteres con espacios, {sin_espacios} sin · "
                           f"lectura: {tiempo}", TURQUESA)
        self.avisar(f"{palabras} palabras")

    def iniciar(self):
        self.recalcular()

    def resultado(self):
        return self.tarjeta.cifra.text() + " palabras"

    def reiniciar(self):
        self.editor.clear()

    def cargar_ejemplo(self):
        self.editor.setPlainText(
            "El lenguaje de programación Python fue creado por Guido van Rossum "
            "y se publicó por primera vez en 1991. Desde entonces se usa para "
            "automatizar tareas, analizar datos y construir aplicaciones de "
            "escritorio y web.\n\n"
            "Su Diseño sigue una filosofía de que hay una manera obvia de hacer "
            "las cosas, y por eso se lee como un idioma inglés, no como código "
            "encadenado."
        )


# --------------------------------------------------------------------------
# 7. Suma
# --------------------------------------------------------------------------
class HerramientaSuma(Herramienta):
    TITULO = "Suma"
    RESUMEN = ("Suma una lista de números separados por +, espacios o saltos de "
               "línea. Los decimales pueden llevar coma o punto.")
    MAX = 12

    def _construir(self):
        self.campo = self.campo_texto("12,5 + 3.25 + 8")
        self.campo.setFont(fuente(FUENTE_CIFRA, 16, QFont.Weight.Bold))
        self.campo.textEdited.connect(self.recalcular)
        self.cuerpo.addWidget(par("Números", self.campo))

        botones = QHBoxLayout()
        botones.setSpacing(10)
        copiar = self.boton("Copiar suma")
        copiar.clicked.connect(lambda: self.ventana.copiar_resultado())
        limpiar = self.boton("Limpiar")
        limpiar.clicked.connect(self.reiniciar)
        botones.addWidget(copiar)
        botones.addWidget(limpiar)
        botones.addStretch(1)
        self.cuerpo.addLayout(botones)

        self.tarjeta = Tarjeta("SUMA")
        self.cuerpo.addWidget(self.tarjeta)

    def recalcular(self):
        # La coma es decimal y no separador: los signos + y los espacios ya
        # bastan para separar, asi "12,5" se lee como doce coma cinco.
        trozos = [t for t in re.split(r"[+;\s]+", self.campo.text().strip()) if t]
        if not trozos:
            self.tarjeta.fijar("—", "Escribe al menos un número", ROJO)
            return
        if len(trozos) > self.MAX:
            self.error(f"Como mucho {self.MAX} números a la vez.")
            return
        total, sumados, partes = 0.0, 0, []
        for trozo in trozos:
            valor = leer_numero(trozo)
            if valor is None:
                self.error(f"“{trozo}” no es un número.")
                return
            total += valor
            sumados += 1
            partes.append(formatear_numero(valor))
        self.tarjeta.fijar(formatear_numero(total),
                           f"{sumados} números: {' + '.join(partes)}", VERDE)
        self.avisar(f"Suma de {sumados} números: {formatear_numero(total)}")

    def iniciar(self):
        self.recalcular()

    def resultado(self):
        return self.tarjeta.cifra.text()

    def reiniciar(self):
        self.campo.setText("")
        self.tarjeta.fijar("—", "Escribe al menos un número")


# --------------------------------------------------------------------------
# Ventana principal y menu
# --------------------------------------------------------------------------
class VentanaPrincipal(QMainWindow):
    HERRAMIENTAS = [HerramientaNotas, HerramientaBases, HerramientaPorcentajes,
                    HerramientaUnidades, HerramientaContrasenas, HerramientaTexto,
                    HerramientaSuma]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Herramientas · PySide6")
        self.resize(860, 640)
        self.setMinimumSize(700, 540)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.instancias = []
        for clase in self.HERRAMIENTAS:
            herramienta = clase(self)
            self.instancias.append(herramienta)
            self.tabs.addTab(herramienta, clase.TITULO)
        self.setCentralWidget(self.tabs)
        self.tabs.currentChanged.connect(self.cambio_pestana)

        self.construir_menu()
        for herramienta in self.instancias:
            herramienta.iniciar()
        self.cambio_pestana(0)
        self.statusBar().showMessage("Listo. Pulsa F1 para ver la guía rápida.")

    # -- menu ------------------------------------------------------------
    def construir_menu(self):
        self.grupo = QActionGroup(self)
        self.grupo.setExclusive(True)

        herramientas = self.menuBar().addMenu("&Herramientas")
        for indice, herramienta in enumerate(self.instancias):
            accion = QAction(f"{indice + 1}   {herramienta.TITULO}", self)
            accion.setCheckable(True)
            accion.setShortcut(QKeySequence(f"Ctrl+{indice + 1}"))
            accion.triggered.connect(lambda _=False, i=indice: self.tabs.setCurrentIndex(i))
            self.grupo.addAction(accion)
            herramientas.addAction(accion)
            herramienta.accion = accion

        herramientas.addSeparator()
        copiar = QAction("Copiar resultado", self)
        copiar.setShortcut(QKeySequence("Ctrl+Shift+C"))
        copiar.setStatusTip("Copia el resultado de la herramienta activa")
        copiar.triggered.connect(self.copiar_resultado)
        herramientas.addAction(copiar)

        reiniciar = QAction("Reiniciar herramienta", self)
        reiniciar.setShortcut(QKeySequence("Ctrl+R"))
        reiniciar.setStatusTip("Vuelve a poner la herramienta activa en su estado inicial")
        reiniciar.triggered.connect(self.reiniciar_activa)
        herramientas.addAction(reiniciar)

        ayuda = self.menuBar().addMenu("A&yuda")
        guia = QAction("Guía rápida", self)
        guia.setShortcut(QKeySequence("F1"))
        guia.triggered.connect(self.guia_rapida)
        ayuda.addAction(guia)
        pistas = QAction("Atajos de teclado", self)
        pistas.triggered.connect(self.atajos)
        ayuda.addAction(pistas)
        acerca = QAction("Acerca de", self)
        acerca.triggered.connect(self.acerca_de)
        ayuda.addAction(acerca)

    # -- acciones del menu ----------------------------------------------
    def cambio_pestana(self, indice):
        if not 0 <= indice < len(self.instancias):
            return
        herramienta = self.instancias[indice]
        herramienta.accion.setChecked(True)
        self.statusBar().showMessage(f"{herramienta.TITULO} — {herramienta.RESUMEN}")

    def herramienta_activa(self):
        return self.instancias[self.tabs.currentIndex()]

    def copiar_resultado(self):
        texto = self.herramienta_activa().resultado()
        if not texto:
            self.statusBar().showMessage("Esta herramienta no tiene un resultado que copiar.")
            return
        QApplication.clipboard().setText(texto)
        self.statusBar().showMessage(f"Copiado: {texto}")

    def reiniciar_activa(self):
        self.herramienta_activa().reiniciar()
        self.statusBar().showMessage("Herramienta reiniciada.")

    def guia_rapida(self):
        QMessageBox.information(
            self, "Guía rápida",
            "La ventana tiene una pestaña por herramienta y el menú Herramientas\n"
            "salta entre ellas.\n\n"
            "Notas        media ponderada y qué nota falta para aprobar.\n"
            "Bases        decimal, binario, octal y hexadecimal sincronizados.\n"
            "Porcentajes  descuentos, IVA, aumentos, propinas y «X es el % de Y».\n"
            "Unidades     longitud, masa, tiempo, datos, volumen, área y temperatura.\n"
            "Contraseñas  generador con secrets y estimación de entropía.\n"
            "Texto        palabras, caracteres, líneas y tiempo de lectura.\n"
            "Suma         suma una lista de números.\n\n"
            "En todas se puede copiar el resultado y reiniciarlas.")

    def atajos(self):
        QMessageBox.information(
            self, "Atajos de teclado",
            "Ctrl+1 … Ctrl+7   Ir a cada herramienta\n"
            "Ctrl+Mayús+C      Copiar el resultado\n"
            "Ctrl+R            Reiniciar la herramienta activa\n"
            "F1                Guía rápida\n"
            "Ctrl+C / Ctrl+V   Copiar y pegar en los campos de texto\n"
            "Ctrl+1 … Ctrl+9   También funcionan mientras se escribe")

    def acerca_de(self):
        QMessageBox.about(
            self, "Acerca de Herramientas",
            "<h3>Herramientas · PySide6</h3>"
            "<p>Siete utilidades de escritorio en un único archivo.</p>"
            f"<p>Python {sys.version.split()[0]} · "
            f"PySide6 {PySide6.__version__}</p>"
            "<p>Las expresiones y conversiones se validan sin usar <code>eval</code>, "
            "y las contraseñas se generan con <code>secrets</code>.</p>")


# --------------------------------------------------------------------------
# Arranque
# --------------------------------------------------------------------------
def hay_pantalla():
    if os.environ.get("QT_QPA_PLATFORM") in ("offscreen", "minimal"):
        return False
    if sys.platform == "darwin" or sys.platform == "win32":
        return True
    return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def guardar_imagen(aplicacion, ventana, base):
    ventana.resize(880, 660)
    ventana.show()
    aplicacion.processEvents()
    rutas = []
    for indice in range(ventana.tabs.count()):
        ventana.tabs.setCurrentIndex(indice)
        aplicacion.processEvents()
        titulo = re.sub(r"[^a-z0-9]+", "-",
                        ventana.tabs.tabText(indice).lower().replace("ñ", "n")).strip("-")
        ruta = f"{base}-{indice + 1}-{titulo}.png"
        if ventana.grab().save(ruta):
            rutas.append(ruta)
        else:
            print("No se pudo guardar la imagen en", ruta)
            return 1
    for ruta in rutas:
        print("Imagen guardada en", os.path.abspath(ruta))
    return 0


def main():
    opciones = argparse.ArgumentParser(description="Menu de herramientas con PySide6")
    opciones.add_argument(
        "--captura",
        metavar="ARCHIVO",
        nargs="?",
        const="herramientas",
        help="Guarda un PNG por herramienta en vez de abrir la ventana.",
    )
    argumentos = opciones.parse_args()

    if argumentos.captura or not hay_pantalla():
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    aplicacion = QApplication([sys.argv[0]])
    aplicacion.setStyle("Fusion")
    aplicacion.setStyleSheet(ESTILO)
    aplicacion.setApplicationName("Herramientas")

    ventana = VentanaPrincipal()

    if argumentos.captura or not hay_pantalla():
        return guardar_imagen(aplicacion, ventana, argumentos.captura or "herramientas")

    ventana.show()
    return aplicacion.exec()


if __name__ == "__main__":
    raise SystemExit(main())
