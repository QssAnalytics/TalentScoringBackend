from datetime import datetime


def get_date_weight(finnly_date):
        if 0 <= finnly_date < 1:
                finnly_date_weight = 0.9
        elif 1 <= finnly_date < 3:
                finnly_date_weight = 0.7
        elif 3 <= finnly_date < 5:
                finnly_date_weight = 0.5
        elif 5 <= finnly_date <10:
                finnly_date_weight = 0.3
        elif 10 <= finnly_date <20:
                finnly_date_weight = 0.1
        elif 20 <= finnly_date:
                finnly_date_weight = 0.01

        return finnly_date_weight

def calculate_date_difference(data):
        if data["endDate"] == "":
            current_date = datetime.now()
            start_date = datetime.strptime(data["startDate"], "%Y-%m-%d")
            difference = current_date - start_date
        else:
            start_date = datetime.strptime(data["startDate"], "%Y-%m-%d")
            end_date = datetime.strptime(data["endDate"], "%Y-%m-%d")
            difference = end_date - start_date
        return difference
