
def db1():
    import sqlite
    conn = sqlite.connect('languagedb') # create file if it doesn't exist
    conn.execute("create table if not exists language_strings(id, language, string)") #create table
    data = []

    for x in xrange (0,1000):
        str1 = (u'STRING#' + str(x))
        data += [(x, u'ENG', str1)] # data for table

    #print data
    conn.executemany("insert into language_strings(id, language, string) values (?,?,?)", data) #record to DB
    conn.commit() # save
    conn.close() # close

    conn = sqlite.connect('languagedb') # open DB
    for row in conn.execute("select * from language_strings"): # regular request
        print row[0], row[1], row[2]
        print '==='

        #conn.row_factory = sqlite3.Row # create the fabric f ROW
        #cur = conn.cursor() # create a cursore
        #cur.execute("select * from person")
        #for row in cur:
        #    print row['firstname'], row[1]
    conn.close()  # close DB

def db2(str9):
    import sqlite

    import time
    print time.time()
    
    conn = sqlite.connect('./languagedb') # create file if it doesn't exist    
    c = conn.cursor()
    strq = 'select * from language_strings where string="'+str9+'"'
    c.execute(strq)
    print strq
    for row in c:
        print row[0],row[1],row[2]

    print time.time()
    conn.close()
    
def csv1():
    file1 = open("./languagedb.csv","w+")
    data = []

    for x in xrange (0,1000):
        str1 = (u'STRING#' + str(x))
        data += [(x, u'ENG', str1)] # data for table
        str2=""
        str2 = str(x)+",ENG,"+str1+'\n'
        file1.write(str2)
    
    file1.read()
    
def csv2(str9):
    import csv
    
    import time
    print time.time()

    spamReader = csv.reader(open('./languagedb.csv'), delimiter=',', quotechar='|')
    for row in spamReader:
        if str9 in row:
            print "CSV HAS THE " + str9
            #    print ', '.join(row)
    
    print time.time()
    

import profile
import pstats 
profile.run("csv2(u'STRING#999')","csv.res")
profile.run("db2(u'STRING#999')","db.res")

stat = pstats.Stats('csv.res')
stat.strip_dirs()
stat.sort_stats('cumulative')
stat.print_stats()

stat = pstats.Stats('db.res')
stat.strip_dirs()
stat.sort_stats('cumulative')
stat.print_stats()

#csv2("STRING#999")
#db2 ('STRING#999')

if __name__ == '__main__':
    pass
