"""
This is just where things start, kinda ugly right now but I don't really see the point in cleaning it
Everyone that looks into this will likely want to do different things with it so this is essentially
a scratch work zone

TODO make Documentation for useful filter names per app and how to use these base parts
TODO Keep in mind this will likely need to pull from another folder eventually, maybe an argparser to take that folder?
"""
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from fixers import check_and_fix_unformatted_logs
from utils import load_or_generate_frame, final_touches

register_matplotlib_converters()

start = '2019-6-20'
end = '2019-7-30'
fix = False

# If you only want a couple of apps uncomment the ones you want
apps = {
    # 'imsws',
    # 'lasso',
    'mchaos',
    # 'mchec',
    # 'oauth',
    # 'pdr',
    # 'profilerest',
    # 'ps3',
    # 's3',
    # 'scomp',
    # 'sphinx'
}

# Uncomment for all apps to be observed
# apps = os.listdir("logs/unformatted_logs")

if fix:
    check_and_fix_unformatted_logs(apps)
    exit(0)

if "s3" in apps:
    s3_frame = load_or_generate_frame("s3", "LOAD")
    s3_frame = final_touches(s3_frame,
                             view_cols="",
                             remove_cols="",
                             start_date=start,
                             end_date=end,
                             trim_outliers=True)
    s3_frame.plot()

if "lasso" in apps:
    lasso_frame = load_or_generate_frame("lasso", "LOAD")
    lasso_frame = final_touches(lasso_frame,
                                remove_cols="",
                                view_cols="",
                                start_date=start,
                                end_date=end,
                                trim_outliers=True)
    lasso_frame.plot()

if "mchec" in apps:
    mchec_frame = load_or_generate_frame("mchec", "LOAD")
    mchec_frame = final_touches(mchec_frame,
                                remove_cols="",
                                view_cols="",
                                start_date=start,
                                end_date=end,
                                trim_outliers=True)
    mchec_frame.plot()

if "pdr" in apps:
    pdr_frame = load_or_generate_frame("pdr", "GENERATE")
    pdr_frame = final_touches(pdr_frame,
                              remove_cols="",
                              view_cols="",
                              start_date=start,
                              end_date=end,
                              trim_outliers=True)
    pdr_frame.plot()

if "scomp" in apps:
    scomp_frame = load_or_generate_frame("scomp", "GENERATE")
    scomp_frame = final_touches(scomp_frame,
                                remove_cols="",
                                view_cols="",
                                start_date=start,
                                end_date=end,
                                trim_outliers=True)
    scomp_frame.plot()

if "sphinx" in apps:
    sphinx_frame = load_or_generate_frame("sphinx", "GENERATE")
    sphinx_frame = final_touches(sphinx_frame,
                                 remove_cols="",
                                 view_cols="",
                                 start_date=start,
                                 end_date=end,
                                 trim_outliers=True)
    sphinx_frame.plot()

if "imsws" in apps:
    imsws_frame = load_or_generate_frame("imsws", "GENERATE")
    imsws_frame = final_touches(imsws_frame,
                                remove_cols="",
                                view_cols="",
                                start_date=start,
                                end_date=end,
                                trim_outliers=True)
    imsws_frame.plot()

if "mchaos" in apps:
    mchaos_frame = load_or_generate_frame("mchaos", "GENERATE")
    mchaos_frame = final_touches(mchaos_frame,
                                 remove_cols="",
                                 view_cols="",
                                 start_date=start,
                                 end_date=end,
                                 trim_outliers=True)
    mchaos_frame.plot()

if "oauth" in apps:
    oauth_frame = load_or_generate_frame("oauth", "GENERATE")
    oauth_frame = final_touches(oauth_frame,
                                remove_cols="",
                                view_cols="",
                                start_date=start,
                                end_date=end,
                                trim_outliers=True)
    oauth_frame.plot()

if "ps3" in apps:
    ps3_frame = load_or_generate_frame("ps3", "GENERATE")
    ps3_frame = final_touches(ps3_frame,
                              remove_cols="",
                              view_cols="",
                              start_date=start,
                              end_date=end,
                              trim_outliers=True)
    ps3_frame.plot()

if "profilerest" in apps:
    profilerest_frame = load_or_generate_frame("profilerest", "GENERATE")
    profilerest_frame = final_touches(profilerest_frame,
                                      remove_cols="",
                                      view_cols="",
                                      start_date=start,
                                      end_date=end,
                                      trim_outliers=True)
    profilerest_frame.plot()
plt.show()
