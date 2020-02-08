#!/usr/bin/python3

import brownie
from brownie.test import strategy


def test_stateful_transfer_one_token(BaseStateMachine, state_machine, NFToken, accounts):

    """
    Stateful test that verifies range pointer modifications when
    dealing with single token transfers and small ranges.
    """

    class StateMachine(BaseStateMachine):

        st_amount = strategy("uint256", max_value=1000000)
        st_sender = strategy("address")
        st_receiver = strategy("address")

        def __init__(cls, NFToken, accounts):
            super().__init__(cls, NFToken, accounts, len(accounts))
            for account in accounts[1:]:
                cls.nft.transfer(account, 1, {"from": accounts[0]})

        def setup(self):
            self.balances = {i: 1 for i in self.accounts}

        # transfers a single token
        def rule_transfer_one(self, st_sender, st_receiver):
            if self.balances[st_sender]:
                self.nft.transfer(st_receiver, 1, {"from": st_sender})
                self.balances[st_sender] -= 1
                self.balances[st_receiver] += 1
            else:
                with brownie.reverts("dev: underflow"):
                    self.nft.transfer(st_receiver, 1, {"from": st_sender})

        # transfers a single token using transferRange
        def rule_transfer_range_one(self, st_sender, st_receiver):
            if self.balances[st_sender]:
                start = self.nft.rangesOf(st_sender)[-1][0]
                self.nft.transferRange(st_receiver, start, start + 1, {"from": st_sender})
                self.balances[st_sender] -= 1
                self.balances[st_receiver] += 1
            else:
                with brownie.reverts("dev: underflow"):
                    self.nft.transfer(st_receiver, 1, {"from": st_sender})

    settings = {"stateful_step_count": 20, "max_examples": 20}
    state_machine(StateMachine, NFToken, accounts, settings=settings)
