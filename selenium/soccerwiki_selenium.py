import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver

# Make our own configuration 
from selenium.webdriver.chrome.options import Options

# initialise options 
options = Options()

# change some defaults
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_argument('log-level=3')

# start the driver with our options
driver = webdriver.Chrome(options=options)

# get stats -variables
player_stats = []
stats_file = "selenium_stats.csv"

# start from this URL
URL = "https://en.soccerwiki.org/search/player?minrating=90&maxrating=99"
pages = [URL]

# get the next pages dynamically
for page in range(15,121,15):
    next_payload = "&offset=" + str(page)

    if page == 15:
        next_url = URL + next_payload
        pages.append(next_url)
    elif page == 30:
        next_url = pages[-1] + next_payload
        pages.append(next_url)
    elif page == 45:
        next_url = pages[-1] + next_payload
        pages.append(next_url)
    elif page == 60:
        next_url = pages[-1] + next_payload
        pages.append(next_url)
    elif page == 75:
        next_url = pages[-1] + next_payload
        pages.append(next_url)
    elif page == 90:
        next_url = pages[-1] + next_payload
        pages.append(next_url)
    elif page == 105:
        next_url = pages[-1] + next_payload
        pages.append(next_url)
    else:
        pass

# soccer stats function
def get_soccer():
    # loop though our pages and get each url data
    for idx , url in enumerate(pages):
        driver.get(url)
        stats_body = driver.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    
        # Get NAME, CLUB, POSITION from stats body
        for stat in stats_body:
            NAME = stat.find_elements(By.CLASS_NAME, "text-left")[0].text
            CLUB = stat.find_elements(By.CLASS_NAME, "text-left")[1].text
            POSITION = stat.find_elements(By.TAG_NAME, "span")[1].text
            
            # get the remaining stats
            other_stats = stat.text.split(" ")  
            
            # Get HEIGHT, FOOT, AGE & RATING
            HEIGHT = other_stats[-4]
            FOOT = other_stats[-3]
            AGE = other_stats[-2]
            RATING = other_stats[-1]
            
            # test
            # print(NAME, CLUB, POSITION, HEIGHT, FOOT, AGE, RATING)
            print("getting info >>>")
            
            # create a list for scraped information
            player_stats.append((NAME, CLUB, POSITION, HEIGHT, FOOT, AGE, RATING))
        print(f"we are done page {idx}", end="\n")
    print("done for the top 120 players")

# write to stats file           
def write_stats():
    # get only 100 players from 120
    top_100_players = player_stats[0:101]
    
    # create column headers
    COLUMN_NAMES = ["NAME", "CLUB", "POSITION", "HEIGHT", "FOOT", "AGE" , "RATING"]
    
    # finally write
    crypto_dataframe = pd.DataFrame(top_100_players, columns=COLUMN_NAMES)
    crypto_dataframe.to_csv(stats_file)
    print("done writing to stats file")
 

# run our functions
get_soccer()
write_stats()

# finish session
driver.quit()

