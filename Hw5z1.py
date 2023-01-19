
import random as rnd

from DBManager.DBManager import DBManager

if __name__ == "__main__":

    db1 = DBManager(db_name="clients_db", user_name="postgres", passw="111")

    ret_val = db1.AddClient("client 1", "2 name ", '1@1.com', client_id = 1)
    print(ret_val)

    ret_val = db1.AddClient("vasya " + str(rnd.randrange(99)), "pupkin "+ str(rnd.randrange(99)), 'asds@aidj.com')
    print(ret_val)

    ret_val = db1.AddClientPhone(1, rnd.randrange(9999999999))
    print(ret_val)

    ret_val = db1.AddClientPhone(1, 666)
    print(ret_val)

    ret_val = db1.ChangeClientData(1, "clkient 1 name " + str(rnd.randrange(99)), "client 1 second name "+ str(rnd.randrange(99)), "eml@eeee.name")
    print(ret_val)

    print("#######################################")
    ret_val = db1.FindClient(email="eml@eeee.name")
    print(ret_val)
    ret_val = db1.FindClient(last_name="%a%")
    print(ret_val)
    print("#######################################")

    ret_val = db1.RemoveClientPhone(1, 666)
    print(ret_val)

    ret_val = db1.RemoveClient(1)
    print(ret_val)

    db1.CloseDB()
    
