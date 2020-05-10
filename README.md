# AnalyticsTechnologyMap

This project tries to understand more about Analytics and Big Data technologies such as Spark, MongoDB or Tableau by analyzing how reddit users talk about them. The goal of the project is to give information about which technolgogies are similar to other technolgies, and which technolgies are often used together. Updates about what has already been implemented are given.

Currently the repository contains:

  - get_data.py:     A python script that uses the pushlift API to get comments and posts from reddit.com and adds them to a SQLite database
  - create_usefull_views.py:     A python script that uses SQLite queries to order the data in view that are usefull for analysis
  - technologies.json:     A json file that contains technologies I find interesting for the analysis (first draft)
  - extract_techs.py:     A python script that extracts the technologies given in "technologies.json" from the reddit posts and comments
