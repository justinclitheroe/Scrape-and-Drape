import os
import pandas as pd
from handlers import *


# GENERATE: Generates a data frame from the html files
# LOAD: the handlers run pretty fast because pandas is tight as hell but
#   there's no reason to do all that computation every day
# TODO, make it so that you can just append to an already generated file
def load_or_generate_frame(appname, load_or_generate="GENERATE"):
    if load_or_generate == "LOAD":
        return pd.read_pickle("./{}.pkl".format(appname))
    elif load_or_generate == "GENERATE":
        files = get_files_list(appname)
        # Get a list of dictionary lists ready to be turned into pd frames
        data = handle_html(files, appname)
        # Turn those lists into dicts
        return pd.DataFrame(data)



# Saves the data, not super necessary but pretty convenient
def save_frame(frame, appname):
    frame.to_pickle("{}.pkl".format(appname))


# Gets a list of file paths for the  handlers (Not the files themselves)
def get_files_list(app):
    path = "logs/" + app
    files = [os.path.join(os.getcwd(), path, f)
             for f in os.listdir(path)
             if os.path.isfile(os.path.join(path, f))]
    files.sort()
    return files


# Catch all for frame formatting, currently mostly used to set date ranges,
# probably will pull that part out and put it in the main file
def frame_format(frame):
    frame["DATE"] = pd.to_datetime(frame["DATE"])
    mask = (frame['DATE'] >= '2019-6-1') & \
           (frame['DATE'] <= '2019-7-14')
    return frame[mask]

def filter_frame(frame, filter=""):
    return [col for col in frame if col.startswith(filter)]


# Routing between the handlers, already use the appname to get the file names, might as well use it here too
def handle_html(file_names, appname):
    if appname is "s3":
        data = handle_s3_html(file_names)
    elif appname is "lasso":
        data = handle_lasso_html(file_names)
    return data


def plot_frames(frame, difference=[], views=["all"]):
    views.append("DATE")
    frame = frame_format(frame)
    if difference is not []:
        frame = frame.loc[:, frame.columns.difference(difference)]
    if views[0] == "all":
        frame = frame.loc[:]
    else:
        frame = frame.loc[:, views]
    frame.plot(x="DATE")

# i.columns.difference(exclude)
