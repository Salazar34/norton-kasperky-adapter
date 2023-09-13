# /usr/bin/python3
import csv
import json
import pandas as pd

credentials = []


def converter(metadata: dict, input: str) -> None:
    """
    Converts a JSON file into CSV

    Arguments:
    - metadata [dict]: Norton metadata automatically generated from a CSV export of the vault.
    """
    if metadata == None or metadata[0].keys().__len__() == 0:
        raise ValueError("The provided metadata has an invalid format or is null")
    if input == None or len(input) == 0:
        raise ValueError("Input file not found. Please retry")

    # Creating the CSV file with credentials
    dataframe = pd.read_csv(input, on_bad_lines="skip")
    dataframe.to_csv("./data/credentials.csv", index=None)

    with open("./data/credentials.csv", newline="") as data:
        reader = csv.DictReader(data)

        for row in reader:
            parameter = str(tuple(row.values())).removeprefix("(").removesuffix(")")

            # Avoiding empty credentials
            if len(parameter) < 4 or len(parameter) < 7:
                continue
            else:
                column = parameter.split(sep=":")

                if column[0] == "'Website name" or column[0] == "Application":
                    if len(column) == 3:
                        web_name = (
                            column[2]
                            .split("'")[0]
                            .removeprefix("//")
                            .replace("'", "")
                            .replace("\\", "")
                            .removeprefix(" ")
                        )
                    else:
                        web_name = (
                            column[1]
                            .split("'")[0]
                            .removeprefix("//")
                            .replace("'", "")
                            .replace("\\", "")
                            .removeprefix(" ")
                        )
                if column[0] == "'Website URL":
                    if len(column) == 3:
                        web_url = "https:" + column[2].split("'")[0]
                    else:
                        web_url = "https://{0}".format(
                            column[1].split("'")[0].removeprefix(" ") + " , "
                        )
                if column[0] == "'Login":
                    username = column[1].split("'")[0].removeprefix(" ")
                if column[0] == "'Password":
                    password = column[1].split("'")[0].removeprefix(" ")

                    correct_credential = {
                        "Tipo di elemento": "login",
                        "Nome utente": username,
                        "Password": password,
                        "Nome sito": web_name,
                        "URL di accesso": web_url,
                        "username": username,
                        "Note": "",
                        "Sicuro": "false",
                        "Preferito": "false",
                    }
                    credentials.append(correct_credential)

    # Writing JSON file with all credentials
    with open("./data/output.json", "w+", encoding="utf-8") as output:
        data = json.dumps(credentials)
        json.dump(data, output, ensure_ascii=False, indent=4)

    # Writing Norton metadata on a separate JSON file in order to avoid conflicts
    with open("./data/norton.json", "w+", encoding="utf-8") as output:
        data = json.dumps(metadata)
        json.dump(data, output, ensure_ascii=False, indent=4)

    with open("./data/output.json", encoding="utf-8") as output:
        items = json.load(output)
        real_data = json.loads(items)

        with open("./data/norton.json", encoding="utf-8") as norton:
            norton_items = json.load(norton)
            norton_data = json.loads(norton_items)

        # Getting headers for metadata and credentials
        headers = real_data[0].keys()
        metadata_headers = metadata[0].keys()

        with open("./data/output/output.csv", "w", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=metadata_headers)
            writer.writeheader()
            writer.writerows(norton_data)

            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(real_data)
