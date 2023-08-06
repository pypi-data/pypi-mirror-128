import argparse
import json
import traceback
import pyfiglet
from pathlib import Path


def get_capital(country):
    try:
        file_path = "/".join(str(Path(__file__).absolute()).split("/")[:-1]) + "/resources/capital.json"
        data = json.load(open(file_path, ))
        available_countries = list(data.keys())
        if country.lower() not in available_countries:
            print("Country name might be invalid or not available in our dataset!")
            return
        art = pyfiglet.figlet_format(data[country.lower()])
        print(art)
    except Exception as e:
        print(traceback.format_exc())
        raise e


def load_arguments():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--country", action="store", dest="country", default="")
        args = parser.parse_args()

        if args.country == '':
            raise Exception("Please provide counrty parameter. \ne.g. --country India")
        return args
    except Exception as e:
        print("Please provide counrty parameter. \ne.g. --country India")
        raise Exception("Invalid input!")


def main():
    try:
        args = load_arguments()
        get_capital(args.country)
    except Exception as e:
        print(traceback.format_exc())
        raise e


if __name__ == '__main__':
    main()
