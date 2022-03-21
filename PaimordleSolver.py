import time
import requests
import ast
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options






def getWordList():
    url="https://paimordle.vercel.app/"
    req=requests.get(url,'html.parser').text
    start= req.find("src=")+len("src=")+1
    end=req.find(">",start)-1
    url_end=req[start:end]
    js_url="https://paimordle.vercel.app"+url_end
    req_text=requests.get(js_url).text
    start= req_text.find("],c=")+len("],c=")
    end=req_text.find("],f=",start)+1
    word_string=req_text[start:end]
    word_list=ast.literal_eval(word_string)
    return word_list






def openWebsite():
    chrome_options = Options() 
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://paimordle.vercel.app/')
    time.sleep(1)
    game=driver.find_element(By.TAG_NAME,'html')
    game.send_keys(Keys.ESCAPE)
    time.sleep(1)
    return driver,game



def sendWord(element,word,turn):
    for i in word:
        element.send_keys(i)
        time.sleep(0.25)
    element.send_keys(Keys.ENTER)
    time.sleep(0.25)

    row=driver.find_elements(By.XPATH,"/html/body/div/div/div[2]/div[1]/div["+str(turn)+"]/div")
    colors=[]
    for i in row:
        colors.append(i.get_attribute("class"))
    for i in range(len(colors)):
        start= colors[i].find("shadowed bg-")+len("shadowed bg-")
        end=colors[i].find("-",start)
        colors[i]=colors[i][start:end]
    
    return colors


def filterWordBank(colors,word,wordBank):
    for color,letter in zip(colors,word):
        if color=='green' or color=='yellow' and letter not in existingLetters:
            existingLetters.append(letter)

    for i in range(len(colors)):
        if colors[i]=='slate' and word[i] not in existingLetters:
            wordBank=[x for x in wordBank if word[i] not in x]
        if colors[i]=='green':
            wordBank=[x for x in wordBank if word[i]==x[i]]
        if colors[i]=='yellow':
            wordBank=[x for x in wordBank if word[i] in x and word[i]!=x[i]]
    return wordBank


existingLetters=[]
wordBank=getWordList()
driver,game=openWebsite()
count=1
found=False
while count<7 and found==False:
    word=random.choice(wordBank)
    colors=sendWord(game,word,count)
    count+=1
    found=True
    for i in colors:
        if i!='green' :
            found=False
    if found==False:
        wordBank=filterWordBank(colors,word,wordBank)
