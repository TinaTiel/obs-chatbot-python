from queue import Queue, Empty
import irc.bot
import logging
import threading
import time
import os
from bot.clients.twitch.TwitchBotCore import TwitchBotCore, TwitchCommand, TwitchUser
from bot.clients.twitch.TwitchApi import TwitchApi


class TwitchBot(object):
    """
    Twitch bot. Meant to be inherited from to create a bot.
    
    Manages the Twitch side of a Twitch bot.
    
    Attributes
    ----------
    server : str
        Address of the Twitch IRC server.
    port : int
        Port on the Twitch IRC server to connect to.
    username : str
        Username to use for Twitch IRC.
    chat_token : str
        Twitch chat OAuth token, used in place of a password.
    channel : str
        Channel to join upon connection. Must start with '#'
    cooldown : float
        Delay after command reports it is finished executing
        until another command can be invoked.
    timeout : float
        Delay until another command can be invoked if current command
        does not report when is finished.
    api_client_id : str
        Client ID from dev.twitch.tv for access to the Twitch API.
    api_client_secret : str
        Client secert from dev.twitch.tv for access to the Twitch API.
    no_cooldown : set
        List of commands which bypass the cooldown timer completely.
    
    Methods
    -------
    on_twitch_command(cmd : dict)
        Method which is called by the bot whenever a user
        in chat invokes a command by prepending their message with '!'.
        The cmd dict is a dict version of TwitchCommand and TwitchUser.
    twitch_say(text : str)
        Have the bot say something in Twitch chat.
    twitch_done()
        Inform the bot that your action has completed.
        This starts the bot's cooldown timer.
    twitch_failed()
        Inform the bot that your action has failed.
        This allows another action to be started immediately.
    twitch_sleep(float : duration)
        Tell the bot to stop responding to commands for a given time.
    twitch_shutdown()
        Tell the bot to shut down.
    start()
        Start the Twitch bot core in its own thread. Call only once.
    run_forever() -> no return
        Run eternally, forever polling for commands from the bot,
        invoking the on_twitch_command method whenever one is received.
    run_once(block : bool, timeout : float)
        Poll once for commands from the bot. Invokes the
        on_twitch_command method when a command is received.
        See documentation for Python's Queue.Queue for information
        about the block and timeout parameters.
    get_twitch_command(block : bool, timeout : float) -> dict
        Behaves similarly to run_once. The only difference is this
        function returns the dictionary representing the command
        and does NOT call on_twitch_command.
    """

    def __init__(self,
                 server, port, username,
                 chat_token, channel,
                 cooldown, timeout,
                 api_client_id,
                 api_client_secret,
                 no_cooldown):
        self.server            = server
        self.port              = port
        self.username          = username
        self.chat_token        = chat_token
        self.channel           = channel
        self.cooldown          = cooldown
        self.timeout           = timeout
        self.api_client_id     = api_client_id
        self.api_client_secret = api_client_secret
        self.no_cooldown       = no_cooldown

        self.out_queue  = Queue()
        self.in_queue   = Queue()

        self.log = logging.getLogger(__name__)

    def _decode_twitch_command(self, cmd):
        """Converts TwitchCommand and TwitchUser to dictionaries."""

        # Special shutdown command straight from bot with no
        # user data means an internal shutdown command was received.
        # Shut down immediately if that happens.
        if cmd.user == None and cmd.action == "shutdown":
            self.log.info("Twitch bot core is shutting down; quitting.")
            self.twitch_bot_core_thread.join()
            raise SystemExit()

        cmd = cmd._asdict()
        cmd["user"] = cmd["user"]._asdict()

        return cmd

    def on_twitch_command(self, cmd):
        """Override this method to implement bot behavior.
        
        This is called by the bot whenever a user in chat invokes
        a command by prepending their message with '!'.
        
        Parameters
        ----------
        cmd : dict
            A dict version of TwitchCommand and TwitchUser named tuples.
        """
        self.log.info("Received commmand '%s(%s)' but no handler is specified."
                      % (cmd.action, str(cmd.args)))
        pass

    def twitch_say(self, text):
        """Has the bot say something in Twitch chat.
        
        Parameters
        ----------
        text : str
            The text to say in chat.
        """

        self.log.info("Telling Twitch bot core to say '%s'"
                      % text)
        msg = TwitchCommand(None, None, None, "say", text)
        self.in_queue.put(msg)

    def twitch_done(self):
        """Informs the bot that your action has completed.
        
        This starts the bot's cooldown timer.
        """

        self.log.info("Telling Twitch bot core to start cooldown timer.")
        msg = TwitchCommand(None, None, None, "done", None)
        self.in_queue.put(msg)

    def twitch_failed(self):
        """Informs the bot that your action has failed.
        
        This allows another action to be started immediately.
        """

        self.log.info("Telling Twitch bot core to reset cooldown timer.")
        msg = TwitchCommand(None, None, None, "failed", None)
        self.in_queue.put(msg)

    def twitch_sleep(self, duration):
        """Tells the bot to stop responding to commands for a given time.
        
        Makes the bot "sleep" by setting its cooldown timer.
        
        Parameters
        ----------
        duration : float
            How many seconds the bot should ignore commands for.
        """

        self.log.info("Telling Twitch bot core to sleep for %s seconds."
                      % str(duration))
        msg = TwitchCommand(None, None, None, "sleep", duration)
        self.in_queue.put(msg)

    def twitch_shutdown(self):
        """Tells the bot to shut down."""

        self.log.info("Telling Twitch bot core to shut down.")
        msg = TwitchCommand(None, None, None, "shutdown", None)
        self.in_queue.put(msg)

    def _start(self):
        """Thread which contains the twitch bot core."""

        self.log.info("Twitch bot core thread started.")
        twitch_bot_core = TwitchBotCore(self.server, self.port, self.username,
                                        self.chat_token, self.channel,
                                        self.out_queue,  self.in_queue,
                                        self.cooldown,   self.timeout,
                                        self.api_client_id,
                                        self.api_client_secret,
                                        self.no_cooldown)
        twitch_bot_core.start()

    def start(self):
        """Starts the Twitch bot core in its own thread. Call only once."""

        self.log.info("Starting Twitch bot core thread.")
        self.twitch_bot_core_thread = threading.Thread(target = self._start)
        self.twitch_bot_core_thread.name = "TwitchBotCoreThread"
        self.twitch_bot_core_thread.start()

    def run_forever(self):
        """Run this if you want to let the bot control the program.
        
        Runs eternally, forever polling for commands from the bot,
        invoking the on_twitch_command method whenever one is received.
        """
        if(os.name == 'nt'):
            self.run_forever_win()

        self.log.info("Twitch bot is running forever on Linux/OSX (not Windows).")
        while True:
            try:
                cmd = self.get_twitch_command()
                self.log.info("Twitch bot received command '%s(%s)'."
                              % (cmd["action"], str(cmd["args"])))
                self.on_twitch_command(cmd)
            except KeyboardInterrupt:
                self.twitch_shutdown()

    def run_forever_win(self):
        """Run this if you want to let the bot control the program on Windows.
        
        Runs eternally, forever polling for commands from the bot,
        invoking the on_twitch_command method whenever one is received.
        """
        self.log.info("Twitch bot is running forever on Windows.")
        while True:
            try:
                try:
                    cmd = self.get_twitch_command(block = False)
                except Empty:
                    pass
                else:
                    self.log.info("Twitch bot received command '%s(%s)'."
                                  % (cmd["action"], str(cmd["args"])))
                    self.on_twitch_command(cmd)
                time.sleep(0.1)
            except KeyboardInterrupt:
                self.twitch_shutdown()
            except:
                self.twitch_shutdown()
                raise

    def run_once(self, block = True, timeout = None):
        """Run this if you want to control the program yourself.
        
        Polls once for commands from the bot. Invokes the
        on_twitch_command method when a command is received.
        See documentation for Python's Queue.Queue for information
        about the block and timeout parameters.
        """

        try:
            self.log.info("Twitch bot waiting for single command.")
            cmd = self.get_twitch_command(block, timeout)
            self.on_twitch_command(cmd)
        except Empty:
            pass

    def get_twitch_command(self, block = True, timeout = None):
        """Run this if you don't want to use on_twitch_command at all.
        
        Behaves similarly to run_once. The only difference is this
        function returns the dictionary representing the command
        and does NOT call on_twitch_command.
        
        Returns
        -------
        dict
            A dict version of TwitchCommand and TwitchUser named tuples.
        """

        return self._decode_twitch_command(self.out_queue.get(block, timeout))

