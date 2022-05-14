# import  our module files
import scrapy
import pandas as pd

# main url and getting urls
base_url = "https://en.soccerwiki.org/search/player?minrating=90&maxrating=99"
next_urls = [base_url]

# create pages
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


# inherit from scrapy
class Soccer(scrapy.Spider):
    
    # name of our spider
    name = 'soccer_spider'
    
    # Our Start URLS 
    start_urls = next_urls 
    
    # Later write to file
    output = "scrapy_player_stats.csv"
    
    # player STATS
    stats_list = list()

    # Parse our HTML with scrapy's perse
    def parse(self, response):
        # Get the response from the get_request(start_urls)
        all_stats = response.css("tbody > tr")
        
        # Now we will be looping through the table rows under the body 
        # Finding where our data is located

        for stat in all_stats:
            NAME = ".//td[@class='text-left']/a/text()"
            CLUB = './/td[@class="text-left"]/a/text()'
            POSITION = './/td[@class="text-left text-dark"]/span/text()'
            HEIGHT = './/td[@class="text-center text-dark"]/text()'
            FOOT = './/td[@class="text-center text-dark"]/text()'
            AGE = './/td[@class="text-center text-dark"]/text()'
            RATING = './/td[@class="text-center text-dark"]/text()'
            
            # empty stats dict
            STATS = dict()

            # update our stats dictionary with join method that converts list to string
            STATS["NAME"] = ' '.join(stat.xpath(NAME)[0].getall())
            STATS["CLUB"] = ' '.join(stat.xpath(CLUB)[1].getall())
            STATS["POSITION"] = stat.xpath(POSITION).get()
            STATS["HEIGHT"] = ' '.join(stat.xpath(HEIGHT)[0].getall())
            STATS["FOOT"] = ' '.join(stat.xpath(FOOT)[1].getall())
            STATS["AGE"] = ' '.join(stat.xpath(AGE)[2].getall())
            STATS["RATING"] = ' '.join(stat.xpath(RATING)[3].getall())
            
            # test
            # print(STATS["NAME"], STATS["CLUB"],STATS["POSITION"],STATS["HEIGHT"], STATS["FOOT"], STATS["AGE"], STATS["RATING"])

            # update our stats fil
            self.stats_list.append((STATS["NAME"], STATS["CLUB"],STATS["POSITION"],STATS["HEIGHT"], STATS["FOOT"], STATS["AGE"],STATS["RATING"]))
            # print("--on it--")
            
            print("getting data ....")
        
        # get only top 100
        top_100_players = self.stats_list[0:101]
        # print(top_100_players)
        
        #Include Headers in our CSV
        HEADERS = ["NAME", "CLUB", "POSITION", "HEIGHT", "FOOT", "AGE" , "RATING"]
        
        # CREATE A stats pandas DATAFRAME
        stats_dataframe = pd.DataFrame(top_100_players, columns=HEADERS)
        
        # Open our output file & write to it
        stats_dataframe.to_csv(self.output)
        
        print(f"Updated {self.output} File")

