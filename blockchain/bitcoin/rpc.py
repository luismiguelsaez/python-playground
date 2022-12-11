from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from datetime import datetime

rpc_user = "bitcoin"
rpc_pass = "bitcoin"

rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_pass}@127.0.0.1:8332")

blockchain_height = rpc_connection.getblockchaininfo()['blocks']
last_block_hash = rpc_connection.getblockhash(blockchain_height)
last_block = rpc_connection.getblock(last_block_hash)

last_block_date_epoch = datetime.fromtimestamp(last_block['time'])
last_block_date_fmt = datetime.strftime(last_block_date_epoch, '%Y-%m-%d %H:%M:%S')

print(f"Got last block #{blockchain_height} [{last_block_hash}, created at {last_block_date_fmt} with {len(last_block['tx'])} transactions")
