"""
Author: Jamie Antal
Date: 12/4/2022
Notes:

"""


import index_tools as it
from period_ranking import sortSecond


def cagr(idxlist, periods):
    """
    calculates the change in index between two periods, will product a percentage representing the change
    :param idxlist: a 2-item list/tuple of [HPI0, HPI1], where HPI0 is the index value of the earlier period and HPI1
    is the index value of the ending period
    :param periods: a number (N) of periods (years) between the two HPI values in the list
    :return:  float representing the CAGR (compound annual growth rate) of the index values in the list for the
    specified period
    """
    start_index = idxlist[0]
    end_index = idxlist[1]
    result = ((end_index / start_index) ** (1 / periods) - 1) * 100
    return result


def calculate_trends(data, year0, year1):
    """
    receives and converts a data into refined list of lists with state names and percentage representing the change in
    indexs between two periods
    :param data: a dictionary from region to a list of AnnualHPI
    :param year0: starting year (must be int and less than year1)
    :param year1: ending year (must be int and greater than year0)
    :return: a list of (region, rate) tuples sorted in descending order by the compound annual growth rate
    """
    if year0 > year1:
        "Error. year0 must be less than year1."
        quit()
    refined_list = []
    key_list = list(data.keys())
    for key in key_list:
        got_year0 = False
        got_year1 = False
        for element in data[key]:
            if int(element.year) == year0:
                year0_index = float(element.index)
                got_year0 = True
            if int(element.year) == year1:
                year1_index = float(element.index)
                got_year1 = True
            if got_year0 == got_year1 == True:
                result = cagr((year0_index, year1_index), int(year1) - int(year0))
                refined_list.append((key, result))
                break
    refined_list.sort(key=sortSecond, reverse=True)
    return refined_list


def main():
    """
    prompts the user for filepath, starting year, and ending year. then it will check the filepath to check which it
    will use either one of both read functions. from there, it will print out the top 10 and bottom 10 of product of
    calculate_trends() function used on the refined data in formal way
    :return:
    """
    file_input = input("Enter house price index filename: ")
    year0_input = int(input("Enter start year of interest: "))
    year1_input = int(input("Enter ending year of interest: "))
    if "ZIP" in file_input:
        raw_data = it.read_zip_house_price_data("data/" + file_input)
        refined_data = calculate_trends(smelt_data, year0_input, year1_input)
        it.print_ranking(refined_data, "{}-{} Compound Annual Growth Rate".format(year0_input, year1_input))
    else:
        raw_data = it.read_state_house_price_data("data/" + file_input)
        smelt_data = it.annualize(raw_data)
        refined_data = calculate_trends(smelt_data, year0_input, year1_input)
        it.print_ranking(refined_data, "{}-{} Compound Annual Growth Rate".format(year0_input, year1_input))


if __name__ == "__main__":
    main()
