import datetime
import streamlit as st
from streamlit_option_menu import option_menu
import helper

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

title = st.markdown('''<h1 style= "text-align:center; color:#ff4b4b;">
                    EXPENSES TRACKER
                    </h1>''',
                    unsafe_allow_html=True)
def log_submit_transaction(user_id):
    '''
    Allows the user to log transaction details and submit them. By doing so, they will be sent to mongo. We will use the
    dataset to calculate savings. We use previous functions defined on the helper.py file.
    :param user_id: The user_id will be used as a parameter to call the functions add_transactions and get_savings
    :return:
    '''
    categories = ["Income", "Housing", "Food", "Transport", "Entertainment", "Personal", "Insurance", "Other"]
    log_text = st.markdown('''<h6 style= "text-align:center; color:#ff4b4b;">
                                                                    Please log  your transactions
                                                                    </h6>''', unsafe_allow_html=True)
    amount = st.number_input("Please enter the amount:")
    today = datetime.date.today()
    date = st.date_input("Please enter the date:", today)
    category = st.selectbox("Please select the category:", categories)
    submit_transaction = st.checkbox("Submit transaction details")
    if submit_transaction:
        mongo_date = date.strftime('%Y-%m-%d')
        transaction_dict = {"amount": amount, "date": mongo_date, "category": category}
        transactions = [transaction_dict]
        helper.add_transactions(user_id, transactions)
        savings = helper.get_savings(user_id)
        st.text(f"Your savings are {savings} euros.")


with st.sidebar:
    option = option_menu("User Login", ["Register", "Login", "Reset Password"],
                         menu_icon="house", default_index=0)
if option == "Register":
    with st.expander("Expand to register", expanded=True):
        cols = st.columns([1, 3, 1])
        name = cols[1].text_input("Enter name: ")
        email = cols[1].text_input("Enter email:")
        password = cols[1].text_input("Enter password:", type="password")
        if st.button("Register"):
            result = helper.userregistration(name, email, password)
            st.success(result)

if option == "Login":
    # with st.expander("Expand to login", expanded=True):
    cols = st.columns([1, 3, 1])
    email = cols[1].text_input("Enter email:")
    password = cols[1].text_input("Enter password:", type="password")
    if cols[1].checkbox("Submit"):
        global result_login
        result_login = helper.login(email, password)
        st.success(result_login[0])
        if result_login[0] == "success":
            with st.sidebar:
                 option_transactions = option_menu("Overview", ["Log Transaction", "Analyse by date"],
                                                      menu_icon="bar-chart", default_index=0)

            if option_transactions == "Log Transaction":
                        user_id = result_login[1]
                        transactions_list = helper.get_user_transactions(user_id)
                        current_balance = helper.get_savings(user_id)
                        fig_pie = helper.get_expenses_charts(transactions_list)[1]
                        fig_hist = helper.get_hist(transactions_list)
                        if len(transactions_list) > 0:
                            transactions_text = st.markdown('''<h5 style= "text-align:left; color:#ff4b4b;">
                                                                                                 Transactions overview:
                                                                                                 </h5>''', unsafe_allow_html=True)
                            current_balance_text = st.text(f"Your current balance is {current_balance} euros.")
                            st.plotly_chart(fig_hist, use_container_width=True)
                            st.plotly_chart(fig_pie, use_container_width=True)
                            ask_log_transaction = st.checkbox("Please check to log a transaction")
                            if ask_log_transaction:
                                log_submit_transaction(user_id)

                        elif len(transactions_list) == 0:
                            log_submit_transaction(user_id)

            if option_transactions == "Analyse by date":
                        today = datetime.date.today()
                        s_date = st.date_input("Please enter the start date:", today)
                        start_date = s_date.strftime('%Y-%m-%d')
                        e_date = st.date_input("Please enter the end date:", today)
                        end_date = e_date.strftime('%Y-%m-%d')

                        user_id = result_login[1]
                        all_transactions = helper.get_user_transactions(user_id)
                        range_transactions_list = helper.get_overview_activity(all_transactions, start_date, end_date)
                        fig_bar_specific = helper.get_expenses_charts(range_transactions_list)[0]
                        fig_pie_specific = helper.get_expenses_charts(range_transactions_list)[1]

                        st.plotly_chart(fig_bar_specific, use_container_width=True)
                        st.plotly_chart(fig_pie_specific, use_container_width=True)


if option == "Reset Password":
    with st.expander("Expand to reset password", expanded=True):
        cols = st.columns([1, 3, 1])
        email = cols[1].text_input("Enter email:")
        new_password = cols[1].text_input("Enter new password:", type="password")
        if cols[1].checkbox("Reset password"):
            result_new_password = helper.reset_password(email, new_password)
            st.success("You have a new password")





