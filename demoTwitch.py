import logging
import time
import json
import os
from twitch.TwitchBot import TwitchBot

#logging.basicConfig(level=logging.DEBUG, filename='debug.log')
logging.basicConfig(level=logging.INFO)


# Pretty print a dictionary.
def pretty_print_dict(d, depth = 0):
    for k,v in d.items():
        if isinstance(v, dict):
            print("%s:" % k)
            pretty_print_dict(v, depth + 1)
        else:
            print(("    " * depth) +
                  "%s: %s" % (k,v))


# Demo implementation.
class PrintCommandBot(TwitchBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_twitch_command(self, cmd):
        print("-----------------")
        print("Received command:")
        pretty_print_dict(cmd)

        if cmd["action"] == "say":
            if cmd["args"]:
                self.twitch_say(cmd["args"])
            else:
                self.twitch_say("What do you want me to say?")
        elif cmd["action"] == "shutdown":
            if cmd["args"] == "please":
                self.twitch_shutdown()
            else:
                self.twitch_say("You didn't say the magic word.")
        else:
            self.twitch_say("I don't know that command.")
        self.twitch_failed() # Always "fail" so cooldown timer is not used.

# Example of using the Twitch bot with run_forever.
# This allows the bot to control the execution flow
# of your program. All you have to do is handle the
# on_twitch_command function.
def main():
    testbot = PrintCommandBot(**getConfig())
    testbot.start()
    testbot.run_forever()


# Example of using the Twitch bot with run_once. This
# allows your program to remain in control of execution flow
# by manually polling for twitch commands.
#
# Be sure to catch KeyboardInterrupt and pass a twitch_shutdown
# command or the bot probably won't want to shut down.
# (The KeyboardInterrupt could occur outside of run_once and
#  the bot would have no way of knowing it's supposed to stop.)
def main2():
    testbot = PrintCommandBot(**getConfig())
    testbot.start()
    while True:
        try:
            testbot.run_once(block = True, timeout = 1.5)
            print("Doing something else every 1.5 seconds.")
        except KeyboardInterrupt:
            testbot.twitch_shutdown()


# Another example of using the Twitch bot with run_once. This
# allows your program to remain in control of execution flow
# by manually polling for twitch commands.
#
# This version does not block with a timeout, so sleep or
# do something else time consuming between calls to run_once
# or it will use 100% CPU.
def main3():
    testbot = PrintCommandBot(**getConfig())
    testbot.start()
    while True:
        try:
            testbot.run_once(block = False)
            print("Doing something else (sleeping in this case).")
            time.sleep(0.5)
        except KeyboardInterrupt:
            testbot.twitch_shutdown()

def getConfig():
    with open('config.json', encoding='utf-8') as json_file:
        try:
            data = json.load(json_file)
        except Exception as e:
            print("Cannot read config.json! Error message: \n" + str(e))

    twitch_config = data.get('twitch', None)
    if(twitch_config is None):
        print("Cannot initialize, missing twitch configuration information!")

    return twitch_config

# Run main code if this module is executed from the command line.
if __name__ == "__main__":
    main()
    #main2()
    #main3()