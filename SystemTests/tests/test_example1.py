import unittest
import time
from optparse import OptionParser
import json
import requests

class TaggedFieldTest(unittest.TestCase):

    def setUp(self):
        self.s = 2
        self.verbosity=2
        self.r_url = 'http://ec2-54-200-187-137.us-west-2.compute.amazonaws.com:5555/login'
        self.r_headers = {'Content-type': 'application/json', 'Accept':'application/json'}
        
    def testlogin(self):
        data_login = {"admin_sessions":{"password":"test", "email":"krozin@gmail.com"}}
        r = requests.post(self.r_url, data=json.dumps(data_login), headers=self.r_headers)
        print "login"
        self.assertEqual(r.status_code, 200, 'invalid code')

    def testcheck_json(self):
        r_url = 'http://ec2-54-200-187-137.us-west-2.compute.amazonaws.com:5555/login'
        r_headers = {'Content-type': 'application/json', 'Accept':'application/json'}
        data_login = {"admin_sessions":{"password":"test", "email":"krozin@gmail.com"}}
        r = requests.post(self.r_url, data=json.dumps(data_login), headers=self.r_headers)
        print "check_json"
        self.assertTrue(len(r.text)>0)

#if __name__ == '__main__':
#    unittest.main(verbosity=2)

parser = OptionParser()
parser.add_option("-f")
(opt, args) = parser.parse_args()
#print opt.f
output_stream = open(opt.f,'w+')
suite = unittest.TestLoader().loadTestsFromTestCase(TaggedFieldTest)
result = unittest.TextTestRunner(stream=output_stream, verbosity=2).run(suite)
output_stream.write("%s"%result)
output_stream.close()
