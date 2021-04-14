from itertools import product

columns = ['Year',
       'Agriculture, value added (% of GDP)',
       'CO2 emissions (metric tons per capita)',
       'Domestic credit provided by financial sector (% of GDP)',
       'Electric power consumption (kWh per capita)',
       'Energy use (kg of oil equivalent per capita)',
       'Exports of goods and services (% of GDP)',
       'Fertility rate, total (births per woman)', 
       'GDP growth (annual %)',
       'Imports of goods and services (% of GDP)',
       'Industry, value added (% of GDP)',
       'Inflation, GDP deflator (annual %)',
       'Life expectancy at birth, total (years)',
       'Population density (people per sq. km of land area)',
       'Services, etc., value added (% of GDP)', 'pop', 'continent',
       'gdpPercap']

abbrev = ['year',
       'agri',
       'co2',
       'domCred',
       'electric',
       'energy',
       'exp',
       'fertility',
       'gdp',
       'impo',
       'industry',
       'infl',
       'lifeExp',
       'popDense',
       'service', 
       'pop', 
       'continent',
       'gdpPercap']

classifiers = ['_gt', '_st']

url_params = [a + b for a, b in product(abbrev, classifiers)]

url_params.extend(abbrev)

translation = {a:b for a, b in zip(abbrev, columns)}