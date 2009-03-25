#!/usr/bin/env python


import mgcp

class Parameter(mgcp.MGCPObject):
    name = ''
    HCOLON=':'
    def __init__(self, buf=None, **kwargs):
        self.values = []
        super(Parameter, self).__init__(buf, **kwargs)

    def _set_value(self, val):
        self.values[0] = val
    value = property(lambda s: len(s.values) and s.values[0] or None,
                     fset=_set_value, doc="parameter value")
    def parse(self, buf):
        # figure out the type from the header, then change class, and parse..
        def get_code():
            return buf.split(self.HCOLON,1)
        def set_class(code):
            class_list = {
                'B' : BearerInformation().__class__,
                'C' : CallId().__class__,
                'A' : Capabilities().__class__,
                'I' : ConnectionId().__class__,
                'M' : ConnectionMode().__class__,
                'P' : ConnectionParameters().__class__,
                'T' : DetectEvents().__class__,
                'ES' : EventStates().__class__,
                'D' : DigitMap().__class__,
                'L' : LocalConnectionOptions().__class__,
                'MD' : MaxMGCPDatagram().__class__,
                'N' : NotifiedEntity().__class__,
                'O' : ObservedEvents().__class__,
                'PL' : PackageList().__class__,
                'Q' : QuarantineHandling().__class__,
                'E' : ReasonCode().__class__,
                'R' : RequestedEvents().__class__,
                'F' : RequestedInfo().__class__,
                'X' : RequestIdentifier().__class__,
                'K' : ResponseAck().__class__,
                'RD' : RestartDelay().__class__,
                'RM' : RestartMethod().__class__,
                'I2' : SecondConnectionId().__class__,
                'Z2' : SecondEndpointId().__class__,
                'S' : SignalRequests().__class__,
                'Z' : SpecificEndPointId().__class__,
                'RC' : RemoteConnectionDescriptor().__class__,
                'LC' : LocalConnectionDescriptor().__class__,
            }
            self.__class__ = class_list.get(code.strip().upper(),
                                            ExtendedParameter().__class__)
        code, buf = get_code()
        set_class( code )
        self._parsevalues(buf.strip())

    def _parsevalues(self, buf):
        self.values.append(buf)
    def _packvalues(self):
        return ', '.join(['%s'%val for val in self.values])
    def pack(self):
        return '%s%s %s' % (self.name, self.HCOLON, self._packvalues())

class BearerInformation(Parameter):
    name = 'B'
    #values = [] 
    # name[':' val], ...
    def _parsevalues(self, buf):
        pass

class CallId(Parameter):
    # value = Token [32 digit hex string]
    name = 'C'

class Capabilities(Parameter):
    name = 'A'
    # value, special values

class ConnectionId(Parameter):
    # value = Token [32 digit hex string]
    name = 'I'

class ConnectionMode(Parameter):
    name = 'M'
    # value, special values

class ConnectionParameters(Parameter):
    # value, special values
    name = 'P'

class DetectEvents(Parameter):
    name = 'T'
    # value, comma seperated list of Events

class EventStates(Parameter):
    name = 'ES'
    # value, comma seperated list of Events

class DigitMap(Parameter): name = 'D'


class LocalConnectionOptions(Parameter):
    # value, special values
    name = 'L'

class MaxMGCPDatagram(Parameter):
    # value, Token [9 digits]
    name = 'MD'

class NotifiedEntity(Parameter): name = 'N'

class ObservedEvents(Parameter):
    # value, comma seperated list of events
    name = 'O'

class PackageList(Parameter):
    # value, comma seperated list of events
    name = 'PL'

class QuarantineHandling(Parameter):
    # value, comma seperated list of special values
    name = 'Q'

class ReasonCode(Parameter):
    # value, DDD reasonString
    name = 'E'

class RequestedEvents(Parameter):
    # value, comma seperated list of Events
    name = 'R'

class RequestedInfo(Parameter):
    # value, comma seperated list of parameter codes
    name = 'F'

class RequestIdentifier(Parameter):
    # value, Token [32 hex]
    name = 'X'


class ResponseAck(Parameter):
    # value, comma seperated list of parameter codes
    name = 'K'

class RestartDelay(Parameter):
    name = 'RD'

class RestartMethod(Parameter):
    name = 'RM'
    # value, keyword

class SecondConnectionId(Parameter): name = 'I2'
class SecondEndpointId(Parameter): name = 'Z2'
class SignalRequests(Parameter):
    # value, comma seperated list of Signals(Events?)
    name = 'S'


class ExtendedParameter(Parameter): name = '' # Vendor, Package, Other... ?
class SpecificEndPointId(Parameter): name = 'Z'
class RemoteConnectionDescriptor(Parameter): name = 'RC'
class LocalConnectionDescriptor(Parameter): name = 'LC'
