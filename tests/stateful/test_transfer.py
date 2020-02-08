#!/usr/bin/python3

import brownie
from brownie.test import strategy


def test_stateful_transfer(BaseStateMachine, state_machine, NFToken, accounts):

    """
    Stateful test that verifies transfer behavior with NFToken.transfer
    """

    class StateMachine(BaseStateMachine):

        st_amount = strategy("uint256", max_value=1000000)
        st_sender = strategy("address")
        st_receiver = strategy("address")

        def setup(self):
            self.balances = {i: 0 for i in self.accounts}
            self.balances[self.accounts[0]] = self.total_supply

        # transfers an arbitrary amount
        def rule_transfer(self, st_sender, st_receiver, st_amount):
            self._transfer(st_sender, st_receiver, st_amount)

        # transfers the entire balance of an account
        def rule_transfer_all(self, st_sender, st_receiver):
            self._transfer(st_sender, st_receiver, self.balances[st_sender])

        # transfers a single token
        def rule_transfer_one(self, st_sender, st_receiver):
            self._transfer(st_sender, st_receiver, 1)

        # internal shared transfer logic
        def _transfer(self, sender, receiver, amount):
            if amount <= self.balances[sender]:
                self.nft.transfer(receiver, amount, {"from": sender})
                self.balances[sender] -= amount
                self.balances[receiver] += amount
            else:
                with brownie.reverts("dev: underflow"):
                    self.nft.transfer(receiver, amount, {"from": sender})

    settings = {"stateful_step_count": 20, "max_examples": 20}
    state_machine(StateMachine, NFToken, accounts, 1000000, settings=settings)
