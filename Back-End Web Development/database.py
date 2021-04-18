# #TODO: adjust param names for query (columns), so that column names with spaces are goin to be wrapped in quotes

# --- import libraries 
import sqlite3
import datetime
import json

# create connection
connection = sqlite3.connect("./data.db", check_same_thread=False)  #NOTE re-cerate data.db, as the other one was created in dorectory above --> .. changed  to . now

# initiate cursor 
cursor = connection.cursor()

# queries
create_gapminder_table = r"""CREATE TABLE IF NOT EXISTS gapminder (
                        id INTEGER PRIMARY KEY,
                        'Country Name' TEXT NOT NULL, 
                        'Year' INTEGER NOT NULL,
                        'Agriculture, value added (% of GDP)' REAL,
                        'CO2 emissions (metric tons per capita)' REAL,
                        'Domestic credit provided by financial sector (% of GDP)' REAL,
                        'Electric power consumption (kWh per capita)' REAL,
                        'Energy use (kg of oil equivalent per capita)' REAL,
                        'Exports of goods and services (% of GDP)' REAL,
                        'Fertility rate, total (births per woman)' REAL, 
                        'GDP growth (annual %)' REAL,
                        'Imports of goods and services (% of GDP)' REAL,
                        'Industry, value added (% of GDP)' REAL,
                        'Inflation, GDP deflator (annual %)' REAL,
                        'Life expectancy at birth, total (years)' REAL,
                        'Population density (people per sq. km of land area)' REAL,
                        'Services, etc., value added (% of GDP)' REAL, 
                        'pop' REAL, 
                        'continent' TEXT,
                        'gdpPercap' REAL
                    );"""

# ----- Database Functions ------
#create table
def create_tables():
    with connection:
        cursor.execute(create_gapminder_table)
    print("Table created!")
    return 
    

def get_all():
    # define current query
    query_all = """SELECT * FROM gapminder;"""
    # query_upcoming = """SELECT * FROM movies WHERE release_date > ?;"""
    # save results in variable
    with connection:
        results = cursor.execute(query_all).fetchall()
        names = [description[0] for description in cursor.description]
        # return results
        if not results:
            print("No entries yet!")
            print(f"return value: {results}")
            return results
        else:
            print("Results returned!!!")
            result_dicts = query_result_to_json(results, names)
            return result_dicts


def get_selection_by_params(params):
    # create string to add to query from param-dict
    condition_str = create_query_string_from_params(params)

    # define current query
    query = f"""SELECT * FROM gapminder
               WHERE {condition_str};
            """

    print("Query: ", query)

    with connection:
        results = cursor.execute(query).fetchall()
        names = [description[0] for description in cursor.description]
        # return results
        if not results:
            print("No entries yet!")
            print(f"return value: {results}")
            return results
        else:
            print("Results returned!!!")
            #  convert results into list of dicts
            result_dicts = query_result_to_json(results, names)
            return result_dicts


def get_country_by_params(params):
    # create string to add to query from param-dict
    condition_str = create_query_string_from_params(params)

    # define current query
    if 'Year' in params.keys():
        year_given = True
        query = f"""SELECT DISTINCT "Country Name" FROM gapminder
                WHERE {condition_str};
                """
    else:
        year_given = False
        query = f"""SELECT "Country Name", "Year" FROM gapminder
                WHERE {condition_str};
                """

    print("Query: ", query)

    with connection:
        results = cursor.execute(query).fetchall()
        names = [description[0] for description in cursor.description]
        # return results
        if not results:
            print("No entries yet!")
            print(f"return value: {results}")
            return results
        else:
            print("Results returned!!!")
            result_dicts = query_result_to_json(results, names)
            result_dict_countries = {}
            country_list = []
            if year_given == True:
                for entry in result_dicts:
                    country_list.append(entry['Country Name'])
                result_dict_countries['countries'] = country_list
            elif year_given == False:
                years = sorted(list(set([d['Year'] for d in result_dicts])))
                for year in years:
                    result_dict_countries[str(year)] = []
                    for entry in result_dicts:
                        if entry['Year'] == year:
                            result_dict_countries[str(year)].append(entry['Country Name'])
            return result_dict_countries


# ---- Helper Functions ----
def query_result_to_json(results, names):
    #  convert results into list of dicts
    result_dicts = []
    for row in results:
        current_dict = {}
        for idx, val in zip(names, row):
            current_dict[idx] = val
        result_dicts.append(current_dict)

    return result_dicts


def create_query_string_from_params(params):
    condition_str = ""

    print("PARAMS PASSED TO DB: ", params)

    for counter, (key, value) in enumerate(params.items()):
        value = f"'{value}'" if type(value) == str else value  #add extra quotes to string-values in order to keep quotes in query

        if len(key.split("_")) > 1:
            key, classifier = key.split("_")
            key = f'"{key}"' if len(key.split(" ")) > 1 else key
            if classifier == "gt":
                classifier = ">"
            elif classifier == "st":
                classifier = "<"
            condition_str += f"{key} {classifier} {value} AND "

        else:
            key = f'"{key}"' if len(key.split(" ")) > 1 else key  #note: column names with spaces need to be wrapped in DOIBLE QUOTES, not single quotes for query!!
            condition_str += f"{key} = {value} AND "

    print("CONDITION STRING :",condition_str)

    condition_str = condition_str[:-5]

    return condition_str
        