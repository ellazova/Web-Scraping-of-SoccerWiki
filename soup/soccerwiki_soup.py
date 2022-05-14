# modules to use
from bs4 import BeautifulSoup 
import requests
import pandas as pd

# create an http header
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
 Chrome/86.0.4240.75 Safari/537.36'}

base_url = "https://en.soccerwiki.org/search/player?minrating=90&maxrating=99"

# put stats here
player_stats = []

# write to file later
output_file = "soup_player_stats.csv"

# All URLS we need
next_urls = [base_url]
URLS = next_urls

# build urls on from base_url
def build_urls():
    for page in range(15,121,15):
        next_payload = "&offset=" + str(page)
        
        if page == 15:
            next_url = base_url + next_payload
            next_urls.append(next_url)
        elif page == 30:
            next_url = next_urls[-1] + next_payload
            next_urls.append(next_url)
        elif page == 45:
            next_url = next_urls[-1] + next_payload
            next_urls.append(next_url)
        elif page == 60:
            next_url = next_urls[-1] + next_payload
            next_urls.append(next_url)
        elif page == 75:
            next_url = next_urls[-1] + next_payload
            next_urls.append(next_url)
        elif page == 90:
            next_url = next_urls[-1] + next_payload
            next_urls.append(next_url)
        elif page == 105:
            next_url = next_urls[-1] + next_payload
            next_urls.append(next_url)
        else:
            pass
    print("urls built for scraping")
# print(next_urls)

# get stats from urls 
def get_stats():
    for url in URLS:
        response = requests.get(url, headers=headers)
        # Let's create a  of our soup to parse the HTML for operations using  "lxml"    
        soup = BeautifulSoup(response.content.decode(), "html.parser")

        # get the body of stats
        stats_body = soup.find("tbody").findAll('tr')
        
        # test
        # print(stats_body)
        
        # Loop through and get the data from the body;
        for stat in stats_body:        
            NAME = stat.find_all(class_="text-left")[0].get_text()
            CLUB = stat.find_all(class_="text-left")[1].get_text()
            POSITION =  stat.find(class_="text-left text-dark").get_text()
            HEIGHT = stat.find_all(class_="text-center text-dark")[0].get_text()
            FOOT = stat.find_all(class_="text-center text-dark")[1].get_text()
            AGE = stat.find_all(class_="text-center text-dark")[2].get_text()
            RATING = stat.find_all(class_="text-center text-dark")[3].get_text()

            # print(NAME, CLUB, POSITION, HEIGHT, FOOT, AGE , RATING)
            # print(HEIGHT)
            
            # Update our list of player stats
            player_stats.append((NAME, CLUB, POSITION, HEIGHT, FOOT, AGE , RATING))
    print(" Finished Scraping ")

# Writing our scraped stats to a file
def write_stats_to_file():
    # Get the top 100 from 120
    top_100_players = player_stats[0:101]
    
    #Include Headers in our CSV
    HEADERS = ["NAME", "CLUB", "POSITION", "HEIGHT", "FOOT", "AGE" , "RATING"]
    
    # CREATE A DATAFRAME for top 100
    stats_dataframe = pd.DataFrame(top_100_players, columns=HEADERS)
    stats_dataframe.to_csv(output_file)
    
    print(f"Finished Creating {output_file} file ")
        
# # Running our scraper
build_urls()
get_stats()  
write_stats_to_file()
