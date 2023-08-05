from typing import Dict

from coinpay.api import API


class CoinPay(API):

    def __init__(self,
                 api_key: str,
                 api_secret: str,
                 host: str,
                 timeout: int = None,
                 proxies: Dict = None):
        super().__init__(api_key, api_secret, host, timeout, proxies)

    # CURRENCY METHODS
    from coinpay.processing.currency import get_currencies

    # DEPOSIT METHODS
    from coinpay.processing.deposit import _generate_deposit_address
    from coinpay.processing.deposit import generate_fiat_deposit_address
    from coinpay.processing.deposit import generate_crypto_deposit_address

    # EXCHANGE METHODS
    from coinpay.processing.exchange import create_exchange
    from coinpay.processing.exchange import calculate_exchange
    from coinpay.processing.exchange import repeat_exchange
    from coinpay.processing.exchange import cancel_exchange

    # EXCHANGE RATE METHODS
    from coinpay.processing.exchange_rate import get_exchange_rate

    # INTERNAL MOVEMENT METHODS
    from coinpay.processing.internal_movement import create_internal_movement
    from coinpay.processing.internal_movement import repeat_internal_movement

    # INVOICE METHODS
    from coinpay.processing.invoice import create_invoice
    from coinpay.processing.invoice import pay_invoice
    from coinpay.processing.invoice import pay_public_invoice

    # PAIR METHODS
    from coinpay.processing.pair import get_pairs

    # ORDERS METHODS
    from coinpay.processing.orders import get_order_details
    from coinpay.processing.orders import get_orders_history

    # USER METHODS
    from coinpay.processing.user import set_account_setting
    from coinpay.processing.user import get_account_info
    from coinpay.processing.user import get_balance

    # WITHDRAWAL METHODS
    from coinpay.processing.withdrawal import create_withdrawal
    from coinpay.processing.withdrawal import repeat_withdrawal
