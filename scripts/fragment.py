#!/usr/bin/python3

from brownie import NFTokenMintable, accounts


# adjust the amount and range count to test gas costs for large transfers
def main(amount=65535, ranges=100):
    nft = accounts[0].deploy(NFTokenMintable, "NFT", "NFT", 0)
    for i in range(ranges * 2):
        nft.mint(accounts[i % 2], amount, {"from": accounts[0]})
    nft.transfer(accounts[2], nft.balanceOf(accounts[0]), {"from": accounts[0]})
