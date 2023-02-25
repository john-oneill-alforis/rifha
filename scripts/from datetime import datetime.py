from datetime import datetime

date_time_str = "Tue, 21 Feb 2023 14:14:40 -0500"
date_time_str = date_time_str[:-15]


date = datetime.strptime(date_time_str, "%a, %d %b %Y")


print("The date is", date_time_str.date())
