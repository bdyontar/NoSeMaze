# -*- coding: utf-8 -*-
"""
This module contains methods used for e-mailing. Currently, is used to write 
notification message in a folder. Codes to send e-mail is saved as commentar.

Custom notification messages are saved in Email folder also in HelperFunctions
folder as text files. The text files can be edited accordingly, but the keywords
with curly braces must be included in the text, as the keywords will be used to
display some information messages from the methods below.
"""
"""
Copyright (c) 2019, 2022 [copyright holders here]

This file is part of NoSeMaze.

NoSeMaze is free software: you can redistribute it and/or 
modify it under the terms of GNU General Public License as 
published by the Free Software Foundation, either version 3 
of the License, or (at your option) at any later version.

NoSeMaze is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public 
License along with NoSeMaze. If not, see https://www.gnu.org/licenses.
"""

# Modules for e-mail messaging
#from email.message import EmailMessage
#import smtplib
#import time

# Import custom module.
from Analysis import Analysis
from Sensors import constants

# Import standard modules.
import datetime
import traceback
import os
import numpy as np
import scipy.stats as stats
Z = stats.norm.ppf
message_folder_path = None


def parse_list(string):
    """
    Method used to parse string of a list into a list of float, then sum it.

    Parameters
    ----------
    string : str
        String of a list to be parsed.

    Return
    ------
    result : float
        Sum of the parsed list.
    """
    result = np.sum(list(map(float, string.strip('[ ]').split())))

    return result


def _get_file_path(file):
    """Check wether the file is in Email folder, if folder exists.

    Parameters
    ----------
    file : str
        Name of the file to be checked.
    
    Returns
    -------
    res : str | None
        Result of checking file. If file can be found, return the file path. Else return None.
    """

    currWorkDir = os.getcwd()
    if "NoSeMazeControl" in currWorkDir:
        filepath = "./HelperFunctions/Email/" + file
    else:
        filepath = "./NoSeMazeControl/HelperFunctions/Email/" + file
    
    if os.path.isfile(filepath):
        return filepath
    else:
        return None

def deadmans_switch(experiment):
    """
    Notification every day to indicate if experiment is running.

    Parameters
    ----------
    exeperiment : Experiment.experiment
        Instance of Experiment.experiment class to take information from.
    """

    subject = "Report of the Hours"
    filename = _get_file_path("deadmans_switch.txt")
    if filename:
        with open(filename, encoding='utf-8') as f:
            content = f.read()
    else:  # set content to default message if text file does not exist
        content = "Hello {name}, this is the overview.\n\n{overview}"

    # table will be shown in the notification message. First, header of the
    # table should be defined. Then, the table will be extended with the actual
    # data

    # Create header for table.
#    table = ['Tag Id | Trials | Trials 12 Hrs | Wait 12 Hrs | Rewarded (R) 12 Hrs | Not-Rewarded (NR) 12 Hrs | Avg. Wait Licks R 12h | Avg. Wait Licks NR 12h | Avg. Response Licks R 12h | Avg. Response Licks NR 12h | Licks R 12h | Licks NR 12h | Trials R 12h | Trials NR 12h | Water Given 12 Hrs ']
    table = ['Tag Id | Trials | Trials 12 Hrs | Water Given 12 Hrs']

    # Create list of attachment to be attached in e-mail.
    attachment = list()
    for animal in experiment.animal_list.keys():
        this_mouse = experiment.animal_list[animal]
        id = this_mouse.id
        n_trials = Analysis.n_trials_performed(this_mouse)
        n_trials_last_12h = Analysis.n_trials_since(
            this_mouse, datetime.datetime.now() - datetime.timedelta(hours=12))

        if this_mouse.fname is not None and os.path.isfile(this_mouse.fname):
            with open(this_mouse.fname, 'r', newline='') as f:
                licks_list = f.readlines()
                licks_list = licks_list[1:]
            for i, row in enumerate(licks_list):
                licks_list[i] = row.split(';')
        else:
            licks_list = list()

        if len(licks_list) != 0:
            licks_T = list(map(list, zip(*licks_list)))
            y = None
            for x in range(len(licks_T[0])):
                time_x = datetime.datetime.strptime(
                    licks_T[0][x].strip('\n'), '%Y-%m-%d %H:%M:%S.%f')
                if time_x <= datetime.datetime.now() - datetime.timedelta(hours=12):
                    y = x
            if y != None:
                try:
                    water_given = np.sum(list(map(float, licks_T[7][y:])))
                except:
                    water_given = np.sum(list(map(parse_list, licks_T[7][y:])))
            else:
                try:
                    water_given = np.sum(list(map(float, licks_T[7])))
                except:
                    water_given = np.sum(list(map(parse_list, licks_T[7][y:])))
        else:
            water_given = 0.0

        # Table to be shown in attachment.
        analysis_table = list()
        for schedule in this_mouse.schedule_list:
            left = 0
            right = 0
            correct_left = 0
            correct_right = 0
            num_rew_prob = 0
            num_to_reject = 0
            correct_rew_prob = 0
            num_rew_prob_l = 0
            num_rew_prob_r = 0
            correct_rejection = 0
            hit_gng = 0.01
            false_gng = 0.01
            hit_lr = 0.01
            false_lr = 0.01

            for trial in schedule.trial_list:
                if trial.rewarded[0] == 0 and trial.rewarded[1] != 0:
                    right += 1
                    if trial.correct:
                        correct_right += 1
                elif trial.rewarded[0] != 0 and trial.rewarded[1] == 0:
                    left += 1
                    if trial.correct:
                        correct_left += 1
                elif trial.rewarded[0] != 0 and trial.rewarded[1] != 0:
                    num_rew_prob += 1
                    if trial.correct:
                        correct_rew_prob += 1
                        if trial.response[0]:
                            num_rew_prob_l += 1
                        elif trial.response[1]:
                            num_rew_prob_r += 1
                elif trial.rewarded[0] == 0 and trial.rewarded[1] == 0:
                    num_to_reject += 1
                    if trial.correct:
                        correct_rejection += 1

            if len(schedule.trial_list) == 0:
                analysis_table.append(
                    "{name} | 00.00 % | 00.00 % | 00.00 % | 00.00 % | NaN | NaN | 0 | 0\n".format(name=str(schedule.id)))
            elif left == 0:
                percent_correct_left = 0
                if right == 0:
                    percent_correct_right = 0
                else:
                    percent_correct_right = correct_right/right * 100
                    hit_lr = 0.01
                    false_lr = 1 - percent_correct_right/100

                if num_rew_prob == 0 and num_to_reject != 0:
                    percent_correct_rew_prob = 0
                    percent_correct_rejection = correct_rejection/num_to_reject*100
                    hit_gng = 0.01
                    false_gng = 1 - percent_correct_rejection/100
                elif num_to_reject == 0 and num_rew_prob != 0:
                    percent_correct_rew_prob = correct_rew_prob/num_rew_prob*100
                    percent_correct_rejection = 0
                    hit_gng = percent_correct_rew_prob/100
                    false_gng = 0.99
                elif num_to_reject == 0 and num_rew_prob == 0:
                    percent_correct_rew_prob = 0
                    percent_correct_rejection = 0
                else:
                    percent_correct_rew_prob = correct_rew_prob/num_rew_prob*100
                    percent_correct_rejection = correct_rejection/num_to_reject*100
                    hit_gng = percent_correct_rew_prob/100
                    false_gng = 1 - percent_correct_rejection/100

                if hit_lr == 1:
                    hit_lr = 0.99
                elif hit_lr == 0:
                    hit_lr = 0.01
                if false_lr == 1:
                    false_lr = 0.99
                elif false_lr == 0:
                    false_lr = 0.01
                if hit_gng == 1:
                    hit_gng = 0.99
                elif hit_gng == 0:
                    hit_gng == 0.01
                if false_gng == 1:
                    false_gng = 0.99
                elif false_gng == 0:
                    false_gng = 0.01

                if left + right == 0:
                    dprime_lr = "NaN"
                else:
                    dprime_lr = Z(hit_lr)-Z(false_lr)

                if num_to_reject + num_rew_prob == 0:
                    dprime_gng = "NaN"
                else:
                    dprime_gng = Z(hit_gng)-Z(false_gng)

                analysis_table.append("{name} | {percentl:.2f} | {percentr:.2f} | {percentg:.2f} | {percentrej:.2f} | {dprime1:.2f} | {dprime2:.2f} | {no_gng_l} | {no_gng_r}\n".format(name=str(schedule.id), percentl=percent_correct_left,
                                      percentr=percent_correct_right, percentg=percent_correct_rew_prob, percentrej=percent_correct_rejection, dprime1=float(dprime_lr), dprime2=float(dprime_gng), no_gng_l=num_rew_prob_l, no_gng_r=num_rew_prob_r))

            elif left != 0:
                percent_correct_left = correct_left/left*100
                hit_lr = percent_correct_left/100

                if right == 0:
                    percent_correct_right = 0
                    false_lr = 0.99
                else:
                    percent_correct_right = correct_right/right*100
                    false_lr = 1 - percent_correct_right/100

                if num_rew_prob == 0 and num_to_reject != 0:
                    percent_correct_rew_prob = 0
                    percent_correct_rejection = correct_rejection/num_to_reject*100
                    hit_gng = 0.01
                    false_gng = 1 - percent_correct_rejection/100
                elif num_to_reject == 0 and num_rew_prob != 0:
                    percent_correct_rew_prob = correct_rew_prob/num_rew_prob*100
                    percent_correct_rejection = 0
                    hit_gng = percent_correct_rew_prob/100
                    false_gng = 0.99
                elif num_to_reject == 0 and num_rew_prob == 0:
                    percent_correct_rejection = 0
                    percent_correct_rew_prob = 0
                elif num_to_reject != 0 and num_rew_prob != 0:
                    percent_correct_rew_prob = correct_rew_prob/num_rew_prob*100
                    percent_correct_rejection = correct_rejection/num_to_reject*100
                    hit_gng = percent_correct_rew_prob/100
                    false_gng = 1 - percent_correct_rejection/100

                if hit_lr == 1:
                    hit_lr = 0.99
                elif hit_lr == 0:
                    hit_lr = 0.01
                if false_lr == 1:
                    false_lr = 0.99
                elif false_lr == 0:
                    false_lr = 0.01

                if hit_gng == 1:
                    hit_gng = 0.99
                elif hit_gng == 0:
                    hit_gng == 0.01
                if false_gng == 1:
                    false_gng = 0.99
                elif false_gng == 0:
                    false_gng = 0.01

                dprime_lr = Z(hit_lr)-Z(false_lr)

                if num_to_reject + num_rew_prob == 0:
                    dprime_gng = "Nan"
                else:
                    dprime_gng = Z(hit_gng)-Z(false_gng)

                analysis_table.append("{name} | {percentl:.2f} | {percentr:.2f} | {percentg:.2f} | {percentrej:.2f} | {dprime1:.2f} | {dprime2:.2f} | {no_gng_l} | {no_gng_r}\n".format(name=str(schedule.id), percentl=percent_correct_left,
                                      percentr=percent_correct_right, percentg=percent_correct_rew_prob, percentrej=percent_correct_rejection, dprime1=float(dprime_lr), dprime2=float(dprime_gng), no_gng_l=num_rew_prob_l, no_gng_r=num_rew_prob_r))

        # Data to be shown in e-mail message.
        row = ' | '.join([id,
                          str(n_trials),
                          str(n_trials_last_12h),
                          '{0:.2f} ml'.format(water_given)])
        table.append(row)

        if os.path.isfile(experiment.logs_path+'/licks_log_'+animal+'.txt'):
            with open(experiment.logs_path+'/licks_log_'+animal+'.txt', 'r') as f:
                log = f.readlines()
            if len(log) > 100:
                header = [log[0]]
                header.extend(log[-100:])
                log = header
            log.append(
                "\n\nif d'-lr positive, left was readilly recognized; negative, right was readilly recognized.")
            log.append("\n\nSchedule Name | Percent Correct Left | Percent Correct Right | Percent Correct Rewarded | Percent Correct Rejection | d'-LR | d'-GNG | n GNG-left | n GNG-right\n")
            log.extend(analysis_table)
            attachment.append(
                dict(log="".join(log), name='licks_log_'+animal+'.txt'))
        else:
            attachment.append(
                dict(log="The mouse hasn't licked...", name='licks_log_'+animal+'.txt'))

    # Sensornode status
    offline_nodes = []
    node_info = "All nodes online"
    
    # Check if any nodes are offline == False
    for key in constants.node_connected.keys():
        if constants.node_connected[key] == False:
            offline_nodes.append(key)
    
    # If offline nodes exist, write a message
    if offline_nodes:
        node_info = f"The following nodes are offline: {''.join(str(offline_nodes))}"

    table = '\n'.join(table)
    content = content.format(name='{name}', overview=table, node_overview=node_info)

    send(subject, content, attachment)


def crash_error(exctype, value, tb):
    """
    Get traceback if software is crashed and send e-mail. Currently, a message 
    will be written in a folder.

    Parameters
    ----------
    exctype : Type of Exception
        Type of exception

    value : int
        Error id.

    tb : obj
        Traceback object.
    """

    subject = "Software has crashed"
    error = "".join(traceback.format_exception(exctype, value, tb))
    filename = _get_file_path("crash_error.txt")
    if filename:
        with open(filename, encoding='utf-8') as f:
            content = f.read()
    else:
        content = "Hello {name}, this the error.\n\n{error}"
    content = content.format(name='{name}', error=error)
    attachment = None
    send(subject, content, attachment)


def warning_licks(logs_path, namelist):
    """
    Send warning e-mail if any mouse has not licked in a period of time.
    Currently, a message will be written in a folder.

    Parameters
    ----------
    logs_path : str
        Directory path to folder with all licks log of mice.

    namelist : list
        List of mouse's ID which has not licked in a period of time.
    """
    subject = "Warning"
    mice = "\n".join(namelist)
    filename = _get_file_path("warning_licks.txt")
    if filename:
        with open(filename, encoding='utf-8') as f:
            content = f.read()
    else:
        content = "Hello {name}, this is the lists of mice.\n\n{mice}"
    content = content.format(name='{name}', mice=mice)
    attachment = list()
    for name in namelist:
        if os.path.isfile(logs_path+'/licks_log_'+name+'.txt'):
            with open(logs_path+'/licks_log_'+name+'.txt', 'r') as f:
                log = f.readlines()
            if len(log) > 100:
                log = log[-100:]
            attachment.append(
                dict(log="".join(log), name='licks_log_'+name+'.txt'))
        else:
            attachment.append(
                dict(log="The mouse hasn't licked...", name='licks_log_'+name+'.txt'))

    send(subject, content, attachment)


def send(subject, content, attachment):
    """
    Write a message with subject, content and attachment in a folder.

    Parameters
    ----------
    subject : str
        Subject of message

    content : str
        Content of message

    attachement : list
        List of attachment.
    """

    if message_folder_path is not None:
        today = datetime.datetime.today().isoformat().split(".")[
            0].replace(":", "")
        dire = message_folder_path + '/' + today + '/'
        if not os.path.isdir(dire):
            os.mkdir(dire)

        filename = dire + subject + ".txt"  # File in folder

        text = content.format(name="User")
 
        with open(filename, 'w', encoding='utf-8-sig') as f:
            f.write(text)

        if attachment is not None:
            for attach in attachment:
                fn = dire + attach['name']
                with open(fn, 'w', newline='') as f:
                    f.write(attach['log'])

# def send(subject, content, attachment):
#    """
#    Send e-mail with subject, content, and attachment.
#
#    Parameters
#    ----------
#    subject : str
#        Subject of message
#
#    content : str
#        Content of message
#
#    attachement : list
#        List of attachment.
#    """
#
#    filename = os.getcwd()+'\\HelperFunctions\\Email\\mailing_list.txt'
#    with open(filename,encoding='utf-8') as f:
#        mlist = f.readlines()
#        for i,item in enumerate(mlist):
#            mlist[i] = item.strip("\n")
#
#    msg = list()
#    for i, email in enumerate(mlist):
#        name = email.split(".")[0].capitalize()
#        msg.append(EmailMessage())
#        msg[i]['From'] = "beast@zi-mannheim.de"
#        msg[i]['Subject'] = subject
#        msg[i]['To'] = email
#        msg[i].set_content(content.format(name=name))
#        if attachment is not None:
#            for att in attachment:
#                msg[i].add_attachment(att['log'], subtype ='txt', filename = att['name'])
#
#    try:
#        with smtplib.SMTP('smtp.zi.local') as server:
#            server.starttls()
#            print('\nsending email: start tls')
#            for i in range(len(msg)):
#                print('sending email: sending message...')
#                server.send_message(msg[i])
#                print('sending email: {} message(s) sent'.format(i+1))
#                time.sleep(0.05)
#            print('all message(s) sent. Date:', datetime.datetime.now().isoformat())
#    except:
#        print('mail cannot be sent. Date;', datetime.datetime.now().isoformat())
