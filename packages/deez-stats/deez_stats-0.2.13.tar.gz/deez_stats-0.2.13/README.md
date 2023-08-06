![salt]
# deez_stats
Python connection to Yahoo! Fantasy API implementing the yahoo_fantasy_api from [spilchen] 

## Build Status
I'll figure this out one day

## Installation
Eventually, this package can be installed via pip:
```
python3 -m pip install deez-stats (mac)
python -m pip install deez-stats (windows)
```
## Getting Started
First, you need to register your application on Yahoo Developer network to get Oauth credentials. Details found at [Registering Your Application].  

After it is registered, you can see your Client ID (Consumer Key) and Client Secret (Consumer Secret) on the [apps page].

With these two elements, the need to be put into a JSON file with the following format for the ```yahoo_oauth``` package to read it in correctly.
### oauth2.json file format
 ```
{
    "consumer_key": "my_very_long_and_weird_consumer_key",
    "consumer_secret": "my_not_that_long_consumer_secret"
}
 ```
## Sample API Usage
Now with your Yahoo Oauth2 credentials, we will use the ```yahoo_oauth``` package to generate a token.  

First, let's import the needed packages and modules:
```
>>> from yahoo_oauth import OAuth2
>>> import deez_stats as ds
```
Now, we want to generate the Yahoo Oauth2 token from the file containing our credentials:
```
>>> file = 'tokens/yahoo/oauth2.json'
>>> oauth2_token = OAuth2(None, None, from_file=file)
```
After that, we are all set to begin! Right now, there is limited functionality but we can create an object that contains all the league information. Optionally, you can pass it a season and week for a snapshot of the past. Otherwise, it will return the current league information/status.
```
>>> li = ds.LeagueInfo(oauth2_token, season=2021, week=None)
```
You can also get information about all the weekly matchups. Additionally, you can get all the historical info about the matchup.
```
>>> wm = li.weekly_matchups
>>> wmh = li.weekly_matchup_histories
```
Lastly, you can see the classes with a simple method to display the info above.
```
li.display_matchup_info()
```
Have fun and reach out if you have any cool statistical ideas!


  [spilchen]: <https://github.com/spilchen/yahoo_fantasy_api>
  [salt]: <https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Morton_Salt_Umbrella_Girl.svg/320px-Morton_Salt_Umbrella_Girl.svg.png>
  [Registering Your Application]: <https://developer.yahoo.com/fantasysports/guide/#registering-your-application>
  [apps page]: <https://developer.yahoo.com/apps/>