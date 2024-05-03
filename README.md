# Sepolia Auto Faucet (L0, testnet bridge)

## 🔗 Links

🔔 CHANNEL: https://t.me/JamBitPY

💬 CHAT: https://t.me/JamBitChat

💰 DONATION EVM ADDRESS: 0xe23380ae575D990BebB3b81DB2F90Ce7eDbB6dDa


## 📜 Description
This script uses the L0 bridge https://testnetbridge.com/sepolia to automatically obtain Sepolia test tokens from the ARB network. The exchange rate can be found on the bridge website.

The script will take a random ETH value based on min_amount and max_amount in config for bridge.

```At the time of publication 0.0000323 ETH (0.1$) ARB = 1 ETH Sepolia```


## 📦 Installation
`` Required python >= 3.10``

``1. Close the repo and open CMD (console) inside it``

``2. Install requirements: pip install -r requirements.txt``

``3. Setup configuration and accounts``

``4. Run: python run.py``


## ⚙️ Config (config > settings.yaml)

| Name | Description                                        |
| --- |----------------------------------------------------|
| threads | number of accounts that will work in parallel      |
| arb_rpc | ARB RPC URL (if not have, leave the default value) |
| min_amount | min amount to bridge (in ETH)                      |
| max_amount | max amount to bridge (in ETH)                      |
| delay_before_start_min | min delay before account starts working            |
| delay_before_start_max | max delay before account starts working            |


## ⚙️ Accounts format (config > accounts.txt)

- private_key
- mnemonic


## 📝 Results

```angular2html
The script will save success/failed accounts to config > success_accounts.txt and config > failed_accounts.txt
```