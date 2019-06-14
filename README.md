# About
OBS Chat Bot is a set of Python scripts that allows your viewers to cause actions directly in OBS during broadcasts! For example, an user may invoke a `!pride` command and your OBS instance would briefly show a rainbow flag. Or, a series of users may vote to execute the `!special` command to change scenes in some interactive fun way. The possibilities are endless as OBS Websockets.

# Dependencies
This project requires Python 3+, and dependencies are defined in requirements.txt. Install them with:
```
pip install -r requirements.txt
```
This project also depends on [OBS Websockets](https://obsproject.com/forum/resources/obs-websocket-remote-control-of-obs-studio-made-easy.466/) and was tested in versions 23.1 of OBS studio and 4.6.1 of OBS Websockets. 

# Setup / Authentication
1. Rename `config.example.json` to `config.json`.
1. Create a Twitch account to act as your Chat Bot, if you don't already have one.
1. In config.json, set `twitch.username` to your Chat Bot username
1. In config.json, set `twitch.channel` to your broadcaster username
1. Setup your Twitch Application:
   1. Signup at [Twitch Dev](https://dev.twitch.tv) with your broadcaster account.
   1. [Create a new App](https://dev.twitch.tv/console/apps) (NOT an Extension):
       1. Use a meaningful name, such as "Broadcaster Username OBS ChatBot App"
       1. Set the OAuth Redirect URL to something you can access, such as http://localhost
       1. Set the category to Chat Bot
   1. In config.json, set `twitch.api_client_id` and `twitch.app_client_secret` from your app you just created. Note, you should NEVER share the client secret, treat it as a password.
1. Authorize your Chat Bot access to Twitch chat:
   1. Login to Twitch as your Chat Bot account, and navigate to https://twitchapps.com/tmi to generate a chat token.
   2. In config.json, set `twitch.chat_token` to the token you receive after authorizing access to your Chat Bot.
1. Authorize access to OBS:
   1. If you haven't already, install  [OBS Websockets](https://obsproject.com/forum/resources/obs-websocket-remote-control-of-obs-studio-made-easy.466/) and set your credentials in _OBS > Tools > Websocket Server Settings_. 
   1. In config.json, set your OBS websocket credentials (`obs.obs_websockets.host`, `obs.obs_websockets.port`, and `obs.obs_websockets.password`).
1. Verify your setup is working correctly by running the bot...
   ```
   python startBot.py
   ```
   ...And executing these commands in your chat (from Twitch, or OBS -- doesn't matter):
   ```
   yourname: !test
   ```
   If working, the bot will respond in Twitch chat with some basic information about you and with your OBS Websockets version. Note this command can only be executed by the broadcaster (you).
   ```
   yourbot: All systems up and running @yourname, running OBS Websockets version 4.6.1
   ```
You are now setup! See the documentation below on the commands you can execute.

# Commands
The configuration file `config.json` includes several examples of commands that can be configured. 
The elements of a command are described below:
`name`: Name of the chat command an user would type, without the !. Examples: 'party', 'pride', 'letschat', etc.
`action`: The overall behavior that will occur when an user executes a chat command. These are the actions available by default, they are just dynamically-loaded python classes available in obs/actions. 
`args`: The arguments required to describe what the action does

This table below describes the `action`/`args` configurations available. If the configuration is invalid, it will be printed to the command line that invoked the bot. 

| action        | What This Does                                                                                                          | mandatory args                                                                                           | optional args                                                                  |
|---------------|-------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| SetScene      | Changes to a scene permanently                                                                                          | `scene` (string): The scene to switch to                                                                 | (none)                                                                         |
| ShowSceneItem | Shows a scene item for a specified duration. Defaults to the item in the current scene unless parent scene is specified | `scene_item` (string): The scene item to show/hide <br> `duration` (integer): Seconds to show the scene item | `scene` (string): The scene the scene item is nested in. Depth does not matter |
| Alias         | Simply executes the command specified                                                                                   | `command_name` (string): The command name to execute                                                     | (none)                                                                         |

`min_votes`: Describes the minimum number of unique votes needed to execute a command. Must be greater than zero. 
`permission`: The minimum status required to execute a command. Can be `EVERYONE`, `FOLLOWER`, `SUBSCRIBER`, `MODERATOR`, or `BROADCASTER`. 

### Extending Commands
Commands are just classes in the `obs/actions` directory, initialized dynamically with arguments in config.json when the bot starts up. The only hard requirements for these classes are:
1. The initializtion function must accept the `obs_client`, `command_name`, `permission`, `min_votes`, and `args` arguments. 
2. There must be an `execute` method accepting an `user` argument. 

Optionally you may use `eval_permission` and `eval_votes` if necessary. Refer to [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py) and the source code here for examples.