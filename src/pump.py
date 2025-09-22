from qwiic.qwiic_relay import QwiicRelay

class VaccuumPump:
    relay:QwiicRelay
    relaynum:int

    _state:bool

    def __init__(self, relay:QwiicRelay, relaynum:int=1):
        self.relay = relay
        self.relaynum = relaynum
        self.update_state()

    # makes state readonly
    @property
    def state(self): return self._state

    def update_state(self) -> None:
        self._state = self.relay.get_relay_state()
    
    def set_on(self) -> None:
        self.relay.set_relay_on(self.relaynum)
        self._state = False

    def set_off(self) -> None:
        self.relay.set_relay_off(self.relaynum)
        self._state = True