# Visual app to verify proof
# It uses PyQt5 

from PyQt5.QtWidgets import QApplication,QMessageBox, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import ast
import sys
sys.path.append('../ring_signature')
from hackyaosring import haosring_check
class ProofApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("proof verifier")

        # Create input field and button
        self.proof_input = QLineEdit()
        self.proof_button = QPushButton("Submit")
        self.proof_button.clicked.connect(self.handle_proof)

        # Create layout and add input field and button
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Proof:"))
        self.layout.addWidget(self.proof_input)
        self.layout.addWidget(self.proof_button)

        # Set layout
        self.setLayout(self.layout)

    def handle_proof(self):
        proof = self.proof_input.text()
        tempo = ast.literal_eval(proof)
        verified = haosring_check(*tempo)
        if(verified):
        # Add pop-up notification here
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("The proof is VALID")
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("The proof is INVALID")
            msg.exec_()
if __name__ == '__main__':
    app = QApplication([])
    proof_app = ProofApp()
    proof_app.show()
    app.exec_()
