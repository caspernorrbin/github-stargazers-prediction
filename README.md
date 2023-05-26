
# Predicting Stargazers

This project explores predicting the number of stargazers of popular GitHub repositories using different machine learning models.

## Architecture
The architecture consists of one production server and one development server. It is possible to connect additional worker nodes to the development server. The model used for model serving on the production server is pushed from the development server using git hooks.

## Orchestration
This project uses a combination of Cloud-init, Docker, and Ansible to orchestrate the various machines. Cloud-init starts the different nodes, and is used for the worker nodes. Ansible is used to contextualize both the production and development server. Docker is used on the production server to containerize the various parts of the application.

## Running instructions
The various orchestration and contextualization files can be found in `model_serving/openstack-client/single_node_with_docker_ansible_client`. Use Cloud-init to create the machines, then use Ansible to contextualize them. Docker will be configured and run automatically on the production server.

A CSV is already in provided, but the generate a new one with different parameters, use the files in `github/`, this requires a GitHub token to be generated

To start model training and evaluation, run `model_serving/ci_cd/development_server/eval_models.py`. The best model will be saved in the same directory.

To deploy this model to the production server, create a git repository and a git hook. Push the model to repository for it to be automatically downloaded on the production server. It is also possible to transfer the model manually or using other methods.

The predictions on the front-end can be accessed on port `5100`, the predictions can be reached in `IP/predictions`

## Authors
Rabia Bashir
Sebastian Mikkelsen Toth
Casper Norrbin
Magnus Olander
