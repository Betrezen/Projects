from xml.parsers import expat

LISTCOMMANDS = ['GetNewToken']
TAGS = ['XMLAction']

class DEBUG:
    def __init__(self,msg):
        if msg:
            print msg

class DynamicTokenXMLHandler:
    def __init__(self,command,data):
        self.status = False
        self._data = data or None
        self._command = command or None
        if self._data and self._command: 
            self.status = True
        
    def __repr__(self):
        return 'DynamicTokenXMLHandler INFO: commands=%s data=%s'%(self._command,self._data)


class DynamicTokenXMLParser:
    def __init__(self, xmlbody=None):
        self._parser = expat.ParserCreate('UTF-8')
        self._parser.returns_unicode = 0
        self._parser.StartElementHandler = self._startElementHandler
        #self._parser.EndElementHandler = self._endElementHandler
        self._parser.CharacterDataHandler = self._charDataHandler
        self._xml = xmlbody
        self._tags = []
        self._tree = []
        self.status = False
        self.reply = None
        if xmlbody:
            self.xmlparcer(xmlbody)

    def __repr__(self):
        return 'DynamicTokenXMLParser INFO: XML %s' %(self._tree)

    def _print_tree(self):
        for tag in self._tags:           
            if tag:
                key = tag.keys()[0]
                value = '_'
                for x in self._tree:
                    if x.keys()[0] == tag.keys()[0]:
                        value = x.values()
                print 'tag name: ', tag.keys(), 'attr: ', tag.values(), 'value: ', value

    def _startElementHandler(self, name, attrs):
        self._tags.append({name:attrs})
    
    #def _endElementHandler(self,name):
    #    pass
    def _checktag(self, key):
        for item in self._tree:
            if item['TagName'] == key:
                return True
        return False
    
    def _checkdata(self,key):
        for item in self._tree:
            if item['TagName'] == key:
                data = item.get('Data','').strip()
                # it can be replased of new data
                if (data == '\n' or data==''):
                    return False
        return True

    def _charDataHandler(self,data):
        key = self._tags[-1].keys()[0]
        attrs = self._tags[-1].values()[0]
        #print key, attrs, repr(data)
        if self._checkdata(key) and not self._checktag(key):
            self._tree.append({'TagName':key,'Attrs':attrs, 'Data':data})

    def _xmlcommandcheck(self,key):
        if key in commandlist:
            return key
        return None

    def _postParserHandler(self):
        for item in self._tree:
            for command in LISTCOMMANDS:
                tag = item.get('TagName','')
                tag_command = item.get('Data','')
                #print tag, tag_command
                if str(tag) in TAGS and str(tag_command) in LISTCOMMANDS:
                    handler = DynamicTokenXMLHandler(tag_command,self._tree)
                    print handler.__repr__()
        
    def xmlparcer(self,xml):
        try:
            try:
                self._parser.Parse(xml)
                self.status = True
                self._postParserHandler()
            except expat.error,e:
                DEBUG ('DynamicTokenXMLParser ERROR: xmlparcer - %s' % e)
        finally:
            return "xml"