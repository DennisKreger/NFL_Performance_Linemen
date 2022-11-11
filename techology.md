# Technologies Used
## Data Cleaning and Analysis
Pandas will be used to clean the data and perform an exploratory analysis. We also plan on using both python and R to analyze the data. 

## Database Storage
Google cloud services is the database we intend to use, and we will integrate Spark and Java to display the data as DataFrames in PostreSQL.

## Machine Learning
SciKitLearn is the ML library we'll be using to create a classifier. Our training and testing setup is to identify when players are "in trouble" and then analyze some of the reasons why (why did a sack occur, what was the defensive matchup like, etc.) and we are also starting a model that looks into the acceleration of players after they emerge from "clinching" with another player. This should help determine performance metrics and can point out who is most explosive and might need the most time off in between games. Plots from both of these models have been promising so far with high accuracy, we just need to sort through more data and make some of the necessary connections that the data is showing in these models. 

## Dashboard
In addition to using a Spark template, we will also integrate D3.js for a fully functioning and interactive dashboard. It will be hosted on a HTML web page using bootstrap templates. We also plan on performing some visualizations on Tableu, which will be linked within the dashboard.
