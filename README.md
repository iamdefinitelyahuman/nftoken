# NFToken

`NFToken` is a non-fungible implementation of the [ERC20 Standard](https://eips.ethereum.org/EIPS/eip-20).

## How it Works

`NFToken` applies a unique, sequential index value to every token. This results in non-fungible tokens that can transfer at scale without prohibitively high gas costs.

The first token minted will have an index value of `1`.  The maximum index value is `18446744073709551616` (`2**64 - 2`).  References to token ranges are in the format `start:stop` where the final included value is `stop-1`.  For example, a range of `2:6` would contains tokens `2`, `3`, `4` and `5`.

Each transfer of tokens will include one or more `TransferRange` events. Monitoring this event allows you to track the chain of custody for each token.

## Motivations

`NFToken` is inspired by discussions with [Gabriel Shapiro](https://twitter.com/lex_node) about the legal benefits and technical challenges of representing certificated shares on the Ethereum blockchain. See his excellent article "[Tokenizing Corporate Capital Stock](https://gabrielshapiro.wordpress.com/2018/10/28/2/)" for more information on this subject.

An expanded version of this contract is an integral component of the [Zerolaw Augmentation Protocol](https://github.com/iamdefinitelyahuman/ZAP-Tech).

## Limitations

Any time a range is created, modified or transferred, it is merged with neighboring ranges if possible. Over time fragmentation of the ranges is inevitable and will result in increased transfer costs. This can be somewhat mitigated with strategic use of the `transferRange` function.

Ultimately, this design is less practical for tokens that have a very large number of holders making small, frequent transfers. It is ideal for cases where a token is expected to transfer infrequently and in large volumes - e.g. unregistered corporate stock.

## Testing

Unit testing and deployment of this project is performed with [Brownie](https://github.com/iamdefinitelyahuman/brownie).

To run the tests:

``bash
$ pytest tests/
``

A [dockerfile](Dockerfile) is available if you are experiencing issues.

## License

This project is licensed under the [MIT](https://github.com/iamdefinitelyahuman/nftoken/blob/master/LICENSE) license.
