# Hamro Notes

<p align="center">
 <!-- <img width="100px" src="https://res.cloudinary.com/dhu3zenko/image/upload
 /v1597226777/Hamronotes/logo_vszykh.png" align="center" alt="Hamro Notes
 " /> -->
 <img width="400px" src="./assets/Logo890x180.svg" align="center" alt="Hamro Notes
 " />
<p align="center">Get your necessary Univeristy Notes</p>

</p>

 <p align="center">
    <a href="#">View Demo</a>
    ·
    <a href="https://github.com/iw-academy-project/iw-acad-hamro-note-be/issues">Report Bug</a>
    ·
    <a href="https://github.com/iw-academy-project/iw-acad-hamro-note-be/issues">Request Feature</a>
</p>

## ✨ Features

- Login/Signup Functionality
- Upload Specific Notes
- Specific groups with related Notes
- Discussion Forums
- Blog section with commenting features

## Tech Stack

| Stack   | -                                                                                           | -                                                                                           | -                                                                                                   | -                                                                                     | -                                                                                           |
| ------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| BackEnd | <p align="center"><img src="./assets/python.jpg" width="100" height="100"> <br />Python</p> | <p align="center"><img src="./assets/Django.jpg" width="100" height="100"> <br />Django</p> | <p align="center"><img src="./assets/Postgresql.png" width="100" height="100"> <br />Postgresql</p> | <p align="center"><img src="./assets/AWS.png" width="100" height="100"> <br />AWS</p> | <p align="center"><img src="./assets/REST.png" width="100" height="100"> <br />REST API</p> |

# Overview

<img  src="./assets/hamronoteapi.png" align="center" alt="Hamro Notes
 " />

# Installation

## Method 1

> Use setup.sh for automating the installation of the project

```sh
$ chmod +x setup.sh
$ ./setup.sh
```

> Make sure your are on project directory

## Method 2

### Step 1: Clone the repo

```sh
$ git clone https://github.com/iw-academy-project/iw-acad-hamro-note-be.git
$ cd iw-acad-hamro-note-be
```

### Step 2: Setup Environement and install Dependencies

```
$ virtualenv venv
$ source bin/activate
$ pip install -r requirements.txt
```

### Step 3: Configure env variables

```sh
$ cp .env.example .env
```

Now, edit .env to contain
`DEBUG = True`
`SECRET_KEY = <your_key>`
`EMAIL_USE_TLS = True`
`EMAIL_HOST = smtp.gmail.com`
`EMAIL_HOST_USER = <your_gmail>`
`EMAIL_HOST_PASSWORD = <your_gmail_password>`
`EMAIL_PORT = 587`

### Step 4: Configure

```sh
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

> Make sure, you know to create superuser for administration.
> You must enable less secure access on the gmail account

### Step 5: Running tests with coverage

```sh
$ python manage.py test coverage
```

## License

Licensed under the [MIT License](./LICENSE).

## Acknowledgements and Credits

<table>
	<tr>
		<td align="center">
			<a href="https://github.com/Aju100"><img src="https://avatars2.githubusercontent.com/u/29862610?s=400&v=4" width="100px;" alt=""/><br /><sub><b>Aju Tamang</b></sub></a><br />
		</td>	
		<td align="center">
			<a href="https://github.com/AnjalBam"><img src="https://avatars2.githubusercontent.com/u/50726466?s=400&u=1e7347041ed721299eafd73af5f391401e2f3858&v=4" width="100px;" alt=""/><br /><sub><b>Anjal Bam</b></sub></a><br />
		</td>
		<td align="center">
			<a href="https://github.com/rajeshpandey2053"><img src="https://avatars0.githubusercontent.com/u/29334243?s=400&u=63afd14c253c38bb4b4eb928080a9e4bd327a66e&v=4" width="100px;" alt=""/><br /><sub><b>Rajesh Pandey</b></sub></a><br />
		</td>
		<td align="center">
			<a href="https://github.com/razyesh"><img src="https://avatars3.githubusercontent.com/u/33127872?s=400&u=87e7f67c7a08dba1dec329986e5e06629b37e545&v=4" width="100px;" alt=""/><br /><sub><b>Rajesh Pudasaini</b></sub></a><br />
		</td>
	</tr>
</table>

> Names are sorted by Alphabet
