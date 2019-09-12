#!/usr/bin/python3

import functools
import pytest


# test isolation, always use!
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


# contract deployment
@pytest.fixture(scope="module")
def nft(accounts, NFToken):
    token = accounts[0].deploy(NFToken, "Test NFT", "NFT", 30000)
    token.transfer(accounts[1], 10000, {'from': accounts[0]})
    token.transfer(accounts[2], 10000, {'from': accounts[0]})
    token.transfer(accounts[3], 10000, {'from': accounts[0]})
    yield token


@pytest.fixture(scope="module")
def nftmint(accounts, NFTokenMintable):
    token = accounts[0].deploy(NFTokenMintable, "Test NFT", "NFT", 0)
    yield token


@pytest.fixture(scope="module")
def check_ranges(accounts, nft):
    upper = nft.totalSupply() + 1
    yield functools.partial(_check_ranges, accounts, upper, nft=nft)


def _check_ranges(accounts, upper, *expected_ranges, nft=None):
    for num, expected in enumerate(expected_ranges, start=1):
        account = accounts[num]
        ranges = nft.rangesOf(account)
        assert set(ranges) == set(expected)
        assert nft.balanceOf(account) == sum((i[1] - i[0]) for i in ranges)
        for start, stop in ranges:
            if stop - start == 1:
                assert nft.getRange(start)[:3] == (account, start, stop)
                continue
            for i in range(max(1, start - 1), start + 2):
                try:
                    data = nft.getRange(i)
                except Exception:
                    raise AssertionError(f"Could not get range pointer {i} for account {num}")
                if i < start:
                    assert data[0] != account
                else:
                    assert data[0] == account
            for i in range(stop - 1, min(stop + 1, upper)):
                data = nft.getRange(i)
                if i < stop:
                    assert data[0] == account
                else:
                    assert data[0] != account
