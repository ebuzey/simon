# simon.py

import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette
# Si usas PyQt5 versiones recientes, es preferible usar QGuiApplication
from PyQt5.QtGui import QGuiApplication

class SimonGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.sequence = []
        self.user_sequence = []
        self.level = 0
        self.accepting_input = False

    def initUI(self):
        # Configurar la ventana
        self.setWindowTitle('Simon: Teclas de Movimiento')
        self.setFixedSize(300, 300)  # Establece un tamaño fijo para la ventana

        # Posicionar la ventana en la esquina inferior derecha
        self.position_window_bottom_right()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Crear una etiqueta para mostrar la puntuación
        self.score_label = QLabel('Puntuación: 0', self)
        self.score_label.setFont(QFont('Arial', 14))
        self.score_label.setStyleSheet('color: white')
        self.score_label.move(100, 10)

        # Crear botones para las teclas de movimiento
        self.buttons = {}
        positions = {
            'up': (100, 50),
            'left': (-2, 102),
            'right': (202, 102),
            'down': (100, 102)
        }

        for key, pos in positions.items():
            btn = QPushButton(self)
            btn.setText(self.get_arrow_symbol(key))
            btn.setFont(QFont('Arial', 24))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(85, 85, 85, 180);
                    border: 2px solid #555;
                    border-radius: 10px;
                    color: white;
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 0, 180);
                    color: black;
                }
            """)
            btn.setGeometry(pos[0], pos[1], 100, 50)
            btn.clicked.connect(lambda checked, k=key: self.handle_user_input(k))
            self.buttons[key] = btn

        # Crear botón de inicio
        self.start_button = QPushButton('Comenzar', self)
        self.start_button.setFont(QFont('Arial', 12))
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                border: none;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.start_button.setGeometry(100, 220, 100, 40)
        self.start_button.clicked.connect(self.start_game)

        # Crear etiqueta para mensajes
        self.message_label = QLabel('', self)
        self.message_label.setFont(QFont('Arial', 12))
        self.message_label.setStyleSheet('color: white')
        self.message_label.setGeometry(50, 270, 200, 20)

    def position_window_bottom_right(self):
        """Posiciona la ventana en la esquina inferior derecha de la pantalla."""
        # Obtener el objeto de pantalla
        app = QGuiApplication.instance()
        if app is None:
            app = QGuiApplication(sys.argv)

        screen = app.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Obtener el tamaño de la ventana
        window_size = self.size()

        # Calcular la posición x e y
        x = screen_geometry.width() - window_size.width() - 10  # 10 píxeles de margen desde el borde
        y = screen_geometry.height() - window_size.height() - 40  # 40 píxeles para la barra de tareas

        self.move(x, y)

    def get_arrow_symbol(self, key):
        symbols = {
            'up': '⬆️',
            'left': '⬅️',
            'right': '➡️',
            'down': '⬇️'
        }
        return symbols.get(key, '')

    def start_game(self):
        self.sequence = []
        self.user_sequence = []
        self.level = 0
        self.score_label.setText(f'Puntuación: {self.level}')
        self.message_label.setText('')
        QTimer.singleShot(500, self.next_round)

    def next_round(self):
        self.level += 1
        self.score_label.setText(f'Puntuación: {self.level}')
        next_key = random.choice(['up', 'left', 'right', 'down'])
        self.sequence.append(next_key)
        self.play_sequence()

    def play_sequence(self):
        self.accepting_input = False
        self.user_sequence = []
        delay = 1000  # Retraso inicial
        for key in self.sequence:
            QTimer.singleShot(delay, lambda k=key: self.activate_key(k))
            delay += 700  # Intervalo entre teclas
        QTimer.singleShot(delay, lambda: setattr(self, 'accepting_input', True))

    def activate_key(self, key):
        btn = self.buttons[key]
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 0, 180);
                border: 2px solid #555;
                border-radius: 10px;
                color: black;
            }
        """)
        # Opcional: Reproducir sonido aquí
        QTimer.singleShot(300, lambda: btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(85, 85, 85, 180);
                border: 2px solid #555;
                border-radius: 10px;
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 0, 180);
                color: black;
            }
        """))

    def handle_user_input(self, key):
        if not self.accepting_input:
            return
        self.user_sequence.append(key)
        self.activate_key(key)
        current_step = len(self.user_sequence) - 1
        if self.user_sequence[current_step] != self.sequence[current_step]:
            self.game_over()
            return
        if len(self.user_sequence) == len(self.sequence):
            self.accepting_input = False
            QTimer.singleShot(1000, self.next_round)

    def game_over(self):
        self.message_label.setText('¡Juego Terminado!')
        self.accepting_input = False
        # Opcional: Reproducir sonido de error aquí

    # Hacer la ventana arrastrable
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

def main():
    app = QApplication(sys.argv)
    game = SimonGame()
    game.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
