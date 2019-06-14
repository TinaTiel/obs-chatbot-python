from collections import namedtuple
import requests
import logging
import time
from FuncCache import FuncCache


AppToken = namedtuple("AppToken", ["data", "expires"])
AppToken.__doc__ = """App token used to authorize API access.

data : str
    The token itself, stored as a string.
expires : int
    The time in seconds (unix timestamp) at which this token expires.
"""

class TwitchApi(object):
    """
    Twitch API class.
    
    Provides access to various Twitch APIs, and manages
    app tokens automatically. API call results are
    cached by default.
    
    Attributes
    ----------
    client_id : str
        Twitch client ID, from dev.twitch.tv.
    client_secret : str
        Twitch client secret, from dev.twitch.tv.
    
    Methods
    -------
    is_follower(from_id : str, to_id : str) -> bool
        Check whether from_id is a follower of to_id.
    
    get_user_id(target_user : str) -> str
        Return the numerical user ID of the given username.
    """

    def __init__(self, client_id, client_secret):
        self.client_id     = client_id
        self.client_secret = client_secret
        self.app_token     = AppToken(None, 0)
        self.log = logging.getLogger(__name__)

    def _refresh_app_token(self):
        """Refreshes the Twitch app token when necessary.
        
        This method will request a new app token when
        the existing one is near or at expiration.
        has expired.
        
        See: https://dev.twitch.tv/docs/authentication
                    /getting-tokens-oauth/#oauth-client-credentials-flow
        """

        # Do nothing if the token is not nearing expiration.
        if self.app_token.expires > (time.time() + 5*60):
            self.log.debug("Twitch API token is still fresh.")
            return
        
        if self.app_token.expires > time.time():
            self.log.debug("Twitch API token expires in %d seconds."
                           " Getting new token."
                           % (self.app_token.expires - time.time()))
        else:
            self.log.debug("Twitch API token expired %d seconds ago."
                           " Getting new token."
                           % (time.time() - self.app_token.expires))

        # Generate a request to the Twitch API endpoint for
        # requesting an app token.
        params = {
            "client_id"     : self.client_id,
            "client_secret" : self.client_secret,
            "grant_type"    : "client_credentials"
        }

        try:
            # Allow requests to raise an exception on error.
            response = requests.post("https://id.twitch.tv/oauth2/token",
                                     params = params)
            response.raise_for_status()
        except RequestException as e:
            # If expired, raise exception. Otherwise, just log a warning.
            if time.time() > self.app_token.expires:
                self.log.warning("Failed to refresh Twitch API token: %s"
                                 % str(e))
            else:
                raise
        else:
            # Convert response to json.
            data = response.json()
            self.app_token = AppToken(data["access_token"],
                                      data["expires_in"])

    def _call_api(self, action, endpoint, params):
        """Helper method that makes the actual Twitch API call.
        
        This method automatically refreshes the app token and
        adds it as a header to the request.
        
        Parameters
        ----------
        action : str
            HTTP action verb
        endpoint : str
            Portion of the Twitch API URL after /helix/
        params : dict
            Query parameters as required for the request.
        
        Returns
        -------
        dict
            Dictionary containing the JSON response from Twitch.
        """
        
        # Try to refresh the app token first.
        self._refresh_app_token()

        self.log.debug("Calling Twitch API: %s %s(%s)"
                       % (action, endpoint, str(params)))
        headers = {
            "Authorization": "Bearer %s" % self.app_token.data
        }
        response = requests.get("https://api.twitch.tv/helix/%s"
                                % endpoint.strip("/"),
                                params  = params,
                                headers = headers)
        response.raise_for_status()
        return response.json()

    @FuncCache(size = 1000, expiry = 5.0)
    def is_follower(self, from_id, to_id):
        """Checks whether from_id is a follower of to_id.
        
        See: https://dev.twitch.tv/docs/api
                    /reference/#get-users-follows

        Parameters
        ----------
        from_id : str
            Numerical user ID of the following user.
        to_id : str
            Numerical user ID of the followed user.
        
        Returns
        -------
        bool
            True if user from_id is following user to_id.
        """

        self.log.info("Calling Twitch API: Does user ID %s follow user ID %s?"
                      % (from_id, to_id))
        response = self._call_api("GET", "/users/follows",
                                  {"from_id": from_id, "to_id": to_id})
        self.log.info("Twitch API response: %s"
                      % ("Yes" if response["total"] == 1 else "No"))
        if response["total"] == 1:
            return True
        else:
            return False

    @FuncCache(size = 1000, expiry = 5.0)
    def get_user_id(self, login):
        """Returns the numerical user ID of the given username.
        
        See: https://dev.twitch.tv/docs/api
                    /reference/#get-users

        Parameters
        ----------
        login : str
            The user's username.
        
        Returns
        -------
        str
            Numerical user ID.
        """

        self.log.info("Calling Twitch API: What is %s's user ID?"
                      % login)
        response = self._call_api("GET", "users",
                                  {"login": login})
        self.log.info("Twitch API response: %s's user ID is %s"
                      % (login, response["data"][0]["id"]))
        return response["data"][0]["id"]
