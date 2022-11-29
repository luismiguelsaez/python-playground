from web3 import Web3
from decimal import Decimal

class EthWallet:
  ETH_ENDPOINT = 'https://mainnet.infura.io/v3'

  def __init__(self, addr: str, eth_ep: str=ETH_ENDPOINT)->None:
    self.addr = addr
    self.eth_endpoint = eth_ep
    self.eth_conn = Web3(Web3.HTTPProvider(self.eth_endpoint))

  def get_balance_wei(self)->int:
    cs_addr = self.eth_conn.toChecksumAddress(self.addr)
    bal = self.eth_conn.eth.get_balance(cs_addr)

    return bal

  def get_balance_ether(self)->Decimal:
    eth_bal = self.get_balance_wei()
    bal = self.eth_conn.fromWei(eth_bal, 'ether')

    return Decimal(bal)


eth_addr = '0xdfsdfasd....'
eth_ep = 'https://mainnet.infura.io/v3/0d0....'

w = EthWallet(
  addr=eth_addr,
  eth_ep=eth_ep
)

print(w.get_balance_ether())
