from decimal import Decimal as D
import os
import tkinter as tk
from tkinter import filedialog
import re
import time


def choose_file():
    print('Choose a prepared .txt file with list of accounts.\n')

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def extract_data(file_path):
    accounts_dict = {}
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
    return accounts_dict

def sort_data(accounts_dict):
    all_space = 0
    used_space = 0
    users_counter = 0

    tmp_all = ''
    tmp_used = ''
    tmp_values = ''
    
    for username, values in accounts_dict.items():
        tmp_values = values.split('/')

        tmp_used = tmp_values[0]
        tmp_used = tmp_used.split()

        tmp_all = tmp_values[1]
        tmp_all = tmp_all.split()

        used_space += D(tmp_used[0])
        all_space += D(tmp_all[0])

        users_counter += 1

        accounts_dict[username] = [float(tmp_used[0]), float(tmp_all[0]), float(D(tmp_all[0])-D(tmp_used[0]))]

    return used_space, all_space, users_counter, accounts_dict

def show_menu(used_space, all_space, users_counter, accounts_dict):

    choice = ''
    while choice != 'q':
        print('We have {USERS} users.\nWe have {USED} MB of used space on users\' accounts.\nWe have {ALL} MB of assigned to users\' accounts.\nWe have {AVA} MB of free space on users\' accounts.\n'.format(USERS=users_counter, USED=used_space, ALL=all_space, AVA=all_space-used_space))
        print("Menu:\n1 - List 5 users with the most available free space\n2 - Save all users to file in order of available free space\n3 - List 5 users with the biggest quota\n4 - Save all users to file in order of quota size\nq - exit program\n(file will be saved in this same directory that running program)")
        choice = input('--> ')
        if choice == '1':
            os.system('cls')
            counter = 0
            accounts_dict_tmp = dict(accounts_dict)

            while counter < 5:
                most_free_space = 0
                email = ''
                all_space_tmp = 0
                used_space_tmp = 0
                for username, values in accounts_dict_tmp.items():
                    if values[2] > most_free_space:
                        most_free_space = values[2]
                        email = username
                        all_space_tmp = values[1]
                        used_space_tmp = values[0]
                print('Email {EMAIL}\nfree: {FREE}\nused: {USED}\ntotal: {ALL}\n'.format(EMAIL=email, FREE=most_free_space, USED=used_space_tmp, ALL=all_space_tmp))
                accounts_dict_tmp.pop(email)
                counter += 1

        elif choice == '2':
            os.system('cls')
            timestr = time.strftime("%Y%m%d-%H%M%S")
            counter = 0
            accounts_dict_tmp = dict(accounts_dict)

            with open('free_space_mails-' + timestr + '.txt', 'w') as mails:
                while counter < users_counter:
                    email = ''
                    most_free_space = 0
                    for username, values in accounts_dict_tmp.items():
                        if email == '':
                            most_free_space = values[2]
                            email = username
                            all_space_tmp = values[1]
                            used_space_tmp = values[0]
                        if values[2] > most_free_space:
                            most_free_space = values[2]
                            email = username
                            all_space_tmp = values[1]
                            used_space_tmp = values[0]
                    mails.write('Email {EMAIL}\nfree: {FREE}\nused: {USED}\ntotal: {ALL}\n\n'.format(EMAIL=email, FREE=most_free_space, USED=used_space_tmp, ALL=all_space_tmp))
                    accounts_dict_tmp.pop(email)
                    counter += 1

            print('File \'free_space_mails-' + timestr + '.txt\' saved!\n')

        elif choice == '3':
            os.system('cls')

            counter = 0
            accounts_dict_tmp = dict(accounts_dict)

            while counter < 5:
                most_free_space = 0
                email = ''
                all_space_tmp = 0
                used_space_tmp = 0
                for username, values in accounts_dict_tmp.items():
                    if values[1] > all_space_tmp:
                        most_free_space = values[2]
                        email = username
                        all_space_tmp = values[1]
                        used_space_tmp = values[0]
                print('Email {EMAIL}\nfree: {FREE}\nused: {USED}\ntotal: {ALL}\n'.format(EMAIL=email, FREE=most_free_space, USED=used_space_tmp, ALL=all_space_tmp))
                accounts_dict_tmp.pop(email)
                counter += 1

        elif choice == '4':
            os.system('cls')
            timestr = time.strftime("%Y%m%d-%H%M%S")
            counter = 0
            accounts_dict_tmp = dict(accounts_dict)

            with open('total_space_mails-' + timestr + '.txt', 'w') as mails:
                while counter < users_counter:
                    email = ''
                    all_space_tmp = 0
                    for username, values in accounts_dict_tmp.items():
                        if email == '':
                            most_free_space = values[2]
                            email = username
                            all_space_tmp = values[1]
                            used_space_tmp = values[0]
                        if values[1] > all_space_tmp:
                            most_free_space = values[2]
                            email = username
                            all_space_tmp = values[1]
                            used_space_tmp = values[0]
                    mails.write('Email {EMAIL}\nfree: {FREE}\nused: {USED}\ntotal: {ALL}\n\n'.format(EMAIL=email, FREE=most_free_space, USED=used_space_tmp, ALL=all_space_tmp))
                    accounts_dict_tmp.pop(email)
                    counter += 1

            print('File \'total_space_mails-' + timestr + '.txt\' saved!\n')

        elif choice == 'q':
            break
        else:
            os.system('cls')
            print('Selected wrong option!\n')

if __name__=="__main__":
    os.system('cls')
    file_path = choose_file()
    data = extract_data(file_path)
    used_space, all_space, users_counter, accounts_dict= sort_data(data)
    show_menu(used_space, all_space, users_counter, accounts_dict)