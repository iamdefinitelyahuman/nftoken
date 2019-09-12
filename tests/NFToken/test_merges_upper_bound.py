#!/usr/bin/python3

import pytest


# contract deployment
@pytest.fixture(scope="module", autouse=True)
def nftupper(NFToken, accounts):
    token = accounts[0].deploy(NFToken, "Test NFT", "NFT", 2**64-2)
    token.transfer(accounts[1], 2**64 - 20002, {'from': accounts[0]})
    token.transfer(accounts[2], 10000, {'from': accounts[0]})
    token.transfer(accounts[3], 10000, {'from': accounts[0]})
    yield token


def test_initial(check_ranges, accounts, nftupper):
    check_ranges(
        [(1, 2 ** 64 - 20001)],
        [(2 ** 64 - 20001, 2 ** 64 - 10001)],
        [(2 ** 64 - 10001, 2 ** 64 - 1)],
        [],
        nft=nftupper,
    )


def test_whole_range_right_abs(check_ranges, accounts, nftupper):
    '''whole range, merge right, absolute'''
    nftupper.transferRange(accounts[3], 2 ** 64 - 20001, 2 ** 64 - 10001, {'from': accounts[2]})
    check_ranges(
        [(1, 2 ** 64 - 20001)],
        [],
        [(2 ** 64 - 20001, 2 ** 64 - 1)],
        [],
        nft=nftupper,
    )


def test_whole_range_same_both(check_ranges, accounts, nftupper):
    '''whole range, merge both sides, absolute both'''
    nftupper.transferRange(accounts[3], 1, 2 ** 64 - 20001, {'from': accounts[1]})
    nftupper.transferRange(accounts[3], 2 ** 64 - 20001, 2 ** 64 - 10001, {'from': accounts[2]})
    check_ranges(
        [],
        [],
        [(1, 2 ** 64 - 1)],
        [],
        nft=nftupper,
    )


def test_whole_range_same_right(check_ranges, accounts, nftupper):
    '''whole range, merge both sides, absolute right'''
    nftupper.transferRange(accounts[3], 5000, 2 ** 64 - 20001, {'from': accounts[1]})
    nftupper.transferRange(accounts[3], 2 ** 64 - 20001, 2 ** 64 - 10001, {'from': accounts[2]})
    check_ranges(
        [(1, 5000)],
        [],
        [(5000, 2 ** 64 - 1)],
        [],
        nft=nftupper,
    )


def test_stop_absolute(check_ranges, accounts, nftupper):
    '''partial, touch stop, absolute'''
    nftupper.transferRange(accounts[4], 2 ** 64 - 5000, 2 ** 64 - 1, {'from': accounts[3]})
    check_ranges(
        [(1, 2 ** 64 - 20001)],
        [(2 ** 64 - 20001, 2 ** 64 - 10001)],
        [(2 ** 64 - 10001, 2 ** 64 - 5000)],
        [(2 ** 64 - 5000, 2 ** 64 - 1)],
        nft=nftupper,
    )


def test_stop_partial_same_abs(check_ranges, accounts, nftupper):
    '''partial, touch stop, merge, absolute'''
    nftupper.transferRange(accounts[3], 2 ** 64 - 15000, 2 ** 64 - 10001, {'from': accounts[2]})
    check_ranges(
        [(1, 2 ** 64 - 20001)],
        [(2 ** 64 - 20001, 2 ** 64 - 15000)],
        [(2 ** 64 - 15000, 2 ** 64 - 1)],
        [],
        nft=nftupper,
    )
