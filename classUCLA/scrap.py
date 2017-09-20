#! /usr/bin/python

import requests
from bs4 import BeautifulSoup

TERM = '17F'

# Get web page and build a soup
def get_web_page(URL):    
    try:
        r = requests.get(URL)
    except:
        print("check your input")
        
    try:
        soup = BeautifulSoup(r.text, 'html.parser')
    except:
        print("parser failed")
    return soup

# get URL for detailed website
def get_class_info_basic(index):
    #initialize variables
    URL = 'https://sa.ucla.edu/ro/public/soc/Results?t='+TERM+'&sBy=classidnumber&id='+index+'&undefined=Go&btnIsInIndex=btn_inIndex'
    soup = get_web_page(URL)
    text = str(soup.find_all('p')) #find all tags
    loc1 = text.find("n<a href=\"") + 10
    loc2 = text.find("20\" target=") + 2
    string = "https://sa.ucla.edu" + text[loc1:loc2]
    string = string.replace("amp;", "")
    return string

''' order: 0subject, 1course number, 2title, 3website, 4status, 5waitlist status, 6days, 7time, 8location, 9units, 10instructor, 11final_exam_day, 12final_exam_weekday, 13final_exam_time, 14final_exam_avail, 15grade_type, 16restriction, 17impacted, 18individual studies, 19level, 20 requisite //TODO, 21course description, 22class description, 23GE requirement, 24writingII requirement, 25diversity requirement, 26class notes
'''

#extract features
import pandas as pd
def get_class_info_detailed(URL):
    soup = get_web_page(URL)
    text = str(soup.find_all('p')) #find all tags
    info = []
    
    print text
    
def main():
    #URL = get_class_info_basic("262660200")
    #print URL
    get_class_info_detailed("https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=17F&subj_area_cd=MATH%20%20%20&crs_catlg_no=0170A%20%20%20&class_id=262660210&class_no=%20002%20%20")

if __name__ == "__main__":
    main()
