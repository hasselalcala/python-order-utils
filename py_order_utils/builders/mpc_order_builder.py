from ..MPCSigner import MPCSigner
from .mpc_base_builder import MPCBaseBuilder
from ..utils import generate_seed

class MpcOrderBuilder(MPCBaseBuilder):
    """
    Order builder
    """

    def __init__(
        self,
        exchange_address: str,
        chain_id: int,
        signer: MPCSigner,
        salt_generator=generate_seed,
    ):
        super().__init__(exchange_address, chain_id, signer, salt_generator)