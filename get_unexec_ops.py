from utils import read_json_file
import sys
import re
import numpy as np


## sample run command : python get_unexec_ops.py logs/timeline_logs/timeline_rnnlm_med_0_100.ctf.json new_unexecute_ops.txt ##



def get_unexec_ops(timeline_fname, out_fname):
    timeline = read_json_file(timeline_fname)

    gpu_pids_regex = re.compile('/device:GPU:0/.*Compute')
    cpu_pids_regex = re.compile('/job:localhost/replica:0/task:0/device:CPU:0 Compute')
    gpukernel_pids_regex = re.compile('/job:localhost/replica:0/task:0/device:GPU:.* Compute')


    gpu_pids = set([])
    cpu_pids = set([])
    gpu_kernel_pids = set([])

    for event in timeline['traceEvents']:
        if event['ph'] == 'M':
            event_id = event['pid']
            if gpu_pids_regex.match(event['args']['name']):
                gpu_pids.add(event_id)
            elif gpukernel_pids_regex.match(event['args']['name']):
                gpu_kernel_pids.add(event_id)
            elif cpu_pids_regex.match(event['args']['name']):
                cpu_pids.add(event_id)



    gpu_ops = set([])
    gpu_ops_exec = set([])
    cpu_ops = set([])

    for event in timeline['traceEvents']:
        if event['ph'] == 'X' and 'args' in event.keys() and not(event['args']['op'].startswith('MEMCPY')):
            op_name = event['args']['name']
            pid = event['pid']
            ts = event['ts']
            dur = event['dur']

            if pid in gpu_kernel_pids:
                gpu_ops.add(op_name)
            elif pid in gpu_pids:
                gpu_ops_exec.add(op_name)
            elif pid in cpu_pids:
                cpu_ops.add(op_name)

    unexecuted_ops = set([])

    for op_name in gpu_ops:
        if op_name not in gpu_ops_exec:
            unexecuted_ops.add(op_name)

    print('number of gpu ops : ', len(gpu_ops))
    print('number of cpu ops : ', len(cpu_ops))
    print('number of unexecuted ops : ', len(unexecuted_ops))

    with open(out_fname, 'w') as f:
        for op_name in unexecuted_ops:
            f.write('%s\n' % (op_name))


def main():
    timeline_fname = sys.argv[1]
    out_fname = sys.argv[2]
    get_unexec_ops(timeline_fname, out_fname)



if __name__ == '__main__':
    main()


