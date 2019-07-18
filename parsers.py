

# Parses the most general kind of table
def parse_basic_tables(body, d, table_name, table_range=None, alt_title=""):
    if table_range is not None:
        for i in range(table_range[0], table_range[1]):
            if not alt_title:
                title = body.xpath('//*[@id="{}{}"]/thead/tr/th[1]'.format(table_name, i))[0].text_content()
            else:
                title = alt_title
            rows = body.findall('.//*[@id="{}{}"]/tbody/tr'.format(table_name, i))
            for j in rows:
                d["{}_{}".format(title, j[0].text_content())] = int(j[1].text_content())
    # In case there's only one table and it doesn't follow the TABLENAME# naming convention
    else:
        title = alt_title
        rows = body.findall('.//*[@id="{}"]/tbody/tr'.format(table_name))
        for j in rows:
            d["{}_{}".format(title, j[0].text_content())] = int(j[1].text_content())
    return d


# This parser works on a table with format text/numeric/numeric data
def parse_mchec_req_res_table(body, d, table_name="reqRespTable", alt_title=""):
    title = alt_title
    rows = body.findall('.//*[@id="{}"]/tbody/tr'.format(table_name))
    for j in rows:
        d["{}_{}_{}".format(title, j[0].text_content(), j[1].text_content())] = int(j[2].text_content())
    return d


# This parser works on a table with format text/text/numeric data
def parse_three_col_table(body, d, table_name, alt_title=""):
    title = alt_title
    rows = body.findall('.//*[@id="{}"]/tbody/tr'.format(table_name))
    for j in rows:
        d["{}_{}_{}".format(title, j[0].text_content(), j[1].text_content())] = int(j[2].text_content())
    return d