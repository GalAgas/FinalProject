from typing import List
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from collections import OrderedDict

PATH_TO_WEBDRIVER = r'C:\Users\Guyzaid\PycharmProjects\pythonProject3\chromedriver_win32\chromedriver.exe'
PATH_TO_WEBSITE = r'https://www.drugs.com'


class SeleniumSearch:
    """
    Wrapper class for extracting Drug-Drug Interactions between antibiotics and patient drugs
    """
    def __init__(self):
        self.webdriver = PATH_TO_WEBDRIVER
        self.website = PATH_TO_WEBSITE
        self.user_name = "guyzaid"
        self.password = "GuyZaid1994"
        
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--disable-extensions')

    def search_drugs(self, antibiotics:dict, prev_drugs:List)->dict:
        """Main search function, web scrapes www.drugs.com for interactions between to collections of grugs

        Args:
            antibiotics (dict): possible antibiotics
            prev_drugs (List): durgs taken by the patient

        Returns:
            dict: dictinary of lists, each key is a antibiotic<->drug combination,
            each value is a list which each entery represents the number of major, moderate and minor interacions
        """
        driver = webdriver.Chrome(self.webdriver, options=self.options)
        driver.maximize_window()

        driver.get(self.website)
        assert "Drugs" in driver.title
        
        if len(antibiotics) + len(prev_drugs) > 3:
            self.register(driver)
            driver.switch_to.default_content()
        
        interaction_page_button = driver.find_element(By.LINK_TEXT, value="Interactions Checker")
        interaction_page_button.click()
        driver.switch_to.default_content()

        primary_search = driver.find_element(by=By.ID, value="livesearch-interaction-basic")
        first_drug = prev_drugs[0]
        l = (17 + 8 + 8) * (len(prev_drugs) + len(antibiotics)) + 700
        prev_drugs.remove(first_drug)

        self.search_drug(first_drug, primary_search)
        driver.switch_to.default_content()

        secondary_search = driver.find_element(by=By.ID, value="livesearch-interaction")

        for drug in prev_drugs:
            # secondary_search = driver.find_element(by=By.ID, value="livesearch-interaction")
            self.search_drug(drug, secondary_search)
            driver.switch_to.default_content()
            
        for drug in antibiotics:
            # secondary_search = driver.find_element(by=By.ID, value="livesearch-interaction")
            self.search_drug(drug, secondary_search)
            driver.switch_to.default_content()

        driver.execute_script("window.scrollTo(0," + str(l) + ")")
        time.sleep(1)
        interaction_search_button = driver.find_element(By.LINK_TEXT, value="Check for Interactions")
        interaction_search_button.click()
        
        driver.switch_to.default_content()
        time.sleep(1)
        
        # Find interactions divs
        interactions = {}
        div_wraper = driver.find_element(By.CLASS_NAME, value='interactions-reference-wrapper')
        try:
            header_divs = div_wraper.find_elements(By.CLASS_NAME, value="interactions-reference-header")
        except:
            print(interactions)
            return interactions
            
        for web_elem in header_divs:    
            p = web_elem.find_element(By.TAG_NAME, value="p")
            # print(p.text)
            options = p.text[10:].split(',')
            for anti in antibiotics:
                for prev_d in prev_drugs:
                    if anti.lower() in options[0].lower() and prev_d.lower() in options[1].lower() \
                    or  anti.lower() in options[1].lower() and prev_d.lower() in options[0].lower():
                        span = web_elem.find_element(By.TAG_NAME, value="span")
                        # print(span.text)
                        new_val = interactions.get((anti,prev_d),[0,0,0])
                        if span.text == 'Minor':
                            new_val[2] += 1
                        elif span.text == 'Moderate':
                            new_val[1] += 1
                        elif span.text == 'Major':
                            new_val[0] += 1
                        interactions[(anti,prev_d)] = new_val
                        
        for anti in antibiotics:
            for prev_d in prev_drugs:
                if (anti,prev_d) not in interactions:
                    interactions[(anti,prev_d)] = [0,0,0]

        driver.close()
        return interactions
         
    def register(self, driver):
        """
        registers to the drugs.com site for multi-input search
        Args:
            driver (WebDriver): the web driver in use currently
        """
        
        NEXT_BUTTON_XPATH = '//*[@id="header"]/div/div/div/nav[2]/a[2]'
        sign_in_button = driver.find_element(By.XPATH, value=NEXT_BUTTON_XPATH)
        sign_in_button.click()
        
        NEXT_BUTTON_XPATH = '//*[@id="content"]/div[2]/form/div[1]/label/input'
        user_name_input = driver.find_element(By.XPATH, value=NEXT_BUTTON_XPATH)
        user_name_input.clear()
        user_name_input.send_keys(self.user_name)

        NEXT_BUTTON_XPATH = '//*[@id="content"]/div[2]/form/div[2]/label/input'
        password_input = driver.find_element(By.XPATH, value=NEXT_BUTTON_XPATH)
        password_input.clear()
        password_input.send_keys(self.password)
        
        NEXT_BUTTON_XPATH = '//*[@id="content"]/div[2]/form/div[3]/input'
        sign_in_button = driver.find_element(By.XPATH, value=NEXT_BUTTON_XPATH)
        sign_in_button.click()
        
        time.sleep(2)

    def search_drug(self, drug_name, search_elem):
        """
        enters each drug to the system
        """
        search_elem.clear()
        search_elem.send_keys(drug_name)
        print(drug_name)
        search_elem.send_keys(Keys.RETURN)
        time.sleep(1)

def sort_interactions(d: dict) -> dict:
    return {k:d[k] for k in sorted(d, key= lambda k:(d[k][0],d[k][1],d[k][2]), reverse=False)}


