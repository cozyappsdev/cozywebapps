import streamlit as st

import sqlite3
import pandas as pd
import os

from datetime import datetime, date
import time

#current_date = date.today()

current_date = datetime.now()

# Format date as string

formatted_curdate = current_date.strftime("%d/%m/%Y  %H:%M:%S")


# Define the dialog Function

@st.dialog("Message")

def show_message(msg):

    st.write(msg)

    if st.button("Close"):

        st.rerun() # Closesthe dialog


def init_db():

    cnnOne = sqlite3.connect("ATFDb.db")

    cursor = cnnOne.cursor()    

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS AccommoRecs (

    RecID INTEGER PRIMARY KEY AUTOINCREMENT,

    RecDte TEXT(25) NOT NULL,       

    Country TEXT(25) NOT NULL,

    City TEXT(25) NOT NULL,        

    Suburb TEXT(25) NOT NULL,

    NoOfRooms TEXT(5) NOT NULL,

    Rent TEXT(10) NULL,        

    EntryNo TEXT(25) NOT NULL,        

    ContactNo TEXT(20) NOT NULL,

    RS TEXT(5) NOT NULL

    )"""

    )
   

    # Commit the changes

    cnnOne.commit()


# Initialize database

init_db()


# App main title

st.set_page_config(page_title = "The Accommodation Market", layout = "centered")


#pvProcessFeedback = st.empty()
#pvSuccessFeedback = ""

def clearFormFields():

    st.session_state["dtaRecDte"] = ""

    st.session_state["dtaCountry"] = ""

    st.session_state["dtaCity"] = ""

    st.session_state["dtaSuburb"] = ""

    st.session_state["dtaNoOfRooms"] = ""

    st.session_state["dtaRent"] = ""

    st.session_state["dtaEntryNo"] = ""

    st.session_state["dtaContactNo"] = ""


def home_page():

    # App main title    

    st.header("Home Page") 

    st.title("Welcome to The Accommodation Market") 

    st.write("Use the App Pages Panel on the left to navigate to the various pages of the application.")


def EnterAvailableAccommodation_page():

    st.header("Accommodation Offers Entry Page")

    st.write("ENTER AND SUBMIT THE DETAILS OF THE ACCOMMODATION YOU WANT TO RENT OUT")

    st.write("NB: After entering data in each field (including the DATE), press ENTER/TAB to apply. If the date is already entered, begin by clicking within the DATE field and exiting it through the TAB to apply the date.")
    
    dtaRent = ""  

    # Initialize session state for the input if it doesn't exist      

    if "dtaCountry" not in st.session_state:

        st.session_state["dtaCountry"] = ""

    if "dtaCity" not in st.session_state:

        st.session_state["dtaCity"] = ""

    if "dtaSuburb" not in st.session_state:

        st.session_state["dtaSuburb"] = ""

    if "dtaNoOfRooms" not in st.session_state:

        st.session_state["dtaNoOfRooms"] = ""

    if "dtaRent" not in st.session_state:

        st.session_state["dtaRent"] = ""

    if "dtaEntryNo" not in st.session_state:

        st.session_state["dtaEntryNo"] = ""

    if "dtaContactNo" not in st.session_state:

        st.session_state["dtaContactNo"] = ""


    # Use st.markdown to inject custom CSS

    st.markdown("""

    <style>

    .stTextInput input {text-transform: uppercase;

    }

    </style>

    """, unsafe_allow_html = True)


    dtaRecDte = st.text_input("Enter the DATE.", key = "dtaRecDte", value=formatted_curdate,on_change = None) # pvRecDte =

    dtaCountry = st.text_input("Enter the COUNTRY in which the accommodation is available.", key = "dtaCountry", on_change = None) # pvCountry = 

    dtaCity = st.text_input("Enter the CITY/TOWN", key = "dtaCity") 

    dtaSuburb = st.text_input("Enter the SUBURB where the accommodation is available.",  key = "dtaSuburb", on_change = None) # pvSuburb = 

    dtaNoOfRooms = st.text_input("Enter the NUMBER OF ROOMS available.", key = "dtaNoOfRooms", on_change = None) 

    dtaRent = st.text_input("Enter the MONTHLY RENT TOTAL AMOUNT: e.g. $450.00 or £150.00", key = "dtaRent", on_change = None)      

    dtaEntryNo = st.text_input("Enter a UNIQUE REF for the record, e.g. 392GREENSIDEROOMS", key = "dtaEntryNo", on_change = None) # pvEntryNo = 

    dtaContactNo = st.text_input("Enter your BUSINESS CONTACT NUMBER", key = "dtaContactNo", on_change = None) 


    # Function to insert data into the table

    def InsertAccommoToRentOut(): #RecDte,Country,City,Suburb,NoOfRooms,Rent,EntryNo,ContactNo,RS):    

        #pvProcessFeedback = ""

        # Convert all text in python variables to uppercase

        upcRecDte = dtaRecDte.upper()

        upcCountry = dtaCountry.upper() 

        upcCity = dtaCity.upper()

        upcSuburb = dtaSuburb.upper()

        upcNoOfRooms = dtaNoOfRooms.upper()

        upcRent = dtaRent.upper()  

        upcEntryNo = dtaEntryNo.upper()

        upcContactNo = dtaContactNo

        dtaRS = 'Lld'    
    

        # CHECK PRESENCE OF RECORD BY COUNTING RECORD'S ID

        try:               

            cnnOne= sqlite3.connect('ATFDb.db')       

            cur = cnnOne.cursor()       

            RowsQuery="SELECT COUNT(*) FROM AccommoRecs WHERE EntryNo=?"       

            cur.execute(RowsQuery, (upcEntryNo,))           

            # Collect result of count

            NumberOfAccs=cur.fetchone()[0]

        except sqlite3.Error as e:

            st.warning(f"An error occurred: {e}")

        finally:

            if cnnOne:

                cnnOne.close()
                

        if NumberOfAccs > 0:

            st.warning(f"{upcEntryNo} is not available. Please create a different entry number and try again.")

        else:


            if upcRecDte and upcCountry and upcCity and upcSuburb and upcNoOfRooms and upcRent and upcEntryNo and upcContactNo:
            

                try:
                    

                    cnnOne =sqlite3.connect('ATFDb.db')

                    cursor = cnnOne.cursor() 


                    InsertDetailsQuery = "INSERT INTO AccommoRecs (RecDte,Country,City,Suburb,NoOfRooms,Rent,EntryNo,ContactNo,RS) VALUES (?,?,?,?,?,?,?,?,?)"
                    

                    cursor.execute(InsertDetailsQuery, (upcRecDte,upcCountry,upcCity,upcSuburb,upcNoOfRooms,upcRent,upcEntryNo,upcContactNo,dtaRS))

                    # Confirm success 
                                      
                    st.toast(f"Entry number {upcEntryNo} inserted successfully.")                   

                    # persist the changes to database by calling cnnOne.commit() 

                    cnnOne.commit()

                    # close the connection

                    cnnOne.close()                                         


                except sqlite3.Error as ex:

                    sqlstate = ex.args[0]

                    st.warning(f"Error inserting new record: {sqlstate}.")

                finally:

                    # Close the connection

                    if cnnOne:

                        cnnOne.close()

            else:

                st.warning("Please enter data in every data field.")

    st.button("Submit", on_click =  InsertAccommoToRentOut)
    
def EnterWantedAccommodation_page():

    st.header("Accommodation Wanted Entry Page")

    st.write("ENTER AND SUBMIT THE DETAILS OF THE ACCOMMODATION YOU ARE LOOKING FOR")

    st.write("NB: After entering data in each field (including the DATE), press ENTER/TAB to apply. If the date is already entered, begin by clicking within the DATE field and exiting it through the TAB to apply the date.")


    # FOR CLEARING DATA FIELDS

    # Initialize session state for the input if it doesn't exist         

    if "dtaCountry" not in st.session_state:

        st.session_state["dtaCountry"] = ""

    if "dtaCity" not in st.session_state:

        st.session_state["dtaCity"] = ""

    if "dtaSuburb" not in st.session_state:

        st.session_state["dtaSuburb"] = ""

    if "dtaNoOfRooms" not in st.session_state:

        st.session_state["dtaNoOfRooms"] = ""

    if "dtaRent" not in st.session_state:

        st.session_state["dtaRent"] = ""

    if "dtaEntryNo" not in st.session_state:

        st.session_state["dtaEntryNo"] = ""

    if "dtaContactNo" not in st.session_state:

        st.session_state["dtaContactNo"] = ""


    # Use st.markdown to inject custom CSS

    st.markdown("""

    <style>

    .stTextInput input {text-transform: uppercase;

    }

    </style>

    """, unsafe_allow_html = True)


    #rawRecDte = st.text_input("Enter the DATE.", key = "dtaRecDte", on_change = None) # pvRecDte =

    rawRecDte = st.text_input("Enter the DATE.", key = "dtaRecDte", value=formatted_curdate,on_change = None)

    rawCountry = st.text_input("Enter the COUNTRY in which you are looking for accommodation.", key = "dtaCountry", on_change = None)

    rawCity = st.text_input("Enter the CITY/TOWN", key = "dtaCity", on_change = None)

    rawSuburb = st.text_input("Enter the SUBURB where you wish the accommodation to be.", key = "dtaSuburb", on_change = None)

    rawNoOfRooms = st.text_input("Enter the NUMBER OF ROOMS you want.", key = "dtaNoOfRooms", on_change = None)       

    rawEntryNo = st.text_input("Enter a UNIQUE REF for the record, e.g. GREENSIDESEARCHES001", key = "dtaEntryNo", on_change = None)

    rawContactNo = st.text_input("Enter your BUSINESS CONTACT NUMBER", key = "dtaContactNo", on_change = None)


    def InsertAccommoWanted():


        # Convert all text in python variables to uppercase

        hgcRecDte = rawRecDte.upper()

        hgcCountry = rawCountry.upper() 

        hgcCity = rawCity.upper()

        hgcSuburb = rawSuburb.upper()

        hgcNoOfRooms = rawNoOfRooms.upper()   

        hgcEntryNo = rawEntryNo.upper()

        hgcContactNo = rawContactNo

        rawRS = 'Tnt'    
    

        # CHECK PRESENCE OF RECORD BY COUNTING RECORD'S ID

        try:               

            cnnOne= sqlite3.connect('ATFDb.db')       

            cur = cnnOne.cursor()       

            RowsQuery="SELECT COUNT(*) FROM AccommoRecs WHERE EntryNo=?"       

            cur.execute(RowsQuery, (hgcEntryNo,))           

            # Collect result of count

            NumberOfAccs=cur.fetchone()[0]

        except sqlite3.Error as e:

            st.warning(f"An error occurred: {e}")

        finally:

            if cnnOne:

                cnnOne.close()
                

        if NumberOfAccs > 0:

            st.warning(f"{ hgcEntryNo} is not available. Please create a different entry number and try again.")

        else:

            if hgcRecDte and hgcCountry and hgcCity and hgcSuburb and hgcNoOfRooms and hgcEntryNo and hgcContactNo:            

                try:                    

                    cnnOne =sqlite3.connect('ATFDb.db')

                    cursor = cnnOne.cursor()

                    InsertDetailsQuery = "INSERT INTO AccommoRecs (RecDte,Country,City,Suburb,NoOfRooms,EntryNo,ContactNo,RS) VALUES (?,?,?,?,?,?,?,?)"
                    
                    cursor.execute(InsertDetailsQuery, (hgcRecDte,hgcCountry,hgcCity,hgcSuburb,hgcNoOfRooms,hgcEntryNo,hgcContactNo,rawRS))                    

                    st.toast(f"Entry number {hgcEntryNo} inserted successfully.")                            

                    # persist the changes to database by calling cnnOne.commit() 

                    cnnOne.commit()

                    # close the connection

                    cnnOne.close()

                except sqlite3.Error as ex:

                    sqlstate = ex.args[0]

                    st.warning(f"Error inserting new record: {sqlstate}.")

                finally:

                    # Close the connection

                    if cnnOne:

                        cnnOne.close()

            else:

                st.warning("Please enter data in every data field.")

    st.button("Submit", on_click =  InsertAccommoWanted)

def ViewAvailableAccommodation_page():

    st.header("Accommodation Offers Enquiry Page")

    st.write("VIEW POSTS OF ACCOMMODATION AVAILABLE IN THE AREA YOU WISH TO STAY")

    st.write("Enter Details Of The Accommodation You Are Looking For and Click The View Button")

    st.write("NB: After entering data in each field (including the DATE), press ENTER/TAB to apply. If the date is already entered, begin by clicking within the DATE field and exiting it through the TAB to apply the date.")

    # FOR CLEARING DATA FIELDS

    # Initialize session state for the input if it doesn't exist        

    if "dtaCountry" not in st.session_state:

        st.session_state["dtaCountry"] = ""

    if "dtaCity" not in st.session_state:

        st.session_state["dtaCity"] = ""

    if "dtaSuburb" not in st.session_state:

        st.session_state["dtaSuburb"] = ""

    if "dtaNoOfRooms" not in st.session_state:

        st.session_state["dtaNoOfRooms"] = ""

    # Use st.markdown to inject custom CSS

    st.markdown("""

    <style>

    .stTextInput input {text-transform: uppercase;

    }

    </style>

    """, unsafe_allow_html = True)

    lldCountry = st.text_input("Enter the COUNTRY in which the accommodation is available.", key = "dtaCountry", on_change = None)

    lldCity = st.text_input("Enter the CITY/TOWN", key = "dtaCity", on_change = None)

    lldSuburb = st.text_input("Enter the SUBURB in which the accommodation is available.", key = "dtaSuburb", on_change = None)

    # VIEW LANDLORDS OFFERS

    def viewLandlordsOffers():

        cnnOne = sqlite3.connect("ATFDb.db")

        cursor = cnnOne.cursor()

        lldRS = 'Lld' 

        st.write("RECORDS OF ACCOMMODATION ON OFFER")

        upcaSuburd = lldSuburb.upper()

        upcaCity = lldCity.upper()

        upcaCountry = lldCountry.upper()

        st.write(f"in {upcaSuburd}, {upcaCity}, {upcaCountry}")

        st.write(f"as at {formatted_curdate}")    

        df = cursor.execute("SELECT RecDte,NoOfRooms,Rent,ContactNo FROM AccommoRecs WHERE RS = ? and  Country COLLATE NONCASE LIKE ? and City COLLATE NONCASE LIKE ? and Suburb COLLATE NONCASE LIKE ?", (lldRS,lldCountry,lldCity,lldSuburb,))  # and NoOfRooms = ?  lldNoOfRooms, 

        st.dataframe(df)

    st.button("View", on_click =  viewLandlordsOffers)

def ViewWantedAccommodation_page():

    st.header("Wanted Accommodation Enquiry Page")

    st.write("VIEW POSTS OF PEOPLE LOOKING FOR ACCOMMODATION IN THE AREAS WHERE YOU ARE OFFERING ACCOMMODATION")

    st.write("Enter Details Of The Accommodation You Are Looking For and Click The View Button")

    st.write("NB: After entering data in each field (including the DATE), press ENTER/TAB to apply. If the date is already entered, begin by clicking within the DATE field and exiting it through the TAB to apply the date.")

    # FOR CLEARING DATA FIELDS

    # Initialize session state for the input if it doesn't exist  

    if "dtaCountry" not in st.session_state:

        st.session_state["dtaCountry"] = ""

    if "dtaCity" not in st.session_state:

        st.session_state["dtaCity"] = ""

    if "dtaSuburb" not in st.session_state:

        st.session_state["dtaSuburb"] = ""

    if "dtaNoOfRooms" not in st.session_state:

        st.session_state["dtaNoOfRooms"] = ""        

    # Use st.markdown to inject custom CSS

    st.markdown("""

    <style>

    .stTextInput input {text-transform: uppercase;

    }

    </style>

    """, unsafe_allow_html = True)

    tntCountry = st.text_input("Enter the COUNTRY in which accommodation is sought.", key = "dtaCountry", on_change = None)

    tntCity = st.text_input("Enter the CITY/TOWN", key = "dtaCity", on_change = None)

    tntSuburb = st.text_input("Enter the SUBURB where they intend to stay.", key = "dtaSuburb", on_change = None)

    # VIEW SEARCHES BY TENANTS

    def viewSearchesByTenants():

        cnnOne = sqlite3.connect("ATFDb.db")

        cursor = cnnOne.cursor()

        tntRS = 'Tnt' 

        st.write("RECORDS OF SEARCHES FOR ACCOMMODATION")

        uppSuburd = tntSuburb.upper()

        uppCity = tntCity.upper()

        uppCountry = tntCountry.upper()

        st.write(f"in {uppSuburd}, {uppCity}, {uppCountry}")

        st.write(f"as at {formatted_curdate}")    

        df = cursor.execute("SELECT RecDte,NoOfRooms,ContactNo FROM AccommoRecs WHERE RS = ? and  Country COLLATE NONCASE LIKE ? and City COLLATE NONCASE LIKE ? and Suburb COLLATE NONCASE LIKE ?", (tntRS,tntCountry,tntCity,tntSuburb,))  

        st.dataframe(df)

    st.button("View", on_click =  viewSearchesByTenants)

# ---Siderbar Navigation ---

# Use 'with st.sidebar:' to place widgets in the siderbar

with st.sidebar:

    st.title("App Pages Panel")

    page_options = ["Home Page", "Enter Details Of Accommodation You Want To Rent Out", "Enter Details Of Accommodation Wanted", "View Posts Of Accommodation Available In:","View Posts Of Searches For Accommodation In:"]

    # Create the radio buttons

    selected_page = st.radio("Go to", page_options)

# --- Main Content Area ( Conditional Logic) ---

if selected_page == "Home Page":

    home_page()

elif selected_page == "Enter Details Of Accommodation You Want To Rent Out":

    EnterAvailableAccommodation_page()

elif selected_page == "Enter Details Of Accommodation Wanted":

    EnterWantedAccommodation_page()

elif selected_page == "View Posts Of Accommodation Available In:":

    ViewAvailableAccommodation_page()

elif selected_page == "View Posts Of Searches For Accommodation In:":

    ViewWantedAccommodation_page()

# VIEW ACCOMMODATION WANTED

def accommodationWanted():

    cnnOne = sqlite3.connect(ATFDb.db)        

    query = f"SELECT RecDte,Country,City,Suburb,NoOfRooms,ContactNo FROM AccommoRecs WHERE RS = 'Tnt'"  # and  Country == {TntCountry} and City == {TntCity} and Suburb == {TntSuburb} and NoOfRooms == {TntNoOfRooms} "

    # Use pandas to read the SQL query directly into DataFrame

    df = pd.read_sql_query(query, cnnOne)

    cnnOne.Close()

    return df

def viewAccommodationWanted(): 

    # Get the landlord's filtered offers

    accommodationWanted_df = accommodationWanted()

    # initialize database

    init_db()

    # Display the offers using st.dataframe

    if not accommodationWanted_df.empty:

        st.write(f"Details of Accommodation Wanted By Tenants in {lldSuburb}, {lldCity}, {lldCountry}")

        st.dataframe(accommodationWanted_df) # Ue st.dataframe for an interactive table

    else:

        st.info("No searches for accommodation in the specified area")

if selected_page == "Enter Details Of Accommodation You Want To Rent Out" or selected_page == "Enter Details Of Accommodation Wanted" or selected_page == "View Posts Of Accommodation Available In:" or selected_page == "View Posts Of Searches For Accommodation In:":

    st.button("Clear Data Fields", on_click = clearFormFields)
