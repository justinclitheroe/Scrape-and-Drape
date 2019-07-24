"""
These functions serve as fixes for any issue that might pop up, typically only run once on a file
"""


import os
import re
import lxml.html as html
from lxml.html.clean import Cleaner
import utils


def fix_mchec_error_tables(body):
    """
    If you've already read through the rest of the code you know that there's a fairly debilitating issue in the mchec logs

    In brief, the Error tables are not actually formatted correctly
    Instead of <tr> <td> DATA </td> </tr>
    we have         <td> DATA </td> </tr>

    This isn't the fault of the person who wrote the log generator as modern browsers
    will actually fix tables made like this following the first row and it's pretty much impossible
    to notice the bug when it still looks normal in your browser

    This script will go in, fix the tables, then mark the file as fixed in the header
    """
    body_string = html.tostring(body).decode()
    top = re.compile(r"(<td></td>)")
    bottom = re.compile(r"(<td>\d+\.\d+</td>)(\n.*<tr>)")

    body_string = re.sub(top, r"<tr>\n\1", body_string)
    body_string = re.sub(bottom, r"\1\n</tr>\2", body_string)

    body = html.fromstring(body_string)
    return body


def remove_scripts_and_style(body):
    """
    All of the Html files have fairly large blocks dedicated to style and script

    This function cleans out the large useless blocks out of the files and typically drops the size down significantly
    """
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.style = True
    cleaner.page_structure = False
    return cleaner.clean_html(body)


def check_and_fix_unformatted_logs(apps):
    for app in apps:
        try:
            os.mkdir(os.path.join("logs", "formatted_logs", app))
        except FileExistsError:
            print("folder Exists skipping")

        files = utils.get_files_list(app, formatted=False)
        for file in files:
            with open(file, "r") as f:
                body = f.read()
            body = html.fromstring(body)
            body = remove_scripts_and_style(body)
            if app == "mchec":
                body = fix_mchec_error_tables(body)
            new_file_name = os.path.join(os.getcwd(), "logs", "formatted_logs", app, file.split('\\')[-1])
            with open(new_file_name, "w+") as f:
                f.write(html.tostring(body, pretty_print=True).decode())
    return
