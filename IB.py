from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from InstagramAPI import InstagramAPI
import time
import random


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        # self.driver = None
        self.actions = ActionChains(self.driver)
        self.black_list = ['https://www.instagram.com/', 'https://www.instagram.com/explore/',
                      'https://www.instagram.com/accounts/activity/', 'https://www.instagram.com/mytolstoi/',
                      'https://www.instagram.com/about/us/', 'https://help.instagram.com/',
                      'https://instagram-press.com/', 'https://www.instagram.com/developer/',
                      'https://www.instagram.com/about/jobs/', 'https://www.instagram.com/legal/privacy/',
                      'https://www.instagram.com/legal/terms/', 'https://www.instagram.com/explore/locations/',
                      'https://www.instagram.com/directory/profiles/', 'https://www.instagram.com/directory/hashtags/']
        self.vip_name_list = ['tomhanks', 'endorphinagames', 'rishi_sinha', 'peskovausy', 'dolphinmusic', 'norimyxxxo',
                              'rottentomatoes', 'natgeo.russia', 'nph', 'hollywoodreporter', 'imdb', 'theacademy',
                              'nasa', 'ugarnaya__politika', 'radiosvoboda', 'kremlin_gang', 'navalny', 'yoshkinkrot',
                              'meduzapro', 'discovery', 'cnn', 'nytimes', 'innopolis', 'natgeomagazineru', 'natgeowild',
                              'esquireru', 'hbo', 'theellenshow', 'thiago_deponte', 'leonardodicaprio', 'natgeo',
                              'shnurovs', 'yfaonline', 'instagramru']
        self.comment_list = ['Wonderful! 👍', 'Amazing! 👍', 'Nice! 👍', 'I like that! 👍', 'So cool! 👍',
                             'So wonderful! 👍', 'So nice! 👍', 'Cool! 👍', "Look's cool! 👍", "Look's good! 👍",
                             "Look's amazing! 👍", "Look's wonderful! ", "Look's Nice! 👍", "That's great! 👍"]
        self.api = InstagramAPI(self.username, self.password)
        self.api.login()
        self.user_id = self.api.username_id

    def get_vip_list(self):
        vip_list = self.vip_name_list
        return vip_list

    def get_total_subs_list(self):
        subs_name_list = []
        total_subs_list = self.api.getTotalFollowers(self.user_id)
        for sub in total_subs_list:
            subs_name_list.append(sub["username"])
        return subs_name_list

    def get_total_subing_list(self):
        subing_name_list = []
        total_subing_list = self.api.getTotalFollowings(self.user_id)
        for subing in total_subing_list:
            subing_name_list.append(subing["username"])
        return subing_name_list

    def save_total_subing_list_to_file(self):
        with open('lists/total_subing_list.txt', 'w') as f:
            for item in self.get_total_subing_list():
                f.write("%s\n" % item)
            f.close()

    def get_list_to_unsub(self):
        unsubs_list = []
        vip_list = self.get_vip_list()
        total_subs_list = self.get_total_subs_list()
        total_subing_list = self.get_total_subing_list()
        for name in total_subing_list:
            if name not in total_subs_list:
                if name not in vip_list:
                    unsubs_list.append(name)
        return unsubs_list

    def close_browser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.maximize_window()
        driver.get('https://www.instagram.com/')
        time.sleep(4)
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(4)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(self.password)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(4)

    def like_photo(self, hashtag):
        pic_hrefs = []
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)
        for i in range(1, 10):
            self.actions.send_keys(Keys.PAGE_DOWN)
            self.actions.perform()
            time.sleep(2)
        hrefs = self.driver.find_elements_by_tag_name('a')
        for elem in hrefs:
            if elem.get_attribute('href') not in self.black_list:
                pic_hrefs.append(elem.get_attribute('href'))
        print(hashtag + ' photos: ' + str(len(pic_hrefs)))

        for pic_href in pic_hrefs:
            driver.get(pic_href)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(1)
                driver.find_element_by_xpath("//span[@aria-label='Like']").click()
                time.sleep(17)
            except Exception as e:
                time.sleep(2)

    def unsub(self, names_list):
        for name in names_list:
            try:
                self.driver.find_element_by_xpath("//input[@placeholder='Search']").clear()
                self.driver.find_element_by_xpath("//input[@placeholder='Search']").send_keys(name)
                time.sleep(1)
                self.driver.find_element_by_xpath("//input[@placeholder='Search']").send_keys(Keys.RETURN)
                time.sleep(1)
                self.driver.find_element_by_xpath("//input[@placeholder='Search']").send_keys(Keys.RETURN)
                time.sleep(1)
                self.driver.find_element_by_xpath("//button[contains(text(),'Following')]").click()
                time.sleep(1)
                self.driver.find_element_by_xpath("//button[contains(text(),'Unfollow')]").click()
                print(name + ' unsub')
            except Exception as e:
                print(e)
                time.sleep(1)

    def random_comment(self):
        comment = self.comment_list[random.randint(0, (len(self.comment_list) - 1))]
        return comment

    def generate_subs(self, hashtag):
        pic_hrefs = []
        self.driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)
        for i in range(1, 5):
            self.actions.send_keys(Keys.PAGE_DOWN)
            self.actions.perform()
            time.sleep(2)
        hrefs = self.driver.find_elements_by_tag_name('a')
        for elem in hrefs:
            if elem.get_attribute('href') not in self.black_list:
                pic_hrefs.append(elem.get_attribute('href'))
        print(hashtag + ' photos: ' + str(len(pic_hrefs)))
        for pic_href in pic_hrefs:
            self.driver.get(pic_href)
            time.sleep(2)
            try:
                like = self.driver.find_element_by_xpath("//span[@aria-label='Like']")
                like.click()
                time.sleep(1)
                follow = self.driver.find_element_by_xpath("//button[contains(text(),'Follow')]")
                follow.click()
                time.sleep(1)
                self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']").click()
                self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']").clear()
                self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']").send_keys(
                    str(self.random_comment()))
                time.sleep(11)
                self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']").send_keys(Keys.RETURN)
                time.sleep(2)
            except Exception as e:
                print(e)
                time.sleep(2)

    def save_new_subing_list(self):
        new_subbing_list = []
        with open("lists/total_subing_list.txt", "r") as ins:
            total_subing_list = []
            for line in ins:
                line = line.rstrip('\n')
                total_subing_list.append(line)
            for subing in self.get_total_subing_list():
                if subing not in total_subing_list:
                    new_subbing_list.append(subing)
            with open('lists/new_subing_list.txt', 'w') as f:
                for item in new_subbing_list:
                    f.write("%s\n" % item)
                f.close()
        return None

    def like_my_feed(self):
        driver = self.driver
        like_counter = 0
        for i in range(1, 10):
            time.sleep(1)
            try:
                driver.find_element_by_xpath("//span[@aria-label='Like']").click()
                # driver.find_element_by_css_selector('article._8Rm4L:nth-child(4) > div:nth-child(3) > section:nth-child(1) > span:nth-child(1) > button:nth-child(1)').click()
                like_counter += 1
            except Exception as e:
                print(e)
                time.sleep(2)
            time.sleep(1)
            self.actions.send_keys(Keys.PAGE_DOWN)
            self.actions.perform()
            try:
                driver.find_element_by_xpath("//span[@aria-label='Like']").click()
                # driver.find_element_by_css_selector('article._8Rm4L:nth-child(4) > div:nth-child(3) > section:nth-child(1) > span:nth-child(1) > button:nth-child(1)').click()
                like_counter += 1
            except Exception as e:
                print(e)
                time.sleep(2)
            time.sleep(1)
        print('Total Likes: ' + str(like_counter))

    def show_statistics(self):
        total_subs_list = self.get_total_subs_list()
        total_subing_list = self.get_total_subing_list()
        list_to_unsub = self.get_list_to_unsub()
        print('Total VIP list               : ' + str(len(self.vip_name_list)))
        print('Total following without VIPs : ' + str(len(total_subing_list) - len(self.vip_name_list)))
        print('Total followers              : ' + str(len(total_subs_list)))
        print('Total unsubs                 : ' + str(len(list_to_unsub)))
        print('Unsubs: ' + str(list_to_unsub))


if __name__ == "__main__":
    MikhailIG = InstagramBot("login", "password")

    MikhailIG.login()
    MikhailIG.like_my_feed()
    MikhailIG.like_photo("follow4like")
    #MikhailIG.unsub(
    MikhailIG.generate_subs('nature')
    # MikhailIG.get_total_subing_list()
    # MikhailIG.save_total_subing_list_to_file()
    # MikhailIG.save_new_subing_list()
    MikhailIG.show_statistics()
    MikhailIG.close_browser()
