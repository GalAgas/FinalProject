from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

PATH_TO_WEBDRIVER = r'C:\Users\Guyzaid\PycharmProjects\pythonProject3\chromedriver_win32\chromedriver.exe'
PATH_TO_WEBSITE = r'https://www.drugs.com'


class SeleniumSearch:
    def __init__(self):
        self.webdriver = PATH_TO_WEBDRIVER
        self.website = PATH_TO_WEBSITE

    def search_drugs(self, drugs):
        driver = webdriver.Chrome(self.webdriver)
        driver.maximize_window()

        driver.get(self.website)
        assert "Drugs" in driver.title

        interaction_page_button = driver.find_element(By.LINK_TEXT, value="Interactions Checker")
        interaction_page_button.click()
        driver.switch_to.default_content()

        primary_search = driver.find_element(by=By.ID, value="livesearch-interaction-basic")
        first_drug = drugs[0]
        l = (17 + 8 + 8) * (len(drugs) + 1) + 200
        drugs.remove(first_drug)

        search_drug(first_drug, primary_search)

        secondary_search = driver.find_element(by=By.ID, value="livesearch-interaction")
        driver.switch_to.default_content()

        driver.execute_script("window.scrollTo(0," + str(l) + ")")

        for drug in drugs:
            search_drug(drug, secondary_search)


        # driver.execute_script("window.scrollTo(0," + str(l) + ")")
        time.sleep(1)
        interaction_search_button = driver.find_element(By.LINK_TEXT, value="Check for Interactions")
        interaction_search_button.click()
        driver.switch_to.default_content()
        time.sleep(1)

        form = driver.find_element(By.ID, value="filterSection")

        print(form.text)

        driver.close()


def search_drug(drug_name, search_elem):
    search_elem.clear()
    search_elem.send_keys(drug_name)
    search_elem.send_keys(Keys.RETURN)
    time.sleep(0.5)


# def test_selenium():
#     driver = webdriver.Chrome(r'C:\Users\Guyzaid\PycharmProjects\pythonProject3\chromedriver_win32\chromedriver.exe')
#     # driver = webdriver.Chrome()
#     driver.get("http://www.python.org")
#     assert "Python" in driver.title
#     # elem = driver.find_element_by_name("q")
#     elem = driver.find_element(by=By.NAME, value="q")
#     elem.clear()
#     elem.send_keys("pycon")
#     elem.send_keys(Keys.RETURN)
#     assert "No results found." not in driver.page_source
#     driver.close()
#
# def main():
#     driver = webdriver.Chrome(PATH_TO_WEBDRIVER)
#     driver.maximize_window()
#
#     driver.get(PATH_TO_WEBSITE)
#     assert "Drugs" in driver.title
#
#     interaction_page_button = driver.find_element(By.LINK_TEXT, value="Interactions Checker")
#     interaction_page_button.click()
#     driver.switch_to.default_content()
#
#     primary_search = driver.find_element(by=By.ID, value="livesearch-interaction-basic")
#     search_drug("Abilify", primary_search)
#
#     secondary_search = driver.find_element(by=By.ID, value="livesearch-interaction")
#     driver.switch_to.default_content()
#
#     search_drug("Ativan", secondary_search)
#     driver.switch_to.default_content()
#     search_drug("Advil", secondary_search)
#     driver.switch_to.default_content()
#
#     interaction_search_button = driver.find_element(By.LINK_TEXT, value="Check for Interactions")
#     interaction_search_button.click()
#     driver.switch_to.default_content()
#
#     form = driver.find_element(By.ID, value="filterSection")
#
#     print(form.text)
#
#     driver.close()


if __name__ == '__main__':
    # main()
    ss = SeleniumSearch()
    ss.search_drugs(['Abilify', 'Ativan', 'Advil'])

# no interactions drugs - cefazolin, ampicillin, cefoxitin
# no interactions drugs - Abilify, Ativan, Advil
