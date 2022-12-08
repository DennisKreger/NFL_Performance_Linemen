# Technologies Used
## Data Cleaning and Analysis
Pandas was used to clean the data and perform an exploratory analysis. We also used PostgreSQL for joining our data and python for our analyses and statistics. 

## Database Storage
Google cloud services is the database we are using to load in our data. Flask, CSS, HTML, and JS were used to load and display our data from the cloud database.

## Machine Learning
SciKitLearn is the ML library we used to create a classifier. Our training and testing setup is to identify historical data on teams wins and losses since 2011, specifically comparing offensive and defensive stats. A logistic regression model was used to predict the outcome of games in the 2021 season, and this model has an accuracy of 61.2%. A confidence value was also calculated for each prediction to showcase the strength of the prediction based on the data that we found for each team. 

## Dashboard
We use a Flask application to display our dashboard via an HTML webpage.  Bootstrap/CSS was used for styling the dashboard.  Google App engine was utilized to host the app through a cloud service, and SQL alchemy was also used to help facilitate the dashboard commuication between python files and the database. Both Plotly and Matplotlib were utilized to create the visualizations that are embedded in our dashboard's static HTML files.


### Additional technological architecture that we utilized for this project can be seen in this summary image below:


![architecture](/api/static/images/architecture.png)
