from datetime import datetime, timedelta
from signal import signal, SIGINT, SIGTERM
from sys import exit
import argparse
import random
import sys
import os
import time
from downloader import Downloader
from utils import month_to_date, month_to_str


def generate_id(lenght=6):
    base58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    return ''.join(random.choice(base58chars) for _ in range(lenght))


def log(agent, action, value=''):
    with open(HISTORIC_FILE, 'a') as f:
        f.write(f'{datetime.now().isoformat()}\t{agent}\t{action}\t{value}\n')


def generate_months(start_date, end_date):
    while start_date <= end_date:
        yield start_date
        start_date += timedelta(days=32)
        start_date = start_date.replace(day=1)


def load_state():
    with open(HISTORIC_FILE, 'r') as historic:
        state = {}
        # action init
        (timestamp, agent, action, value) = historic.readline().split('\t')
        start_date, end_date = [month_to_date(x) for x in value.strip().split(' ')]

        candidates = []
        for month in generate_months(start_date, end_date):
            candidates.append(month)

        for line in historic:
            (timestamp, agent, action, value) = line.split('\t')
            if action == 'started':
                month = month_to_date(value)
                if month in candidates:
                    candidates.remove(month)

            elif action == 'stopped':
                month = month_to_date(value)
                if month not in candidates:
                    candidates.append(month)

            elif action == 'ended':
                month = month_to_date(value)
                if month in candidates:
                    candidates.remove(month)

            elif action == 'completed':
                candidates = []
        state['candidates'] = sorted(candidates)
        return state
    print('Error al cargar el estado')
    sys.exit(1)


def process_candidates(state, id):
    if state['candidates']:
        focus_month = state['candidates'][0]
        log(id, 'started', month_to_str(focus_month))
        state['candidates'].pop(0)
    else:
        print('Descarga completa')


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--output-folder', type=str, help='output folder',
                        default=f'snapshot-{datetime.now().strftime("%Y-%m-%d")}')
    args = parser.parse_args()
    config = vars(args)
    if not os.path.exists(config['output_folder']):
        os.makedirs(config['output_folder'])

    global HISTORIC_FILE

    HISTORIC_FILE = f'{config["output_folder"]}/historic.log'
    instance_id = generate_id()

    if not os.path.exists(HISTORIC_FILE) or open(HISTORIC_FILE, 'r').read() == '':
        start_date = month_to_str(datetime(2019, 1, 1))
        end_date = month_to_str(datetime.now().replace(day=1))
        log(instance_id, 'init', f'{start_date} {end_date}')

    state = load_state()
    while state['candidates']:
        try:
            focus_month = state['candidates'][0]
            log(instance_id, 'started', month_to_str(focus_month))
            state['candidates'].pop(0)

            # Aquí se implementa la descarga de un mes
            downloader = Downloader(instance_id, focus_month, config["output_folder"])
            downloader.start()

            log(instance_id, 'ended', month_to_str(focus_month))
            state = load_state()
        except (KeyboardInterrupt, SystemExit):
            log(instance_id, 'stopped', month_to_str(focus_month))
            print('\nProgram Exiting gracefully')
            exit(0)

    print('Descarga completa')


def handle_exit(sig, frame):
    raise (SystemExit)


signal(SIGTERM, handle_exit)
signal(SIGINT, handle_exit)

if __name__ == '__main__':
    main()
