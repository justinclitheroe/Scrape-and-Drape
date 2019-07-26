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
        cb_dict = dict()
        body = html.fromstring(body)

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
        lasso_dict = dict()
        body = html.fromstring(body)

        lasso_dict = parse_basic_tables(body, lasso_dict,
                                        table_name="apiTable",
                                        table_range=(0, 8))
        lasso_dict = parse_basic_tables(body, lasso_dict,
                                        table_name="componentTable")
        lasso_dict = parse_basic_tables(body, lasso_dict,
                                        table_name="attackTable",
                                        alt_title="Vulnerabilities")
        lasso_dict = parse_three_col_table(body, lasso_dict,
                                           table_name="errorTable",
                                           title="ERROR")
        lasso_dict["TOTAL_ERRORS"] = int(body.xpath('/html/body/div[4]/h3')[0].text_content().split(":")[1])
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

        mchec_dict = parse_three_col_two_data_table(body, mchec_dict,
                                                    title="REQRES", table_name="reqRespTable",
                                                    col_names=["REQ", "RES"])
        mchec_dict = parse_mchec_component_table(body, mchec_dict,
                                                 title="ComponentResults")
        mchec_dict = parse_three_col_table(body, mchec_dict,
                                           title="Error",
                                           table_name="errorTable")
        mchec_dict = parse_basic_tables(body, mchec_dict,
                                        table_name="platformTable",
                                        alt_title="PlatformType")
        mchec_dict = parse_three_col_table(body, mchec_dict,
                                           table_name="notificationTable",
                                           title="NotificationCode")
        mchec_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")

        mchec_list.append(mchec_dict)
    return mchec_list


def handle_pdr_html(files):
    pdr_list = []
    for file in files:
        with open(file, "r") as f:
            body = f.read()
        pdr_dict = dict()
        body = html.fromstring(body)

        pdr_dict = parse_basic_tables(body, pdr_dict,
                                      table_name="apiTable", alt_title="APICalls")
        pdr_dict = parse_basic_tables(body, pdr_dict,
                                      table_name="componentTable", alt_title="ComponentCalls")
        pdr_dict = parse_basic_tables(body, pdr_dict,
                                      table_name="toIMSWSTable", alt_title="IMSWSCalls")
        pdr_dict = parse_basic_tables(body, pdr_dict,
                                      table_name="toClientTable", alt_title="PDR->Client")
        pdr_dict = parse_basic_tables(body, pdr_dict,
                                      table_name="fromClientTable", alt_title="PDR<-Client")
        pdr_dict = parse_basic_tables(body, pdr_dict,
                                      table_name="policyTable", alt_title="PolicyAPICalls")
        pdr_dict = parse_basic_tables(body, pdr_dict,
                                      table_name="serverTable", alt_title="Servers")

        pdr_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")

        pdr_list.append(pdr_dict)
    return pdr_list


def handle_scomp_html(files):
    scomp_list = []
    for file in files:
        print(file)
        with open(file, "r") as f:
            body = f.read()
        scomp_dict = dict()
        body = html.fromstring(body)

        scomp_dict = parse_basic_tables(body, scomp_dict,
                                        table_name="apiTable",
                                        table_range=[0, 9])

        # Three separated tables for some reason means three separate calls,
        # no reason to write a new parser for that
        scomp_dict = parse_basic_tables(body, scomp_dict,
                                        table_name="left",
                                        alt_title="RequestsByClient")
        scomp_dict = parse_basic_tables(body, scomp_dict,
                                        table_name="right",
                                        alt_title="RequestsByClient")
        scomp_dict = parse_basic_tables(body, scomp_dict,
                                        table_name="center",
                                        alt_title="RequestsByClient")

        scomp_dict = parse_scomp_login_stats(body, scomp_dict,
                                             table_name="loginStatTable",
                                             title="LoginApplicationSource")

        scomp_dict = parse_basic_tables(body, scomp_dict,
                                        table_name="loginProviderTable",
                                        alt_title="SocialLoginsByProvider")

        scomp_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")
        scomp_list.append(scomp_dict)
    return scomp_list


def handle_sphinx_html(files):
    sphinx_list = []
    for file in files:
        with open(file, "r") as f:
            body = f.read()
        sphinx_dict = dict()
        body = html.fromstring(body)

        sphinx_dict = parse_basic_tables(body, sphinx_dict,
                                         table_name="apiTable",
                                         alt_title="APICallTotals")
        sphinx_dict = parse_basic_tables(body, sphinx_dict,
                                         table_name="signatureTable",
                                         alt_title="IncomingTransactions")

        # SCOMP EMAIL NOTIFICATIONS

        sphinx_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")
        sphinx_list.append(sphinx_dict)
    return sphinx_list


def handle_imsws_html(files):
    imsws_list = []
    for file in files:
        with open(file, "r") as f:
            body = f.read()
        imsws_dict = dict()
        body = html.fromstring(body)

        imsws_dict = parse_basic_tables(body, imsws_dict,
                                        table_name="serviceTable",
                                        table_range=[0, 9])

        imsws_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")
        imsws_list.append(imsws_dict)
    return imsws_list


def handle_mchaos_html(files):
    mchaos_list = []
    for file in files:
        with open(file, "r") as f:
            body = f.read()
        mchaos_dict = dict()
        body = html.fromstring(body)

        mchaos_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")
        mchaos_list.append(mchaos_dict)
    return mchaos_list


def handle_oauth_html(files):
    oauth_list = []
    for file in files:
        with open(file, "r") as f:
            body = f.read()
        oauth_dict = dict()
        body = html.fromstring(body)

        oauth_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")
        oauth_list.append(oauth_dict)
    return oauth_list


def handle_ps3_html(files):
    ps3_list = []
    for file in files:
        with open(file, "r") as f:
            body = f.read()
        ps3_dict = dict()
        body = html.fromstring(body)

        ps3_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")
        ps3_list.append(ps3_dict)
    return ps3_list


def handle_profilerest_html(files):
    profilerest_list = []
    for file in files:
        with open(file, "r") as f:
            body = f.read()
        profilerest_dict = dict()
        body = html.fromstring(body)

        profilerest_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")
        profilerest_list.append(profilerest_dict)
    return profilerest_list
