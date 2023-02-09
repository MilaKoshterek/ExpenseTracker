import helper

# test code mongo db without streamlit
for userData in helper.col.find({}):
    print('--------------------------------------------')
    user_id = userData.get('_id')
    print("test login")
    test_login = helper.login(userData.get('Email'), userData.get("Password"))
    print(test_login)
    print(userData)
    print("SAVINGS NUMBER IS:")
    print(helper.get_savings(user_id))
    all_transactions = helper.get_user_transactions(user_id)
    print("ALL TRANSACTIONS LIST: ")
    print(all_transactions)
    range_transactions = helper.get_overview_activity(helper.get_user_transactions(user_id), '2022-12-28', '2023-01-03')
    print("RANGE TRANSACTIONS LIST:")
    print(range_transactions)
    helper.get_expenses_charts(all_transactions)







# today = date.today()
# print(today)
#
# d = st.date_input(
#     "When\'s your birthday", today)
# st.write('Your birthday is:', d)
#
# print(px.colors.sequential.Mint)