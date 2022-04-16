
import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest
import time
from html.parser import HTMLParser
from multiprocessing import Pool
from requests.exceptions import RequestException
from requests import Session
from requests.auth import HTTPBasicAuth
from requests_html import HTMLSession

# empty lists
job_title1 = []
company_name1 = []
location1 = []
job_skill1 = []
job_requirement1 = []
job_description1 = []
links = []
post_date1 = []
page_num = 0
##########


def go(d1):
    print(f"sarting in page {page_num}")
    d1 = f'https://wuzzuf.net/search/jobs/?a=hpb&q=sales&start={page_num}'
    print(d1)
    method = HTMLSession()

    results = method.get(d1, timeout=5)
    source = results.content

    ##########

    soup = BeautifulSoup(source, "lxml")

    ##########

    job_title = soup.find_all("h2", {"class": "css-m604qf"})
    company_name = soup.find_all("a", {"class": "css-17s97q8"})
    location = soup.find_all("span", {"class": "css-5wys0k"})
    job_skill = soup.find_all("div", {"class": "css-y4udm8"})
    post_date = soup.find_all("div", {"class": "css-4c4ojb"})

    ##########

    def into_text(x, y):
        for i in range(len(x)):
            y.append(x[i].text)

    into_text(job_title, job_title1)
    into_text(company_name, company_name1)
    into_text(location, location1)
    into_text(job_skill, job_skill1)
    into_text(post_date, post_date1)

    for z in range(len(job_title)):
        links.append(job_title[z].find("a").attrs["href"])
        links[z] = "https://wuzzuf.net" + links[z]

    # links per link
    # for link in links:
    #     result = requests.get(link)
    #     src = result.content
    #     soup = BeautifulSoup(src, "lxml")
    #     job_requirement = soup.find_all("div", {"class": "css-1t5f0fr"})
    #     into_text(job_requirement, job_requirement1)
    #     job_description = soup.find_all("div", {"class": "css-1uobp1k"})
    #     into_text(job_description, job_description1)
    #     #job_description1 = job_description1.text+"||"

    # filtering charcaters
    company_name1 = [q.replace("-", "") for q in company_name1]
    job_skill1 = [any.replace("-", "||") for any in job_skill1]
    job_requirement1 = [any.splitlines() for any in job_requirement1]
    job_description1 = [any.splitlines() for any in job_description1]
    #########
    file_list = [job_title1, post_date1, company_name1, location1,
                 job_skill1, job_description1, job_requirement1, links]
    exported_file_list = list(zip_longest(*file_list))

    with open("/Users/Matrix10/Downloads/Projects/1files/webscarping.csv", "w") as my_file:
        wr = csv.writer(my_file)
        wr.writerow(["Job Title", "Date", "Company", "Location", "Job Skills",
                     "Job Description", "Job Requirement", "Links"])
        wr.writerows(exported_file_list)

    with open("/Users/Matrix10/Downloads/Projects/1files/webscarping.csv", newline='') as in_file:
        with open("/Users/Matrix10/Downloads/Projects/1files/webscarping2.csv", 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if any(row):
                    writer.writerow(row)


###########
