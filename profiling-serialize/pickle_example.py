import sys
import getopt
import string

#-*- coding: ISO-8859-1 -*-

  
    
def f8():
    import cPickle as pickle
    obj = {"one": 123, "two": [1, 2, 3]}
    output = pickle.dumps(obj, 2)
    print output

    obj = pickle.loads(output)
    print obj
    
    #out1=u'\x80\x02ctesla.tps.lib\nTemplateLibrary\nq\x01)\x81q\x02}q\x03(U\x05byfmtq\x04}q\x05(U\x1bpoi-events-config\x00priority\x00q\x06ctesla.tps.lib\nTemplate\nq\x07)\x81q\x08}q\t(U\x05attrsq\n]q\x0bU\x08priorityq\x0caU\x02idq\rM\x80\x01U\x04nameq\x0eU\x11poi-events-configq\x0fubU\x08default\x00q\x10h\x07)\x81q\x11}q\x12(h\n]q\x13h\rM\x90\x01h\x0eU\x07defaultq\x14ubU\x1frecent-loc\x00frequency\x00last-used\x00q\x15h\x07)\x81q\x16}q\x17(h\n]q\x18(U\tfrequencyq\x19U\tlast-usedq\x1aeh\rMO\x01h\x0eU\nrecent-locq\x1bubU\x0elicense-query\x00q\x1ch\x07)\x81q\x1d}q\x1e(h\n]q\x1fh\rM\xa5\x01h\x0eU\rlicense-queryq ubU*subscription-check-status\x00user-identifier\x00q!h\x07)\x81q"}q#(h\n]q$U\x0fuser-identifierq%ah\rM?\x01h\x0eU\x19subscription-check-statusq&ubU\x17place-msg-recipient\x00to\x00q\'h\x07)\x81q(}q)(h\n]q*U\x02toq+ah\rK\xadh\x0eU\x13place-msg-recipientq,ubU"toward-roadinfo\x00primary\x00secondary\x00q-h\x07)\x81q.}q/(h\n]q0(U\x07primaryq1U\tsecondaryq2eh\rK]h\x0eU\x0ftoward-roadinfoq3ubU\x0flink\x00href\x00text\x00q4h\x07)\x81q5}q6(h\n]q7(U\x04hrefq8U\x04textq9eh\rM\xa1\x01h\x0eU\x04linkq:ubU\x14road-local\x00priority\x00q;h\x07)\x81q<}q=(h\n]q>U\x08priorityq?ah\rK\x8eh\x0eU\nroad-localq@ubU!map-style\x00legend\x00route-id\x00scheme\x00qAh\x07)\x81qB}qC(h\n]qD(U\x06legendqEU\x08route-idqFU\x06schemeqGeh\rK\x07h\x0eU\tmap-styleqHubU current-roadinfo\x00primary\x00pronun\x00qIh\x07)\x81qJ}qK(h\n]qL(U\x07primaryqMU\x06pronunqNeh\rKVh\x0eU\x10current-roadinfoqOubU\rshow-headsup\x00qPh\x07)\x81qQ}qR(h\n]qSh\rK\x14h\x0eU\x0cshow-headsupqTubU\x0fpair\x00key\x00value\x00qUh\x07)\x81qV}qW(h\n]qX(U\x03keyqYU\x05valueqZeh\rK\xcfh\x0eU\x04pairq[ubU\'proxpoi-query\x00maneuver\x00route-id\x00scheme\x00q\\h\x07)\x81q]}q^(h\n]q_(U\x08maneuverq`U\x08route-idqaU\x06schemeqbeh\rK\xd6h\x0eU\rproxpoi-queryqcubU\x12traffic-map-query\x00qdh\x07)\x81qe}qf(h\n]qgh\rM\x00\x01h\x0eU\x11traffic-map-queryqhubU\x0cavoid\x00value\x00qih\x07)\x81qj}qk(h\n]qlU\x05valueqmah\rK~h\x0eU\x05avoidqnubU\tdirected\x00qoh\x07)\x81qp}qq(h\n]qrh\rK+h\x0eU\x08directedqsubU:send-place-message-query\x00from\x00from-name\x00message\x00signature\x00qth\x07)\x81qu}qv(h\n]qw(U\x04fromqxU\tfrom-nameqyU\x07messageqzU\tsignatureq{eh\rK\xabh\x0eU\x18send-place-message-queryq|ubU)road-limited-access\x00label\x00lanes\x00priority\x00q}h\x07)\x81q~}q\x7f(h\n]q\x80(U\x05labelq\x81U\x05lanesq\x82U\x08priorityq\x83eh\rK\xf1h\x0eU\x13road-limited-accessq\x84ubU)toward-roadinfo\x00primary\x00pronun\x00secondary\x00q\x85h\x07)\x81q\x86}q\x87(h\n]q\x88(U\x07primaryq\x89U\x06pronunq\x8aU\tsecondaryq\x8beh\rK\\h\x0eU\x0ftoward-roadinfoq\x8cubU\x1emaptile-source\x00gen\x00projection\x00q\x8dh\x07)\x81q\x8e}q\x8f(h\n]q\x90(U\x03genq\x91U\nprojectionq\x92eh\rMe\x01h\x0eU\x0emaptile-sourceq\x93ubU\nurl\x00value\x00q\x94h\x07)\x81q\x95}q\x96(h\n]q\x97U\x05valueq\x98ah\rMg\x01h\x0eU\x03urlq\x99ubU\nset-value\x00q\x9ah\x07)\x81q\x9b}q\x9c(h\n]q\x9dh\rM\x92\x01h\x0eU\tset-valueq\x9eubU\x15road-rotary\x00priority\x00q\x9fh\x07)\x81q\xa0}q\xa1(h\n]q\xa2U\x08priorityq\xa3ah\rK\x90h\x0eU\x0broad-rotaryq\xa4ubU\x1droute-number-info\x00class\x00name\x00q\xa5h\x07)\x81q\xa6}q\xa7(h\n]q\xa8(U\x05classq\xa9U\x04nameq\xaaeh\rKjh\x0eU\x11route-number-infoq\xabubU\x1dturn-roadinfo\x00primary\x00pronun\x00q\xach\x07)\x81q\xad}q\xae(h\n]q\xaf(U\x07primaryq\xb0U\x06pronunq\xb1eh\rKZh\x0eU\rturn-roadinfoq\xb2ubUKiden\x00carrier\x00credential\x00device\x00gps\x00gwsubid\x00language\x00mdn\x00min\x00os\x00platform-id\x00q\xb3h\x07)\x81q\xb4}q\xb5(h\n]q\xb6(U\x07carrierq\xb7U\ncredentialq\xb8U\x06deviceq\xb9U\x03gpsq\xbaU\x07gwsubidq\xbbU\x08languageq\xbcU\x03mdnq\xbdU\x03minq\xbeU\x02osq\xbfU\x0bplatform-idq\xc0eh\rKqh\x0eU\x04idenq\xc1ubU\x19bundle\x00enddate\x00name\x00type\x00q\xc2h\x07)\x81q\xc3}q\xc4(h\n]q\xc5(U\x07enddateq\xc6U\x04nameq\xc7U\x04typeq\xc8eh\rM\xac\x01h\x0eU\x06bundleq\xc9ubU\x10internal-source\x00q\xcah\x07)\x81q\xcb}q\xcc(h\n]q\xcdh\rMf\x01h\x0eU\x0finternal-sourceq\xceubU\x1creverse-geocode-query\x00scale\x00q\xcfh\x07)\x81q\xd0}q\xd1(h\n]q\xd2U\x05scaleq\xd3ah\rK(h\x0eU\x15reverse-geocode-queryq\xd4ubUVnav-maneuver\x00command\x00current-heading\x00distance\x00max-instruction-distance\x00polyline\x00speed\x00q\xd5h\x07)\x81q\xd6}q\xd7(h\n]q\xd8(U\x07commandq\xd9U\x0fcurrent-headingq\xdaU\x08distanceq\xdbU\x18max-instruction-distanceq\xdcU\x08polylineq\xddU\x05speedq\xdeeh\rK?h\x0eU\x0cnav-maneuverq\xdfubU\x10cache-item\x00name\x00q\xe0h\x07)\x81q\xe1}q\xe2(h\n]q\xe3U\x04nameq\xe4ah\rKDh\x0eU\ncache-itemq\xe5ubU\x17road-terminal\x00priority\x00q\xe6h\x07)\x81q\xe7}q\xe8(h\n]q\xe9U\x08priorityq\xeaah\rK\x8fh\x0eU\rroad-terminalq\xebubU\x1cgold-events-config\x00priority\x00q\xech\x07)\x81q\xed}q\xee(h\n]q\xefU\x08priorityq\xf0ah\rM\x7f\x01h\x0eU\x12gold-events-configq\xf1ubU\x12place-msg-want-id\x00q\xf2h\x07)\x81q\xf3}q\xf4(h\n]q\xf5h\rK\xb2h\x0eU\x11place-msg-want-idq\xf6ubU\x1bpoint-label\x00label\x00priority\x00q\xf7h\x07)\x81q\xf8}q\xf9(h\n]q\xfa(U\x05labelq\xfbU\x08priorityq\xfceh\rK\xefh\x0eU\x0bpoint-labelq\xfdubU%traffic-region\x00length\x00location\x00start\x00q\xfeh\x07)\x81q\xff}r\x00\x01\x00\x00(h\n]r\x01\x01\x00\x00(U\x06lengthr\x02\x01\x00\x00U\x08locationr\x03\x01\x00\x00U\x05startr\x04\x01\x00\x00eh\rM \x01h\x0eU\x0etraffic-regionr\x05\x01\x00\x00ubU#road-arterial\x00label\x00lanes\x00priority\x00r\x06\x01\x00\x00h\x07)\x81r\x07\x01\x00\x00}r\x08\x01\x00\x00(h\n]r\t\x01\x00\x00(U\x05labelr\n\x01\x00\x00U\x05lanesr\x0b\x01\x00\x00U\x08priorityr\x0c\x01\x00\x00eh\rK\xf2h\x0eU\rroad-arterialr\r\x01\x00\x00ubU\rtagline\x00text\x00r\x0e\x01\x00\x00h\x07)\x81r\x0f\x01\x00\x00}r\x10\x01\x00\x00(h\n]r\x11\x01\x00\x00U\x04textr\x12\x01\x00\x00ah\rM`\x01h\x0eU\x07tagliner\x13\x01\x00\x00ubU\nmap-event\x00r\x14\x01\x00\x00h\x07)\x81r\x15\x01\x00\x00}r\x16\x01\x00\x00(h\n]r\x17\x01\x00\x00h\rMt\x01h\x0eU\tmap-eventr\x18\x01\x00\x00ubU\x15traffic-notify-reply\x00r\x19\x01\x00\x00h\x07)\x81r\x1a\x01\x00\x00}r\x1b\x01\x00\x00(h\n]r\x1c\x01\x00\x00h\rM$\x01h\x0eU\x14traffic-notify-replyr\x1d\x01\x00\x00ubU\x18map-style\x00legend\x00scheme\x00r\x1e\x01\x00\x00h\x07)\x81r\x1f\x01\x00\x00}r \x01\x00\x00(h\n]r!\x01\x00\x00(U\x06legendr"\x01\x00\x00U\x06schemer#\x01\x00\x00eh\rK\x06h\x0eU\tmap-styler$\x01\x00\x00ubU\x14search-detail-event\x00r%\x01\x00\x00h\x07)\x81r&\x01\x00\x00}r\'\x01\x00\x00(h\n]r(\x01\x00\x00h\rMs\x01h\x0eU\x13search-detail-eventr)\x01\x00\x00ubU\x15vector-tile\x00tx\x00ty\x00tz\x00r*\x01\x00\x00h\x07)\x81r+\x01\x00\x00}r,\x01\x00\x00(h\n]r-\x01\x00\x00(U\x02txr.\x01\x00\x00U\x02tyr/\x01\x00\x00U\x02tzr0\x01\x00\x00eh\rK\xe9h\x0eU\x0bvector-tiler1\x01\x00\x00ubU\x0froute-polyline\x00r2\x01\x00\x00h\x07)\x81r3\x01\x00\x00}r4\x01\x00\x00(h\n]r5\x01\x00\x00h\rK\xe6h\x0eU\x0eroute-polyliner6\x01\x00\x00ubU\x14sync-delete-item\x00id\x00r7\x01\x00\x00h\x07)\x81r8\x01\x00\x00}r9\x01\x00\x00(h\n]r:\x01\x00\x00U\x02idr;\x01\x00\x00ah\rK\xa5h\x0eU\x10sync-delete-itemr<\x01\x00\x00ubU\x14add-favorites-event\x00r=\x01\x00\x00h\x07)\x81r>\x01\x00\x00}r?\x01\x00\x00(h\n]r@\x01\x00\x00h\rMw\x01h\x0eU\x13add-favorites-eventrA\x01\x00\x00ubU\nexhausted\x00rB\x01\x00\x00h\x07)\x81rC\x01\x00\x00}rD\x01\x00\x00(h\n]rE\x01\x00\x00h\rK4h\x0eU\texhaustedrF\x01\x00\x00ubU\x1amessage-query\x00language\x00ts\x00rG\x01\x00\x00h\x07)\x81rH\x01\x00\x00}rI\x01\x00\x00(h\n]rJ\x01\x00\x00(U\x08languagerK\x01\x00\x00U\x02tsrL\x01\x00\x00eh\rK\xb3h\x0eU\rmessage-queryrM\x01\x00\x00ubU\x0bincomplete\x00rN\x01\x00\x00h\x07)\x81rO\x01\x00\x00}rP\x01\x00\x00(h\n]rQ\x01\x00\x00h\rK"h\x0eU\nincompleterR\x01\x00\x00ubU\x13nav-reply\x00route-id\x00rS\x01\x00\x00h\x07)\x81rT\x01\x00\x00}rU\x01\x00\x00(h\n]rV\x01\x00\x00U\x08route-idrW\x01\x00\x00ah\rKAh\x0eU\tnav-replyrX\x01\x00\x00ubU\x1cdetour-avoid\x00label\x00route-id\x00rY\x01\x00\x00h\x07)\x81rZ\x01\x00\x00}r[\x01\x00\x00(h\n]r\\\x01\x00\x00(U\x05labelr]\x01\x00\x00U\x08route-idr^\x01\x00\x00eh\rK\xe2h\x0eU\x0cdetour-avoidr_\x01\x00\x00ubU\nrouteable\x00r`\x01\x00\x00h\x07)\x81ra\x01\x00\x00}rb\x01\x00\x00(h\n]rc\x01\x00\x00h\rK\x1dh\x0eU\trouteablerd\x01\x00\x00ubU\r'
    #obj1 = pickle.loads(out1)
    #print obj1

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

f8()    

#main()  
#if __name__ == "__main__":
#    sys.exit(main())     