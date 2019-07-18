import matplotlib.pyplot as plt
from utils import *
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# s3 Views
#   -CB-GET
#   -CB-SAVE
#   -CB-DELETE
#   -ERRORS

start = '2019-7-1'
end = '2019-7-14'

s3_frame = load_or_generate_frame("s3", "LOAD")
s3_frame = final_touches(s3_frame,
                         view_cols="CB",
                         remove_cols="Error",
                         start_date=start,
                         end_date=end)
s3_frame.plot()

lasso_frame = load_or_generate_frame("lasso", "LOAD")
lasso_frame = final_touches(lasso_frame,
                            remove_cols="Vulnerabilities_a",
                            view_cols="Login",
                            start_date=start,
                            end_date=end)
lasso_frame.plot()

plt.show()
