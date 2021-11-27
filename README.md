# Trading Post Watcher

TPW is a web application written in Python (using the [Flask](https://flask.palletsprojects.com/en/2.0.x/) framework) which helps keep track of things the average [Guild Wars 2](https://www.guildwars2.com) player cares about.

### Features

* Users can view (and filter through) the following:
  * Trading post transaction history
  * Current buy and sell orders
  * Bank inventory (with an indicator for items bound to a specific character)
  * Unlocked dyes
  * Account wallet (including PVP, WvW, and map-specific currencies)

* Current orders now alert the user if undercut or outbid
  * Users can click on the item name to copy it to their clipboard for quick searching in-game
* Item, currency, and dye data is now stored in a database, rather than pulled every time an API call is made
* TPW now stores your public API key as a salted & hashed string in the database (previously it was stored as a 30-day signed cookie) 

### To Do

* Finish porting the mount progress tracker from GW2API project
* Finish porting crafting recipe page from GW2API project

* Add logic to suggest "safe" high volume/margin items to flip
* View specific characters' stored talent builds?
