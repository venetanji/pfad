import streamlit as st
import hashlib
from model import User

# Streamlit app
st.title("An app with users")

if 'flash' not in st.session_state:
    st.session_state.flash = st.empty()
       
# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to register a new user
def register_user(username, email, password):
    try:
        user = User.create(username=username, email=email, password=hash_password(password))
    except Exception as e:
        st.warning(f"Error: {e}")

# Function to login a user
def login_user(username, password):
    try:
        user = User.get(User.username == username)
        if user.password == hash_password(password):
            st.success("Login successful!")
            return user
        else:
            st.error("Invalid username or password.")
    except User.DoesNotExist:
        st.error("Invalid username or password.")


def register():
    st.subheader("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')
    if st.button("Register"):
        if password != confirm_password:
            st.session_state.flash.warning("Passwords do not match!")
        elif not username or not email or not password:
            st.session_state.flash.warning("Please fill in all fields.")
        else:
            user = register_user(username, email, password)
            # redirect to login page
            st.switch_page(login_page)
            
def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if user := login_user(username, password):
            st.session_state.user = user
            st.success(f"Welcome, {user.username}!")
            # redirect to home page

login_page = st.Page(login, title="Login")
register_page = st.Page(register, title="Register")

pg = st.navigation([login_page, register_page])

pg.run()