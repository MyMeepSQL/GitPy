import configparser
import os
from src.config import Configuration

def save_notification_settings(
    github_repo_name,
    github_repo_owner,
    github_repo_branch,
    github_repo_url,
    github_repo_api_url,

    receiver_email_address,
    
    smtp_server,
    smtp_port,
    smtp_security,
    smtp_sender_email_address,

    email_subject,
    email_message
    ):

    GITPY_PATH = os.environ[Configuration.gitpy_path_env_var_name]
    INSTALL_PATH = GITPY_PATH

    # Create the configparser object
    config_file = '%s/config/new_version_notification.conf' % INSTALL_PATH
    config = configparser.ConfigParser()
    config.read(config_file)

    # Add the sections
    config.add_section(section=github_repo_name)

    # Add the options
    config.set(github_repo_name, 'github_repo_name', github_repo_name)
    config.set(github_repo_name, 'github_repo_owner', github_repo_owner)
    config.set(github_repo_name, 'github_repo_branch', github_repo_branch)
    config.set(github_repo_name, 'github_repo_url', github_repo_url)
    config.set(github_repo_name, 'github_repo_api_url', github_repo_api_url)

    config.set(github_repo_name, 'receiver_email_address', receiver_email_address)

    config.set(github_repo_name, 'smtp_server', smtp_server)
    config.set(github_repo_name, 'smtp_port', smtp_port)
    config.set(github_repo_name, 'smtp_security', smtp_security)
    config.set(github_repo_name, 'smtp_sender_email_address', smtp_sender_email_address)

    config.set(github_repo_name, 'email_subject', email_subject)
    config.set(github_repo_name, 'email_message', email_message)

    # Write the updated configuration back to the file
    with open(config_file, 'w') as configfile:
        config.write(configfile)

# An small exemple of how to use the configparser module
# to read and write in a .conf file.

# config_file = 'new_version_notification.conf'
# config = configparser.ConfigParser()
# config.read(config_file)

# # config.add_section(section='test')
# config.remove_section(section='test')

# # Write the updated configuration back to the file
# with open(config_file, 'w') as configfile:
#     config.write(configfile)

# # Value variables (of the 'convpro.conf' file)
# rootperm = config.get('general', 'rootperm')
# reset = config.get('console', 'reset')

# # Get the console section
# console_info = config['console']
# # Write the loaded module into 'convpro.conf' file
# console_info['module_selected'] = 'VALUE'

save_notification_settings(
    github_repo_name='test',
    github_repo_owner='test',
    github_repo_branch='test',
    github_repo_url='test',
    github_repo_api_url='test',

    receiver_email_address='test',

    smtp_server='test',
    smtp_port='test',
    smtp_security='test',
    smtp_sender_email_address='test',

    email_subject='test',
    email_message='test'
    )