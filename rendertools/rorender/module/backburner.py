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

log_root = os.path.join(os.getcwd(), 'backburner.log')
machine_status = dict()
job_status = dict()


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
                    
                    if job in job_status:
                        job_status[job].append(machine)
                    else:
                        job_status.setdefault(job, [])
                        job_status[job].append(machine)
                    
                    return (machine, 'rendering', job)

                # if jobs finished
                if message.endswith('Complete'):
                    job = message.split("'")[1]
                    if job in job_status:
                        del job_status[job]

            if date_time_obj and debug_level == 'ERR':
                # job was cancelled? failed?
                if '(#$$??$$##)' in message:
                    machine = message.split(' ')[-1]
                    job = message.split(' ')[1]

                    if job in job_status:
                        if machine in job_status[job]:
                            job_status[job].remove(machine)


            if date_time_obj and debug_level == 'DBG':
                # job was deleted
                if message.endswith('deleted'):
                    job = message.split("'")[1]


        except Exception as e:
            # print(f'found an error: {e}')
            pass

        return False


with open(log_root, encoding="utf-16") as fp:
    line = fp.readline()
    while line:
        result = check_log_line(line)

        if result:
            machine_status[result[0]] = [result[1], result[2]]

        line = fp.readline()


print(job_status)