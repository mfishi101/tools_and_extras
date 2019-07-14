import os
from multiprocessing import Pool

processes = (""" put list of processes here""")
no_of_processes = len(processes)

def run_process(process):
    os.system('python {}'.format(process))

if __name__ == '__main__':

    pool = Pool(processes=no_of_processes)
    pool.map(run_process, processes)