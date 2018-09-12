import os
import time
import re
from googlesearch import search
from slackclient import SlackClient

# instantiate slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
DELAY = 1  # 1 second delay


def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Regex match for google search
    bot_response = re.match(r".*?\W*(google)\s+\b(.*)", command.lower())
    # This is where you start to implement more commands!

    if bot_response:
        query = bot_response.group(2)
        tmp = [i for i in search(query, tld="co.in", num=10, stop=1, pause=2)]
        try:
            response = tmp[0]
        # Exception for index out of range
        except IndexError:
            response = "No Search"
    else:
        return
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Bot running!")
        # Read bot's user ID by calling Web API method `auth.test`
        while True:
            events = slack_client.rtm_read()
            for event in events:
                if (
                    'channel' in event and
                    'text' in event and
                    event.get('type') == 'message'
                ):
                    channel = event['channel']
                    command = event['text']
                    if command:
                        handle_command(command, channel)
                    time.sleep(DELAY)
    else:
        print("Connection failed.")