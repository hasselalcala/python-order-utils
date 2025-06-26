from .base_builder import BaseBuilder
from py_clob_client.MPCSigner import MPCSigner
from ..utils import generate_seed, normalize_address, prepend_zx
from .exception import ValidationException
from ..model.order import OrderData, Order, SignedOrder
from ..model.sides import BUY, SELL
from ..model.signatures import EOA, POLY_GNOSIS_SAFE, POLY_PROXY

class MpcOrderBuilder(BaseBuilder):
    
    """
    Order builder for MPC signing
    """

    def __init__(
        self,
        exchange_address: str,
        chain_id: int,
        signer: MPCSigner,
        salt_generator=generate_seed,
    ):
        super().__init__(exchange_address, chain_id, signer, salt_generator)

    def build_order(self, data: OrderData) -> Order:
        """
        Builds an order
        """
        if not self._validate_inputs(data):
            raise ValidationException("Invalid order inputs")

        if data.signer is None:
            data.signer = data.maker

        if data.signer != self.signer.ota_account:  # Cambiar a ota_account
            raise ValidationException("Signer does not match")

        if data.expiration is None:
            data.expiration = "0"

        if data.signatureType is None:
            data.signatureType = EOA

        return Order(
            salt=int(self.salt_generator()),
            maker=normalize_address(data.maker),
            signer=normalize_address(data.signer),
            taker=normalize_address(data.taker),
            tokenId=int(data.tokenId),
            makerAmount=int(data.makerAmount),
            takerAmount=int(data.takerAmount),
            expiration=int(data.expiration),
            nonce=int(data.nonce),
            feeRateBps=int(data.feeRateBps),
            side=int(data.side),
            signatureType=int(data.signatureType),
        )

    async def build_order_signature(self, _order: Order) -> str:
        """
        Signs the order using MPC
        """
        value_to_sign = self._create_struct_hash(_order)
        
        if value_to_sign.startswith('0x'):
            value_to_sign = value_to_sign[2:]
        
        sig = await self.signer.sign(value_to_sign)
        return sig

    async def build_signed_order(self, data: OrderData) -> SignedOrder:
        """
        Builds and signs a order using the MPC signer
        """
        order = self.build_order(data)
        sig = await self.build_order_signature(order)
        print("\n\n ->>>>> SIGNED ORDER local: ", order, sig)
        return SignedOrder(order, sig)
    
    def _validate_inputs(self, data: OrderData) -> bool:
        return not (
            data.maker is None
            or data.tokenId is None
            or data.makerAmount is None
            or data.takerAmount is None
            or data.side is None
            or data.side not in [BUY, SELL]
            or not data.feeRateBps.isnumeric()
            or int(data.feeRateBps) < 0
            or not data.nonce.isnumeric()
            or int(data.nonce) < 0
            or not data.expiration.isnumeric()
            or int(data.expiration) < 0
            or data.signatureType is None
            or data.signatureType not in [EOA, POLY_GNOSIS_SAFE, POLY_PROXY]
        )