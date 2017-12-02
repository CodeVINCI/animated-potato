# animated-potato
Localhost instllation

Prior to setting up the project download latest postgreSQL version and create a new database such as "website". 

Step1:Create a new directory such as ~/Desktop/project
Step2:fork the repo https://github.com/CodeVINCI/animated-potato
Step3:cd to ~/Desktop/project
Step4:run git clone https://github.com/<Your_github_username>/animated-potato
Step5:create a virtual enviroment with python 2.7 with the command- "virtualenv socrates"
Step6:run source socrates/bin/activate, this will activate the virtual enviroment
Step7:cd to animated-potato
Step8:run pip install -r requirements.txt
Step9:cd website
Step10:sudo nano +80 settings.py
Step11:the position of cursor must show Database block nearby there change the name of the database to Ex:"website" change the user and it password accordingly
Step:12:cd ../ you should reach the animated-potato folder now
Step13:run python manage.py runserver
Step14:Open your browser at localhost:8000 and you have a socrates instance working at your local machine.
