from decimal import Decimal as D
import os
import tkinter as tk
from tkinter import filedialog
import re
import time

os.system('cls')
accounts = []
accounts_dict = {}

print('Choose a prepared .txt file with accounts list.\n')

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

with open(file_path, errors='ignore') as lh_accounts:
    username = ''

    if lh_accounts.read(1) != '<':
        lh_accounts.seek(0)
        for i in lh_accounts:
            index_at = i.find('@')
            if index_at != -1:
                username = i[:i.find(' ')]

            if i.find('/') != -1 and i.find('.') != -1:
                accounts_dict[username] = i.strip()
    else:
        content = lh_accounts.read()
        lh_accounts.seek(0)
        users = re.findall(r'([a-zA-Z0-9.&]+@[a-zA-Z0-9.&]+)\s\(\*\)<\/span><\/a><\/td><td class=\"w160\".{0,20}>(\d+\.\d{2})\sMB\s\/\s(\d+\.\d{2})', content, re.MULTILINE)
        for user, used, total in users:
            accounts_dict[user] = used + ' / ' + total

used_space = 0
all_space = 0
tmp = ''
tmp_used = ''
tmp_all = ''

for username, space in accounts_dict.items():
    tmp = space.split('/')

    tmp_used = tmp[0]
    tmp_used = tmp_used.split()

    tmp_all = tmp[1]
    tmp_all = tmp_all.split()

    used_space += D(tmp_used[0])
    all_space += D(tmp_all[0])

    accounts_dict[username] = [float(tmp_used[0]), float(tmp_all[0]), float(D(tmp_all[0])-D(tmp_used[0]))]

accounts_free_dict = {}
accounts_all_dict = {}
for username, space in accounts_dict.items():
    #print('Email {EMAIL}\nfree: {FREE}\nused: {USED}\ntotal: {ALL}\n'.format(EMAIL=username, FREE=space[2], USED=space[0], ALL=space[1]))
    accounts_free_dict[space[2]] = [username, space[0], space[1]]
    accounts_all_dict[space[1]] = [username, space[0], space[2]]

#with open('test3.txt', 'w') as testing:
    #for i in sorted (accounts_free_dict, reverse=True):
        #testing.write('Email {EMAIL}\nfree: {FREE}\nused: {USED}\ntotal: {ALL}\n'.format(EMAIL=accounts_free_dict[i][0], FREE=i, USED=accounts_free_dict[i][1], ALL=accounts_free_dict[i][2]))
    #print('Email {EMAIL}\nfree: {FREE}\nused: {USED}\ntotal: {ALL}\n'.format(EMAIL=accounts_free_dict[i][0], FREE=i, USED=accounts_free_dict[i][1], ALL=accounts_free_dict[i][2]))

#print('We have {USED} MB used space on users\' accounts.\nWe have {ALL} MB assigned to users\' accounts.\nWe have {AVA} MB free space on users\' accounts.\n'.format(USED=used_space, ALL=all_space, AVA=all_space-used_space))

choice = ''
while choice != 'q':
    print('We have {USED} MB used space on users\' accounts.\nWe have {ALL} MB assigned to users\' accounts.\nWe have {AVA} MB free space on users\' accounts.\n'.format(USED=used_space, ALL=all_space, AVA=all_space-used_space))
    print("Menu:\n1 - List 5 users with the most available free space\n2 - Save all users to file in order of available free space\n3 - List 5 users with the biggest quota\n4 - Save all users to file i order of quota size\nq - exit program\n(file will be saved in this same directory that running program)")
    choice = input('--> ')
    if choice == '1':
        os.system('cls')
        counter = 0
        for i in sorted (accounts_free_dict, reverse=True):
            print('Email {EMAIL}\nfree: {FREE}\nused: {USED}\ntotal: {ALL}\n'.format(EMAIL=accounts_free_dict[i][0], FREE=i, USED=accounts_free_dict[i][1], ALL=accounts_free_dict[i][2]))
            counter += 1
            if counter >= 5:
                break 
    elif choice == '2':
        os.system('cls')
        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open('mails-' + timestr + '.txt', 'w') as mails:
            for i in sorted (accounts_free_dict, reverse=True):
                mails.write('Email {EMAIL}\nfree: {FREE}\nused: {USED}\ntotal: {ALL}\n\n'.format(EMAIL=accounts_free_dict[i][0], FREE=i, USED=accounts_free_dict[i][1], ALL=accounts_free_dict[i][2]))
        print('File \'mails-' + timestr + '.txt\' saved!\n')
    elif choice == '3':
        os.system('cls')
        counter = 0
        for i in sorted (accounts_all_dict, reverse=True):
            print('Email {EMAIL}\nfree: {FREE}\nused: {USED}\ntotal: {ALL}\n'.format(EMAIL=accounts_all_dict[i][0], FREE=accounts_all_dict[i][2], USED=accounts_all_dict[i][1], ALL=i))
            counter += 1
            if counter >= 5:
                break 
    elif choice == '4':
        os.system('cls')
        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open('mails-' + timestr + '.txt', 'w') as mails:
            for i in sorted (accounts_all_dict, reverse=True):
                mails.write('Email {EMAIL}\nfree: {FREE}\nused: {USED}\ntotal: {ALL}\n'.format(EMAIL=accounts_all_dict[i][0], FREE=accounts_all_dict[i][2], USED=accounts_all_dict[i][1], ALL=i))
        print('File \'mails-' + timestr + '.txt\' saved!\n')
    else:
        os.system('cls')
        print('Selected wrong option!\n')