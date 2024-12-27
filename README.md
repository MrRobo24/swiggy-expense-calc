# swiggy-expense-calc

- __swiggy-expense-calc__ is a script that analyzes your Swiggy expenses over the past year.
- You are expected to login to your swiggy account on the web and paste the cookies here in a file for the script to use. 
- The script will fetch swiggy orders from last 1 year and give you a csv sheet with grouped data and also generate a csv with all the orders.

### Install Dependencies

```
pip3 install -r requirements.txt
```

### Insert Cookies

1. Login to [swiggy](https://www.swiggy.com) on the browser and open the [orders page](https://www.swiggy.com/my-account/orders).
2. Inspect the page and search for __all?order_id=__ in the Network tab.
3. Expand the request and copy the __cookie:__ header's value.
4. Paste the value in __cookies__ file in the project directory: swiggy-expense-calc/cookies.

### Run Script

Initially execute the following command to run this script in sandbox mode on only a few past orders.
```
python3 -u main.py
```

If the script successfully outputs the _swiggy-expenses.csv_ with valid data then you can go ahead use environemnt as _production_ to fetch orders from last 1 year:

```
ENV='production' python3 -u main.py
```