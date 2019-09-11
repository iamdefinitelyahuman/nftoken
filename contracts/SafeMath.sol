pragma solidity ^0.5.11;


library SafeMath {

    function mul(uint256 _a, uint256 _b) internal pure returns (uint256) {
        if (_a == 0) {
            return 0;
        }

        uint256 c = _a * _b;
        require(c / _a == _b);

        return c;
    }

    function div(uint256 _a, uint256 _b) internal pure returns (uint256) {
        require(_b > 0);
        uint256 c = _a / _b;

        return c;
    }

    function sub(uint256 _a, uint256 _b) internal pure returns (uint256) {
        require(_b <= _a); // dev: underflow
        uint256 c = _a - _b;

        return c;
    }

    function add(uint256 _a, uint256 _b) internal pure returns (uint256) {
        uint256 c = _a + _b;
        require(c >= _a); // dev: overflow

        return c;
    }

    function mod(uint256 _a, uint256 _b) internal pure returns (uint256) {
        require(_b != 0);
        return _a % _b;
    }
}


library SafeMath64 {

    function mul(uint64 _a, uint64 _b) internal pure returns (uint64) {
        if (_a == 0) {
            return 0;
        }

        uint64 c = _a * _b;
        require(c / _a == _b);

        return c;
    }

    function div(uint64 _a, uint64 _b) internal pure returns (uint64) {
        require(_b > 0);
        uint64 c = _a / _b;

        return c;
    }

    function sub(uint64 _a, uint64 _b) internal pure returns (uint64) {
        require(_b <= _a); // dev: underflow
        uint64 c = _a - _b;

        return c;
    }

    function add(uint64 _a, uint64 _b) internal pure returns (uint64) {
        uint64 c = _a + _b;
        require(c >= _a); // dev: overflow

        return c;
    }

    function mod(uint64 _a, uint64 _b) internal pure returns (uint64) {
        require(_b != 0);
        return _a % _b;
    }
}
