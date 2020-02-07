#!/usr/bin/python3


def test_transfer(accounts, nft):
    """transfer events"""
    tx = nft.transfer(accounts[2], 1000, {"from": accounts[1]})

    assert "Transfer" in tx.events
    expected = {"from": accounts[1], "to": accounts[2], "amount": 1000}
    assert tx.events["Transfer"] == expected

    assert "TransferRange" in tx.events
    expected = {"from": accounts[1], "to": accounts[2], "start": 1, "stop": 1001, "amount": 1000}
    assert tx.events["TransferRange"] == expected


def test_transferFrom(accounts, nft):
    """transferFrom events"""
    nft.approve(accounts[3], 1000, {"from": accounts[1]})
    tx = nft.transferFrom(accounts[1], accounts[2], 1000, {"from": accounts[3]})

    assert "Transfer" in tx.events
    expected = {"from": accounts[1], "to": accounts[2], "amount": 1000}
    assert tx.events["Transfer"] == expected

    assert "TransferRange" in tx.events
    expected = {"from": accounts[1], "to": accounts[2], "start": 1, "stop": 1001, "amount": 1000}
    assert tx.events["TransferRange"] == expected


def test_transferRange(accounts, nft):
    """transferRange events"""
    tx = nft.transferRange(accounts[2], 1, 1001, {"from": accounts[1]})

    assert "Transfer" in tx.events
    expected = {"from": accounts[1], "to": accounts[2], "amount": 1000}
    assert tx.events["Transfer"] == expected

    assert "TransferRange" in tx.events
    expected = {"from": accounts[1], "to": accounts[2], "start": 1, "stop": 1001, "amount": 1000}
    assert tx.events["TransferRange"] == expected
