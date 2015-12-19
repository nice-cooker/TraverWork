#!/usr/bin/env python

#-*-coding: UTF-8-*-

import web
import MySQLdb
import json 
import logging
import base64 
import sys
import time

urls = (
    '/airticket.cgi', 'AirTicket',
    '/pickservice.cgi', 'PickService'
    '/channel.cgi', 'Channel'
    '/channelrelation.cgi', 'ChannelRelation'
)
reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='debug.log', filemode='w+')

db_info = {'dbn':'mysql', 'user':'root', 'pw':'', 'db':'db_traver_price'}

class AirTicketDB:
    def __init__(self):
        self.db = web.database(**db_info)

    def addTicket(self, ticket_num, ticket_info):
        #logging.debug(ticket_info)
        return self.db.query('replace t_air_ticket (ticket_num, ticket_info) values (' +  MySQLdb.escape_string(ticket_num) + ',"' + MySQLdb.escape_string(ticket_info) + '")')

    def delTicket(self, ticket_num):
        return self.db.query('delete from t_air_ticket where ticket_num=' +  MySQLdb.escape_string(ticket_num))
    
    def getTicket(self):
        return self.db.query('select ticket_info from t_air_ticket where UNIX_TIMESTAMP(LASTTIME)>=' +  str(time.time() - 356*86400))

class AirTicket:
    def GET(self):
        return self.POST() 

    def POST(self):
        ticket_data = web.input()

        if (not any(ticket_data)):
            return json.dumps(dict(ret=-1, msg='input empty'))
        try:
            air_ticket_db = AirTicketDB();      
            if (ticket_data.op == "insert" or ticket_data.op == "update"):
                ret = air_ticket_db.addTicket(ticket_data.ticket_num, ticket_data.ticket_info)
                if (ret == 1 or ret == 2):
                    return json.dumps(dict(ret=0, msg='ok'))
                else:
                    return json.dumps(dict(ret=1, msg='err'))
            elif (ticket_data.op == "delete"):
                ret = air_ticket_db.delTicket(ticket_data.ticket_num)
                if (ret >= 0):
                    return json.dumps(dict(ret=0, msg='ok'))
                else:
                    return json.dumps(dict(ret=1, msg='err'))
            elif (ticket_data.op == 'load'):
                return json.dumps(list(air_ticket_db.getTicket()))
                 
        except (Exception) as e:
            return json.dumps(dict(ret=-1,msg=str(e)))

class PickServiceDB:
    def __init__(self):
        self.db = web.database(**db_info)

    def addService(self, service_num, service_info):
        return self.db.query('replace t_pick_service (service_num, service_info) values (' +  MySQLdb.escape_string(service_num) + ',"' + MySQLdb.escape_string(service_info) + '")')

    def delService(self, service_num):
        return self.db.query('delete from t_pick_service where service_num=' +  MySQLdb.escape_string(service_num))

    def getService(self):
        return self.db.query('select service_info from t_pick_service where LASTTIME>=' +  str(time.time() - 356*86400))


class PickService:
    def GET(self):
        return self.POST() 

    def POST(self):
        service_data = web.input()

        if (not any(service_data)):
            return json.dumps(dict(ret=-1, msg='input empty'))
        try:
            pick_service_db = PickServiceDB()    
            if (service_data.op == "insert" or service_data.op == "update"):
                ret = pick_service_db.addService(service_data.service_num, service_data.service_info)   
                if (ret == 1 or ret == 2):
                    return json.dumps(dict(ret=0, msg='ok'))
                else:
                    return json.dumps(dict(ret=1, msg='err'))
            elif (service_data.op == "delete"):
                ret = air_ticket_db.delService(service_data.service_num)
                if (ret >= 0):
                    return json.dumps(dict(ret=0, msg='ok'))
                else:
                    return json.dumps(dict(ret=1, msg='err'))
            elif (service_data.op == "load"):
                return json.dumps(list(pick_service_db.getService()))
        except (Exception) as e:
            return json.dumps(dict(ret=-1,msg=str(e)))

class ChannelDB:
    def __init__(self):
        self.db = web.database(**db_info)

    def addChannel(self, channel_name,  channel_info):
        return self.db.query('replace t_channel(channel_name, channel_info) values ("' +  MySQLdb.escape_string(channel_name) + '","' + MySQLdb.escape_string(channel_info) + '")')

    def delChannel(self, channel_name):
        return self.db.query('delete from t_channel where channel_name="' +  MySQLdb.escape_string(channel_name) + '"')

    def getChannel(self):
        return self.db.query('select channel_info from t_channel where LASTTIME>=' +  str(time.time() - 356*86400))

class Channel:
    def GET(self):
        return self.POST() 

    def POST(self):
        channel_data = web.input()

        if (not any(channel_data)):
            return json.dumps(dict(ret=-1, msg='input empty'))
        try:
            channel_db = ChannelDB()    
            if (channel_data.op == "insert" or channel_data.op == "update"):
                ret = channel_db.addChannel(channel_data.channel_name, channel_data.channel_info)   
                if (ret == 1 or ret == 2):
                    return json.dumps(dict(ret=0, msg='ok'))
                else:
                    return json.dumps(dict(ret=1, msg='err'))
            elif (channel_data.op == "delete"):
                ret = channel_db.delChannel(channel_data.channel_name)
                if (ret >= 0):
                    return json.dumps(dict(ret=0, msg='ok'))
                else:
                    return json.dumps(dict(ret=1, msg='err'))
            elif (channel_data.op == "load"):
                return json.dumps(list(channel_db.getChannel()))
        except (Exception) as e:
            return json.dumps(dict(ret=-1,msg=str(e)))

class ChannelRelationDB:
    def __init__(self):
        self.db = web.database(**db_info)

    def addChannelRelation(self, channel_name,  product_id, channel_relation_info):
        return self.db.query('replace t_channel_relation(channel_name, shop_product_id, channel_relation_info) values ("' +  MySQLdb.escape_string(channel_name) + '",' + MySQLdb.escape_string(product_id) + ',"' + MySQLdb.escape_string(channel_relation_info) + '")')

    def delChannelRelation(self, channel_name, product_id):
        return self.db.query('delete from t_channel_relation where channel_name="' +  MySQLdb.escape_string(channel_name) + '", and shop_procuct_id=' + product_id)

    def getChannelRelation(self):
        return self.db.query('select channel_relation_info from t_channel_relation where LASTTIME>=' +  str(time.time() - 356*86400))

class ChannelRelation:
    def GET(self):
        return self.POST() 

    def POST(self):
        data = web.input()

        if (not any(data)):
            return json.dumps(dict(ret=-1, msg='input empty'))
        try:
            channel_relation_db = ChannelRelationDB()    
            if (data.op == "insert" or data.op == "update"):
                ret = channel_relation_db.addChannelRelation(data.channel_name, data.product_id, data.channel_relation_info)   
                if (ret == 1 or ret == 2):
                    return json.dumps(dict(ret=0, msg='ok'))
                else:
                    return json.dumps(dict(ret=1, msg='err'))
            elif (data.op == "delete"):
                ret = channel_relation_db.delChannelRelation(data.channel_name, data.product_id)
                if (ret >= 0):
                    return json.dumps(dict(ret=0, msg='ok'))
                else:
                    return json.dumps(dict(ret=1, msg='err'))
            elif (data.op == "load"):
                return json.dumps(list(channel_relation_db.getChannelRelation()))
        except (Exception) as e:
            return json.dumps(dict(ret=-1,msg=str(e)))

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
