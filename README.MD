# Twitter API Apps
**by**: Nate Muth ([@analyticsNate](https://twitter.com/analyticsnate))<br>
<br>
#### 01_Tableau_vs_PowerBI
This app pulls tweets with #Tableau and #PowerBI since a certain date. Then, using matplotlib, the tweets are counted by day and displayed on a dual bar chart. The bar chart is then saved as a tab_vs_pbi.png file in the local directory.<br>
![alt text](https://github.com/analyticsnate/twitter-api/blob/master/tab_vs_pbi.PNG)
<br>
- Add date as parameter <br>
<br>

#### 02_Most_Tweets_On_Subject
This app pulls tweets with about a given subject in the last *n* hours. The tweets are the grouped by the twitter username, sorted, and displayed in simple horizontal bar chart. The bar chart is also saved as a .png in the local directory. <br>
Run via command line: <br>
`> python 02_Most_Tweets_On_Subject.py "NationalFrenchToastDay" 2 "black"` <br>
![alt text](https://github.com/analyticsnate/twitter-api/blob/master/most_tweets_NationalFrenchToastDay.png)
