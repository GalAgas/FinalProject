from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
import time
from collections import OrderedDict

PATH_TO_WEBDRIVER = r'C:\Users\Guyzaid\PycharmProjects\pythonProject3\chromedriver_win32\chromedriver.exe'
PATH_TO_WEBSITE = r'https://www.drugs.com'


class SeleniumSearch:
    def __init__(self):
        self.webdriver = PATH_TO_WEBDRIVER
        self.website = PATH_TO_WEBSITE
        self.user_name = "guyzaid"
        self.password = "GuyZaid1994"
        
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--disable-extensions')
        # self.options.add_argument('--headless')

    def search_drugs(self, antibiotics, prev_drugs):
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
        l = (17 + 8 + 8) * (len(prev_drugs) + len(antibiotics)) + 400
        prev_drugs.remove(first_drug)

        self.search_drug(first_drug, primary_search)
        driver.switch_to.default_content()

        secondary_search = driver.find_element(by=By.ID, value="livesearch-interaction")

        for drug in prev_drugs:
            self.search_drug(drug, secondary_search)
            
        for drug in antibiotics:
            self.search_drug(drug, secondary_search)

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
                        new_val = interactions.get(anti,[0,0,0])
                        if span.text == 'Minor':
                            new_val[2] += 1
                        elif span.text == 'Moderate':
                            new_val[1] += 1
                        elif span.text == 'Major':
                            new_val[0] += 1
                        interactions[anti] = new_val
                        
        for anti in antibiotics:
            if anti not in interactions:
                interactions[anti] = [0,0,0]

        driver.close()
        return interactions
        
    
    def register(self, driver):
        
        NEXT_BUTTON_XPATH = '//*[@id="header"]/div/div/div/nav[2]/a[2]'
        sign_in_button = driver.find_element(By.XPATH, value=NEXT_BUTTON_XPATH)
        # print(sign_in_button)
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
        search_elem.clear()
        search_elem.send_keys(drug_name)
        search_elem.send_keys(Keys.RETURN)
        time.sleep(0.5)

def sort_interactions(d: dict) -> dict:
    return {k:d[k] for k in sorted(d, key= lambda k:(d[k][0],d[k][1],d[k][2]), reverse=False)}

if __name__ == '__main__':
    prev = ['Abilify', 'Ativan', 'Advil', 'Lasix', 'Aspirin']
    # prev = ['Abilify']
    anti = ['gentamicin', 'levofloxacin']
    # anti = ['gentamicin']
    # ss = SeleniumSearch()
    # d = ss.search_drugs(anti, prev)
    d = {'gentamicin': [1, 2, 0], 'levofloxacin': [0, 2, 0], 'x': [0,0,0]}
    print(d)
    d2 = sort_interactions(d)
    print(d2)

# no interactions drugs - cefazolin, ampicillin, cefoxitin
# no interactions drugs - Abilify, Ativan, Advil


# {
#     'z':[1,0,0],
#     'y':[0,1,0],
#     'x':[0,0,1],
# }

# {
#     'a':[0,0,0],
#     'x':[0,0,1],
#     'q':[0,0,2],
#     'y':[0,1,0],
#     'w':[0,2,0],
#     'z':[1,0,0],
# }
