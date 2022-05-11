// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract TokenFarm is Ownable {
    address[] public allowedToken;
    mapping(address=>mapping(address=>uint256)) public TokenToStaker;
    address[] public stakers;
    mapping(address=>uint256) public num_token_per_user;
    mapping(address=>address) public tokentopricefee;
    IERC20 public dapp_contract;
    constructor(address _dapp_address)public{
        dapp_contract=IERC20(_dapp_address);
    }

    function setPricefee(address token,address pricefee) public onlyOwner{
        tokentopricefee[token]=pricefee;
    }

    function stake(uint256 amount, address token) public {
        require(amount > 0);
        require(is_allowed(token));
        IERC20(token).transferFrom(msg.sender,address(this),amount);
        update(msg.sender,token);
        TokenToStaker[token][msg.sender]=TokenToStaker[token][msg.sender]+amount;
        if(num_token_per_user[msg.sender]==1){
            stakers.push(msg.sender);
        }
    }
    function update(address user,address token) internal{
            if(TokenToStaker[token][user]<=0){
                num_token_per_user[user]++;
            }
    }

    function add_token(address token) public onlyOwner {
        allowedToken.push(token);
    }

    function is_allowed(address token) public view returns (bool) {
        for (uint256 i = 0; i < allowedToken.length; i++) {
            if (allowedToken[i] == token) {
                return true;
            }
        }
        return false;
    }

    function unstake(address token)public{
        require(TokenToStaker[token][msg.sender]>0);
        IERC20(token).transfer(msg.sender,TokenToStaker[token][msg.sender]);
        TokenToStaker[token][msg.sender]=0;
        num_token_per_user[msg.sender]--;
    }

    function issueToken()public{
        for(uint256 i=0;i<stakers.length;i++){
            dapp_contract.transfer(stakers[i],recomto_user(stakers[i]));
        }
    }
    function (address user)internal view returns(uint256){
        uint256 total=0;
        for(uint256 i=0;i<allowedToken.length;i++){
            total=total+recomto_user_to_token(user,allowedToken[i]);
        }
        return total;
    }

    function recomto_user_to_token(address user,address token) internal view returns(uint256){
        if(TokenToStaker[token][user]<=0){
            return 0;
        }
        (uint256 price,uint256 decimals)=getTokenvalue(token);
        uint256 amount=TokenToStaker[token][user];
        return amount*price/(10**decimals);
    }

    function getTokenvalue(address token) public view returns(uint256,uint256){
        AggregatorV3Interface pricefee=AggregatorV3Interface(tokentopricefee[token]);
        (,int256 price,,,)=pricefee.latestRoundData();
        uint256 decimals=uint256(pricefee.decimals());
        return (uint256(price),decimals);


    }
}
