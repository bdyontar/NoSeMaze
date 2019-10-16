# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 10:45:56 2018

@author: jir-mb
"""

from email.message import EmailMessage
import smtplib
import traceback
import os
import time

def crash_error(exctype, value, tb):
    subject = "Software has crashed"
    error = "".join(traceback.format_exception(exctype,value,tb))
    filename = os.getcwd()+'\\HelperFunctions\\Email\\crash_error.txt'
    with open(filename, encoding='utf-8') as f: content = f.read()    
    content = content.format(name='{name}',error=error)
    attachment = None
    send(subject, content, attachment)
    
def connection_error():
    subject = "Cannot connect to RFID Decoder"
    filename = os.getcwed()+'\\HelperFunctions\\Email\\connection_error.txt'
    with open(filename, encoding='utf-8') as f: content = f.read()
    attachment = None
    send(subject, content, attachment)
    
def log_reports(dates, start, logspath, logs):
    logs.sort()
    logs = logs[-3:]
    subject = "Log Reports" + dates[0] + " and " + dates[1]
    filename = os.getcwd()+'\\HelperFunctions\\Email\\logs_report.txt'
    with open(filename, encoding='utf-8') as f: content = f.read()
    content = content.format(name='{name}', start=start.split('.')[0].replace('T',', '), logs=logs)
    attachment = list()
    for date in dates:
        fn = logspath+"\\LOG_"+date+".csv"
        if os.path.isfile(fn):
            with open(fn,'r') as f: log = f.readlines()
            attachment.append(dict(log="".join(log), name="LOG_"+date+".csv"))
        else:
            attachment.append(dict(log="There is no activity today.",name = "LOG_"+date+".csv"))
    send(subject, content, attachment)

def send(subject, content, attachment):
    filename = os.getcwd()+'\\HelperFunctions\\Email\\mailing_list.txt'
    with open(filename,encoding='utf-8') as f:
        mlist = f.readlines()
        for i,item in enumerate(mlist):
            mlist[i] = item.strip("\n")
    
    msg = list()
    for i, email in enumerate(mlist):
        name = email.split(".")[0].capitalize()
        msg.append(EmailMessage())
        msg[i]['From'] = "RFID.Tracking.Server@zi-mannheim.de"
        msg[i]['Subject'] = subject
        msg[i]['To'] = email
        msg[i].set_content(content.format(name=name))
        if attachment is not None: 
            for att in attachment:
                msg[i].add_attachment(att['log'], subtype ='txt', filename = att['name']) 
    
    try:        
        with smtplib.SMTP('smtp.zi.local') as server:
            server.starttls()
            print('\nsending email: start tls')
            for i in range(len(msg)): 
                print('sending email: sending message...')
                server.send_message(msg[i])
                print('sending email: {} message(s) sent'.format(i+1))
                time.sleep(0.05)     
            print('all message(s) sent')
    except:
        print('mail cannot be sent')

    