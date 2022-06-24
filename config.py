from symbols import symbol

# get option chain for specific expiration
opt = symbol.option_chain('2022-06-24')
# data available via: opt.calls, opt.puts