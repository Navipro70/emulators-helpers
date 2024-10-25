import json

from tonutils.client import TonapiClient
from tonutils.wallet import WalletV5R1

# API key for accessing the Tonapi (obtainable from https://tonconsole.com)
API_KEY = ""
IS_TESTNET = False  # Set to True for test network, False for main network
WALLETS = 220  # Укажите нужное количество кошельков


def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)

    mnemonics = []
    addresses = []

    for _ in range(WALLETS):
        wallet, public_key, private_key, mnemonic = WalletV5R1.create(client)

        mnemonics.append(" ".join(mnemonic))
        addresses.append(wallet.address.to_str(True, True, False))

    with open("mnemonics.json", "w") as json_file:
        json.dump(mnemonics, json_file, indent=4)

    with open("addresses.txt", "w") as txt_file:
        for address in addresses:
            txt_file.write(f"{address}\n")

    with open("mnemonics.txt", "w") as txt_file:
        for mnemonic in mnemonics:
            txt_file.write(f"{mnemonic}\n")

    print(
        f"Generated {WALLETS} wallets. Mnemonics saved to 'mnemonics.json' and addresses saved to 'addresses.txt'."
    )


if __name__ == "__main__":
    main()
