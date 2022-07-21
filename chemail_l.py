#!/usr/bin/python3

import re
import os
from email.parser import Parser
import argparse

class EmlDisassembly:
    def __init__(self):
        self.list_paths = []

    def message_count(self, path_file):
        for (paths,dirs,files) in os.walk(path_file):
            for file in files:
                path = paths + file
                self.list_paths.append(path)
        messages = '\n\033[47m\033[30m----Number of messages in a folder:\033[0m \033[32m{0}\033[0m\n'.format(str(len(self.list_paths)))
        print(messages)

    def create_files(self,login,raw_email,file):
        os.mkdir(login)
        print('\033[33m----Folder with name {0} created\033[0m'.format(login))
        new_eml = open(login + '/' + file, 'a+')
        new_eml.write(raw_email)
        new_eml.close()
        print('----Message with name <<<{0}>>> created---\033[33m{1}\033[0m'.format(file, login))

    def create_files_oserror(self,login,raw_email,file):
        new_eml = open(login + '/' + file, 'a+')
        new_eml.write(raw_email)
        new_eml.close()
        print('----Message with name <<<{0}>>> created---\033[33m{1}\033[0m'.format(file, login))

    def folder_mails(self, path_file):
        for (paths,dirs,files) in os.walk(path_file):
            for file in files:
                path = paths + file
                with open(path) as fp:
                    raw_email = fp.read()
                    ur = ['undisclosed-recipients']
                    emailcontent = Parser().parsestr(raw_email)
                    To = emailcontent['To']
                    if re.findall('<.*@.*>', To):
                        login = ''.join(re.findall('<(.*@.*)>', To))
                        with open('logins.txt') as logins_file:
                            for login_file in logins_file.readlines():
                                login_up = ''.join(login_file.split('\n'))
                                if login_up == login:
                                    try:
                                        self.create_files(login,raw_email,file)
                                    except OSError:
                                        self.create_files_oserror(login,raw_email,file)
                        logins_file.close()
                    elif re.findall('.*@.*', To):
                        login_next = ''.join(re.findall('.*@.*', To))
                        with open('logins.txt') as logins_file_next:
                            for login_file in logins_file_next.readlines():
                                login_up_ = ''.join(login_file.split('\n'))
                                if login_up_ == login_next:
                                    try:
                                        self.create_files(login_next,raw_email,file)
                                    except OSError:
                                        self.create_files_oserror(login_next,raw_email,file)
                    elif re.findall('undisclosed-recipients:;', To):
                        try:
                            self.create_files(''.join(ur), raw_email, file)
                        except OSError:
                            self.create_files_oserror(''.join(ur), raw_email, file)
                    else:
                        pass

    def main(self):
        parser = argparse.ArgumentParser(description='Sorting an array of messages by creating a recipient directory')
        parser.add_argument('-p', '--path', type=str, help='Path to file array')
        args = parser.parse_args()

        if args.path:
            self.message_count(args.path)
            self.folder_mails(args.path)
        else:
            print('\033[31mUnknown Argument\033[0m')

if __name__ == '__main__':
    obj = EmlDisassembly()
    obj.main()
