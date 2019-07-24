"""
This is just where things start, kinda ugly right now but I don't really see the point in cleaning it
Everyone that looks into this will likely want to do different things with it so this is essentially
a scratch work zone

TODO make Documentation for useful filter names per app and how to use these base parts
TODO Keep in mind this will likely need to pull from another folder eventually, maybe an argparser to take that folder?
"""
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from utils import load_or_generate_frame, final_touches

register_matplotlib_converters()

start = '2019-4-14'
end = '2019-7-14'

apps = {
    # "s3",
    # "lasso",
    "mchec"
}

# check_and_fix_unformatted_logs(apps)

# exit()

if "s3" in apps:
    s3_frame = load_or_generate_frame("s3", "LOAD")
    s3_frame = final_touches(s3_frame,
                             view_cols="CB",
                             remove_cols="Error",
                             start_date=start,
                             end_date=end,
                             trim_outliers=True)
    print(s3_frame)
    s3_frame.plot()

if "lasso" in apps:
    lasso_frame = load_or_generate_frame("lasso", "LOAD")
    lasso_frame = final_touches(lasso_frame,
                                remove_cols="Vulnerabilities_a",
                                view_cols="Login",
                                start_date=start,
                                end_date=end,
                                trim_outliers=True)
    lasso_frame.plot()

if "mchec" in apps:
    mchec_frame = load_or_generate_frame("mchec", "GENERATE")
    print(mchec_frame.shape)
    mchec_frame = final_touches(mchec_frame,
                                remove_cols=".*RES",
                                view_cols="NotificationCode",
                                start_date=start,
                                end_date=end,
                                trim_outliers=True)
    mchec_frame.plot()

plt.show()
