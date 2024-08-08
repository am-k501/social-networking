Using this commond create a Project
    "django-admin startproject social_network"
After that go to the inside the project path create Virtual use this commond
    "python3 -m venv social_networking"
Once created the Virtual activate it. After that run the project getting some dependency error instal this
    "pip install django"
After Makemigrations and Migrate it.
    "python manage.py makemigrations"
    "python manage.py migrate"
After that run the project use this commond
    "python manage.py runserver"
Createsuperuser because by default i dont have users, use this commond
    "python manage.py createsuperuser"
    After that it will ask enter username,email,password,password after submitting this one you will get sucess msg in terminal like "Superuser created successfully."
Requriement file need to see in the project use this commond
    "pip freeze >> requriement.txt" 
For creating the new app use this commond
    "python manage.py startapp users"
    
Dependency to be install use this commonds
    "pip install djangorestframework"

For search functionlity use this type url after ?q= key any word it will search
    "http://127.0.0.1:8001/users/search/?q=am"
    

    
    