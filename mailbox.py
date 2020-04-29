from decimal import Decimal as D

accounts = []
with open('list.txt', errors='ignore') as lh_accounts:
    for i in lh_accounts:
        if i.find('/') != -1 and i.find('.') != -1:
            accounts.append(i.strip())

used_space = 0
all_space = 0
tmp = ''
tmp_used = ''
tmp_all = ''
for i in range(len(accounts)):
    tmp = accounts[i].split('/')

    tmp_used = tmp[0]
    tmp_used = tmp_used.split()

    tmp_all = tmp[1]
    tmp_all = tmp_all.split()

    used_space += D(tmp_used[0])
    all_space += D(tmp_all[0])

print('We have {USED} MB used space on users\' accounts.\nWe have {ALL} MB assigned to users\' accounts.\nWe have {AVA} MB free space on users\s accoutns.\n'.format(USED=used_space, ALL=all_space, AVA=all_space-used_space))