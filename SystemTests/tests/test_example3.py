import unittest
import time
from optparse import OptionParser

class TaggedFieldTest3(unittest.TestCase):
    def setUp(self):
        self.s = 3
        self.verbosity=2

    def test1(self):
        time.sleep(self.s)
        i=0
        j=0
        self.assertTrue(i == 0 and j == 0 or i != 0 and j != 0)

    def tests2(self):
        time.sleep(3)
        a = [1,2] 
        self.assertTrue(a, [])

#if __name__ == '__main__':
#    unittest.main()
parser = OptionParser()
parser.add_option("-f")
(opt, args) = parser.parse_args()
print opt.f
output_stream = open(opt.f,'w+')
suite = unittest.TestLoader().loadTestsFromTestCase(TaggedFieldTest3)
result = unittest.TextTestRunner(stream=output_stream, verbosity=2).run(suite)
output_stream.write("%s"%result)
output_stream.close()
