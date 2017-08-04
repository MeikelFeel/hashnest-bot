#!/usr/bin/python3
import json, os, sys, redis, requests
from hashnest import hashnest
from datetime import datetime, timedelta, date
from statistics import mean, harmonic_mean, median_high, median, median_low

def getCryptoPrice(currency_pair):
    URL = 'https://www.bitstamp.net/api/v2/ticker/' + currency_pair
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['last'])
        return priceFloat
    except requests.ConnectionError:
        print('Error querying Bitstamp API')

db=redis.from_url(os.environ['REDIS_URL'])

#hashnest_api = hashnest('username', 'access_key', 'secret_key')
hashnest_api = hashnest(os.environ['username'], os.environ['access_key'], os.environ['secret_key'])

l3 = json.loads(hashnest_api.get_currency_orders(22))
s9 = json.loads(hashnest_api.get_currency_orders(21))
s7 = json.loads(hashnest_api.get_currency_orders(20))

l3_ask = l3['sale']
l3_bid = l3['purchase']
s9_ask = s9['sale']
s9_bid = s9['purchase']
s7_ask = s7['sale']
s7_bid = s7['purchase']

l3_trades = json.loads(hashnest_api.get_currency_trades(22))
s9_trades = json.loads(hashnest_api.get_currency_trades(21))
s7_trades = json.loads(hashnest_api.get_currency_trades(20))

l3tradeslist = []
s9tradeslist = []
s7tradeslist = []

for i in l3_trades:
    l3tradeslist.append(float(i['ppc']))
for i in s9_trades:
    s9tradeslist.append(float(i['ppc']))
for i in s7_trades:
    s7tradeslist.append(float(i['ppc']))

l3asklist = []
l3bidlist = []
s9asklist = []
s9bidlist = []
s7asklist = []
s7bidlist = []

for i in l3_ask:
    l3asklist.append(float(i['ppc']))
for i in l3_bid:
    l3bidlist.append(float(i['ppc']))
for i in s9_ask:
    s9asklist.append(float(i['ppc']))
for i in s9_bid:
    s9bidlist.append(float(i['ppc']))
for i in s7_ask:
    s7asklist.append(float(i['ppc']))
for i in s7_bid:
    s7bidlist.append(float(i['ppc']))

l3asklist.sort()
l3bidlist.sort(reverse=True)
s9asklist.sort()
s9bidlist.sort(reverse=True)
s7asklist.sort()
s7bidlist.sort(reverse=True)

l3_tradesmeanppc=[]
l3_ordersmeanppc=[]
s9_tradesmeanppc=[]
s9_ordersmeanppc=[]
s7_tradesmeanppc=[]
s7_ordersmeanppc=[]

for i in range(1, 21):
    l3_tradesmeanppc.append([mean(l3tradeslist[0:i]), harmonic_mean(l3tradeslist[0:i]), median_high(l3tradeslist[0:i]), median_low(l3tradeslist[0:i])])
    s9_tradesmeanppc.append([mean(s9tradeslist[0:i]), harmonic_mean(s9tradeslist[0:i]), median_high(s9tradeslist[0:i]), median_low(s9tradeslist[0:i])])
    s7_tradesmeanppc.append([mean(s7tradeslist[0:i]), harmonic_mean(s7tradeslist[0:i]), median_high(s7tradeslist[0:i]), median_low(s7tradeslist[0:i])])
    l3_ordersmeanppc.append([mean(l3asklist[0:i] + l3bidlist[0:i]), harmonic_mean(l3asklist[0:i] + l3bidlist[0:i]), median_high(l3asklist[0:i] + l3bidlist[0:i]), median_low(l3asklist[0:i] + l3bidlist[0:i])])
    s9_ordersmeanppc.append([mean(s9asklist[0:i] + s9bidlist[0:i]), harmonic_mean(s9asklist[0:i] + s9bidlist[0:i]), median_high(s9asklist[0:i] + s9bidlist[0:i]), median_low(s9asklist[0:i] + s9bidlist[0:i])])
    s7_ordersmeanppc.append([mean(s7asklist[0:i] + s7bidlist[0:i]), harmonic_mean(s7asklist[0:i] + s7bidlist[0:i]), median_high(s7asklist[0:i] + s7bidlist[0:i]), median_low(s7asklist[0:i] + s7bidlist[0:i])])

#l3_ppc = l3_ordersmeanppc[5-1] + l3_ordersmeanppc[10-1] + l3_ordersmeanppc[15-1] + l3_ordersmeanppc[20-1] + l3_tradesmeanppc[5-1] + l3_tradesmeanppc[10-1] + l3_tradesmeanppc[15-1] + l3_tradesmeanppc[20-1]
l3_ppc=[]
for order in l3_ordersmeanppc:
    l3_ppc=l3_ppc+order
for trade in l3_tradesmeanppc:
    l3_ppc=l3_ppc+trade
l3_ppc_max=max(l3_ppc+l3tradeslist)
l3_ppc_min=min(l3_ppc+l3tradeslist)
l3_ppc_mean=mean([l3_ppc_max, l3_ppc_min])
l3_ppc_lowmean=mean([l3_ppc_mean, l3_ppc_min])
l3_ppc_highmean=mean([l3_ppc_mean, l3_ppc_max])

#s9_ppc = s9_ordersmeanppc[5-1] + s9_ordersmeanppc[10-1] + s9_ordersmeanppc[15-1] + s9_ordersmeanppc[20-1] + s9_tradesmeanppc[5-1] + s9_tradesmeanppc[10-1] + s9_tradesmeanppc[15-1] + s9_tradesmeanppc[20-1]
s9_ppc=[]
for order in s9_ordersmeanppc:
    s9_ppc=s9_ppc+order
for trade in s9_tradesmeanppc:
    s9_ppc=s9_ppc+trade
s9_ppc_max=max(s9_ppc+s9tradeslist)
s9_ppc_min=min(s9_ppc+s9tradeslist)
s9_ppc_mean=mean([s9_ppc_max, s9_ppc_min])
s9_ppc_lowmean=mean([s9_ppc_mean, s9_ppc_min])
s9_ppc_highmean=mean([s9_ppc_mean, s9_ppc_max])

#s7_ppc = s7_ordersmeanppc[5-1] + s7_ordersmeanppc[10-1] + s7_ordersmeanppc[15-1] + s7_ordersmeanppc[20-1] + s7_tradesmeanppc[5-1] + s7_tradesmeanppc[10-1] + s7_tradesmeanppc[15-1] + s7_tradesmeanppc[20-1]
s7_ppc=[]
for order in s7_ordersmeanppc:
    s7_ppc=s7_ppc+order
for trade in s7_tradesmeanppc:
    s7_ppc=s7_ppc+trade
s7_ppc_max=max(s7_ppc+s7tradeslist)
s7_ppc_min=min(s7_ppc+s7tradeslist)
s7_ppc_mean=mean([s7_ppc_max, s7_ppc_min])
s7_ppc_lowmean=mean([s7_ppc_mean, s7_ppc_min])
s7_ppc_highmean=mean([s7_ppc_mean, s7_ppc_max])

wallet = json.loads(hashnest_api.get_account_balance())
btc_balance = float(wallet[0]['amount'])
btc_blocked = float(wallet[0]['blocked'])
ltc_balance = float(wallet[1]['amount'])
ltc_blocked = float(wallet[1]['blocked'])

hashrate = json.loads(hashnest_api.get_account_hashrate())
s7hashrate = int(float(hashrate[6]['total']))
s9hashrate = int(float(hashrate[7]['total']))
l3hashrate = int(float(hashrate[8]['total']))
s7hashrate_blocked = int(float(hashrate[6]['blocked']))
s9hashrate_blocked = int(float(hashrate[7]['blocked']))
l3hashrate_blocked = int(float(hashrate[8]['blocked']))
db.set('s7hashrate', s7hashrate)
db.set('s9hashrate', s9hashrate)
db.set('l3hashrate', l3hashrate)

btcusd=getCryptoPrice('btcusd')
ltcusd=getCryptoPrice('ltcusd')

orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f

print('\n')
print('================================')
print('\n')
print('  Hashnest bot by astrolince')
print('\n')
utctimenow = datetime.utcnow()
print('  %s UTC' % (str(utctimenow)))
print('  %s UTC-3' % (str(utctimenow - timedelta(hours=3))))
print('\n')
print('================================')
print('\n')

print('BTC balance: %10.8f' % (btc_balance))
if btc_blocked>0:
    print('  Locked: %10.8f' % (btc_blocked))
print('LTC balance: %10.8f' % (ltc_balance))
if ltc_blocked>0:
    print('  Locked: %10.8f' % (ltc_blocked))

print('\n')

print('%s hashrate: %i' % (hashrate[6]['currency']['code'], s7hashrate))
if s7hashrate_blocked>0:
    print('  Locked: %i' % (s7hashrate_blocked))
print('%s hashrate: %i' % (hashrate[7]['currency']['code'], s9hashrate))
if s9hashrate_blocked>0:
    print('  Locked: %i' % (s9hashrate_blocked))
print('%s hashrate: %i' % (hashrate[8]['currency']['code'], l3hashrate))
if l3hashrate_blocked>0:
    print('  Locked: %i' % (l3hashrate_blocked))

print('\n')

l3tradesmedian = median(l3tradeslist)
db.set('l3tradesmedian', '%10.8f' % (l3tradesmedian))
s9tradesmedian = median(s9tradeslist)
db.set('s9tradesmedian', '%10.8f' % (s9tradesmedian))
s7tradesmedian = median(s7tradeslist)
db.set('s7tradesmedian', '%10.8f' % (s7tradesmedian))

accbtcvalue=btc_balance+btc_blocked+s9hashrate*s9tradesmedian+s7hashrate*s7tradesmedian
accltcvalue=ltc_balance+ltc_blocked+l3hashrate*l3tradesmedian
accusdvalue=btcusd * accbtcvalue + ltcusd * accltcvalue
today = date.today()
meantoday = mean([float(db.get(today) or accusdvalue), accusdvalue])
db.set(today, meantoday)
yesterday = accusdvalue / (float(db.get(today - timedelta(days=1)) or meantoday)) * 100 - 100
week = accusdvalue / (float(db.get(today - timedelta(days=7)) or accusdvalue)) * 100 - 100
month = accusdvalue / (float(db.get(today - timedelta(days=30)) or accusdvalue)) * 100 - 100
year = accusdvalue / (float(db.get(today - timedelta(days=365)) or accusdvalue)) * 100 - 100
print('Account value: USD %4.2f [%4.2f%% 24hs] [%4.2f%% 7d] [%4.2f%% 30d] [%4.2f%% 365d]' % (accusdvalue, yesterday, week, month, year))

print('\n')

print('L3 trade [%10.8f] [USD %4.4f]' % (l3tradesmedian, l3tradesmedian * ltcusd))
print('Ask:  %10.8f' % (min(l3asklist)))
print('Max:  %10.8f' % (l3_ppc_max))
print('High: %10.8f' % (l3_ppc_highmean))
print('Mean: %10.8f' % (l3_ppc_mean))
print('Low:  %10.8f' % (l3_ppc_lowmean))
print('Min:  %10.8f' % (l3_ppc_min))
print('Bid:  %10.8f' % (max(l3bidlist)))

autobuy=os.environ['l3autobuy']
if autobuy:
    if ltc_blocked>0:
        print('\n')
        active_orders = json.loads(hashnest_api.get_orders(22))
        for order in active_orders:
            delorder=json.loads(hashnest_api.delete_order(order['id']))
            if str(delorder['success'])=='True':
                print('Deleted order: %s of %i MHS, %10.8f ppc, %10.8f total, created at %s' % (order['category'], float(order['amount']), float(order['ppc']), float(order['amount']) * float(order['ppc']), order['created_at']))
    hashrate_amount=int((ltc_balance+ltc_blocked)/l3_ppc_min)
    if hashrate_amount >= 1:
        print('\n')
        created_order = json.loads(hashnest_api.create_order(22, hashrate_amount, l3_ppc_min, 'purchase'))
        print('New order: %s of %i MHS, %10.8f ppc, %10.8f total, created at %s' % (created_order['category'], float(created_order['amount']), float(created_order['ppc']), float(created_order['amount']) * float(created_order['ppc']), created_order['created_at']))

print('\n')

print('S9 trade [%10.8f] [USD %4.4f]' % (s9tradesmedian, s9tradesmedian * btcusd))
print('Ask:  %10.8f' % (min(s9asklist)))
print('Max:  %10.8f' % (s9_ppc_max))
print('High: %10.8f' % (s9_ppc_highmean))
print('Mean: %10.8f' % (s9_ppc_mean))
print('Low:  %10.8f' % (s9_ppc_lowmean))
print('Min:  %10.8f' % (s9_ppc_min))
print('Bid:  %10.8f' % (max(s9bidlist)))

autobuy=os.environ['s9autobuy']
if autobuy:
    if btc_blocked>0:
        print('\n')
        active_orders = json.loads(hashnest_api.get_orders(21))
        for order in active_orders:
            delorder=json.loads(hashnest_api.delete_order(order['id']))
            if str(delorder['success'])=='True':
                print('Deleted order: %s of %i MHS, %10.8f ppc, %10.8f total, created at %s' % (order['category'], float(order['amount']), float(order['ppc']), float(order['amount']) * float(order['ppc']), order['created_at']))
    hashrate_amount=int((btc_balance+btc_blocked)/s9_ppc_min)
    if hashrate_amount >= 1:
        print('\n')
        created_order = json.loads(hashnest_api.create_order(21, hashrate_amount, s9_ppc_min, 'purchase'))
        print('New order: %s of %i MHS, %10.8f ppc, %10.8f total, created at %s' % (created_order['category'], float(created_order['amount']), float(created_order['ppc']), float(created_order['amount']) * float(created_order['ppc']), created_order['created_at']))

print('\n')

print('S7 trade [%10.8f] [USD %4.4f]' % (s7tradesmedian, s7tradesmedian * btcusd))
print('Ask:  %10.8f' % (min(s7asklist)))
print('Max:  %10.8f' % (s7_ppc_max))
print('High: %10.8f' % (s7_ppc_highmean))
print('Mean: %10.8f' % (s7_ppc_mean))
print('Low:  %10.8f' % (s7_ppc_lowmean))
print('Min:  %10.8f' % (s7_ppc_min))
print('Bid:  %10.8f' % (max(s7bidlist)))

autobuy=os.environ['s7autobuy']
if autobuy:
    if btc_blocked>0:
        print('\n')
        active_orders = json.loads(hashnest_api.get_orders(20))
        for order in active_orders:
            delorder=json.loads(hashnest_api.delete_order(order['id']))
            if str(delorder['success'])=='True':
                print('Deleted order: %s of %i MHS, %10.8f ppc, %10.8f total, created at %s' % (order['category'], float(order['amount']), float(order['ppc']), float(order['amount']) * float(order['ppc']), order['created_at']))
    hashrate_amount=int((btc_balance+btc_blocked)/s7_ppc_min)
    if hashrate_amount >= 1:
        print('\n')
        created_order = json.loads(hashnest_api.create_order(20, hashrate_amount, s7_ppc_min, 'purchase'))
        print('New order: %s of %i MHS, %10.8f ppc, %10.8f total, created at %s' % (created_order['category'], float(created_order['amount']), float(created_order['ppc']), float(created_order['amount']) * float(created_order['ppc']), created_order['created_at']))

print('\n')
print('================================')
print('\n')

sys.stdout = orig_stdout
f.close()

readlog = open('out.txt', 'r')
savedlog = readlog.read()
readlog.close()

print(savedlog)
db.set('savedlog', savedlog)
