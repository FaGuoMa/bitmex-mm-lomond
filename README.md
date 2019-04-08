# bitmex-mm-lomond
This is a toy, but we figured code could be usefull. Essentially, [Btimex MM code](https://github.com/BitMEX/sample-market-maker) relies on the `weboscket` library, which is all but intuitive. Instead, we leverage on `Lomond` which makes for much easier to read code.  
**We have made an honest effort to clean the code, but this is not production code, nor a current priority. I will try to accomodate issues and PR, but be patient (and compassionate)**

This semi-functional (as in "it will trade, but should really NOT be used as is") market maker is the product of a sprint. We eventually ported some of our finding in production but this is not used, yet can illustrate a few (we believe) interesting ideas. For example:
- [Dataplicity Lomond](https://github.com/wildfoundry/dataplicity-lomond) is a very nice alternative to `websockets`, especially for iterative development. The API exposes the websocket stream as a generator, which in turns allow for appropriate event-based rules to be put in place. It also has a `persist` method to deal with reconnections, hassle-free
- spawning an `asyncio` event_loop, then using it in a daemonized thread. We send executions into the asyncio loop because events flow through the websocket. This ia an excelent idea described in this [medium article](https://hackernoon.com/threaded-asynchronous-magic-and-how-to-wield-it-bba9ed602c32) by [Cristian Medina](https://hackernoon.com/@tryexceptpass)
- onboarding the logic of trading in a separate module `agent.agent` class ` MM`. This would allow to replace a market making logic by a smart execution of external indicators, for example
- studies in classes for an orderbook, or for a "keep" of one's orders on market
- an original, but ultimately flawed, approach to the infamous issues with prices showing floating point approx (API's don't like to get a million decimals, which tends to happen A LOT for satoshi-level securities. Btw, I personally think the `decimal` package  kinda sucks when it comes to float compatibility, or general API

# Installation & Notes

Do create a virtual environment (`python=3.6`), and install:
- lomond: `pip install lomond`
- bitmex' provided API wrapper: `pip install bitmex`
- bravado: `pip install --upgrade bravado`
- edit the files `config.py` and `config_prod.py` 
- change the current security in the main of `trader/trader.py`. Do adjust tick size accordingly in the agent parameters if you do (and yes, it's quirky)

Then, simply run with `python trader/trader.py`

## Notes
- Bitmex does NOT like machine-gun orders. Allow a relatively high size for each order, or get marked as spam (do not use on your main account with real money)  
- the `agent` part is dodgy. A key issue we had was how to queue estimate (this is pretty critical unless you want to be holding the pags when price move), and especially at the best bid/ask. The agents tries to keep try of bid/asks that are "burnt", that is: for which we were on the ladder, but nobody came after so after a grace period, we canceled the order. At the end of the sprint, we ported parts of this experiment rather than use it as-is
- We did run it for a while on

