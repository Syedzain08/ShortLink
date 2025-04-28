# ====================
# IMPORTS
# ====================

from pandas import read_csv, to_datetime
from datetime import datetime, timedelta
from pyperclip import copy
from pyautogui import hotkey, click
from time import sleep

# ===================
# CONFIGURATION
# ===================


CSV_PATH = "jobs.csv"  # Download the CSV
DAYS_BACK = 7  # Number of days to look back for job postings

# The template for the email response

TEMPLATE = """Hi {{firstName}},

Thank you so much for your interest. Here is a link to the job description for your convenience: {link}

If you have any questions regarding this position, feel free to contact me.

Best Wishes,
[Your Name]
"""


# ===================
# MAIN FUNCTION
# ===================


def main():
    # Read the job title and advertiser name from the output file
    # This file is created by the Flask app when it receives the HTML

    with open("output.txt", "r") as file:
        JOB_TITLE = file.readline().strip()
        ADVERTISER_NAME = file.readline().strip()

    cuttoff_date = datetime.now() - timedelta(days=DAYS_BACK)

    df = read_csv("jobs.csv")

    # Convert the "Date" column to datetime format
    df["Date"] = to_datetime(df["Date"], errors="coerce")

    # Filter the DataFrame based on the date, advertiser name, and job title
    # Ensure that the date does not exceed the cutoff date
    filtered_df = df[
        (df["Date"] >= cuttoff_date)
        & (df["Advertiser Name"] == ADVERTISER_NAME)
        & (df["Position"] == JOB_TITLE)
    ]

    if filtered_df.empty:
        # If there are no results
        copy("No matching job found.")
        sleep(0.2)
        click()
        hotkey("ctrl", "v")
        sleep(0.3)
        return False

    elif len(filtered_df) > 1:
        # If there are multiple results
        copy("Multiple results found. Quitting.")
        sleep(0.2)
        click()
        hotkey("ctrl", "v")
        sleep(0.3)
        return True

    else:
        # If there is exactly one result
        link = filtered_df["Job Listing Link"].iloc[0]

        Pasteable_template = TEMPLATE.format(link=link)

        copy(Pasteable_template)
        sleep(0.5)
        click()
        hotkey("ctrl", "v")
        sleep(0.3)
        return Pasteable_template


# ===================
# RUNNING THE SCRIPT
# ===================

if __name__ == "__main__":
    main()
