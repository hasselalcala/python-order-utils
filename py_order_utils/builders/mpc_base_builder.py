from ..MPCSigner import MPCSigner
from ..utils import normalize_address
from poly_eip712_structs import make_domain, EIP712Struct


class MPCBaseBuilder:
    def __init__(
        self, exchange_address: str, chain_id: int, signer: MPCSigner, salt_generator
    ):
        self.contract_address = normalize_address(exchange_address)
        self.signer = signer
        self.chain_id = chain_id
        self.domain_separator = self._get_domain_separator(
            self.chain_id, self.contract_address
        )
        self.salt_generator = salt_generator

    def _get_domain_separator(
        self, chain_id: int, verifying_contract: str
    ) -> EIP712Struct:
        return make_domain(
            name="Polymarket CTF Exchange",
            version="1",
            chainId=str(chain_id),
            verifyingContract=verifying_contract,
        )