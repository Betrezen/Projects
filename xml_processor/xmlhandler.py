class DEBUG:
    def __init__(self,msg):
        if msg:
            print msg

class DynamicTokenXMLHandler:
    def __init__(self,command,data):
        self.status = False
        self._data = data or None
        self._command = str(command).strip() or None
        self.reply = None
        if self._data and self._command: 
            self._commandhandler()
            if self.reply:
                self.status = True

    def __repr__(self):
        return 'DynamicTokenXMLHandler INFO: commands=%s data=%s'%(self._command,self._data)
       
    def _commandhandler(self):
        if self._command == 'GetNewToken':
            self.reply = 'krozin.mycompany.dev.verizon.com'