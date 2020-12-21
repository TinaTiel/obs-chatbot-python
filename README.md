# About
OBS Chat Bot is a set of Python scripts that allows your viewers to cause actions directly in OBS during broadcasts! For example, a viewer may invoke a `!tiel` command and your OBS instance would briefly show a bird mov file. Or, a series of viewers may vote to execute the `!special` command to change scenes in some interactive fun way.

# Holup
I'm working on an improved version of this in Java that will address issues of stability and concurrency observed in the Pthon version here. 

It works. 
Most of the Time.

You're free to use it, but please be aware I'm not spending anymore time on this.
You're of course welcome to fork this repository and develop on your own independently.

# Dependencies
This project requires Python 3+, and dependencies are defined in requirements.txt. Install them with:
```
pip install -r requirements.txt
```
This project also depends on [OBS Websockets](https://obsproject.com/forum/resources/obs-websocket-remote-control-of-obs-studio-made-easy.466/) and was developed in Windows 7 and Linux on versions 23.1 of OBS studio (not Streamlabs OBS) and 4.6.1 of OBS Websockets.

# Setup / Authentication
1. Rename `config.example.json` to `config.json`.
1. Create a Twitch account to act as your Chat Bot, if you don't already have one.
1. In config.json, set `twitch.viewername` to your Chat Bot viewername
1. In config.json, set `twitch.channel` to your broadcaster viewername
1. Setup your Twitch Application:
   1. Signup at [Twitch Dev](https://dev.twitch.tv) with your broadcaster account.
   1. [Create a new App](https://dev.twitch.tv/console/apps) (NOT an Extension):
       1. Use a meaningful name, such as "Broadcaster viewername OBS ChatBot App"
       1. Set the OAuth Redirect URL to something you can access, such as http://localhost
       1. Set the category to Chat Bot
   1. In config.json, set `twitch.api_client_id` and `twitch.app_client_secret` from your app you just created. Note, you should NEVER share the client secret, treat it as a password.
1. Authorize your Chat Bot access to Twitch chat:
   1. Login to Twitch as your Chat Bot account, and navigate to https://twitchapps.com/tmi to generate a chat token.
   1. In config.json, set `twitch.chat_token` to the token you receive after authorizing access to your Chat Bot.
1. Authorize access to OBS:
   1. If you haven't already, install  [OBS Websockets](https://obsproject.com/forum/resources/obs-websocket-remote-control-of-obs-studio-made-easy.466/) and set your credentials in OBS at _Tools > Websocket Server Settings_. 
   1. In config.json, set your OBS websocket credentials (`obs.host`, `obs.port`, and `obs.password`).
1. Add your chatbot as moderator on your broadcaster channel (if you do not, you'll see errors such as 'Your message was not sent because you are sending messages too quickly'):
   ```
   /mod YourChatBot
   ```
1. Verify your setup is working correctly by running the bot...
   ```
   python startBot.py
   ```
   ...And executing these commands in your chat (from Twitch, or OBS -- doesn't matter):
   ```
   yourname: !obsstatus
   ```
   If working, the bot will respond in Twitch chat with some basic information about you and with your OBS Websockets version. Note this command can only be executed by the broadcaster (you).
   ```
   yourname: !obsstatus
   yourbot: Twitch Bot is up and running. Connected to OBS Websockets version 4.6.1.
   ```
   If not, you may get a message like this; this means the bot cannot connect to OBS Websockets. If OBS is running, verify that the connection information is correct.
   ```
   yourname: !obsstatus
   yourbot: Twitch Bot is up and running. Could not communicate with OBS. Exception: socket is already closed
   ```
   After addressing the underlying problem, you can then attempt to reconnect with the commands `reconnect`, `reset` or `recover`. If necessary, you can restart the bot with `CTRL-C` in the command line where you launched it.
   ```
   yourname: !reconnect
   bot: Attempting to reconnect to OBS...
   bot: Twitch Bot is up and running. Connected to OBS Websockets version 4.6.1
   ```

You are now setup! See the documentation below on the commands you can configure in `obs.commands`.

# Commands

## Built-In Commands
These commands are part of the bot itsself and cannot be disabled without changing the statements in startBot.py. 

`obsstatus`: Displays the status of the bot and connection to OBS. Only the broadcaster can execute this command.

`reconnect`: Tries to reconnect the bot to OBS, up to three attempts. Only the broadcaster can execute this command. Can also be invoked as `reset` or `recover`.

## Custom Commands
Custom command can be configured by you, the broadcaster, to make OBS respond in any number of ways. The configuration file `config.json` includes several examples of commands that can be configured, and the elements of a command are described below: 

`disabled` (optional): When `true` then the command is not made available. Default is `false` if not provided.

`name`: Name of the chat command a viewer would type (**_without the `!`_**). For example, if an user types _!hype_ then there must exist a command with the name _hype_.

`description`: Description for the chat command; used in the !help command, and displayed during votes. 

`aliases`: List of strings that also execute this command, for example the command _birb_ may also have aliases _tiel_ and _squawk_; this means viewers may also invoke the !birb command with !tiel and !squawk. 

`min_votes`: Describes the minimum number of unique votes needed to execute a command. Must be greater than zero. The Broadcaster and any Moderators skip voting validation.

`permission`: The minimum status required to execute a command. Can be `EVERYONE`, `FOLLOWER`, `SUBSCRIBER`, `MODERATOR`, or `BROADCASTER`. 

`action`: The overall behavior that will occur when a viewer executes a chat command. These are the actions available by default, they are just dynamically-loaded python classes available in obs/actions. 

`args`: The arguments required to describe what the action does

This table below describes the `action`/`args` configurations available. If the configuration is invalid, it will be printed to the command line. 

| action | What This Does | mandatory args | optional args |
|--------|----------------|----------------|---------------|
| Help | Responds in chat with each available command that has been configured (one message per command since IRC doesn't natively support newlines in a single chat message) | (none) | `short` (Boolean): If `true` then will print all the command names in a single chat message (excluding description); otherwise the default behavior is to send a chat message for each command with its full description. |
| ShowScene | Changes to a scene permanently | `scene` (string): The scene to switch to | `duration` (integer): Seconds to show the scene. Permanent if not specified. |
| ShowSource / HideSource | Shows/Hides a scene item for a specified duration. Defaults to the item in the current scene unless parent scene is specified | `source` (string or list): The source to show/hide. If provided as a list, then `pick_from_group` is ignored and a scene is picked randomly from the specified list. | `scene` (string): The scene the scene item is nested in. Depth/nesting does not matter; if a scene is included in another scene, the item will still be shown/hidden. <br> `duration` (integer): Seconds to show/hide the scene source. Permanent if not specified. <br> `pick_from_group` (true/false): If `true`, then it treats the specified source as a group, picking a child source from the group to show/hide <br> **If this doesn't behave correctly after adding/removes groups/sources in OBS** try restarting OBS to clear OBS's cache. |
| Say | Says a series of texts in chat, in order | `messages` (list): List of messages to say in chat <br> **If this fails** after one message then verifiy your chat bot has been granted moderator permissions in your broadcaster channel. | (none) |
| Wait | Waits a specified duration, most useful in a `Chain` command | `duration` (integer): Seconds to wait | (none) |
| Chain | Excecutes a series of commands above, in order | `commands` (list): List of `action` and `args` data commands, describing the commands to execute. <br> Each command inherits the parent attributes for `name`, `description`, `aliases`, `min_votes`, and `permission`; these do not need to be provided | (none) |
| Toggle | hides/shows a pair of sources simulataneously | `toggle_on` (object) & `toggle_off` (object): Sources to show / hide simultaneously. Takes same arguments as `ShowSource` and `HideSource`, but will ignore any randomization-related features | `duration` (integer): Seconds to wait between swaps; if omitted then permanent. |

## Custom Command Action Classes
Command actions are subclasses of the Action class, see examples in the `obs/actions` directory, and are initialized dynamically with arguments in config.json when the bot starts up. 

When returning from an error or success on the execute() command, call `self._twitch_failed()` or `self._twitch_done()` and return a Boolean (the Boolean is required for the Chain command). After a chat command, the chat bot waits for one of these calls before accepting more chat commands; the difference is that `self._twitch_failed()` has no cooldown whereas `self._twitch_done()` has a cooldown/delay after the command completes. If you want to allow uses to submit commands continuously, return `self._twitch_failed()`, but if you want to limit spamming of commands use `self._twitch_done()`.

You also have the example of saying something in chat in response to a command as well; in this case use `self._twitch_say("some message")` but remember to still call `self.twitch_failed()` or `self.twitch_done()` after each message and note that if you cannot send messages in succession ensure your bot has been added as a moderator on the broadcaster's chat.

Otherwise, refer to [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py) for examples of calling OBS, and refer to the source code here and below for examples of how to create your own commands.

Example Class:
```
import logging
import obswebsocket, obswebsocket.requests
from obs.actions.Action import Action
from obs.Permission import Permission

class Foo(Action):

  def __init__(self, obs_client, command_name, aliases, description, permission, min_votes, args):
    """Initializes this class, see Action.py
    """
    super().__init__(obs_client, command_name, aliases, description, permission, min_votes, args)
    self.log = logging.getLogger(__name__)
    self._init_args(args)

  def execute(self, viewer):
    """Make calls to OBS or whatever you want to do with Python here. These are
    always blocking tasks, so you must tell the twitch bot when you are done via
    twitch_failed() or twitch_done(); see the TwitchBot class.
    """

    # Check viewer permissions and votes
    if(not (
      self._has_permission(viewer) 
      and self._has_enough_votes(viewer) 
      )
    ):
      return self._twitch_failed()
    
    # Check viewer permissions and votes
    if(not (
      self._has_permission(viewer) 
      and self._has_enough_votes(viewer) 
      )
    ):
      self._twitch_failed()
      return False

    # Execute an OBS command, see the obs-websocket-py documentation and NOTE that the 
    # error returning in/out is from the perspective of the class and not this one, so 
    # in/out are opposite of what you may expect
    res = self.obs_client.client.call(obswebsocket.requests.SomeObsWebsocketPyClass(self.somearg, self.anotherarg))
    if(res.status == False):
      self.log.warn("Could not show scene item {}! Error: {}".format(self.source, res.datain['error']))
      self._twitch_failed()
      return False

    self.log.debug("Executed {} successfully".format(self.command_name))
    self._twitch_say("You executed my custom commands!")
    self._twitch_success()
    return True

  def _init_args(self, args):
    """This validates the arguments are valid for this instance, 
    and raises a ValueError if they aren't.
    """
    self.somearg = args.get('somearg', None)
    self.anotherarg = args.get('anotherarg', None)
    if(self.somearg is None or self.anotherarg is None):
      raise ValueError("Command {}: Args error, missing 'somearg' or 'anotherarg'".format(self.command_name))
```
Example Config Entry:
```
{
  "twitch": {
    ...
  },
  "obs": {
    "host": "localhost",
    "port": 4444,
    "password": "password",
    "commands": [
      {
        "name": "somecommand",
        "description": "see a custom command!",
        "aliases": ["somedemand", "someampersand", "icantryhme"],
        "min_votes": 0,
        "permission": "EVERYONE",
        "action": "Foo",
        "args": {
          "somearg": "someargvalue",
          "someotherarg": "someotherargvalue"
        }
      },
      ...
    ]
  }
}
```
And in a Chain command:
```
{
  "twitch": {
    ...
  },
  "obs": {
    "host": "localhost",
    "port": 4444,
    "password": "password",
    "commands": [
      {
        "name": "somechaincommand",
        "description": "see a custom chain command!",
        "aliases": ["somedemand", "someampersand", "icantryhme"],
        "min_votes": 0,
        "permission": "EVERYONE",
        "action": "Chain",
        "args": {
          "commands": [
            {
              "action": "Foo",
              "args": {
                "somearg": "someargvalue",
                "someotherarg": "someotherargvalue"
              }
            },
            ...
          ]
        }
      },
      ...
    ]
  }
}
```

# Other Configuration

`log_level`: Logging level for the program, can be `CRITICAL`, `ERROR`, `WARNING`, `INFO`, or `DEBUG` per the Python 3 [logging](https://docs.python.org/3/library/logging.html) facility. When not set, it defaults to `INFO` so that program startup is shown on the command line.

`twitch.cooldown`: How long (seconds) a viewer must wait until commands can be executed once they've finished (and if the command has cooldown).

`twitch.timeout`: If a command does not internally call `self._twitch_done()` or `self._twitch_failed()` this is the amount of time (seconds) the chatbot will wait. Therefore, if you anticipate some commands may take a long time to execute then you may want to set this to a higher value otherwise your command may be interrupted.

`twitch.no_cooldown`: List of commands such as _help_ that should never have cooldown / can be spammed as frequently as viewers want.
