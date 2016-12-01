import blockchain as blc
import peer_mgr 
import gui
import entity
import movement
import time


blockchain = blc.Blockchain(1000, 30, 10)

[pending_mvts, results_mvts] = blockchain.get_queue()
peers_manager = peer_mgr.PeerManager(results_mvts, pending_mvts)

inital_mvt = movement.Movement()
inital_mvt.fill_mvt(0, 0, 1, 1, 0, movement.admin_str) 

peers_manager.create_new_peer( 2, "MISYS", inital_mvt)

gui_thread =  gui.GuiThread(peers_manager.get_model_list())
gui_thread.load()
blockchain.set_guit(gui_thread.get_block())

peers_manager.start()
blockchain.start()
gui_thread.run()
peers_manager.exit = True
blockchain.exit = True
