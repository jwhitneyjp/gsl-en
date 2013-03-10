#!/usr/bin/python

import sys,os,unittest

sys.path.append('./tests')

load = unittest.TestLoader()
testlist = []

for filename in os.listdir('./tests'):
    if filename.startswith('test_') and filename.endswith('.py'):
        exec 'import %s' % filename[:-3]
        exec 'testlist.append( load.loadTestsFromModule( %s ) )' % filename[:-3]

alltests = unittest.TestSuite(testlist)

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=0) 
    runner.run(alltests)
    for file in os.listdir('.'):
        if file.endswith('.pyc'):
            os.unlink(file)
