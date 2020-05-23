# Analytics Technology Map

Using Python 3.8

This project tries to understand more about Analytics and Big Data technologies such as Spark, MongoDB or Tableau by analyzing how reddit users talk about them. The goal of the project is to give information about which technolgogies are similar to other technolgies, and which technolgies are often used together. Updates about what has already been implemented are given.

Currently the repository contains:

  - get_data.py:     A python script that uses the pushlift API to get comments and posts from reddit.com and adds them to a SQLite database
  - create_usefull_views.py:     A python script that uses SQLite queries to order the data in view that are usefull for analysis
  - technologies.json:     A json file that contains technologies I find interesting for the analysis (first draft)
  - extract_techs.py:     A python script that extracts the technologies given in "technologies.json" from the reddit posts and comments
  - Joint_Occurrence_Heatmap.ipynb:	A jupyter notebook that uses a heatmap to visualize how often two of the technologies that are listed in "technologies.json" appear together in the posts and comments safed in the SQL database 

The following heeatmap shows, how often two technologies appeared together in a comment or post (obviously there are many cells with a much larger number than 20). Basis for this visualization are comments and posts that have a vote larger or equal to one and that were written in the last two years in the subreddits [MaschineLearning', 'webdev', 'bigdata', 'datascience', 'analytics' or  'ArtificialInteligence'. See jupyter notebook "Joint_Occurrence_Heatmap.ipynb".

![Technology Heatmap](https://github.com/HannoMaximilian/AnalyticsTechnologyMap/blob/master/Visualizations/heatmap.png)

This is the current version of the Analytics Technology Map:

[<img src="https://github.com/HannoMaximilian/AnalyticsTechnologyMap/blob/master/Visualizations/TechnologyMapV2.jpg">](https://github.com/HannoMaximilian/AnalyticsTechnologyMap/blob/master/Visualizations/techmap_V2_threshold015.html)

