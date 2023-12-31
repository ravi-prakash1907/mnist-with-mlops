import json
import os
import sys


class JSONReader:
    def __init__(self, yang_path=None, json_path=None, xml_path=None,jsonData=None, xmlStr=None):
        print(1)
        self.xmlStr = xmlStr
        self.yang_path = yang_path
        self.xml_path = xml_path
        self.json_path = json_path
        self.tables = []
        self.module_name = ''
        self.connections = []
        self.ports = []
        self.table = None
        abs_path = sys.path[0]
        base_name = os.path.dirname(abs_path)
        resources_path = os.path.join(base_name, "..\\resources\\config.json")
        print(resources_path)
        self.db_credentials = json.loads(open(resources_path).read())

        print(self.db_credentials)

        # Print the type of data variable
        print("Type:", type(self.db_credentials))

        # Print the data of dictionary
        print("\ndag:", self.db_credentials['dag'][0]['dagname'])
        print("\nmodel:", self.db_credentials['model'][0])

    @staticmethod
    def main():
        lm = JSONReader()

if __name__ == '__main__':
    JSONReader.main()
 