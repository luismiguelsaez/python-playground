from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from datetime import datetime

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


best_block_hash = rpc_connection.getbestblockhash()
last_block = rpc_connection.getblock(best_block_hash)
block_time = datetime.fromtimestamp(int(last_block['time'])).strftime("%Y-%m-%d %H:%M:%S")

print("Block [{}] mined at {}, has a size of {} bytes and {} transactions".format(last_block['height'], block_time, last_block['size'], len(last_block['tx'])))

peers = rpc_connection.getpeerinfo()

for peer in peers:
    last_transaction_time = datetime.fromtimestamp(int(peer['last_transaction'])).strftime("%Y-%m-%d %H:%M:%S")
    print("- {} - {} - <{} >{}".format(peer['addr'], last_transaction_time, peer['bytessent'], peer['bytesrecv']))
