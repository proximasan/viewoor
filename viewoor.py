from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPlainTextEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
import json
import sys

class DropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def closeEvent(self, event):
        print("Closing application...")
        QApplication.quit()


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
            # Remove all existing widgets from the layout
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for filepath in files:
            with open(filepath, 'rb') as f:
                contents = f.read().decode(errors='ignore')

            lora_start = contents.find('"lora_name": "')
            seed_start = contents.find('"seed": ')
            steps_start = contents.find('"steps": ')
            cfg_start = contents.find('"cfg": ')
            sampler_name_start = contents.find('"sampler_name": "')
            text_start = contents.find('"text": "')
            second_text_start = contents.find('"text": "', text_start + 1)
            ckpt_name_start = contents.find('"ckpt_name": "')
            if ckpt_name_start != -1:
                ckpt_name_start += len('"ckpt_name": "')
                ckpt_name_end = contents.find('"', ckpt_name_start)
                ckpt_name = contents[ckpt_name_start:ckpt_name_end]
            else:
                ckpt_name = None


            if all([lora_start != -1, seed_start != -1, steps_start != -1, 
                cfg_start != -1, sampler_name_start != -1, 
                text_start != -1, second_text_start != -1,
                ckpt_name_start != -1]):  # Add ckpt_name_start != -1


                lora_start += len('"lora_name": "')
                lora_end = contents.find('.safetensors"', lora_start)
                lora_name = contents[lora_start:lora_end]

                seed_start += len('"seed": ')
                seed_end = contents.find(',', seed_start)
                seed = contents[seed_start:seed_end]

                steps_start += len('"steps": ')
                steps_end = contents.find(',', steps_start)
                steps = contents[steps_start:steps_end]

                cfg_start += len('"cfg": ')
                cfg_end = contents.find(',', cfg_start)
                cfg = contents[cfg_start:cfg_end]

                sampler_name_start += len('"sampler_name": "')
                sampler_name_end = contents.find('"', sampler_name_start)
                sampler_name = contents[sampler_name_start:sampler_name_end]

                text_start += len('"text": "')
                text_end = contents.find('", "clip"', text_start)
                text = contents[text_start:text_end]

                second_text_start += len('"text": "')
                second_text_end = contents.find('", "clip"', second_text_start)
                second_text = contents[second_text_start:second_text_end]

                info = (f'Lora Name: {lora_name}\n'
                        f'Seed: {seed}\n'
                        f'Steps: {steps}\n'
                        f'Cfg: {cfg}\n'
                        f'Sampler Name: {sampler_name}\n'
                        f'Text: {text}\n'
                        f'Second Text: {second_text}')

                self.layout.addWidget(self.create_info_widget('Lora Name', lora_name, True))
                self.layout.addWidget(self.create_info_widget('Ckpt Name', ckpt_name, True))
                self.layout.addWidget(self.create_info_widget('Seed', seed, True))
                self.layout.addWidget(self.create_info_widget('Steps', steps, True))
                self.layout.addWidget(self.create_info_widget('Cfg', cfg, True))
                self.layout.addWidget(self.create_info_widget('Sampler Name', sampler_name, True))
                self.layout.addWidget(self.create_info_widget('Prompt', text, True))
                self.layout.addWidget(self.create_info_widget('Negative', second_text, True))

            else:
                # Clear all widgets from the layout
                for i in reversed(range(self.layout.count())): 
                    self.layout.itemAt(i).widget().setParent(None)

                # Display error message
                self.layout.addWidget(QLabel('Could not find all required fields in file contents.'))

    def create_info_widget(self, label, text, with_copy_button=False):
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)

        label_widget = QLabel(f'{label}: {text}')
        label_widget.setWordWrap(True)
        layout.addWidget(label_widget)

        if with_copy_button:
            button = QPushButton('⧉')
            button.setMaximumWidth(70)

            def on_button_clicked():
                QApplication.clipboard().setText(text)
                button.setText('✓')
                QTimer.singleShot(1000, lambda: button.setText('⧉'))  # change the text back after 2 seconds

            button.clicked.connect(on_button_clicked)
            layout.addWidget(button)

        return widget


app = QApplication(sys.argv)
app.setWindowIcon(QIcon('icon.png'))
app.aboutToQuit.connect(app.quit)  # Add this line

window = DropWidget()
window.setFixedSize(800, 600)
window.setWindowTitle("☆━━━━VIEWOOR━━━━☆")  # Add this line
window.show()


app.exec_()
