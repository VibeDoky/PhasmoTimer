# PhasmoTimer

PhasmoTimer es una herramienta diseñada para llevar un control de los tiempos de ataque de los fantasmas. Este temporizador muestra alertas en momentos específicos, ayudándote a identificar el tipo de fantasma basándose en sus patrones de ataque.

## Características

- ⏱️ Temporizador para rastrear ataques de fantasmas
- 🔔 Alertas automáticas en momentos clave:
  - 20s: Probabilidad de Demonio
  - 60s: Probabilidad de Demonio (si se usó incienso)
  - 90s: Ataque normal (no es Demonio ni Espíritu)
  - 180s: Probable Espíritu (si se usó incienso)
  - (si se usó incienso)) Se tiene que contar el tiempo desde que se tiro el incienso.
- 📌 Siempre visible encima de otras ventanas
- ⌨️ Atajos de teclado para control rápido

## Instalación

### Opción 1: Ejecutable (.exe)
1. Descarga el archivo `PhasmoTimer.exe`
2. Ejecuta el archivo directamente (no requiere instalación)

### Opción 2: Desde el código fuente (Python)
1. Clona el repositorio:
```bash
git clone [URL del repositorio]
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta el programa:
```bash
python timer.py
```

## Requisitos (para ejecutar con Python)
- Python 3.x
- PyQt5
- keyboard

## Uso

### Atajos del sistema
- `Ctrl + R`: Reiniciar temporizador
- `Ctrl + X`: Detener y limpiar temporizador
- `X` en la ventana emergente: Cerrar el programa

### Alertas
El temporizador mostrará automáticamente alertas en la esquina superior derecha de tu pantalla en momentos específicos para ayudarte a identificar el tipo de fantasma basado en sus patrones de ataque.

## Contribuir
Las contribuciones son bienvenidas. Por favor, siente libre de:
- Reportar bugs
- Sugerir nuevas características
- Crear pull requests

## Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Discord
d.o_k.y


---
⚠️ **Nota**: PhasmoTimer es una herramienta no oficial y no está afiliada con Kinetic Games o Phasmophobia. 