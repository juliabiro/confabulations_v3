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
$ docker-compose run web python manage.py collectstatic
 
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

The app is being archived. It is yet unclear how it will be reused; but it should be runnable both locally and as a new heroku app. 
To resurrect, you need the following data:

1. a copy of the database backup
2. API KEYS to the AWS and Cloudinary accounts


### Local resurrect up

1. Create a web-variables file locally. Add the needed variables in a `key=value` format 
2. In the web-variables-file, set  up
```
DATABASE_URL=                   postgres://db:5432 
LOCAL_RESTORE= up1
```
3. create a directory called 'db_backups' in this directory, and move the DB backup file there  up
4. remove the `data` direcotry if exists

5. Run `docker-compose --file docker-compose-restore-local.yml up` This will sort of fail or hang, but it will have a DB container that you can connect to
In another terminal `docker exec` into the created postgres container, connect to the database qith `psql -h localhost -U postgres` and change the password to "postgres"  with the `\password` ommand

6. Now you can stop the previous docker compose, and run the makemigrations and migrate and collectstaticsetup steps as described above, but with `--file docker-compose-restore-local.yml` everywhere. You don't need to run the createsuperuser one. 

If you load `localhost:8000` in your browser, you will see now the starting page, but with no content. 

No is the time when we fill up the database:
7. `docker exec` into the postgres container again and import the DB backup:
```
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d postgres db_backups/DB_backup
```
As it is described here https://devcenter.heroku.com/articles/heroku-postgres-import-export#restore-to-local-database

If you reload now, you will see new content on the website. If you click around, you will be prompted for a password, you can get it from it's usual source (a passwordmanager)

If you would lose it, you can always create a new one with the createsuperuser command (but the DB backu already contains that)



### Heroku resurrect

Create new herokup app, load DB into a new DB as described here [https://devcenter.heroku.com/articles/heroku-postgres-import-export
