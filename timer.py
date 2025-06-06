import sys
import os
import keyboard
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QFont, QFontDatabase, QKeyEvent

VERSION = "1.0.0"

# Configuración de mensajes y sus tiempos
MESSAGES = {
    20: "PROBABILIDAD DE DEMONIO",
    60: "PROBABILIDAD DE DEMONIO\nSI USASTE INCIENSO",
    90: "ATAQUE NORMAL NO ES D NI E",
    180: "ESPIRITU PROBABLE"
}

def load_custom_fonts():
    """Carga todas las fuentes personalizadas de la carpeta fonts"""
    if getattr(sys, 'frozen', False):
        # Si es un ejecutable
        fonts_dir = os.path.join(sys._MEIPASS, 'fonts')
    else:
        # Si es desarrollo
        fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
    
    custom_font = None
    
    if os.path.exists(fonts_dir):
        for file in os.listdir(fonts_dir):
            if file.lower().endswith(('.ttf', '.otf')):
                font_path = os.path.join(fonts_dir, file)
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    custom_font = QFontDatabase.applicationFontFamilies(font_id)[0]
                    print(f"Fuente cargada: {custom_font}")
                    break
    else:
        print(f"Directorio de fuentes no encontrado: {fonts_dir}")
    
    return custom_font

class MessageWindow(QMainWindow):
    def __init__(self, font_size=24, custom_font=None):
        super().__init__()
        self.font_size = font_size
        self.custom_font = custom_font
        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        
        screen = QApplication.primaryScreen().geometry()
        self.width = 600  # Reducido para ajustarse mejor a la esquina
        self.height = 100  # Reducido para ser más compacto
        
        # Posicionar en la esquina superior derecha
        self.setGeometry(
            screen.width() - self.width - 10,  # 10 píxeles desde la derecha
            10,  # 10 píxeles desde arriba
            self.width,
            self.height
        )
        
        self.label = QLabel('', self)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Alineado a la derecha
        self.label.setWordWrap(True)
        
        if self.custom_font:
            self.label.setFont(QFont(self.custom_font, self.font_size, QFont.Bold))
        else:
            self.label.setFont(QFont('Arial', self.font_size, QFont.Bold))
            
        self.label.setStyleSheet('color: red; background-color: transparent;')
        self.label.setGeometry(0, 0, self.width, self.height)
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        
    def showMessage(self, message, duration=3000):
        self.label.setText(message)
        self.show()
        QTimer.singleShot(duration, self.hide)

class InfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"PhasmoTimer v{VERSION}")
        self.setGeometry(100, 100, 350, 100)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        layout = QVBoxLayout()
        label = QLabel("Temporizador listo. Se minimizará en un segundo.\nAtajos: Ctrl+R (Reiniciar), Ctrl+X (Limpiar).")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)
        
        # Minimizar automáticamente después de 1 segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showMinimized)
        self.timer.setSingleShot(True)  # El timer solo se ejecutará una vez
        self.timer.start(1000)

class Timer(QMainWindow):
    def __init__(self, width=250, height=50, custom_font=None):
        super().__init__()
        self.seconds = 0
        self.width = width
        self.height = height
        self.custom_font = custom_font
        self.message_window = MessageWindow(font_size=32, custom_font=custom_font)
        self.timer_active = False
        self.oldPos = None
        self.check_hotkeys_timer = QTimer()
        self.check_hotkeys_timer.timeout.connect(self.check_hotkeys)
        self.check_hotkeys_timer.start(100)  # Revisar cada 100ms
        self.initUI()
        self.showWelcomeMessage()

    def showWelcomeMessage(self):
        self.info = InfoWindow()
        self.info.show()

    def check_hotkeys(self):
        try:
            if keyboard.is_pressed('ctrl+r'):
                self.resetTimer()
            elif keyboard.is_pressed('ctrl+x'):
                self.clearTimer()
        except:
            pass  # Ignorar cualquier error de keyboard

    def initUI(self):
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(
            (screen.width() - self.width) // 2,
            10,
            self.width,
            self.height
        )
        
        self.label = QLabel('00:00', self)
        self.label.setAlignment(Qt.AlignCenter)
        
        if self.custom_font:
            self.label.setFont(QFont(self.custom_font, 34, QFont.Bold))
        else:
            self.label.setFont(QFont('Arial', 34, QFont.Bold))
            
        self.label.setStyleSheet('color: #e6ebec; background-color: transparent;')
        layout.addWidget(self.label)
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)
        
        self.startTimer()
        self.show()

    def startTimer(self):
        if not self.timer_active:
            self.timer.start(1000)
            self.timer_active = True
    
    def stopTimer(self):
        if self.timer_active:
            self.timer.stop()
            self.timer_active = False
    
    def showMessage(self, message, duration=3000):
        self.message_window.showMessage(message, duration)
    
    def updateTimer(self):
        if self.seconds > 180:  # Cambiado de >= a > para permitir mostrar 3:00
            self.stopTimer()
            self.seconds = 180
            minutes = self.seconds // 60
            secs = self.seconds % 60
            self.label.setText(f'{minutes:02d}:{secs:02d}')
            return

        minutes = self.seconds // 60
        secs = self.seconds % 60
        self.label.setText(f'{minutes:02d}:{secs:02d}')
        
        if self.seconds in MESSAGES:
            self.showMessage(MESSAGES[self.seconds])
            
        self.seconds += 1
    
    @pyqtSlot()
    def resetTimer(self):
        self.seconds = 0
        self.message_window.hide()
        self.stopTimer()  # Primero detenemos el temporizador
        self.startTimer()  # Luego lo iniciamos de nuevo
    
    @pyqtSlot()
    def clearTimer(self):
        self.seconds = 0
        self.label.setText('00:00')
        self.message_window.hide()
        self.stopTimer()
    
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        
    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def keyPressEvent(self, event: QKeyEvent):
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_R:
                self.resetTimer()
            elif event.key() == Qt.Key_X:
                self.clearTimer()
        super().keyPressEvent(event)

    def closeEvent(self, event):
        self.check_hotkeys_timer.stop()
        super().closeEvent(event)

if __name__ == '__main__':
    width = 250
    height = 50
    if len(sys.argv) > 2:
        try:
            width = int(sys.argv[1])
            height = int(sys.argv[2])
        except ValueError:
            print("Por favor, introduce números válidos para el ancho y alto")
            sys.exit(1)
    
    app = QApplication(sys.argv)
    custom_font = load_custom_fonts()
    timer = Timer(width, height, custom_font)
    sys.exit(app.exec_()) 