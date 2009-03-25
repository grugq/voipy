

class Event(MGCPObject):
    pass
    # [packageName|'*' "/"]    ["@" connection ID | '*']

    # signal-type: {"OO" : "On/Off", "TO":"Time-out", "BR":"Brief"}
    # OO => '+' on, '-' off ... default is on

    # params are in '(' ')', and can be either p=v, or p(v)

    # 
