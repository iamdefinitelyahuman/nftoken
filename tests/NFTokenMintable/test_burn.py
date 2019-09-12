#!/usr/bin/python3

import pytest


def test_burn(accounts, nftmint):
    '''burn'''
    nftmint.mint(accounts[0], 5000, {'from': accounts[0]})
    nftmint.mint(accounts[1], 10000, {'from': accounts[0]})
    nftmint.burn(3001, 5001, {'from': accounts[0]})
    assert nftmint.totalSupply() == 13000
    assert nftmint.balanceOf(accounts[0]) == 3000
    assert nftmint.balanceOf(accounts[1]) == 10000
    nftmint.transfer(accounts[0], 3000, {'from': accounts[1]})
    nftmint.burn(5001, 8001, {'from': accounts[0]})
    assert nftmint.totalSupply() == 10000
    assert nftmint.balanceOf(accounts[0]) == 3000
    assert nftmint.balanceOf(accounts[1]) == 7000
    nftmint.burn(1, 3001, {'from': accounts[0]})
    assert nftmint.totalSupply() == 7000
    assert nftmint.balanceOf(accounts[0]) == 0
    assert nftmint.balanceOf(accounts[1]) == 7000
    nftmint.transfer(accounts[0], 7000, {'from': accounts[1]})
    nftmint.burn(8001, 15001, {'from': accounts[0]})
    assert nftmint.totalSupply() == 0
    assert nftmint.balanceOf(accounts[0]) == 0
    assert nftmint.balanceOf(accounts[1]) == 0


def test_burn_range(accounts, nftmint):
    '''Burn range'''
    nftmint.mint(accounts[1], 10000, {'from': accounts[0]})
    nftmint.mint(accounts[0], 5000, {'from': accounts[0]})
    nftmint.mint(accounts[1], 5000, {'from': accounts[0]})
    assert nftmint.totalSupply() == 20000
    assert nftmint.rangesOf(accounts[0]) == [(10001, 15001), ]
    assert nftmint.rangesOf(accounts[1]) == [(1, 10001), (15001, 20001)]
    nftmint.burn(10001, 15001, {'from': accounts[0]})
    assert nftmint.totalSupply() == 15000
    assert nftmint.rangesOf(accounts[0]) == []
    assert nftmint.rangesOf(accounts[1]) == [(1, 10001), (15001, 20001)]
    assert nftmint.balanceOf(accounts[0]) == 0


def test_burn_all(accounts, nftmint):
    '''Burn total supply'''
    nftmint.mint(accounts[0], 10000, {'from': accounts[0]})
    nftmint.burn(1, 10001, {'from': accounts[0]})
    assert nftmint.totalSupply() == 0
    assert nftmint.balanceOf(accounts[1]) == 0
    assert nftmint.rangesOf(accounts[1]) == ()


def test_burn_inside(accounts, nftmint):
    '''Burn inside'''
    nftmint.mint(accounts[0], 10000, {'from': accounts[0]})
    nftmint.burn(2000, 4000, {'from': accounts[0]})
    assert nftmint.totalSupply() == 8000
    assert nftmint.balanceOf(accounts[0]) == 8000
    assert nftmint.rangesOf(accounts[0]) == [(1, 2000), (4000, 10001)]


def test_burn_left(accounts, nftmint):
    '''Burn left'''
    nftmint.mint(accounts[1], 1000, {'from': accounts[0]})
    nftmint.mint(accounts[0], 9000, {'from': accounts[0]})
    nftmint.burn(1001, 5001, {'from': accounts[0]})
    assert nftmint.totalSupply() == 6000
    assert nftmint.rangesOf(accounts[0]) == [(5001, 10001)]


def test_burn_right(accounts, nftmint):
    '''Burn right'''
    nftmint.mint(accounts[0], 9000, {'from': accounts[0]})
    nftmint.mint(accounts[1], 1000, {'from': accounts[0]})
    nftmint.burn(5001, 9001)
    assert nftmint.totalSupply() == 6000
    assert nftmint.rangesOf(accounts[0]) == [(1, 5001)]


def test_burn_abs_left(accounts, nftmint):
    '''Burn absolute left'''
    nftmint.mint(accounts[0], 10000, {'from': accounts[0]})
    nftmint.burn(1, 5001, {'from': accounts[0]})
    assert nftmint.totalSupply() == 5000
    assert nftmint.rangesOf(accounts[0]) == [(5001, 10001)]


def test_burn_abs_right(accounts, nftmint):
    '''Burn absolute right'''
    nftmint.mint(accounts[0], 10000, {'from': accounts[0]})
    nftmint.burn(5001, 10001, {'from': accounts[0]})
    assert nftmint.totalSupply() == 5000
    assert nftmint.rangesOf(accounts[0]) == [(1, 5001)]


def test_burn_left_one_token(accounts, nftmint):
    '''Burn left one token'''
    nftmint.mint(accounts[1], 1000, {'from': accounts[0]})
    nftmint.mint(accounts[0], 9000, {'from': accounts[0]})
    nftmint.burn(1001, 1002, {'from': accounts[0]})
    assert nftmint.totalSupply() == 9999
    assert nftmint.rangesOf(accounts[0]) == [(1002, 10001)]


def test_burn_right_one_token(accounts, nftmint):
    '''Burn right one token'''
    nftmint.mint(accounts[0], 9000, {'from': accounts[0]})
    nftmint.mint(accounts[1], 1000, {'from': accounts[0]})
    nftmint.burn(9000, 9001, {'from': accounts[0]})
    assert nftmint.totalSupply() == 9999
    assert nftmint.rangesOf(accounts[0]) == [(1, 9000)]


def test_burn_zero(accounts, nftmint):
    '''cannot burn 0 tokens'''
    nftmint.mint(accounts[0], 10000, {'from': accounts[0]})
    with pytest.reverts("dev: burn 0"):
        nftmint.burn(1, 1, {'from': accounts[0]})
    with pytest.reverts("dev: burn 0"):
        nftmint.burn(5000, 5000, {'from': accounts[0]})
    with pytest.reverts("dev: burn 0"):
        nftmint.burn(10000, 10000, {'from': accounts[0]})


def test_burn_exceeds_balance(accounts, nftmint):
    '''burn exceeds balance'''
    with pytest.reverts("dev: exceeds upper bound"):
        nftmint.burn(1, 101, {'from': accounts[0]})
    nftmint.mint(accounts[0], 4000, {'from': accounts[0]})
    with pytest.reverts("dev: exceeds upper bound"):
        nftmint.burn(1, 5001, {'from': accounts[0]})
    nftmint.burn(1, 3001, {'from': accounts[0]})
    with pytest.reverts("dev: exceeds upper bound"):
        nftmint.burn(3001, 4002, {'from': accounts[0]})
    nftmint.burn(3001, 4001, {'from': accounts[0]})
    with pytest.reverts("dev: exceeds upper bound"):
        nftmint.burn(4001, 4101, {'from': accounts[0]})


def test_burn_multiple_ranges(accounts, nftmint):
    '''burn multiple ranges'''
    nftmint.mint(accounts[0], 1000, {'from': accounts[0]})
    nftmint.mint(accounts[1], 1000, {'from': accounts[0]})
    with pytest.reverts("dev: multiple ranges"):
        nftmint.burn(500, 1500, {'from': accounts[0]})


def test_reburn(accounts, nftmint):
    '''cannot burn non-owner tokens'''
    nftmint.mint(accounts[0], 1000, {'from': accounts[0]})
    nftmint.mint(accounts[1], 1000, {'from': accounts[0]})
    with pytest.reverts("dev: only owner tokens"):
        nftmint.burn(1500, 1600, {'from': accounts[0]})
    nftmint.burn(100, 200, {'from': accounts[0]})
    with pytest.reverts("dev: only owner tokens"):
        nftmint.burn(100, 200, {'from': accounts[0]})
