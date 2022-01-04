# What is this?

This is a django webapp displaying the PhD research work of Eszter Biro at the Glasgow School of Arts. The deployed version of the app is not public, as it displays private photographs of research subjects. Moreover this version of the app contains logic that is specific to the actual database entries. 

This app is intended to serve as a display of the research, accessible only for certain authorized users, and later maybe to be presented as an exhibition item. 

The actual data is in a postgres DB. 

## where is the media?

The media files are stored on AWS S3, and they are served by CloudFront using signed URLs that expire, therefore ensuring that just visiting the app doesn't give permanent access to the files. Some images are served by Cloudinary. 

## what else?
The site doesn't work as an API, with meaningful URI structure. This is intentional, this site is not intended to be used as such, this is strictly for browsing. It was designed to display private photos belonging to the research participants, therefore the signed URLs. To prevent casual broswers from downloading the content easily, the context menus (mouse right-click) is disabled. It doesn't restrict access to the files, but makes it harder to just casually download the images and videos. 

# Development

For local development, you will need docker. 

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

## Architecture

This part here is just the source code, but I want to document how to set the whole thing up again from scratch, if needed. 
Apart from the source code, the content itself lives in 2 places: a set of media files in S3, and in a postgres database that contains the texts and the connections. The media files are placed following some path- and naming conventions, and the application builds the paths to access them from the DB contents. 

#### IaaC

There is no IaaC, but there should be, because then I wouldn't have to figure out from the setup how I did it 4 years ago.

### Deployment

The application is deployed on heroku, as a standard django app. It is deployed using the standard tooling from Heroku, the secrets are set as environment variables. 

It displays content from 3 sources:
- media files stored on aws s3
- media files served from Cloudinary
- text from its own postgres DB

The database is a standard postgres DB, it can be handled with the standard postgres tools. The app uses an aws client library, so to access the files (without code  modification) they need to live on AWS S3. 

There is a CloudFront distribution in front of the S3 bucket, and there is a Cloudinary distribution that is used to retrieve some of the files.

### Media

The path to the media files on S3 are set in [here](https://github.com/juliabiro/confabulations_v3/blob/master/confabulation/utils/data.py). 

The displayed media files need to be uploaded following a special path- and naming convention:

```
- confabulations
-- <participant> # ie: XY
--- graphs # pre-generated graph images 
--- i # images 
---- <participant><id_number>.jpg # ie XY001.jpg, assumes 3 digits
---- ...
--- r # voice recordings
---- <participant><id_number>.mp4 # ie XY001.mp4, assumes 3 digits
---- ...
--- v # video recordings
---- <participant><id_number>.mp4 # ie XY001.mp4, assumes 3 digits
---- ...
-- graphs # pregenerated graph images
-- thumbnails #
--- <participant><id>.jpg # thumbnail images from all videos in the participant directories
-- Video
--- 720
---- <participant><id>.mp4 # all videos of all participants
```
File formats are assumed. Across the files, it is assumed that files with the same name but different extensions belong together, just used as different places. ie XY001.jpg is an image from XY001.mp4; in another directory, the same filename may refer to a voice recording or a thumbnail for the same video. (Today I would implement this differently, ie using an API that can create screenshots and thumbnails form images, while providing access control)

#### Access control

The participant-specific mediafiles in S3 all have restricted access. 
Access in controlled from 2 sides: there is a Bucket policy, and there are individual access permissions

1. There is an IAM user that the app uses, that has Get permissions for the necessary files, and for the CloudFront distribution. The user authenticates with an AWS keypair (today I would use an IAM role instead). The graph images are available publicly. 
The requests are pre-signed by the IAM user, it is implemented [here](https://github.com/juliabiro/confabulations_v3/blob/master/confabulation/utils/s3_helpers.py)

2. The bucket policy allow access to the admin users, to the CloudFront distribution and to Cloudinary. 

### CDNs

The app uses 2 kinds of CDNs:
It uses CloudFront to access the files on S3, and it uses Cloudinary to get the thumbnails

#### CloudFront

There is a CloudFront distribution in front of the S3 bucket that contains the media files. It only allows access from signed requests.  

#### Cloudinary

The graph and thumbnail files are served through Cloudinary (as they need to be loaded a lot, and they represent little personal information)
The app authenticates with a API keypair, and creates signed urls. this way the generated urls (though long-lived) are hard to guess. The images are resized to thumbnail size on request, and the signature belongs to the specific image size. Thus, even though the Cloudinary has access to the full-size image, and the signature is longe-lived, it only allow access to the thumbnail. 

## Archived version

The app is being archived. It is yet unclear how it will be reused; but it should be runnable both locally and as a new heroku app. 

What do I mean by archived? That the heroku application and the database serving it will be deleted; all other parts are left intact. Why? because that costs the most money, other parts (except from AWS S3) cost little or none. The AWS storage is kept up because it is still the cheapest option to store the mediafiles. 

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

Now you can restore the DB from the backup as described here [https://devcenter.heroku.com/articles/heroku-postgres-import-export
1. upload the file to s3
2. create presigned url (you can create one from the console)
3. `heroku pg:backups:restore '<SIGNED URL>' DATABASE_URL -a archival-test`

When this finishes, you can reload the heroku app and you should see all the database contents. You can use the existing credentials to log in, or create new ones with th `createsuperuser`


