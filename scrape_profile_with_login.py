import requests
from bs4 import BeautifulSoup
session = requests.Session()
login_url = 'https://www.linkedin.com/login'
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'loginCsrfParam'}).get('value')
login_data = {
    'session_key': 'yukendiran.k@ideas2it.com',
    'session_password': 'Yuki@2001',
    'loginCsrfParam': csrf_token,
}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-US,en;q=0.9',
                        'upgrade-insecure-requests': '1',
                        'scheme': 'https'}

session.headers.update(headers)

login_url = 'https://www.linkedin.com/login-submit'
response = session.post(login_url, data=login_data)
if "Feed" in response.text:
    print("Success")
links = [
"https://www.linkedin.com/in/mary-barra",
"https://www.linkedin.com/in/stevenbartlett-123",
# "https://www.linkedin.com/in/pascalbornet",
# "https://www.linkedin.com/in/nithin-kamath-81136242",
# "https://www.linkedin.com/in/theahmadimam",
# "https://www.linkedin.com/in/dharmesh",
# "https://www.linkedin.com/in/lexfridman",
# "https://www.linkedin.com/in/sarahdjohnston",
# "https://www.linkedin.com/in/sanyin",
# "https://www.linkedin.com/in/laszlobock",
# "https://www.linkedin.com/in/hadenjeff",
# "https://www.linkedin.com/in/officialjohnmaxwell",
# "https://www.linkedin.com/in/daniel-abrahams",
# "https://www.linkedin.com/in/nesli-neslihan-girgin",
# "https://www.linkedin.com/in/robynnstorey",
# "https://www.linkedin.com/in/amy-cuddy-3654034",
# "https://www.linkedin.com/in/bersin",
# "https://www.linkedin.com/in/beerbiceps",
# "https://www.linkedin.com/in/shayrowbottom"
]
for link in links:
    user = session.get('https://www.linkedin.com/in/mary-barra')

    with open("{0}.html".format(link.split('/')[-1]), "w") as f:
        f.write(user.text)

