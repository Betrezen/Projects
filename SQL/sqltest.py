import env
import common_interface as isql

def _getId(headers,list,name_id):
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

db = isql.DBSQLite(env.sql.dbpath)
request = {'table':env.sql.table,'all':'*','where':{'mdn':'123456789'}}
s,h,l = db.select(request)
print str(s),str(h),str(l), l
pin = db.getId(h,l,'pin')
mdn = db.getId(h,l,'mdn')
print "MDN=%s PIN=%s"%(mdn,pin)
for x in l:
    print l

print l[0]
#l[1]

request = {'table':env.sql.table,'all':'*','where':{'mdn':'123456788'}}
s,h,l = db.select(request)
print str(s),str(h),str(l), l
pin = _getId(h,l,'pin')
mdn = _getId(h,l,'mdn')
print "MDN=%s PIN=%s"%(mdn,pin)

