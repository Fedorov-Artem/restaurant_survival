# restaurant_survival
### Project scope
This project's goal is to check which restaurants stay in business and which close. To answer this question, I used two datasets: one from 2021 scraped by STEFANO LEONE and published on [Kaggle](https://www.kaggle.com/datasets/stefanoleone992/tripadvisor-european-restaurants), and another scraped by me in 2023 as a part of the project; it is available in the current repository and also on [Kaggle](https://www.kaggle.com/datasets/artemfedorov/restraunt-survival). I decided to limit the project to four European countries present in the original dataset: Northern Ireland (part of UK), Slovakia, Bulgaria and Finland. The code used to scrape the TripAdvisor website and then clean the data is in the scraping_cleaning directory of this repository. The analysis was made in two Jupyter notebooks on Kaggle. [The first notebook](https://www.kaggle.com/code/artemfedorov/resrt-survival-join) joins the datasets and calculates a number of distance features that take time to calculate, [the second one](https://www.kaggle.com/code/artemfedorov/restaurant-survival-eda) contains the analysis itself. Both notebooks are also available in this repository.

As part of the analysis, an ML model that predicts which restaurants are going to close has been trained, and then features that increase the model's performance were selected. The most important features were visualized, including several maps.

### Data scraping and cleaning
The TripAdvisor website was scraped with the Selenium package, the code is in the restaurant_by_id.py file. The script uses an input list of known restaurant IDs from the 2021 dataset and saves the raw data in a *.csv file. That raw data is later cleaned with the code in the data_cleaning.py file. To distinguish better between restaurants that have actually closed but were not reported as closed on TripAdvisor and the restaurants that stay in business, an additional check was performed: restaurant site URLs obtained during scraping were checked to determine whether the site is online or not. A significant number of restaurants list their Facebook page as their website, and to better understand which restaurants continue working, some additional information, including the date of the last post and description, was also collected from Facebook. The scraping script is available in check_websites.py, and the final data cleaning code is in data_clean_final.py.

There are several more scraping and cleaning files in the directory. Those files were used to make a list of all restaurants from the selected countries that are available on TripAdvisor now. I decided to leave that data out of the scope of the project but to keep those files in the repository, as this code is functional.

I wanted to make the process of producing a joined dataset to be publicly visible on Kaggle, so I decided to produce that dataset using Jupyter notebook, but not pure python. In the same notebook, several distance count features were calculated (like total number of restaurants that match some criteria within a certain distance from the restaurant).

### Subset of restaurants with known status
Unfotunately, it turned out that while TripAdvisor makes many checks before marking a restaurnat as closed, not all the restaurants that have actually closed are reported on Tripadvisor. That was a huge problem for the project, so I had to create a subset of restaurants that I could be sure are open. This subset includes only restaurants that recieved significant number of reviews on TripAdvisor, about 25% of all restaurants are included in the dataset. The process of creating the dataset is described in detail in the EDA notebook. 

### Analysis itself
After the subset of restaurants with known status is finalized, a number of features that are expected to correlate with the target feature are visualized. Then about 80 features are generated, and an ML model is fitted using all the features available. Then features of very low importance are removed. The volume of data is relatively small, so it is possible to check the model's performance without each single feature and then to remove features that decrease the model's performance the most until only important and useful features remain. In this project, a few features that increased the model's performance insignificantly were also removed. 

### Conclusions
It turned out that it is impossible to make a good prediction about restaurants that are going to close; probably, the information that matters is not in the dataset. But it is possible to differentiate between restaurants that are more likely and less likely to close.

The important features that increase the model's performance are the following:
* The feature that turned out to be the most important was the **total number of reviews**. Even when the comparison is limited only to restaurants with at least 30 reviews, additional reviews significantly improve a restaurant's survival chances.
* **Number of restaurants with at least 10 reviews and located within 1 km**. The survival chances are higher for restaurants that are located in areas with fewer restaurants nearby. Most restaurants that get many reviews are located in the city centers, this means it is harder for a restaurant outside a city center to get the same number of reviews, so among selected restaurants with 30+ reviews, restaurants located outside a city center survive more often. Notably, the algorithm shows better results when only restaurants with 10 or more reviews are counted. This is one more indicator that data about restaurants that get few reviews is not reliable.
* **Number of restaurants with at least 10 reviews and located within 200 m**. This feature is less important than the previous one, and they correlate. But the model gives better results with both features present in the inputs.
* **Share of new restaurants within 1 km** - restaurants located in areas with a high share of newly opened restaurants survive more often.
* **TripAdvisor's average rating**: this feature is important, and it improves the model's performance significantly, but restaurants with the highest possible rating of 5.0 have a relatively low survival rate. One possible explanation is that a very high rating can be a sign that a restaurant's rating is being manipulated. Restaurants with medium ratings of 3.5 to 4.5 show the highest survival rate.
* **Open days per week** - no surprise here, restaurants open all 7 days a week have the highest survival rate, while restaurants open just a few days per week tend to close more often.
* A boolean feature with a "True" value for **fast food** restaurants. These restaurants survive more often, probably because it is difficult for fast food restaurants to get a significant number of reviews, and those that cross the threshold of 30 reviews are all in some way successful.

### Final thoughts

