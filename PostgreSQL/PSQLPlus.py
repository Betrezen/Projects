
__author__="emakar"
__date__ ="$24.09.2010 11:49:23$"

import postgresql

class PSQLPlus:
    def __init__(self,database,user,password,host,port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = postgresql.open(database = self.database,user = self.user,password = self.password, host = self.host, port = self.port)

    def executeQuery(self,query):
        self.RowSet = self.db.prepare(query)
        self.ColumnNames = self.RowSet.column_names
        self.ColumnTypes = self.RowSet.column_types

    def reconnect(self,database,user,password,host,port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = postgresql.open(database = self.database,user = self.user,password = self.password, host = self.host, port = self.port)
        


if __name__ == "__main__":        
    psqlplus = PSQLPlus('vzw-mon-2010-08','nimwh','nimwh', 'report2.nimone.com', 5432)
    psqlplus.executeQuery('select * from accepted_iden_details_01 limit 5')
    psqlplus.reconnect('vzw-mon-2010-08','nimwh','nimwh', 'report2.nimone.com', 5432)
    