import os
from distutils.dir_util import copy_tree
from pathlib import Path

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'

## jupyterhub auth settings
admin_users = os.environ['ADMIN_USERS']
print("Admin Users", admin_users)
admin_users_set = set(filter(len, map(str.strip, admin_users.split(','))))
print("Admin Users Set", admin_users_set)

oauthstr = os.environ.get('OAUTH_CALLBACK_URL')

if (oauthstr is not None) and (len(oauthstr)>0):
    c.JupyterHub.authenticator_class = "oauthenticator.LocalGitHubOAuthenticator"
    c.LocalGitHubOAuthenticator.create_system_users = True
    c.LocalGitHubOAuthenticator.allowed_users = admin_users_set
    c.Authenticator.admin_users = admin_users_set
else:
    c.Authenticator.admin_users = admin_users_set
    c.JupyterHub.admin_access = True
    c.LocalAuthenticator.create_system_users = True
    c.LocalGitHubOAuthenticator.allowed_users = admin_users_set


## mount a data location to persist login and user data
data_dir = os.environ['JUPYTERHUB_CONTAINER_DATA_DIR']
c.JupyterHub.cookie_secret_file = os.path.join(data_dir, 'jupyterhub_cookie_secret')

## remove proxy file as it gives error if it exists on container restart
#proxy_pid_file = "/var/run/jupyterhub-proxy.pid"
#if os.path.exists(proxy_pid_file):
#    print("Cleaning up proxy pid file")
#    os.remove(proxy_pid_file)
#c.ConfigurableHTTPProxy.pid_file = proxy_pid_file


def populate_user_home(spawner):
    username = spawner.user.name
    # we expect to see creates users in /home
    volume_path = os.path.join('/home', username)
    flag_file = os.path.join(volume_path, '.iotics.notebook.flag')

    # if not os.path.exists(volume_path):
    #     os.mkdir(volume_path, 0o777)

    if not os.path.isfile(flag_file):
        copy_tree("/tmp/src", os.path.join(volume_path,'examples'))
        Path(flag_file).touch()

c.Spawner.pre_spawn_hook = populate_user_home
