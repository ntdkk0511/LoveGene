#
# VALUE_CALC|value|(add|sub|mul|div)|number
#  -> VALUE_EVENT_CALC|value
#
import MMDA_connector

values = {}

def set(connector, msg):
    values[msg[1]] = int(msg[2])

def calc(connector, msg):    
    number = int(msg[3])
    result = None
    status = "done"

    if msg[1] in values:
        msg_data = ["VALUE_SET", msg[1]]
        if msg[2]=="add":
            result = values[msg[1]] + number
        elif msg[2]=="sub":
            result = values[msg[1]] - number
        elif msg[2]=="mul":
            result = values[msg[1]] * number
        elif msg[2]=="div":
            result = values[msg[1]] / number
        if result is not None:
            msg_data.append(str(result))
            connector.put_msg(msg_data)
        else:
            status = "no_operation"
    else:
        status = "no_value"
    connector.put_msg(["VALUE_EVENT_CALC", msg[1], status])
    

connector = MMDA_connector.MMDA_connector()
connector.add_handler("VALUE_SET", set)
connector.add_handler("VALUE_CALC", calc)

connector.mainloop()
