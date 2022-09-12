import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class KdpBrowser:
    '''docstring for KdpBrowser'''
    def __init__(self, login, pw, headless=False):
        self.login = login
        self.password = pw
        self.headless = headless

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, ex_type, ex_val, ex_tb):
        self.close()

    def wait_for(self, elem_id, ty=By.ID, timeout=10):
        elem = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((ty, elem_id))
        )
        return elem

    def write_to_field(self, value, field_id, ty=By.ID):
        field = self.driver.find_element(ty, field_id)
        field.clear()
        field.send_keys(value)
        return field

    def connect(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-extensions')
            # chrome_options.add_argument('--disable-gpu')
            # chrome_options.add_argument('--no-sandbox') # linux only
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://kdp.amazon.com/fr_FR/bookshelf')
        
        login_field = self.wait_for('ap_email')
        login_field.clear()
        login_field.send_keys(self.login)

        pw_field = self.write_to_field(self.password, 'ap_password')
        pw_field.send_keys(Keys.RETURN)

    def upload(self, book):
        self.driver.get('https://kdp.amazon.com/fr_FR/bookshelf')
        create_btn = self.wait_for('Créer', By.PARTIAL_LINK_TEXT)
        create_btn.click()

        broche_btn = self.wait_for('(//button)[2]', By.XPATH)
        broche_btn.click()

        # First fields page
        title_field = self.wait_for('data-print-book-title')
        title_field.send_keys(book['title'])

        if 'subtitle' in book:
            self.write_to_field(book['subtitle'], 'data-print-book-subtitle')

        firstname, lastname = book['author']
        self.write_to_field(firstname, 'data-print-book-primary-author-first-name')
        self.write_to_field(lastname, 'data-print-book-primary-author-last-name')

        # The description field lies inside another page that is displayed within an iframe
        # thus we need to switch to that frame, and then switch back out.
        # ref : https://stackoverflow.com/questions/7534622/select-iframe-using-python-selenium
        frame = self.driver.find_element(By.TAG_NAME, 'iframe')
        self.driver.switch_to.frame(frame)
        body = self.write_to_field(book['description'], 'body', By.TAG_NAME)
        self.driver.switch_to.default_content()

        radio_btn = self.driver.find_element(By.ID, 'non-public-domain')
        radio_btn.click()

        ### Keywords
        # Up to 7 keywords are allowed
        if 'keywords' not in book:
            book['keywords'] = []
        assert len(book['keywords']) <= 7, "Too many keywords !"
        for i, kw in enumerate(book['keywords']):
            self.write_to_field(kw, f'data-print-book-keywords-{i}')

        ### Rubriques
        rubriques_btn = self.driver.find_element(By.ID, 'data-print-book-categories-button-proto-announce')
        rubriques_btn.click()

        non_fiction = self.wait_for('Non-fiction', By.LINK_TEXT)
        non_fiction.click()
        games = self.wait_for('Jeux', By.LINK_TEXT)
        games.click()
        
        cat_games = self.wait_for('checkbox-games_logic-and-brain-teasers')
        cat_games.click()
        cat_sudoku = self.wait_for('checkbox-games_sudoku')
        cat_sudoku.click()
        
        save_btn = self.wait_for('category-chooser-ok-button')
        save_btn.click()

        # I think sudokus qualify as low content
        sleep(.5)
        low_content = self.driver.find_element(By.ID, 'data-view-is-lcb')
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(low_content)
        )
        low_content.click()

        nsfw = self.driver.find_element(By.NAME, 'data[print_book][is_adult_content]-radio')
        nsfw.click()
        
        validate = self.driver.find_element(By.ID, 'save-and-continue-announce')
        validate.click()

        input()
        # self.write_to_field(, 'cke_1_contents')
        # sleep(10)

    def close(self):
        self.driver.close()

# assert 'Python' in driver.title
# assert 'No results found.' not in driver.page_source

if __name__ == '__main__':
    with KdpBrowser('gabibathie@gmail.com', sys.argv[1], False) as kb:
        kb.upload({
            'title':'This is a test title',
            'subtitle':'This is a test subtitle',
            'author':('Hilbert','Bagaie'),
            'description':'A long long description',
            'keywords': ['Sudoku', 'Puzzle', 'jeu de réflexion']
            })