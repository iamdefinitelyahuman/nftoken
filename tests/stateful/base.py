#!/usr/bin/python3


class BaseStateMachine:
    def __init__(cls, NFToken, accounts, total_supply):
        cls.accounts = accounts
        cls.total_supply = total_supply
        cls.nft = NFToken.deploy("Test NFT", "NFT", total_supply, {"from": accounts[0]})

    def setup(self):
        self.balances = {i: 0 for i in self.accounts}
        self.balances[self.accounts[0]] = self.total_supply

    def invariant_balances(self):
        for account, balance in self.balances.items():
            assert self.nft.balanceOf(account) == balance

    def invariant_ranges(self):
        all_ranges = []
        for account in self.accounts:
            ranges = self.nft.rangesOf(account)
            all_ranges.extend(ranges)

            # check that ranges are valid
            assert not next((i for i in ranges if i[1] <= i[0]), False)
            assert sum(i[-1] - i[0] for i in ranges) == self.balances[account]

        # check for overlapping or missing ranges
        all_ranges = sorted(all_ranges, key=lambda k: k[0])
        assert sum(i[-1] - i[0] for i in all_ranges) == self.total_supply
        assert all_ranges[0][0] == 1
        assert all_ranges[-1][1] == self.total_supply + 1

        for i in range(len(all_ranges) - 1):
            assert all_ranges[i][1] == all_ranges[i + 1][0]
