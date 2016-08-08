#Definition of a block.
import copy


class Block:
    """
        A block contains mouvements.
    """

    def __init__(self, id, max_size):
        self._id = id
        self._elems = []
        self.max_size = max_size

    def get_id(self):
        return self._id

    def add_elem(self, element):
        """
            return true if an element can be added to the block.
            Otherwise the blockchain has to generate a new block.
        """
        if len(self._elems) == self.max_size:
            return False
        else:
            self._elems.append(element)
            return True

    def add_list_elems(self, elements):
        if  len(self._elems) + len(elements) <= self.max_size :
            for elem in elements:
                self._elems.append(elem)
            return True
        else:
            return False

    def get_elems(self):
        """
            Expose elements of the block, for printing or linear search
        """
        return copy.deepcopy(self._elems)

    def get_str(self):
        return [str(e) for e in self._elems]

