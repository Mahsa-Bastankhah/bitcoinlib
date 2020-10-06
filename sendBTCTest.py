
#
# Bitcoinlib - Send transaction without wallet and database
#

from bitcoinlib.keys import *
from bitcoinlib.transactions import *
from bitcoinlib.services.services import *

network = 'testnet'
witness_type = 'segwit'
version = 2
prv_wif = 'tprv8ZgxMBicQKsPdMBKZ8uweTpmFq8rJhnYYBrJKMW8J9pXZJo2KajQWaaE7Z2Gq7JEAbM5A4oZwMrVJ6owFfBCxdVBQSSpG7TLa2XZCJgdeac'

mk = HDKey(prv_wif, witness_type=witness_type)

# Create address and check UTXO's
addr_index = 1
k1 = mk.child_private(addr_index)

print("Check UTXO's for address %s" % k1.address())
srv = Service(network='testnet')
utxos = srv.getutxos(k1.address())
print(utxos)
if not utxos:
    print("No utox's found")
    sys.exit()
print("%d utxo's found" % len(utxos))
indx = 2
prev_txid = utxos[indx]['tx_hash']
output_n = utxos[indx]['output_n']
value = utxos[indx]['value']
fee = 1000

# Create and send transaction

addr_to = 'tb1qy0qr0cmv80m0gqkmhcly3t58gggupq2vyg0ruc'
input = Input(prev_hash=prev_txid, output_n=output_n, keys=k1.public(), network='testnet', value=value,
              witness_type=witness_type)
output = Output(value - fee, address=addr_to, network='testnet')
t = Transaction([input], [output], network='testnet', witness_type=witness_type, version=version)
t.sign(k1)
t.verify()
t.info()
s = t.inputs[0].signatures[0].s
print("s: ", s)
print("max s:", int(secp256k1_n / 2))
print("canonical? ", bool(int(s) < secp256k1_n / 2))
print(t.raw_hex())

rawtx = t.raw_hex()
t = Transaction.import_raw(rawtx=rawtx , network="testnet" )
print(t.witness_type)
s1 = t.inputs[0].signatures[0].s
print("s1: ", s1)
print("max s:", int(secp256k1_n / 2))
print("canonical? ", bool(int(s1) < secp256k1_n / 2))
assert(rawtx == t.raw_hex())
assert (s == s1)

