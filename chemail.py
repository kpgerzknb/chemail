import re
import os
from email.parser import Parser

class EmlDisassembly:
    def __init__(self):
        self.list_paths = []

    def create_files(self,login,raw_email,file):
        os.mkdir(login)
        print('\033[33m----Folder with name {0} created\033[0m'.format(login))
        new_eml = open(login + '\\' + file, 'a+')
        new_eml.write(raw_email)
        new_eml.close()
        print('----Message with name {0} created'.format(file))

    def create_files_oserror(self,login,raw_email,file):
        new_eml = open(login + '\\' + file, 'a+')
        new_eml.write(raw_email)
        new_eml.close()
        print('----Message with name {0} created'.format(file))

    def folder_mails(self):
        for (paths,dirs,files) in os.walk('files\\'):
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
        self.folder_mails()

if __name__ == '__main__':
    obj = EmlDisassembly()
    obj.main()
