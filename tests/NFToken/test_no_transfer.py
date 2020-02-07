#!/usr/bin/python3


def test_same_addr_transferRange(accounts, nft):
    ranges = nft.rangesOf(accounts[2])
    nft.transferRange(accounts[2], 11000, 12000, {"from": accounts[2]})

    assert nft.rangesOf(accounts[2]) == ranges
    assert nft.balanceOf(accounts[2]) == 10000


def test_same_addr_transfer(accounts, nft):
    ranges = nft.rangesOf(accounts[2])
    nft.transfer(accounts[2], 1000, {"from": accounts[2]})

    assert nft.rangesOf(accounts[2]) == ranges
    assert nft.balanceOf(accounts[2]) == 10000


def test_same_addr_transferFrom(accounts, nft):
    ranges = nft.rangesOf(accounts[2])
    nft.approve(accounts[1], 1000, {"from": accounts[2]})
    nft.transferFrom(accounts[2], accounts[2], 1000, {"from": accounts[1]})

    assert nft.rangesOf(accounts[2]) == ranges
    assert nft.balanceOf(accounts[2]) == 10000


def test_zero_tokens_transfer(accounts, nft):
    ranges = nft.rangesOf(accounts[2])
    nft.transfer(accounts[2], 0, {"from": accounts[2]})

    assert nft.rangesOf(accounts[2]) == ranges
    assert nft.balanceOf(accounts[2]) == 10000


def test_zero_tokens_transferFrom(accounts, nft):
    ranges = nft.rangesOf(accounts[2])
    nft.transferFrom(accounts[2], accounts[1], 0, {"from": accounts[1]})

    assert nft.rangesOf(accounts[2]) == ranges
    assert nft.balanceOf(accounts[2]) == 10000
