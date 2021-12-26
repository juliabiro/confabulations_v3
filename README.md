# What is this?

This is a django webapp displaying the PhD research work of Eszter Biro at the Glasgow School of Arts. The deployed version of the app is not public, as it displays private photographs of research subjects. Moreover this version of the app contains logic that is specific to the actual database entries. 

This app is intended to serve as a display of the research, accessible only for certain authorized users, and later maybe to be presented as an exhibition item. 

The actual data is in a postgres DB. 

## where is the media?

The media files are stored on AWS S3, and they are served by CloudFront using signed URLs that expire, therefore ensuring that just visiting the app doesn't give permanent access to the files. Some images are served by Cloudinary. 

## what else?
The site doesn't work as an API, with meaningful URI structure. This is intentional, this site is not intended to be used as such, this is strictly for browsing. It was designed to display private photos belonging to the research participants, therefore the signed URLs. To prevent casual broswers from downloading the content easily, the context menus (mouse right-click) is disabled. It doesn't restrict access to the files, but makes it harder to just casually download the images and videos. 

# Development

## setup

```
$ docker-compose build

# set up superuser
$ docker-compose run web python manage.py createsuperuser

# set up database schema
$ docker-compose run web python manage.py makemigrations
$ docker-compose run web python manage.py migrate
 
# run server
$ docker-compose up

# access page on localhost/8000
```

## secrets

The secrets come form environmental variables. Required variables:
 - AWS_ACCESS_KEY_ID
 - AWS_SECRET_ACCESS_KEY
 - AWS_REGION
 - CLOUDINARY_API_KEY
 - CLOUDINARY_API_SECRET
 - DJANGO_SECRET_KEY
 - CLOUDFRONT_KEY_ID
 - CLOUDFRONT_KEY (in a one-line string that contains the CR and NL character as \r and \n)
 
 Locally these values are read from a file that is set in https://github.com/juliabiro/confabulations_v3/blob/master/.env. 

Optionally a LOCAL variable can be set to enable Django DEBUG mode. 

## Archived version

The app is being archived. To resurrect:

1. obtain a copy of the database
2. obtain API KEYS to the AWS and Cloudinary accounts
3. upgrade Python version :(
