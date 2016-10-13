# python -O pqsql_example.py monrpt markers dev11.nimone.com 5432 mon
# author: krozin
try:
    import pgdb
except ImportError:
    pass
import md5
import sys,os
import string

#from tesla import credfile
#from tesla import env
#from tesla import log

class DbWriter(object):
    """Provides interface to PyGresql libraries."""
    def __init__ (self, db_user, db_password, db_host, db_name):
        print ( "DbWriter.__init__ - user: %r, password: %r, host: %r, DbName: %r" \
                % ( db_user, db_password, db_host, db_name ) )

        if db_password != None:
            m = md5.new()
            m.update(db_password)

        self.conn = pgdb.connect(user=db_user,password=db_password,host=db_host,database=db_name)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        print ( "DbWriter.close_connection - Called." )
        self.conn.close()

class PowerDNSPostgreSQLWriter:
    def __init__(self, user,password,dbhost,dbport,dbname):
        #creds = credfile.CredFile('monrec_mon_db.creds')
        self.psqldb=None
        # = hasattr(creds, 'u') and creds.u or None
        self.user = user
        # = hasattr(creds, 'p') and creds.p or None
        self.password = password
        # = hasattr(creds, 'r') and creds.r or None
        self.dbname = dbname
        # = '%s:%s' % ( env.monitor.events_db_host,env.monitor.events_db_port )
        self.dbhost = '%s:%s' % (dbhost,dbport)
        print self.user, self.password, self.dbhost, self.dbname
        if self.user and self.password and self.dbhost and self.dbname:
            try:
                self.psqldb = DbWriter(db_user=self.user, db_password=self.password, db_host = self.dbhost, db_name = self.dbname)
            except pgdb.Error, e:
                print "Can't to connect to %s",(self.dbhost)


    def insert(self,dic):
        pass
       
    def update(self,dic):
        pass

    def delete(self,dic):
        pass

    def view(self,dic):
        if self.psqldb and dic:
            table = dic.get('table', '')
            columns = dic.get('where',{}).keys()
            values = dic.get('where',{}).values()
            columns_str = ','.join(str(column) for column in columns)
            where_str = ' AND '.join((str(columns[i])+"='"+str(values[i])+"'") for i in xrange(len(columns)))
            limit = dic.get('limit',2)
            headers = self.get_headers(dic)
            #select_columns = dic.get('all', columns_str) # by default '*' - select all columns
            select_columns = ','.join(headers)
            if where_str:
                sql = "SELECT %s FROM %s WHERE %s LIMIT(%d);"%(select_columns, table, where_str, limit)
            else:
                sql = "SELECT %s FROM %s LIMIT %d;"%(select_columns, table, limit)
            #sql = "select * from information_schema.tables where table_schema='public' and table_type='BASE TABLE';"
            print 'SQL=%s'%sql
            self.psqldb.cursor.execute(sql)
            print "\nNumber of records: %d\n" % self.psqldb.cursor.rowcount
        
            # Fetch the first result from the cursor
            print "Content of table:"
            print "*"*40
            print '|','\t\t|\t\t'.join(headers),'|'
            for i in xrange(1,self.psqldb.cursor.rowcount):
                row = self.psqldb.cursor.fetchone()
                print " %s"%(row)
            self.psqldb.conn.commit()            

            #try:
            #    print self.psqldb.cursor.execute(sql)
            #    self.viewtable()
            #except pgdb.Error, e:
            #    print "Can't to perform %s"%(sql)
            #    self.psqldb.conn.rollback()
            #except Exception, e:
            #    print "Can't to perform: %s"%(e)
            #    self.psqldb.conn.rollback()
            #else:
            #    self.psqldb.conn.commit()
        pass

    def get_headers(self, dic):
        lists = []
        row = ''
        # if headers is presented in request - take it otherwise ->
        # if 'all' is presented - take all headers otherwise ->
        # if 'where' returns headers which described in 'WHERE'
        if dic.get('table',''):
            sql = "SELECT attname, attnum FROM pg_attribute, pg_class WHERE attrelid = pg_class.oid and relname = '%s' and attnum > 0;" % (dic.get('table'))
            self.psqldb.cursor.execute(sql)
            #print "\nNumber of records: %d\n" % self.psqldb.cursor.rowcount
	    for i in xrange(1,self.psqldb.cursor.rowcount):
                row = self.psqldb.cursor.fetchone()
                if isinstance(row,list):
                    lists.append(row[0])
            self.psqldb.conn.commit()            

        if dic.get('headers',[]):
            columns = dic.get('headers')
        elif dic.get('all',''):
            columns = []
        elif not dic.get('all', '') and dic.get('where',{}):
            columns = dic.get('where').keys()
        #print "COLUMNS=%s LIST=%s"%(columns,lists)
        
        if columns and lists:
            return list(set(columns).intersection(set(lists)))
        return lists

    def close(self):
        self.psqldb.cursor.close ()

def main(argv=None):
    user = 'monrpt'
    password = 'markers'
    dbhost = 'dev11.nimone.com'
    dbport = '5432'
    dbname = 'mon'
    if len(argv) >= 5:
        user = argv[1]
        password = argv[2]
        dbhost = argv[3]
        dbport = argv[4]
        dbname = argv[5]
    d = PowerDNSPostgreSQLWriter(user,password,dbhost,dbport,dbname)
    dic = {'table':'accepted_iden_details','where':{'credential':'/8AYlokzgIXbEY0s0Sn4EwDWCYIGJa8y8NVV7w5r'},'headers':['credential','connection_name_hash','time'],'limit':10}
    #dic = {'table':'accepted_iden_details','all':'*','limit':10}
    d.view(dic)
    #print d.get_headers(dic)
    d.close()


if __name__ == '__main__':
    sys.exit(main(sys.argv))


