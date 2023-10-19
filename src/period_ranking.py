"""
Author: Jamie Antal
Date: 12/4/2022
Notes:

"""


import index_tools as it


def sortSecond(val):
    """
    used as key for sort() function
    :param val: must be a list
    :return: second element of the list
    """
    return val[1]


def quarter_data(data, year, qtr):
    """
    receives and converts a dict with assigned states to lists of quarterHPIs to same kind of dict, but limited to
    given year and quarter if it exists
    :param data: a dictionary mapping a state region to a list of QuarterHPI instances
    :param year: a year of interest (must be int)
    :param qtr: a quarter of interest (must be int)
    :return: a list of (region, HPI) tuples sorted from high value HPI to low value HPI
    """
    refined_list = []
    key_list = list(data.keys())
    for key in key_list:
        for element in data[key]:
            if element.year == str(year) and element.qtr == str(qtr):
                refined_list.append((key, float(element.index)))
    refined_list.sort(key=sortSecond, reverse=True)
    return refined_list


def annual_data(data, year):
    """
    receives and converts a dict with assigned states to lists of annualHPIs to same kind of dict, but limited to given
    year if it exists
    :param data: a dictionary mapping a state or zip code to a list of AnnualHPI objects
    :param year: a year of interest (must be int)
    :return: a list of (region, HPI) tuples sorted from high value HPI to low value HPI
    """
    refined_list = []
    key_list = list(data.keys())
    for key in key_list:
        for element in data[key]:
            if element.year == str(year):
                refined_list.append((key, float(element.index)))
    refined_list.sort(key=sortSecond, reverse=True)
    return refined_list


def main():
    """
    will prompt user for filepath and year, and it will check for which kind is filepath (ZIP5 or not), and continues
    to process the data into refined data and prints the top 10 and bottom 10
    :return:
    """
    file_input = input("Enter region-based house price index filename: ")
    year_input = int(input("Enter year of interest for house prices: "))
    if "ZIP" in file_input:
        raw_data = it.read_zip_house_price_data("data/" + file_input)
        refined_data = annual_data(raw_data, year_input)
        it.print_ranking(refined_data, "{} Annual Ranking".format(year_input))
    else:
        raw_data = it.read_state_house_price_data("data/" + file_input)
        smelt_data = it.annualize(raw_data)
        refined_data = annual_data(smelt_data, year_input)
        it.print_ranking(refined_data, "{} Annual Ranking".format(year_input))


if __name__ == "__main__":
    main()
