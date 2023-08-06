import os
import time

import pytest  # pip install pytest-asyncio
from api import Api  # relative to project root
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv('MYSECRET.env')  # relative to project root
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
device_token = os.getenv('DEVICE_TOKEN')

api = Api(username=username, password=password, device_token=device_token)


def test_get_device_token():
    res = api.get_device_token()
    assert type(res) is str
    assert len(res) == 36 and res[8] == res[13] == res[18] == res[23] == '-'
    assert res == device_token


@pytest.mark.asyncio
async def test_get_me():
    async with api:
        res = await api.get_me()
        assert type(res) is dict
        assert list(res.keys()) == ['id', 'email', 'firstName', 'lastName', 'kycFirstName', 'kycLastName', 'title',
                                    'gender', 'birthDate', 'signupCompleted', 'nationality', 'mobilePhoneNumber',
                                    'shadowUserId', 'transferWiseTermsAccepted', 'idNowToken']


@pytest.mark.asyncio
async def test_get_me_statuses():
    async with api:
        res = await api.get_me_statuses()
        assert type(res) is dict
        assert list(res.keys()) == ['id', 'created', 'updated', 'singleStepSignup', 'emailValidationInitiated',
                                    'emailValidationCompleted', 'productSelectionCompleted', 'phonePairingInitiated',
                                    'phonePairingCompleted', 'userStatusCol', 'kycInitiated', 'kycCompleted',
                                    'kycPersonalCompleted', 'kycPostIdentInitiated', 'kycPostIdentCompleted',
                                    'kycWebIDInitiated', 'kycWebIDCompleted', 'kycDetails', 'cardActivationCompleted',
                                    'cardIssued', 'pinDefinitionCompleted', 'accountClosed', 'coreDataUpdated',
                                    'unpairingProcessStatus', 'isDeceased', 'firstIncomingTransaction', 'flexAccount',
                                    'flexAccountConfirmed', 'signupStep', 'unpairTokenCreation', 'pairingState',
                                    'showScreen', 'signingRequired', 'signingCompleted']


@pytest.mark.asyncio
async def test_get_addresses():
    async with api:
        res = await api.get_addresses()
        assert type(res) is dict
        assert list(res.keys()) == ['paging', 'data']
        assert type(res['paging']) is dict
        assert list(res['paging'].keys()) == ['previous', 'next', 'totalResults']
        assert type(res['data']) is list
        for address in res['data']:
            assert type(address) is dict
            assert list(address.keys()) == ['id', 'userId', 'type', 'country', 'countryName', 'city', 'cityName',
                                            'zipCode', 'houseNumberBlock', 'street', 'streetName', 'addressLine1',
                                            'state', 'created', 'updated']


@pytest.mark.asyncio
async def test_get_barzahlen_check():
    async with api:
        res = await api.get_barzahlen_check()
        print(res, type(res), res.keys(), type(res.keys()))
        assert type(res) is dict
        assert list(res.keys()) == ['transactionId', 'depositAllowance', 'withdrawAllowance', 'remainingAmountMonth',
                                    'feeRate', 'cash26WithdrawalsCount', 'cash26WithdrawalsSum', 'atmWithdrawalsCount',
                                    'atmWithdrawalsSum', 'monthlyDepositFeeThreshold', 'success']


@pytest.mark.asyncio
async def test_get_spaces():
    async with api:
        res = await api.get_spaces()
        print(res, type(res), res.keys(), type(res.keys()))
        assert type(res) is dict
        assert list(res.keys()) == ['totalBalance', 'visibleBalance', 'spaces', 'userFeatures']
        for space in res['spaces']:
            print(type(space))
            assert type(space) is dict
            assert list(space.keys()) == ['id', 'accountId', 'name', 'imageUrl', 'backgroundImageUrl', 'balance',
                                          'isPrimary', 'isHiddenFromBalance', 'isCardAttached', 'isLocked']
        assert type(res['totalBalance']) is float
        assert type(res['userFeatures']) is dict
        assert type(res['visibleBalance']) is float


@pytest.mark.asyncio
async def test_get_accounts():
    async with api:
        res = await api.get_accounts()
        assert type(res) is dict
        assert list(res.keys()) == ['id', 'currency', 'availableBalance', 'usableBalance', 'bankBalance',
                                    'legalEntity', 'externalId', 'bic', 'iban']


@pytest.mark.asyncio
async def test_get_settings_account_limits():
    async with api:
        res = await api.get_settings_account_limits()
        assert type(res) is list
        for item in res:
            assert type(item) is dict
            assert list(item.keys()) == ['limit', 'amount', 'countryList']


# set_settings_account_limits


@pytest.mark.asyncio
async def test_get_smrt_categories():
    async with api:
        res = await api.get_smrt_categories()
        assert type(res) is list
        for item in res:
            assert type(item) is dict
            assert list(item.keys()) == ['id', 'base64Image', 'name', 'backgroundUrl']


@pytest.mark.asyncio
async def test_get_smrt_transactions():
    # each item can have flexible fields. Currently, after 250+ transactions, I've found 7 combinations only
    key_options = [
        ['id', 'userId', 'type', 'amount', 'currencyCode', 'originalAmount', 'originalCurrency', 'exchangeRate',
         'merchantCity', 'visibleTS', 'mcc', 'mccGroup', 'merchantName', 'recurring', 'partnerAccountIsSepa',
         'accountId', 'category', 'cardId', 'userCertified', 'pending', 'transactionNature', 'createdTS',
         'merchantCountry', 'smartLinkId', 'linkId', 'confirmed'],

        ['id', 'userId', 'type', 'amount', 'currencyCode', 'originalAmount', 'originalCurrency', 'exchangeRate',
         'merchantCity', 'visibleTS', 'mcc', 'mccGroup', 'merchantName', 'recurring', 'partnerAccountIsSepa',
         'accountId', 'category', 'cardId', 'userCertified', 'pending', 'transactionNature', 'createdTS',
         'merchantCountry', 'txnCondition', 'smartLinkId', 'linkId', 'confirmed'],

        ['id', 'userId', 'type', 'amount', 'currencyCode', 'originalAmount', 'originalCurrency', 'exchangeRate',
         'merchantCity', 'visibleTS', 'mcc', 'mccGroup', 'merchantName', 'recurring', 'partnerAccountIsSepa',
         'accountId', 'category', 'cardId', 'userCertified', 'pending', 'transactionNature', 'createdTS',
         'merchantCountry', 'merchantCountryCode', 'txnCondition', 'smartLinkId', 'linkId', 'confirmed'],

        ['id', 'userId', 'type', 'amount', 'currencyCode', 'originalAmount', 'originalCurrency', 'exchangeRate',
         'ecbMarkupRate', 'merchantCity', 'visibleTS', 'mcc', 'mccGroup', 'merchantName', 'recurring',
         'partnerAccountIsSepa', 'accountId', 'category', 'cardId', 'userCertified', 'pending',
         'transactionNature', 'createdTS', 'merchantCountry', 'merchantCountryCode', 'txnCondition',
         'smartLinkId', 'linkId', 'confirmed'],

        ['id', 'userId', 'type', 'amount', 'currencyCode', 'visibleTS', 'partnerName', 'accountId',
         'partnerIban', 'category', 'referenceText', 'userCertified', 'pending', 'transactionNature',
         'createdTS', 'smartLinkId', 'linkId', 'confirmed'],

        ['id', 'userId', 'type', 'amount', 'currencyCode', 'visibleTS', 'partnerBic', 'partnerName',
         'accountId', 'partnerIban', 'category', 'referenceText', 'userCertified', 'pending',
         'transactionNature', 'createdTS', 'smartLinkId', 'linkId', 'confirmed'],

        ['id', 'userId', 'type', 'amount', 'currencyCode', 'merchantCity', 'visibleTS', 'mcc', 'mccGroup',
         'merchantName', 'recurring', 'partnerAccountIsSepa', 'accountId', 'category', 'cardId',
         'userCertified', 'pending', 'transactionNature', 'createdTS', 'merchantCountry', 'merchantCountryCode',
         'smartLinkId', 'linkId', 'confirmed'],
    ]
    async with api:
        # test 1: without parameters (default <= 500 transactions)
        res = await api.get_smrt_transactions()
        assert type(res) is list
        for item in res:
            assert type(item) is dict
            # print(item.keys())
            assert list(item.keys()) in key_options
        # test 2: with from and to time ranges
        from_time = int(time.time() * 1000) - 86400000 * 365
        to_time = int(time.time() * 1000) - 86400000 * 90
        res = await api.get_smrt_transactions(from_time=from_time, to_time=to_time)
        assert type(res) is list
        for item in res:
            assert type(item) is dict
            # print(item.keys())
            assert list(item.keys()) in key_options
            assert from_time <= item['visibleTS'] <= to_time


# set_transactions (not working yet)

# get_transactions_so (not working yet)


@pytest.mark.asyncio
async def test_get_statements():
    async with api:
        res = await api.get_statements()
        assert type(res) is list
        for item in res:
            assert type(item) is dict
            assert list(item.keys()) == ['id', 'url', 'visibleTS', 'month', 'year']


# get_statement


@pytest.mark.asyncio
async def test_get_smrt_statistics_categories():
    async with api:
        res = await api.get_smrt_statistics_categories()
        # print(res, type(res), res.keys(), type(res.keys()))
        assert type(res) is dict
        assert list(res.keys()) == ['from', 'to', 'total', 'totalIncome', 'totalExpense', 'items', 'incomeItems',
                                    'expenseItems']
        assert type(res['expenseItems']) == list
        for expItem in res['expenseItems']:
            assert type(expItem) == dict
            assert list(expItem.keys()) == ['id', 'income', 'expense', 'total']
        assert type(res['from']) == int
        assert type(res['incomeItems']) == list
        for incItem in res['incomeItems']:
            assert type(incItem) == dict
            assert list(incItem.keys()) == ['id', 'income', 'expense', 'total']
        assert type(res['items']) == list
        for item in res['items']:
            assert type(item) == dict
            assert list(item.keys()) == ['id', 'income', 'expense', 'total']
        assert type(res['to']) == int
        assert type(res['total']) == float
        assert type(res['totalExpense']) == float
        assert type(res['totalIncome']) == float


@pytest.mark.asyncio
async def test_get_hub_savings_accounts():
    async with api:
        res = await api.get_hub_savings_accounts()
        # print(res, type(res), res.keys(), type(res.keys()))
        assert type(res) is dict
        assert list(res.keys()) == ['totalBalance', 'canOpenMore', 'accounts', 'pendingAccounts']


@pytest.mark.asyncio
async def test_get_v2_cards():
    async with api:
        res = await api.get_v2_cards()
        assert type(res) is list
        for item in res:
            assert type(item) is dict
            assert list(item.keys()) == ['id', 'maskedPan', 'publicToken', 'pinDefined', 'cardActivated',
                                         'usernameOnCard', 'status', 'design', 'cardProductType', 'applePayEligible',
                                         'googlePayEligible', 'pan', 'expirationDate', 'cardType', 'cardProduct',
                                         'exceetExpressCardDelivery', 'membership', 'exceetActualDeliveryDate',
                                         'exceetExpressCardDeliveryEmailSent', 'exceetCardStatus',
                                         'exceetExpectedDeliveryDate', 'exceetExpressCardDeliveryTrackingId',
                                         'cardSettingsId', 'mptsCard', 'orderId']


# set_cards_block

# set_cards_unblock


@pytest.mark.asyncio
async def test_get_smrt_contacts():
    async with api:
        res = await api.get_smrt_contacts()
        assert type(res) is list
        for item in res:
            assert type(item) is dict
            assert list(item.keys()) == []


# get_aff_invitations


# @pytest.mark.asyncio
# async def test_xxxxx():
#     async with api:
#         res = await api.xxxxx()
#         # print(res, type(res), res.keys(), type(res.keys()))
#         assert type(res) is dict
#         assert list(res.keys()) == []
