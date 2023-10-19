"""
Author: Jamie Antal
Date: 12/5/2022
Notes:
    to future coders/readers, I want to warn that I assumed that for plot_whiskers(), it is assumed that it will depend
    on the data it was given, meaning it could be limited to time period. This is because there's no specific
    instructions on that part
"""


import index_tools as it
import numpy.ma as ma
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import copy


def build_plottable_array(xyears, regiondata):
    """
    will receive specified annual state data with specified years to convert it into masked array for matplotlib
    functions to use
    :param xyears: a list of integer year values
    :param regiondata: a list of AnnualHPI objects
    :return: an array suitable for plotting with the matplotlib module
    """
    x_list = []
    years_list = list(i for i in range(xyears[0], xyears[-1] + 1))
    for year in years_list:
        saved_element = None
        for element in regiondata:
            if int(element.year) == year:
                saved_element = element
        if saved_element is not None:
            x_list.append(float(saved_element.index))
        else:
            x_list.append(saved_element)
    weird_array = ma.array(x_list)
    weird_array = ma.masked_where(weird_array == None, weird_array)
    return weird_array


def filter_years(data, year0, year1):
    """
    will receive and convert a data into data with limited scope on time period gave by the user
    :param data: a dictionary mapping from regions to lists of AnnualHPI objects
    :param year0: must be int and less than year1; represents starting year
    :param year1: must be int and more than year0; represents ending year
    :return: a refined data that's filtered to only between year0 and year1
    """
    if year0 > year1:
        print("Error. year0 must be less than year1.")
        quit()
    years_list = [i for i in range(year0, year1 + 1)]
    refined_dict = {}
    key_list = list(data.keys())
    for key in key_list:
        for element in data[key]:
            if int(element.year) in years_list:
                if key in refined_dict:
                    refined_dict[key].append(element)
                else:
                    refined_dict[key] = [element]
    return refined_dict


def plot_HPI(data, regionList):
    """
    will create and plot out a graph presenting the changes in home price indinces between given states; prints a
    message instructing user to continue
    :param data: a dictionary mapping a state or zip code to a list of AnnualHPI objects
    :param regionList: a list of key values whose type is string
    :return:
    """
    years_list = []
    for key in regionList:
        for element in data[key]:
            if int(element.year) not in years_list:
                years_list.append(int(element.year))
    years_list.sort()
    for key in regionList:
        sample_plot = build_plottable_array(years_list, data[key])
        plt.plot(years_list, sample_plot, "*", linestyle="-")
    plt.title("Home Price Indices: {}-{}".format(years_list[0], years_list[-1]))
    legend = plt.gca()
    legend.legend(regionList)
    plt.show()
    print("Close display window to continue")


def plot_whiskers(data, regionList):
    """
    will create and plot out a whiskers presenting the range, median, and means in home price indinces between
    given states; prints a message instructing user to continue
    :param data: a dictionary mapping a state or zip code to a list of AnnualHPI objects
    :param regionList: a list of key values whose type is string
    :return:
    """
    box_list = []
    for key in regionList:
        stuff_list = []
        for element in data[key]:
            stuff_list.append(float(element.index))
        box_list.append(stuff_list)
    plt.boxplot(box_list, labels=regionList, showmeans=True)
    plt.title("Home Price Indice Comparsion. Median is a line. Mean is a triangle.")
    plt.show()
    print("Close display window to continue")



def main():
    """
    will prompt user for filepath, starting year, ending year, and states to check. If the filepath is not ZIP5, it
    will print out the highest and lowest home price indexs of user's chosen states. If the filepath is ZIP5, it will
    do nothing. after that, both filepaths will continue to use functions provided in this module to plot out the
    states in graph and whiskers. finally, it will print out two same message instructing user to continue; this is
    because those two plot functions follow each other in sequence
    :return:
    """
    file_input = input("Enter house price index filename: ")
    if "ZIP" in file_input:
        state_data = False
        annualized_data = it.read_zip_house_price_data("data/" + file_input)
    else:
        state_data = True
        raw_data = it.read_state_house_price_data("data/" + file_input)
        annualized_data = it.annualize(raw_data)
    year0_input = int(input("Enter the start year of the range to plot: "))
    year1_input = int(input("Enter the end year of the range to plot: "))
    list_inputs = []
    copy_inputs = []
    user_input = input("Next region of interest( Hit ENTER to stop): ")
    while user_input != "":
        list_inputs.append(user_input)
        copy_inputs.append(user_input)
        user_input = input("Next region of interest( Hit ENTER to stop): ")
    while len(list_inputs) != 0 and state_data == True:
        current_state = list_inputs[0]
        it.print_range(raw_data, current_state)
        list_inputs.remove(current_state)
    refined_data = filter_years(annualized_data, year0_input, year1_input)
    plot_HPI(refined_data, copy_inputs)
    plot_whiskers(refined_data, copy_inputs)


if __name__ == "__main__":
    main()
