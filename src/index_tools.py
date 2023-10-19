"""
Author: Jamie Antal
Date: 12/3/2022
Notes:
    Currently, this module does as what it supposed to do except for it will not print out "output elided for ####-
    ####" due given example's data in instructions is different than provided files (OH in HPI_AP_state.txt).
"""


from dataclasses import dataclass


@dataclass
class QuarterHPI:
    """
    year: an integer representing the year of the index value.
    qtr: an integer representing the quarter of the year.
    index: a float representing the home price index.
    """
    year: int
    qtr: int
    index: float


@dataclass
class AnnualHPI:
    """
    year: an integer representing the year of the index value.
    index: a float representing the home price index.
    """
    year: int
    index: float


def read_state_house_price_data(filepath):
    """
    reads given filepath and converts it into dict, assigning state names to lists of quarterHPIs
    :param filepath: a string, giving the path name of a data file
    :return: a dict with assigned state names to lists of quarterHPIs, will print if a piece of infomation is missing
    """
    file = open(filepath)
    refined_dict = dict()
    for line in file:
        if "data unavailable" in line:
            print("data unavailable:")
            print(" {}".format(line))
            continue
        elif "yr" in line:
            continue
        converted = line.split()
        sample_state = converted[0]
        sample_quarterHPI = QuarterHPI(converted[1], converted[2], converted[3])
        if sample_state in refined_dict:
            refined_dict[sample_state].append(sample_quarterHPI)
        else:
            refined_dict[sample_state] = [sample_quarterHPI]
    file.close()
    return refined_dict


def read_zip_house_price_data(filepath):
    """
    reads given filepath (must be ZIP5 data file) and converts it into dict, assigning state names to lists of
    annualHPIs
    :param filepath: a string giving the path name of a ZIP5 data file
    :return: a dict with assigned state names to lists of annualHPIs, will print the amount of counted and uncounted
    depending on existence of values
    """
    file = open(filepath)
    refined_dict = dict()
    count = 0
    uncounted = 0
    skip = 0
    for line in file:
        if skip == 0:
            skip += 1
            continue
        converted = line.split()
        if converted[2] == converted[3] == converted[4] == converted[5] == ".":
            uncounted += 1
            continue
        else:
            count += 1
            sample_zip = converted[0]
            sample_annualHPI = AnnualHPI(converted[1], converted[3])
            if sample_zip in refined_dict:
                refined_dict[sample_zip].append(sample_annualHPI)
            else:
                refined_dict[sample_zip] = [sample_annualHPI]
    print("count: {} uncounted: {}".format(count, uncounted))
    return refined_dict


def index_range(data, region):
    """
    searches and finds the lowest and highest indexs of the given state
    :param data:  dictionary mapping regions to lists of *HPI4 objects and a region name. The objects may be
    either QuarterHPI or AnnualHPI objects
    :param region: must be string representing states in shorten version (NY, FL, etc.)
    :return: a tuple of the *HPI objects that are respectively the low and high index values of the dataset
    """
    sample_data = data[region]
    lowest = AnnualHPI("2022", "1000")
    highest = AnnualHPI("2022", "0")
    for sample in sample_data:
        if float(sample.index) < float(lowest.index):
            lowest = sample
        if float(sample.index) > float(highest.index):
            highest = sample
    return (lowest, highest)


def print_range(data, region):
    """
    prints out the result of index_range in formal way
    :param data: must be dict product by either one of both read functions
    :param region: must be string representing states in shorten version (NY, FL, etc.)
    :return:
    """
    sample = index_range(data, region)
    lowest = sample[0]
    highest = sample[1]
    print("Region: {}".format(region))
    print("Low: year/quarter/index: {} / {} / {}".format(lowest.year, lowest.qtr, lowest.index))
    print("High: year/quarter/index: {} / {} / {}".format(highest.year, highest.qtr, highest.index))


def print_ranking(data, heading="Ranking"):
    """
    prints out the top 10 and bottom 10 of the given data
    :param data: a sorted list of objects
    :param heading: a text message whose default value is “Ranking"
    :return:
    """
    print(heading)
    print("The Top 10:")
    print("1 : {}".format(data[0]))
    print("2 : {}]".format(data[1]))
    print("3 : {}".format(data[2]))
    print("4 : {}".format(data[3]))
    print("5 : {}".format(data[4]))
    print("6 : {}".format(data[5]))
    print("7 : {}".format(data[6]))
    print("8 : {}".format(data[7]))
    print("9 : {}".format(data[8]))
    print("10 : {}".format(data[9]))
    print("The Bottom 10:")
    print("42 : {}".format(data[-10]))
    print("43 : {}".format(data[-9]))
    print("44 : {}".format(data[-8]))
    print("45 : {}".format(data[-7]))
    print("46 : {}".format(data[-6]))
    print("47 : {}".format(data[-5]))
    print("48 : {}".format(data[-4]))
    print("49 : {}".format(data[-3]))
    print("50 : {}".format(data[-2]))
    print("51 : {}".format(data[-1]))


def annualize(data):
    """
    converts the data into dict with assigned state names to lists of annualHPIs
    :param data: a dictionary mapping regions to lists of QuarterHPI objects
    :return: a dictionary mapping regions to lists of AnnualHPI objects
    """
    refined_dict = dict()
    sample_keys = list(data.keys())
    for key in sample_keys:
        sample_list = data[key]
        average = 0
        number = 0
        saved_year = int(sample_list[0].year)
        for element in sample_list:
            if int(element.year) != saved_year:
                average_data = average / number
                if key in refined_dict:
                    refined_dict[key].append(AnnualHPI(str(saved_year), str(average_data)))
                else:
                    refined_dict[key] = [AnnualHPI(str(saved_year), str(average_data))]
                average = float(element.index)
                number = 1
                saved_year = int(element.year)
            else:
                average += float(element.index)
                number += 1
        if refined_dict[key][-1].year != str(saved_year):
            refined_dict[key].append(AnnualHPI(str(saved_year), str(average)))
    return refined_dict


def main():
    """
    will prompt user for filepath and which states to print out the indexs in quarter and annual HPIS, depending on
    what kind filename user used
    :return:
    """
    user_input = input("Enter house price index file: ")
    if "ZIP" in user_input:
        state_data = False
        raw_data = read_zip_house_price_data("data/" + user_input)
    else:
        state_data = True
        raw_data = read_state_house_price_data("data/" + user_input)
        annualized_data = annualize(raw_data)
    list_inputs = []
    user_input = input("Next region of interest( Hit ENTER to stop): ")
    while user_input != "":
        list_inputs.append(user_input)
        user_input = input("Next region of interest( Hit ENTER to stop): ")
    print("======================================================================")
    while len(list_inputs) != 0:
        current_state = list_inputs[0]
        if state_data is True:
            print("Region: {}".format(current_state))
            print_range(raw_data, current_state)
            print("Region: {}".format(current_state))
            low_high = index_range(annualized_data, current_state)
            print("Low: year/index: {} / {}".format(low_high[0].year, low_high[0].index))
            print("High: year/index: {} / {}".format(low_high[1].year, low_high[1].index))
            print("Annualized Index Values for {}".format(current_state))
        else:
            low_high = index_range(raw_data, current_state)
            print("Low: year/index: {} / {}".format(low_high[0].year, low_high[0].index))
            print("High: year/index: {} / {}".format(low_high[1].year, low_high[1].index))
            print("Annualized Index Values for {}".format(current_state))
        for element in annualized_data[current_state]:
            print(element)
        list_inputs.remove(current_state)


if __name__ == "__main__":
    main()