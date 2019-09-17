# NFToken

`NFToken` is a non-fungible implementation of the ERC20 standard, allowing scaleable NFT transfers with fixed gas costs.

## Motivations

`NFToken` is inspired by discussions with [Gabriel Shapiro](https://twitter.com/lex_node) about the legal benefits and technical challenges of representing certificated shares on the Ethereum blockchain. See his excellent article "[Tokenizing Corporate Capital Stock](https://gabrielshapiro.wordpress.com/2018/10/28/2/)" for more information on this subject.

The goal in building `NFToken` was to create a token that is transferrable like an ERC20, allows anyone to verify the complete chain of custody for any given token, and does not have prohibitively high gas costs for large transfers.

The implementation in this repository is a minimal proof of concept that can serve as a starting point for those who wish to expand upon these ideas and integrate them within their own projects. We have also produced an expanded version as an integral component of the [ZeroLaw Augmentation Protocol (ZAP)](https://github.com/iamdefinitelyahuman/ZAP-Tech), that allows unique attributes to be applied on a per-token basis.

## How it Works

`NFToken` applies a unique, sequential index value to every token. The first token minted will have an index value of `1`. The maximum index value is `18446744073709551616` (`2^64-2`). References to token ranges are in the format `start:stop` where the final included value is `stop-1`. For example, a range of `2:6` would contains tokens `2`, `3`, `4` and `5`.

Rather than storing every individual ID number, the contract only records the start and end of each token range. It takes advantage of the lack of cost in declaring empty storage, and saves range data in long fixed-length arrays.

Each transfer of tokens will include one or more `TransferRange` events. Monitoring this event allows you to track the chain of custody for each token.

## Gas Costs

The upper bound cost to mint is `~500,000` gas. This mints `2^64-2` tokens - the maximum `totalSupply` for the contract.

The upper bound gas cost to transfer a single range is `~86,000` gas for the first range, and `~38,000` for each additional range. With a maximally framented token range, transferring one hundred tokens with a single token per range will cost `~39,000` gas per token.

However, **transfer costs remain consistent regardless of the size of the range**. This means the absolute lower bound cost, transfering `2^64-2` tokens as a single range, is `~0.00000000145` gas per token. A more reasonable lower bound, transferring one hundred tokens within a single range, costs `~860` gas per token.

The contract will merge ranges whenever possible, however fragmentation is inevitable and over time transfer costs are expected to increase. There are likely further optimizations that can be performed on this code to decrease costs and reduce the rate of fragmentation. If you have any ideas, [I would love to hear from you](mailto:b.hauser@zerolaw.tech).

## Interface

`NFToken` fully implements the [ERC20 interface](https://theethereum.wiki/w/index.php/ERC20_Token_Standard) and adheres to all [expected behaviours](https://eips.ethereum.org/EIPS/eip-20). It also includes additional methods for working with token ranges, minting, and burning.

### Working with Token Ranges

Tokens may be transferred via the standard ERC20 `transfer` and `transferFrom` methods, however if calling these methods there is no guarantee which specific tokens will be sent. The `transferRange` method allows a user to select exactly which tokens to transfer.

The following methods are available for accessing range data and initiating transfers:

#### `rangesOf`

```javascript
function rangesOf(address _owner) external view returns (uint64[2][] memory)
```

Getter method that returns the `start:stop` indexes of each token range belonging to `_owner`.

```python
>>> nft.rangesOf(accounts[1])
((1, 1000), (2000, 10001))
```

#### `getRange`

```javascript
function getRange(uint256 _idx) external view returns (address _owner, uint64 _start, uint64 _stop)
```

Getter method that returns information about the range contains token `_idx`.

```python
>>> token.getRange(31337).dict()
{
    '_owner': "0xf414d65808f5f59aE156E51B97f98094888e7d92",
    '_start': 30000,
    '_stop': 35001,
}
```

#### `transferRange`

```javascript
function transferRange(address _to, uint64 _start, uint64 _stop) external returns (bool)
```

Transfers the token range ``_start:_stop`` from ``msg.sender`` to ``_to``. Transferring a partial range is allowed. Transferring tokens from multiple ranges in the same call is not.

All transfers will emit one ``Transfer`` and one or more ``TransferRange`` events.

```python
>>> nft.rangesOf(accounts[1])
((1, 1000), (2000, 10001))
>>> nft.transferRange(accounts[2], 3333, 4242, {'from': accounts[1]})
Transaction sent: 0x9ae3c41984aad767b2a535a5ade8f70b104b125da622124e9c3be52b7e373a11
NFToken.transferRange confirmed - block: 4   gas used: 134829 (100.00%)

>>> nft.rangesOf(accounts[1])
((1, 1000), (2000, 3333), (4242, 10001))
```

### Minting and Burning

`NFTokenMintable` inherits `NFToken`, and includes functionality for minting and burning tokens.

#### `mint`

```javascript
function mint(address _target, uint64 _value) external returns (bool)
```

Mints `_value` new tokens that are owned by `_target`.

```python
>>> nft.rangesOf(accounts[0])
((1, 1001),)
>>> nft.mint(accounts[0], 5000, {'from': accounts[0]})
Transaction sent: 0x77ec76224d90763641971cd61e99711c911828053612cc16eb2e5d7faa20815e
NFToken.mint confirmed - block: 3   gas used: 182038 (100.00%)

>>> nft.rangesOf(accounts[0])
((1, 6001),)
```

#### `burn`

```javascript
function burn(uint64 _start, uint64 _stop) external returns (bool)
```

Burns the tokens within the range `_start:_stop`. Only the contract owner can call to burn, and only tokens belonging to the owner can be burned.

```python
>>> nft.burn(accounts[0], 42, 1337, {'from': accounts[0]})
Transaction sent: 0x5414b31e3e44e657ed5ee04c0c6e4c673ab2c6300f392dfd7c282b348db0bbc7
NFToken.burn confirmed - block: 6   gas used: 48312 (100.00%)

>>> nft.rangesOf(accounts[0])
((1, 42), (1337, 6001))
```

## Testing

Unit testing and deployment of this project is performed with [Brownie](https://github.com/iamdefinitelyahuman/brownie).

To run the tests:

```bash
$ pytest tests/
```

A [dockerfile](Dockerfile) is available if you are experiencing issues.

## License

This project is licensed under the [MIT](https://github.com/iamdefinitelyahuman/nftoken/blob/master/LICENSE) license.
