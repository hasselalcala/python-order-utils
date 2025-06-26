from eth_account import Account


class Signer:
    """
    Signs orders using a private key
    """

    def __init__(self, key: str):
        self._key = key
        self.account = Account.from_key(key)

    def sign(self, struct_hash) -> str:
        """
        Signs an EIP712 struct hash
        """

        print("->>>> struct_hash: ", struct_hash)
        signature = Account._sign_hash(struct_hash, self._key).signature.hex()
        print("->>>> signature: ", signature)
        return signature

    def address(self) -> str:
        return self.account.address
