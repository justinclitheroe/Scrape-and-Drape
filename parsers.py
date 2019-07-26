"""
The parsers responsible for getting data from the html

Frustratingly similar for what they do, lots of them are one offs because
the reports don't follow any kind of uniform layout and frequently don't follow
best practices for html and are fairly annoying to parse in a sane manner

typically the parsers are fairly simple
    Get rows
    populate data in dict through those rows
The data just happens to manifest itself in different ways
"""


# Parses the most general kind of table, format: text/numeric data
# It also can do multiple similarly titled ones in a row,
# though that was only useful in lasso so far
def parse_basic_tables(body, d, table_name, table_range=None, alt_title=""):
    if table_range is not None:
        for i in range(table_range[0], table_range[1]):
            if not alt_title:
                test = f"{table_name}{i}"
                title = body.xpath(f'//*[@id="{table_name}{i}"]/thead/tr/th[1]')[0].text_content()
            else:
                title = alt_title
            rows = body.findall(f'.//*[@id="{table_name}{i}"]/tbody/tr')
            for j in rows:
                d[f"{title}_{j[0].text_content()}"] = int(j[1].text_content())
    # In case there's only one table and it doesn't follow the TABLENAME# naming convention
    else:
        title = alt_title
        rows = body.findall(f'.//*[@id="{table_name}"]/tbody/tr')
        for j in rows:
            d[f"{title}_{j[0].text_content()}"] = int(j[1].text_content())
    return d


def parse_imsws_error_tables(body, d):
    for i in range(0, 9):
        table_name = f"errorTable{i}"
        title = body.xpath(f'//*[@id="{table_name}"]/thead/tr/th[1]')[0].text_content()
        rows = body.findall(f'.//*[@id="{table_name}"]/tbody/tr')
        for j in rows:
            d[f"IMSWSErrors_{title}_{j[0].text_content()}"] = int(j[1].text_content())
        return d


def parse_mchec_component_table(body, d, title):
    """
    This parser will not work unless mchec files are cleaned using the mchec cleaner in "fixers"
    """
    rows = body.findall('.//table[2]/tbody/tr')
    component_name = ""
    for j in rows:
        if j[0].text_content():
            component_name = j[0].text_content()
        d[f"{title}{component_name}_COUNT_{j[1].text_content()}"] = int(j[2].text_content())
        d[f"{title}{component_name}_RES(ms)_{j[1].text_content()}"] = float(j[3].text_content())
    return d


# This parser works on a table with format text/text/numeric data
def parse_three_col_table(body, d, title, table_name):
    rows = body.findall(f'.//*[@id="{table_name}"]/tbody/tr')
    for j in rows:
        d[f"{title}_{j[0].text_content()}"] = int(j[2].text_content())
    return d


def parse_scomp_login_stats(body, d, title, table_name):
    rows = body.findall(f'.//*[@id="{table_name}"]/tbody/tr')
    for j in rows:
        d[f"{title}_{j[0].text_content()}_{j[1].text_content()}_Successful"] = int(j[2].text_content())
        d[f"{title}_{j[0].text_content()}_{j[1].text_content()}_Failed"] = float(j[3].text_content())
    return d


def parse_three_col_two_data_table(body, d, title, table_name,
                                   col_names=["", ""]):
    if col_names[0] == "" or col_names[1] == "":
        raise ValueError("No Column names given")
    rows = body.findall(f'.//*[@id="{table_name}"]/tbody/tr')
    for j in rows:
        d[f"{title}_{j[0].text_content()}_{col_names[0]}"] = int(j[1].text_content())
        d[f"{title}_{j[0].text_content()}_{col_names[1]}"] = float(j[2].text_content())
    return d
