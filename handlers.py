from lxml import html
from datetime import datetime
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
        lasso_dict = parse_three_col_table(body, lasso_dict, table_name="errorTable", alt_title="ErrorCode->Message")
        lasso_dict = parse_basic_tables(body, lasso_dict, table_name="attackTable", alt_title="Vulnerabilities")

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
        body = html.fromstring(body)
        mchec_dict = dict()
        mchec_dict = parse_basic_tables(body, mchec_dict, table_name="apiTable", table_range=(0, 8))

        mchec_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")
        mchec_list.append(mchec_dict)
    return mchec_list
