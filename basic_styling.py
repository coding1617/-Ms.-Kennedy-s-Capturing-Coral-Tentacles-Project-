def get_basic_styling():
    return """
        QLabel {
            color: #00abd5;
            font-family: 'Lucida Sans Typewriter';
            font-size: 17px;
            font-weight: bold;
        }

        QPushButton {
            color: white;
            background-color: #3f72af;
            font-family: 'Lucida Sans Typewriter';
            font-size: 17px;
            font-weight: bold;
            border-radius: 15px;
            padding: 10px 20px;
        }

        QPushButton:hover {
            background-color: #00abd5;
        }

        QLineEdit {
            font-size: 17px;
            font-family: 'Lucida Sans Typewriter';
        }
    """