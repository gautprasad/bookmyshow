
Open the project folder run below commands in the terminal

python3 -m venv venv
source venv/bin/activate

pip install -r requirement.txt

python manage.py migrate

python manage.py createsuperuser (optional)

python manage.py runserver

------------------------------------------------------------------------------------------------------------------
In order to get the mail please update these in the settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST_USER = 'aaaaaaaaa@gmail.com'  # Your email address
EMAIL_HOST_PASSWORD = 'aaaa aaaa aaaa aaaa'  # Your app password
DEFAULT_FROM_EMAIL = 'aaaaaaaaa@gmail.com'


for Gmail:

Enable 2-Step Verification:

Go to your Google Account: myaccount.google.com
Navigate to the "Security" tab.
Under "Signing in to Google," enable 2-Step Verification if it is not already enabled.
Generate an App Password:

After enabling 2-Step Verification, go back to the "Security" tab.
Under "Signing in to Google," you will see an option for "App passwords."
Click on "App passwords."
You may need to sign in again.
Select "Mail" as the app and "Other" as the device, then give it a name (e.g., "Django App").
Click "Generate."
You will be provided with a 16-character password. This is your EMAIL_HOST_PASSWORD. and update the above settings
------------------------------------------------------------------------------------------------------------------


import BookMyShow Django.postman_collection.json in the post man create variable