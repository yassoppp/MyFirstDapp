import shutil
from scripts.helpful_scripts import get_account, get_contract
from brownie import DAPP, TokenFarm
import os
import shutil 
import yaml
import json

KEPT = 5 * (10**18)


def main():
    deploy_token_farm(front_end=True)


def deploy_token_farm(front_end=False):
    account = get_account()
    dapp_token = DAPP.deploy({"from": account})
    token_farm = TokenFarm.deploy(dapp_token.address, {"from": account})
    tx = dapp_token.transfer(
        token_farm.address, dapp_token.totalSupply() - KEPT, {"from": account}
    )
    tx.wait(1)
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")

    diction = {
        dapp_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }

    add_allowed_tokkens(token_farm, diction, account)
    if front_end:
        update_front_end()
    return token_farm, dapp_token


def add_allowed_tokkens(token_farm, diction, account):
    for token in diction:
        tx = token_farm.add_token(token.address, {"from": account})
        tx.wait(1)
        set_tx = token_farm.setPricefee(
            token.address, diction[token].address, {"from": account}
        )  #######################################################
        set_tx.wait(1)


def update_front_end():
    copyFoldertofrontend("./build","./front_end/src/info")
    # Sending the front end our config in JSON format
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open("./front_end/src/brownie-config.json", "w") as brownie_config_json:
            json.dump(config_dict, brownie_config_json)
    print("Front end updated!")
def copyFoldertofrontend(src,dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src,dest)   