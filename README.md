# Zelthy-PurchaseAssignment

# Setup Instructions

## Pyenv Setup(MacOS 10.9+)

#### Step 1: Install Pre-Requisites

```
brew install openssl readline sqlite3 xz zlib

export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/
```

#### Step 2: Install pyenv

```
curl https://pyenv.run | bash
```

Add the following code to your `~/.bash_profile` file
```
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
This will load pyenv when a terminal is started

#### Step 3: Install Python 3.6.10

```
pyenv install -v 3.6.10
```
Here `-v` represents the python version. In our case it is `3.6.10`.
You could install different versions using the `-v` option.

#### Step 4: Create Virtual Environment

```
pyenv virtualenv 3.6.10 zelthy-3.6.10
```
The above command creates a virtual environment with name `zelthy-3.6.10` using python version `3.6.10`. You can choose a name that is preferable to you.

#### Step 5: Activate Virtual Environment

```
pyenv activate zelthy-3.6.10
```
Once the virtual environment that you created is activated, you can install the requirements and run the server. Once the work is completed you could deactivate your virtual environment using `pyenv deactivate`# Setup Instructions


## DB Setup

#### Step 1: Install Postgres
```
brew install postgresql@9.6
```

#### Step 2: Enter Postgres Shell

```
psql
```

#### Step 3: Create Database

```
CREATE DATABASE zelthy WITH OWNER postgres;
```

## Django Project Setup

#### Pre-Requisites

- Forked and cloned this repository.
- Navigate into cloned location.
- An activated virtual environment with python version 3.6.10

#### Step 1: Install requirements.

```
pip install -r requirements.txt
```

#### Step 2: Migrate

```
python manage.py migrate
```

#### Step 3: SeedData

```
python manage.py seed_data
```
This will create 5000 records


#### Step 4: Create an admin user

```
python manage.py createsuperuser
```

#### Step 5: Runserver

```
python manage.py runserver 0:8000
```

## Testing the Application

#### Admin URL for viewing/creating Purchases

```
http://localhost:8000/admin/purchase/purchase/
```

#### URL for loading Analytics chart

```
http://localhost:8000/purchase/analyse-purchases/
```

#### Postman Collection for Testing the Search API.
```
https://www.getpostman.com/collections/aa0b195feca8ac0447fb
```