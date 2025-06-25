from ..MPCSigner import MPCSigner
from ..utils import normalize_address

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
