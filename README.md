# What is this?

This is a django webapp displaying the PhD research work of Eszter Biro at the Glasgow School of Arts. The deployed version of the app is not public, as it displays private photographs of research subjects. Moreover this version of the app contains logic that is specific to the actual database entries. 

This app is intended to serve as a display of the research, accessible only for certain authorized users, and later maybe to be presented as an exhibition item. 

The actual data is in a postgres DB. 

## where is the media?

The media files are stored on AWS S3, and they are shown using signed URLs that expire, therefore ensuring that just visiting the app doesn't give permanent access to the files. Some images are served by Cloudinary. 

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
 
 Locally these values are read from a file that is set in https://github.com/juliabiro/confabulations_v3/blob/master/.env. 

Optionally a LOCAL variable can be set to enable Django DEBUG mode. 
