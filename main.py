import sys
from view.app import ContextoApp
from PyQt6.QtWidgets import QApplication
from utils import load_data



def main() -> None:
    words, matrix = load_data()

    app = QApplication(sys.argv)
    app.setApplicationName("Contexto")
    window = ContextoApp(words, matrix)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()