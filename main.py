import matplotlib.pyplot as plt
from utils import *
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

"""
This is just where things start, kinda ugly right now but I don't really see the point in cleaning it
Everyone that looks into this will likely want to do different things with it so this is essentially
a scratch work zone

TODO make Documentation for useful filter names per app and how to use these base parts
"""

start = '2019-4-14'
end = '2019-7-14'

# s3_frame = load_or_generate_frame("s3", "LOAD")
# s3_frame = final_touches(s3_frame,
#                          view_cols="CB",
#                          remove_cols="Error",
#                          start_date=start,
#                          end_date=end,
#                          trim_outliers=True)
# s3_frame.plot()
#
# lasso_frame = load_or_generate_frame("lasso", "LOAD")
# lasso_frame = final_touches(lasso_frame,
#                             remove_cols="Vulnerabilities_a",
#                             view_cols="Login",
#                             start_date=start,
#                             end_date=end,
#                             trim_outliers=True)
# lasso_frame.plot()

mchec_frame = load_or_generate_frame("mchec", "GENERATE")
mchec_frame = final_touches(mchec_frame,
                            remove_cols="",
                            view_cols="PlatformType",
                            start_date=start,
                            end_date=end,
                            trim_outliers=True)
mchec_frame.plot()

plt.show()
