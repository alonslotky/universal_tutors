GETTING STARTED
_______________________________________________________________________________
To set this project up, CD into the root and execute the following:

virtualenv --no-site-packages --python /opt/local/bin/python env;
source env/bin/activate;
sudo pip install -r requirements.txt;
sh manage linkmedia;

The last command (linkmedia) will setup the various media symlinks for you :)

Now some fixtures:
sh manage loaddata social.json;


ACCESSING MANAGE.PY:
_______________________________________________________________________________
Here at Raw Jam, we make use of a specific directory structure. If you look inside iic/configs/ you will notice that we have common, staging and production folders. Common is used to define the BASE urls.py and settings.py. This then allows us to create environment specific overrides in the Staging and Production folders. To give us further flexibility, each of these environment folders has its own manage.py. As a result, we have created a helper shellscript to access the manage.py from the root project directory.

To run manage.py cd into the root folder of the project and execute: sh manage runserver (replacing runserver which whatever management command you need). If you do not want to use this method then you can simply run the manage.py file directly from within the iic/configs/common folder.

IMPORTANT: If you need to create any setting overrides (i.e. database, or email settings) then please create a local_settings.py file in the configs/common folder.