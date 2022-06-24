from genericpath import exists
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


        ###############################
        ### GENERAL INFORMATION SECTION
        ###############################

        path_values = "values\{}".format(symbol_process+".json")
        if os.path.isfile(path_values):
            pass
        else:
            print('Downloading the general information about '+symbol_process+'...')
            if symbol.info:
                info = symbol.info
                print('General information downloaded!')
            else:
                print('Not exist general information about {} symbol'.format(symbol_process))

            print('Writing the information in json '+symbol_process+' file...')

            info_route = 'values\{}.json'.format(symbol_process)
            with open(info_route, 'w') as file:
                json.dump(info, file, indent=4)
            

        ################
        ### NEWS SECTION
        ################
        
        path_news = "news\{}".format(symbol_process+".json")
        if os.path.isfile(path_news):
            pass
        else:
            print('Downloading the news about '+symbol_process+'...')
            if symbol.news:
                news = symbol.news
                print('News downloaded!')
            else:
                print('Not exist news information about {} symbol'.format(symbol_process))

            print('Writing the information in json '+symbol_process+' file...')

            news_route = 'news\{}.json'.format(symbol_process)
            with open(news_route, 'w') as file:
                json.dump(news, file, indent=4)


        #######################
        ### ACCOUNTING SECTION
        #######################

        path_accounting = "accounting\{}".format(symbol_process+".json")
        if os.path.isfile(path_accounting):
            pass
        else:
            print('Downloading the balance sheet about '+symbol_process+'...')
            if symbol.balance_sheet is not None:
                balance = symbol.balance_sheet.to_json()
                print('Balance sheet downloaded!')
            else:
                print('Not exist accounting information about {} symbol'.format(symbol_process))

            print('Writing the information in json '+symbol_process+' file...')

            balance_route = 'accounting\{}.json'.format(symbol_process)
            with open(balance_route, 'w') as file:
                json.dump(balance, file, indent=4)
            
    print('All was good!')