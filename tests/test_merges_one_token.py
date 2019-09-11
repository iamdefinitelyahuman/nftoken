#!/usr/bin/python3

import pytest


@pytest.fixture(scope="module", autouse=True)
def setup(accounts, nft):
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    nft.mint(accounts[2], 10000, {'from': accounts[0]})
    nft.mint(accounts[3], 10000, {'from': accounts[0]})


def test_inside_one(check_ranges, accounts, nft):
    '''inside, one nft'''
    nft.transferRange(accounts[4], 12000, 12001, {'from': accounts[2]})
    check_ranges(
        [(1, 10001)],
        [(10001, 12000), (12001, 20001)],
        [(20001, 30001)],
        [(12000, 12001)]
    )


def test_one_left(check_ranges, accounts, nft):
    '''one nft, touch left'''
    nft.transferRange(accounts[4], 10001, 10002, {'from': accounts[2]})
    check_ranges(
        [(1, 10001)],
        [(10002, 20001)],
        [(20001, 30001)],
        [(10001, 10002)]
    )


def test_one_left_abs(check_ranges, accounts, nft):
    '''one nft, touch left, absolute'''
    nft.transferRange(accounts[4], 1, 2, {'from': accounts[1]})
    check_ranges(
        [(2, 10001)],
        [(10001, 20001)],
        [(20001, 30001)],
        [(1, 2)]
    )


def test_one_left_merge(check_ranges, accounts, nft):
    '''one nft, touch left, merge'''
    nft.transferRange(accounts[4], 1, 5000, {'from': accounts[1]})
    nft.transferRange(accounts[1], 10001, 10002, {'from': accounts[2]})
    check_ranges(
        [(5000, 10002)],
        [(10002, 20001)],
        [(20001, 30001)],
        [(1, 5000)]
    )


def test_one_left_merge_abs(check_ranges, accounts, nft):
    '''one nft, touch left, merge, absolute'''
    nft.transferRange(accounts[1], 10001, 10002, {'from': accounts[2]})
    check_ranges(
        [(1, 10002)],
        [(10002, 20001)],
        [(20001, 30001)],
        []
    )


def test_one_right(check_ranges, accounts, nft):
    '''one nft, touch right'''
    nft.transferRange(accounts[4], 20000, 20001, {'from': accounts[2]})
    check_ranges(
        [(1, 10001)],
        [(10001, 20000)],
        [(20001, 30001)],
        [(20000, 20001)]
    )


def test_one_right_abs(check_ranges, accounts, nft):
    '''one nft, touch right, absolute'''
    nft.transferRange(accounts[4], 30000, 30001, {'from': accounts[3]})
    check_ranges(
        [(1, 10001)],
        [(10001, 20001)],
        [(20001, 30000)],
        [(30000, 30001)]
    )


def test_one_right_merge(check_ranges, accounts, nft):
    '''one nft touch right, merge'''
    nft.transferRange(accounts[4], 25000, 30001, {'from': accounts[3]})
    nft.transferRange(accounts[3], 20000, 20001, {'from': accounts[2]})
    check_ranges(
        [(1, 10001)],
        [(10001, 20000)],
        [(20000, 25000)],
        [(25000, 30001)]
    )


def test_one_right_merge_abs(check_ranges, accounts, nft):
    '''one nft, touch right, merge absolute'''
    nft.transferRange(accounts[3], 20000, 20001, {'from': accounts[2]})
    check_ranges(
        [(1, 10001)],
        [(10001, 20000)],
        [(20000, 30001)],
        []
    )


def test_create_one_start(check_ranges, accounts, nft):
    '''create one nft range at start'''
    nft.transferRange(accounts[4], 10002, 12001, {'from': accounts[2]})
    check_ranges(
        [(1, 10001)],
        [(10001, 10002), (12001, 20001)],
        [(20001, 30001)],
        [(10002, 12001)]
    )


def test_create_one_start_abs(check_ranges, accounts, nft):
    '''create one nft range at start, absolute'''
    nft.transferRange(accounts[4], 2, 1000, {'from': accounts[1]})
    check_ranges(
        [(1, 2), (1000, 10001)],
        [(10001, 20001)],
        [(20001, 30001)],
        [(2, 1000)]
    )


def test_create_one_end(check_ranges, accounts, nft):
    '''create one nft range at end'''
    nft.transferRange(accounts[4], 19000, 20000, {'from': accounts[2]})
    check_ranges(
        [(1, 10001)],
        [(10001, 19000), (20000, 20001)],
        [(20001, 30001)],
        [(19000, 20000)]
    )


def test_create_one_end_abs(check_ranges, accounts, nft):
    '''create one nft range at end, absolute'''
    nft.transferRange(accounts[4], 29000, 30000, {'from': accounts[3]})
    check_ranges(
        [(1, 10001)],
        [(10001, 20001)],
        [(20001, 29000), (30000, 30001)],
        [(29000, 30000)]
    )
