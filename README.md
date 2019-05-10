This project contains the final year project source code

-------- TO ACCESS CODE -----
1. Clone the project
    git clone Final_up918154.git
    
2. Activate Virtual Environment by using the command below:
      mkvirtualenv environment
      . environment/Scripts/activate
      
3. Install dependencies
      pip install -r requirements.txt
      
4. intialize database
      python ./manage.py syncdb
      python ./manage.py migrate

5. Create superuser
      python ./manage.py createsuperuser
 6. Run Server
     python ./manage.py runserver
      
---------- END ----------
