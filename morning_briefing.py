import requests
from bs4 import BeautifulSoup
import pyshorteners

# URL shortening function
def shorten_url(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url) # Aqui se obtem o URL encurtado da pagina de noticias fornecida como parametro

def scrape_news_itatiaia(url, k):
    url_position = url.find(".br") + 3 # Obtem o indice correspondente ao fim da url absoluta
    cropped_url = url[:url_position] # Armazena a url absoluta, ex.: https://www.itatiaia.com.br

    response = requests.get(url) # Requisicao de metodo GET feita para a url

    if response.encoding is None or response.enconding == "ISO-8859-1": # condicional para validar se a resposta possui a encodificacao adequada
        response.encoding = response.apparent_encoding
    
    soup = BeautifulSoup(response.content, 'html.parser') # interpretacao do conteudo da resposta como HTML

    news_links = soup.find_all('a', class_='jumbotron-default-link') # selecao de todos os links da resposta (tag <a>), que sao armazenados na lista news_links

    news_data = []

    for link in news_links:
        title = link.get('title')
        href = link.get('href') 

        if href and href.startswith('/'):
            href = cropped_url + href  

        news_data.append((title, href)) 
        
        # para cada link da pagina (armazenados na lista news_links), armazena-se uma tupla na lista news_data. A tupla cntem o titulo da respectiva pagina e o href.

        if len(news_data) > k: # se a quantidade de noticias for maior/igual do que o parametro k fornecido pelo usuario, interrompe o loop
            break

    
    return news_data # retorna a lista de tuplas contendo as noticias
    

def scrape_news_o_tempo(url):
    pass

def scrape_news_estado_de_minas(url):
    position = url.find('.br') + 3  # +3 to include '.br'
    cropped_url = url[:position]

    # Send a GET request to the website
    response = requests.get(url)
    # Ensure the correct encoding is used based on the webpage's content type

    if response.encoding is None or response.encoding == 'ISO-8859-1':
        response.encoding = response.apparent_encoding

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')  # Use response.content to avoid re-encoding issues

    # Find all <a> elements with the class 'jumbotron-default-link'
    news_links = soup.find_all('a', class_='jumbotron-default-link')

    # Prepare a list to store tuples of (title, link)
    news_data = []
    for link in news_links:
        title = link.get('title')  # Extract the title from the 'title' attribute
        href = link.get('href')  # Extract the URL from the 'href' attribute
        # Check if the link is relative and prepend the base URL if needed
        if href and href.startswith('/'):
            href = cropped_url + href  # Append the base domain to the relative URL
        # Append the tuple (title, href) to the list
        news_data.append((title, href))
    return news_data

def gather_news_o_tempo(news_sources):
    pass

def gather_news_itatiaia(news_sources, k):
    
    all_news = {} # é declarado um dicionario que armazenara as noticias de acordo com suas categorias
    
    for url, category in news_sources.items(): # iteracao por cada item do dicionario news_sources_Itatiaia

        news = scrape_news_itatiaia(url, k) # a variavel news recebe a lista de tuplas contendo o titulo e href da pagina da respectiva noticia. O parametro k corresponde a quantidade de noticias que o usuario deseja receber.

        if category not in all_news:
            all_news[category] = [] # se a categoria ainda nao existe no dicionario, ela eh adicionada
        
        all_news[category].extend(news) # a lista referente a categoria recebe a noticia (tupla)

    return all_news

def gather_news_EM(news_sources):
        # Gather all news
    all_news = {}
    for url, category in news_sources.items():
        news = scrape_news_estado_de_minas(url)
        if category not in all_news:
            all_news[category] = []
        all_news[category].extend(news)

    return all_news

def format_news(all_news):
    # Format news text
    news_text = ""
    for category, items in all_news.items():
        news_text += f"📌 {category.title()}:\n"
        for title, link in items:
            short_link = shorten_url(link)
            news_text += f"📰 {title}: {short_link}\n"
        news_text += "\n"

    return news_text

    

if __name__ == "__main__":

    from datetime import datetime
    from tqdm import tqdm
   
    # News websites and categories (example)
    """ news_sources_EM = {
        'https://www.em.com.br/politica/': 'Política',
        'https://www.em.com.br/economia/': 'Economia',
        'https://www.em.com.br/educacao/': 'Educação',
        # Add more sources as needed
    } """

    news_sources_Itatiaia = {
        'https://www.itatiaia.com.br/politica': 'Política',
        'https://www.itatiaia.com.br/financas': 'Finanças'
    }

    # all_news = gather_news_EM(news_sources_EM)
    k = int(input("Quantidade de notícias: "))
    all_news = gather_news_itatiaia(news_sources_Itatiaia, k)
    news_text = format_news(all_news)
    print(news_text)



    