# -*- python -*-
# xml_processor.py: created 2011/07/14.
#

""" XMLProcessor: module for XML parsing """

import string
import xml
import xml.dom.minidom
from xml.parsers.expat import ExpatError
from xml.etree.ElementTree import ElementTree

class FormatError(Exception):
    """  XML format error """
    def __init__(self, value):
        self.value = '%s' % value
    def __str__(self):
        return repr(self.value)

class TagMissingError(Exception):
    """  Tag excaption  """
    def __init__(self, value):
        self.value = '%s' % value
    def __str__(self):
        return repr(self.value)

class TagParamError(Exception):
    """  Tag excaption  """
    def __init__(self, value):
        self.value = '%s' % value
    def __str__(self):
        return repr(self.value)

class XML2DICT(object):
    def __init__(self,xmlstring=None):
        self.xmlstring = xmlstring

    @staticmethod
    def xmltodict(xmlstring):
        """  Convert xmlstring to dict object """
        dic={}
        try:
            if xmlstring:
                dom = xml.dom.minidom.parseString(xmlstring)
                dic[dom.documentElement.nodeName] = elementtodict(dom.documentElement)
                return dic
            else:
                raise FormatError('XML is empty')
        except ExpatError, e:
            raise FormatError('%s' % str(e))
        except Exception, e:
            print e
            pass
        return dic

    @staticmethod
    def xmlfiletodict(filename):
        import os
        dic = {}
        if os.path.exists(filename):
            try:
                dom = xml.dom.minidom.parse(filename)
                dic = {}
                dic[dom.documentElement.nodeName] = elementtodict(dom.documentElement)
            except ExpatError, e:
                raise FormatError('%s' % str(e))
            except Exception, e:
                print e
                pass
        return dic

    @staticmethod
    def convertStrToDic(str):
        d = {}
        if str:
            for item in str.split(','):
                key, value = item.split(':')
                if key and value:
                    d[key] = value
        return d

    @staticmethod
    def dicttoxml(dic):
        def xmlitem(dic):
            """ Convert dic to ElementTree.Element """
            nodes = []
            if not isinstance(dic, dict):
                return None
            tag = dic.get('tag')
            texts = dic.get('text',{})
            attrs = dic.get('attrs',{})
            count = dic.get('count')
            #print tag, texts, attrs
            if texts:
                ii = 0
                for i in texts:
                    text = i
                    attr = {}
                    if attrs and ii <= (len(attrs)-1):
                        attr = attrs[ii]
                    node = xml.etree.ElementTree.Element(tag, attrib=attr)
                    node.text = text
                    nodes.append(node)
                    ii += 1
            else:
                node = None
                if dic.get('childs'):
                    ii = 0
                    for j in dic.get('childs'):
                       attr = {}
                       if attrs and ii <= (len(attrs)-1):
                           attr = attrs[ii]
                       node = xml.etree.ElementTree.Element(tag, attrib=attr)
                       node.text = ''
                       for k,v in j.items():
                           nods = xmlitem(v)
                           for a in nods:
                              node.append(a)
                       ii += 1
                       nodes.append(node)
                elif attrs:
                    for a in attrs:
                        node = xml.etree.ElementTree.Element(tag, attrib=a)
                        nodes.append(node)
            #for i in nodes:
            #print ElementTree.tostring(i)
            return nodes
        """ Converting the given dict to the XML string """
        elem = None
        if not dic or not isinstance(dic,dict):
            return None
        for key, value in dic.items():
            elem = xml.etree.ElementTree.Element(key)
            for _key, _value in value.items():
                subelems = xmlitem(_value)
                for i in subelems:
                    elem.append(i)
        return '<?xml version="1.0" encoding="utf-8"?>' + xml.etree.ElementTree.tostring(elem)

def elementtodict(parent):
    """ Convert XML string to object dict """
    def get_text(node):
        value = None
        child = node.firstChild
        while child is not None:
            if child.nodeType == xml.dom.minidom.Node.TEXT_NODE:
                value = child.nodeValue.strip()
            child = child.nextSibling
        return value
    def get_attributes(node):
        dic = {}
        if node.hasAttributes():
            for i in node.attributes.items():
                dic[i[0]]=i[1]
        return dic
    def get_next_child(node):
        child = node.firstChild
        if not child:
            if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                yield node
        else:
            while child is not None:
                if child.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                    yield child
                child = child.nextSibling
    d = {}
    node = parent.firstChild
    if not node:
        return None
    while node is not None:
        if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
            node_text = get_text(node)
            node_attrs = get_attributes(node)
            #print node.nodeName, node_text, d
            if not d.get('node.nodeName'):
                d.setdefault(node.nodeName, {'tag':node.nodeName})
            if node_text:
                if not d[node.nodeName].get('text'):
                    d[node.nodeName]['text'] = []
                d[node.nodeName]['text'].append(node_text)
            if node_attrs:
                if not d[node.nodeName].get('attrs'):
                    d[node.nodeName]['attrs'] = []
                d[node.nodeName]['attrs'].append(node_attrs)
            child_dict = elementtodict(node)
            if child_dict:
                if not d[node.nodeName].get('childs'):
                    d[node.nodeName]['childs'] = []
                d[node.nodeName]['childs'].append(child_dict)
        node = node.nextSibling
    for key, value in d.items():
        if isinstance(value, list) and len(value) == 1:
            d[key] = value[0]
    return d

def test():
    query="""<?xml version="1.0" encoding="utf-8"?><request><requestType g='sss' k='bbb'>NBI_ISMS_MDN_VERIFICATION_REQUEST</requestType><mdn>9494219858</mdn><language>en-US<l1 hh='90'>l1</l1><l2>l2</l2></language><udid g='10' m='100'>777</udid><udid k='11'>888</udid></request>"""
    dic =  XML2DICT.xmltodict(query)
    print dic, "\n"
    xml = XML2DICT.dicttoxml(dic)
    print xml, "\n"

def test1():
    dic =  XML2DICT.xmlfiletodict('xml.tmp')
    print dic, "\n"
    xml = XML2DICT.dicttoxml(dic)
    print xml, "\n"
"""
<?xml version="1.0" encoding="utf-8"?>
<request>
  <requestType g='sss' k='bbb'>NBI_ISMS_MDN_VERIFICATION_REQUEST</requestType>
  <mdn>9494219858</mdn>
  <language>en-US
      <l1 hh='90'>l1</l1>
      <l2>l2</l2>
  </language>
  <udid g='10' m='100'>777</udid>
  <udid k='11'>888</udid>
</request>
"""

def test2():
    dic =  XML2DICT.xmlfiletodict('xml1.tmp')
    print dic, "\n"
    xml = XML2DICT.dicttoxml(dic)
    print xml, "\n"
"""
<?xml version="1.0" encoding="utf-8"?>
<traffic-notify-query>
    <traffic-record-identifier value="821-1309974603.5565-vnav_android-USA-NAVTEQ">
        <nav-progress session-id="821-1309974603.5565-vnav_android-USA-NAVTEQ" position="13" state="start" route-id="|BkYx77+9a++/vUIp77+9NgDvv73vv73vv70f77+9|"></nav-progress>
    </traffic-record-identifier>
    <cache-contents>
        <cache-item name="maz-186322"></cache-item>
        <cache-item name="maz-1951863"></cache-item>
        <pair value="female-1-amr-v3" key="pronun-style"></pair>
    </cache-contents>
</traffic-notify-query>
"""

def test3():
    dic =  XML2DICT.xmlfiletodict('xml2.tmp')
    print dic, "\n"
    xml = XML2DICT.dicttoxml(dic)
    print xml, "\n"
"""
<?xml version="1.0" encoding="utf-8"?>
<traffic-notify-query>
    <traffic-record-identifier>
        <value>"821-1309974603.5565-vnav_android-USA-NAVTEQ"</value>
        <nav-progress>
            <session-id>"821-1309974603.5565-vnav_android-USA-NAVTEQ"</session-id>
            <position>"13"</position>
            <state>"start"</state>
            <route-id>|BkYx77+9a++/vUIp77+9NgDvv73vv73vv70f77+9|</route-id>
        </nav-progress>
    </traffic-record-identifier>
    <cache-contents>
        <cache-item>
            <name>"maz-186322"</name>
        </cache-item>
        <cache-item>
            <name>"maz-1951863"</name>
        </cache-item>
        <pair>
            <value>"female-1-amr-v3"</value>
            <key>pronun-style</key>
        </pair>
    </cache-contents>
</traffic-notify-query>
"""

def test4():
    dic =  XML2DICT.xmlfiletodict('xml3.tmp')
    print dic, "\n"
    xml = XML2DICT.dicttoxml(dic)
    print xml, "\n"
"""
<?xml version="1.0" encoding="utf-8"?>
<traffic-notify-query>
    <traffic-record-identifier>
        <value>"821-1309974603.5565-vnav_android-USA-NAVTEQ"</value>
        <nav-progress>
            <session-id>"821-1309974603.5565-vnav_android-USA-NAVTEQ"</session-id>
            <position>"13"</position>
            <state>"start"</state>
            <route-id>|BkYx77+9a++/vUIp77+9NgDvv73vv73vv70f77+9|</route-id>
        </nav-progress>
    </traffic-record-identifier>
    <cache-contents>
        <cache-item a="1">
            <name>"maz-186322"</name>
        </cache-item>
        <cache-item b="2">
            <name>"maz-1951863"</name>
        </cache-item>
        <pair>
            <value>"female-1-amr-v3"</value>
            <key>pronun-style</key>
        </pair>
    </cache-contents>
</traffic-notify-query>
"""
test()
print "\n\n"
#test1()
#print "\n\n"
#test2()
#print "\n\n"
#test3()
#print "\n\n"
#test4()
#print "\n\n"
