import asyncio
import aiohttp
import logging
import time
import ssl
import certifi
import uuid
import click
import json
import base64

# "pip install pycryptodome" installs Crypto
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad

LOGGER = logging.getLogger(__name__)
BASE_URL_DE = 'https://api.tech26.de'
BASE_URL_GLOBAL = 'https://api.tech26.global'
BASIC_AUTH_HEADERS = {"Authorization": "Basic bmF0aXZld2ViOg=="}
USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/59.0.3071.86 Safari/537.36")


class Api(object):

    def __init__(self, username, password, device_token=None):
        LOGGER.debug(f'N26 init (user: {username})')
        self._token_data = {}
        self.config = {'USERNAME': username,
                       'PASSWORD': password,
                       'DEVICE_TOKEN': device_token if device_token else str(uuid.uuid4()),
                       'MFA_TYPE': 'app'}
        BASIC_AUTH_HEADERS["device-token"] = self.config['DEVICE_TOKEN']

    async def __aenter__(self):
        """
        Runs when an API instance is created with 'async with' (when entering)
        """
        ssl_ctx = ssl.create_default_context(cafile=certifi.where())
        self.connector = aiohttp.TCPConnector(ssl=ssl_ctx)
        return self

    async def __aexit__(self, *info):
        """
        Runs when an API instance is created with 'async with' (when exiting)
        """
        LOGGER.debug(f'N26 exit (user: {self.config["USERNAME"]})')
        await self.connector.close()

    def get_device_token(self) -> str:
        """
        it returns the device_token used for login (it could be the device_token provided, or in case it was not pro-
        vided, it is automatically generated when this Api is instantiated, so you can save it for this user for the
        next time (and use the same one for each user every time, as if the user had only this device to connect)
        :return:
        """
        return self.config['DEVICE_TOKEN']

    async def get_me(self) -> dict:
        """
        Retrieves basic user information

        Example data returned:
        {'birthDate': -190494900000,
         'email': 'user@mail.com',
         'title': '',
         'firstName': 'John',
         'lastName': 'Doe',
         'gender': 'MALE',
         'nationality': 'ARG',
         'mobilePhoneNumber': '+34*****1010',
         'kycFirstName': 'JOHN',
         'kycLastName': 'DOE',
         'id': '1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a',             # userId
         'idNowToken': None,
         'shadowUserId': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',   # '6f723de4-6700-4dfd-92cc-a64d6b14e3d8'
         'signupCompleted': False,
         'transferWiseTermsAccepted': False}
        """
        return await self._request('get', f'{BASE_URL_DE}/api/me')

    async def get_me_statuses(self) -> dict:
        """
        Retrieves additional account information

        Example data returned:
        {'accountClosed': None,
         'cardActivationCompleted': 1579215988830,
         'cardIssued': None,
         'coreDataUpdated': None,
         'created': 1577641998206,
         'emailValidationCompleted': 1577642529368,
         'emailValidationInitiated': 1577641998301,
         'firstIncomingTransaction': None,
         'flexAccount': False,
         'flexAccountConfirmed': 0,
         'id': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',
         'isDeceased': None,
         'kycCompleted': 1577646485958,
         'kycDetails': {'provider': 'SAFENED', 'status': 'COMPLETED'},
         'kycInitiated': 1577645941220,
         'kycPersonalCompleted': None,
         'kycPostIdentCompleted': None,
         'kycPostIdentInitiated': None,
         'kycWebIDCompleted': None,
         'kycWebIDInitiated': None,
         'pairingState': 'PAIRED',
         'phonePairingCompleted': 1579128450643,
         'phonePairingInitiated': 1579128450643,
         'pinDefinitionCompleted': 1579128497062,
         'productSelectionCompleted': 1577643173889,
         'showScreen': None,
         'signingCompleted': False,
         'signingRequired': False,
         'signupStep': None,
         'singleStepSignup': 1577641998206,
         'unpairTokenCreation': None,
         'unpairingProcessStatus': None,
         'updated': 1635771943745,
         'userStatusCol': None}
        """
        return await self._request('get', f'{BASE_URL_DE}/api/me/statuses')

    async def get_addresses(self) -> dict:
        """
        Retrieves a list of addresses of the account owner

        Example data returned:
        {'data': [{'addressLine1': '',
           'city': 'Madrid',
           'cityName': 'Madrid',
           'country': 'ESP',
           'countryName': 'ESP',
           'created': 1577641998301,
           'houseNumberBlock': '32',
           'id': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',
           'state': 'Comunidad de Madrid',
           'street': 'Calle X',
           'streetName': 'Calle X',
           'type': 'SHIPPING',
           'updated': 1579216145233,
           'userId': '1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a',   # userId,
           'zipCode': '24000'},
          {'addressLine1': '',
           'city': 'Villanueva de la Cañada',
           'cityName': 'Villanueva de la Cañada',
           'country': 'ESP',
           'countryName': 'ESP',
           'created': 1577646485817,
           'houseNumberBlock': '252',
           'id': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',
           'state': None,
           'street': 'Calle Y',
           'streetName': 'Y',
           'type': 'PASSPORT',
           'updated': 1577646485817,
           'userId': '1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a',   # userId,
           'zipCode': '28000'},
          {'addressLine1': '',
           'city': 'Villanueva de la Cañada',
           'cityName': 'Villanueva de la Cañada',
           'country': 'ESP',
           'countryName': 'ESP',
           'created': 1577641998301,
           'houseNumberBlock': '252',
           'id': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',
           'state': 'Comunidad de Madrid',
           'street': 'Calle Y',
           'streetName': 'Calle Y',
           'type': 'LEGAL',
           'updated': 1579215988901,
           'userId': '1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a',   # userId,
           'zipCode': '28000'}],
        'paging': {'next': None, 'previous': None, 'totalResults': 3}}

        """
        return await self._request('get', f'{BASE_URL_DE}/api/addresses')

    async def get_barzahlen_check(self) -> dict:
        """

        Example data returned:
        {'atmWithdrawalsCount': '0',
         'atmWithdrawalsSum': '0',
         'cash26WithdrawalsCount': '0',
         'cash26WithdrawalsSum': '0',
         'depositAllowance': '999.0',
         'feeRate': '0.015',
         'monthlyDepositFeeThreshold': '100.0',
         'remainingAmountMonth': '0',
         'success': False,
         'transactionId': None,
         'withdrawAllowance': '999.0'}
        """
        return await self._request('get', f'{BASE_URL_DE}/api/barzahlen/check')

    async def get_spaces(self) -> dict:
        """
        Retrieves a list of all spaces

        Example data returned:
        {'spaces':
           [{'accountId': '2a2a2a2a-2a2a-2a2a-2a2a-2a2a2a2a2a2a',             # accountId,
             'backgroundImageUrl': 'https://cdn.number26.de/spaces/background-images/account_cards_background.jpg?'
                                   'version=1',
             'balance': {'availableBalance': 12345.67, 'currency': 'EUR'},
             'id': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',
             'imageUrl': 'https://cdn.number26.de/spaces/default-images/account_cards.jpg?version=1',
             'isCardAttached': True,
             'isHiddenFromBalance': False,
             'isLocked': False,
             'isPrimary': True,
             'name': 'JOHN'},
            {'accountId': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',
             'backgroundImageUrl': 'https://cdn.number26.de/spaces/background-images/saving_piggy_background.jpg?'
                                   'version=1',
             'balance': {'availableBalance': 0.0, 'currency': 'EUR'},
             'id': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',
             'imageUrl': 'https://cdn.number26.de/spaces/default-images/saving_piggy.jpg?version=1',
             'isCardAttached': False,
             'isHiddenFromBalance': False,
             'isLocked': False,
             'isPrimary': False,
             'name': 'Savings'}],
         'totalBalance': 12345.67,
         'userFeatures': {'availableSpaces': 1, 'canUpgrade': True},
         'visibleBalance': 12345.67}
        """
        return await self._request('get', f'{BASE_URL_DE}/api/spaces')

    async def get_accounts(self) -> dict:
        """
        Retrieves the current balance

        {'availableBalance': 12345.67,
         'bankBalance': 12345.67,
         'bic': 'NTSBESM1XXX',
         'currency': 'EUR',
         'externalId': {'bic': 'NTSBESM1XXX', 'iban': 'ES3211111111111111111111'},
         'iban': 'ES3211111111111111111111',
         'id': '2a2a2a2a-2a2a-2a2a-2a2a-2a2a2a2a2a2a',       # accountId
         'legalEntity': 'ES',
         'usableBalance': 12345.67}
        """
        return await self._request('get', f'{BASE_URL_DE}/api/accounts')

    async def get_settings_account_limits(self) -> list:
        """
        Retrieves a list of all active account limits

        Example data returned:
        [{'amount': 2500.0, 'countryList': None, 'limit': 'POS_TRANSACTION'},
         {'amount': 1000.0, 'countryList': None, 'limit': 'ATM_TRANSACTION'}]
        """
        return await self._request('get', f'{BASE_URL_DE}/api/settings/account/limits')

    async def set_settings_account_limits(self, daily_withdrawal_limit: int = None,
                                          daily_payment_limit: int = None) -> None:
        """
        Sets account limits
        :param daily_withdrawal_limit: daily withdrawal limit
        :param daily_payment_limit: daily payment limit
        """
        if daily_withdrawal_limit is not None:
            await self._request('post', f'{BASE_URL_DE}/api/settings/account/limits', json_={
                                         'limit': 'ATM_DAILY_ACCOUNT',
                                         'amount': daily_withdrawal_limit})

        if daily_payment_limit is not None:
            await self._request('post', f'{BASE_URL_DE}/api/settings/account/limits', json_={
                                         'limit': 'POS_DAILY_ACCOUNT',
                                         'amount': daily_payment_limit})

    async def get_smrt_categories(self) -> list:
        """
        Categories

        Example data returned:
        [{'backgroundUrl': 'https://cdn.number26.de/images/categories/micro-v2-household-utilities.jpeg',
          'base64Image': 'iVBORw0KGgoAAAANSUh...FgCBgChoAhYAgYAoZAGhH4L8krdisUEINBAAAAAElFTkSuQmCC',
          'id': 'micro-v2-household-utilities',
          'name': 'Household & Utilities'},
         {'backgroundUrl': 'https://cdn.number26.de/images/categories/micro-v2-travel-holidays.jpeg',
          'base64Image': 'iVBORw0KGgoAAAANSUh...PAEDAEDAFDwBAwBAwBQ8AQaKwI/D85xwHwF9SCuQAAAABJRU5ErkJggg==',
          'id': 'micro-v2-travel-holidays',
          'name': 'Travel & Holidays'},
          ...
        ]
        """
        return await self._request('get', f'{BASE_URL_DE}/api/smrt/categories')

    async def get_smrt_transactions(self, from_time: int = None, to_time: int = None, limit: int = 500,
                                    pending: bool = None, categories: str = '', text_filter: str = '',
                                    last_id: str = '') -> dict:
        """
        Get a list of transactions.
        Note that some parameters can not be combined in a single request (like text_filter and pending) and
        will result in a bad request (400) error.

        Note: from_time & to_time relate to field "visibleTS"

        :param from_time: earliest transaction time as a Timestamp > 0 - milliseconds since 1970 in CET
        :param to_time: latest transaction time as a Timestamp > 0 - milliseconds since 1970 in CET
        :param limit: Limit the number of transactions to return to the given amount - N26 defaults to 20
        :param pending: show only pending transactions
        :param categories: Comma separated list of category IDs
        :param text_filter: Query string to search for
        :param last_id: ??
        :return: list of transactions

        [{'accountId': '2a2a2a2a-2a2a-2a2a-2a2a-2a2a2a2a2a2a',         # accountId
          'amount': -6.99,
          'cardId': '3a3a3a3a-3a3a-3a3a-3a3a-3a3a3a3a3a3a',            # cardId,
          'category': 'micro-v2-media-electronics',
          'confirmed': 1635511745847,
          'createdTS': 1635511745851,
          'currencyCode': 'EUR',
          'exchangeRate': 1.0,
          'id': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',                # 'ff606184-63a9-408b-8a58-525c92f5ce76',
          'linkId': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',            # 'ff606184-63a9-408b-8a58-525c92f5ce76',
          'mcc': 4899,
          'mccGroup': 5,
          'merchantCity': '800-022-1476',
          'merchantCountry': 3,
          'merchantCountryCode': 528,
          'merchantName': 'DISNEY PLUS',
          'originalAmount': -6.99,
          'originalCurrency': 'EUR',
          'partnerAccountIsSepa': False,
          'pending': False,
          'recurring': False,
          'smartLinkId': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',       # 'ff606184-63a9-408b-8a58-525c92f5ce76',
          'transactionNature': 'NORMAL',
          'txnCondition': 'ECOMMERCE',
          'type': 'PT',
          'userCertified': 1635511745847,
          'userId': '1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a',            # userId,
          'visibleTS': 1635412707067},
         {'accountId': '2a2a2a2a-2a2a-2a2a-2a2a-2a2a2a2a2a2a',         # accountId
          'amount': -21.44,
          'cardId': '3a3a3a3a-3a3a-3a3a-3a3a-3a3a3a3a3a3a',            # cardId,
          'category': 'micro-v2-healthcare-drugstores',
          'confirmed': 1635473710789,
          'createdTS': 1635473710793,
          'currencyCode': 'EUR',
          'exchangeRate': 1.0,
          'id': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',                # '6c2de6f5-0464-4df5-ac2e-e9fd650e5dd3',
          'linkId': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',            # '6c2de6f5-0464-4df5-ac2e-e9fd650e5dd3',
          'mcc': 5912,
          'mccGroup': 8,
          'merchantCity': 'MADRID',
          'merchantCountry': 9,
          'merchantCountryCode': 724,
          'merchantName': 'FARMACIA LDA VERONICA',
          'originalAmount': -21.44,
          'originalCurrency': 'EUR',
          'partnerAccountIsSepa': False,
          'pending': False,
          'recurring': False,
          'smartLinkId': '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',       # '6c2de6f5-0464-4df5-ac2e-e9fd650e5dd3',
          'transactionNature': 'NORMAL',
          'txnCondition': 'CARD_PRESENT',
          'type': 'PT',
          'userCertified': 1635473710789,
          'userId': '1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a',            # userId,
          'visibleTS': 1635326862885},
        ...
        ]
        """
        params = {'from': 0 if from_time is None else from_time,
                  'to': int(time.time() * 1000) if to_time is None else to_time,
                  'limit': limit,
                  'categories': categories,
                  'textFilter': text_filter,
                  'lastId': last_id}
        if pending:
            params['pending'] = pending
            if limit:
                del params['limit']  # pending does not support limit
        return await self._request('get', f'{BASE_URL_DE}/api/smrt/transactions', params)

    # not working
    async def set_transactions(self, iban: str, bic: str, name: str, reference: str, amount: float, pin: str):
        """
        Creates a bank transfer order
        :param iban: recipient IBAN
        :param bic: recipient BIC
        :param name: recipient name
        :param reference: transaction reference
        :param amount: money amount
        :param pin: user PIN required for the transaction approval
        """
        encrypted_secret, encrypted_pin = await self._encrypt_user_pin(pin)
        pin_headers = {
            'encrypted-secret': encrypted_secret,
            'encrypted-pin': encrypted_pin
        }

        # Prepare headers as a json for a transaction call
        data = {
            "transaction": {
                "amount": amount,
                "partnerBic": bic,
                "partnerIban": iban,
                "partnerName": name,
                "referenceText": reference,
                "type": "DT"
            }
        }

        return await self._request('post', f'{BASE_URL_DE}/api/transactions', params={}, json_=data, headers=pin_headers)

    # not working
    async def get_transactions_so(self) -> dict:
        """
        Get a list of standing orders

        Example data returned:
        """
        return await self._request('get', f'{BASE_URL_DE}/api/transactions/so')

    async def get_statements(self) -> list:
        """
        Retrieves a list of all statements

        Example data returned:
        [{'id': 'statement-2021-11',
          'month': 11,
          'url': '/api/balance-statements/statement-2021-11',
          'visibleTS': 1635724800000,
          'year': 2021},
         ...
         {'id': 'statement-2019-12',
          'month': 12,
          'url': '/api/balance-statements/statement-2019-12',
          'visibleTS': 1575158400000,
          'year': 2019}]
        """
        return await self._request('get', f'{BASE_URL_DE}/api/statements')

    async def get_statement(self, statement_url: str):
        """
        Retrieves a balance statement as pdf binary
        :param statement_url: Download URL of a balance statement document
        """
        return await self._request('get', f'{BASE_URL_DE}{statement_url}')

    async def get_smrt_statistics_categories(self, from_time: int = 0, to_time: int = int(time.time()) * 1000) -> dict:
        """
        Get statistics in a given time frame
        :param from_time: Timestamp - milliseconds since 1970 in CET
        :param to_time: Timestamp - milliseconds since 1970 in CET


        {'expenseItems': [{'expense': 357.46000000000004,
                           'id': 'micro-v2-media-electronics',
                           'income': 9.99,
                           'total': -347.47},
                          {'expense': 139.07999999999998,
                           'id': 'micro-v2-healthcare-drugstores',
                           'income': 0.0,
                           'total': -139.07999999999998},
                          {'expense': 1188.61,
                           'id': 'micro-v2-transport-car',
                           'income': 0.01,
                           'total': -1188.6},
                          {'expense': 1976.8599999999997,
                           'id': 'micro-v2-bars-restaurants',
                           'income': 0.0,
                           'total': -1976.8599999999997},
                          {'expense': 295.0,
                           'id': 'micro-v2-education',
                           'income': 0.0,
                           'total': -295.0},
                          {'expense': 397.49,
                           'id': 'micro-v2-household-utilities',
                           'income': 0.0,
                           'total': -397.49},
                          {'expense': 2043.45,
                           'id': 'micro-v2-shopping',
                           'income': 3.95,
                           'total': -2039.5},
                          {'expense': 3287.229999999999,
                           'id': 'micro-v2-food-groceries',
                           'income': 0.0,
                           'total': -3287.229999999999},
                          {'expense': 654.62,
                           'id': 'micro-v2-leisure-entertainment',
                           'income': 0.0,
                           'total': -654.62},
                          {'expense': 30.2,
                           'id': 'micro-v2-travel-holidays',
                           'income': 0.0,
                           'total': -30.2},
                          {'expense': 140.0,
                           'id': 'micro-v2-atm',
                           'income': 0.0,
                           'total': -140.0},
                          {'expense': 119.0,
                           'id': 'micro-v2-tax-fines',
                           'income': 0.0,
                           'total': -119.0},
                          {'expense': 171.0,
                           'id': 'micro-v2-business',
                           'income': 0.0,
                           'total': -171.0},
                          {'expense': 179.98000000000002,
                           'id': 'micro-v2-miscellaneous',
                           'income': 50.22,
                           'total': -129.76000000000002}],
         'from': 0,
         'incomeItems': [{'expense': 357.46000000000004,
                          'id': 'micro-v2-media-electronics',
                          'income': 9.99,
                          'total': -347.47},
                         {'expense': 1188.61,
                          'id': 'micro-v2-transport-car',
                          'income': 0.01,
                          'total': -1188.6},
                         {'expense': 2043.45,
                          'id': 'micro-v2-shopping',
                          'income': 3.95,
                          'total': -2039.5},
                         {'expense': 0.0,
                          'id': 'micro-v2-income',
                          'income': 23739.960000000003,
                          'total': 23739.960000000003},
                         {'expense': 179.98000000000002,
                          'id': 'micro-v2-miscellaneous',
                          'income': 50.22,
                          'total': -129.76000000000002}],
         'items': [{'expense': 357.46000000000004,
                    'id': 'micro-v2-media-electronics',
                    'income': 9.99,
                    'total': -347.47},
                   {'expense': 139.07999999999998,
                    'id': 'micro-v2-healthcare-drugstores',
                    'income': 0.0,
                    'total': -139.07999999999998},
                   {'expense': 1188.61,
                    'id': 'micro-v2-transport-car',
                    'income': 0.01,
                    'total': -1188.6},
                   {'expense': 1976.8599999999997,
                    'id': 'micro-v2-bars-restaurants',
                    'income': 0.0,
                    'total': -1976.8599999999997},
                   {'expense': 295.0,
                    'id': 'micro-v2-education',
                    'income': 0.0,
                    'total': -295.0},
                   {'expense': 397.49,
                    'id': 'micro-v2-household-utilities',
                    'income': 0.0,
                    'total': -397.49},
                   {'expense': 2043.45,
                    'id': 'micro-v2-shopping',
                    'income': 3.95,
                    'total': -2039.5},
                   {'expense': 3287.229999999999,
                    'id': 'micro-v2-food-groceries',
                    'income': 0.0,
                    'total': -3287.229999999999},
                   {'expense': 654.62,
                    'id': 'micro-v2-leisure-entertainment',
                    'income': 0.0,
                    'total': -654.62},
                   {'expense': 30.2,
                    'id': 'micro-v2-travel-holidays',
                    'income': 0.0,
                    'total': -30.2},
                   {'expense': 140.0,
                    'id': 'micro-v2-atm',
                    'income': 0.0,
                    'total': -140.0},
                   {'expense': 0.0,
                    'id': 'micro-v2-income',
                    'income': 23739.960000000003,
                    'total': 23739.960000000003},
                   {'expense': 119.0,
                    'id': 'micro-v2-tax-fines',
                    'income': 0.0,
                    'total': -119.0},
                   {'expense': 171.0,
                    'id': 'micro-v2-business',
                    'income': 0.0,
                    'total': -171.0},
                   {'expense': 179.98000000000002,
                    'id': 'micro-v2-miscellaneous',
                    'income': 50.22,
                    'total': -129.76000000000002}],
         'to': 1635771932000,
         'total': 12824.150000000003,
         'totalExpense': 10979.98,
         'totalIncome': 23804.130000000005}
        """
        return await self._request('get', f'{BASE_URL_DE}/api/smrt/statistics/categories/{from_time}/{to_time}')

    async def get_hub_savings_accounts(self) -> dict:
        """

        Example data returned:
        {'accounts': [], 'canOpenMore': False, 'pendingAccounts': [], 'totalBalance': 0}
        """
        return await self._request('get', f'{BASE_URL_DE}/api/hub/savings/accounts')

    async def get_v2_cards(self):
        """
        Retrieves a list of all cards

        Example data returned:
        [{'applePayEligible': True,
          'cardActivated': 1579216981791,
          'cardProduct': 'MDS_SPAIN',
          'cardProductType': 'STANDARD',
          'cardSettingsId': None,
          'cardType': 'MASTERCARD',
          'design': 'STANDARD',
          'exceetActualDeliveryDate': None,
          'exceetCardStatus': None,
          'exceetExpectedDeliveryDate': None,
          'exceetExpressCardDelivery': None,
          'exceetExpressCardDeliveryEmailSent': None,
          'exceetExpressCardDeliveryTrackingId': None,
          'expirationDate': 1732924800000,
          'googlePayEligible': True,
          'id': '3a3a3a3a-3a3a-3a3a-3a3a-3a3a3a3a3a3a',       # cardId,
          'maskedPan': '534321******4321',
          'membership': None,
          'mptsCard': True,
          'orderId': None,
          'pan': None,
          'pinDefined': 1579215988450,
          'publicToken': None,
          'status': 'M_ACTIVE',
          'usernameOnCard': 'JOHN D DOE'}]
        """
        return await self._request('get', f'{BASE_URL_DE}/api/v2/cards')

    async def set_cards_block(self, card_id: str) -> dict:
        """
        Blocks a card.
        If the card is already blocked this will have no effect.
        :param card_id: the id of the card to block

        Example data returned:
        {'cardActivated': 1579215988791,
         'cardProductType': 'STANDARD',
         'cardStatus': 'M_DISABLED',                       # <--
         'cardType': 'MASTERCARD',
         'design': 'STANDARD',
         'expirationDate': 1732924800000,
         'id': '3a3a3a3a-3a3a-3a3a-3a3a-3a3a3a3a3a3a',     # cardId
         'isMptsCard': True,
         'maskedPan': '534321******4321',
         'pinDefined': 1579215988450,
         'usernameOnCard': 'JOHN D DOE'}
        """
        return await self._request('post', f'{BASE_URL_DE}/api/cards/{card_id}/block')

    async def set_cards_unblock(self, card_id: str) -> dict:
        """
        Unblocks a card.
        If the card is already unblocked this will have no effect.
        :param card_id: the id of the card to block

        Example data returned:
        {'cardActivated': 1579215988791,
         'cardProductType': 'STANDARD',
         'cardStatus': 'M_ACTIVE',                         # <--
         'cardType': 'MASTERCARD',
         'design': 'STANDARD',
         'expirationDate': 1732924800000,
         'id': '119c03f2-bae8-4508-b610-d5cbd0b3f12f',     # cardId
         'isMptsCard': True,
         'maskedPan': '534321******4321',
         'pinDefined': 1579215988450,
         'usernameOnCard': 'JOHN D DOE'}
        """
        return await self._request('post', f'{BASE_URL_DE}/api/cards/{card_id}/unblock')

    async def get_smrt_contacts(self):
        """
        Retrieves a list of all contacts

        Example data returned:
        []
        """
        return await self._request('get', f'{BASE_URL_DE}/api/smrt/contacts')

    # not working
    async def get_aff_invitations(self) -> list:
        """

        Example data returned:
        """
        return await self._request('get', f'{BASE_URL_DE}/api/aff/invitations')

    # methods below are for internal use
    async def _request(self, method: str = "get", url: str = "/", params: dict = None,
                       json_: dict = None, headers: dict = None) -> list or dict or None:
        """
        Executes a http request based on the given parameters
        :param method: the method to use ("get", "post")
        :param url: the url to use
        :param params: query parameters that will be appended to the url
        :param json_: request body
        :param headers: custom headers
        :return: the response parsed as a json
        """
        auth_token = await self._get_auth_token()
        _headers = {'Authorization': f'Bearer {auth_token}'}
        if headers is not None:
            _headers.update(headers)
        if method not in ['get', 'post']:
            raise ValueError(f'Unsupported method: {method}')

        async with aiohttp.request(method, url, params=params, headers=_headers, json=json_, connector=self.connector) \
                as response:
            response.raise_for_status()
            # some responses do not return data so we just ignore the body in that case
            if len(await response.read()) > 0:
                if "application/json" in response.headers.get("Content-Type", ""):
                    return await response.json()
                else:
                    return await response.read()  # response.content

    async def _get_auth_token(self):
        """
        Returns the access token to use for api authentication.
        1) If a token has been requested before it will be reused if it is still valid.
        2) If the previous token has expired it will be refreshed.
        3) If no token has been requested it will be requested from the server.
        :return: the access token
        """
        new_authentication_token_required = False

        # 1) if we already have a valid authentication token, we return it
        if self._validate_auth_token(self._token_data):
            return self._token_data["access_token"]

        # 2) if we don't have a valid authentication token, we try to refresh the previous one
        #    (if we fail we set new_authentication_token_required to True)
        else:
            try:
                if "refresh_token" in self._token_data:
                    LOGGER.debug(f'Refreshing existing authentication token for username {self.config["USERNAME"]}')
                    # refresh token
                    async with aiohttp.request(method='POST',
                                               url=f'{BASE_URL_GLOBAL}/oauth2/token',
                                               data={'grant_type': "refresh_token",
                                                     'refresh_token': self._token_data["refresh_token"]},
                                               headers=BASIC_AUTH_HEADERS,
                                               connector=self.connector) as response:
                        response.raise_for_status()
                        refreshed_token_data = await response.json()
                else:
                    raise AssertionError("No existing authentication token found")

                # as N26 only informs expiration delta from now, we save the explicit expiration_time in the
                # refreshed_token_data
                refreshed_token_data["expiration_time"] = time.time() + refreshed_token_data["expires_in"]

                # if the refreshed authentication token is still not valid, raise an exception
                if not self._validate_auth_token(refreshed_token_data):
                    raise PermissionError("Unable to refresh authentication token")

                # if the refreshed authentication token is valid, replace the old token
                self._token_data = refreshed_token_data

            except aiohttp.ClientResponseError as e:
                if e.status == 401:
                    new_authentication_token_required = True
                else:  # unexpected ClientResponseError, raise it.
                    raise e

            except AssertionError:
                new_authentication_token_required = True

        # 3) up to this point we couldn't find or refresh a valid authentication token, so we authenticate from scratch
        #    with N26 customer's username & password
        if new_authentication_token_required:

            # 1) Initiate authentication by getting the oauth_token
            LOGGER.debug(f'Requesting new authentication token for username {self.config["USERNAME"]}')
            async with aiohttp.request(method='POST',
                                       url=f'{BASE_URL_GLOBAL}/oauth2/token',
                                       data={'grant_type': 'password',
                                             'username': self.config['USERNAME'],
                                             'password': self.config['PASSWORD']},
                                       headers=BASIC_AUTH_HEADERS,
                                       connector=self.connector) as response:
                if response.status == 403:
                    response_data = await response.json()
                    if response_data.get("error", "") == "mfa_required":
                        mfa_token = response_data["mfaToken"]
                    else:
                        raise ValueError("Unexpected response data")
                else:
                    raise ValueError(f'Unexpected response for initial auth request: {response.text}')

            # 2) request approval of the mfa_token
            LOGGER.debug(f'Requesting MFA approval using mfa_token {mfa_token} for username {self.config["USERNAME"]}')
            async with aiohttp.request(method='POST',
                                       url=f'{BASE_URL_DE}/api/mfa/challenge',
                                       json={'mfaToken': mfa_token,
                                             'challengeType': 'otp' if self.config['MFA_TYPE'] == 'sms' else 'oob'},
                                       headers={**BASIC_AUTH_HEADERS, "User-Agent": USER_AGENT,
                                                "Content-Type": "application/json"},
                                       connector=self.connector) as response:
                response.raise_for_status()

            # 3) Complete authentication by getting N26 customer approval (through the app or through sms)
            #    (if app: we check every ~5 seconds for a total of 60 seconds)
            t = time.time()
            while time.time() - t < 60:

                LOGGER.debug(f'Completing authentication flow for mfa_token {mfa_token}')
                mfa_response_data = {
                    "mfaToken": mfa_token,
                    'grant_type': 'mfa_otp' if self.config['MFA_TYPE'] == 'sms' else 'mfa_oob'
                }

                if self.config['MFA_TYPE'] == 'sms':
                    hint = click.style("Enter the 6 digit SMS OTP code", fg="yellow")
                    # type=str because it can have significant leading zeros
                    mfa_response_data['otp'] = click.prompt(hint, type=str)

                async with aiohttp.request(method='POST',
                                           url=f'{BASE_URL_DE}/oauth2/token',
                                           data=mfa_response_data,
                                           headers=BASIC_AUTH_HEADERS,
                                           connector=self.connector) as response:

                    try:
                        response.raise_for_status()
                    except aiohttp.ClientResponseError:
                        await asyncio.sleep(5)
                        continue

                    new_token_data = await response.json()

                    # as N26 only informs expiration delta from now, we save the explicit expiration_time in the
                    # refreshed_token_data
                    new_token_data["expiration_time"] = time.time() + new_token_data["expires_in"]

                    # if the new authentication token is still not valid, raise an exception
                    if not self._validate_auth_token(new_token_data):
                        raise PermissionError("Unable to request authentication token")

                    # if the new authentication token is valid, save it, and return it
                    self._token_data = new_token_data

                    return self._token_data["access_token"]

    @staticmethod
    def _validate_auth_token(token_data: dict):
        """
        Checks if a token is valid
        :param token_data: the token data to check
        :return: true if valid, false otherwise
        """
        if "expiration_time" not in token_data:
            # there was a problem adding the expiration_time property
            return False
        elif time.time() >= token_data["expiration_time"]:
            # token has expired
            return False

        return "access_token" in token_data and token_data["access_token"]

    # the following methods are used exclusively for set_transaction method (that is not working)

    # used 1
    async def _get_encryption_key(self, public_key: str = None) -> dict:
        """
        Receive public encryption key for the JSON String containing the PIN encryption key
        """
        return await self._request(method="get",
                                   url=f'{BASE_URL_DE}/api/encryption/key',
                                   params={'publicKey': public_key})

    # used 1
    async def _encrypt_user_pin(self, pin: str):
        """
        Encrypts user PIN and prepares it in a format required for a transaction order
        :return: encrypted and base64 encoded PIN as well as an
                 encrypted and base64 encoded JSON containing the PIN encryption key
        """
        # generate AES256 key and IV
        random_password = Random.get_random_bytes(32)
        salt = Random.get_random_bytes(16)
        # noinspection PyTypeChecker
        key = PBKDF2(random_password, salt, 32, count=1000000, hmac_hash_module=SHA512)
        iv = Random.new().read(AES.block_size)
        key64 = base64.b64encode(key).decode('utf-8')
        iv64 = base64.b64encode(iv).decode('utf-8')
        # encode the key and iv as a json string
        aes_secret = {
            'secretKey': key64,
            'iv': iv64
        }
        # json string has to be represented in byte form for encryption
        unencrypted_aes_secret = bytes(json.dumps(aes_secret), 'utf-8')
        # Encrypt the secret JSON with RSA using the provided public key
        public_key = await self._get_encryption_key()
        public_key_non64 = base64.b64decode(public_key['publicKey'])
        public_key_object = RSA.importKey(public_key_non64)
        public_key_cipher = PKCS1_v1_5.new(public_key_object)
        encrypted_secret = public_key_cipher.encrypt(unencrypted_aes_secret)
        encrypted_secret64 = base64.b64encode(encrypted_secret)
        # Encrypt user's pin
        private_key_cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        # the pin has to be padded and transformed into bytes for a correct ecnryption format
        encrypted_pin = private_key_cipher.encrypt(pad(bytes(pin, 'utf-8'), 16))
        encrypted_pin64 = base64.b64encode(encrypted_pin)

        return encrypted_secret64, encrypted_pin64

