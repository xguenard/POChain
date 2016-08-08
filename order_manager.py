import queue

#self defined classes
import movement


class OrderManager:

    def __init__(self, pending_mvts):
        self.pending_mvts = pending_mvts
        self.last_id = 1

    def get_id(self):
        tmp = self.last_id
        self.last_id += 1
        return tmp

    def create_entity(self, peer_id, peer_type, new_type, name):
        """
            Create an mvt to add a new entity in the network
        """
        new_mvt = movement.Movement()
        new_mvt.fill_mvt(peer_id, self.get_id(), peer_type, new_type\
                , 0, "new_joiner")
        new_mvt.set_name(name)
        self.pending_mvts.put(new_mvt)

    
    def create_mvt(self, peer_id, peer_type, target_id\
            , target_type, ref_tx, cmd):
        """
            Create any other kind of mvt
        """
        new_mvt = movement.Movement()
        new_mvt.fill_mvt(peer_id, target_id, peer_type, target_type\
                , ref_tx, cmd)
        self.pending_mvts.put(new_mvt)

