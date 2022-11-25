# Zelthy-PurchaseAssignment

# Problem Statement

Consider the below Django Models:
```
Class PurchaseModel(models.Model):
    purchaser_name = models.CharField(...)
    quantity = models.IntegerField(...)

Class PurchaseStatusModel(model.Model):
    purchase = models.ForeignKey(PurchaseModel)
    status = models.CharField(
    max_length=25,
    choices=(
        ('open', 'Open'),
        ('verified', 'Verified'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
```

**Use Django 1.11 and Postgresql 9.6 to make a project with single app called “purchase” with the above two models. Write a script to populate the two models with:**
1. 5000 PurchaseModel entries with purchaser_name randomly chosen from 10 random names. Quantity can be any random number between 1 and 10 such that:
    - Average quantity of all PurchaseModel entries is 7
    - No two purchasers will have the same average quantity
2. Each PurchaseModel object should have at most 4 out of the 5 statuses from the available status choices.
    - The created dates for the PurchaseStatusModel objects must be randomly distributed between 01st Jan 2019 05 pm IST and 31st March 2020 10 pm IST

**Create a dashboard using echarts (https://echarts.apache.org/) showing a bar chart of the PurchaseModel with a Date Filter.**
- On Page load the bar chard should show 1 year data with monthly frequency.
- On changing date filter, trigger an ajax request and update the graph.

Criteria for filtering PurhaseModel with dates:
- If the latest status of PurchaseModel is dispatched, filter by created_at date of dispatched status
- If the latest status of PurchaseModel is delivered and the PurchaseModel also has a dispatched status, filter by created_at date of dispatched status
- If the latest status of PurchaseModel is delivered and the PurchaseModel does not have a dispatched status, filter by created_at date of delivered status


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
