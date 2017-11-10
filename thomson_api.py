import json
import time
from xml.dom import minidom
from datetime import datetime
import requests# $ pip install requests
from requests.auth import HTTPDigestAuth
from config import *


##############################################################################
#                                                                            #
#------------------------------------THOMSON---------------------------------#
#                                                                            #
##############################################################################

class Thomson:
    def __init__(self):
        self.user = USER
        self.passwd = PASSWD
        self.url = URL

    def get_response(self, headers, body):
        response = requests.post(self.url, data=body, headers=headers, \
            auth=HTTPDigestAuth(self.user, self.passwd))
        #print response.content
        response_xml = response.content[response.content.find('<soapenv:Envelope') :\
         response.content.find('</soapenv:Envelope>') + len('</soapenv:Envelope>')]
        return response_xml

##############################################################################
#                                                                            #
#-----------------------------------JOBDETAIL--------------------------------#
#                                                                            #
##############################################################################

class JobDetail:
    def __init__(self, jid):
        self.jid = jid

    def parse_status(self, xml):
        result = 'NotOK'
        try:
            xmldoc = minidom.parseString(xml)
            if xmldoc.getElementsByTagName('mg:RspNotOK'):
                message = xmldoc.getElementsByTagName('mg:RspNotOK')
                result = message[0].attributes['Desc'].value \
                 if "'Desc'" in str(message[0].attributes.items()) else result
            elif xmldoc.getElementsByTagName('mg:RspDone'):
                result = 'OK'
        except Exception as e:
            print e
            result = 'Unknow'
        return result

    def start(self):
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'SOAPAction': 'JobStart'
        }

        body ="""<soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:job="JobStart">
              <soapenv:Body>
                <job:JobStartReq Cmd="Start" OpV="01.00.00" JId="%s"/>
              </soapenv:Body>
            </soapenv:Envelope>"""%(self.jid)
        #response_xml = Thomson().get_response(headers, body)
        response_xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Body>
               <jStart:JobStartRsp xmlns:mg="MalteseGlobal" xmlns:jStart="JobStart" OpV="01.00.00">
                       <mg:RspDone />
               </jStart:JobStartRsp>
        </soapenv:Body>
        </soapenv:Envelope>"""
        #print response_xml
        return self.parse_status(response_xml)

    def abort(self):
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'SOAPAction': 'JobAbort'
        }

        body ="""<soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:job="JobAbort">
              <soapenv:Body>
                <job:JobAbortReq Cmd="Start" OpV="01.00.00" JId="%s"/>
              </soapenv:Body>
            </soapenv:Envelope>"""%(self.jid)
        response_xml = Thomson().get_response(headers, body)
        print response_xml
        return self.parse_status(response_xml)

    def send_action(self, action):
        if action == 'start':
            return self.start()
        elif action == 'stop':
            return self.abort()
        else:
            return 'Option %s not specified' % action
        

#JobDetail('13429').start()
#JobDetail('13429').abort()
