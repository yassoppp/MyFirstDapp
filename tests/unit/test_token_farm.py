from brownie import network,exceptions
from scripts.helpful_scripts import get_account,LOCAL_BLOCKCHAIN_ENVIRONMENTS,get_contract
import pytest
from scripts.deploy import deploy_token_farm 

def test_set_pricefee():
    account = get_account()
    non_owner=get_account(index=1)
    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        pytest.skip("pas ici a frerot")
    token_farm,dapp_token=deploy_token_farm()


    token_farm.setPricefee(dapp_token,get_contract("dai_usd_price_feed"),{"from":account})
    assert token_farm.tokentopricefee(dapp_token.address)==get_contract("dai_usd_price_feed").address
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPricefee(dapp_token,get_contract("dai_usd_price_feed"),{"from":non_owner})


#








def test_stake_tokens(amount_staked):
    account = get_account()
    non_owner=get_account(index=1)
    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        pytest.skip("pas ici a frerot")
    token_farm,dapp_token=deploy_token_farm()
    dapp_token.approve(token_farm.address,amount_staked,{"from":account})
    token_farm.stake(amount_staked,dapp_token.address,{"from":account})
    assert token_farm.TokenToStaker(dapp_token.address,account.address)==amount_staked
    assert token_farm.num_token_per_user(account.address)==1
    assert token_farm.stakers(0)==account
    return token_farm,dapp_token

