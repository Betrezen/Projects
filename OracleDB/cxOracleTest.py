import cx_Oracle

class mycxOracle:
	def __init__(self, constr=None):
		if constr:
			self.connection = cx_Oracle.connect(constr)
		else:
			self.connection = cx_Oracle.connect("MERA_JUPITER/zorro@doraps003.eict.vpdc/DEVRD")
		self.cursor = connection.cursor()
		
	def __delete__(self):
		if self.cursor:
			cursor.close()
		if self.connection:
			connection.close()

	def request(self, req):
		if cursor:
			cursor.execute(req)
			return cursor.fetchall()
		return None

a = mycxOracle()
res = a.request("explain plan set statement_id=test_simple_stmt for select * from emsasset;")
print res