import sys
import getopt
# -*- coding: ISO-8859-1 -*-

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
        #print (sys.argv)
        self = [sys.argv[1], sys.argv[2], sys.argv[3]]
        print (self)
        return 0
    
_configs = {}
_configs['error'] = [4020, 4021];
_configs['regions'] = {'AMERICA':{'redirect':1, 'bbox':{'top-left':[200,100], 'bottom-right':[100,200]}},
                       'RUSSIA':{'redirect':2, 'bbox':{'top-left':[300,200], 'bottom-right':[200,300]}},
                       'Canada':{'redirect':3, 'bbox':{'top-left':[400,300], 'bottom-right':[300,400]}}}
#_configs['regions']['Canada'] = {'redirect':1, 'type':100}        

def check1(current_region, lat, lon):    

    print "START check1"

    if current_region not in _configs['regions'].keys():
        print current_region + ' None'
        return None

    else:
        #print current_region + ' ' + str(_configs['regions'][current_region]) + ' Yes, It is'
        
        #redirection
        region_info = _configs['regions'][current_region]

        #if 'redirect' not in region_info.keys():
        #    print "redirect" + ' None'
        #    return None

        try:
            if region_info['redirect'] == 0:
                print 'check_redirect_by_latlon : No redirect option'
                return None
        except KeyError:
            print "KEY ERROR: redirect"
        else:
            print "KEY OK: redirect"
        
        if 'bbox' not in region_info.keys():
             print 'check_redirect_by_latlon: Ignoring region' + current_region + ' as no country list available by bbox'
             return None
        if 'top-left' not in region_info['bbox'].keys():
             print 'check_redirect_by_latlon: Ignoring region ' + current_region + ' as no country list available by top-left'
             return None
        if 'bottom-right' not in region_info['bbox'].keys():
             print 'check_redirect_by_latlon: Ignoring region ' + current_region + ' as no country list available by bottom-right'
             return None
             
        top_left = region_info['bbox']['top-left']
        bottom_right = region_info['bbox']['bottom-right']

        print current_region + str(top_left) + str(bottom_right) + "lat=" + str(lat) + "lon=" + str(lon)
            
        if lat >= bottom_right[0] and lat <= top_left[0] and lon >= top_left[1] and lon <= bottom_right[1]:
             print 'check_redirect_by_latlon: Supported by current region'
             return None
        else:
             print 'check_redirect_by_latlon: out of range in current, checking redirect'
             return 1
        return 1;

    return 1 #_configs['regions'].keys() 



res = None
res = check1 ('Franch', 120, 110)
res = check1 ('Canada', 350, 350)
res = check1 ('Canada', 50, 50)

#if __name__ == "__main__":
#    sys.exit(main())