# Visual app to create a ring signature and store the proof in a nft 
# It uses PyQt5 

from PyQt5.QtWidgets import QApplication,QDesktopWidget, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
import sys
sys.path.append('../')
from main import getProof

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'ring proof'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 240
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create labels
        label1 = QLabel('Secret key to sign:', self)
        label1.move(20, 20)
        label2 = QLabel('Secret key to receive NFT:', self)
        label2.move(20, 60)
        label3 = QLabel('Amount to prove:', self)
        label3.move(20, 100)

        # Create input fields
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(180, 20)
        self.textbox1.resize(140, 20)
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(180, 60)
        self.textbox2.resize(140, 20)
        self.textbox3 = QLineEdit(self)
        self.textbox3.move(180, 100)
        self.textbox3.resize(140, 20)

        # Create button
        button = QPushButton('Prove', self)
        button.setToolTip('Click to prove')
        button.move(140, 160)
        button.clicked.connect(self.on_button_click)
        self.show()

    def on_button_click(self):
        # Import function and call it with the inputs
       
        secret_key_sign = self.textbox1.text()
        secret_key_receive = self.textbox2.text()
        amount = self.textbox3.text()
        a = int(amount)
        if( getProof(a, secret_key_sign,secret_key_receive)):
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("You have mint your proof")
            msg.exec_()
        else : 
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("Error while minting your proof, ensure that you hold enough funds")
            msg.exec_()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
