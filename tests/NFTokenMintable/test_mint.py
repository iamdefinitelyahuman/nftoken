#!/usr/bin/python3

import pytest

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'


def test_mint(accounts, nftmint):
    '''mint'''
    nftmint.mint(accounts[1], 1000, {'from': accounts[0]})
    assert nftmint.totalSupply() == 1000
    assert nftmint.balanceOf(accounts[1]) == 1000
    nftmint.mint(accounts[2], 2000, {'from': accounts[0]})
    assert nftmint.totalSupply() == 3000
    assert nftmint.balanceOf(accounts[1]) == 1000
    assert nftmint.balanceOf(accounts[2]) == 2000
    nftmint.mint(accounts[1], 3000, {'from': accounts[0]})
    assert nftmint.totalSupply() == 6000
    assert nftmint.balanceOf(accounts[1]) == 4000
    assert nftmint.balanceOf(accounts[2]) == 2000
    nftmint.mint(accounts[2], 4000, {'from': accounts[0]})
    assert nftmint.totalSupply() == 10000
    assert nftmint.balanceOf(accounts[1]) == 4000
    assert nftmint.balanceOf(accounts[2]) == 6000


def test_mint_burn_mint(accounts, nftmint):
    '''mint, burn, mint'''
    nftmint.mint(accounts[0], 10000, {'from': accounts[0]})
    assert nftmint.totalSupply() == 10000
    nftmint.burn(1, 10001, {'from': accounts[0]})
    assert nftmint.totalSupply() == 0
    nftmint.mint(accounts[0], 10000, {'from': accounts[0]})
    assert nftmint.totalSupply() == 10000
    assert nftmint.rangesOf(accounts[0]) == [(10001, 20001,)]
    assert nftmint.getRange(1)[0] == ZERO_ADDRESS


def test_mint_no_merge_owner(accounts, nftmint):
    '''Mint and do not merge'''
    nftmint.mint(accounts[1], 10000, {'from': accounts[0]})
    nftmint.mint(accounts[2], 5000, {'from': accounts[0]})
    assert nftmint.totalSupply() == 15000
    assert nftmint.balanceOf(accounts[1]) == 10000
    assert nftmint.balanceOf(accounts[2]) == 5000
    assert nftmint.rangesOf(accounts[1]) == [(1, 10001)]
    assert nftmint.rangesOf(accounts[2]) == [(10001, 15001)]


def test_mint_merge(accounts, nftmint):
    '''Mint and merge range'''
    nftmint.mint(accounts[1], 10000, {'from': accounts[0]})
    nftmint.mint(accounts[1], 5000, {'from': accounts[0]})
    assert nftmint.totalSupply() == 15000
    assert nftmint.rangesOf(accounts[1]) == [(1, 15001)]
    assert nftmint.balanceOf(accounts[1]) == 15000

def test_mint_one(accounts, nftmint):
    '''mint 1 token'''
    nftmint.mint(accounts[1], 1, {'from': accounts[0]})
    assert nftmint.totalSupply() == 1
    assert nftmint.balanceOf(accounts[1]) == 1
    assert nftmint.rangesOf(accounts[1]) == [(1, 2)]
    nftmint.mint(accounts[2], 1, {'from': accounts[0]})
    assert nftmint.totalSupply() == 2
    assert nftmint.balanceOf(accounts[2]) == 1
    assert nftmint.rangesOf(accounts[2]) == [(2, 3)]
    nftmint.mint(accounts[2], 1, {'from': accounts[0]})
    assert nftmint.totalSupply() == 3
    assert nftmint.balanceOf(accounts[2]) == 2
    assert nftmint.rangesOf(accounts[2]) == [(2, 4)]


def test_mint_zero(accounts, nftmint):
    '''mint 0 tokens'''
    with pytest.reverts("dev: mint 0"):
        nftmint.mint(accounts[0], 0, {'from': accounts[0]})
    nftmint.mint(accounts[0], 10000, {'from': accounts[0]})
    with pytest.reverts("dev: mint 0"):
        nftmint.mint(accounts[0], 0, {'from': accounts[0]})


def test_mint_overflow(accounts, nftmint):
    '''mint - overflows'''
    nftmint.mint(accounts[0], (2**64) - 10, {'from': accounts[0]})
    with pytest.reverts("dev: overflow"):
        nftmint.mint(accounts[0], 1000, {'from': accounts[0]})
    with pytest.reverts("dev: upper bound"):
        nftmint.mint(accounts[0], 9, {'from': accounts[0]})


def test_events(accounts, nftmint):
    tx = nftmint.mint(accounts[1], 1000, {'from': accounts[0]})
    assert 'Transfer' in tx.events
    expected = {'from': ZERO_ADDRESS, 'to': accounts[1], 'amount': 1000}
    assert tx.events['Transfer'] == expected
    assert 'TransferRange' in tx.events
    expected = {'from': ZERO_ADDRESS, 'to': accounts[1], 'start': 1, 'stop': 1001, 'amount': 1000}
    assert tx.events['TransferRange'] == expected
