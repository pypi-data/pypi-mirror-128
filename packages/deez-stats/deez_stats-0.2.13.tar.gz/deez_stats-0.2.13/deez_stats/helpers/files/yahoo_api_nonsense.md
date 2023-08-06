# Yahoo API
<https://developer.yahoo.com/fantasysports/guide/>

### spilchen: yahoo fantasy api
<https://pypi.org/project/yahoo-fantasy-api/>

### Base URI
<https://fantasysports.yahooapis.com/fantasy/v2/>

### Game Resource
<https://fantasysports.yahooapis.com/fantasy/v2/game/nfl>

**GAME** Resource: game_id for nfl  

| Season | ```nfl``` game_id | Yahoo league_id |
| ------ | ----------------- | --------------- |
| 2001   | 49                | -               |
| 2002   | 57                | -               |
| 2003   | 79                | -               |
| 2004   | 101               | -               |
| 2005   | 124               | -               |
| 2006   | 153               | -               |
| 2007   | 175               | -               |
| 2008   | 199               | -               |
| 2009   | 222               | -               |
| 2010   | 242               | -               |
| 2011   | 257               | -               |
| 2012   | 273               | -               |
| 2013   | 314               | -               |
| 2014   | 331               | -               |
| 2015   | 348               | 898971          |
| 2016   | 359               | 247388          |
| 2017   | 371               | 470610          |
| 2018   | 380               | 81769           |
| 2019   | 390               | 72883           |
| 2020   | 399               | 228404          |
| 2021   | 406               | 53342           |

GAMES Resource: game_id for nfl  
<https://fantasysports.yahooapis.com/fantasy/v2/games;game_keys={game_key1}>

LEAGUE Resource:
https://fantasysports.yahooapis.com/fantasy/v2/league/223.l.431
https://fantasysports.yahooapis.com/fantasy/v2/league/223.l.431/settings
https://fantasysports.yahooapis.com/fantasy/v2/league/223.l.431/standings
https://fantasysports.yahooapis.com/fantasy/v2/league/223.l.431/scoreboard

TEAM Resource:
https://fantasysports.yahooapis.com/fantasy/v2/team/
https://fantasysports.yahooapis.com/fantasy/v2/team/223.l.431.t.1
https://fantasysports.yahooapis.com/fantasy/v2/team/223.l.431.t.1/matchups;weeks=1,5
https://fantasysports.yahooapis.com/fantasy/v2/team/223.l.431.t.1/stats;type=season
https://fantasysports.yahooapis.com/fantasy/v2/team/253.l.102614.t.10/stats;type=date;date=2011-07-06


ROSTER Resource:
https://fantasysports.yahooapis.com/fantasy/v2/team//roster
https://fantasysports.yahooapis.com/fantasy/v2/team//roster;week=10
https://fantasysports.yahooapis.com/fantasy/v2/team/253.l.102614.t.10/roster/players

https://fantasysports.yahooapis.com/fantasy/v2/league/223.l.431/players;player_keys=223.p.5479
https://fantasysports.yahooapis.com/fantasy/v2/league/223.l.431/players;player_keys=223.p.5479/stats

https://fantasysports.yahooapis.com/fantasy/v2/transaction/
https://fantasysports.yahooapis.com/fantasy/v2/transaction/257.l.193.tr.2 - Completed add/drop transaction
https://fantasysports.yahooapis.com/fantasy/v2/transaction/257.l.193.w.c.2_6390 - Waiver claim transaction
https://fantasysports.yahooapis.com/fantasy/v2/transaction/257.l.193.pt.1 - Pending trade transaction

type	add,drop,commish,trade	/transactions;type=add
types	Any valid types	/transactions;types=add,trade
team_key	A team_key within the league	/transactions;team_key=257.l.193.t.1
type with team_key	waiver,pending_trade	You can only use these options when also providing the team_key, ie /transactions;team_key=257.l.193.t.1;type=waiver
count	Any integer greater than 0	/transactions;count=5



```https://fantasysports.yahooapis.com/fantasy/v2/league/{}/scoreboard;week={}'.format(league_id, week))```
* raw_matchups_query.json
