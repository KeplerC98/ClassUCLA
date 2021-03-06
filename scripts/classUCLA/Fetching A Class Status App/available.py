#! /usr/bin/python

import requests
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText
from email.header import Header

TERM = '17F'
CLASS_ID = ['262660200', '262660210', '262344200', '186811200']

def getOpenSeats(index):
    URL = 'https://sa.ucla.edu/ro/public/soc/Results?t='+TERM+'&sBy=classidnumber&id='+index+'&undefined=Go&btnIsInIndex=btn_inIndex'
    try:
        r = requests.get(URL)
    except:
        print("Check your input")

    try:
        soup = BeautifulSoup(r.text, 'html.parser')
    except:
        print("parser failed")

    #string processing    
    text = soup.find_all('p') #find all tags
    flag = -1
    printed = False #a flag for printing class names
    ostream = ""
    for i in range(len(text)):
        string = str(text[i])
        #print(string)
        if flag != -1:
            #print(string)
            #message parsers
            try:
                loc1 = string.find("</i>")+4
                loc2 = string.find("<br/>")
                loc3 = string.find("</p>")
            except:
                print("cannot parse the website")
            #output stream
            if loc2 == -1: #class is cancelled
                ostream+=" is cancelled \n"
            else:
                msg1 = string[loc1: loc2]
                msg2 = string[loc2+5: loc3]
                ostream+=" is " + msg1
                ostream+=". Its status is "+msg2+"\n"
            flag = -1
        if string.find("Lec") != -1:
            #print(string)
            i+=1        #jump two lines
            flag = 0    #found it
        if string.find("Dis") != -1 and len(string) > 200:
            #print(string)
            i+=1        #jump two lines
            flag = 1    #found it
        if flag != -1 and printed == False:
            printed = True
            try:
                loc1 = string.find("subj_area_cd=") + 13 #class title
                loc2 = string.find("%20")
                loc3 = string.find("catlg_no=") + 10  #class number
                loc4 = string.find("%20", loc3) #find next after loc3
            except:
                print("cannot parse the website")
            
            ostream += string[loc1 : loc2]
            ostream += " "
            if string[loc3] == '0':
                loc3 += 1
            ostream += string[loc3 : loc4]
            ostream += '\n'
        if flag != -1:
            loc1 = string.find("</a>")
            loc2 = loc1 - 6         
            if(string[loc2] == '>'):
                loc2 += 1
            msg = string[loc2 : loc1]
            
            ostream += string [loc2 : loc1]
    return ostream 

mail_host="smtp.mailgun.org"
mail_user="postmaster@sandbox771d908665d24655b9cd402f4ece3dc8.mailgun.org"   
mail_pass="bfce1771c370570883fd229be0f3638a"
receivers = ['chenkaiyuan@ucla.edu'] 

def sendEmail(content):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("UCLA Class Assistant", 'utf-8')
    message['To'] =  Header("Kaiyuan Chen", 'utf-8')
    message['Subject'] = Header("class update", 'utf-8')
    try:
        sender = 'chenkaiyuan@ucla.edu'
        smtpObj = smtplib.SMTP('smtp.mailgun.org', 587)
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print "success"
    except:
        print "failed"
        
if __name__ == '__main__':
    ostream='''Dear, 
Please find class information below
'''
    ostream=''
    for ID in CLASS_ID:
        ostream+=getOpenSeats(ID)
    ostream+='''
Best Regards,
Kaiyuan Chen and his class assistant'''
    print ostream
    sendEmail(ostream)

