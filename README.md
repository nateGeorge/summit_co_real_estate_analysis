# summit_co_real_estate_analysis
After buying and living in a condo in the mountains for a few years, I decided it was time to sell.  I was able to qualify as living in the condo full-time due to working remotely in the summers and sometimes on long weekends during the winter, which gave me greater than 50% of my living time at the condo.  From watching the market for a few years, I had noticed prices seemed to dip at the end of the summer, and be higher in the winter ski season.  I wondered if there were any significant differences between selling in January or waiting a month of two, and analyzed past sales data to answer this question.

## Data Source
Fortunately, Summit County makes [recent sales data public](http://www.co.summit.co.us/389/Sales-Reports).  I just manually downloaded all the excel files since there aren't that many.

## Results
First, one reason I believed prices might be higher in the winter is due to low supply.  I had seen this in realtors' newsletters, and here is the raw data:

![condo sales counts per month](images/summit_co_condo_number_of_sales.png)

As we can see, the number of sales is much lower in the winter months than summer.  Obviously, lower supply is good for the seller.

Looking at the price data, we can see there is no clear monthly trend in price.  There is a strong uptrend in price, which is to be expected in a "strong" economy where the value of the dollar is being depreciated significantly via QE and lower interest rates (and stocks are going up).

![condo prices per SF](images/summit_co_condo_price_per_sf.png)

The trend seems to be flattening out during 2019, but also flattened out in 2016 when the stock market had a weak spell.  In 2018, it looks like there was a dip in prices, which was the year I started paying close attention to prices.  This explains my belief (which I have since revised) that prices are usually lower at the end of the summer.

Looking specifically at the condo complex where I own(ed) a unit, we can see the average price per square foot is almost the same as the Summit County trend:

![treehouse prices per sf](images/treehouse_price_per_sf.png)

Even more specifically, we can see the top-floor 1000-square-foot units (like mine) follow the trend as well.

![treehouse 3nd floor prices per sf](images/3rd_floor_unit_sales_per_sf.png)

Since there are so few sales of these units, this data is difficult to use to summarize trends.  The sales prices of these units depends on how well the unit is marketed and negotiated, as well as the seller's specific situation.  The condition of the units also varies widely, and can effect price significantly. For example, the $425K sale in 2019 was an extensively-remodeled unit, which was probably also expertly marketed and negotiated.  The other lower sales were not as nice of units and the sellers may have needed money quikly.

![treehouse 3nd floor prices per sf](images/3rd_floor_unit_sales.png)

# Conclusion
In conclusion, it appears there is no specific advantage to selling at any particular time of year for top-floor 1000-sq-ft Treehouse condo units.  However, condo supply in Summit County is lowest around December through March, which coincides with the peak ski season.  This is not suprising, as no one wants to sell a ski condo during the season.  However, basic supply and demand economics principles dictates the best time to sell is in the peak ski season and the best time to buy is during the late part of summer or early fall.  Prices do not seem to reflect this exectation, but perhaps other metrics such as days on market and number of offers do.

Further research into this topic could include modeling the data with fbprohpet to extract trends (e.g. long-term trends and monthly trends), as well as looking at other data not available from the public dataset such as days on market and the pictures and text from the MLS listing.