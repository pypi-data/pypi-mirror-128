class L2Output:

    @property
    def asks(self):
        return [(price, size) for price, size in self._asks.items()]

    @property
    def bids(self):
        return [(price, size) for price, size in self._bids.items()]
