import xml.dom.minidom
from xmlhandler import DynamicTokenXMLHandler
LISTCOMMANDS = ['GetNewToken']
TAGS = ['XMLAction']

class DEBUG:
    def __init__(self,msg):
        if msg:
            print msg

class DynamicTokenXMLParser:
    def __init__(self, xmlbody=None):
        self.status = False
        self.reply = None
        self._xml = xmlbody or None
        self._dom = None
        self._list_nodes = []
        self._handler = None
        if xmlbody:
            self.xmlparcer(xmlbody)

    def __repr__(self):
        return 'DynamicTokenXMLParser INFO: XML body=%s'%(self._xml)        

    def _postprocess(self,node=None):
        if node is None:
            node = self._dom
            dic = {str(node.nodeName):{'item':node,'data':''}}
            self._list_nodes.append(dic)
        for child in node.childNodes:
            if child.nodeType != node.TEXT_NODE: 
                self._postprocess(child)
            elif child.parentNode:
                data = child.nodeValue.strip() or ''
                dic = {str(child.parentNode.nodeName):{'item':child.parentNode,'data':data}}
                if not self._checkitem(str(child.parentNode.nodeName).strip()):
                    self._list_nodes.append(dic)
    
    def _posthandler(self):
        for item in self._list_nodes:
            end = 0
            for command in LISTCOMMANDS:
                tag = item.keys()[0] or ''
                data = item.values()[0] or ''
                tag_command = ''
                if data:
                    tag_command = data.get('data') or ''
                if str(tag) in TAGS and str(tag_command) in LISTCOMMANDS:                    
                    self._handler = DynamicTokenXMLHandler(tag_command,self._list_nodes)
                    #DEBUG('STATUS=%s'%self._handler.status)
                    #DEBUG(self._handler.__repr__())
                    self.reply = self._handler.reply or None
                    end = 1
                    break
            if end:
                break
        return self.reply

    def _checkitem(self, key):
        if self._list_nodes and key:
            for dic in self._list_nodes:
                dk = dic.keys()[0]
                if dk and str(dk) == str(key):
                    return True
        return False
    
    def xmlparcer(self,xmlbody):
        self.status = False
        try:
            self._dom = xml.dom.minidom.parseString(xmlbody)
            self._dom.normalize()
            self._postprocess()
            self._posthandler()
            DEBUG(" _list_nodes : %s"%(self._list_nodes))
            if self.reply:
                self.status = True
        except xml.dom.expatbuilder.expat.ExpatError,e:
            self.status = False
            self.reply = "ERROR: DynamicTokenXMLParser::xmlparcer %s"%e
            DEBUG("ERROR: DynamicTokenXMLParser::xmlparcer %s"%e)

    def _print_tree(self,node=None,level=0):
        if node is None:
            node = self._dom
        if node.nodeType != node.TEXT_NODE:
            atts = node.attributes or {}
            att_string = ", ".join(["Attr: %s=%s " % (k.strip(), v.strip()) for k, v in atts.items()])
            DEBUG(". "*level, 'Tag:', node.nodeName.strip(), att_string)
            for child in node.childNodes:
                self._print_tree(child, level+1)
        else:
            if node.nodeValue.strip():
                DEBUG(". "*level, 'name_parent:',node.parentNode.nodeName, "Value: %s" % repr(node.nodeValue.strip()))
