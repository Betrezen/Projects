#example
"""
    import profile
    import pstats
    filename1 = '/tmp/nav_profile_stats_1.stats'

    while True:
        #Load accumulators with the options

        profile.runctx('load_accumulators(rcx.rd,queryparser,origin,destin,is_first_included, is_last_included,rfs,to,points_num)',globals(),locals(),filename1)

        accums = load_accumulators(rcx.rd, queryparser, origin, destin,
                                   is_first_included, is_last_included,
                                   rfs, to,
                                   points_num)
                                   
    filenameM = []
    for i,a in enumerate(accums):
        filenameM = '/tmp/nav_main_profile_stats_%d.stats' % i
        profile.runctx('a(manrecs)',globals(),locals(),filenameM)
        manrecs = a(manrecs)
        
    #read all files and print it to corresponding format
    stat = pstats.Stats('/tmp/nav_profile_stats_1.stats')
    for i in xrange(0, len(accums)):
        stat.add('/tmp/nav_main_profile_stats_%d.stats' % i)

    stat.strip_dirs()
    stat.sort_stats('cumulative')
    #stat
    stat.print_stats('\(')
    #incom
    stat.print_callers()
    #out
    stat.print_callees()
        
                                   
"""

import profile
import pstats 

stat = pstats.Stats('c:\\tmp\\nav_main_profile_stats_0.stats')
filename=[]
for i in xrange (1,40):
    filename='c:\\tmp\\nav_main_profile_stats_%d.stats' % i
    stat.add(filename)

stat.strip_dirs()
stat.sort_stats('cumulative')
stat.print_stats()
#incom
stat.print_callers()
#out
stat.print_callees()