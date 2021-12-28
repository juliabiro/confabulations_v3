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

# set up database schema
$ docker-compose run web python manage.py makemigrations
$ docker-compose run web python manage.py migrate
$ docker-compose run web python manage.py collectstatic
 
# set up superuser
$ docker-compose run web python manage.py createsuperuser

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
 - DATABASE_URL (in the format of `postgres://<dbname>:<db_suer>@<url>:5432/<db_password>`)
 
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
DATABASE_URL=                   postgres://postgres:postgres@db:5432/postgres 
LOCAL_RESTORE=1
```
3. create a directory called 'db_backups' in this directory, and move the DB backup file there 
4. run the setup steps described above with `--file docker-compose-restore-local.yml`.  (This is the same as the main `doker-compse.yml`, but it mounts the directory with the backup, so we can access it later.  

If you load `localhost:8000` in your browser, you will see now the starting page, but with no content. 

Now is the time when we fill up the database:
5. `docker exec` into the postgres container again and import the DB backup:
```
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d postgres db_backups/DB_backup
```
As it is described here https://devcenter.heroku.com/articles/heroku-postgres-import-export#restore-to-local-database

If you reload now, you will see new content on the website. If you click around, you will be prompted for a password, you can get it from it's usual source (a passwordmanager)

If you would lose it, you can always create a new one with the createsuperuser command (but the DB backu already contains that)



### Heroku resurrect


For that you will need the [heroku cli tool](https://devcenter.heroku.com/articles/heroku-cli)

1. Create new [herokup app](https://dashboard.heroku.com/apps)

2. Modify the settngs.py toa [allow the new apps domain as an allowed host](https://github.com/juliabiro/confabulations_v3/pull/118).
push the confabulations code to it as described in the insturctions after the app is created

2. set the environmental variables in heroku 

3. run the migrations and the collectstatic
```
$ heroku run python manage.py  makemigrations -a <app name>
$ heroku run python manage.py  makemigrations migrate-a <app name>

```

4. load DB into a new DB as described here [https://devcenter.heroku.com/articles/heroku-postgres-import-export
