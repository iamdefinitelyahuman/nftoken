#!/usr/bin/python3

import pytest


@pytest.fixture(scope="module", autouse=True)
def setup(accounts, nft):
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    nft.mint(accounts[2], 10000, {'from': accounts[0]})
    nft.mint(accounts[3], 10000, {'from': accounts[0]})


def test_approve(accounts, nft):
    assert nft.allowance(accounts[1], accounts[2]) == 0
    nft.approve(accounts[2], 10000, {'from': accounts[1]})
    assert nft.allowance(accounts[1], accounts[2]) == 10000
    nft.approve(accounts[2], 42, {'from': accounts[1]})
    assert nft.allowance(accounts[1], accounts[2]) == 42


def test_transfer_from(accounts, nft):
    nft.approve(accounts[2], 10000, {'from': accounts[1]})
    nft.transferFrom(accounts[1], accounts[4], 3000, {'from': accounts[2]})
    assert nft.allowance(accounts[1], accounts[2]) == 7000
    assert nft.balanceOf(accounts[1]) == 7000
    assert nft.balanceOf(accounts[2]) == 10000
    assert nft.balanceOf(accounts[4]) == 3000


def test_insufficient_allowance(accounts, nft):
    nft.approve(accounts[2], 3000, {'from': accounts[1]})
    with pytest.reverts("dev: underflow"):
        nft.transferFrom(accounts[1], accounts[4], 4000, {'from': accounts[2]})
    with pytest.reverts("dev: underflow"):
        nft.transferFrom(accounts[3], accounts[4], 1, {'from': accounts[2]})
