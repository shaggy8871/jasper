# -*- coding: utf-8-*-
import feedparser
from client import app_utils
import re
import string
from semantic.numbers import NumberService

WORDS = ["NEWS", "YES", "NO", "FIRST", "SECOND", "THIRD"]

PRIORITY = 2

URL = 'http://news.ycombinator.com/rss'


class Article:

    def __init__(self, title, URL):
        self.title = title
        self.URL = URL


def getTopGoogleNewsStories(maxResults=None):
    d = feedparser.parse("https://news.google.co.uk/?output=rss")

    count = 0
    articles = []
    for item in d['items']:
        articles.append(Article(item['title'], item['link'].split("&url=")[1]))
        count += 1
        if maxResults and count > maxResults:
            break

    return articles


def getTopHackerNewsArticles(maxResults=None):
    d = feedparser.parse("https://news.ycombinator.com/rss")

    count = 0
    articles = []
    for item in d['items']:
        articles.append(Article(item.title, item.link))
        count += 1
        if maxResults and count > maxResults:
            break
    return articles


def handleSource(text, mic):
    if text and re.search(r'\b(google)\b', text, re.IGNORECASE):
        articles = getTopGoogleNewsStories(maxResults=3)
        titles = [" ".join(x.title.split(" - ")[:-1]) for x in articles]
        mic.say("Here are the current top headlines from Google News.")
    else:
        articles = getTopHackerNewsArticles(maxResults=3)
        titles = [filter(lambda x: x in string.printable, x.title) for x in articles]
        mic.say("Here are the current top headlines from Hacker News.")

    return titles


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, with a summary of
        the day's top news headlines, sending them to the user over email
        if desired.
 
        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    mic.say("Google News or Hacker News")
    titles = handleSource(mic.activeListen(), mic)

    for title in titles:
        mic.say(title)


    def handleResponse(text):

        def extractOrdinals(text):
            output = []
            service = NumberService()
            for w in text.split():
                if w in service.__ordinals__:
                    output.append(service.__ordinals__[w])
            return [service.parse(w) for w in output]

        if text == "":
            return False

        chosen_articles = extractOrdinals(text)
        send_all = not chosen_articles and app_utils.isPositive(text)

        if send_all or chosen_articles:
            mic.say("Sure, just give me a moment")

            if profile['prefers_email']:
                body = "<ul>"

            def formatArticle(article):
                tiny_url = app_utils.generateTinyURL(article.URL)

                if profile['prefers_email']:
                    return "<li><a href=\'%s\'>%s</a></li>" % (tiny_url,
                                                           article.title)
                else:
                    return article.title + " -- " + tiny_url

            for idx, article in enumerate(articles):
                if send_all or (idx + 1) in chosen_articles:
                    article_link = formatArticle(article)

                    if profile['prefers_email']:
                        body += article_link
                    else:
                        if not app_utils.emailUser(profile, SUBJECT="",
                                                   BODY=article_link):
                            mic.say("I'm having trouble sending you these " +
                                    "articles. Please make sure that your " +
                                    "phone number and carrier are correct " + 
                                    "on the dashboard.")
                            return

            # if prefers email, we send once, at the end
            if profile['prefers_email']:
                body += "</ul>"
                if not app_utils.emailUser(profile,
                                           SUBJECT="Your Top Headlines",
                                           BODY=body):
                    mic.say("I'm having trouble sending you these articles. " +
                            "Please make sure that your phone number and " +
                            "carrier are correct on the dashboard.")
                    return

            mic.say("All set")

        else:

            mic.say("OK I will not send any articles")


    if 'phone_number' in profile:
        mic.say("Would you like me to send you these articles? " +
                "If so, which?")
        handleResponse(mic.activeListen())


def isValid(text):
    """
        Returns True if the input is related to the news.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(news|headline)\b', text, re.IGNORECASE))
