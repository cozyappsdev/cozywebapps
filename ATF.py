import streamlit as st
import psycopg2
import sqlalchemy
import pandas as pd
import os
from datetime import datetime, date
import time
import toml
#from sqlalchemy import create_engine

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

cnnOne = None
cursor = None

try:
    # Load the secrets from the secrets.toml file
    secrets_path = os.path.abspath('.streamlit/secrets.toml')
    st.secrets = toml.load(secrets_path)       

    cnnOne = psycopg2.connect(
        host = st.secrets["database"]["host"],
        dbname = st.secrets["database"]["database"],
        user = st.secrets["database"]["username"],
        password = st.secrets["database"]["password"],
        port = st.secrets["database"]["port"]
        )    

    cursor = cnnOne.cursor()

    # Create table
    create_table_query = """

        CREATE TABLE IF NOT EXISTS AccommoRecs (

            RecID SERIAL PRIMARY KEY,

            RecDte varchar(25),       

            Country varchar(25) NOT NULL,

            City varchar(25) NOT NULL,        

            Suburb varchar(25) NOT NULL,

            NoOfRooms varchar(5) NOT NULL,

            Rent varchar(10) NULL,        

            EntryNo varchar(25) NOT NULL,        

            ContactNo varchar(20) NOT NULL,

            RS varchar(5) NOT NULL

            );
            """
    cursor.execute(create_table_query)

    cnnOne.commit()
    # st.write("Table 'AccommoRecs' created successfully")
    
except Exception as error:
    print(error)
finally:
    if cursor is not None:
     cursor.close()
    if cnnOne is not None:
     cnnOne.close()

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

    def InsertAccommoToRentOut():    

        NumberOfAccs = 0

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

        cnnOne = None

        cursor = None

        # CHECK PRESENCE OF RECORD BY COUNTING RECORD'S ID

        try:
            # Load the secrets from the secrets.toml file
            secrets_path = os.path.abspath('.streamlit/secrets.toml')
            st.secrets = toml.load(secrets_path)       

            cnnOne = psycopg2.connect(
                host = st.secrets["database"]["host"],
                dbname = st.secrets["database"]["database"],
                user = st.secrets["database"]["username"],
                password = st.secrets["database"]["password"],
                port = st.secrets["database"]["port"]
                )    

            cursor = cnnOne.cursor()       

            RowsQuery="SELECT COUNT(*) FROM AccommoRecs WHERE EntryNo = %s"       

            cursor.execute(RowsQuery, (upcEntryNo,))           

            # Collect result of count

            NumberOfAccs=cursor.fetchone()[0]

        except Exception as e:
            with st.sidebar:
                placeholder = st.empty()
                with placeholder:            
                    placeholder.warning(f"An error occurred: {e}")
                    time.sleep(6)
                    placeholder = st.empty()

        finally:

            if cursor is not None:

                cursor.close()

            if cnnOne is not None:

                cnnOne.close()
                

        if NumberOfAccs > 0:
            with st.sidebar:
                placeholder = st.empty()
                with placeholder:
                    placeholder.warning(f"{upcEntryNo} is not available. Please create a different entry number and try again.")
                    time.sleep(3)
                    placeholder =st.empty()

        else:

            #if upcRecDte and upcCountry and upcCity and upcSuburb and upcNoOfRooms and upcRent and upcEntryNo and upcContactNo:

            cnnOne = None

            cursor = None            

            try:
                # Load the secrets from the secrets.toml file
                secrets_path = os.path.abspath('.streamlit/secrets.toml')
                st.secrets = toml.load(secrets_path)       

                cnnOne = psycopg2.connect(
                    host = st.secrets["database"]["host"],
                    dbname = st.secrets["database"]["database"],
                    user = st.secrets["database"]["username"],
                    password = st.secrets["database"]["password"],
                    port = st.secrets["database"]["port"]
                    )    

                cursor = cnnOne.cursor()
                
                InsertDetailsQuery = "INSERT INTO AccommoRecs (RecDte,Country,City,Suburb,NoOfRooms,Rent,EntryNo,ContactNo,RS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"                    

                cursor.execute(InsertDetailsQuery, (upcRecDte,upcCountry,upcCity,upcSuburb,upcNoOfRooms,upcRent,upcEntryNo,upcContactNo,dtaRS))

                # Confirm success 
                                    
                ######st.toast(f"Entry number {upcEntryNo} inserted successfully.")                   

                # persist the changes to database by calling cnnOne.commit() 

                cnnOne.commit()
                
            except Exception as ex:

                sqlstate = ex.args[0]
                with st.sidebar:
                    placeholder = st.empty()
                    with placeholder:
                        placeholder.warning(f"Error inserting new record: {sqlstate}.")
                        time.sleep(6)
                        placeholder =st.empty()

            finally:

                # Close the connection

                if cursor is not None:

                    cursor.close()

                if cnnOne is not None:

                    cnnOne.close()
                    
            #else:

                #st.warning("Please enter data in every data field.")

    #st.button("Submit", on_click =  InsertAccommoToRentOut)
    if st.sidebar.button('SUBMIT ENTRY'):
        # Convert all text in python variables to uppercase
        upcRecDte = dtaRecDte.upper()
        upcCountry = dtaCountry.upper()
        upcCity = dtaCity.upper()
        upcSuburb = dtaSuburb.upper()
        upcNoOfRooms = dtaNoOfRooms.upper()
        upcRent = dtaRent.upper()
        upcEntryNo = dtaEntryNo.upper()
        upcContactNo = dtaContactNo
        if upcRecDte and upcCountry and upcCity and upcSuburb and upcNoOfRooms and upcRent and upcEntryNo and upcContactNo:
            InsertAccommoToRentOut()
           
            with st.sidebar:

                placeholder = st.empty()            
                with placeholder:                   
                    placeholder.success("Record inserted successfully!")
                    time.sleep(3)
                    placeholder = st.empty()
                    
        else:
            with st.sidebar:
                placeholder = st.empty()
                with placeholder:
                    placeholder.warning("Please enter data in every data field.")
                    time.sleep(3)
                    placeholder = st.empty      
    
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

        NumberOfAccs = 0

        # Convert all text in python variables to uppercase

        hgcRecDte = rawRecDte.upper()

        hgcCountry = rawCountry.upper() 

        hgcCity = rawCity.upper()

        hgcSuburb = rawSuburb.upper()

        hgcNoOfRooms = rawNoOfRooms.upper()   

        hgcEntryNo = rawEntryNo.upper()

        hgcContactNo = rawContactNo

        rawRS = 'Tnt' 

        cursor = None 

        cnnOne = None   

        # CHECK PRESENCE OF RECORD BY COUNTING RECORD'S ID

        try:               

            # Load the secrets from the secrets.toml file
            secrets_path = os.path.abspath('.streamlit/secrets.toml')
            st.secrets = toml.load(secrets_path)       

            cnnOne = psycopg2.connect(
                host = st.secrets["database"]["host"],
                dbname = st.secrets["database"]["database"],
                user = st.secrets["database"]["username"],
                password = st.secrets["database"]["password"],
                port = st.secrets["database"]["port"]
                )    

            cursor = cnnOne.cursor()       

            RowsQuery="SELECT COUNT(*) FROM AccommoRecs WHERE EntryNo = %s"       

            cursor.execute(RowsQuery, (hgcEntryNo,))           

            # Collect result of count

            NumberOfAccs=cursor.fetchone()[0]

        except Exception as e:

            st.warning(f"An error occurred: {e}")

        finally:

            if cursor is not None:

                cursor.close()

            if cnnOne is not None:

                cnnOne.close()                

        if NumberOfAccs > 0:
            with st.sidebar:
                placeholder = st.empty()
                with placeholder:
                    placeholder.warning(f"{ hgcEntryNo} is not available. Please create a different entry number and try again.")
                    time.sleep(3)
                    placeholder = st.empty()

        else:

            #if hgcRecDte and hgcCountry and hgcCity and hgcSuburb and hgcNoOfRooms and hgcEntryNo and hgcContactNo:

            cursor = None

            cnnOne = None            

            try:
               # Load the secrets from the secrets.toml file
                secrets_path = os.path.abspath('.streamlit/secrets.toml')
                st.secrets = toml.load(secrets_path)       

                cnnOne = psycopg2.connect(
                    host = st.secrets["database"]["host"],
                    dbname = st.secrets["database"]["database"],
                    user = st.secrets["database"]["username"],
                    password = st.secrets["database"]["password"],
                    port = st.secrets["database"]["port"]
                    )    

                cursor = cnnOne.cursor()

                InsertDetailsQuery = "INSERT INTO AccommoRecs (RecDte,Country,City,Suburb,NoOfRooms,EntryNo,ContactNo,RS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                
                cursor.execute(InsertDetailsQuery, (hgcRecDte,hgcCountry,hgcCity,hgcSuburb,hgcNoOfRooms,hgcEntryNo,hgcContactNo,rawRS))                    

                #st.toast(f"Entry number {hgcEntryNo} inserted successfully.")                            

                # persist the changes to database by calling cnnOne.commit() 

                cnnOne.commit()
                
            except Exception as ex:

                sqlstate = ex.args[0]
                with st.sidebar:
                    placeholder = st.empty()
                    with placeholder:
                        placeholder.warning(f"Error inserting new record: {sqlstate}.")
                        time.sleep(6)
                        placeholder = st.empty()

            finally:

                # Close the connection

                if cursor is not None:

                    cursor.close()

                if cnnOne is not None:

                    cnnOne.close()

            #else:

                #st.warning("Please enter data in every data field.")

    #st.button("Submit", on_click =  InsertAccommoWanted)
    if st.sidebar.button('SUBMIT ENTRY'):
        # Convert all text in python variables to uppercase
        hgcRecDte = rawRecDte.upper()
        hgcCountry = rawCountry.upper()
        hgcCity = rawCity.upper()
        hgcSuburb = rawSuburb.upper()
        hgcNoOfRooms = rawNoOfRooms.upper()       
        hgcEntryNo = rawEntryNo.upper()
        hgcContactNo = rawContactNo
        if hgcRecDte and hgcCountry and hgcCity and hgcSuburb and hgcNoOfRooms and hgcEntryNo and hgcContactNo:
            InsertAccommoWanted()            
            with st.sidebar:
                placeholder = st.empty() 
                with placeholder:                   
                    placeholder.success("Record inserted successfully!")
                    time.sleep(3)
                    placeholder = st.empty()
        else:
            st.sidebar.warning("Please enter data in every data field.")

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

    def viewLandlordsOffers(): # cursor_factory=psycopg2.extras.DictCursor):
        
        # Load the secrets from the secrets.toml file
        secrets_path = os.path.abspath('.streamlit/secrets.toml')
        st.secrets = toml.load(secrets_path)       

        cnnOne = psycopg2.connect(
            host = st.secrets["database"]["host"],
            dbname = st.secrets["database"]["database"],
            user = st.secrets["database"]["username"],
            password = st.secrets["database"]["password"],
            port = st.secrets["database"]["port"]
            )        

        # Prepare the cursor
        cursor = cnnOne.cursor()        
        
        # Prepare criteria values        
        lldRS = 'Lld'
        upcaSuburd = lldSuburb.upper()
        upcaCity = lldCity.upper()
        upcaCountry = lldCountry.upper()

        # Report header        
        st.write("RECORDS OF ACCOMMODATION ON OFFER") 

        st.write(f"in {upcaSuburd}, {upcaCity}, {upcaCountry}")

        st.write(f"as at {formatted_curdate}")  

        # Define the Query with 4 criteria
        query = "SELECT recdte,noofrooms,rent,contactno FROM AccommoRecs WHERE RS = %s and Country = %s and City = %s and Suburb = %s"
        # Provide criteria values
        params = (lldRS,upcaCountry,upcaCity,upcaSuburd) 
        # Execute the query
        cursor.execute(query, params)
        # collect all the matching records
        records = cursor.fetchall()

        # initialize an empty list to store records
        data = []

        # Populate the list using a for loop
        for record in records: 
            data.append({
                'Date_Posted': record[0],
                'No_of_Rooms_Available': record[1],
                'Rent/Month': record[2],
                'Bus_Contact_No': record[3]
                 })  
            
        # Create a DataFrame from the list
        df = pd.DataFrame(data)

        # Display the DataFrame in Streamlit
        st.dataframe(df)       
        
    #st.button("View", on_click =  viewLandlordsOffers)
    if st.sidebar.button("VIEW PROVIDERS POSTS"):      

        #lldRS = 'Lld'
        upcaSuburd = lldSuburb.upper()
        upcaCity = lldCity.upper()
        upcaCountry = lldCountry.upper()

        if lldCountry and lldCity and lldSuburb:
            viewLandlordsOffers()  #  (cursor_factory=psycopg2.extras.DictCursor)
            with st.sidebar:
                placeholder = st.empty()
                with placeholder:
                    placeholder.success("Check the records below the form!")
                    time.sleep(3)
                    placeholder = st.empty()
        else:
            st.warning("Please enter data in every data field.")

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

        # Load the secrets from the secrets.toml file
        secrets_path = os.path.abspath('.streamlit/secrets.toml')
        st.secrets = toml.load(secrets_path)       

        cnnOne = psycopg2.connect(
            host = st.secrets["database"]["host"],
            dbname = st.secrets["database"]["database"],
            user = st.secrets["database"]["username"],
            password = st.secrets["database"]["password"],
            port = st.secrets["database"]["port"]
            )
                
        # Prepare the cursor
        cursor = cnnOne.cursor()        

        # Prepare criteria values
        tntRS = 'Tnt' 
        uppSuburd = tntSuburb.upper()
        uppCity = tntCity.upper()
        uppCountry = tntCountry.upper()

        # Report header
        st.write("RECORDS OF SEARCHES FOR ACCOMMODATION")

        st.write(f"in {uppSuburd}, {uppCity}, {uppCountry}")

        st.write(f"as at {formatted_curdate}")    

        # Define the Query with 4 criteria
        query = "SELECT RecDte,NoOfRooms,ContactNo FROM AccommoRecs WHERE RS = %s AND Country = %s AND City = %s AND Suburb = %s"  
        # Provide criteria values
        params = (tntRS,uppCountry,uppCity,uppSuburd) 
        # Execute the query
        cursor.execute(query, params)
        # collect all the matching records
        records = cursor.fetchall()

        # initialize an empty list to store records
        data = []

        # Populate the list using a for loop
        for record in records: 
            data.append({
                'Date_Posted': record[0],
                'No_of_Rooms_Wanted': record[1],                
                'Bus_Contact_No': record[2]
                 })  
            
        # Create a DataFrame from the list
        df = pd.DataFrame(data)

        # Display the DataFrame in Streamlit
        st.dataframe(df)

    #st.button("View", on_click =  viewSearchesByTenants)
    if st.sidebar.button("VIEW SEEKERS POSTS"):      

        #lldRS = 'Tnt'
        uppSuburb = tntSuburb.upper()
        uppCity = tntCity.upper()
        uppCountry = tntCountry.upper()

        if uppCountry and uppCity and uppSuburb:
            viewSearchesByTenants()  #  (cursor_factory=psycopg2.extras.DictCursor)
            with st.sidebar:
                placeholder = st.empty()
                with placeholder:
                    placeholder.success("Check report below the form!")
                    time.sleep(3)
                    placeholder = st.empty()
        else:
            with st.sidebar:
                placeholder = st.empty()
                with placeholder:
                    placeholder.warning("Please enter data in every data field.")
                    time.sleep(3)
                    placeholder = st.empty()

def DeleteEntries_page():

    st.header("Delete Entries Page")

    st.write("DELETE YOUR POSTS THAT HAVE EXPIRED")

    st.write("Enter The UNIQUE REF of the Entry You Want to Delete and then Click the DELETE ENTRY Button")

    st.write("NB: After entering your ENTRY REF NUMBER, press ENTER/TAB to apply.")

    # FOR CLEARING DATA FIELDS

    # Initialize session state for the input if it doesn't exist 
    if "dtaEntryNo" not in st.session_state:

        st.session_state["dtaEntryNo"] = ""             

    # Use st.markdown to inject custom CSS

    st.markdown("""

    <style>

    .stTextInput input {text-transform: uppercase;

    }

    </style>

    """, unsafe_allow_html = True)    

    delEntryNo = st.text_input("Enter the ENTRY REF NUMBER of the Entry You Want to Delete.", key = "dtaEntryNo", on_change = None)

    # VIEW SEARCHES BY TENANTS

    def DeleteEntry():

        try:

            # Load the secrets from the secrets.toml file
            secrets_path = os.path.abspath('.streamlit/secrets.toml')
            st.secrets = toml.load(secrets_path)       

            cnnOne = psycopg2.connect(
                host = st.secrets["database"]["host"],
                dbname = st.secrets["database"]["database"],
                user = st.secrets["database"]["username"],
                password = st.secrets["database"]["password"],
                port = st.secrets["database"]["port"]
                )    

            cursor = cnnOne.cursor()      

            # Prepare criteria values            
            capEntryNo = delEntryNo.upper()

            # check presence of EntryNo
            
            RowsQuery="SELECT COUNT(*) FROM AccommoRecs WHERE EntryNo = %s"       

            cursor.execute(RowsQuery, (capEntryNo,))           

            # Collect result of count

            itemfrequency=cursor.fetchone()[0]

            if itemfrequency > 0:
                # Define the Query with 4 criteria
                query = "DELETE FROM AccommoRecs WHERE EntryNo = %s"  
                # Provide criteria values
                params = (capEntryNo,) 
                # Execute the query
                cursor.execute(query, params)                
                # Commit the changes to the database
                cnnOne.commit()
                with st.sidebar:
                    placeholder = st.empty()
                    with placeholder:
                        placeholder.success(f"Entry {capEntryNo} sucessfully deleted!")
                        time.sleep(3)
                        placeholder = st.empty()

            else:
                with st.sidebar:
                    placeholder = st.empty()
                    with placeholder:
                        placeholder.warning(f"Entry Ref Number {capEntryNo} not found!")
                        time.sleep(3)
                        placeholder = st.empty()                    
                
        except Exception as ex:

            sqlstate = ex.args[0]
            with st.sidebar:
                placeholder = st.empty()
                with placeholder:
                    placeholder.warning(f"Error deleting record: {sqlstate}.")
                    time.sleep(6)
                    placeholder = st.empty()  

        finally:

            # Close the connection

            if cursor is not None:

                cursor.close()

            if cnnOne is not None:

                cnnOne.close()        
               
    #st.button("View", on_click =  viewSearchesByTenants)
    if st.sidebar.button("DELETE ENTRY"):
        #lldRS = 'Tnt'
        capEntryNo = delEntryNo.upper() 
        #if capEntryNo:
        DeleteEntry()  #  (cursor_factory=psycopg2.extras.DictCursor)
           

# ---Siderbar Navigation ---

# Use 'with st.sidebar:' to place widgets in the siderbar

with st.sidebar:

    st.title("App Pages Panel")

    page_options = ["Home Page", "Enter Details Of Accommodation You Want To Rent Out", "Enter Details Of Accommodation Wanted", "View Posts Of Accommodation Available In:","View Posts Of Searches For Accommodation In:","Delete Entries"]

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

elif selected_page == "Delete Entries":

    DeleteEntries_page()

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
        with st.sidebar:
            placeholder = st.empty()
            with placeholder:
                placeholder.info("No searches for accommodation in the specified area")
                time.sleep(5)
                placeholder = st.empty()

if selected_page == "Enter Details Of Accommodation You Want To Rent Out" or selected_page == "Enter Details Of Accommodation Wanted" or selected_page == "View Posts Of Accommodation Available In:" or selected_page == "View Posts Of Searches For Accommodation In:" or selected_page == "Delete Entries":    
    with st.sidebar:
        st.button("CLEAR DATA FIELDS", on_click = clearFormFields)

#if st.sidebar.button('DELETE ENTRY'):
    # Your code to delete the entry goes here
    #st.sidebar.success("Record deleted successfully!")