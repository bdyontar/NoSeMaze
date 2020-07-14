"""
This module contains method to show risk taskin performance of mouses.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime as dt

def show_risk_per_mouse(data, mouse, bins):
    """
    Plot rate of risk taken per mouse.
    
    Parameters
    ----------
    data : 2d-list of float
        Data to be plotted.
    
    mouse : str
        Id of the mouse.
    
    bins : int
        Bin size.
    """
    
    fig, ax = plt.subplots(3,1)
    fig.suptitle("Percent of Risk. ID: {}. \nN = {}, High Risk Probability = 0.4, Low Risk Probability = 0.8, Bin = {}".format(mouse, len(data[0]), bins))
    fig.autofmt_xdate()
    ax[0].plot(data[0], data[-6], label = 'high')
    ax[0].plot(data[0], data[-4], label = 'low')
    ax[0].grid()
    ax[0].legend()
    ax[0].set_ylim(0,100)
    ax[0].set_ylabel("percent [%]")
    ax[0].set_title("Odour 1")
    
    ax[1].plot(data[0], data[-5], label = 'high')
    ax[1].plot(data[0], data[-3], label = 'low')
    ax[1].grid()
    ax[1].legend()
    ax[1].set_ylim(0,100)
    ax[1].set_ylabel("percent [%]")
    ax[1].set_title("Odour 2")
    
    ax[2].plot(data[0], data[-2], label = 'high')
    ax[2].plot(data[0], data[-1], label = 'low')
    ax[2].grid()
    ax[2].legend()
    ax[2].set_ylim(0,100)
    ax[2].set_ylabel("percent [%]")
    ax[2].set_title("Total Risk of Odour 1 and 2")

def show_risk_per_odour(data, mouses, bins):
    """
    Plot rate of risk taken per odour.
    
    Parameters
    ----------
    data : 2d-list of float
        Data to be plotted.
    
    mouse : str
        Id of the mouse.
    
    bins : int
        Bin size.
    """
    
    fig, ax = plt.subplots(2,1)
    ax[0].plot(data[mouses[0]][0], data[mouses[0]][-6], label='high')
    ax[1].plot(data[mouses[1]][0], data[mouses[1]][-6], label='high')
    
    ax[0].plot(data[mouses[0]][0], data[mouses[0]][-4], label='low')
    ax[1].plot(data[mouses[1]][0], data[mouses[1]][-4], label='low')
    
    ax[0].grid()
    ax[1].grid()
    
    ax[0].set_ylim(0,100)
    ax[1].set_ylim(0,100)
    
    fig.autofmt_xdate()
    
    ax[0].set_title("ID: "+mouses[0]+" N = {}".format(len(data[mouses[0]][0])))
    ax[1].set_title("ID: "+mouses[1]+" N = {}".format(len(data[mouses[1]][0])))
    
    ax[0].set_ylabel("percent [%]")
    ax[1].set_ylabel("percent [%]")
    
    ax[0].legend()
    ax[1].legend()
    
    fig.suptitle("Percent of risks odour 1. \nHigh risk prob = 0.4, Low risk prob 0.8, Bin = {}.".format(bins))
    
    fig, ax = plt.subplots(2,1)
    ax[0].plot(data[mouses[0]][0], data[mouses[0]][-5], label='high')
    ax[1].plot(data[mouses[1]][0], data[mouses[1]][-5], label='high')
    
    ax[0].plot(data[mouses[0]][0], data[mouses[0]][-3], label='low')
    ax[1].plot(data[mouses[1]][0], data[mouses[1]][-3], label='low')
    
    ax[0].grid()
    ax[1].grid()
    
    ax[0].set_ylim(0,100)
    ax[1].set_ylim(0,100)
    
    fig.autofmt_xdate()
    
    ax[0].set_title("ID: "+mouses[0]+" N = {}".format(len(data[mouses[0]][0])))
    ax[1].set_title("ID: "+mouses[1]+" N = {}".format(len(data[mouses[1]][0])))
    
    ax[0].set_ylabel("percent [%]")
    ax[1].set_ylabel("percent [%]")
    
    ax[0].legend()
    ax[1].legend()
    
    fig.suptitle("Percent of risk odour 2. \nHigh risk prob = 0.4, Low risk prob 0.8, Bin = {}.".format(bins))

def show_total_risk(data, mouses, bins):
    """
    Plot rate of risk taken.
    
    Parameters
    ----------
    data : 2d-list of float
        Data to be plotted.
    
    mouse : str
        Id of the mouse.
    
    bins : int
        Bin size.
    """
    
    fig, ax = plt.subplots(2,1)
    
    ax[0].plot(data[mouses[0]][0], data[mouses[0]][-2], label='high')
    ax[1].plot(data[mouses[1]][0], data[mouses[1]][-2], label='high')
    
    ax[0].plot(data[mouses[0]][0], data[mouses[0]][-1], label='low')
    ax[1].plot(data[mouses[1]][0], data[mouses[1]][-1], label='low')
    
    ax[0].grid()
    ax[1].grid()
    
    ax[0].set_ylim(0,100)
    ax[1].set_ylim(0,100)
    
    fig.autofmt_xdate()
    
    ax[0].set_title("ID: "+mouses[0]+" Number of data = {}".format(len(data[mouses[0]][0])))
    ax[1].set_title("ID: "+mouses[1]+" Number of data = {}".format(len(data[mouses[1]][0])))
    
    ax[0].set_ylabel("percent [%]")
    ax[1].set_ylabel("percent [%]")
    
    ax[0].legend()
    ax[1].legend()
    
    fig.suptitle("Percent of sum risks odour 1 and odour 2. Bin = {}.".format(bins))

def show_percent_left_right(data, mouses, bins):
    """
    Plot rate of licks between left and right.
    
    Parameters
    ----------
    data : 2d-list of float
        Data to be plotted.
    
    mouse : str
        Id of the mouse.
    
    bins : int
        Bin size.
    """
    
    fig, ax = plt.subplots(2,1)
    
    ax[0].plot(data[mouses[0]][0], data[mouses[0]][2], label='left')
    ax[1].plot(data[mouses[1]][0], data[mouses[1]][2], label='left')
    
    ax[0].plot(data[mouses[0]][0], data[mouses[0]][3], label='right')
    ax[1].plot(data[mouses[1]][0], data[mouses[1]][3], label='right')
    
    ax[0].grid()
    ax[1].grid()
    
    ax[0].set_ylim(0,100)
    ax[1].set_ylim(0,100)
    
    fig.autofmt_xdate()
    
    ax[0].set_title("ID: "+mouses[0]+" Number of data = {}".format(len(data[mouses[0]][0])))
    ax[1].set_title("ID: "+mouses[1]+" Number of data = {}".format(len(data[mouses[1]][0])))
    
    ax[0].set_ylabel("percent [%]")
    ax[1].set_ylabel("percent [%]")
    
    ax[0].legend()
    ax[1].legend()
    
    fig.suptitle("Percent of left and right licks. Bin = {}.".format(bins))

def show_percent_correct(data, mouses, bins):
    """
    Plot rate of correct hit or correct rejection.
    
    Parameters
    ----------
    data : 2d-list of float
        Data to be plotted.
    
    mouse : str
        Id of the mouse.
    
    bins : int
        Bin size.
    """
    
    fig, ax = plt.subplots(2,1)
    
    ax[0].plot(data[mouses[0]][0], data[mouses[0]][1], label=mouses[0])
    ax[1].plot(data[mouses[1]][0], data[mouses[1]][1], label=mouses[1])
    
    ax[0].grid()
    ax[1].grid()
    
    ax[0].set_ylim(0,100)
    ax[1].set_ylim(0,100)
    
    fig.autofmt_xdate()
    
    ax[0].set_title("ID: "+mouses[0]+" Number of data = {}".format(len(data[mouses[0]][0])))
    ax[1].set_title("ID: "+mouses[1]+" Number of data = {}".format(len(data[mouses[1]][0])))
    
    ax[0].set_ylabel("percent [%]")
    ax[1].set_ylabel("percent [%]")
    
    fig.suptitle("Percent of correct licks (licked either left or right and not both). Bin = {}.".format(bins))

def load_data(filepath, start_date, stop_date):
    """Load experiment data. 
    
    Parameters
    ----------
    filepath : str
        Path to experiment file.
        
    start_date : datetime.datetime
        Start date of time of interest.
    
    stop_date : datetime.datetime
        Stop date of time of interest.
    
    Return
    ------
    header : list
        List of header
    all_data : list of dict
        List of dictionary of all data with headers as keys.
    """
    
    with open(filepath) as file:
        header = next(file).split(",")
        tmp = [dict(zip(header,row.split(","))) for row in file]
    
    # change data type accordingly
    all_data = list()
    for data in tmp:
        tmp_dict = dict()
        keys = data.keys()
        if "timestamp" in keys:
            tmp_dict["timestamp"] = dt.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
        if "rewarded" in keys:
            tmp_dict["rewarded"] = dict(zip(["left prob", "right prob", "left reward", "right reward"], map(float, data["rewarded"].split("|"))))
        if "licks after odour" in keys:
            tmp_dict["licks after odour"] = dict(zip(["left","right"],map(int,data["licks after odour"].split("|"))))
        if "water amount" in keys:
            tmp_dict["water amount"] = float(data["water amount"])
        if "correct" in keys:
            tmp_dict["correct"] = int(data["correct"])
        if "timeout" in keys:
            tmp_dict["timeout"] = int(data["timeout"])
        if "licks at waiting" in keys:
            tmp_dict["licks at waiting"] = dict(zip(["left","right"],map(int,data["licks at waiting"].split("|"))))
#        if "total licks" in keys:
#            tmp_dict["total licks"] = dict(zip(["left","right"],map(int,data["total licks"].split("|"))))
        
        #only take from 25.10.2019 till 22.11.2019
        if start_date < tmp_dict["timestamp"] < stop_date:
            all_data.append(tmp_dict)

    return header, all_data

def get_performance(all_data, bins):
    """
    Get performance list in data.
    
    Parameters
    ----------
    all_data : list of dict
        Data is a list of data. 
    
    bins : int
        Window to determine performance.
        
    Return 
    ------
    performance : 2d-list
        A list of performance with the length of data.
    """
    
    def not_left_right(data):
        rewarded = data["rewarded"]
        return rewarded["left prob"] != 0 and rewarded["right prob"] != 0
    
    performance = list()
    
    for i, row in enumerate(all_data):
        if not_left_right(row):
            if i < bins:
                data = all_data[i:i+bins]
            else:
                data = all_data[i-bins:i]
            
            percent_correct = np.mean([d["correct"] for d in data if not_left_right(d)])*100
            right = [d["licks after odour"]["right"]>0 for d in data if not_left_right(d) and d["correct"]]
            left = [d["licks after odour"]["left"]>0 for d in data if not_left_right(d) and d["correct"]]
            
            number_right = sum(right)
            number_left = sum(left)
            
            percent_right = np.mean(right)*100
            percent_left = np.mean(left)*100
            
            number_high_risk_odour1 = sum([d["licks after odour"]["right"]>0 for d in data if not_left_right(d) and d["rewarded"]["right prob"]<=0.5 and d["correct"]])
            number_high_risk_odour2 = sum([d["licks after odour"]["left"]>0 for d in data if not_left_right(d) and d["rewarded"]["left prob"]<=0.5 and d["correct"]])
            
            number_low_risk_odour2 = sum([d["licks after odour"]["right"]>0 for d in data if not_left_right(d) and d["rewarded"]["right prob"]>0.5 and d["correct"]])
            number_low_risk_odour1 = sum([d["licks after odour"]["left"]>0 for d in data if not_left_right(d) and d["rewarded"]["left prob"]>0.5 and d["correct"]])
            
            if number_high_risk_odour1 == 0 and number_low_risk_odour1 == 0:
                percent_high_risk_odour1 = 0
                percent_low_risk_odour1 = 0
            else:
                percent_high_risk_odour1 = number_high_risk_odour1 / (number_high_risk_odour1 + number_low_risk_odour1)  * 100
                percent_low_risk_odour1 = 100 - percent_high_risk_odour1
            
            if number_high_risk_odour2 == 0 and number_low_risk_odour2 == 0:
                percent_high_risk_odour2 = 0
                percent_low_risk_odour2 = 0
            else:
                percent_high_risk_odour2 = number_high_risk_odour2 / (number_high_risk_odour2 + number_low_risk_odour2) * 100
                percent_low_risk_odour2 = 100 - percent_high_risk_odour2
            
            if number_right == 0 and number_left == 0:
                percent_high_risk = 0
                percent_low_risk = 0
            else:
                percent_high_risk = (number_high_risk_odour1 + number_high_risk_odour2) / (number_right + number_left) * 100
                percent_low_risk = (number_low_risk_odour1 + number_low_risk_odour2) / (number_right + number_left) * 100
            
            performance.append([row["timestamp"],percent_correct, percent_left, percent_right, percent_high_risk_odour1, percent_high_risk_odour2, percent_low_risk_odour1, percent_low_risk_odour2, percent_high_risk, percent_low_risk])
    
    return performance

if __name__ == "__main__":
    dropbox_path = "C:\\Users\\Michael\\Dropbox"
    dir_path = "Autonomouse_1\\Log\\logs_experiment20191017"
    mouses = ["0007CD86B3", "0007CE0327"]
    data = dict()
    bins = 150
    start_date = dt(2019,10,27,0,0,0,0)
    stop_date = dt(2019,11,23,0,0,0,0)
    for mouse in mouses:
        filepath = os.path.join(dropbox_path, dir_path, "licks_log_"+mouse+".txt")
        header, all_data = load_data(filepath, start_date, stop_date)
        performance = get_performance(all_data, bins)
        performance = list(map(list,zip(*performance)))
        data[mouse] = performance
#    show_percent_correct(data, mouses, bins)
#    show_percent_left_right(data, mouses,bins)
#    show_total_risk(data, mouses, bins)
#    show_risk_per_odour(data, mouses, bins)
    for mouse in mouses:
        show_risk_per_mouse(data[mouse], mouse, bins)
        
        

