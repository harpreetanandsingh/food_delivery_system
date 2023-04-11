# Food Delivery Management System
This repository contains the project of Database Systems(CS F212) Course at BITS-Pilani,Pilani Campus.The contributors of the project are:
1) Harpreet Singh Anand (2021A7PS2416P)
2) Yash Pandey (2021A7PS0661P)

Instructions to install:
1) Download the whole folder as a zip file
2) Extract the folder into any folder of your choice
3) Now open the folder in a code editor like VS Code and create a new terminal
4) Using the terminal commands, navigate inside the food_delivery_project folder
5) Now you have to create a virtual environment in the terminal. 

    For Windows Users:https://medium.com/co-learning-lounge/create-virtual-environment-python-windows-2021-d947c3a3ca78
    
    For Mac Users: https://programwithus.com/learn/python/pip-virtualenv-mac
    
6) Now execute the command "pip install -r requirements.txt" inside the virtual environment.
7) After all the packages are downloaded, run the command "python manage.py makemigrations" and "python manage.py migrate" one after the other.
8) If you want to add the database using sql queries, run the scipt.sql file in MySQL workbench.
9) In the settings.py file, navigate to the DATABASES part which would look something like this,
          
      <img width="362" alt="Screenshot 2023-04-11 at 9 32 55 PM" src="https://user-images.githubusercontent.com/92373075/231221945-334a4d64-91e8-4ee2-bf94-0d9a2cfbec5f.png">

 Now change the password to your_password(here  your_password denotes the password of your MySQL root user)
 
 10) Now run the server using "python manage.py runserver" 

 11) You can now open any browser(Chrome is preferred) and go to "localhost:8000" to check the working of the frontend interface and its backend implementation.To see the SQL queries executed in the backend, go to food_delivery_app/views.py. Here you can see all the SQL queries executed in the application.
 
 12) To shut-down the server, just type (control+c)

# Frontend Documentation

1)The HomePage <br/><br/>
<img width="840" alt="Screenshot 2023-04-11 at 9 48 14 PM" src="https://user-images.githubusercontent.com/92373075/231225807-9fb2137c-bbd1-4eb5-bc09-646ada82c645.png"><br/><br/>
The homepage show four options to register as a customer,manager or a delivery personnel. If you are already registered, you can login.

2)Customer Registration<br/><br/>
<img width="765" alt="Screenshot 2023-04-11 at 9 52 21 PM" src="https://user-images.githubusercontent.com/92373075/231226786-d13dd9de-f746-4379-be5d-acd06ccd3c81.png"><br/><br/>
Enter your details and click the button to register yourself as a customer

3)Login Page<br/><br/>
<img width="1144" alt="Screenshot 2023-04-11 at 10 03 08 PM" src="https://user-images.githubusercontent.com/92373075/231229290-0cda3488-8315-4ffa-a6f0-c3465095b0fc.png">

4)Customer Home Page<br/><br/>
<img width="949" alt="Screenshot 2023-04-11 at 10 05 27 PM" src="https://user-images.githubusercontent.com/92373075/231229859-5a16cd06-11a3-4b3f-810f-0363c62702d5.png">

5)My Orders<br/><br/>
<img width="491" alt="Screenshot 2023-04-11 at 10 09 21 PM" src="https://user-images.githubusercontent.com/92373075/231230691-73eed117-f603-4763-8e1f-b9e4360248e4.png">


