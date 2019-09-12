pragma solidity ^0.5.11;

import "./NFToken.sol";

/**
    @title Mintable/Burnable Non-Fungible ERC20
    @author Ben Hauser - @iamdefinitelyahuman
    @author with guidance from Gabriel Shapiro - @lex-node
    @dev
        Expands upon the ERC20 token standard
        https://theethereum.wiki/w/index.php/ERC20_Token_Standard
 */
contract NFTokenMintable is NFToken {

    address owner;

    /**
        @notice constructor method
        @param _name Token Name
        @param _symbol Token symbol
        @param _totalSupply Total supply (assigned to msg.sender)
     */
    constructor(
        string memory _name,
        string memory _symbol,
        uint64 _totalSupply
    )
        public
        NFToken(_name, _symbol, _totalSupply)
    {
        owner = msg.sender;
    }

    /**
        @notice Mints new tokens
        @dev Only the owner can mint tokens
        @param _target Address to assign new tokens to
        @param _value Number of tokens to mint
        @return Bool success
     */
    function mint(address _target, uint64 _value) external returns (bool) {
        require(msg.sender == owner); // dev: only owner
        require(_value > 0); // dev: mint 0
        require(upperBound.add(_value) <= MAX_UPPER_BOUND); // dev: upper bound
        uint64 _start = upperBound.add(1);
        uint64 _stop = _start + _value;
        if (rangeMap[tokens[upperBound]].owner == _target) {
            /* merge with previous range */
            uint64 _pointer = tokens[upperBound];
            rangeMap[_pointer].stop = _stop;
        } else {
            /* create new range */
            _setRange(_start, _target, _stop);
            balances[_target].ranges[balances[_target].length] = _start;
            balances[_target].length = balances[_target].length.add(1);
        }
        balances[_target].balance = balances[_target].balance.add(_value);
        totalSupply = totalSupply.add(_value);
        upperBound = upperBound.add(_value);
        emit Transfer(ZERO_ADDRESS, _target, _value);
        emit TransferRange(ZERO_ADDRESS, _target, _start, _stop, _value);
        return true;
    }

    /**
        @notice Burns tokens
        @dev
            * Only the owner can burn tokens
            * Only tokens held by the owner can be burned
            * Cannot burn multiple ranges in a single call
        @param _start Start index of range to burn
        @param _stop Stop index of range to burn
        @return Bool success
     */
    function burn(uint64 _start, uint64 _stop) external returns (bool) {
        require(msg.sender == owner); // dev: only owner
        require(_stop > _start); // dev: burn 0
        uint64 _pointer = _getPointer(_stop-1);
        require(_pointer <= _start); // dev: multiple ranges
        address _target = rangeMap[_pointer].owner;
        require(_target == owner); // dev: only owner tokens
        if (rangeMap[_pointer].stop > _stop) {
            _splitRange(_stop);
        }
        if (_pointer < _start) {
            _splitRange(_start);
        }
        _replaceInBalanceRange(_target, _start, 0);
        uint64 _value = _stop.sub(_start);
        totalSupply = totalSupply.sub(_value);
        balances[_target].balance = balances[_target].balance.sub(_value);
        emit Transfer(_target, ZERO_ADDRESS, _value);
        emit TransferRange(_target, ZERO_ADDRESS, _start, _stop, _value);
        rangeMap[_start].owner = ZERO_ADDRESS;
        return true;
    }

    /**
        @notice Splits a range during burning
        @param _split Index to split the range at
     */
    function _splitRange(uint64 _split) internal {
        uint64 _pointer = _getPointer(_split);
        Range storage r = rangeMap[_pointer];
        uint64 _stop = r.stop;
        r.stop = _split;
        _replaceInBalanceRange(r.owner, 0, _split);
        _setRangePointers(_pointer, _stop, 0);
        _setRangePointers(_pointer, _split, _pointer);
        _setRange(_split, r.owner, _stop);
    }

}
