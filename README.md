The following are only development notes. This repo is in heavy development at this time

# LND setup

```
docker pull lnzap/lnd
docker run -v lnd-data:/lnd --name=lnd-node -d \
    -p 9735:9735 \
    -p 10009:10009 \
    lnzap/lnd:latest \
    --bitcoin.active \
    --bitcoin.testnet \
    --debuglevel=info \
    --bitcoin.node=neutrino \
    --neutrino.connect=testnet1-btcd.zaphq.io \
    --neutrino.connect=testnet2-btcd.zaphq.io \
    --autopilot.active \
    --rpclisten=0.0.0.0:10009
docker start lnd-node 

# Example commands
docker exec -it lnd-node lncli --tlscertpath /lnd/.lnd/tls.cert getinfo
docker exec -it lnd-node lncli --tlscertpath /lnd/.lnd/tls.cert --macaroonpath
/lnd/.lnd/data/chain/bitcoin/testnet/admin.macaroon getinfo
```

# Bitcoind setup
```
docker pull jamesob/bitcoind 
docker run --name bitcoind-node -d \
    -p 8333:8333 \
    -p 127.0.0.1:8332:8332 \
    -p 127.0.0.1:18332:18332 \
    -p 127.0.0.1:18443:18443 \
    --env 'BTC_RPCUSER=user' \
    --env 'BTC_RPCPASSWORD=password' \
    --env 'BTC_RPCPORT=18332' \
    --env 'BTC_TXINDEX=1' \
    --env 'BTC_TESTNET=1' \
    --env 'BTC_DISABLEWALLET=0' \
    --volume $HOME/.bitcoin:/root/.bitcoin \
    jamesob/bitcoind
```
