import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

url = "https://www.uece.br/uece/noticias/"
driver = webdriver.Firefox()
driver.get(url)
driver.implicitly_wait(5) # Seconds

posts = driver.find_element(By.CLASS_NAME, "cc-posts")
posts_html = posts.get_attribute('innerHTML')

soup = BeautifulSoup(posts_html, 'html.parser')
posts_title = soup.find_all("h3")
posts_description = soup.find_all(class_="cc-post-excerpt")

if len(posts_title) != len(posts_description):
    quit()

join_title_description = {key.text.strip() : value.text.strip() for key, value in zip(posts_title, posts_description)}
df = pd.DataFrame(list(join_title_description.items()), columns=["Title", "Description"])
df.to_json('results.json', orient="records", force_ascii=False, indent=4)
print('Success in Web Scrapping!')
driver.quit()