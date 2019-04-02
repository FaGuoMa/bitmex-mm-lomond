# bitmex-mm-lomond
This is a toy, but we figured code could be usefull. Essentially, [Btimex MM code](https://github.com/BitMEX/sample-market-maker) relies on the `weboscket` library, which is all but intuitive. Instead, we leverage on `Lomond` which makes for much easier to read code.
**We have made an honest effort to clean the code, but this is not production code, nor a current priority. I will try to accomodate issues and PR, but be patient (and compassionate)**

This semi-functional (as in "it will trade, but should really NOT be used as is") market maker is the product of a sprint. We eventually ported some of our finding in production but this is not used, and can illustrate a few (we believe) interesting ideas. For example:
- [Dataplicity Lomond](https://github.com/wildfoundry/dataplicity-lomond) is a very nice alternative to `webosckets`, especially for iterative development. The API exposes the websocket stream as a generator, which in turns allow for appropriate event-based rules to be put in place. It also has a `persist` method to deal with reconnections, hassle-free
- 

# Installation & Notes

Do create a virtual environment (`python=3.6`), and install:
- lomond: `pip install lomond`
- bitmex' provided API wrapper: `pip install bitmex`

Then, simply run with `python mm.py`
