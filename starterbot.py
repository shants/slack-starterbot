import os
import time
from slackclient import SlackClient
import datetime

#shants changes

import re
#import urllib2
import requests

class BookMyShowClient(object):
    NOW_SHOWING_REGEX = '{"event":"productClick","ecommerce":{"currencyCode":"INR","click":{"actionField":{"list":"Filter Impression:category\\\/now showing"},"products":\[{"name":"(.*?)","id":"(.*?)","category":"(.*?)","variant":"(.*?)","position":(.*?),"dimension13":"(.*?)"}\]}}}'
    #COMING_SOON_REGEX = '{"event":"productClick","ecommerce":{"currencyCode":"INR","click":{"actionField":{"list":"category\\\/coming soon"},"products":{"name":"(.*?)","id":"(.*?)","category":"(.*?)","variant":"(.*?)","position":(.*?),"dimension13":"(.*?)"}}}}'

    def __init__(self, location = 'Bengaluru'):
        self.__location = location.lower()
        self.__url = "https://in.bookmyshow.com/%s/movies" % self.__location
        self.__html = None

    def __download(self):
        req = requests.get(self.__url) 
        #urllib2.Request(self.__url, headers={'User-Agent' : "Magic Browser"})
        html = req.text #urllib2.urlopen(req).read()
        return html

    def get_now_showing(self):
        if not self.__html:
            self.__html = self.__download()
            now_showing = re.findall(self.NOW_SHOWING_REGEX, self.__html)
        return now_showing
        #return self.__html

    def get_coming_soon(self):
        if not self.__html:
            self.__html = self.__download()
            coming_soon = re.findall(self.COMING_SOON_REGEX, self.__html)
        return coming_soon


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    if "do day" in command:
	    response = "Hello, the day is -- " +  datetime.date.today().strftime("%A") + ", " + datetime.date.today().strftime("%B") + " " + datetime.date.today().strftime("%d") 
    if "do movie" in command:
	    bms_client = BookMyShowClient('Bengaluru')
	    now_showing = bms_client.get_now_showing()
	    response = "Hello, Movie list in Bengaluru == "
	    for m in now_showing:
	        response +=str(m)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
