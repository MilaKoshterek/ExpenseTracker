# Registration - name,email,password,id
# userdetails - credentials- documents of user {"Name":name, "Email": email, "Password":password after hashing}
# Check for existence of registered user
import datetime
import hashlib
import uuid
import pymongo
import pandas as pd
import certifi
import plotly.express as px

client = pymongo.MongoClient(
    "mongodb+srv://Alejandra:ZVMrff3p5nBaTgU@tracker.v3pj7t7.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where())
db = client["MoneyTracker"]
col = db["UserData"]
col_transactions = db["user_transactions"]

def userregistration(name, email, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    user_details = {"_id": uuid.uuid4().hex, "Name": name, "Email": email, "Password": hashed_password}
    check = col.find_one({"Email": email})
    if check:
        return 'user already exists'
    else:
        col.insert_one(user_details)
        return 'registration is successful'


def login(email, password):
    check = col.find_one({"Email": email})
    if check:
        hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if check["Password"] == hash_password:
            return ['success', check['_id']]

        else:
            return ['wrong password']
    else:
        return ['No user found']


def reset_password(email, password):
    check = col.find_one({"Email": email})
    if check:
        col.update_one({'Email': email}, {'$set': {'Password': hashlib.sha256(password.encode('utf-8')).hexdigest()}})


def add_transactions(id, transactions):
    idcheck = col_transactions.find_one({'_id': id})
    if idcheck:
        new_transaction = idcheck["transactions"] + transactions
        col_transactions.find_one_and_update({"_id": id}, {"$set": {"transactions": new_transaction}})
    else:
        search_details = {"_id": id, "transactions": transactions}
        col_transactions.insert_one(search_details)


def get_user_transactions(user_id):
    user_data = col_transactions.find_one({'_id': user_id})
    if not user_data:
        return []

    return user_data.get('transactions')


def get_savings(user_id):
    expenses = []
    incomes = []
    savings = 0
    sum_incomes = 0
    sum_expenses = 0

    transactions = get_user_transactions(user_id)

    print('Total transactions {}'.format(len(transactions)))
    for transaction in transactions:
        if transaction["category"] != "Income":
            expenses.append(transaction["amount"])
            sum_expenses = sum(expenses)
        if transaction["category"] == "Income":
            incomes.append(transaction["amount"])
            sum_incomes = sum(incomes)
        savings = sum_incomes - sum_expenses

    print(f"The savings are: {savings} euros.")
    return savings


def get_overview_activity(transactions, start_date, end_date):
    date_format = '%Y-%m-%d'

    start_date = datetime.datetime.strptime(start_date, date_format)
    end_date = datetime.datetime.strptime(end_date, date_format)
    transactions_within_range = []
    for transaction in transactions:
        if 'date' not in transaction:
            continue

        transaction_date = datetime.datetime.strptime(transaction['date'], date_format)
        if start_date <= transaction_date <= end_date:
            transactions_within_range.append(transaction)

    return transactions_within_range


def get_expenses_charts(transactions_list):
    df = pd.DataFrame(transactions_list, columns=["amount", "date", "category"])
    df_only_expenses = df[df.category != "Income"]
    fig_bar = px.bar(df_only_expenses, x="date", y="amount", title="Expenses by date",
                     color_discrete_sequence=['rgb(40, 114, 116)'])
    fig_pie = px.pie(df_only_expenses, names="category", values="amount", title="Percentage of expenses by category",
                     color_discrete_sequence=px.colors.sequential.Mint)
    return [fig_bar, fig_pie]


def get_hist(transactions_list):
    '''
    In this function, I made a quick loop through the list passed as a parameter to change the value of each
    string that is not "Income", and make it "Expense". This will give us a new list to make a dataframe for the
    histogram chart with just income and expenses.
    :param transactions_list:
    :return: a histogram chart - Similar to a bar chart, but I believe with more functionalities
    '''
    main_categories_transactions_list = transactions_list
    for i in main_categories_transactions_list:
        if i["category"] != "Income":
            i["category"] = "Expense"
    df_main_categories = pd.DataFrame(main_categories_transactions_list, columns=["amount", "date", "category"])
    fig_histogram = px.histogram(df_main_categories, x="amount", y="category", text_auto=True,
                                 title="Overview income and expenses",
                                 barmode="group",
                                 color="category", color_discrete_sequence=['rgb(137, 192, 182)', 'rgb(40, 114, 116)'])
    return fig_histogram

