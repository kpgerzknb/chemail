import re
import os

class EmlDisassembly:
    def __init__(self):
        self.list_paths = []
    def paths(self):
        for (paths,dirs,files) in os.walk('files/'):
            for file in files:
                all_paths_local = paths + file
                self.list_paths.append(all_paths_local)
    def open_eml(self, path):
        open_eml_file = open(path)
        return open_eml_file.read()
    def to_find(self,string):
        if re.findall('<.*@.*>', string):
            return string
        else: pass
    def comprasion_logins(self,string,login):
        if re.findall(login, string):
            print('c')
    def main(self):
        self.paths()
        file_logins = open('logins.txt')
        for true_path in self.list_paths:
            open_eml = self.open_eml(true_path)
            for login_in in file_logins:
                if re.findall(login_in, open_eml):
                    print(open_eml)


if __name__ == '__main__':
    obj = EmlDisassembly()
    obj.main()
