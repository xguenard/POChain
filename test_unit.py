import blockchain
import movement

class simple_order():
    def run( description):
        return [True, ["test"]]
    def get_id():
        return 0



def is_valid(desc):
    return True

class TestBlockchain():

    def test_simple_blockchain(self):
        try:
            my_blockchain = blockchain.Blockchain(["empty"], 10, 0.1, 10)
            my_blockchain.pending_mvts.put(simple_order)
            my_blockchain.start()
            my_blockchain.join()
        except Exception as e:
            print(e)
            assert False
        else:
            assert True











class TestMovement():

    def test_movement_1(self):
       empty_mvt = movement.Movement() 
       creation_mvt = movement.Movement()
       creation_mvt.fill_mvt(0, 0, 1, 2, 0, "new_joiner")

       movement.check(empty_mvt, creation_mvt)
       assert creation_mvt.is_valid()

    def test_movement_2(self):
        old_mvt = movement.Movement()
        old_mvt.fill_mvt(0, 10, 1, 3, 0, "new_joiner")
        old_mvt.validate()

        deal_mvt = movement.Movement()
        deal_mvt.fill_mvt(10, 100, 3, 1, 0, "creation_deal")

        movement.check(old_mvt, deal_mvt)
        assert deal_mvt.is_valid()

    def test_movement_3(self):
        old_mvt = movement.Movement()
        old_mvt.fill_mvt(10, 100, 3, 1, 0, "creation_deal")
        old_mvt.validate()

        deal_mvt = movement.Movement()
        deal_mvt.fill_mvt(100, 10, 1, 2, 0, "create_loan")

        movement.check(old_mvt, deal_mvt)
        assert deal_mvt.is_valid()


    def test_movement_4(self):
        old_mvt = movement.Movement()
        old_mvt.fill_mvt(10, 100, 3, 1, 0, "creation_deal")

        deal_mvt = movement.Movement()
        deal_mvt.fill_mvt(101, 10, 1, 2, 0, "create_loan")

        movement.check(old_mvt, deal_mvt)
        assert not deal_mvt.is_valid()


    def test_movement_5(self):
        old_mvt = movement.Movement()
        old_mvt.fill_mvt(10, 100, 3, 1, 0, "creation_deal")

        deal_mvt = movement.Movement()
        deal_mvt.fill_mvt(100, 10, 1, 2, 0, "blablabal")

        movement.check(old_mvt, deal_mvt)
        assert not deal_mvt.is_valid()
