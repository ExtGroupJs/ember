# EMBER
[![built with Codeium](https://codeium.com/badges/main)](https://codeium.com)
# STEPS FOR CLONING 
```
cd existing_folder
git remote add origin https://github.com/ExtGroupJs/ember.git
git branch -M main
git push -uf origin main
```

# STEPS FOR DEVELOPING
1.  when the code is already cloned, create a python virtual enviroment (currently using python 3.11):
python -m venv venv

2. Activate virtual enviroment:
source /venv/bin/activate # for linux
source /venv/Scripts/activate # for windows (there's other ways too)

3. Install required packages running in the console:
pip install -r requirements.txt

4. Run migrations (with this we have created a superuser):
python manage.py migrate

5. Create some dummy user objects (300):
python manage.py create_test_users

5. run server:
python manage.py runserver

6. interact with API, available on:
http://127.0.0.1:8000/api/swagger/

