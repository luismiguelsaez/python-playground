from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from datetime import datetime
from time import sleep


with open("/data/bitcoin/.cookie") as f:
  rpcuserpass = f.read()

try:
  rpc_connection = AuthServiceProxy("http://%s@127.0.0.1:8332"%(rpcuserpass))
except JSONRPCException as exc:
  print("Exception while connecting!")
  exit(1)
except Exception as exc:
  print("General error")
  exit(1)


first_block = 500000


block_hash = rpc_connection.getblockhash(first_block)
while True:
  # Get current block
  block = rpc_connection.getblock(block_hash)

  block_height = block['height']
  block_hash = block['hash']
  block_time = datetime.fromtimestamp(int(block['time'])).strftime("%Y-%m-%d %H:%M:%S")
  block_size = block['size']
  block_tx_count = len(block['tx'])

  print(f"Current block [{block_height}]: {block_hash} at {block_time} ( size: {block_size}, tx: {block_tx_count})")

  # Get next block hash
  block_hash = block['nextblockhash']
  sleep(0.5)
