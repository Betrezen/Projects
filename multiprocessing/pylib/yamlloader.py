# -*- python -*-
# author: krozin@gmail.com
# yamlloader.py: created 2011/07/14.
# Copyright (c) krozin@gmail.com
#
# EXAMPLES:
# python -c "from yamlloader import get_env; env=get_env(); print env.__dict__; import time; time.sleep(12); print env._reload(); print env.__dict__"
# sha.new(os.urandom(30).encode('base64')[:-1]).hexdigest()
# d = copy({'foo':42, 'bar':4711}); d.foo == d.get('foo')
# python -c "import time; from yamlloader import get_env; env=get_env(); env.nextUpdate = time.time() + 10; time.sleep(10); print env._reload();"
# python -c "import os,time; print 'last modified: %s'%time.ctime(os.path.getmtime('/var/log/python_server/jsonserv.log'))"
# python -c "import os,time; (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat('/var/log/pthon_server/jsonserv.log'); print (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)"


import yaml
import os
import sha
import time

def copy(x):
    """Makes a deep copy of x, replacing dict with attrdict."""
    if isinstance(x, dict):
        d = attrdict()
        for k, v in x.iteritems():
            d[copy(k)] = copy(v)
        return d
    elif isinstance(x, list):
        return map(copy, x)
    return x

def copyx(x):
    """Makes a deep copy of x, replacing attrdict with dict."""
    if isinstance(x, attrdict):
        d = {}
        for k, v in x.iteritems():
            d[copyx(k)] = copyx(v)
        return d
    elif isinstance(x, list):
        return map(copy, x)
    return x


def deep_update(base, new):
    """Recursively updates a dictionary with new values.
    Similar to base.update(new), except that values at any level deep
    in the dictionary can be updated instead of just the ones at the
    top level.
    """
    for k, v in new.iteritems():
        try:
            if isinstance(base[k], dict) and isinstance(v, dict):
                deep_update(base[k], v)
            else:
                base[k] = v
        except KeyError:
            # new key not yet in base
            base[k] = v

class YamlConfig(object):
    # __loading__
    # import yaml
    # f = open('tree.yaml')
    # use safe_load instead load
    # dataMap = yaml.safe_load(f)
    # f.close()
    
    # __saving__
    # f = open('newtree.yaml', "w")
    # yaml.dump(dataMap, f)
    # f.close()
    def __init__(self,filepath='../server.conf'):
        self.config = {}
        self.filepath = '../server.conf'
        self.latestUpdate = time.time()
        if filepath:
            self.filepath = filepath
        if os.path.exists(self.filepath):
            try:
                f = open(self.filepath,"r")
                self.config = yaml.safe_load(f)                
                self.envlifetime = self.config.get('mainserver').get('envlifetime',100)
                self.nextUpdate = self.latestUpdate + self.envlifetime
                f.close()
            except:
                pass
        else:
            pass

    def _save(self, filepath, dataMap):
        if os.path.exists(filepath):
            try:
                f = open(filepath,"w")
                d={}
                deep_update(d,copyx(dataMap))
                yaml.dump(d, f)
                f.close()
                return True
            except:
                return False
        else:
            return False

    '''
    def _reload(self):
        try:
            if time.time() > self.nextUpdate:
                self.config['mainserver']['mainprocess']['token'] = sha.new(os.urandom(30).encode('base64')[:-1]).hexdigest()
                self.config['mainserver']['mongodbprocess']['token'] = sha.new(os.urandom(30).encode('base64')[:-1]).hexdigest()
                self.nextUpdate = time.time() + self.envlifetime                
                return self._save(filepath=self.filepath,dataMap=self.config)
        except Exception, ex:
            print "__Exception__ %s"%ex
            return False
        return False
    '''
        
class attrdict(dict):
    """Dictionary with support for attribute syntax.
    d = attrdict({'foo-bar':42, 'baz':777}); d.foo_bar == d['foo-bar']; d.hello = "hello"; d.hello == d['hello']
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            pass
        try:
            return self[name.replace('_', '-')]
        except KeyError:
            pass
        raise AttributeError, 'no such attribute or key: %s' % name

    def __setattr__(self, name, value):
        self[name] = value

def get_env(filepath='./server.conf'):
    yt = YamlConfig(filepath)
    d = yt.config
    if not isinstance(d, dict):
        raise ValueError, 'top level is not a dictionary'
    #deep_update(yt.config, copy(d))
    yt.config = copy(d)
    return yt

#def main():
#    env = get_env()
#if __name__ == '__main__':
#    main()