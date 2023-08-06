Cleverange Auth
-----------

Cleverange Auth is a Django app to managing authenticated systems.



Quick start
-----------

1. Add "accounts" to your INSTALLED_APPS setting like this::


    INSTALLED_APPS = [

        ...
        'accounts',

    ]



2. Include the accounts URLconf in your project urls.py like this::



    ``path('accounts/', include('accounts.urls')),``



3. Include the "AUTH_USER_MODEL" and "AUTHENTICATION_BACKENDS" in your project settings.py like this::



    

    ``AUTH_USER_MODEL = 'accounts.User'``

    ``AUTHENTICATION_BACKENDS = ['accounts.backends.EmailOrUsernameBackend']``

    



4. Include the "LOGIN_REDIRECT_PATH" (to redirect user after login) in your project settings.py like this.




    ``LOGIN_REDIRECT_PATH = '/'``




5. Include the EMAIL access (to send verification mail) in your project settings.py like this.




    

    ``EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'``

    ``EMAIL_HOST = 'smtp.gmail.com'``

    ``EMAIL_USE_TLS = True``

    ``EMAIL_PORT = 587``

    ``EMAIL_HOST_USER = 'your_email_address@gmail.com'``

    ``EMAIL_HOST_PASSWORD = 'your_app_password'``


    




6. Run ``python manage.py migrate`` to create the accounts models.






7. Start the development server and visit to your endpoint.

  


    `http://127.0.0.1:8000/accounts/register/`

    `http://127.0.0.1:8000/accounts/login/`






THANK YOU FOR USING OUR APP.