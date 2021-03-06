from PyQt5 import QtWidgets, QtCore, QtWidgets
import threading
import sys
import movement
import block_gui

class MvtList(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.label = QtWidgets.QLabel("TRANSACTIONS LINKED TO THE SELECTED ENTITY")

        self.list_view = QtWidgets.QListView()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.list_view)
        self.setLayout(layout)

    def set_entity(self, entity):
        self.model = entity.get_tx_list()
        self.entity = entity
        self.list_view.setModel(self.model)
        self.update()

class EntityList(QtWidgets.QWidget):
    """
        Manage list of entities created in the blockchain
        Is connected to a form entity 
    """
    def __init__(self, model, form, mvt_list):
        super().__init__()
        self.model = model
        self.mvt_list = mvt_list
        self.form = form
        self.label = QtWidgets.QLabel("ENTITIES IN THE NETWORK")
        self.list_view = QtWidgets.QListView()
        self.list_view.clicked.connect(self.selected)

        self.list_view.setModel(self.model)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.list_view)
        self.setLayout(layout)

    def selected(self, index):
        """
            When I select an elem in the list I am able to modify it
        """
        current_entity = self.model.get_entity(index)
        self.form.set_entity(current_entity)
        self.mvt_list.set_entity(current_entity)


class FormEntity(QtWidgets.QWidget):
    """
        Widget used to create new movmements with entities
    """
    def __init__(self):
        super().__init__()
        self.initUI()
        self.entity = None

    def initUI(self):
        layout = QtWidgets.QFormLayout()
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label = QtWidgets.QLabel("SELECT AN ENTITY IN THE LIST")
        self.label.setStyleSheet('color:blue')
        layout.addRow(self.label)
        layout.addRow(line)

###### CREATE PEER INITIALIZATION ######
        
        self.line_txt = QtWidgets.QLineEdit("PEER NAME")
        self.btn = QtWidgets.QPushButton("CREATE PEER")
        label_2 = QtWidgets.QLabel("PEER CREATION INTERFACE")
        label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.list_text = list(movement.dico_types.keys())
        self.cmb_box = QtWidgets.QComboBox()
        self.cmb_box.addItems(self.list_text)
        
        self.btn.clicked.connect(self.create_entity)
        layout.addRow(label_2)
        layout.addRow("PEER ROLE ",self.cmb_box)
        layout.addRow("PEER NAME ",self.line_txt)
        layout.addRow("",self.btn)

###### END OF CREATE PEER INITIALIZATION ######
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addRow(line)

######  CREATE MVT  INITIALIZATION ######
        label_2 = QtWidgets.QLabel("TRANSACTION CREATION INTERFACE")
        label_2.setAlignment(QtCore.Qt.AlignCenter)
        layout.addRow(label_2)

        self.list_cmd = movement.all_cmd_str
        self.cmb_box2 = QtWidgets.QComboBox()
        self.cmb_box2.addItems(self.list_cmd)
        layout.addRow("ORDER TYPE ", self.cmb_box2)

        self.line_id = QtWidgets.QLineEdit()
        layout.addRow("COUNTERPARTY ID",self.line_id)

        self.line_tx = QtWidgets.QLineEdit()
        layout.addRow("REFERENCE TRANSACTION ID", self.line_tx)

        self.btn2 = QtWidgets.QPushButton("CREATE TRANSACTION")
        self.btn2.clicked.connect(self.create_mvt)
        layout.addRow("", self.btn2)

######  END OF CREATE MVT  INITIALIZATION ######
        self.setLayout(layout)

    def set_entity(self, entity):
        self.entity = entity
        self.label.setText(self.entity.get_label())

    def create_entity(self):
        if self.entity:
            name = self.line_txt.text()
            type = movement.dico_types[self.list_text[\
                    self.cmb_box.currentIndex()]]
            self.entity.create_peer(name, type)

    def create_mvt(self):
        if self.entity:
            cmd = self.list_cmd[self.cmb_box2.currentIndex()]
            target_id = [int(s) for s in (self.line_id.text()).split(',')]
            tx_id = int(self.line_tx.text())
            self.entity.create_mvts(target_id, tx_id, cmd)



class MainWindow(QtWidgets.QWidget):
    def __init__(self, model_entities):
        super().__init__()
        self.model_entities = model_entities
        self.initUI()
    
    def initUI(self):
        self.setGeometry(50, 50, 1400, 900)
        h_layout = QtWidgets.QHBoxLayout()
        v_layout = QtWidgets.QVBoxLayout()
        # First part the list
        self.form = FormEntity()
        self.mvt_list = MvtList()
        self.list_view_entity = EntityList(self.model_entities\
                , self.form, self.mvt_list)
        v_layout.addWidget(self.list_view_entity)
        
        v_layout.addWidget(self.mvt_list)

        #Secon part the formdialog
        v_layout.addWidget(self.form)
        
        h_layout.addLayout(v_layout)

        self.block_ui = block_gui.BlockchainWindow(self.size())

        v_layout2 = QtWidgets.QVBoxLayout()
        annex_widget = QtWidgets.QMainWindow()
        annex_widget.setCentralWidget(self.block_ui)
        v_layout2.addWidget(annex_widget)
        h_layout.addLayout(v_layout2)
        self.setLayout(h_layout)
        self.block_ui.update()
        self.show()

    def get_block_ui(self):
        return self.block_ui


class GuiThread:
    def __init__(self, entity_model):
        self.entity_model = entity_model
        

    def load(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = MainWindow(self.entity_model)

    def run(self):
        self.app.exec_()

    def get_block(self):
        return self.main_window.get_block_ui()
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    app.exec_()
