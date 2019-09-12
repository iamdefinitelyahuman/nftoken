#!/usr/bin/python3

import pytest


def test_same_addr(accounts, nft):
    '''send to self'''
    nft.transferRange(accounts[2], 11000, 12000, {'from': accounts[2]})
    nft.transfer(accounts[1], 1000, {'from': accounts[1]})
    nft.approve(accounts[1], 1000, {'from': accounts[1]})
    nft.transferFrom(accounts[1], accounts[1], 1000, {'from': accounts[1]})


def test_zero_tokens(accounts, nft):
    '''send zero tokens'''
    nft.transfer(accounts[1], 0, {'from': accounts[1]})
    nft.transferFrom(accounts[2], accounts[1], 0, {'from': accounts[1]})
