#This classe is used to simulate a network of elements.
#For the moment it's really basic, if needed it can be improved.
#libs
import threading
import queue
import time

#self defined classes
import entity
import movement
import data_models

class PeerManager(threading.Thread):

    def __init__(self, result_pending, pending_mvts):
        super().__init__()
        self.peers_list = []
        self.peer_id = 0

        self.results  = result_pending
        self.new_mvts = pending_mvts

        self.create_req = queue.Queue()

        self.entities_gui = data_models.EntityListModel() 

    def run(self):
        while True:
            time.sleep(0.5)
            self.process_create_q()
            self.process_results()

    def get_model_list(self):
        return self.entities_gui

    def get_peer_id(self):
        self.peer_id += 1
        return self.peer_id

    def create_new_peer(self, type, name, mvt):
        new_entity = entity.Entity(name, self.get_peer_id(), type\
                , self.new_mvts, self.create_req)
        new_entity.original_mvt(mvt)
        self.peers_list.append(new_entity)
        self.entities_gui.addElem(new_entity)

    def process_create_q(self):
        """
            Process the queues where new peer requests are made
        """
        while not self.create_req.empty():
            [new_name, new_type, mvt] = self.create_req.get()
            self.create_new_peer(new_type, new_name, mvt)
            self.create_req.task_done()

    def process_results(self):
        """
            Process the result queue and create new peers if needed
            of refresh the peer tx list
        """

        while not self.results.empty():
            mvt = self.results.get()

            for peer in self.peers_list:
                peer.check_mvt(mvt)

            self.results.task_done()
