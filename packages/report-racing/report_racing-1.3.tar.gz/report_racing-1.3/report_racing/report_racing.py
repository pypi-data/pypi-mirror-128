import argparse
from datetime import datetime, timedelta
import pathlib
from dataclasses import dataclass


@dataclass
class Pilot(object):
    racer_name: str = None
    start_time: datetime = None
    company: str = None
    end_time: datetime = None

    @property
    def lap_time(self):

        if self.start_time and self.end_time and self.end_time >= self.start_time:
            return self.end_time - self.start_time


"""The program displays the rating of the tournament participants"""
SPLITTER = 15
DATE_TEMPLATE = '%Y-%m-%d_%H:%M:%S.%f'


def parse_files(start, end, abbreviations):
    """Function for parsing files with participant data

    Reads all files, converts text to objects and adds
    data to a dictionary"""
    pilots = {}

    for line in abbreviations:
        pilot_abbr = line[:3]
        key, name, company = line.split('_')
        pilots[pilot_abbr] = Pilot(racer_name=name, company=company.replace('\n', ''))

    get_dates(pilots, start, 'start_time')

    get_dates(pilots, end, 'end_time')

    return pilots


def get_dates(pilots, data, attr_name):

    for line in data:
        pilot_abbr = line[:3]
        date = datetime.strptime(line[3:].strip(), DATE_TEMPLATE)
        params = {attr_name: date}

        if pilot_abbr in pilots:
            setattr(pilots[pilot_abbr], attr_name, date)
        else:
            pilots[pilot_abbr] = Pilot(**params)

    return pilots


def build_report(pilots, reverse=False):
    """Sorts by lap time

    Reads a data dictionary, calculates lap times
    and sorts by lap times"""
    abbr_racer = []

    sorted_abbr = sorted(
        pilots,
        key=lambda pilot: (0, pilots[pilot].lap_time) if pilots[pilot].lap_time is not None
        else (1, 0),
        reverse=reverse
    )

    for element in sorted_abbr:
        abbr_racer.append(pilots[element])
    return abbr_racer


def print_report(abbr_racer, reversing=False):
    """Function for forming the standings

    Handles lap time errors, returns a list with the data
    of the riders in the given sequence"""
    standings = []

    if reversing:
        cut_index = len(abbr_racer) - 1 - SPLITTER
    else:
        cut_index = SPLITTER - 1

    for counter, elements in enumerate(abbr_racer):

        if elements.lap_time is not None:
            _, minutes, seconds = str(elements.lap_time).split(':')

            standings.append('{0: <20}{1: <26}{2}'.format(elements.racer_name, elements.company, f'{minutes}:{seconds.rstrip("0")}'))

        else:
            standings.append('{0: <18}{err}'.format(elements.racer_name, err="- Error"))

        if counter == cut_index:
            standings.append(f'-------------------------------------------------------')

    return '\r\n'.join(standings)


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('--files', type=pathlib.Path, required=True)
    parser.add_argument('--asc', action='store_true')
    parser.add_argument('--desc', action='store_true')
    parser.add_argument('--driver', type=str)

    return parser.parse_args()


def get_single_driver(data, driver_name):
    for key, value in data.items():
        if driver_name == value['racer_name']:
            return {key: value}


def main():
    arguments = parse_arguments()
    start = list(arguments.files.glob('start.log')).pop()
    end = list(arguments.files.glob('end.log')).pop()
    abbreviations = list(arguments.files.glob('abbreviations.txt')).pop()

    data = parse_files(start.open(), end.open(), abbreviations.open())
    if arguments.asc and arguments.desc:
        raise ValueError('Should be one argument --asc or --desc')

    reversing = arguments.desc

    if arguments.driver:
        data = get_single_driver(data, arguments.driver)

    print(print_report(build_report(data, reversing), reversing))


if __name__ == '__main__':
    main()
