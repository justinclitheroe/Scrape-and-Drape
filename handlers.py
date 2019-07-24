"""
Handlers exist to create the list of dictionaries that will eventually become a panda frame using the parsers found
in parsers.py

All Handlers follow roughly the same format
    for file_name in list of files:
        open file at filename
        read html in file
        create or clear a dictionary
        parse the tables on the html page using one or many of the parsers
        get the date from the filename
        append the dict to the end of the list (best practice for fast dataframe creation)
    return proto-frame
"""
from datetime import datetime
from fixers import *
from parsers import *



def handle_s3_html(files):
    cb_list = []
    for file in files:
        with open(file, "r") as f:
            body = f.read()
        body = html.fromstring(body)
        # Requests
        cb_dict = dict()
        cb_dict = parse_basic_tables(body, cb_dict,
                                     table_name="apiTable")
        cb_dict = parse_basic_tables(body, cb_dict,
                                     table_name="errorTable")
        cb_dict = parse_basic_tables(body, cb_dict,
                                     table_name="errorMessageTable")
        cb_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")
        cb_list.append(cb_dict)
    return cb_list


def handle_lasso_html(files):
    lasso_list = []
    for file in files:
        with open(file, "r") as f:
            body = f.read()
        body = html.fromstring(body)
        lasso_dict = dict()
        lasso_dict = parse_basic_tables(body, lasso_dict, table_name="apiTable", table_range=(0, 8))
        lasso_dict = parse_basic_tables(body, lasso_dict, table_name="componentTable")
        lasso_dict = parse_basic_tables(body, lasso_dict, table_name="attackTable", alt_title="Vulnerabilities")
        lasso_dict = parse_three_col_table(body, lasso_dict, title="ERROR", table_name="errorTable")

        lasso_dict["TOTAL_ERRORS"] = int(body.xpath('/html/body/div[4]/h3')[0].text_content().split(":")[1])
        # lasso_dict[""] = int(body.xpath('')[0].text_content())

        lasso_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")
        lasso_list.append(lasso_dict)
    return lasso_list


def handle_mchec_html(files):
    mchec_list = []
    for file in files:
        with open(file, "r") as f:
            body = f.read()
        mchec_dict = dict()
        body = html.fromstring(body)
        mchec_dict = parse_mchec_req_res_table(body, mchec_dict, title="REQRES", table_name="reqRespTable")
        # This function is busted for now
        mchec_dict = parse_mchec_component_table(body, mchec_dict, title="ComponentResults")
        mchec_dict = parse_three_col_table(body, mchec_dict, "Error", "errorTable")
        mchec_dict = parse_basic_tables(body, mchec_dict, table_name="platformTable", alt_title="PlatformType")
        mchec_dict = parse_three_col_table(body, mchec_dict, "NotificationCode", "notificationTable")
        mchec_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")
        mchec_list.append(mchec_dict)
    return mchec_list
