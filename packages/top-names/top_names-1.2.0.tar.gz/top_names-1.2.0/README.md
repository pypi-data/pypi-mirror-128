# top-names

Program to scrape from the most common first names (male and female) in the United States from the decades 1880s-2010s. Please note that these names are not guaranteed to be unique.
Data provided by the Social Security Admnistration.
If you do not want to run the program, you can view the results as of November 25th, 2021 in [output.txt](output.txt).

## Getting Started

### Installing

Simply run `python3 setup.py install` to install the package.

### Usage

After installing, you should use the `top_names.name_list.NameList` class. This is a wrapper class of a list that is generated dynamically by the `top_names.name_scraper.NameScraper` class. Initially, the list is empty, but when trying to retrieve data from the list, it will be populated.

### Running

You can run the module itself using `python3 -m top_names`. By default, this will output to `stdout`. You can specify a file to write to using the `-o` option. You may also see debug information with the `--debug` flag.

## Requirements

Project built with Python 3.8.10.
For modules, please read [requirements.txt](requirements.txt).

## Data Source

Data scraped from the [United States Social Security Administration](https://www.ssa.gov/) through their [Popular Baby Names by Decade](https://www.ssa.gov/oact/babynames/decades/) form.

## Authors

- Will Ciesialka

## License

This project is licensed under the MIT License. For more details, please see [LICENSE](LICENSE).