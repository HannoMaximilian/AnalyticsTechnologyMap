import sqlite3
import pdb
import multiprocessing
import json
import time


# Create a table that contains all technolgies that we extracted from a post or comment.
# (Remember that the view all_content contains posts and comments)
# Posts or comments with less than two technologies named have no value to me

parallel_processes = 4

def extract_techs(query_batch, extraction_dict):
    return_list = []
    for _id, content in query_batch:
        techs = []
        content = content.lower()
        for tech in extraction_dict.keys():
            if tech in content:
                techs.append(extraction_dict[tech])
        if len(techs)>1:
            return_list.append((_id, techs))
    print(len(return_list))
    return return_list


def run():
    conn = sqlite3.connect('C:\\MeinCode\\reddit_scraper\\reddit.db')

    curs = conn.cursor()
    extraction_dict = {}

    with open("C:\\MeinCode\\reddit_scraper\\technologies.json") as json_file:
        technologies_json = json.load(json_file)
    tech_set = technologies_json.keys()

    # Initiate the extraction dict. I will extract the technologie names from 
    # a lowercase text, thats why I have to search with lowercase names as well
    extraction_dict = {tech.lower(): tech for tech in tech_set}

    # I will add my aliases to the extraction dict. I want some names to correspond
    # to the same technology, like Spark and Spark2
    for element in tech_set:
        for alias in technologies_json[element]['aliases']:
            extraction_dict[alias.lower()] = element
    m = multiprocessing.Manager()
    queue = m.Queue()
    curs.execute("SELECT * FROM all_content")
    print("Selected")
    fetch = True


    results = []
    def my_callback(result):
        results.append(result)


    with multiprocessing.Pool(parallel_processes) as pool:
        print(pool._outqueue)  # DEMO
        while fetch:
            query_batch = curs.fetchmany(10000)
            if not query_batch:
                fetch = False
                continue
            pool.apply_async(extract_techs, (query_batch, extraction_dict), callback=my_callback)
            fetch = query_batch # An empty list corresponds to Boolean: False
        time.sleep(5)
        #results = [res.get() for res in results]
    #print(results)

    with conn:
        curs.execute("""CREATE TABLE IF NOT EXISTS techs_extracted_v2 (
                        id TEXT PRIMARY KEY,
                        tech_list TEXT
                        )""")
 
        for solution in results:
            for res in solution:
                _id, _list = res
                _list = str(_list)
                curs.execute("""INSERT OR IGNORE INTO techs_extracted_v2 VALUES (:id, :tech_list)""",
                {'id': _id, 
                'tech_list': _list
                })
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run()