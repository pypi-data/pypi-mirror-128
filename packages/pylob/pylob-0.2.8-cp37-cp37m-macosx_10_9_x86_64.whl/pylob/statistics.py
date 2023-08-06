class Statistics:

    @property
    def best_ask(self):
        """get a tuple containing the best ask price and size
        """
        try:
            return self._asks.peekitem(0)
        except IndexError:
            return ()

    @property
    def best_bid(self):
        """get a tuple containing the best bid price and size
        """
        try:
            return self._bids.peekitem(0)
        except IndexError:
            return ()

    @property
    def abs_spread(self):
        return self.best_ask[0] - self.best_bid[0]

    @property
    def snapshot(self):
        """get a dict containing a list of all ask price levels
        (tuple with price and size) and all bid price levels
        """
        return {
            "asks": [
                (k, v)
                for k, v in self._asks.items()
            ],
            "bids": [
                (k, v)
                for k, v in self._bids.items()
            ]
        }

    def ask_vol_at(self, level):
        try:
            return self._asks[level]
        except KeyError:
            return 0

    def bid_vol_at(self, level):
        try:
            return self._bids[level]
        except KeyError:
            return 0

    def frame(self, length):
        """get a list with the first l ask price levell (in descendent order by price)
        and the first l bid price levels (in descendent order by price)
        """
        asks = []
        bids = []
        for i in range(length):
            try:
                asks.append(self._asks.peekitem(i))
            except IndexError:
                asks.append((0, 0))
        for i in range(length):
            try:
                bids.append(self._bids.peekitem(i))
            except IndexError:
                bids.append((0, 0))
        return {
            "asks": asks,
            "bids": bids
        }

    @property
    def last_time(self):
        """get the timestamp of the last update
        """
        return self.timestamp

    def get_asks(self):
        return [(k, v) for k, v in self._asks.items()]

    def get_bids(self):
        return [(k, v) for k, v in self._bids.items()]

    def __eq__(self, other_lob):
        return self.snapshot == other_lob.snapshot
