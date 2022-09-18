# Generic Real Estate Consulting Project
Groups should generate their own suitable `README.md`.

# Instructions to Reproduce

## [House SpeakingSame](http://house.speakingsame.com/)

1. `/scripts/scrape_house_speakingsame_suburbs.py` outputs to `/data/raw/top_rent_suburbs_<dt>.csv`
2. `/scripts/scrape_house_speakingsame_rent.py` outputs multiple suburbs to `/data/raw/housespeakingsame/rent/<suburb>_<dt>.csv`
3. `/scripts/scrape_house_speakingsame_buy.py` outputs multiple suburbs to `/data/raw/housespeakingsame/buy/<suburb>_<dt>.csv`
4. `/scripts/preprocess_house_speakingsame.py` outputs to `/data/curated/housespeakingsame/<dt>.csv`

