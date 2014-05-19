#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8') 
import re
import urllib
import urllib2
import string
import base64
import random

import cookielib

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import dump
from xml.etree.ElementTree import Comment
from xml.etree.ElementTree import tostring
import xml.etree.ElementTree as ET
# the CDATASection Implentent
def CDATA(text=None):
    element = ET.Element('![CDATA[')
    element.text = text
    return element

ET._original_serialize_xml = ET._serialize_xml


def _serialize_xml(write, elem, encoding, qnames, namespaces):
    if elem.tag == '![CDATA[':
        write("<%s%s]]>" % (elem.tag, elem.text))
        return
    return ET._original_serialize_xml(write, elem, encoding, qnames, namespaces)
ET._serialize_xml = ET._serialize['xml'] = _serialize_xml

class get_solution:
	def __init__(self):
		self.datas={}

	def shaidaima(self,ID):
		pass
	def get_solutionID(self,ID):
		myPage=urllib2.urlopen('http://www.shaidaima.com/source/search/PKU/'+ID).read()
		myMatch=re.findall(r'/source/view/(\d*)',myPage,re.S)
		print 'solution id in www.shaidaima is \n',myMatch
		if not myMatch:
			print 'There is not any solution in www.shaidaima'
			self.datas['solutionID']=None
			return 0
		print 'spider will get the first soulution'
		self.datas['solutionID']=myMatch[0]
		print self.datas['solutionID']
		return 1
		# return myMatch[0]     
	def renrenBrower(self,url,user,password):
    #登陆页面，可以通过抓包工具分析获得，如fiddler，wireshark
	    login_page = "http://www.shaidaima.com/ajax/login"
	    try:
	        #获得一个cookieJar实例
	        cj = cookielib.CookieJar()
	        #cookieJar作为参数，获得一个opener的实例
	        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	        #伪装成一个正常的浏览器，避免有些web服务器拒绝访问。
	        opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
	        urllib2.install_opener(opener)
	        #生成Post数据，含有登陆用户名密码。
	        data = urllib.urlencode({"user_name":user,"password":password})
	        # header = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2'}
	        #以post的方法访问登陆页面，访问之后cookieJar会自定保存cookie
	          
	        opener.open(login_page,data)
	        #以带cookie的方式访问页面
	        op=opener.open(url)
	        #读取页面源码
	        data= op.read()
	        return data
	    except Exception,e:
	        print str(e)
	#访问某用户的个人主页，其实这已经实现了人人网的签到功能.
	def get(self,ID):
		if not self.get_solutionID(ID):
			return None
		soucePage=self.renrenBrower("http://www.shaidaima.com/source/view/"+self.datas['solutionID'],"itshine2014","chinajoy")
		myMatch=re.findall(u'<pre name="code" class="brush: cpp;">(.*?)</pre>',soucePage,re.S)
		# print myMatch
		# print myMatch[0]
		return unicode(myMatch[0],'utf-8')


class HTML_Tool:  
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")  
      
    EndCharToNoneRex = re.compile("<.*?>")  
  
    BgnPartRex = re.compile("<p.*?>")  
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")  
    CharToNextTabRex = re.compile("<td>")  
  
    replaceTab = [("&lt;","<"),("&gt;",">"),("&amp;","&")]  
      
    def Replace_Char(self,x):  
        # x = self.BgnCharToNoneRex.sub("",x)  
        # x = self.BgnPartRex.sub("\n    ",x)  
        # x = self.CharToNewLineRex.sub("\n",x)  
        # x = self.CharToNextTabRex.sub("\t",x)  
        # x = self.EndCharToNoneRex.sub("",x)  
  
        for t in self.replaceTab:    
            x = x.replace(t[0],t[1])    
        return x    

def indent(elem, level=0):
	    i = "\n" + level*"  "
	    if len(elem):
	        if not elem.text or not elem.text.strip():
	            elem.text = i + "  "
	        for e in elem:
	            indent(e, level+1)
	        if not e.tail or not e.tail.strip():
	            e.tail = i
	    if level and (not elem.tail or not elem.tail.strip()):
	        elem.tail = i
	    return elem

class save2xml:
	"""docstring for save2xml"""
	def __init__(self):
		self.savedata={}
		self.now=ElementTree()

	

	def data2xml(self,datas):
		self.savedata=datas
		fps=Element('fps')
		fps.attrib={'verdion':'1.2'}
		self.now._setroot(fps)
		item=SubElement(fps,'item')
		SubElement(item,'title').text=datas['title']
		time_limit=SubElement(item,'time_limit')
		time_limit.attrib={'unit':'s'}
		time_limit.text='1'
		memory_limit=SubElement(item,'memory_limit')
		memory_limit.attrib={'unit':'mb'}
		memory_limit.text='64'
		all=datas['src_num']
		print 'all of image :',all
		i=0
		print datas
		while i!=all:
			img=SubElement(item,'img')
			src=SubElement(img,'src')
			src.text=datas['src'][i]
			base64=SubElement(img,'base64')
			base64.text=datas['base64'][i]
			i=i+1

		SubElement(item,'description').text=datas['description']
		SubElement(item,'input').text=datas['input']
		SubElement(item,'output').text=datas['output']

		sample_input=SubElement(item,'sample_input')
		data=CDATA(datas['sample_input'])
		sample_input.append(data)

		sample_output=SubElement(item,'sample_output')
		data=CDATA(datas['sample_output'])
		sample_output.append(data)

		test_input=SubElement(item,'test_input')
		data=CDATA(datas['sample_input'])
		test_input.append(data)

		test_output=SubElement(item,'test_output')
		data=CDATA(datas['sample_output'])
		test_output.append(data)
		# SubElement(item,'test_input').append(CDATA(datas['sample_input']))
		# SubElement(item,'test_output').append(CDATA(datas['sample_output']))
		solution=SubElement(item,'solution')
		data=CDATA(datas['solution'])
		solution.append(data)
		solution.attrib={'language':'C++'}
		SubElement(item,'hint').text=datas['hint']
		SubElement(item,'source').text=datas['source']+'(POJ'+' '+datas['ID']+')'
		# dump(indent(fps))
		self.save(datas)

	def save(self,datas):
		self.now.write(str(datas['ID'])+'.xml','utf-8')
		print "all of work is finshed"
class poj_spider:
	def __init__(self):
		self.datas={}
		myXml=save2xml
		self.myTool=HTML_Tool()
		# self.myTool=HTML_Tool
		print u'poj_spider have start'
	def poj(self,ID):
		myPage=urllib2.urlopen('http://poj.org/problem?id='+ID).read()
		print 'read_success'
		self.datas['ID']=ID
		title=self.find_title(myPage)
		self.find_content(myPage)
		self.find_io(myPage)
		self.find_pic(myPage)
		daima=get_solution()
		if daima.get(ID)==None:
			self.datas['solution']=None
		else:
			self.datas['solution']=self.myTool.Replace_Char(daima.get(ID))
		# daima.get(ID)
		print self.datas['solution']
		myXml=save2xml()
		myXml.data2xml(self.datas)

	def find_title(self,myPage):
		myMatch=re.search(r'<div class="ptt" lang="en-US">(.*?)</div>',myPage,re.S)
		title =u'no title'
		print myMatch
		if myMatch:
			title=myMatch.group(1)
		self.datas['title']=title
		print 'Seek For Problem Title'+title
		return title
	def find_pic(self,myPage):
		print 'start find picture'
		print myPage
		myMatch=re.findall('<img src="(.*?)">',myPage,re.S)

		if(len(myMatch)==0):
			print 'nopicture'
			self.datas['src']=None
			self.datas['base64']=None
			self.datas['src_num']=0
			return
		print myMatch
		content=myMatch
		print content
		length=len(content)
		self.datas['src_num']=length
		i=0
		print 'length:',length
		# img=None
		self.datas['src']=[]
		self.datas['base64']=[]
		for Item in content:
			print 'i:',i
			if i==length:
				break
			print 'SRC of IMG is'+Item
			img=Item
			self.datas['src'].append(img)
			img_in=urllib2.urlopen('http://poj.org/%s'%img).read()
			ra=str(random.randint(1,10000))
			fp=open(ra+'.jpg','wb')
			fp.write(img_in)
			fp.close()
			fp2=open(ra+'.jpg','rb')
			ls_f=base64.b64encode(fp2.read())
			fp2.close()
			print 'Base64code of IMG is \n'+ls_f
			self.datas['base64'].append(ls_f)
			i+=1

	def find_content(self,myPage):
		myMatch=re.findall(r'<div class="ptx" lang="en-US">(.*?)</div>',myPage,re.S)
		content=myMatch#string
		for Item in content:
			print Item+'content is saved'+'\n'
		length=len(content)
		print length
		self.datas['description']=unicode(content[0],"utf-8")
		self.datas['input']=unicode(content[1],"utf-8")
		self.datas['output']=unicode(content[2],"utf-8")
		if length==5:
			self.datas['hint']=content[3]
			self.datas['source']=unicode(content[4],"utf-8")
		else:
			self.datas['hint']=None
			self.datas['source']=unicode(content[3],"utf-8")
		
	def find_io(self,myPage):
		myMatch=re.findall(r'<pre class="sio">(.*?)</pre>',myPage,re.S)
		content=myMatch
		self.datas['sample_input']=content[0]
		self.datas['sample_output']=content[1]
	
'''
<?xml version="1.0" encoding="UTF-8"?>   
<fps verdion="1.2">
<item>
<title>test1</title>
<time_limit unit="s">1</time_limit>
<memory_limit unit="mb">64</memory_limit>
<img>
<src>JdgeOnline/upload/201009/Screenshot.png</src>
<base64>iVBORw0K[BASE64_ENCODED_IMAGE_BINARY]RU5ErkJggg==</base64>
</img>
<description>
<![CDATA[print the sum of two integer<img src=JudgeOnline/upload/201009/Screenshot.png>]]>
</description>
<input>two integer a and b</input>
<output>the sum of a and b</output>
<sample_input>1 2</sample_input>
<sample_output>3</sample_output>
<test_input>
<![CDATA[2 3
]]>
</test_input>
<test_output>
<![CDATA[5
]]>
</test_output>
<hint>use scanf and printf in stdio.h</hint>
<souce>http://code.google.com/p/freeproblemset</souce>
<solution language="C++">
<![CDATA[
#include <iostream>
       using namespace std;
       int  main()
       {
       int a,b;
       cin >> a >> b;
       cout << a+b << endl;
       return 0;
       }
]]>
</solution>
<spj language="C" />
</item>
</fps>
'''
Pro=str(input('Please input ProID in POJ\n'))
test=poj_spider()
test.poj(Pro)

