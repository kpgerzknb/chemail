import re
import os
from email.parser import Parser
import argparse
import shutil

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

    def movefile(self,path,login,file):
        shutil.copyfile(path, 'downloads\\' + login + '\\' + file)
        message = '----Message: {0}'.format(file)
        print(message)

    def makedir(self,login):
        os.mkdir('downloads\\' + login)
        print('\033[30m---Create folder with name---{0}\033[0m'.format(login))

    def check_downloads_folder(self):
        dirs = [dirs for (paths,dirs,files) in os.walk('.')]
        if dirs[0].count('downloads'):
            message = '\033[32mFolder <DOWNLOADS> exists\033[0m'
            print(message)
        else:
            os.mkdir('downloads')
            message = '\033[32mFolder <DOWNLOADS> make\033[0m'
            print(message)

    def folder_mails(self, path_file):
        for (paths,dirs,files) in os.walk(path_file):
            for file in files:
                path = paths + file
                with open(path) as fp:
                    emailcontent = Parser().parsestr(fp.read())
                    To = emailcontent['To']
                    with open('logins.txt') as logins_file:
                        for login_file in logins_file.readlines():
                            login_up = ''.join(login_file.split('\n'))
                            if re.findall(login_up, To):
                                try:
                                    self.makedir(login_up)
                                    self.movefile(path, login_up, file)
                                except OSError:
                                    self.movefile(path, login_up, file)
                            else:
                                pass

    def main(self):
        try:
            self.check_downloads_folder()
            self.message_count('files\\')
            self.folder_mails('files\\')
        except TypeError:
            pass


if __name__ == '__main__':
    obj = EmlDisassembly()
    obj.main()
