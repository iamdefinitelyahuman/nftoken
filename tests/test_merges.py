#!/usr/bin/python3

import pytest


@pytest.fixture(scope="module", autouse=True)
def setup(accounts, nft):
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    nft.mint(accounts[2], 10000, {'from': accounts[0]})
    nft.mint(accounts[3], 10000, {'from': accounts[0]})


def test_verify_initial(check_ranges):
    '''verify initial ranges'''
    check_ranges(
        [(1, 10001)],
        [(10001, 20001)],
        [(20001, 30001)],
        []
    )


def test_inside(check_ranges, accounts, nft):
    '''inside'''
    nft.transferRange(accounts[4], 12000, 13000, {'from': accounts[2]})
    check_ranges(
        [(1, 10001)],
        [(10001, 12000), (13000, 20001)],
        [(20001, 30001)],
        [(12000, 13000)]
    )


def test_start_partial_different(check_ranges, accounts, nft):
    '''partial, touch start, no merge'''
    nft.transferRange(accounts[4], 10001, 11001, {'from': accounts[2]})
    check_ranges(
        [(1, 10001)],
        [(11001, 20001)],
        [(20001, 30001)],
        [(10001, 11001)]
    )


def test_start_partial_same(check_ranges, accounts, nft):
    '''partial, touch start, merge, absolute'''
    nft.transferRange(accounts[1], 10001, 11001, {'from': accounts[2]})
    check_ranges(
        [(1, 11001)],
        [(11001, 20001)],
        [(20001, 30001)],
        []
    )


def test_start_partial_same_abs(check_ranges, accounts, nft):
    '''partial, touch start, merge'''
    nft.transferRange(accounts[3], 1, 5000, {'from': accounts[1]})
    nft.transferRange(accounts[1], 10001, 11001, {'from': accounts[2]})
    check_ranges(
        [(5000, 11001)],
        [(11001, 20001)],
        [(1, 5000), (20001, 30001)],
        []
    )


def test_start_absolute(check_ranges, accounts, nft):
    '''touch start, absolute'''
    nft.transferRange(accounts[4], 1, 100, {'from': accounts[1]})
    check_ranges(
        [(100, 10001)],
        [(10001, 20001)],
        [(20001, 30001)],
        [(1, 100)]
    )


def test_stop_partial_different(check_ranges, accounts, nft):
    '''partial, touch stop, no merge'''
    nft.transferRange(accounts[4], 19000, 20001, {'from': accounts[2]})
    check_ranges(
        [(1, 10001)],
        [(10001, 19000)],
        [(20001, 30001)],
        [(19000, 20001)]
    )


def test_stop_partial_same_abs(check_ranges, accounts, nft):
    '''partial, touch stop, merge, absolute'''
    nft.transferRange(accounts[3], 19000, 20001, {'from': accounts[2]})
    check_ranges(
        [(1, 10001)],
        [(10001, 19000)],
        [(19000, 30001)],
        []
    )


def test_stop_partial_same(check_ranges, accounts, nft):
    '''partial, touch stop, merge'''
    nft.transferRange(accounts[1], 25000, 30001, {'from': accounts[3]})
    nft.transferRange(accounts[3], 19000, 20001, {'from': accounts[2]})
    check_ranges(
        [(1, 10001), (25000, 30001)],
        [(10001, 19000)],
        [(19000, 25000)],
        []
    )


def test_stop_absolute(check_ranges, accounts, nft):
    '''partial, touch stop, absolute'''
    nft.transferRange(accounts[4], 29000, 30001, {'from': accounts[3]})
    check_ranges(
        [(1, 10001)],
        [(10001, 20001)],
        [(20001, 29000)],
        [(29000, 30001)]
    )


def test_whole_range_different(check_ranges, accounts, nft):
    '''whole range, no merge'''
    nft.transferRange(accounts[4], 10001, 20001, {'from': accounts[2]})
    check_ranges(
        [(1, 10001)],
        [],
        [(20001, 30001)],
        [(10001, 20001)]
    )


def test_whole_range_same(check_ranges, accounts, nft):
    '''whole range, merge both sides'''
    nft.transferRange(accounts[3], 5000, 10001, {'from': accounts[1]})
    nft.transferRange(accounts[1], 25001, 30001, {'from': accounts[3]})
    nft.transferRange(accounts[3], 10001, 20001, {'from': accounts[2]})
    check_ranges(
        [(1, 5000), (25001, 30001)],
        [],
        [(5000, 25001)],
        []
    )


def test_whole_range_same_left(check_ranges, accounts, nft):
    '''whole range, merge both sides, absolute left'''
    nft.transferRange(accounts[1], 20001, 25000, {'from': accounts[3]})
    nft.transferRange(accounts[1], 10001, 20001, {'from': accounts[2]})
    check_ranges(
        [(1, 25000)],
        [],
        [(25000, 30001)],
        []
    )


def test_whole_range_same_right(check_ranges, accounts, nft):
    '''whole range, merge both sides, absolute right'''
    nft.transferRange(accounts[3], 5000, 10001, {'from': accounts[1]})
    nft.transferRange(accounts[3], 10001, 20001, {'from': accounts[2]})
    check_ranges(
        [(1, 5000)],
        [],
        [(5000, 30001)],
        []
    )


def test_whole_range_same_both(check_ranges, accounts, nft):
    '''whole range, merge both sides, absolute both'''
    nft.transferRange(accounts[3], 1, 10001, {'from': accounts[1]})
    nft.transferRange(accounts[3], 10001, 20001, {'from': accounts[2]})
    check_ranges(
        [],
        [],
        [(1, 30001)],
        []
    )


def test_whole_range_left_abs(check_ranges, accounts, nft):
    '''whole range, merge left, absolute'''
    nft.transferRange(accounts[1], 10001, 20001, {'from': accounts[2]})
    check_ranges(
        [(1, 20001)],
        [],
        [(20001, 30001)],
        []
    )


def test_whole_range_left(check_ranges, accounts, nft):
    '''whole range, merge left'''
    nft.transferRange(accounts[3], 1, 5001, {'from': accounts[1]})
    nft.transferRange(accounts[1], 10001, 20001, {'from': accounts[2]})
    check_ranges(
        [(5001, 20001)],
        [],
        [(1, 5001), (20001, 30001)],
        []
    )


def test_whole_range_right_abs(check_ranges, accounts, nft):
    '''whole range, merge right, absolute'''
    nft.transferRange(accounts[3], 10001, 20001, {'from': accounts[2]})
    check_ranges(
        [(1, 10001)],
        [],
        [(10001, 30001)],
        []
    )


def test_whole_range_right(check_ranges, accounts, nft):
    '''whole range, merge right'''
    nft.transferRange(accounts[1], 25001, 30001, {'from': accounts[3]})
    nft.transferRange(accounts[3], 10001, 20001, {'from': accounts[2]})
    check_ranges(
        [(1, 10001), (25001, 30001)],
        [],
        [(10001, 25001)],
        []
    )
