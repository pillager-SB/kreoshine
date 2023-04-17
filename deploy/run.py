"""
Package for deployment
"""
import logging

from ansible import AnsibleExecutor
from deploy.deploy_const import DEVELOPMENT_MODE, PRODUCTION_MODE
from deploy.jobs.connection import echo_host
from deploy.jobs.preparatory import make_preparation, install_docker
from deploy.jobs.service_lifting import configure_nginx
from deploy.utils import create_directory
from settings import config

logger = logging.getLogger('ansible_deploy')


async def perform_deployment(deploy_mode: str, local_output_dir: str):
    """
    Deployment entry point

    Args:
        deploy_mode: mode of deployment
        local_output_dir: path to an existing local directory to be used:
                              - as ansible-runner's private data directory
    """
    create_directory(local_output_dir)

    assert deploy_mode in (PRODUCTION_MODE, DEVELOPMENT_MODE), \
        f"Only two modes of deployment is allowed: '{DEVELOPMENT_MODE}' and '{PRODUCTION_MODE}'"

    target_host = config.server.ip
    logger.info("Initiate '%s' mode of deployment on '%s' host", deploy_mode, target_host)

    ansible_executor = AnsibleExecutor(host_pattern=target_host,
                                       private_data_dir=local_output_dir,
                                       verbosity=config.ansible.verbosity)
    logger.debug("Successfully initiate instance of '%s' class", AnsibleExecutor.__name__)

    await echo_host(ansible=ansible_executor, need_gather_facts=deploy_mode == PRODUCTION_MODE)

    logger.debug("Preparing the project for deployment")
    await make_preparation(ansible=ansible_executor)

    logger.debug("Docker installation")
    await install_docker(ansible=ansible_executor)

    logger.debug("Configure Nginx as a web-server")
    await configure_nginx(ansible=ansible_executor)
