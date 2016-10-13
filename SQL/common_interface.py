import env
from pysqlite2 import dbapi2 as sqlite
#import sqlite3 as sqlite

# imported for supporting file operations
import os
import sys
import pwd
import grp
import stat
import sha

class DEBUG:
    def __init__(self,msg):
        if msg:
            #dtl.logger.debug(msg)
            print msg

def checkFileAttribute(filename, default=False, owner=None, group=None, mode=None):
    """ check DB file """
    defaultfilename = env.sql.dbpath or None
    defaultowner = env.sql.user or None
    defaultgroup = env.sql.group or None
    defaultmode = env.sql.filemode or None
    if default:
        self_filename = filename or defaultfilename
        self_owner = owner or defaultowner
        self_group = group or defaultgroup
        self_mode = mode or defaultmode
    else:
        self_filename = filename or None
        self_owner = owner or None
        self_group = group or None
        self_mode = mode or None
    statinfo = os.stat(self_filename)
    uid = statinfo.st_uid
    gid = statinfo.st_gid
    mode= statinfo.st_mode
    if not os.path.exists(self_filename):
        DEBUG("File %s is absent" % (self_filename))
        return False
    if self_owner and pwd.getpwuid(uid).pw_name != self_owner:
        DEBUG("Owner of file %s must be %s" % (self_filename, self_owner))
        return False
    if self_group and grp.getgrgid(gid).gr_name != self_group:
        DEBUG("Group of file %s must be %s" % (self_filename, self_group))
        return False
    if self_mode and mode != self_mode:
        DEBUG("File %s must have attribute: rw-rw----" % self_filename)
        return False
    return True

   
class DBSQLite(object):
    """ SQLITE common interface """
    
    _NOTINITIALIZED_DB_STATE = 0
    _INITIALIZED_DB_STATE = 1
    _LOADED_DB_STATE = 2

    def __init__(self, fileDB=env.sql.dbpath):
        """ constructor of  DBSQLite """
        if env:
            self.defaultFileDB = env.sql.dbpath
            self.defaultMode = env.sql.filemode
            self.defaultOwner = env.sql.user
            self.defaultGroup = env.sql.group
            #"stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP"
            self.defaultTable = env.sql.table
        self.fileDB = fileDB
        self.db_connection = None
        self.db_cursor = None
        self.currentState = self._NOTINITIALIZED_DB_STATE
        if self._load():
            self.currentState = self._INITIALIZED_DB_STATE

    def __del__(self):
        """ destructor of  DBSQLite """
        return self._close()

    def _getFilename(self):
        """ check file of SQLite DB """
        if os.path.exists(str(self.fileDB)):
            DEBUG("DB_SQLLite->getFilename: FILE is presented %s"%(self.fileDB))
            return str(self.fileDB)
        else:
            DEBUG("DB_SQLLite->getFilename: File is absent %s"%(self.fileDB))
            return None

    def _load(self):
        """ load file of SQLite DB """
        if  self.currentState == self._NOTINITIALIZED_DB_STATE:
            return self._connect()
        DEBUG("DB_SQLLite->LOAD action has been failed")
        return self._NOTINITIALIZED_DB_STATE

    def _connect(self):
        """ connect to SQLite DB """
        filename = self._getFilename()
        if True: #checkFileAttribute(filename):
            self.db_connection = sqlite.connect(filename)
            self.db_connection.row_factory = sqlite.Row
            self.db_cursor = self.db_connection.cursor()
            DEBUG("DB_SQLLite->_conect: connected to %s" % filename)
            return self._INITIALIZED_DB_STATE
        DEBUG("DB_SQLLite->LOAD action has been failed due to file is absent")
        return self._NOTINITIALIZED_DB_STATE

    def _close(self):
        """ disconnect of SQLite DB """
        if self.db_connection:
            try:
                self._commit()
                self.db_connection.close()
                self.db_connection = None
                self.currentState = self._NOTINITIALIZED_DB_STATE
                DEBUG("DB_SQLLite->close: DB has been closed: %s" % self.fileDB)
                return True
            except Exception, e:
                DEBUG("DB_SQLLite->Exception during _close %s"%e)
                pass
        return False

    def _commit(self):
        """ pass a transaction to SQLite DB """
        if self.db_connection:
            try:
                self.db_connection.commit()
                DEBUG("DB_SQLLite->_commit: DATA is stored to %s" % self.fileDB)
                return True
            except Exception, e:
                DEBUG("DB_SQLLite->Exception during _commit request %s"%e)
                pass
        return False

    def _execute(self, sql, parameters=None):
        """ perform the sql request to SQLite DB
            @return: status, headers, list of rows where every row is ()
        """
        status , headers, list = False, None, None
        try:
            DEBUG("DB_SQLLite->_execute try complete sql=%s" %(sql))
            if parameters:
                headers = self.db_cursor.execute(sql, parameters)
            else:
                headers = self.db_cursor.execute(sql)
            list = self.db_cursor.fetchall()
            self._commit()
            status = True
        except Exception, e:
            if parameters:
                DEBUG("DB_SQLLite->Exeption during executing request [%s] parameters: [%s]: %s" % (sql, parameters, e))
            else:
                DEBUG("DB_SQLLite->Exception during executing sql request [%s]: %s" % (sql, e))
            pass
        DEBUG("DB_SQLLite->_execute status=%s sql=%s headers=%s list=%s"%(status,sql,headers,list))
        return status, headers, list

    def getId(self, headers,list,name_id):
        """ return the value or list by name_id """
        if headers and list:
            i = 0
            new_list = []
            for x in headers.description:
                if x and x[0] == name_id:
                    c = 0
                    for v in list:
                        new_list.append(list[c][i])
                        c = c+1
                    #return list[0][i]
                    return new_list
                i = i+1
                       
    def create(self,sql):
        """ CREATE request to SQLite DB """
        return self._execute(sql)

    def insert(self, dic):
        """ INSERT request to SQLite DB """
        table = dic.get('table', '')
        columns = dic.get('values',{}).keys()
        values = dic.get('values',{}).values()
        columns_str = ','.join("'"+str(column)+"'" for column in columns)
        values_str = ','.join("'"+str(values[i]).strip()+"'" for i in xrange(len(values)))
        sql = "INSERT INTO %s (%s) VALUES (%s)" %(table, columns_str, values_str)
        return self._execute(sql)

    def select(self, dic):
        """ SELECT request to SQLite DB """
        table = dic.get('table', '')
        columns = dic.get('where',{}).keys()
        values = dic.get('where',{}).values()
        columns_str = ','.join(str(column) for column in columns)
        where_str = ' AND '.join((str(columns[i])+"='"+str(values[i])+"'") for i in xrange(len(columns)))
        select_columns = dic.get('all', columns_str) # by default '*' - select all columns
        sql = "SELECT %s FROM %s WHERE %s"%(select_columns, table, where_str)
        return self._execute(sql)


    def update(self, dic):
        """ UPDATE request to SQLite DB """
        table = dic.get('table', '')
        columns = dic.get('where',{}).keys()
        values = dic.get('where',{}).values()
        where_str = ' AND '.join((str(columns[i])+"='"+str(values[i])+"'") for i in xrange(len(columns)))
        set_columns = dic.get('set',{}).keys()
        set_values = dic.get('set',{}).values()
        set_str = ','.join((str(set_columns[i])+"='"+str(set_values[i])+"'") for i in xrange(len(set_columns)))
        sql = "UPDATE %s SET %s WHERE %s"%(table, set_str, where_str)
        return self._execute(sql)
    
    def delete(self, dic):
        """ DELETE request to SQLite DB """
        table = dic.get('table', '')
        columns = dic.get('where',{}).keys()
        values = dic.get('where',{}).values()
        where_str = ' AND '.join((str(columns[i])+"='"+str(values[i])+"'") for i in xrange(len(columns)))
        sql = "DELETE FROM %s WHERE %s"%(table,where_str)
        return self._execute(sql)

    def empty(self, dic):
        """ EMPTY request to SQLite DB """
        table = dic.get('table', '')
        sql = "DELETE FROM %s"%(table)
        return self._execute(sql)

    def rowcount(self,dic,get_id=None):
        """ COUNT request to SQLite DB
            @return: count of rows or 'id' of latest row
                     otherwise function returns -1
        """
        try:
            table = dic.get('table', '')
            sql = "SELECT COUNT() FROM %s"%(table)
            if get_id:
                id = dic.get('id', '')
                if id:
                    sql = "SELECT COUNT(),%s FROM %s"%(id,table)
            self.db_cursor.execute(sql)
            result = self.db_cursor.fetchone()
            #DEBUG("DB_SQLLite->rowcount sql=%s" %(sql))
            if not get_id and result:
                return result[0]
            return result
        except Exception, e:
            DEBUG("DB_SQLLite->Exception during rowcount request %s"%e)
            pass
        return -1

    def printTable(self, table, condition = None):
        """ show requested table """
        if self.currentState == self._INITIALIZED_DB_STATE:
            DEBUG("table: %s" % table)
            if condition:
                sql = "SELECT * FROM %s WHERE %s" % (table, condition)
            else:
                sql = "SELECT * FROM %s" % table
            status, h,l = self._execute(sql)
            DEBUG(" | ".join(["%20s"%x[0] for x in h.description]))
            for q in l:
                DEBUG(" | ".join(["%20s"%x for x in q]))

    def printResult(self, headers, list):
        """ show requested rows """
        DEBUG(" | ".join(["%20s"%x[0] for x in headers.description]))
        if list:
            for q in list:
                DEBUG(" | ".join(["%20s"%x for x in q]))
