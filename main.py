#!/usr/bin/python
import time
import os
import datetime
from available_spot import *
import subprocess
from sms import *
from management import *
import time

def get_ostream(data, empty_send = False):
    should_send = False
    ostream='Hey, your class is ready\n'
    print(data["name"])
    for ID in data["list"]:
        stream = getOpenSeats(ID)
        if(stream == None or stream == ""):
            continue
        else:
            k = stream.split("\n")
            stream = k[0] + "\n" + k[1] + "\n"
            if(stream.find("Full") != -1 or stream.find("Closed") != -1):
                print(stream)
                continue
            for i in k[2:]:
                if(i.find("Open") != -1):
                   stream += i
                   stream += "\n"
            ostream+= stream
            should_send = True
            class_remove(data["name"], ID)
            ostream+='''Kepler :)'''
    return ostream, should_send
    
def send_to(data, mean = "sms"):
    ostream, should_send = get_ostream(data)
    if(should_send):
        sendEmail(ostream, "")
        send_sms(ostream, data["phone"])
    else:
        print("Full")
        print(time.asctime(time.localtime(time.time())))
        log_file = open("./log.txt", 'a')
        log_file.write(time.asctime(time.localtime(time.time())))
        log_file.write("  FULL\n")
        log_file.write(data["name"] + str(data["list"]) + "\n")
        log_file.close()    

def process():
    with open ('/u/cs/ugrad/kaiyuanc/scratch/data/index.json') as data_file:
        data = json.load(data_file)
        names = data['list']
        
    for name in names:
        path = '/u/cs/ugrad/kaiyuanc/scratch/data/' + name + '.json'
        with open(path) as data_file:
            data = json.load(data_file)
            send_to(data)
    time_stamp = "{} : {}\n".format(os.getpid(), str(datetime.datetime.now()))
    with open("/u/cs/ugrad/kaiyuanc/scratch/ClassUCLA/log.txt", "a") as log:
        log.write(time_stamp)
        log.close()

from random import randrange
def main():
    counter = 0
    while True:
        process()
        time.sleep(3600)
        counter += 1
        if(counter == 10):
            child =subprocess.call(['./script.sh'])
            print(child)
            if(child == 0):
                time.sleep(randrange(0, 1000))


if __name__ == "__main__":
    main()
