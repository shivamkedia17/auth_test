Simple django-project to demonstrate integration of drive api functionality.

Client Id and Client Secret have been added to the database using the admin app.

In case there is a refresh token error, kindly logout and login again.
The URL to logout is: /accounts/logout.
You shall be redirected to the login page automatically when trying to use the app.

Steps to use (after login):

1. See all the files currently in your google drive using the list button. File IDs are shown in the response.
2. Create file: A file with the current timestamp is created first in the `static/` directory, which is then uploaded to your `My Drive` via the API. This can be confirmed by visiting your google drive page.
3. The same (or any other) file on _your_ google drive can be downloaded via the Download file option. Files are downloaded in the `download` directory of this app (via the python backend, not the browser). Browser based downloads have certain limitations which we shall discuss.
4. Similarly, files can be deleted by supplying the file ID.
