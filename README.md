# Analytics Technology Map

Using Python 3.8


This is the current version of the Analytics Technology Map:

[<img src="https://github.com/HannoMaximilian/AnalyticsTechnologyMap/blob/master/Visualizations/TechnologyMapV2.jpg">](https://github.com/HannoMaximilian/AnalyticsTechnologyMap/blob/master/Visualizations/techmap_V2_threshold015.html)
*Purple: Visualization and BI, Red: Data Processing, Blue: Database, Yellow: Cloud Service, Olive: Web App, Black: Technology Family, Grey: Othes*

For a zoomable Version of the map, please download and open [techmap_V2_threshold015.html](https://github.com/HannoMaximilian/AnalyticsTechnologyMap/blob/master/Visualizations/techmap_V2_threshold015.html "Technology Map Version 2")


------------------------------

This project tries to understand more about Analytics and Big Data technologies such as Spark, MongoDB or Tableau by analyzing how reddit users talk about them. The goal of the project is to give information about which technolgogies are similar to other technolgies, and which technolgies are often used together. Updates about what has already been implemented are given.

Currently the repository contains:

  - get_data.py:     A python script that uses the pushlift API to get comments and posts from reddit.com and adds them to a SQLite database
  - create_usefull_views.py:     A python script that uses SQLite queries to order the data in view that are usefull for analysis
  - technologies_V1.json:     A json file that contains technologies I find interesting for the analysis (first version)
  - technologies_V1.json:     A json file that contains technologies I find interesting for the analysis (second version)
  - extract_techs.py:     A python script that extracts the technologies given in "technologies.json" from the reddit posts and comments
  - Joint_Occurrence_Heatmap.ipynb:	A jupyter notebook that uses a heatmap to visualize how often two of the technologies that are listed in "technologies.json" appear together in the posts and comments safed in the SQL database 
  - Analytics_Technology_Map_V1:    The script that generates the first version of the technology map
  - Analytics_Technology_Map_V2:    The script that generates the second (most recent) version of the technology map

The following heeatmap shows, how often two technologies appeared together in a comment or post (obviously there are many cells with a much larger number than 20). Basis for this visualization are comments and posts that have a vote larger or equal to one and that were written in the last two years in the subreddits [MaschineLearning', 'webdev', 'bigdata', 'datascience', 'analytics' or  'ArtificialInteligence'. See jupyter notebook "Joint_Occurrence_Heatmap.ipynb".

![Technology Heatmap](https://github.com/HannoMaximilian/AnalyticsTechnologyMap/blob/master/Visualizations/heatmap.png)

