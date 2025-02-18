import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

url = "https://www.uece.br/uece/noticias/"
driver = webdriver.Firefox()
driver.get(url)
driver.implicitly_wait(5) # Seconds

# Tenta encontrar o botão de cookies e clicá-lo
try:
    button_cookies = driver.find_element(By.ID, "cc-cookies-confirm-consent")
    button_cookies.click()
    print('Botão de cookies clicado com sucesso!')
except Exception as e:
    print(f'Erro ao tentar clicar no botão de cookies: {e}')


def get_posts():
    posts = driver.find_element(By.CLASS_NAME, "cc-posts")
    posts_html = posts.get_attribute('innerHTML')

    soup = BeautifulSoup(posts_html, 'html.parser')
    posts_title = soup.find_all("h3")
    posts_description = soup.find_all(class_="cc-post-excerpt")

    return posts_title, posts_description

max_posts = 50
max_clicks = 10
max_erros = 3
contador_clicks = 0
contador_erros = 0

posts_title, posts_description = get_posts()

# Busca o botão 'Ver mais' e o clica até 10 vezes ou até acumular até 50 notícias ou até atingir 3 erros
while(len(posts_title) <= max_posts and contador_clicks < max_clicks and contador_erros < max_erros):
    try:
        button_ver_mais = driver.find_element(By.CLASS_NAME, "cc-button")
        button_ver_mais.click()
        contador_clicks += 1
    except Exception as e:
        contador_erros += 1
        print(f'Erro ao tentar clicar no botão Ver Mais: {e}')
    finally:
        time.sleep(2.5)
        posts_title, posts_description = get_posts()

if len(posts_title) != len(posts_description):
    quit()

join_title_description = {key.text.strip() : value.text.strip() for key, value in zip(posts_title, posts_description)}
df = pd.DataFrame(list(join_title_description.items()), columns=["Title", "Description"])
df.to_json('results.json', orient="records", force_ascii=False, indent=4)
print('Success in Web Scrapping!')
driver.quit()

# Valida o número de itens extraídos no json.
caminho_arquivo = 'results.json'

with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

num_itens = len(dados)

print(f'O arquivo JSON contém {num_itens} itens.')
