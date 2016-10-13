Python 2.4.3 (#1, Jul 16 2009, 06:21:14) 
[GCC 4.1.2 20080704 (Red Hat 4.1.2-44)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import pickle 
>>> file1=open('/home/krozin/dir1.txt','w+')
>>> dir1={'tmc':{'N1':{'speed':90,'histspeed':100,'length':150},'N2':{'speed':30,'histspeed':50,'length':900}}}
>>> pickle.dump(dir1,file1)

>>> f1=open('/home/krozin/dir1.txt','r').read()
>>> f1
"(dp0\nS'tmc'\np1\n(dp2\nS'N1'\np3\n(dp4\nS'histspeed'\np5\nI100\nsS'length'\np6\nI150\nsS'speed'\np7\nI90\nssS'N2'\np8\n(dp9\ng5\nI50\nsg6\nI900\nsg7\nI30\nsss.(dp0\nS'tmc'\np1\n(dp2\nS'N1'\np3\n(dp4\nS'histspeed'\np5\nI100\nsS'length'\np6\nI150\nsS'speed'\np7\nI90\nssS'N2'\np8\n(dp9\ng5\nI50\nsg6\nI900\nsg7\nI30\nsss."
>>> print pickle.loads(f1)
{'tmc': {'N1': {'speed': 90, 'length': 150, 'histspeed': 100}, 'N2': {'speed': 30, 'length': 900, 'histspeed': 50}}}
>>>