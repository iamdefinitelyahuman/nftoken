#!/usr/bin/python3

import pytest


def test_burn(accounts, nft):
    '''burn'''
    nft.mint(accounts[1], 5000, {'from': accounts[0]})
    nft.mint(accounts[2], 10000, {'from': accounts[0]})
    nft.burn(3001, 5001, {'from': accounts[0]})
    assert nft.totalSupply() == 13000
    assert nft.balanceOf(accounts[1]) == 3000
    assert nft.balanceOf(accounts[2]) == 10000
    nft.burn(5001, 8001, {'from': accounts[0]})
    assert nft.totalSupply() == 10000
    assert nft.balanceOf(accounts[1]) == 3000
    assert nft.balanceOf(accounts[2]) == 7000
    nft.burn(1, 3001, {'from': accounts[0]})
    assert nft.totalSupply() == 7000
    assert nft.balanceOf(accounts[1]) == 0
    assert nft.balanceOf(accounts[2]) == 7000
    nft.burn(8001, 15001, {'from': accounts[0]})
    assert nft.totalSupply() == 0
    assert nft.balanceOf(accounts[1]) == 0
    assert nft.balanceOf(accounts[2]) == 0


def test_burn_range(accounts, nft):
    '''Burn range'''
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    nft.mint(accounts[2], 5000, {'from': accounts[0]})
    nft.mint(accounts[1], 5000, {'from': accounts[0]})
    assert nft.totalSupply() == 20000
    assert nft.rangesOf(accounts[1]) == ((1, 10001), (15001, 20001))
    assert nft.rangesOf(accounts[2]) == ((10001, 15001), )
    nft.burn(10001, 15001, {'from': accounts[0]})
    assert nft.totalSupply() == 15000
    assert nft.rangesOf(accounts[1]) == ((1, 10001), (15001, 20001))
    assert nft.rangesOf(accounts[2]) == ()
    assert nft.balanceOf(accounts[2]) == 0


def test_burn_all(accounts, nft):
    '''Burn total supply'''
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    nft.burn(1, 10001, {'from': accounts[0]})
    assert nft.totalSupply() == 0
    assert nft.balanceOf(accounts[1]) == 0
    assert nft.rangesOf(accounts[1]) == ()


def test_burn_inside(accounts, nft):
    '''Burn inside'''
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    nft.burn(2000, 4000, {'from': accounts[0]})
    assert nft.totalSupply() == 8000
    assert nft.balanceOf(accounts[1]) == 8000
    assert nft.rangesOf(accounts[1]) == ((1, 2000), (4000, 10001))


def test_burn_left(accounts, nft):
    '''Burn left'''
    nft.mint(accounts[2], 1000, {'from': accounts[0]})
    nft.mint(accounts[1], 9000, {'from': accounts[0]})
    nft.burn(1001, 5001, {'from': accounts[0]})
    assert nft.totalSupply() == 6000
    assert nft.rangesOf(accounts[1]) == ((5001, 10001),)


def test_burn_right(accounts, nft):
    '''Burn right'''
    nft.mint(accounts[1], 9000, {'from': accounts[0]})
    nft.mint(accounts[2], 1000, {'from': accounts[0]})
    nft.burn(5001, 9001)
    assert nft.totalSupply() == 6000
    assert nft.rangesOf(accounts[1]) == ((1, 5001),)


def test_burn_abs_left(accounts, nft):
    '''Burn absolute left'''
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    nft.burn(1, 5001, {'from': accounts[0]})
    assert nft.totalSupply() == 5000
    assert nft.rangesOf(accounts[1]) == ((5001, 10001),)


def test_burn_abs_right(accounts, nft):
    '''Burn absolute right'''
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    nft.burn(5001, 10001, {'from': accounts[0]})
    assert nft.totalSupply() == 5000
    assert nft.rangesOf(accounts[1]) == ((1, 5001),)


def test_burn_left_one_token(accounts, nft):
    '''Burn left one token'''
    nft.mint(accounts[2], 1000, {'from': accounts[0]})
    nft.mint(accounts[1], 9000, {'from': accounts[0]})
    nft.burn(1001, 1002, {'from': accounts[0]})
    assert nft.totalSupply() == 9999
    assert nft.rangesOf(accounts[1]) == ((1002, 10001),)


def test_burn_right_one_token(accounts, nft):
    '''Burn right one token'''
    nft.mint(accounts[1], 9000, {'from': accounts[0]})
    nft.mint(accounts[2], 1000, {'from': accounts[0]})
    nft.burn(9000, 9001, {'from': accounts[0]})
    assert nft.totalSupply() == 9999
    assert nft.rangesOf(accounts[1]) == ((1, 9000),)


def test_burn_zero(accounts, nft):
    '''burn 0 nfts'''
    with pytest.reverts("dev: burn 0"):
        nft.burn(1, 1, {'from': accounts[0]})
    nft.mint(accounts[0], 10000, {'from': accounts[0]})
    with pytest.reverts("dev: burn 0"):
        nft.burn(1, 1, {'from': accounts[0]})


def test_burn_exceeds_balance(accounts, nft):
    '''burn exceeds balance'''
    with pytest.reverts("dev: exceeds upper bound"):
        nft.burn(1, 101, {'from': accounts[0]})
    nft.mint(accounts[0], 4000, {'from': accounts[0]})
    with pytest.reverts("dev: exceeds upper bound"):
        nft.burn(1, 5001, {'from': accounts[0]})
    nft.burn(1, 3001, {'from': accounts[0]})
    with pytest.reverts("dev: exceeds upper bound"):
        nft.burn(3001, 4002, {'from': accounts[0]})
    nft.burn(3001, 4001, {'from': accounts[0]})
    with pytest.reverts("dev: exceeds upper bound"):
        nft.burn(4001, 4101, {'from': accounts[0]})


def test_burn_multiple_ranges(accounts, nft):
    '''burn multiple ranges'''
    nft.mint(accounts[0], 1000, {'from': accounts[0]})
    nft.mint(accounts[1], 1000, {'from': accounts[0]})
    with pytest.reverts("dev: multiple ranges"):
        nft.burn(500, 1500, {'from': accounts[0]})


def test_reburn(accounts, nft):
    '''burn already burnt nfts'''
    nft.mint(accounts[0], 1000, {'from': accounts[0]})
    nft.burn(100, 200, {'from': accounts[0]})
    with pytest.reverts("dev: already burnt"):
        nft.burn(100, 200, {'from': accounts[0]})
