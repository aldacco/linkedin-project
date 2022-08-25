import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re
#NOMBRE
#EXPERIENCE
#EDUCATION
#SKILLS
#LICENSES & CERTIFICATIONS
#COURSES

def chrome(headless=False):
    d = webdriver.DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_argument("--disable-popup-blocking")
    browser = webdriver.Chrome(executable_path=r'/home/aldaco/Downloads/chromedriver', options=opt,desired_capabilities=d)
    browser.implicitly_wait(10)
    return browser

def scroll_down_page(speed=8):
    current_scroll_position, new_height= 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = browser.execute_script("return document.body.scrollHeight")

def load_page(link, route):
    new_link = f"{link}/details/{route}"
    # print(new_link)
    browser.get(new_link)
    browser.implicitly_wait(1)
    scroll_down_page(speed=3)
    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')
    return soup

## Pass True if you want to hide chrome browser
browser = chrome(False)
try:
    browser.get('https://www.linkedin.com/')
    browser.implicitly_wait(3)

    browser.get('https://www.linkedin.com/uas/login')
    browser.implicitly_wait(3)
    file = open('config.txt')
    lines = file.readlines()
    username = lines[0]
    password = lines[1]

    elementID = browser.find_element(By.ID, 'username')
    elementID.send_keys(username)
    elementID = browser.find_element(By.ID, 'password')
    elementID.send_keys(password)
    elementID.submit()
except:
    n = 0
    
input("Press Enter to continue...")

file = open('links.csv')
links = file.readlines()
i = 0
routes = ['experience','education', 'certifications', 'skills', 'courses', 'languages']
DATA = []
for link in links:
    root_link = link.rstrip('\n')
    link = link.rstrip('\n')

    name = ""
    contacts = ""
    experience = []
    education = []
    certifications = []
    skills = []
    courses = []
    languages = []
    

    try:
        browser.get(link)
        browser.implicitly_wait(1)
        scroll_down_page(speed=3)
        src = browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        section = soup.find('section', {'class': 'artdeco-card ember-view pv-top-card'})
        name = span = section.find('h1').get_text().strip()
        contacts = section.find('li', {'class': 'text-body-small'}).find('span', {'class': 't-bold'}).get_text().strip()
        # li = section.find_all('li', {'class': 'pv-text-details__right-panel-item'})
    except:
        name = ""
        contacts = ""

    #experience 
    try:
        soup = load_page(link, routes[0])    
        li = soup.find_all('li', {'class': 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})
        for element in li:
            span = element.find('span', {'class': re.compile(r'^mr1.*.t-bold$')}).find('span', {'class': 'visually-hidden'})
            # print(span.get_text().strip())
            experience.append(span.get_text().strip())
            if len(experience) > 10:
                break
    except:
        experience = []


    try:
        soup = load_page(link, routes[1])    
        li = soup.find_all('li', {'class': 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})
        for element in li:
            span = element.find('span', {'class': re.compile(r'^mr1.*.t-bold$')}).find('span', {'class': 'visually-hidden'})
            # print(span.get_text().strip())
            education.append(span.get_text().strip())
            if len(education) > 10:
                break
    except:
        education = []


    try: 
        soup = load_page(link, routes[2])    
        li = soup.find_all('li', {'class': 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})
        for element in li:
            span = element.find('span', {'class': re.compile(r'^mr1.*.t-bold$')}).find('span', {'class': 'visually-hidden'})
            # print(span.get_text().strip())
            certifications.append(span.get_text().strip())
            if len(certifications) > 10:
                break
    except:
        certifications = []


    try: 
        soup = load_page(link, routes[3])    
        li = soup.find_all('li', {'class': 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})
        for element in li:
            span = element.find('span', {'class': re.compile(r'^mr1.*.t-bold$')}).find('span', {'class': 'visually-hidden'})
            # print(span.get_text().strip())
            skills.append(span.get_text().strip())
            if len(skills) > 10:
                break
    except:
        skills = []

    try: 
        soup = load_page(link, routes[4])    
        li = soup.find_all('li', {'class': 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})
        for element in li:
            span = element.find('span', {'class': re.compile(r'^mr1.*.t-bold$')}).find('span', {'class': 'visually-hidden'})
            # print(span.get_text().strip())
            courses.append(span.get_text().strip())
            if len(courses) > 10:
                break
    except:
        courses = []


    try: 
        soup = load_page(link, routes[5])    
        li = soup.find_all('li', {'class': 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})
        for element in li:
            span = element.find('span', {'class': re.compile(r'^mr1.*.t-bold$')}).find('span', {'class': 'visually-hidden'})
            # print(span.get_text().strip())
            languages.append(span.get_text().strip())
    except:
        languages = ['Español']


    df = pd.DataFrame([name, contacts, root_link, experience, education, certifications, skills, courses, languages])
    df1.to_csv('output.csv', index=None, mode="a", header=not os.path.isfile(path))
    i += 1
    print(f'perfil nro {i}')
