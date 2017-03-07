#! /usr/bin/env python
# Script to remove EVERYTHING from you k8s cluster
# Useful when expirimenting with dev cluster
# Do I need to say "not for production"?
#
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-d', '--data',
                   action='store_true',
                   help='also remove data items (configs, secrets)')
argp = parser.parse_args()

sets = ['deployments', 'daemonsets', 'replicationcontrollers',
        'pods', 'services', 'ingresses']
data_sets = ['secrets', 'configmaps']

def run_cmd(predicate, type, namespace=None, name=None):
    cmd = ['kubectl', predicate, type]
    if namespace:
        if namespace == 'all' and predicate == 'get':
            cmd += ['--all-namespaces']
        else:
            cmd +=  ['-n', namespace]
    if name:
        cmd += [name]
    print  (' '.join(cmd))
    return subprocess.run(cmd, stdout = subprocess.PIPE)

def flush_set(set):
    mylist = run_cmd('get', set, 'all')
    if mylist.returncode == 0:
        stdoutstr = mylist.stdout.decode().strip()
        if len(stdoutstr) == 0:
            return
        lines = stdoutstr.split('\n')
        for line in lines:
            if line.split()[0] == 'NAMESPACE':
                continue
            namespace, name = line.split()[0:2]
            print (set, namespace)
            run_cmd('delete', set, namespace, name)
    else:
       print("failed to read kubectl")

if __name__ == "__main__":
    for set in sets:
        flush_set(set)
    if argp.data:
        for set in data_sets:
            flush_set(set)
