#!/usr/bin/python3

import pytest


@pytest.fixture(scope="module", autouse=True)
def setup(accounts, nft):
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    nft.mint(accounts[2], 10000, {'from': accounts[0]})
    nft.mint(accounts[3], 10000, {'from': accounts[0]})


def test_check_bounds(accounts, nft):
    '''check bounds'''
    with pytest.reverts("dev: index out of bounds"):
        nft.transferRange(accounts[2], 0, 1000, {'from': accounts[0]})
    with pytest.reverts("dev: index out of bounds"):
        nft.transferRange(accounts[2], 1000000, 1000, {'from': accounts[0]})
    with pytest.reverts("dev: index out of bounds"):
        nft.transferRange(accounts[2], 1, 1, {'from': accounts[0]})
    with pytest.reverts("dev: index out of bounds"):
        nft.transferRange(accounts[2], 1, 1000000, {'from': accounts[0]})


def test_stop_start(accounts, nft):
    '''stop below start'''
    with pytest.reverts("dev: stop < start"):
        nft.transferRange(accounts[2], 2000, 1000, {'from': accounts[1]})


def test_multiple_ranges(accounts, nft):
    '''multiple ranges'''
    with pytest.reverts("dev: multiple ranges"):
        nft.transferRange(accounts[2], 1000, 15000, {'from': accounts[1]})
    with pytest.reverts("dev: multiple ranges"):
        nft.transferRange(accounts[2], 10000, 10002, {'from': accounts[1]})


def test_not_owner(accounts, nft):
    '''sender does not own range'''
    with pytest.reverts("dev: sender does not own"):
        nft.transferRange(accounts[3], 11000, 12000, {'from': accounts[1]})


def test_same_addr(accounts, nft):
    '''cannot send to self'''
    with pytest.reverts("dev: cannot send to self"):
        nft.transferRange(accounts[2], 11000, 12000, {'from': accounts[2]})
    with pytest.reverts("dev: cannot send to self"):
        nft.transfer(accounts[1], 1000, {'from': accounts[1]})


def test_uint64_overflow(accounts, nft):
    with pytest.reverts("dev: uint64 overflow"):
        nft.transfer(accounts[2], 2**65, {'from': accounts[1]})


def test_value_exceeds_balance(accounts, nft):
    with pytest.reverts("dev: underflow"):
        nft.transfer(accounts[2], 50000, {'from': accounts[1]})
