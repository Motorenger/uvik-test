import csv
import json


def read_csv():
    '''
    Reads the CSV file and returns a list of objects in a row
    '''
    with open("data.csv", "r") as f:
        x = csv.reader(f)
        next(x)
        for row in x:
            yield row


def main():
    '''
    Main function) Goes through rows and saving data to dict and then
    converts dict to json
    '''
    res = {}

    for row in read_csv():
        if row[0] not in res.keys():
            res[row[0]] = {
                            "people": [row[1]],
                            "count": 1
                            }
        else:
            res[row[0]]["people"].append(row[1])
            res[row[0]]["count"] += 1

    j = json.dumps(res, indent=1)

    print(j)


if __name__ == "__main__":
    main()
