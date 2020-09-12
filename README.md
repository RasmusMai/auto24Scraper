# auto24Scraper

An another learning expirement with web scraping and proper classes. 



## How to use

Main logic and current entry point is in `main.py`. To run, simply run it in a console session and watch errors fly everywhere as there isn't much exception or edge case handling yet. But for the cars it does work currently, I think it's quite nice.


```python
from main import Auto24

auto24 = Auto24()
auto24.scrape(1) # search pages to scrape starting from 0
```

The above code will output a results.json file which contains the details for each car in the search pages scraped.
Auction cars are currently ignored.




## Planned

- Auction cars
- Listing submission date
  - There isn't one in the car listing page in Auto24
  - But it might be possible to get the earliest *known* date of the submission from Web Archives
- Search page should be it's very own class
- Further exception handling

## License
[MIT](https://choosealicense.com/licenses/mit/)
