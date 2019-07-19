"""
The parsers responsible for getting data from the html

Frustratingly similar for what they do, lots of them are likely one offs because
the reports don't follow any kind of uniform layout

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
def parse_mchec_req_res_table(body, d, title, table_name):
    rows = body.findall('.//*[@id="{}"]/tbody/tr'.format(table_name))
    for j in rows:
        d["{}_REQ_{}".format(title, j[0].text_content())] = int(j[1].text_content())
        d["{}_RES(ms)_{}".format(title, j[0].text_content())] = float(j[2].text_content())
    return d


def parse_mchec_component_table(body, d, title):
    """
    Okay here we go this parser is bonkers enough to get its own block documentation

    because of what was likely an imperceptible error when writing on the log generation side of things,
    after about 3 hours of reading tool documentation, I've realized that the problem is that there aren't any
    </tr> closing tags, The solution would to lookahead, but the way that the library works is that it actually
    ends the list at the closing tag, so they're pretty much unreachable

    the likely solution is to write something to clean the files, which I was already probably gonna do to cut the
    file sizes down
    """
    rows = body.findall('.//table[2]/tbody/tr')
    component_name = ""
    for j in rows:
        index = 0
        more = True
        if j[0].text_content():
            component_name = j[0].text_content()
            print("new component detected changing to", component_name)
        while more:
            try:
                print(j[(index * 4) + 0].text_content(), j[(index * 4) + 1].text_content(),
                      j[(index * 4) + 2].text_content(), j[(index * 4) + 3].text_content())
                index += 1
            except:
                more = False

            # d["{}_{}{}REQ".format(title, j[0].text_content(), j[1].text_content())] = int(j[2].text_content())
            # d["{}_{}{}REQ".format(title, j[0].text_content(), j[1].text_content())] = float(j[3].text_content())
    return d


# This parser works on a table with format text/text/numeric data
def parse_three_col_table(body, d, title, table_name):
    rows = body.findall('.//*[@id="{}"]/tbody/tr'.format(table_name))
    for j in rows:
        d["{}_{}".format(title, j[0].text_content())] = int(j[2].text_content())
    return d
