# aioN26
Unofficial Asynchronous N26-bank API implementation

based on https://app.swaggerhub.com/apis/Rots/N26/0.2#/transactions/get_smrt_transactions

I will document this better in the future, but here is a working example:
::

    import asyncio
    from aioN26.api import Api

    from pprint import pprint
    import logging

    import os
    from dotenv import load_dotenv    # pip install python-dotenv

    # We load local environment variables from file MYSECRET.env
    # The file format is as follows:

    # ------------MYSECRET.env-------------
    # USERNAME=john.doe@mail.com
    # PASSWORD=mysecretpassword
    # DEVICE_TOKEN=yourgeneratedtoken
    # -------------------------------------

    # to generate the DEVICE_TOKEN, run this in a python3 console:
    # >>> import uuid ; print(uuid.uuid4())
    # and paste the result in the file

    load_dotenv('MYSECRET.env')    # directory/file containing the environment variables

    logging.basicConfig(level=logging.DEBUG)


    async def main():
        async with Api(username=os.getenv('USERNAME'), password=os.getenv('PASSWORD'),
                       device_token=os.getenv('DEVICE_TOKEN')) as api:

            print(api.get_device_token())

            print('\nget_me = \\')
            pprint(await api.get_me())

            print('\nget_me_statuses = \\')
            pprint(await api.get_me_statuses())

            print('\nget_addresses = \\')
            pprint(await api.get_addresses())

            print('\nget_barzahlen_check = \\')
            pprint(await api.get_barzahlen_check())

            print('\nget_spaces = \\')
            pprint(await api.get_spaces())

            print('\nget_accounts = \\')
            pprint(await api.get_accounts())

            print('\nget_settings_account_limits = \\')
            pprint(await api.get_settings_account_limits())

            print('\nset_settings_account_limits = \\')
            pprint(await api.set_settings_account_limits(500, 3000))

            print('\nget_smrt_categories = \\')
            pprint(await api.get_smrt_categories())

            print('\nget_smrt_transactions = \\')
            transactions = await api.get_smrt_transactions(from_time=1636030755256, to_time=1636030755256)
            pprint(transactions)
            print('TOTAL', len(transactions))

    asyncio.run(main())




