from collections import namedtuple
from queue import Empty
from math import isclose
import logging
import ssl
import irc.bot
import time
import requests
from bot.clients.twitch.TwitchApi import TwitchApi
import re


TwitchCommand = namedtuple("TwitchCommand", ["tags",
                                             "badges",
                                             "user",
                                             "action",
                                             "args"])
TwitchCommand.__doc__ = """A command from or to the Twitch bot core.

Represents both commands originating from the Twitch
bot core, and commands being sent to it.

For commands being sent TO the Twitch bot core, the
tags, badges, and user fields are currently unused.

tags : dict
    A dictionary containing tags attached to a Twitch chat message.
badges : dict
    A dictionary containing Twitch badges and their version number.
user : TwitchUser
    The name and status info of the user who sent the Twitch command.
action : str
    The text after the "!" and before the first space in the command.
args : str
    The text after the first space which appears in the command (or None)
"""


TwitchUser = namedtuple("TwitchUser", ["name",
                                       "follower",
                                       "subscriber",
                                       "subscriber_duration",
                                       "moderator",
                                       "broadcaster"])
TwitchUser.__doc__ = """A Twitch user and associated status information.

Contains the username of the Twitch user, along with
information on whether the user is a follower, subscriber,
moderator, and/or broadcaster.

name : str
    The username of the Twitch user.
follower : bool
    Whether or not this user is following the channel owner.
subscriber : bool
    Whether or not this user is subscribeed to the channel owner.
subscriber_duration : str
    How long the user has been subscribed, or None if N/A.
moderator : bool
    Whether or not this user is a moderator of this channel.
broadcaster : bool
    Whether or not this user is the broadcaster themself.
"""


class TwitchBotCore(irc.bot.SingleServerIRCBot):
    """
    Twitch bot core.
    
    The "core" of the bot, which handles the IRC connection
    and interaction with the Twitch API. This is distinguished
    from the main "Twitch bot" because it runs in its own thread
    and passes data to the main thread via queues.
    
    This class handles message parsing, user status gathering
    including gathering follower status via the Twitch API,
    and communicates with the outside world entirely via
    TwitchCommands.
    
    The connection to the Twitch chat server is assumed to be
    done via a TLS secured connection. Unencrypted connections
    are NOT supported, although the __init__ method can be
    manually modified to achieve this result if desired.
    
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
    out_queue : Queue.Queue
        Queue the core uses to send commands to the main thread.
    in_queue : Queue.Queue
        Queue the cores uses to receive commands from the main thread.
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
    start() -> no return
        Loops forever. Gets the latest messages from the IRC server,
        parses them for commands, and manages both input and output
        queues. Send a "shutdown" command via the input queue to quit.
    """

    def __init__(self,
                 server, port, username,
                 chat_token, channel,
                 out_queue, in_queue,
                 cooldown, timeout,
                 api_client_id,
                 api_client_secret,
                 no_cooldown):
        self.chat_token  = chat_token
        self.channel     = channel
        self.cooldown    = cooldown
        self.timeout     = timeout
        self.out_queue   = out_queue
        self.in_queue    = in_queue
        self.no_cooldown = set(no_cooldown)

        self.twitch_api = TwitchApi(api_client_id,
                                    api_client_secret)

        self.log = logging.getLogger(__name__)


        # Here we assume the channel name is the same as the
        # name of the broadcaster we are running for.
        self.user_id = self.twitch_api.get_user_id(self.channel.lstrip("#"))

        self.log.info("Connecting to " + server + " on port " + str(port) + "...")

        ssl_context = ssl.SSLContext()
        ssl_factory = irc.connection.Factory(wrapper = ssl_context.wrap_socket)
        super().__init__([(server, port, 'oauth:' + chat_token)],
                         username, username,
                         connect_factory = ssl_factory)

    def __del__(self):
        """Disconnects the bot on shutdown."""

        self.log.info("Disconnecting...")
        self.connection.disconnect()

    def _get_user_info(self, source, badges, tags):
        """Gets user info (name, privileges) from chat tags and API"""

        self.log.debug("Parsing user info for source %s..." % source)

        # According to spec, nickname can be <nickname!username@server>,
        # <nickname@server>, or <nickname>, so try all three.

        if "!" in source:
            name = source.split("!", 1)[0]
        elif "@" in source:
            name = source.split("@", 1)[0]
        else:
            name = source

        # Need to query twitch API to get follower status; other
        # statuses are included with the chat data as badges.
        try:
            follower = self.twitch_api.is_follower(tags["user-id"],
                                                   self.user_id)
        except requests.RequestException as e:
            self.log.warning("Error getting follower info from API: %s" % str(e))
            follower = False
        moderator   = True if "moderator" in badges else False
        broadcaster = True if "broadcaster" in badges else False
        subscriber  = True if "subscriber" in badges else False
        if subscriber:
            subscriber_duration = badges["subscriber"]
        else:
            subscriber_duration = None

        self.log.debug("Got data for user %s:"
                       " (follower: %s, moderator: %s,"
                       " broadcaster: %s, subscriber: %s(%s))"
                       % (name, follower, moderator,
                          broadcaster, subscriber,
                          str(subscriber_duration)))

        return TwitchUser(name,
                          follower,
                          subscriber,
                          subscriber_duration,
                          moderator,
                          broadcaster)

    def _parse_command(self, e):
        """Parses a twitch message and turns it into a command."""

        # Extract command and arguments, if present.
        #cmd = e.arguments[0].lstrip("! ")
        cmd = re.findall(r'!\w+', e.arguments[0])[0].lstrip("! ")
        if " " in cmd:
            action, args = cmd.split(" ", 1)
        else:
            action = cmd.strip()
            args = None

        self.log.debug("Parsed command: %s(%s)"
                       % (action, args))

        # Extract tags, which are stored as a list
        # of two-element dictionaries containing
        # "key" and "value" keys, for some reason?
        tags = dict()
        for tag in e.tags:
            try:
                tags[tag["key"]] = tag["value"]
            except (TypeError, KeyError):
                pass

        if tags:
            self.log.debug("Found tags attached to action '%s': %s"
                           % (action, str(list(tags.keys()))))
        else:
            self.log.debug("Didn't find any tags attached to action '%s'."
                           % action)

        # Parse badges, which are comma-delimited
        # elements in the form badge_name/badge_version.
        badges = dict()
        if "badges" in tags and tags["badges"] is not None:
            for badge in tags["badges"].split(","):
                try:
                    badge_name, badge_version = badge.split("/", 1)
                    badges[badge_name] = badge_version
                except ValueError:
                    pass

        if badges:
            self.log.debug("Found badges in tags: %s"
                        % str(list(badges.keys())))
        else:
            self.log.debug("Didn't find any badges in tags for action '%s'."
                           % action)

        # Get user info from twitch chat data and API
        user = self._get_user_info(e.source,
                                   badges,
                                   tags)

        return TwitchCommand(tags,
                             badges,
                             user,
                             action,
                             args)

    def on_welcome(self, c, e):
        """Joins the desired channel and requests capabilities.
        
        This method is automatically called when the bot connects
        to the server. The capabilities requests are required
        so we receive user information with messages.
        """

        self.log.info('Joining ' + self.channel)

        # Request capabilities for twitch features.
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        """Reacts to a message sent to the twitch channel.
        
        Looks for a command in the given message, and manages
        the cooldown timer and output queue.
        """

        # Ignore messages unless sent to channel of interest.
        if e.target != self.channel:
            return
        
        # Ignore messages that don't start with an exclamation point.
        #if not e.arguments[0].startswith('!'):
        if not '!' in e.arguments[0][0:3]:
            self.log.debug("IGNORING IGNORING IGNORING")
            return

        # Parse the command and place it in the queue if cooldown not active.
        cmd = self._parse_command(e)
        if cmd.action in self.no_cooldown:
            self.log.info("Received whitelisted command '%s(%s)'"
                          " from user '%s' in chat; adding to queue."
                          % (cmd.action, str(cmd.args), cmd.user.name))
            self.out_queue.put(cmd)
        else:
            if isclose(self.cooldown_timer, 0.0, rel_tol = 1e-5):
                self.log.info("Received command '%s(%s)'"
                              " from user '%s' in chat; adding to queue."
                              % (cmd.action, str(cmd.args), cmd.user.name))
                self.out_queue.put(cmd)
                if self.timeout is not None:
                    self.cooldown_timer = self.timeout
            else:
                self.log.info("Ignoring command '%s(%s)'"
                              " from user '%s' in chat"
                              " (received during cooldown)."
                              % (cmd.action, str(cmd.args), cmd.user.name))

    def run_command(self, cmd):
        """Runs a command which came in via the input queue."""

        self.log.info("Running action '%s' from input queue."
                      % cmd.action)

        if cmd.action   == "say":
            args = cmd.args
            self.log.debug("Saying '%s'." % args)
            if isinstance(cmd.args, str):
                args = cmd.args.splitlines()
            for arg in args:
                # IRC limits 512 bytes per message, anything too long must be truncated
                # problem is the python IRC lib does NOT return the message sent to the 
                # bot's queue so we cannot determine the full size of the message as it
                # includes the tags, channel, etc. Therefore, we approximate by limiting 
                # the size of the string itself. 
                # Because Fuck You that's why.
                # Why 450? Because Twitch truncates messages at 499 characters ish
                # for my channel name. Channel name is variable but can be up to 25 chars
                # and we want to add a truncated message to it. Close enough. XD
                if(len(arg) > 450):
                    arg = arg[:450] + "...[message truncated]"
                self.connection.privmsg(self.channel, arg)
        elif cmd.action == "done":
            self.log.debug("Starting cooldown timer.")
            self.cooldown_timer = self.cooldown
        elif cmd.action == "failed":
            self.log.debug("Resetting cooldown timer.")
            self.cooldown_timer = 0.0
        elif cmd.action == "sleep":
            try:
                self.log.debug("Setting cooldown timer to %s seconds."
                               % cmd.args)
                self.cooldown_timer = float(cmd.args)
            except (ValueError, TypeError):
                pass # silently fail for now
        elif cmd.action == "shutdown":
            self.log.info("Shutting down Twitch bot core.")
            self.out_queue.put(cmd)
            raise SystemExit()
        else:
            self.log.info("Did not recognize command '%s'."
                          % cmd.action)

    def init_cooldown_timer(self):
        """Initializes the cooldown timer.
        
        Set the cooldown timer to zero initially,
        and measure the current time so when we
        update we get a sane value for dt.
        """
        
        self.log.debug("Initializing cooldown timer.")
        self.cooldown_timer = 0.0
        self.current_time = time.monotonic()

    def update_cooldown_timer(self):
        """Updates the cooldown timer.
        
        Updates the timer as follows:
            dt = elapsed time since last call
            timer = max(0.0, timer - dt)
        """

        # Calculate dt
        new_time = time.monotonic()
        dt = new_time - self.current_time
        self.current_time = new_time

        # Decrement the cooldown timer
        self.cooldown_timer -= dt
        if self.cooldown_timer < 0.0:
            if self.cooldown_timer + dt > 0.0:
                self.log.debug("Cooldown timer reached zero.")
            self.cooldown_timer = 0.0

    def start(self):
        """Start and manage the Twitch bot core.
        
        This method is responsible for starting the bot,
        polling for messages from the server, updating the
        cooldown timer, and running commands received
        from the input queue.
        """

        self.log.debug("Starting Twitch bot core.")
        self._connect()
        self.init_cooldown_timer()
        self.log.debug("Twitch bot core started. Processing commands.")
        while True:
            self.reactor.process_once(timeout = 0.15)
            self.update_cooldown_timer()
            try:
                self.run_command(self.in_queue.get_nowait())
            except Empty:
                pass
