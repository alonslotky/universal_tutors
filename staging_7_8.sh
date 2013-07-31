cd sites/universal_tutors/
source env/bin/activate
cd repository/
git add .
git commit -m "pushing from staging"
git push origin stable
git pull origin signup
git fetch origin signup
pip uninstall django
pip install django==1.4
cd /home/rawjam/sites/universal_tutors/env/lib/python2.7/site-packages
git clone git://github.com/django-mptt/django-mptt.git django-mptt