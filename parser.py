import matplotlib.pyplot as plt
from utils import *



# s3 Views
#   -CB-GET
#   -CB-SAVE
#   -CB-DELETE
#   -ERRORS

s3_frame = load_or_generate_frame("s3", "GENERATE")
s3_frame_filter = filter_frame(s3_frame, filter="Error Message")
plot_frames(s3_frame, difference=s3_frame_filter)

lasso_frame = load_or_generate_frame("lasso", "GENERATE")
lasso_frame_filter = filter_frame(lasso_frame, filter="ChangePassword")
plot_frames(lasso_frame, difference=[], views=lasso_frame_filter)
plt.show()
