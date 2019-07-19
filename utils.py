import os
import re

import pandas as pd
from handlers import *


def get_files_list(app):
    """
    Gets a list of file paths for the  handlers (Not the files themselves)
    """
    path = "logs/" + app
    files = [os.path.join(os.getcwd(), path, f)
             for f in os.listdir(path)
             if os.path.isfile(os.path.join(path, f))]
    return files


def handle_html(file_names, appname):
    """
    Handles the routing for the frame creators

    Python doesn't have cases which is sad in this one context
    """
    if appname is "s3":
        data = handle_s3_html(file_names)
    elif appname is "lasso":
        data = handle_lasso_html(file_names)
    elif appname is "mchec":
        data = handle_mchec_html(file_names)
    return data


def load_or_generate_frame(appname, load_or_generate="GENERATE"):
    """
    GENERATE: Generates a data frame from the html files in the ./logs/{appname} directory
    LOAD: the handlers run pretty fast because pandas is tight as hell but
          there's no reason to do all that computation more than once a day
    """
    if load_or_generate == "LOAD":
        return pd.read_pickle("./{}.pkl".format(appname))
    elif load_or_generate == "GENERATE":
        files = get_files_list(appname)
        # Get a list of dictionary lists ready to be turned into pd frames
        data = handle_html(files, appname)
        # Turn those lists into dicts
        return pd.DataFrame(data)


def frame_format(frame, start_date, end_date):
    """
    Returns a frame with data only between the given dates
    """
    mask = (frame.index >= start_date) & \
           (frame.index <= end_date)
    return frame[mask]


def get_filters(frame, show="", hide=""):
    """
    gets your column filters for "final_touches()
    """
    show_filter = frame_filter(frame, filter=show)
    hide_filter = frame_filter(frame, filter=hide)
    return show_filter, hide_filter


def frame_filter(frame, filter=""):
    """
    returns a list of column names based on a filter
    """
    regex = re.compile(r'{}'.format(filter))
    return [col for col in frame.columns if re.search(regex, col)]


def remove_outliers(frame):
    """
    Removes any data that's outside of 3 standard deviations in either direction
    """
    from numpy import abs
    frame = frame[abs(frame - frame.mean()) <= (3 * frame.std())]
    frame = frame.fillna(frame.mean())
    return frame


def final_touches(frame, view_cols="", remove_cols="", start_date="", end_date="", trim_outliers=True):
    """
    takes a frame and changes it based on the parameters given,
    the *_cols parameters control which columns are taken out
    the *_date parameters control which date-rows are shown
    """
    view_cols, remove_cols = get_filters(
        frame,
        show=view_cols,
        hide=remove_cols
    )
    frame.index = frame["DATE"]
    frame = frame.drop("DATE", 1)
    frame = frame_format(frame, start_date, end_date)
    if view_cols:
        frame = frame.loc[:, view_cols]
    if remove_cols:
        frame = frame.loc[:, frame.columns.difference(["DATE"] + remove_cols)]
    if trim_outliers:
        frame = remove_outliers(frame)
    return frame


def save_frame(frame, appname):
    """
    Saves the data with the given name, not super necessary but pretty convenient
    """
    frame.to_pickle("{}.pkl".format(appname))
