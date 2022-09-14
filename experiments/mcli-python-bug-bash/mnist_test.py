# Copyright 2022 MosaicML Composer authors
# SPDX-License-Identifier: Apache-2.0

from mcli.api.kube.runs import *

platform = 'r1z2'

import requests
import yaml

# Download the MNIST YAML from Composer
req = requests.get(
    'https://raw.githubusercontent.com/mosaicml/composer/v0.9.0/composer/yamls/models/classify_mnist.yaml')

print(f'Downloaded Composer\'s MNIST configuration:\n\n{req.text}')

# Load the YAML into a parameters dictionary
parameters = yaml.safe_load(req.text)

# Define our command
command = """
wget -O entrypoint.py https://raw.githubusercontent.com/mosaicml/composer/v0.9.0/examples/run_composer_trainer.py

composer entrypoint.py -f /mnt/config/parameters.yaml
"""

config = RunConfig(name='mnist-classification',
                   image='mosaicml/composer:0.9.0',
                   gpu_num=1,
                   platform=platform,
                   command=command,
                   parameters=parameters)

# Create the run from a config
run = create_run(config)
print(f'Launching run {run.name}')

# Wait for the run to start "running"
run = wait_for_run_status(run, status='running')
print(f'Run named {run.name} has status {run.status}')

run = get_runs([run])[0]
# The run's status is stored in the `.status` attribute
print(f'Run named {run.name} has status {run.status}')

# The `config` you defined above + any filled in details are stored in the `.config` attribute
print(str(run.config))

# Follow the logs as the run progresses
for line in follow_run_logs(run):
    print(line)

# Wait until run.status reaches "completed"
run = wait_for_run_status(run, status='completed')
print(f'Run named {run.name} has completed with status {run.status}')
