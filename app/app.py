import streamlit as st
import bcrypt
from models import User, Session
import main_page

# Function to hash a password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to check credentials
def check_credentials(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return True
    return False

# Function to register a new user
def register_user(username, password):
    session = Session()
    # Check if user already exists
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user is not None:
        session.close()
        return False  # User already exists

    # Create new user
    hashed_password = hash_password(password)
    new_user = User(username=username, password_hash=hashed_password.decode('utf-8'))
    session.add(new_user)
    session.commit()
    session.close()
    return True

def clear_form():
    # This function will clear all form fields but maintain other necessary session states
    for key in list(st.session_state.keys()):
        if key not in ['logged_in', 'user_id']:  # Preserve login and other essential states
            del st.session_state[key]

# Main app function
def main():

    st.title("Airbus Ship Detection")

    # Session state to keep track of login status
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                if check_credentials(login_username, login_password):
                    st.session_state['logged_in'] = True
                    st.experimental_rerun()  # Rerun the app to clear previous content and proceed
                else:
                    st.error("Incorrect username or password.")
        with tab2:
            reg_username = st.text_input("Choose a Username", key="reg_username")
            reg_password = st.text_input("Choose a Password", type="password", key="reg_password")
            if st.button("Register"):
                if register_user(reg_username, reg_password):
                    st.success("Registered successfully. You can now log in.")
                else:
                    st.error("Username already taken. Please choose another.")
    else:
        # Call the main function from main_page module after clearing the previous content
        main_page.main()
        
if __name__ == "__main__":
    main()
