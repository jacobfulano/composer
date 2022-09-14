# Copyright 2022 MosaicML Composer authors
# SPDX-License-Identifier: Apache-2.0

from mcli.api.kube.runs import *

platform = 'r7z2'

config = RunConfig(name='hello-world',
                   image='bash',
                   command='echo "Hello World!" && sleep 60',
                   gpu_type='none',
                   platform=platform)

# Create the run from a config
run = create_run(config)
print(f'Launching run {run.name}')

# Wait for the run to start "running"
run = wait_for_run_status(run, status='running')
print(f'Run named {run.name} has status {run.status}')

# Print the first line of logs
for line in follow_run_logs(run):
    print(f'First log line was: {line}')
    break

# Stop the run - can be called with a list of runs to stop
run = stop_runs([run])[0]
print(f'Run named {run.name} has status {run.status.value}')
