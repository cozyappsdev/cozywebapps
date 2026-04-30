import streamlit as st
import pg8000.native
from datetime import datetime, date
import pandas as pd


# Autofill Date Field
current_date = datetime.now()
# Format date as string
formatted_curdate = current_date.strftime("%d/%m/%Y  %H:%M:%S")

# 0. Setup Connection (Optimized with cache_resource)
@st.cache_resource
def get_connection():
    # Replace with your actual Aiven connection details
    return pg8000.native.Connection(
        user = st.secrets["postgres"]["user"],
        password = st.secrets["postgres"]["password"],
        host = st.secrets["postgres"]["host"],
        port = st.secrets["postgres"]["port"],
        database = st.secrets["postgres"]["database"],
        ssl_context = True  
    )

db = get_connection()

# --- Performance Optimized Data Retrieval ---
@st.cache_data(ttl=600)
def get_Lld_posts():
    return db.run("SELECT RecDte,Country,City,Suburb,NoOfRooms,Rent,ContactNo FROM AccommoRecs WHERE Country = :cntry and City = :cty and Suburb = :sbb and RS = :rs", cntry=cntry_txt, cty=cty_txt,sbb=sbb_txt,rs=RS) # vacant spaces

@st.cache_data(ttl=600)
def get_Tnt_posts():
    return db.run("SELECT RecDte,Country,City,Suburb,NoOfRooms,ContactNo FROM AccommoRecs WHERE Country = :cntryi and City = :ctyi and Suburb = :sbbi and RS = :rsi", cntryi=Country_txt, ctyi=City_txt,sbbi=Suburb_txt,rsi=RS)  # wanted spaces

@st.cache_data(ttl=600)
def count_males():
    result = db.run("SELECT COUNT(*) FROM AccommoRecs WHERE RS = 'ws' or RS = 'vs'")
    return result[0][0]

@st.cache_data(ttl=600)
def count_ref_no():
    result = db.run("SELECT COUNT(*) FROM AccommoRecs WHERE EntryNo = :refidno", refidno=EntryNo)
    return result[0][0]   

st.title("Accommodation Market")

# 1. Create Table
db.run("""
    CREATE TABLE IF NOT EXISTS AccommoRecs (

            RecID SERIAL PRIMARY KEY,

            RecDte varchar(25),       

            Country varchar(25) NOT NULL,

            City varchar(25) NOT NULL,        

            Suburb varchar(25) NOT NULL,

            NoOfRooms varchar(5) NOT NULL,

            Rent varchar(10) NULL,        

            EntryNo varchar(25) NOT NULL UNIQUE,       

            ContactNo varchar(20) NOT NULL,

            RS varchar(5) NOT NULL

            )
            """)

Tsk = st.selectbox("Task", ["Click on Down Arrow to Select a Task","Enter Details Of Accommodation You Want To Rent Out", "Enter Details Of Accommodation You Are Looking For","View Posts Of Accommodation Available In Areas Where You Are Looking For Accommodation","View Posts Of Searches For Accommodation In Neighbourhoods Where You Need Tenants","Delete Your Posts"])
is_expanded = (Tsk == "Enter Details Of Accommodation You Want To Rent Out" or Tsk == "Enter Details Of Accommodation You Are Looking For" or Tsk == "View Posts Of Accommodation Available In Areas Where You Are Looking For Accommodation" or Tsk == "View Posts Of Searches For Accommodation In Neighbourhoods Of Your Choice" or Tsk == "Delete Your Posts")
# 3. Insert New Records
with st.expander("", expanded=is_expanded):    
    with st.form("Add_a_Post"):
        if Tsk == "Enter Details Of Accommodation You Want To Rent Out":            
            RecDte = st.text_input("Date",value=formatted_curdate)       
            Country = st.text_input("Country")  
            City = st.text_input("City")
            Suburb = st.text_input("Suburb")
            NoOfRooms = st.text_input("Number of Rooms")
            Rent = st.text_input("Monthly Rent in your currency e.g. ZWD250.00/$250.00")
            EntryNo = st.text_input("Create and enter a UNIQUE IDENTIFIER for the post.")
            ContactNo = st.text_input("Business Contact Number")             
            RS=""          
            if st.form_submit_button("Submit"):
                refid_count = count_ref_no()
                if refid_count > 0:
                    st.toast(f"Unique Identifier {EntryNo} is not available. Please create a different entry idenifier and try again.")
                else:
                    if RecDte =="" or Country =="" or City == "" or Suburb == "" or NoOfRooms == "" or Rent == "" or EntryNo == "" or ContactNo == "":
                        st.error("Enter data in all the data fields.")
                    else:
                        if Tsk == "Enter Details Of Accommodation You Want To Rent Out":
                            RS='vs'
                        elif Tsk == "Enter Details Of Accommodation You Are Looking For":
                            RS='ws'
                        db.run("INSERT INTO AccommoRecs (RecDte,Country,City,Suburb,NoOfRooms,Rent,EntryNo,ContactNo,RS) VALUES (:rdte, :cntry, :cty, :sbb, :rms, :rnt, :entno, :cctno, :rs)", 
                            rdte=RecDte, cntry=Country, cty=City, sbb=Suburb, rms=NoOfRooms, rnt=Rent, entno=EntryNo, cctno=ContactNo, rs=RS)                        
                        st.cache_data.clear() # Reset cache to show updated data
                        st.toast("Record successfully inserted.")

        elif Tsk == "Enter Details Of Accommodation You Are Looking For":        
            RecDte = st.text_input("Date", value=formatted_curdate)       
            Country = st.text_input("Country")
            City = st.text_input("City")
            Suburb = st.text_input("Suburb")
            NoOfRooms = st.text_input("Number of Rooms")           
            EntryNo = st.text_input("Create and enter a UNIQUE IDENTIFIER for the post.")
            ContactNo = st.text_input("Business Contact Number") 
            RS=""           
            if st.form_submit_button("Submit"):               
                refid_count = count_ref_no()
                if refid_count > 0:
                    st.toast(f"Unique Identifier {EntryNo} is not available. Please create a different entry idenifier and try again.")
                else:
                    if RecDte =="" or Country =="" or City == "" or Suburb == "" or NoOfRooms == "" or EntryNo == "":
                        st.error("Enter data in all the data fields.")
                    else:
                        if Tsk == "Enter Details Of Accommodation You Want To Rent Out":
                            RS='vs'
                        elif Tsk == "Enter Details Of Accommodation You Are Looking For":
                            RS='ws'
                        db.run("INSERT INTO AccommoRecs (RecDte,Country,City,Suburb,NoOfRooms,EntryNo,ContactNo,RS) VALUES (:rdte, :cntry, :cty, :sbb, :noofrms, :entno, :cctno, :rs)", 
                            rdte=RecDte, cntry=Country, cty=City, sbb=Suburb, noofrms=NoOfRooms,entno=EntryNo, cctno=ContactNo, rs=RS)                        
                        st.cache_data.clear() # Reset cache to show updated data
                        st.toast("Record successfully inserted.")    

if Tsk == "View Posts Of Accommodation Available In Areas Where You Are Looking For Accommodation":         
    cntry_txt = st.text_input("Enter COUNTRY name")
    cty_txt = st.text_input("Enter CITY name")
    sbb_txt = st.text_input("Enter SUBURB name") 
    RS=""                      
    RS = "vs" # vacant spaces
    if st.button("View Available Accommodation"):

        llds_posts = get_Lld_posts()

        lcation=''
        twn=''
        stat=''

        if llds_posts:         

            # initialize an empty list to store records
            llds_data = []

            # Populate the list using a for loop
            for llds_post in llds_posts: 
                llds_data.append({
                    'Date_Posted': llds_post[0],
                    'Rooms_Available': llds_post[4],
                    'Montly_Rent_Amt': llds_post[5],              
                    'Bus_Contact_No': llds_post[6]
                    })
            st.write("")
            st.write(f"DETAILS OF ACCOMMODATION AVAILABLE")
            lcation=sbb_txt.upper()
            twn=cty_txt.upper()
            stat=cntry_txt.upper()
            st.write(f"in {lcation}, {twn}, {stat}")  
                
            # Create a DataFrame from the list
            llds_df = pd.DataFrame(llds_data)

            # Display the DataFrame in Streamlit
            st.dataframe(llds_df)                      

        else:
           
            st.toast(f"No posts of vacant accommodation in {lcation}, {twn}, {stat}")
        
elif Tsk == "View Posts Of Searches For Accommodation In Neighbourhoods Where You Need Tenants":           
    Country_txt = st.text_input("Country")
    City_txt = st.text_input("City")
    Suburb_txt = st.text_input("Suburb")                   
    RS=""                      
    RS = "ws"  # wanted spaces
    if st.button("View Searches for Accommodation"):

        tnts_posts = get_Tnt_posts()

        location=''
        town=''
        state=''

        if tnts_posts:         

            # initialize an empty list to store records
            tnts_data = []

            # Populate the list using a for loop
            for tnts_post in tnts_posts: 
                tnts_data.append({
                    'Date_Posted': tnts_post[0],
                    'No_of_Rooms_Wanted': tnts_post[4],                
                    'Bus_Contact_No': tnts_post[5]
                    })
            st.write("")
            st.write(f"DETAILS OF ACCOMMODATION WANTED BY TENANTS")
            location=Suburb_txt.upper()
            town=City_txt.upper()
            state=Country_txt.upper()
            st.write(f"in {location}, {town}, {state}")  
                
            # Create a DataFrame from the list
            tnts_df = pd.DataFrame(tnts_data)

            # Display the DataFrame in Streamlit
            st.dataframe(tnts_df)

        else:
           
            st.toast(f"No searches for accommodation in {location}, {town}, {state}")

elif  Tsk == "Delete Your Posts":                
        EntryNo = st.text_input("Enter UNIQUE IDENTIFIER of post you want to delete")                              
        if st.button("Delete Post"):                
            if EntryNo =="":
                st.error("Enter the UNIQUE IDENTIFIER of the post you want to delete.")
            else:
                refid_count = count_ref_no()
                if refid_count < 1:
                    st.toast(f"Unique Identifier {EntryNo} not found.")
                else:                        
                    db.run("DELETE FROM AccommoRecs WHERE EntryNo = :pri", pri=EntryNo)                                               
                    st.cache_data.clear() # Reset cache to show updated data
                    st.toast(f"Post with Unique Identifier {EntryNo} successfully deleted!")

if st.sidebar:
    st.sidebar.subheader("Welcome")    
    st.sidebar.write("1. Click on the 'Task' selection box (on right pane) to navigate through app.")    
    st.sidebar.write("2. Press Enter/Tab after entering data to apply.")
    st.sidebar.write("3. Very IMPORTANT:")
    st.sidebar.write("   Keep all your post's UNIQUE IDENTIFIERS in a safe place: You will need them when it's time to delete the posts.")
    
