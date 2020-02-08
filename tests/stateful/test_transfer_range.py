#!/usr/bin/python3

import brownie
from brownie.test import strategy


def test_stateful_transfer_range(BaseStateMachine, state_machine, NFToken, accounts):

    """
    Stateful test that verifies transfer behavior with NFToken.transferRange
    """

    class StateMachine(BaseStateMachine):

        st_idx = strategy("decimal", min_value=0, max_value="0.9999999999")
        st_amount = strategy("decimal", min_value=0, max_value="0.5")
        st_sender = strategy("address")
        st_receiver = strategy("address")

        def __init__(cls, NFToken, accounts):
            super().__init__(cls, NFToken, accounts, 1000)
            for account in accounts[1:]:
                cls.nft.transfer(account, 1000 // len(accounts), {"from": accounts[0]})

        def setup(self):
            initial = self.total_supply // len(self.accounts)
            self.balances = {i: initial for i in self.accounts}

        # transfers a portion of a range starting from the first token in the range
        def rule_from_start(self, st_sender, st_receiver, st_idx, st_amount):
            start, stop, length = self._get_range(st_sender, st_idx)
            stop = start + int(length * st_amount)
            self._transfer(st_sender, st_receiver, start, stop)

        # transfers a portion of a range, ending with the last token in the range
        def rule_from_end(self, st_sender, st_receiver, st_idx, st_amount):
            start, stop, length = self._get_range(st_sender, st_idx)
            start = stop - int(length * st_amount)
            self._transfer(st_sender, st_receiver, start, stop)

        # transfers a portion of a range, from the middle of an existing range
        def rule_from_middle(self, st_sender, st_receiver, st_idx, st_amount):
            start, stop, length = self._get_range(st_sender, st_idx)
            offset = (length - int(length * st_amount)) // 2
            self._transfer(st_sender, st_receiver, start + offset, stop - offset)

        # transfers an entire range
        def rule_full_range(self, st_sender, st_receiver, st_idx):
            start, stop, length = self._get_range(st_sender, st_idx)
            self._transfer(st_sender, st_receiver, start, stop)

        def _get_range(self, address, pct):
            ranges = self.nft.rangesOf(address)
            if not ranges:
                return 0, 0, 0
            range_ = ranges[int(len(ranges) * pct)]
            return range_[0], range_[1], range_[1] - range_[0]

        def _transfer(self, sender, receiver, start, stop):
            if stop <= start:
                with brownie.reverts():
                    self.nft.transferRange(receiver, start, stop, {"from": sender})
            else:
                self.nft.transferRange(receiver, start, stop, {"from": sender})
                self.balances[sender] -= stop - start
                self.balances[receiver] += stop - start

    settings = {"stateful_step_count": 20, "max_examples": 20}
    state_machine(StateMachine, NFToken, accounts, settings=settings)
