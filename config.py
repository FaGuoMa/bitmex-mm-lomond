# end point
try:
    from config_prod import dict_prod
except:
    dict_prod = dict()
    print("production details not in git, create locally and add to your .gitignore, or just continue run test")

connect = dict(test = dict(endpoint ='wss://testnet.bitmex.com/realtime',
                           apiKey = 'YOUR_API_KEY',
                           apiSecret ='YOUR_SECRET'),

               prod= dict_prod)

