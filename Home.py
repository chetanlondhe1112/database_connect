import streamlit as st
import database as db
from PIL import Image
from datetime import datetime
import streamlit_authenticator as stauth

current_date = datetime.now()

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
        users = db.fetch_all_users()

        username = [user["key"] for user in users]
        names = [user["name"] for user in users]
        hashed_password = [user["password"] for user in users]

        authenticator = stauth.Authenticate(names, username, hashed_password, "dbconn", "ghijkl", cookie_expiry_days=30)

        names, st.session_state['authentication_status'], username = authenticator.login("Login", "main")

        if st.session_state["authentication_status"]:
            st.markdown(f'# Welcome *{st.session_state["username"]}*')
            authenticator.logout('Logout', 'sidebar')
        elif st.session_state["authentication_status"] == False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] == None:
            st.warning('Please enter your username and password')

    elif process == "Sign Up":
        users = db.fetch_all_users()
        usernames = [user["key"] for user in users]
        names = [user["name"] for user in users]

        st.subheader("Create New Account")
        name = st.text_input("name")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Sign Up"):
            if name in names and username in usernames:
                st.warning("User already exist!")
            else:
                hashed_password = stauth.Hasher([str(password)]).generate()
                # print(hashed_password[0])
                db.insert_user(username,name,hashed_password)
                st.success("Successfully created.")
                st.balloons()



if __name__ == '__main__':
    main()


