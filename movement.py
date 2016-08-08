#Definiton of a movement
new_deal_str = "New deal creation"
cmd_str = ["Loan creation", "Finalize deal"\
        , "Loan selection", "Loan query", new_deal_str]
new_peer_str = "New peer admission"
admin_str = "ADMIN"

all_cmd_str = cmd_str 

dico_types = { "Basic entity" : 3, "Financial Institution" : 2 \
        , "Provider" : 1}

class Movement:

    def __init__(self):
        self.send_id = None
        self.recv_id = None
        self.send_type = None
        self.recv_type = None
        self.mvt_ref = None
        self.cmd = None
        self.tx_id = 0
        self.status = "empty"
        self.name = ""

    def __str__(self):
        return( "TX ID: {txid} -- TX REF ID {txrid} -- "
                "Creator id: {si} -- target id: {ri} -- "
                "target type: {tt} -- cmd: {cd} -- status: {st}"
                ).format(si = self.send_id, ri = self.recv_id\
                        , cd = self.cmd, st =self.status
                        , txid = self.tx_id, tt = self.recv_type
                        , txrid = self.mvt_ref)

    def short_str(self):
        return( "TX ID: {txid} -- TX REF ID {txrid} -- "
                "Creator id: {si} -- target id: {ri}"
                ).format(si = self.send_id, ri = self.recv_id\
                        , cd = self.cmd, st =self.status
                        , txid = self.tx_id, tt = self.recv_type
                        , txrid = self.mvt_ref)

    def debug_str(self):
        return ("Movement: send_id:{si} - send_type:{sty}"
                "- recv_id:{ri} - recv_type:{rt}"
                "- cmd:{cd} - status+{st}"
                ).format(si = self.send_id, ri = self.recv_id\
                        , cd = self.cmd, st =self.status
                        , sty = self.send_type, rt = self.recv_type)

    def fill_mvt(self, send_id, recv_id, send_type, recv_type, mvt_ref, cmd):
        self.send_id = send_id
        self.recv_id = recv_id
        self.send_type = send_type
        self.recv_type = recv_type
        self.mvt_ref = mvt_ref
        self.tx_id = 0
        self.cmd = cmd
        self.status = "pending"

    def get_ref_mvt(self):
        return self.mvt_ref

    def validate(self):
        self.status = "validated"

    def reject(self):
        self.status = "rejected"

    def is_valid(self):
        if self.status == "validated":
            return True
        return False

    def set_id(self, id):
        self.tx_id = id

    def set_name(self, name):
        self.name = name

def check(Movement_ant, Movement_new):
    """
        Rules to check if a movement is valid.
    """
    global cmd_str
   
    #Admin case 
    if Movement_new.cmd == admin_str:
        Movement_new.cmd = new_peer_str
        Movement_new.validate()
        return 

    #Every other case need a valid referencee
    if not Movement_ant.is_valid():
        Movement_new.reject()
        print("reject for invalid ant")
        return
    
    #New peer creation
    if Movement_new.cmd == new_peer_str:
        check_new_peer(Movement_ant, Movement_new)
        return
    
    if not (Movement_new.send_id in Movement_ant.recv_id):
        Movement_new.reject()
        print("reject for id")
        return
    #New deal creation
    if Movement_new.cmd == new_deal_str:
        check_new_deal(Movement_ant, Movement_new)
        return

    if Movement_new.cmd == cmd_str[3]:  #Loan Query
        check_loan_query(Movement_ant, Movement_new)
        return

    if Movement_new.cmd == cmd_str[0]: #Loan creation
        check_loan_creation(Movement_ant, Movement_new)
        return

    if Movement_new.cmd == cmd_str[2]: #loan selection
        check_loan_selection(Movement_ant, Movement_new)
        return

    if Movement_new.cmd == cmd_str[1]: #Finalization
        check_finalize(Movement_ant, Movement_new)
        return

def check_new_peer(Movement_ant, Movement_new):
    """
        Basic rule to create a new peer
    """
    if Movement_new.send_type != dico_types["Basic entity"]:
        Movement_new.validate()
    else:
        Movement_new.reject()
    return

def check_new_deal(Movement_ant, Movement_new):
    if Movement_new.send_type == dico_types["Basic entity"] and \
            Movement_new.send_id in Movement_ant.recv_id:
        Movement_new.validate()
        return
    else:
        Movement_new.reject()
        print("reject for new dealk")
        print(Movement_new.debug_str())
    return

def check_loan_creation(Movement_ant, Movement_new):
    if Movement_ant.cmd == cmd_str[3]:
        Movement_new.validate()
    else:
        Movement_new.reject()
    return

def check_loan_query(Movement_ant, Movement_new):
    if Movement_ant.cmd == new_deal_str:
        Movement_new.validate()
    else:
        Movement_new.reject()
    return

def check_loan_selection(Movement_ant, Movement_new):
    if Movement_ant.cmd == cmd_str[0]:
        Movement_new.validate()
    else:
        Movement_new.reject()
    return

def check_finalize(Movement_ant, Movement_new):
    if Movement_ant.cmd == cmd_str[2]:
        Movement_new.validate()
    else:
        Movement_new.reject()
    return
