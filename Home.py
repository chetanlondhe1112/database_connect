import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import streamlit_authenticator as stauth
import mysql.connector
from sqlalchemy import create_engine
current_date = datetime.now()


_ = """
    to setup mysql connection Creating connection
"""


def init_msconnection():
    return mysql.connector.connect(**st.secrets["mysql"])


def init_sqconnection():
    connect_string = "mysql://{}:@{}/{}".format(st.secrets["mysql"]["user"],
                                                st.secrets["mysql"]["host"],
                                                st.secrets["mysql"]["database"])
    return create_engine(connect_string)


conn = init_msconnection()
sq_conn = init_sqconnection()
cur = conn.cursor()

admin = st.secrets["admin"]["admin"]
master_table = st.secrets["db_table"]["master_table"]
user_table = st.secrets["db_table"]["user_table"]
query_table = st.secrets["db_table"]["query_table"]

st.set_page_config(
     page_title="Stocks Analyser",
     page_icon="chart",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )


def main():
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = ""
    if "username" not in st.session_state:
        st.session_state["username"]=""
    if "lable" not in st.session_state:
        st.session_state["lable"] = ""

    st.title("Home")
    image = Image.open('images\stock2.png')
    st.image(image, caption='Stocks Analyser', use_column_width='auto')

    Menu = ["Login", "Sign Up"]
    process = st.sidebar.selectbox("Menu", Menu)

    if process == "Login":
        df = pd.read_sql_query("SELECT * FROM " + user_table, conn)
        names = list(df['id'])
        usernames = list(df['username'])
        hashed_passwords = list(df['password'])

        authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "sfdb", "abcdef", cookie_expiry_days=30)

        names, st.session_state['authentication_status'], username = authenticator.login("Login", "main")

        if st.session_state["authentication_status"]:
            st.write(f'Welcome *{st.session_state["username"]}*')
            authenticator.logout('Logout', 'sidebar')
            st.session_state["username"]=username
            if st.session_state["username"]==admin:
                st.session_state["lable"]='admin'
            else:
                st.session_state["lable"]='user'
        elif st.session_state["authentication_status"] == False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] == None:
            st.warning('Please enter your username and password')

    elif process == "Sign Up":
        st.subheader("Create New Account")
        user_id = st.text_input("User ID (mail_id)")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')


        acc_query = "SELECT * FROM user_login where id='" + str(
            user_id) + "' AND username='" + username + "' AND password='" + password + "'"
        cur.execute(acc_query)
        values = cur.fetchall()
        if st.button("Sign Up"):
            if values:
                st.warning("User already exist!")
            else:
                hashed_password = stauth.Hasher([str(password)]).generate()
                # print(hashed_password[0])
                add_query = 'insert into `user_login`(`id`,`username`,`password`)VALUES(%s,%s,%s)'
                cur.execute(add_query, (str(user_id), username, str(hashed_password[0])))
                conn.commit()
                st.success("Successfully created.")
                st.balloons()

if __name__ == '__main__':
    main()


