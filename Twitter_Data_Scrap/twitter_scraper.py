import csv
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class TwitterScraper:
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        
    def login(self):
        # Twitter giriş sayfasını aç
        self.driver.get("https://twitter.com/login")

        time.sleep(5)
        box = ".r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-1dz5y72.r-fdjqy7.r-13qz1uu"
        # Kullanıcı adı giriş alanını bul
        username_input = self.driver.find_element(By.CSS_SELECTOR, box)

        # Kullanıcı adı giriş alanına tıklamak için
        username_input.click()
        username_input.send_keys("EMAIL")
        username_input.send_keys(Keys.ENTER)

        time.sleep(3)
        acc_input = self.driver.find_element(By.CSS_SELECTOR, box)
        acc_input.click()
        acc_input.send_keys("USERNAME")
        acc_input.send_keys(Keys.ENTER)

        time.sleep(3)
        password_input = self.driver.find_element(By.CSS_SELECTOR, box)
        password_input.click()
        password_input.send_keys("PASSWORD")
        password_input.send_keys(Keys.ENTER) 
        
    
    def write_csv(self, username, posts_html):
        file = open(f"{username}_tweets.csv", "w", encoding = "utf-8")
        writer = csv.writer(file)
        writer.writerow(["UDate","Tweet","Reply","Retweet","Like","View"])
        
        soup = BeautifulSoup(posts_html, "html.parser")
        tweets = soup.find_all("article", attrs={"data-testid":"tweet"})
        
        for bod in tweets:
            udate = bod.find("div", attrs={"class":"css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t"}).text
            tweet = bod.find("div", attrs={"class":"css-901oao css-cens5h r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"}).text
            reply = bod.find("div", attrs={"data-testid":"reply"}).text
            retweet = bod.find("div", attrs={"data-testid":"retweet"}).text
            like = bod.find("div", attrs={"data-testid":"like"}).text
            view = bod.find("a", attrs={"class":"css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1777fci r-bt1l66 r-1ny4l3l r-bztko3 r-lrvibr"}).text
            #print(tweet)
            writer.writerow([udate,tweet,reply,retweet,like,view])
            
    
    def get_tweets_by_username(self, username, max_posts:int=5) -> pd.DataFrame:
        #login
        self.login()
        time.sleep(5)
        # get page
        url = f'https://twitter.com/{username}'
        self.driver.get(url)
        time.sleep(8)    
        
        posts_html = ""
        for i in range(max_posts):
            try:
                post = self.driver.find_elements(By.TAG_NAME, 'article')[i]
            except Exception:
                break
            self.driver.execute_script("arguments[0].scrollIntoView(true);", post)
            time.sleep(3)
            posts_html += post.get_attribute('outerHTML')
        
        self.write_csv(username, posts_html)
        df = pd.read_csv(f"{username}_tweets.csv")
        return df
    
    
def main():
    scraper = TwitterScraper()
    df = scraper.get_tweets_by_username("AltayCemMeric", 50)
    print(df)
    #df = pd.read_csv("AltayCemMeric_tweets.csv")
    #print(df)


if __name__ == "__main__":
    main()
                
    