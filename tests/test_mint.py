#!/usr/bin/python3

import pytest


def test_mint(accounts, nft):
    '''mint'''
    nft.mint(accounts[1], 1000, {'from': accounts[0]})
    assert nft.totalSupply() == 1000
    assert nft.balanceOf(accounts[1]) == 1000
    nft.mint(accounts[2], 2000, {'from': accounts[0]})
    assert nft.totalSupply() == 3000
    assert nft.balanceOf(accounts[1]) == 1000
    assert nft.balanceOf(accounts[2]) == 2000
    nft.mint(accounts[1], 3000, {'from': accounts[0]})
    assert nft.totalSupply() == 6000
    assert nft.balanceOf(accounts[1]) == 4000
    assert nft.balanceOf(accounts[2]) == 2000
    nft.mint(accounts[2], 4000, {'from': accounts[0]})
    assert nft.totalSupply() == 10000
    assert nft.balanceOf(accounts[1]) == 4000
    assert nft.balanceOf(accounts[2]) == 6000


def test_mint_burn_mint(accounts, nft):
    '''mint, burn, mint'''
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    assert nft.totalSupply() == 10000
    nft.burn(1, 10001, {'from': accounts[0]})
    assert nft.totalSupply() == 0
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    assert nft.totalSupply() == 10000
    assert nft.rangesOf(accounts[1]) == ((10001, 20001,),)
    assert nft.getRange(1)[0] == '0x0000000000000000000000000000000000000000'


def test_mint_no_merge_owner(accounts, nft):
    '''Mint and do not merge'''
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    nft.mint(accounts[2], 5000, {'from': accounts[0]})
    assert nft.totalSupply() == 15000
    assert nft.balanceOf(accounts[1]) == 10000
    assert nft.balanceOf(accounts[2]) == 5000
    assert nft.rangesOf(accounts[1]) == ((1, 10001), )
    assert nft.rangesOf(accounts[2]) == ((10001, 15001), )


def test_mint_merge(accounts, nft):
    '''Mint and merge range'''
    nft.mint(accounts[1], 10000, {'from': accounts[0]})
    nft.mint(accounts[1], 5000, {'from': accounts[0]})
    assert nft.totalSupply() == 15000
    assert nft.rangesOf(accounts[1]) == ((1, 15001), )
    assert nft.balanceOf(accounts[1]) == 15000

def test_mint_one(accounts, nft):
    '''mint 1 token'''
    nft.mint(accounts[1], 1, {'from': accounts[0]})
    assert nft.totalSupply() == 1
    assert nft.balanceOf(accounts[1]) == 1
    assert nft.rangesOf(accounts[1]) == ((1, 2), )
    nft.mint(accounts[2], 1, {'from': accounts[0]})
    assert nft.totalSupply() == 2
    assert nft.balanceOf(accounts[2]) == 1
    assert nft.rangesOf(accounts[2]) == ((2, 3), )
    nft.mint(accounts[2], 1, {'from': accounts[0]})
    assert nft.totalSupply() == 3
    assert nft.balanceOf(accounts[2]) == 2
    assert nft.rangesOf(accounts[2]) == ((2, 4), )


def test_mint_zero(accounts, nft):
    '''mint 0 tokens'''
    with pytest.reverts("dev: mint 0"):
        nft.mint(accounts[0], 0, {'from': accounts[0]})
    nft.mint(accounts[0], 10000, {'from': accounts[0]})
    with pytest.reverts("dev: mint 0"):
        nft.mint(accounts[0], 0, {'from': accounts[0]})


def test_mint_overflow(accounts, nft):
    '''mint - overflows'''
    nft.mint(accounts[0], (2**64) - 10, {'from': accounts[0]})
    with pytest.reverts("dev: overflow"):
        nft.mint(accounts[0], 1000, {'from': accounts[0]})
    with pytest.reverts("dev: upper bound"):
        nft.mint(accounts[0], 9, {'from': accounts[0]})
