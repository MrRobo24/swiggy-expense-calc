# swiggy-expense-calc

- __swiggy-expense-calc__ is a script that analyzes your Swiggy expenses over the past year.
- You are expected to login to your swiggy account by entering your registered mobile number and OTP from swiggy (feel free to review the [code](https://github.com/MrRobo24/swiggy-expense-calc/blob/main/swiggy.py) if you have trust issues).
- The script will fetch swiggy orders from last 1 year and give you a csv sheet with grouped data and also generate a csv with all the orders.

### Install Dependencies

```
pip3 install -r requirements.txt
```

### Run Script

Initially execute the following command to run this script in sandbox mode on only a few past orders.
```
python3 -u main.py
```

If the script successfully outputs the _swiggy-expenses.csv_ with valid data then you can go ahead use environemnt as _production_ to fetch orders from last 1 year:

```
ENV='production' python3 -u main.py
```
