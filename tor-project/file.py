from datetime import datetime

class File:

    def __init__(self):
        self.name = ''
        self.size = ''
        self.modified = ''

    def __str__(self):
        return 'Name: ' + self.name + ' \tSize: ' + self.size + ' bytes \tLast Modified: ' + self.modified + '\n'

    def update_file(self, name, size, date_modified):
        self.name = name
        self.size = str(size)
        self.modified = self.convert_date(date_modified)

    def convert_date(self, timestamp):
        d = datetime.utcfromtimestamp(timestamp)
        formated_date = d.strftime('%d %b %Y')
        return formated_date
    
    def list_to_string(self, files):
        for i in files:
            str_file += str(i)
        return str_file
            

        