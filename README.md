## Cappr

**Initial Setup**

This assumes you have Postgres installed. If not, please read the postgres installation instructions.

1. `git clone` the repo using SSH or HTTPS.
2. `cd` into the newly cloned repository.
3. Create a Virtual Environment. `virtualenv -p python3 venv`
4.  `source venv/bin/activate` will start the virtualenv.
5.  `pip install -r requirements.txt` will install the dependencies needed for the project into the virtualenv.
6.  `python manage.py migrate` will set up the development database

**Postgres Installation**

1. Download and install `postgres` for your OS [here](https://www.postgresql.org/download/).
2. Enter the Postgres Shell.
3. `CREATE DATABASE capprdb` will create our db.
4. `CREATE USER cappr WITH PASSWORD '<your_password>'` will create a user for our database.
5. `GRANT ALL PRIVILEGES ON DATABASE capprdb TO USER cappr` will grant the necessary permissions to our user.

**Settings**

The settings module is divided into multiple files to streamline the dev environment.

1. `base.py` contains all the common Django required settings.
2. `production.py` contains the settings specific to the Production Server. Don't touch this unless you intentionally want to affect the production server.
3. `templates/` This folder contains the development settings file templates. Copy both files into the `settings/` directory and rename them from `.template` to `.py`. These files are included in `.gitignore` so that every developer can have his own settings without affecting other developers.
4. `dev-sqlite.py` is specifically for the SQLite database. The database itself is not synced to Github.
5. `dev-postgres.py` uses the Postgres database as its backend.

**PyCharm Customizations**

Follow these instructions to setup PyCharm for easy development.

Click on `Edit Configurations` in the `Run` menu.

![](http://image.prntscr.com/image/c8f046fafa0d40b5bd6881665316a8a7.png)

#

Add a `Django Server` configuration and name it.
![](http://image.prntscr.com/image/00b7865af5f141d5b5ce986ed7cc04bd.png)

#

Set the environment variable to point to your settings file.
This one is for the postgres backend. Repeat these steps for `dev-sqlite.py`.

![](http://image.prntscr.com/image/240df980bf254482b8b3ad75f97b81c9.png)

#
When you're done, you should have something like this.

![](http://image.prntscr.com/image/42b8c23536fc4c6aaa2a642aca83b883.png)