#!/usr/bin/env python

def Descriptor(*args, **kwargs):
    # figure out which sort of descriptor we're building, return it
    if args:
        if len(args) == 1:
            type = buf[0]
        else:
            type = args[0]
        dsc = _FactoryDict[type]
    else:
        dsc = descriptors.GenericDescriptor
    return dsc(*args, **kwargs)
