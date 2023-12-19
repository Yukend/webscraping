import json
import requests
from time import sleep
from selenium import webdriver
import random
import argparse
import re
from selenium.webdriver.common.by import By

parser = argparse.ArgumentParser(
    description='Searches Google For Linkedin Profiles')
parser.add_argument('--keyword', type=str, help='keywords to search')
parser.add_argument('--limit', type=int, help='how many profiles to scrape')
args = parser.parse_args()


class LinkedinScraper(object):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.binary_location = "/usr/bin/google-chrome"
    driver = webdriver.Chrome(options=options)
    sleep(10)
    driver.maximize_window()
    sleep(10)
    driver.get("https://www.linkedin.com/")
    sleep(10)
    cookies_dict = {}
    for cookie in driver.get_cookies():
        cookies_dict[cookie['name']] = cookie['value']
    # def login():
    #     # Navigate to the LinkedIn login page
    #     driver.get("https://www.linkedin.com/login")

    #     # Find the username and password input fields
    #     username_field = driver.find_element(by=By.XPATH, value="//input[@name='session_key']")
    #     password_field = driver.find_element(by=By.XPATH, value="//input[@name='session_password']")

    #     # Enter your username and password
    #     username_field.send_keys("yukendiran.k@ieas2it.com")
    #     password_field.send_keys("Yuki@2001")

    #     # Click the sign-in button
    #     sign_in_button = driver.find_element(by=By.XPATH, value="//button[@type='submit']")
    #     sign_in_button.click()

    def __init__(self, keyword, limit):
        """

        :param keyword: a str of keyword(s) to search for
        :param limit: number of profiles to scrape
        """
        self.keyword = keyword.replace(' ', '%20')
        self.all_htmls = ""
        self.server = 'www.google.com'
        self.quantity = '100'
        self.limit = int(limit)
        self.counter = 0
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-US,en;q=0.9',
                        'upgrade-insecure-requests': '1',
                        'scheme': 'https'}

    def search(self):
        """
        perform the search
        :return: a list of htmls from Google Searches
        """

        # choose a random user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/11.10 Chromium/18.0.1025.142 Chrome/18.0.1025.142 Safari/535.19',
            'Mozilla/5.0 (Windows NT 5.1; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.00'
        ]
        while self.counter < self.limit:
            headers = {'User-Agent': random.choice(user_agents)}
            url = 'http://google.com/search?num=100&start=' + \
                str(self.counter) + \
                '&hl=en&meta=&q=site%3Alinkedin.com/in%20' + self.keyword
            resp = requests.get(url, headers=headers)
            if ("Our systems have detected unusual traffic from your computer network.") in resp.text:
                print("Running into captchas")
                return

            self.all_htmls += resp.text
            self.counter += 100

    def parse_links(self):
        reg_links = re.compile(r"url=https:\/\/www\.linkedin.com(.*?)&")
        self.temp = reg_links.findall(self.all_htmls)
        results = []
        for regex in self.temp:
            final_url = regex.replace("url=", "")
            results.append("https://www.linkedin.com" + final_url)
        return results

    def parse_peoples(self):
        """

        :param html: parse the html for Linkedin Profiles using regex
        :return: a list of
        """
        reg_people = re.compile(r'">[a-zA-Z0-9._ -]* -|\| LinkedIn')
        self.temp = reg_people.findall(self.all_htmls)
        results = []
        for iteration in (self.temp):
            delete = iteration.replace(' | LinkedIn', '')
            delete = delete.replace(' - LinkedIn', '')
            delete = delete.replace(' profiles ', '')
            delete = delete.replace('LinkedIn', '')
            delete = delete.replace('"', '')
            delete = delete.replace('>', '')
            delete = delete.strip("-")
            if delete != " ":
                results.append(delete)
        return results

    def get_connections(self, links):
        """

        :param html: parse the html for Linkedin Profiles using regex
        :return: a list of
        """
        connections = []
        for link in links:
            resp = requests.get(link,
                                cookies=self.cookies_dict,
                                headers=self.headers)
            html = resp.text

            if html.css('ul.show-more-less__list'):
                connection_list = html.css('ul.show-more-less__list')
                connection_ref = connection_list.css(
                    'li a::attr(href)').getall()
                for connection in connection_ref:
                    if connection.split('?')[0] != "https://www.linkedin.com/login":
                        connections.append(connection.split('?')[0])

        return connections

    def parse_people(self, link):
        """

        :param html: parse the html for Linkedin Profiles using regex
        :return: a list of
        """
        resp = requests.get(link,
                            cookies=self.cookies_dict,
                            headers=self.headers)
        html = resp.text
        self.parse_profile(html)

    def parse_peoples(self, links):
        """

        :param html: parse the html for Linkedin Profiles using regex
        :return: a list of
        """
        for link in links:
            resp = requests.get(link,
                                cookies=self.cookies_dict,
                                headers=self.headers)
            html = resp.text
            self.parse_profile(html)

    def parse_connections(self, links):
        """

        :param html: parse the html for Linkedin Profiles using regex
        :return: a list of
        """
        for link in links:
            self.parse_people(link)

    def parse_profile(self, response):
        item = {}
        file = open(
            "linkedin_profiles/spiders/webpages/{0}.html".format(response.meta['profile']), "w")
        file.write(response.text)
        file.close()
        item['profile'] = response.meta['profile']
        item['url'] = response.meta['linkedin_url']

        """
            SUMMARY SECTION
        """
        summary_box = response.css("section.top-card-layout")
        item['name'] = summary_box.css("h1::text").get().strip()
        item['description'] = summary_box.css("h2::text").get().strip()

        # Location
        try:
            item['location'] = summary_box.css(
                'div.top-card__subline-item::text').get()
        except:
            item['location'] = summary_box.css(
                'span.top-card__subline-item::text').get().strip()
            if 'followers' in item['location'] or 'connections' in item['location']:
                item['location'] = ''

        item['followers'] = ''
        item['connections'] = ''

        for span_text in summary_box.css('span.top-card__subline-item::text').getall():
            if 'followers' in span_text:
                item['followers'] = span_text.replace(' followers', '').strip()
            if 'connections' in span_text:
                item['connections'] = span_text.replace(
                    ' connections', '').strip()

        item['connections_peoples'] = []
        connection_list = response.css('ul.show-more-less__list')
        connection_ref = connection_list.css('li a::attr(href)').getall()
        for connection in connection_ref:
            if connection.split('?')[0] != "https://www.linkedin.com/login":
                item['connections_peoples'].append(connection.split('?')[0])

        """
            ABOUT SECTION
        """
        item['about'] = response.css(
            'section.summary div.core-section-container__content p::text').get(default='')

        """
            EXPERIENCE SECTION
        """
        item['experience'] = []
        experience_blocks = response.css('li.experience-item')
        for block in experience_blocks:
            experience = {}
            # organisation profile url
            experience['organisation_profile'] = block.css(
                'h4 a::attr(href)').get(default='').split('?')[0]

            # location
            experience['location'] = block.css(
                'p.experience-item__location::text').get(default='').strip()

            # description
            try:
                experience['description'] = block.css(
                    'p.show-more-less-text__text--more::text').get().strip()
            except Exception as e:
                print('experience --> description', e)
                try:
                    experience['description'] = block.css(
                        'p.show-more-less-text__text--less::text').get().strip()
                except Exception as e:
                    print('experience --> description', e)
                    experience['description'] = ''

            # time range
            try:
                date_ranges = block.css('span.date-range time::text').getall()
                if len(date_ranges) == 2:
                    experience['start_time'] = date_ranges[0]
                    experience['end_time'] = date_ranges[1]
                    experience['duration'] = block.css(
                        'span.date-range__duration::text').get()
                elif len(date_ranges) == 1:
                    experience['start_time'] = date_ranges[0]
                    experience['end_time'] = 'present'
                    experience['duration'] = block.css(
                        'span.date-range__duration::text').get()
            except Exception as e:
                print('experience --> time ranges', e)
                experience['start_time'] = ''
                experience['end_time'] = ''
                experience['duration'] = ''

            item['experience'].append(experience)

        """
            EDUCATION SECTION
        """
        item['education'] = []
        education_blocks = response.css('li.education__list-item')
        for block in education_blocks:
            education = {}

            # organisation
            education['organisation'] = block.css(
                'h3::text').get(default='').strip()

            # organisation profile url
            education['organisation_profile'] = block.css(
                'a::attr(href)').get(default='').split('?')[0]

            # course details
            try:
                education['course_details'] = ''
                for text in block.css('h4 span::text').getall():
                    education['course_details'] = education['course_details'] + \
                        text.strip() + ' '
                education['course_details'] = education['course_details'].strip()
            except Exception as e:
                print("education --> course_details", e)
                education['course_details'] = ''

            # description
            education['description'] = block.css(
                'div.education__item--details p::text').get(default='').strip()

            # time range
            try:
                date_ranges = block.css('span.date-range time::text').getall()
                if len(date_ranges) == 2:
                    education['start_time'] = date_ranges[0]
                    education['end_time'] = date_ranges[1]
                elif len(date_ranges) == 1:
                    education['start_time'] = date_ranges[0]
                    education['end_time'] = 'present'
            except Exception as e:
                print("education --> time_ranges", e)
                education['start_time'] = ''
                education['end_time'] = ''

            item['education'].append(education)

        f = open(
            "linkedin_profiles/spiders/data/{0}.html".format(response.meta['profile']), "w")
        f.write(json.dumps(item))
        f.close()
        yield item


if __name__ == "__main__":
    ls = LinkedinScraper(keyword=args.keyword, limit=args.limit)
    # ls.search()
    # links = ls.parse_links()
    # print(links)
    # profile_list = ls.parse_peoples()
    # print(profile_list)
    # profiles = ls.parse_peoples(links)
    # print(profiles)

    profile_list = [""]
    ls.parse_peoples(profile_list)
    connections = ls.get_connections(profile_list)
    ls.parse_connections(connections)
