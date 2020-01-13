"""
python script for parsing Autodesk Backburner log files
"""

# backburners logs much be set to verbose

import os
import datetime

# log location
# read in log
# parse for needed information (render started, render finished/errored)
# update data base


machine_status = dict()
JOB_STATUS = dict()


def check_log_line(line):
    if line[0] != '':
        date = line[:10]
        time = line[11:19]
        debug_level = line[20:23]
        message = line[23:].strip()
        
        try:
            date_time_obj = datetime.datetime.strptime(date + ' ' + time, '%Y/%m/%d %H:%M:%S')

            if date_time_obj and debug_level == 'INF':
                # if machine is recieving job
                if message.startswith('Sending instructions for job'):
                    job = message.split("'")[1]
                    machine = message.split(' ')[-1]
                    
                    if job in JOB_STATUS:
                        JOB_STATUS[job].append(machine)
                    else:
                        JOB_STATUS.setdefault(job, [])
                        JOB_STATUS[job].append(machine)
                    
                    return (machine, 'rendering', job)

                # if jobs finished
                if message.endswith('Complete'):
                    job = message.split("'")[1]
                    if job in JOB_STATUS:
                        del JOB_STATUS[job]

            if date_time_obj and debug_level == 'ERR':
                # job was cancelled? failed?
                if '(#$$??$$##)' in message:
                    machine = message.split(' ')[-1]
                    job = message.split(' ')[1]

                    if job in JOB_STATUS:
                        if machine in JOB_STATUS[job]:
                            JOB_STATUS[job].remove(machine)


            if date_time_obj and debug_level == 'DBG':
                # job was deleted
                if message.endswith('deleted'):
                    job = message.split("'")[1]


        except Exception as e:
            # print(f'found an error: {e}')
            pass

        return False


def parse_backburner():
    # TODO: this is wank, fix.
    try:
        log_root = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'backburner', 'backburner.log')

        with open(log_root, encoding="utf-16") as fp:
            line = fp.readline()
        while line:
            result = check_log_line(line)
            line = fp.readline()

        return JOB_STATUS


    except Exception as e:
        print('USING DEV BACKBURNER LOGS')
        log_root = os.path.join(os.getcwd(), 'rorender', 'module', 'backburner.log')
        print(e)

        with open(log_root, encoding="utf-16") as fp:
            line = fp.readline()
        while line:
            result = check_log_line(line)
            line = fp.readline()

        return JOB_STATUS

    
