from pprint import pprint 

def pipeline(intital, steps):
    res = intital
    for step in steps:
        res = step(res)
    return res

def inspect(arg=None):
    if not callable(arg):
        pprint(arg)
        return arg

    def fun(data):
        logger = arg
        logger(data)
        return data

    return fun