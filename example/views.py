
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from allauth.socialaccount.models import SocialToken
from .forms import FileForm

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_httplib2 import httplib2
from googleapiclient.errors import HttpError

import io
import os
import pdb
from datetime import datetime

def success(request):
    return render(request=request, template_name='success.html')

'''
# TODO
1. Get access and refresh tokens from DB
2. Pass tokens as params and create service api object
3. use methods on object to create a blank file in drive
4. check if blank file is created
5. execute the above from a button
'''

# 1.
@login_required
def list_files(request):
    tokens = SocialToken.objects.get(account__user=request.user, account__provider='google')
    auth_token, refresh_token = tokens.token, tokens.token_secret
    creds = Credentials(
        token=auth_token,
        scopes='https://www.googleapis.com/auth/drive',
    )

    try:
        httplib2.debuglevel = 4
        service = build("drive", "v3", credentials=creds)

        results = service.files().list(pageSize=10).execute()
        print(results)

        items = results.get("files", [])

        if not items:
            print("No files found.")
            return HttpResponse(content="not hehe")

        return HttpResponse(content=f"{items}")

    except HttpError as error:
        print(f"An error occurred: {error}")
        return HttpResponse(content="def not hehe")


@login_required
def create_file(request):
    tokens = SocialToken.objects.get(account__user=request.user, account__provider='google')
    auth_token, refresh_token = tokens.token, tokens.token_secret
    creds = Credentials(
        token=auth_token,
        scopes='https://www.googleapis.com/auth/drive',
    )

    try:
        httplib2.debuglevel = 4
        service = build("drive", "v3", credentials=creds)

        # Get the uploaded file
        # file = request.FILES['file']
        # file_path = os.path.join('/tmp', file.name)

        # Save the file temporarily
        # with open(file_path, 'wb+') as destination:
        #     for chunk in file.chunks():
        #         destination.write(chunk)

        filename = f"{datetime.now()}_File.txt"
        mime_type = "text/plain"
        file_metadata = {
            'name': filename,
            'mimeType': mime_type
        }

        filepath = "static/"+filename
        with open(filepath, 'w') as f:
            f.write(f"File created at {datetime.now()}")

        media = MediaFileUpload(filename=filepath, mimetype=mime_type)

        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print(f'File ID: {file.get("id")}')

        return HttpResponse(content="File ID: "+file.get('id')+"(Copy for reuse)")

    except HttpError as error:
        print(f"An error occurred: {error}")
        return HttpResponse(content="def not hehe")

@login_required
def download_file(request):
    tokens = SocialToken.objects.get(account__user=request.user, account__provider='google')
    auth_token, refresh_token = tokens.token, tokens.token_secret
    creds = Credentials(
        token=auth_token,
        scopes='https://www.googleapis.com/auth/drive',
    )

    try:
        if request.method == 'POST':
            form = FileForm(request.POST)

            if form.is_valid():
                httplib2.debuglevel = 4
                service = build("drive", "v3", credentials=creds)

                file_id = form.cleaned_data['file_id']

                # trying to get a browser-downloadable link does not work if the file isn't publicly shared
                # file = service.files().get(fileId=file_id, fields='webContentLink, name').execute()
                # return HttpResponse(file)

                file = io.BytesIO()
                request = service.files().get_media(fileId=file_id)

                downloader = MediaIoBaseDownload(file, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print(f"Download {int(status.progress() * 100)}.")

                with open(f'download/{file_id}', 'wb') as f:
                    f.write(file.getbuffer())
                return redirect('successful')

            else:
                return HttpResponse("invalid form??")
        else:
            form = FileForm()
            return render(request, 'profile.html', {'download_form': form})

    except BaseException as e:
        print(e)
        return HttpResponse("Noooo")



@login_required
def delete_file(request):
    tokens = SocialToken.objects.get(account__user=request.user, account__provider='google')
    auth_token, refresh_token = tokens.token, tokens.token_secret
    creds = Credentials(
        token=auth_token,
        scopes='https://www.googleapis.com/auth/drive',
    )

    try:
        if request.method == 'POST':
            form = FileForm(request.POST)

            if form.is_valid():
                httplib2.debuglevel = 4
                service = build("drive", "v3", credentials=creds)

                file_id = form.cleaned_data['file_id']

                request = service.files().delete(fileId=file_id).execute()

                return redirect('successful')

            else:
                return HttpResponse("invalid form??")
        else:
            form = FileForm()
            return render(request, 'profile.html', {'download_form': form})

    except BaseException as e:
        print(e)
        return HttpResponse("Noooo")