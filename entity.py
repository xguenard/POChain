#Definition of an entity in the blockchain
import movement
import data_models
from PySide import QtCore

class Entity:
    """
        Contains id, type, and general information of an entity.
        It can be a bank, a seller etc...
    """
   
    changed = QtCore.Signal()
    def __init__(self, name, id, type, queue, create_queue):
        super().__init__()
        self.name = name
        self.id = id

        self.related_tx = data_models.MvtListModel()
        self.recv_tx = []
        self.send_tx = []
        self.refused_tx = []
        self.type = type

        self.mvt_queue = queue
        self.create_q = create_queue

        self.status = "Peer not authentified"
        self.tx_origin = -1

    
    def __str__(self):
        return ("{name} - (id = {id})").format(name = self.name\
                , id = self.id)

    def get_label(self):
        return ("{name} - {ps} - (id = {id})").format(name = self.name\
                , id = self.id, ps = self.status)
    
    def get_tx_list(self):
        return self.related_tx


    def check_mvt(self, mvt):
        """
            Check if a movement is valid
        """
        if mvt.send_id == self.id or self.id in mvt.recv_id:
            self.related_tx.addElem(mvt)

        if self.id in mvt.recv_id and mvt.cmd == movement.new_peer_str:
            if mvt.is_valid():
                print("checking mvt")
                self.status = "Authentified peer"
                self.tx_origin = mvt.tx_id

    def create_mvts(self, recv_id, tx_ref, cmd):
        """
            Create an mvt
        """
        new_mvt = movement.Movement()
        new_mvt.fill_mvt(self.id, recv_id, self.type, "tx" \
                , tx_ref, cmd)
        self.mvt_queue.put(new_mvt)

    def original_mvt(self, mvt):
        """
            First movement of a peer, requesting to be in the world
        """
        mvt.recv_id = [self.id]
        mvt.recv_type = self.type
        self.mvt_queue.put(mvt)

    def create_peer(self, name, type):
        """
            create a new peer
        """
        new_mvt = movement.Movement()
        new_mvt.fill_mvt(self.id, 0, self.type, 0, self.tx_origin\
                , movement.new_peer_str)
        self.create_q.put([name, type, new_mvt])
