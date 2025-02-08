import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from urllib.parse import unquote  # Import unquote to decode the URL

class BrokerWindow(QMainWindow):
    def __init__(self, broker_url):
        super().__init__()

        self.setWindowTitle('FinoFxAlgo - Broker Window')
        self.setGeometry(100, 100, 1200, 800)

        # Create a layout and add the QWebEngineView
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Decode the URL that was passed
        decoded_url = unquote(broker_url)

        # Log the decoded URL to ensure it's correct
        print(f"Decoded URL: {decoded_url}")

        # WebEngineView to display the broker page
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(decoded_url))  # Load the decoded URL
        layout.addWidget(self.browser)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Ensure a URL is passed as a command-line argument
    if len(sys.argv) > 1:
        broker_url = sys.argv[1]  # Get the broker URL
    else:
        broker_url = "https://www.google.com"  # Default to Google if no URL is provided

    # Create the window and load the broker URL
    window = BrokerWindow(broker_url)
    window.show()

    sys.exit(app.exec_())
