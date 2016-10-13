from xmlparser import *
#from xmlparser_simple import DynamicTokenXMLParser as DynamicTokenXMLParser_2
#xml =  \
"""<?xml version="1.0"?>
      <root>
        <parent id="top">
          <child1 name="paul">Text goes here</child1>
          <child2 name="fred">More text</child2>
        </parent>
</root>"""

xml_text = \
    """<?xml version="1.0" encoding="utf-8"?>
       <root>
         <header version="0.1">
             <LanguageName>"ENG"</LanguageName>
         </header>
         <body>
           <XMLAction>GetNewToken</XMLAction>
           <ClientInfo>
               <UserLogin>krozin</UserLogin>
               <UserCompany>aaa</UserCompany>
               <TypeCluster>dev</TypeCluster>
               <GeneratedTokenString>krozin.mycompany.dev.verizon.com</GeneratedTokenString>
           </ClientInfo>
         </body>
       </root>"""

def test1():
    #--------------------------------------------------------------------------------------------------------------------------
    fff = DynamicTokenXMLParser(xml_text)
    #fff._print_tree()
    #fff.test1()    
test1()

def test2():
    #--------------------------------------------------------------------------------------------------------------------------
    fff = DynamicTokenXMLParser_2(xml_text)
    print (fff.__repr__())
    print (fff._print_tree())
#test2()

from xml_processor import *

print request(xml_text)

