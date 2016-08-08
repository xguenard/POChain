#Class used to simulate the behavior of a blockchain.
#It can receive orders from peers, execute and save them in the blockchain.

import threading
import queue
import time

#self defined classes
import block
import movement

class Blockchain(threading.Thread):
    """
        A blockchain will add mvt to block if they are respecting the rules
    """
    def __init__(self, max_iter, timing, block_size):
        super().__init__()
        self.block_id = 0
        self.tx_id = 0

        self.block_list = []    
        self.tx_list = {0 : movement.Movement()}

        self.pending_mvts = queue.Queue(maxsize=0)
        self.result_pending = queue.Queue(maxsize=0)
        
        self.max_iter = max_iter
        self.timing = timing
        self.block_size = block_size

        self.test_ok = False
        self.gui = None
    
    def get_queue(self):
        """
            Return queues for synchronisation
        """
        return [self.pending_mvts, self.result_pending]
    
    def set_guit(self, block_gui):
        self.gui = block_gui
    def update_gui(self, elems):
        if self.gui:
            self.gui.add_elem(elems)
    
    def run(self):
        """
            Process pending mvts and  generate blocks every X secondes
        """
        for t in range(0, self.max_iter):
            print("round #{}".format(t))
            time.sleep(self.timing)
            new_block_data = self.process_pending()
            self.update_gui(new_block_data)
            
            
            if new_block_data:
                print("DATA ADDED THIS  ROUND :\n", *new_block_data)
                new_block = block.Block(self.block_id, self.block_size)
                new_block.add_list_elems(new_block_data)
                self.block_list.append(new_block)

                self.block_id += 1

        self.test_ok = True

    def process_pending(self):
        """
            Process orders in the pending_mvts queue.
            Return a list of mvt to add in the new block
        """
        counter = self.block_size
        new_block_data = []

        while (not self.pending_mvts.empty()) and counter > 0 :
            new_mvt = self.pending_mvts.get()
            ref_id = new_mvt.get_ref_mvt()

            try:
                ref_mvt = self.tx_list[ref_id]
            except:
                ref_mvt = movement.Movement()

            print(ref_mvt)
            print(new_mvt)
            movement.check(ref_mvt, new_mvt)

            new_mvt.set_id(self.tx_id)
            self.tx_list[self.tx_id] = new_mvt
            self.tx_id += 1
            new_block_data.append(new_mvt)

            self.result_pending.put(new_mvt)
            self.pending_mvts.task_done()

        return new_block_data
