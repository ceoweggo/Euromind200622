import yfinance as yf
import json, os

# Opening the quotes file
with open('quotes.json') as file:
    data = json.load(file)

    symbols_list = []
    for symbol_name in data:
        # Add every symbol into variable list
        symbols_list.append(symbol_name['symbol'])

    for symbol_process in symbols_list:
        # Add yfinance information to the symbol's variable
        symbol = yf.Ticker(symbol_process)

        # Get the public information about the business
        if os.path.isfile(symbol_process+'.json'):
            pass
        else:
            # Get information about symbol
            print('Downloading the general information about '+symbol_process+'...')
            info = symbol.info
            print('General information downloaded!')
            print('Downloading the news about '+symbol_process+'...')
            news = symbol.news
            print('News downloaded!')
            print('Downloading the balance sheet about '+symbol_process+'...')
            balance = symbol.balance_sheet
            print('Balance sheet downloaded!')

            # Writing the information about symbol into the json files
            print('Writing the information in json '+symbol_process+' files...')

            # General information route (values folder)
            info_route = 'values\{}.json'.format(symbol_process)
            with open(info_route, 'w') as file:
                json.dump(info.to_json(), file, indent=4)

            # News information route (news folder)
            news_route = 'news\{}.json'.format(symbol_process)
            with open(news_route, 'w') as file:
                json.dump(news.to_json(), file, indent=4)

            # Balance sheet information route (accounting folder)
            balance_route = 'accounting\{}.json'.format(symbol_process)
            with open(balance_route, 'w') as file:
                json.dump(balance.to_json(), file, indent=4)
            
    print('All was good!')