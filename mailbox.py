from decimal import Decimal as D

accounts = []
accounts_dict = {}
flag = False

with open('list.txt', errors='ignore') as lh_accounts:
    username = ''
    
    for i in lh_accounts:
        index_at = i.find('@')
        if index_at != -1:
            username = i[:index_at]

        if i.find('/') != -1 and i.find('.') != -1:
            accounts_dict[username] = i.strip()

used_space = 0
all_space = 0
tmp = ''
tmp_used = ''
tmp_all = ''

for username, space in accounts_dict.items():
    #print(space)
    tmp = space.split('/')

    tmp_used = tmp[0]
    tmp_used = tmp_used.split()

    tmp_all = tmp[1]
    tmp_all = tmp_all.split()

    used_space += D(tmp_used[0])
    all_space += D(tmp_all[0])

    accounts_dict[username] = [float(tmp_used[0]), float(tmp_all[0]), float(D(tmp_all[0])-D(tmp_used[0]))]

accounts_free_dict = {}
for username, space in accounts_dict.items():
    #print('Email {EMAIL}@mforce.pl\nfree: {FREE}\nused: {USED}\ntotal: {ALL}\n'.format(EMAIL=username, FREE=space[2], USED=space[0], ALL=space[1]))
    accounts_free_dict[space[2]] = [username, space[0], space[1]]

for i in sorted (accounts_free_dict, reverse=True):
    print('Email {EMAIL}@mforce.pl\nfree: {FREE}\nused: {USED}\ntotal: {ALL}\n'.format(EMAIL=accounts_free_dict[i][0], FREE=i, USED=accounts_free_dict[i][1], ALL=accounts_free_dict[i][2]))

print('We have {USED} MB used space on users\' accounts.\nWe have {ALL} MB assigned to users\' accounts.\nWe have {AVA} MB free space on users\' accounts.\n'.format(USED=used_space, ALL=all_space, AVA=all_space-used_space))