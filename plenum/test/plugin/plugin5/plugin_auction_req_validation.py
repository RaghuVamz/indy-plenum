from plenum.common.txn import TXN_TYPE, DATA

AUCTION_START = "AUCTION_START"
AUCTION_END = "AUCTION_END"
PLACE_BID = "PLACE_BID"
GET_BAL = "GET_BAL"
AMOUNT = "amount"
ID = "id"


class AuctionReqValidationPlugin:
    pluginType = "VERIFICATION"

    validTxnTypes = [AUCTION_START, AUCTION_END, PLACE_BID, GET_BAL]

    def __init__(self):
        self.count = 0

    def verify(self, operation):
        typ = operation.get(TXN_TYPE)
        assert typ in self.validTxnTypes, \
            "{} is not a valid transaction type, must be one of {}".\
                format(typ, ', '.join(self.validTxnTypes))
        if typ in [AUCTION_START, AUCTION_END, PLACE_BID]:
            data = operation.get(DATA)
            assert isinstance(data, dict), \
                "{} attribute is missing or not in proper format".format(DATA)
            assert ID in data and data[ID], "No id provided for auction"

            if typ == PLACE_BID:
                amount = data.get(AMOUNT)
                assert isinstance(amount, (int, float)) and amount > 0, \
                    "{} must be present and should be a number greater than 0"\
                        .format(AMOUNT)

        self.count += 1