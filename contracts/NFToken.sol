pragma solidity >=0.4.24 <0.5.0;


/**
    @title Non-Fungible ERC20
    @author Ben Hauser - b.hauser@zerolaw.tech
    @dev
        Expands upon the ERC20 token standard
        https://theethereum.wiki/w/index.php/ERC20_Token_Standard
 */
contract NFToken {

    uint256 constant SENDER = 0;
    uint256 constant RECEIVER = 1;

    uint8 public constant decimals = 0;
    string public name;
    string public symbol;
    uint256 public totalSupply;

    uint48 upperBound;
    uint48[281474976710656] tokens;
    mapping (uint48 => Range) rangeMap;
    mapping (address => Balance) balances;
    mapping (address => mapping (address => uint256)) allowed;

    struct Balance {
        uint48 balance;
        uint48[] ranges;
    }

    struct Range {
        address owner;
        uint48 stop;
    }


    event Transfer(address indexed from, address indexed to, uint256 tokens);
    event Approval(
        address indexed tokenOwner,
        address indexed spender,
        uint256 tokens
    );
    event TransferRange(
        address indexed from,
        address indexed to,
        uint256 start,
        uint256 stop,
        uint256 amount
    );

    constructor() public {
        return;
    }

    /* modifier to ensure a range index is within bounds */
    function _checkBounds(uint256 _idx) internal view {
        if (_idx != 0 && _idx <= upperBound) return;
        revert("Invalid index");
    }

    /**
        @notice Fetch the allowance
        @param _owner Owner of the tokens
        @param _spender Spender of the tokens
        @return integer
     */
    function allowance(
        address _owner,
        address _spender
     )
        external
        view
        returns (uint256)
    {
        return allowed[_owner][_spender];
    }

    /**
        @notice ERC-20 balanceOf standard
        @param _owner Address of balance to query
        @return integer
     */
    function balanceOf(address _owner) public view returns (uint256) {
        return balances[_owner].balance;
    }

    /**
        @notice Fetch information about a range
        @param _idx Token index number
        @return owner, start of range, stop of range, time restriction, tag
     */
    function getRange(
        uint256 _idx
    )
        external
        view
        returns (
            address _owner,
            uint48 _start,
            uint48 _stop
        )
    {
        _checkBounds(_idx);
        _start = _getPointer(_idx);
        Range storage r = rangeMap[_start];
        return (r.owner, _start, r.stop);
    }

    /**
        @notice Fetch the token ranges owned by an address
        @param _owner Address to query
        @return Array of [(start, stop),..]
     */
    function rangesOf(address _owner) external view returns (uint48[2][]) {
        Balance storage b = balances[_owner];
        uint256 _count;
        for (uint256 i; i < b.ranges.length; i++) {
            if (b.ranges[i] > 0) {
                _count++;
            }
        }
        uint48[2][] memory _ranges = new uint48[2][](_count);
        _count = 0;
        for (i = 0; i < b.ranges.length; i++) {
            if (b.ranges[i] > 0) {
                _ranges[_count] = [b.ranges[i], rangeMap[b.ranges[i]].stop];
                _count++;
            }
        }
        return _ranges;
    }

    /**
        @notice Mints new tokens
        @param _owner Address to assign new tokens to
        @param _value Number of tokens to mint
        @return Bool success
     */
    function mint(
        address _owner,
        uint48 _value
    )
        external
        returns (bool)
    {
        require(_value > 0); // dev: mint 0
        require(upperBound + _value > upperBound); // dev: overflow
        require(upperBound + _value <= 2**48 - 2); // dev: upper bound
        uint48 _start = uint48(upperBound + 1);
        uint48 _stop = _start + _value;
        if (rangeMap[tokens[upperBound]].owner == _owner) {
            /* merge with previous range */
            uint48 _pointer = tokens[upperBound];
            rangeMap[_pointer].stop = _stop;
        } else {
            /* create new range */
            _setRange(_start, _owner, _stop);
            balances[_owner].ranges.push(_start);
        }
        uint48 _old = balances[_owner].balance;
        balances[_owner].balance += _value;
        totalSupply += _value;
        upperBound += _value;
        emit Transfer(0x00, msg.sender, _value);
        emit TransferRange(0x00, msg.sender, _start, _stop, _value);
        return true;
    }

    /**
        @notice Burns tokens
        @dev Cannot burn multiple ranges in a single call
        @param _start Start index of range to burn
        @param _stop Stop index of range to burn
        @return Bool success
     */
    function burn(uint48 _start, uint48 _stop) external returns (bool) {
        require(_stop > _start); // dev: burn 0
        uint48 _pointer = _getPointer(_stop-1);
        require(_pointer <= _start); // dev: multiple ranges
        address _owner = rangeMap[_pointer].owner;
        require(_owner != 0x00); // dev: already burnt
        if (rangeMap[_pointer].stop > _stop) {
            _splitRange(_stop);
        }
        if (_pointer < _start) {
            _splitRange(_start);
        }
        _replaceInBalanceRange(_owner, _start, 0);
        uint48 _value = _stop - _start;
        totalSupply -= _value;
        uint48 _old = balances[_owner].balance;
        balances[_owner].balance -= _value;
        emit Transfer(_owner, 0x00, _value);
        emit TransferRange(_owner, 0x00, _start, _stop, _value);
        rangeMap[_start].owner = 0x00;
        return true;
    }

    /**
        @notice ERC-20 transfer standard
        @dev calls to _checkTransfer() to verify permission before transferring
        @param _to Recipient
        @param _value Amount being transferred
        @return bool success
     */
    function transfer(address _to, uint256 _value) external returns (bool) {
        _transfer([msg.sender, _to], _value);
        return true;
    }

    /**
        @notice ERC-20 transferFrom standard
        @dev This will transfer tokens starting from balance.ranges[0]
        @param _from Sender address
        @param _to Receipient address
        @param _value Number of tokens to send
        @return bool success
     */
    function transferFrom(
        address _from,
        address _to,
        uint256 _value
    )
        external
        returns (bool)
    {
        require(
            allowed[_from][msg.sender] >= _value,
            "Insufficient allowance"
        );
        allowed[_from][msg.sender] -= _value;
        _transfer([_from, _to], _value);
        return true;
    }

    /**
        @notice Internal transfer function
        @dev common logic for transfer() and transferFrom()
        @param _auth Address that called the method
        @param _addr Array of receiver/sender address
        @param _value Amount to transfer
     */
    function _transfer(
        address[2] _addr,
        uint256 _value
    )
        internal
    {

        uint48 _smallVal = uint48(_value);
        uint48[] memory _range;

        require(balances[_addr[SENDER]].balance >= _smallVal);
        balances[_addr[SENDER]].balance -= _smallVal;
        balances[_addr[RECEIVER]].balance += _smallVal;

        emit Transfer(_addr[SENDER], _addr[RECEIVER], _value);
        for (uint256 i; i < _range.length; i++) {
            if (_range[i] == 0) continue;
            uint48 _start = _range[i];
            uint48 _stop = rangeMap[_start].stop;
            uint48 _amount = _stop - _start;
            if (_smallVal < _amount) {
                _stop -= _amount - _smallVal;
                _smallVal = 0;
            }
            else {
                _smallVal -= _amount;
            }
            _transferSingleRange(
                _start,
                _addr[SENDER],
                _addr[RECEIVER],
                _start,
                _stop
            );
            if (_smallVal == 0) {
                return;
            }
        }
        revert();
    }

    /**
        @notice transfer tokens with a specific index range
        @dev Can send tokens into a custodian, but not out of one
        @param _to Receipient address
        @param _start Transfer start index
        @param _stop Transfer stop index
        @return bool success
     */
    function transferRange(
        address _to,
        uint48 _start,
        uint48 _stop
    )
        external
        returns (bool)
    {
        _checkBounds(_start);
        _checkBounds(_stop-1);
        require(_start < _stop); // dev: stop < start
        uint48 _pointer = _getPointer(_stop-1);
        require(_pointer <= _start); // dev: multiple ranges

        address[2] memory _addr = [msg.sender, _to];
        uint48[2] memory _range = [_start, _stop];

        uint48 _value = _stop - _start;

        require(
            _addr[SENDER] == rangeMap[_pointer].owner,
            "Sender does not own range"
        );
        require(_addr[SENDER] != _addr[RECEIVER], "Cannot send to self");

        require(_value <= balances[_addr[SENDER]].balance);
        balances[_addr[SENDER]].balance -= _value;
        balances[_addr[RECEIVER]].balance += _value;

        _transferSingleRange(
            _pointer,
            _addr[SENDER],
            _addr[RECEIVER],
            _range[0],
            _range[1]
        );
    }

    /**
        @notice internal - transfer ownership of a single range of tokens
        @param _pointer Range array pointer
        @param _from Sender address
        @param _to Recipient address
        @param _start Start index of range
        @param _stop Stop index of range
     */
    function _transferSingleRange(
        uint48 _pointer,
        address _from,
        address _to,
        uint48 _start,
        uint48 _stop
    )
        internal
    {
        Range storage r = rangeMap[_pointer];
        uint48 _rangeStop = r.stop;
        uint48 _prev = tokens[_start-1];
        emit TransferRange(_from, _to, _start, _stop, _stop-_start);

        if (_pointer == _start) {
            /* touches both */
            if (_rangeStop == _stop) {
                _replaceInBalanceRange(_from, _start, 0);
                bool _left = rangeMap[_prev].owner == _to;
                bool _right = rangeMap[_stop].owner == _to;
                /* no join */
                if (!_left && !_right) {
                    _replaceInBalanceRange(_to, 0, _start);
                    r.owner = _to;
                    return;
                }
                _setRangePointers(_pointer, _stop, 0);
                /* join left */
                if (!_right) {
                    delete rangeMap[_pointer];
                    rangeMap[_prev].stop = _stop;
                    _setRangePointers(_prev, _stop, _prev);
                    return;
                }
                /* join right */
                if (!_left) {
                    _replaceInBalanceRange(_to, _stop, _start);
                    _setRange(_pointer, _to, rangeMap[_stop].stop);
                /* join both */
                } else {
                    _replaceInBalanceRange(_to, _stop, 0);
                    delete rangeMap[_pointer];
                    rangeMap[_prev].stop = rangeMap[_stop].stop;
                    _setRangePointers(_prev, _start, 0);
                    _setRangePointers(_stop, rangeMap[_stop].stop, 0);
                    _setRangePointers(_prev, rangeMap[_prev].stop, _prev);
                }
                delete rangeMap[_stop];
                return;
            }

            /* touches left */
            _setRangePointers(_start, _rangeStop, 0);
            _setRange(_stop, _from, _rangeStop);
            _replaceInBalanceRange(_from, _start, _stop);
            delete rangeMap[_pointer];

            /* same owner left */
            if (rangeMap[_prev].owner == _to) {
                _setRangePointers(_prev, _start, 0);
                _start = _prev;
            } else {
                _replaceInBalanceRange(_to, 0, _start);
            }
            _setRange(_start, _to, _stop);
            return;
        }

        /* shared logic - touches right and touches nothing */
        _setRangePointers(_pointer, _rangeStop, 0);
        r.stop = _start;
        _setRangePointers(_pointer, _start, _pointer);

        /* touches right */
        if (_rangeStop == _stop) {
            /* same owner right */
            if (rangeMap[_stop].owner == _to) {
                _replaceInBalanceRange(_to, _stop, _start);
                _setRangePointers(_stop, rangeMap[_stop].stop, 0);
                uint48 _next = rangeMap[_stop].stop;
                delete rangeMap[_stop];
                _stop = _next;
            } else {
                _replaceInBalanceRange(_to, 0, _start);
            }
            _setRange(_start, _to, _stop);
            return;
        }

        /* touches nothing */
        _replaceInBalanceRange(_to, 0, _start);
        _setRange(_start, _to, _stop);
        _replaceInBalanceRange(_from, 0, _stop);
        _setRange(_stop, _from, _rangeStop);
    }

    /**
        @notice Splits a range
        @dev
            Called when a new tag is added, to prevent a balance range
            where some tokens are tagged differently from others
        @param _split Index to split the range at
     */
    function _splitRange(uint48 _split) internal {
        if (tokens[_split-1] != 0 && tokens[_split] > tokens[_split-1]) return;
        uint48 _pointer = _getPointer(_split);
        Range storage r = rangeMap[_pointer];
        uint48 _stop = r.stop;
        r.stop = _split;
        _replaceInBalanceRange(r.owner, 0, _split);
        _setRangePointers(_pointer, _stop, 0);
        _setRangePointers(_pointer, _split, _pointer);
        _setRange(_split, r.owner, _stop);
    }

    /**
        @notice sets a Range struct and associated pointers
        @dev keeping this as a seperate method reduces gas costs from SSTORE
        @param _pointer Range pointer to set
        @param _owner Address of range owner
        @param _stop Range stop index
     */
    function _setRange(
        uint48 _pointer,
        address _owner,
        uint48 _stop
    )
        internal
    {
        Range storage r = rangeMap[_pointer];
        if (r.owner != _owner) r.owner = _owner;
        if (r.stop != _stop) r.stop = _stop;

        _setRangePointers(_pointer, _stop, _pointer);
    }

    /**
        @notice internal - replace value in balance range array
        @param _addr Balance addresss
        @param _old Token index to remove
        @param _new Token index to add
     */
    function _replaceInBalanceRange(
        address _addr,
        uint48 _old,
        uint48 _new
    )
        internal
    {
        uint48[] storage r = balances[_addr].ranges;
        for (uint256 i; i < r.length; i++) {
            if (r[i] == _old) {
                r[i] = _new;
                return;
            }
        }
        if (_new != 0) {
            r.push(_new);
        }
    }

    /**
        @notice Modify pointers in the token range
        @param _start Start index of range
        @param _stop Stop index of range
        @param _value Pointer value
     */
    function _setRangePointers(uint48 _start, uint48 _stop, uint48 _value) internal {
        tokens[_start] = _value;
        _stop -= 1;
        if (_start == _stop) return;
        tokens[_stop] = _value;
        uint256 _interval = 16;
        while (true) {
            uint256 i = (_stop / _interval * _interval);
            if (i == 0) return;
            _interval *= 16;
            if (i % _interval == 0) continue;
            if (i > _start) tokens[i] = _value;
        }
    }

    /**
        @notice Find an array range pointer
        @dev
            Given a token index, this will iterate through the range
            and return the mapping pointer that the index is present within.
        @param i Token index
     */
    function _getPointer(uint256 i) internal view returns (uint48) {
        uint256 _increment = 1;
        while (true) {
            if (tokens[i] != 0x00) return tokens[i];
            if (i % (_increment * 16) == 0) {
                _increment *= 16;
                require(i <= upperBound); // dev: exceeds upper bound
            }
            i += _increment;
        }
    }
}
