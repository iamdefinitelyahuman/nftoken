#!/usr/bin/python3

import pytest

from brownie import accounts


@pytest.fixture(scope="module", autouse=True)
def setup(accounts, nft):
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    nft.mint(accounts[2], 10000, {'from': accounts[0]})
    nft.mint(accounts[3], 10000, {'from': accounts[0]})


def test_check_bounds(nft):
    '''check bounds'''
    with pytest.reverts("Invalid index"):
        nft.transferRange(accounts[2], 0, 1000, {'from': accounts[0]})
    with pytest.reverts("Invalid index"):
        nft.transferRange(accounts[2], 1000000, 1000, {'from': accounts[0]})
    with pytest.reverts("Invalid index"):
        nft.transferRange(accounts[2], 1, 0, {'from': accounts[0]})
    with pytest.reverts("Invalid index"):
        nft.transferRange(accounts[2], 1, 1000000, {'from': accounts[0]})


def test_stop_start(nft):
    '''stop below start'''
    with pytest.reverts("dev: stop < start"):
        nft.transferRange(accounts[2], 2000, 1000, {'from': accounts[1]})


def test_multiple_ranges(nft):
    '''multiple ranges'''
    with pytest.reverts("dev: multiple ranges"):
        nft.transferRange(accounts[2], 1000, 15000, {'from': accounts[1]})
    with pytest.reverts("dev: multiple ranges"):
        nft.transferRange(accounts[2], 10000, 10002, {'from': accounts[1]})


def test_not_owner(nft):
    '''sender does not own range'''
    with pytest.reverts("Sender does not own range"):
        nft.transferRange(accounts[3], 11000, 12000, {'from': accounts[1]})


def test_same_addr(nft):
    '''cannot send to self'''
    with pytest.reverts("Cannot send to self"):
        nft.transferRange(accounts[2], 11000, 12000, {'from': accounts[2]})
