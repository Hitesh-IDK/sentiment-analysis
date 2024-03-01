from django.shortcuts import render
from django.http import HttpResponse

import requests
import time

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from vaderSentiment import SentimentIntensityAnalyzer
from vaderSentiment import startProgram

import validators

url = 'https://twitter.com/Tectone'

def index(request):
    return render(request, "index.html")

# Create your views here.
def result(request):

    if request.method == 'POST':
        print(request.POST.get('profileField', None))
        inputUrl = request.POST.get('profileField', None)

        tweet_messages = []
        tweet_positives = []
        tweet_neutrals = []
        tweet_negatives = []

        totalPositives = 0
        totalNeutrals = 0
        totalNegatives = 0
        totalNegativeScore = 0;

        if not validators.url(inputUrl) :
           requestVariables = {"profile_url": url,"bar_chart_data": [totalPositives, totalNeutrals, totalNegatives], "tweet_messages": tweet_messages, "tweet_positives": tweet_positives,"tweet_neutrals": tweet_neutrals, "tweet_negatives": tweet_negatives}
           return render(request, "result.html", context=requestVariables)
 
        results = startSelenium(inputUrl)

        for result in results:
            slicer = slice(36)

            if result['compound'] > 0:
                totalPositives = totalPositives + 1
            elif result['compound'] < 0:
                totalNegatives = totalNegatives + 1
                totalNegativeScore = totalNegativeScore + result['neg']
            else:
                totalNeutrals = totalNeutrals + 1

            tweet_messages.append(f"{result['sentence'][slicer]}...")
            tweet_positives.append(result['pos'])
            tweet_neutrals.append(result['neu'])
            tweet_negatives.append(result['neg'])


        riskFactor = float(round((totalNegatives / len(results)) * (totalNegativeScore / totalNegatives), 2)) if totalNegatives != 0 else 0
        requestVariables = {"profile_url": inputUrl, "risk_factor": riskFactor, "bar_chart_data": [totalPositives, totalNeutrals, totalNegatives], "tweet_messages": tweet_messages, "tweet_positives": tweet_positives,"tweet_neutrals": tweet_neutrals, "tweet_negatives": tweet_negatives}
        


        return render(request, "result.html", context=requestVariables)
    else:
        return HttpResponse("Method Not Allowed", status=405)
    

    

def startSelenium(setUrl):
    #Driver for chrome
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    print(setUrl)
    driver.get(setUrl)

    time.sleep(4)

    sentences = []
    firstScroll = True
    loops = 20
    verticalLoop = 0

    while(loops > 0):
        loops = loops - 1
        verticalLoop = verticalLoop + 500
        print("\n\n********111111111111***********")

        tweetTexts = driver.find_elements(By.XPATH, "//div[@data-testid = 'tweetText']/span")
        for tweetText in tweetTexts:
            sentences.append(tweetText.text)


        print(sentences)
        driver.execute_script(f"window.scrollTo(0, {verticalLoop});")
        time.sleep(1)

        try:
            if(firstScroll):
                closeElement = driver.find_element(By.XPATH, "//div[@data-testid = 'app-bar-close']")
                firstScroll = False
                if(closeElement):
                    closeElement.click()
        except: 
            print("error here")
        
    sentences = list(set(sentences))
    finalSentences = []

    for sentence in sentences:
        splited = " ".join(sentence.split("\n"))
        finalSentences.append(splited)

    return startProgram(finalSentences)

    # for sentence in sentences:
    #     print(sentence)

    # print("\n\n***************222222222222222222*****************")

    # tweetTexts = driver.find_elements(By.XPATH, "//div[@data-testid = 'tweetText']/span")
    # print(len(tweetTexts))
    # for tweetText in tweetTexts:
    #     print(tweetText.text)

    # time.sleep(3)

    # driver.execute_script("window.scrollTo(0, 500);")
    # time.sleep(1)

    # print("\n\n***********33333333333333333***************")

    # tweetTexts = driver.find_elements(By.XPATH, "//div[@data-testid = 'tweetText']/span")
    # print(len(tweetTexts))
    # for tweetText in tweetTexts:
    #     print(tweetText.text)

    # time.sleep(3)