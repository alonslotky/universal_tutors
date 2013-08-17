Environment "common" is configured with Askbot.

1) In the root of this repo:

    git clone https://github.com/ASKBOT/askbot-devel.git
    cd askbot-devel
    source env/bin/activate
    python setup.py develop #allows to keep askbot in its own git repo
    #django avatar must be from askbot repo, not pypi
    pip install git+git://github.com/ericflo/django-avatar.git#egg=django_avatar

2)  Comment out 'askbot', line from the INSTALLED_APPS in
    universal_tutors/configs/common/settings.py

3)  Build the database (step 1):
    psql -U universaltutors universaltutors --host=localhost < data_dump.sql
    ./manage syncdb --all
    ./manage migrate --fake

4)  activate 'askbot', in the INSTALLED_APPS

5)  Finish the database setup:
    ./manage migrate askbot

Modify ASKBOT_URL setting to have askbot at different url root, etc.
Tested by logging in as admin and posting a question.
