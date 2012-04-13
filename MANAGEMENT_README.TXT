GIT REPO INIT:
mkdir iic;
cd iic;
git init;
git remote add origin ssh://sls@slsapp.com:1234/rawjam/iic.git;
git config remote.origin.push refs/heads/master:refs/heads/master;

PROJECT INIT:
virtualenv --no-site-packages env;
source env/bin/activate;
sudo pip install -r requirements.txt;
mv HIDE.gitignore .gitignore;

COMMIT TO GIT:
git add .;
git commit -am 'initial commit';
git push origin master;

Create test data:
sh manage mockups company.faqitem:20 company.newsitem:20 company.testimonial:20 company.service:20 company.project:20 company.projectimage:20 company.teammember:20;

Generate graphvis
sh manage graph_models company iic -g -o docs/iic_erd.png;
sh manage graph_models -a -g -o docs/everything_erd.png;

APPLYING PATCHES
cd env/lib/python2.6/site-packages/django;
patch --dry-run -p1 < ~/downloads/somefix.patch;