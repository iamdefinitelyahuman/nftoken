#!/usr/bin/python3

import pytest


@pytest.fixture(scope="module", autouse=True)
def setup(accounts, nft):
    nft.mint(accounts[1], 2**64 - 20002, {'from': accounts[0]})
    nft.mint(accounts[2], 10000, {'from': accounts[0]})
    nft.mint(accounts[3], 10000, {'from': accounts[0]})


def test_initial(check_ranges, accounts):
    check_ranges(
        [(1, 2 ** 64 - 20001)],
        [(2 ** 64 - 20001, 2 ** 64 - 10001)],
        [(2 ** 64 - 10001, 2 ** 64 - 1)],
        []
    )


def test_whole_range_right_abs(check_ranges, accounts, nft):
    '''whole range, merge right, absolute'''
    nft.transferRange(accounts[3], 2 ** 64 - 20001, 2 ** 64 - 10001, {'from': accounts[2]})
    check_ranges(
        [(1, 2 ** 64 - 20001)],
        [],
        [(2 ** 64 - 20001, 2 ** 64 - 1)],
        []
    )


def test_whole_range_same_both(check_ranges, accounts, nft):
    '''whole range, merge both sides, absolute both'''
    nft.transferRange(accounts[3], 1, 2 ** 64 - 20001, {'from': accounts[1]})
    nft.transferRange(accounts[3], 2 ** 64 - 20001, 2 ** 64 - 10001, {'from': accounts[2]})
    check_ranges(
        [],
        [],
        [(1, 2 ** 64 - 1)],
        []
    )


def test_whole_range_same_right(check_ranges, accounts, nft):
    '''whole range, merge both sides, absolute right'''
    nft.transferRange(accounts[3], 5000, 2 ** 64 - 20001, {'from': accounts[1]})
    nft.transferRange(accounts[3], 2 ** 64 - 20001, 2 ** 64 - 10001, {'from': accounts[2]})
    check_ranges(
        [(1, 5000)],
        [],
        [(5000, 2 ** 64 - 1)],
        []
    )


def test_stop_absolute(check_ranges, accounts, nft):
    '''partial, touch stop, absolute'''
    nft.transferRange(accounts[4], 2 ** 64 - 5000, 2 ** 64 - 1, {'from': accounts[3]})
    check_ranges(
        [(1, 2 ** 64 - 20001)],
        [(2 ** 64 - 20001, 2 ** 64 - 10001)],
        [(2 ** 64 - 10001, 2 ** 64 - 5000)],
        [(2 ** 64 - 5000, 2 ** 64 - 1)]
    )


def test_stop_partial_same_abs(check_ranges, accounts, nft):
    '''partial, touch stop, merge, absolute'''
    nft.transferRange(accounts[3], 2 ** 64 - 15000, 2 ** 64 - 10001, {'from': accounts[2]})
    check_ranges(
        [(1, 2 ** 64 - 20001)],
        [(2 ** 64 - 20001, 2 ** 64 - 15000)],
        [(2 ** 64 - 15000, 2 ** 64 - 1)],
        []
    )
