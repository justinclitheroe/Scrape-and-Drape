from lxml import html
from datetime import datetime


# Parses the most general kind of table
def parse_basic_tables(body, d, table_name, table_range=None, alt_title=""):
    if table_range is not None:
        for i in range(table_range[0], table_range[1]):
            if not alt_title:
                title = body.xpath('//*[@id="{}{}"]/thead/tr/th[1]'.format(table_name, i))
            rows = body.findall('.//*[@id="{}{}"]/tbody/tr'.format(table_name, i))
            for j in rows:
                d["{}_{}".format(title[0].text_content(), j[0].text_content())] = int(j[1].text_content())
    # In case there's only one table and it doesn't follow the TABLENAME# naming convention
    else:
        if not alt_title:
            title = body.xpath('//*[@id="{}"]/thead/tr/th[1]'.format(table_name))
        rows = body.findall('.//*[@id="{}"]/tbody/tr'.format(table_name))
        for j in rows:
            d["{}_{}".format(title[0].text_content(), j[0].text_content())] = int(j[1].text_content())
    return d


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

        lasso_dict["TOTAL_ERRORS"] = int(body.xpath('/html/body/div[4]/h3')[0].text_content().split(":")[1])
        # lasso_dict[""] = int(body.xpath('')[0].text_content())

        lasso_dict["DATE"] = datetime.strptime(file[-13:-5], "%Y%m%d")
        lasso_list.append(lasso_dict)
    return lasso_list
