import streamlit as st
import pg8000.native
from pg8000.exceptions import InterfaceError, DatabaseError
from datetime import datetime, date
import pandas as pd
import toml
import time

# Autofill Date Field
current_date = datetime.now()
# Format date as string
formatted_curdate = current_date.strftime("%d/%m/%Y  %H:%M:%S")

# __CONNECTION START__

# Define the cached resourc function
@st.cache_resource
def get_db_connection(TrSwpsDb):             
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Retrieve credentials from streamlit secrets
    creds = st.secrets["TrSwps_db"]
    # 2. Establish connection to database for this app in Aiven instance
    return pg8000.native.Connection(
        host = creds["host"],  
        database = creds["database"],  
        user = creds["user"], 
        password = creds["password"], 
        port = creds["port"], 
        ssl_context = True   # Important for Aiven
    )    
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
try:
    cnnOne = get_db_connection("TrSwpsDb")
except ConnectionError:
    st.error("ConnectingError: Couldn't establish a connectionto the database server. Please check your internet connection and that the server is running.")
except InterfaceError:
    st.error("InterfaceError: There's a problem with the database: this often occurs when the connection is closed or not established properly.")
except DatabaseError as e:
    st.error(f"DatabaseError: A database operation failed. Details: {e}. Check data constraints or server status.")

# __CONNECTION END__

if 'infomsg' not in st.session_state:
    st.session_state.infomsg = ""



@st.cache_data(ttl=600)
def count_EUId():
    result = cnnOne.run("SELECT COUNT(*) FROM TrPosts WHERE EnryUId = :euid", euid=EUId)
    return result[0][0]
 
# Selectionbox Options
schoollevel=["","ECD","PRIMARY","SECONDARY"]  

levelToWhichTught = ["","ECD","PRIMARY","FORM-2","O-LEVEL","A-LEVEL"]

subjects=[
    "",
    "ACCOUNTING",
    "ADDITIONAL MATHEMATICS",
    "AGRICULTURE",
    "BIOLOGY",
    "BUILDING TECHNOLOGY & DESIGN",
    "BUSINESS STUDIES",
    "CHEMESTRY",
    "COMBINED SCIENCE",
    "COMMERCE",
    "COMPUTER SCIENCE",
    "DIVINITY",
    "ECD",
    "ECONOMIC HISTORY",
    "ECONOMICS",
    "ENGLISH LANGUAGE",
    "FAMILY & RELIGIOUS STUDIES",
    "FOOD TECHNOLOGY",
    "GENERAL",
    "GENERAL SCIENCE",
    "GEOGRAPHY",
    "HERITAGE STUDIES",
    "HISTORY",
    "HOME MGT & DESIGN",
    "HORTICULTURE",
    "ICT",
    "INTEGRATED SCIENCE",
    "KALANGA",
    "LITERATURE IN ENGLISH",
    "MANAGEMENT OF BUSINESS",
    "MATHEMATICS",
    "METAL TECHNOLOGY & DESIGN",
    "MUSIC",
    "NDEBELE",
    "PE, SPORT & MASS DISPLAY",
    "PHYSICS",
    "PRIMARY ECD",
    "PRIMARY GENERAL",
    "PRINCIPLES OF ACCOUNTS",
    "PURE MATHEMATICS",
    "SOCIAL STUDIES",
    "SOCIOLOGY",
    "TECHNICAL DESIGN",
    "TECHNICAL GRAPHICS & DESIGN",
    "TEXTILE TECHNOLOGY & DESIGN",
    "THEATRE ARTS",
    "TONGA",
    "VISUAL & PERFORMING ARTS",
    "WOOD TECHNOLOGY & DESIGN"
] 

districts=[
    "",
    "BEITBRIDGE RURAL",
    "BEITBRIDGE URBAN",
    "BIKITA",
    "BINDURA RURAL",
    "BINDURA URBAN",
    "BINDURA PERI-URBAN",
    "BINGA",
    "BUBI",
    "BUHERA",
    "BULAWAYO URBAN",
    "BULAWAYO PERI-URBAN",
    "BULILIMA",
    "CHEGUTU RURAL",
    "CHEGUTU URBAN",
    "CHEGUTU PERI-URBAN",
    "CHIKOMBA",
    "CHIMANIMANI EAST",
    "CHIMANIMANI WEST",
    "CHINHOYI",
    "CHIPINGE RURAL",
    "CHIPINGE URBAN",
    "CHIPINGE PERI-URBAN",
    "CHIREDZI RURAL",
    "CHIREDZI URBAN",
    "CHIREDZI PERI-URBAN",
    "CHIRUMHANZU",
    "CHITUNGWIZA URBAN",
    "CHITUNGWIZA PERI-URBAN",
    "CHIVI",
    "EPWORTH URBAN",
    "GOKWE NORTH",
    "GOKWE SOUTH",
    "GOKWE URBAN",
    "GOROMONZI",
    "GURUVE",
    "GUTU",
    "GWANDA RURAL",
    "GWANDA URBAN",
    "GWANDA PERI-URBAN",
    "GWERU RURAL",
    "GWERU URBAN",
    "GWERU PERI-URBAN",
    "HARARE RURAL",
    "HARARE URBAN",
    "HARARE PERI-URBAN",
    "HURUNGWE (KAROI RURAL)",
    "HWANGE RURAL",
    "HWANGE URBAN",
    "HWANGE -PERI-URBAN",
    "HWEDZA",
    "INSIZA",
    "KADOMA RURAL",
    "KADOMA URBAN",
    "KADOMA PERI-URBAN",
    "KAROI",
    "KWEKWE RURAL",
    "KWEKWE URBAN",
    "KWEKWE PERI-URBAN",
    "LUPANE",
    "MAKONI",
    "MANGWE RURAL",
    "MANGWE URBAN (PLUMTREE)",
    "MARONDERA URBAN",
    "MARONDERA PERI-URBAN",
    "MASVINGO RURAL",
    "MASVINGO URBAN",
    "MASVINGO PERI-URBAN",
    "MATOBO",
    "MAZOWE",
    "MBERENGWA",
    "MBIRE",
    "MARONDERA RURAL",
    "MOUNT DARWIN",
    "MUDZI",
    "MUREHWA",
    "MUTARE RURAL",
    "MUTARE URBAN",
    "MUTARE PERI-URBAN",
    "MUTASA",
    "MUTOKO",
    "MUZARABANI",
    "MVURWI",
    "MWENEZI",
    "NKAYI",
    "NYANGA",
    "REDCLIFF",
    "RUSAPE",
    "RUSHINGA",
    "RUWA",
    "SANYATI",
    "SEKE",
    "SHAMVA",
    "SHURUGWI RURAL",
    "SHURUGWI URBAN",
    "SHURUGWI PERI-URBAN",
    "TSHOLOTSHO",
    "UMGUZA",
    "UMZINGWANE",
    "UZUMBA-MARAMBA-PFUNGWE",
    "VICTORIA FALLS",
    "ZAKA",
    "ZVIMBA",
    "ZVISHAVANE RURAL",
    "ZVISHAVANE URBAN",
    "ZVISHAVANE PERI-URBAN"
]

st.title("Teacher-Swops")

st.write("Where all teachers intending to swop can EASILY meet and conclude their swopping deals!")


# 1. Create Table
    
if cnnOne:

    cnnOne.run("""
               
            CREATE TABLE IF NOT EXISTS TrPosts (

            RecID SERIAL PRIMARY KEY,

            RecDte varchar(25),       

            Unme varchar(30) NOT NULL,              

            BusContNo varchar(25) NOT NULL,

            SchLevel varchar(15) NOT NULL,

            SubjTaught varchar(80) NULL,        

            LvlTaughtTo varchar(15) NOT NULL,       

            CurDist varchar(80) NOT NULL,

            DesiredDist varchar(80) NOT NULL,
            
            EnryUId varchar(50) NOT NULL UNIQUE

            )
            """)

Tsk = st.selectbox("Task", ["Click on Down Arrow to Select a Task","ENTER MY DETAILS","FIND MY SWOP MATCHES","DELETE MY ENTRIES"])
is_expanded = (Tsk == "ENTER MY DETAILS" or Tsk == "FIND MY SWOP MATCHES" or Tsk == "DELETE MY ENTRIES")
# 3. Insert New Records
with st.expander("", expanded=is_expanded):    
    with st.form("Add_a_Post"):
        if Tsk == "ENTER MY DETAILS":
            RecDate = st.text_input("Date", value=formatted_curdate) 
            UName = st.text_input("Enter your USERNAME")           
            BusContactNo = st.text_input("Enter your BUSINESS CONTACT NUMBER")
            SchoolLevel = st.selectbox("Select SCHOOL LEVEL", options=schoollevel)
            SubjectTaught = st.selectbox("Select/Enter (full official description of) SUBJECT you teach", options=subjects)
            LevelTaughtTo = st.selectbox("Select LEVEL TO WHICH YOU TEACH subject", options=levelToWhichTught)
            CurrentDistrict = st.selectbox("Select/Enter CURRENT DISTRICT where you are working", options=districts)
            DesiredDistrict = st.selectbox("Select/Enter (full official description of) DISTRICT YOU DESIRE", options=districts)
            EUId = st.text_input("Create and Enter UNIQUE IDENTIFIER for this subject's post. (Keep this; you will be required to use it later).")
            
            if st.form_submit_button("Submit"):
                refid_count = count_EUId()                
                if refid_count > 0:
                    st.toast(f"Unique Identifier {EUId} is not available. Please create a different entry idenifier and try again.")
                else:
                    if RecDate =="" or UName =="" or BusContactNo == "" or SchoolLevel == "" or SubjectTaught == "" or LevelTaughtTo == "" or CurrentDistrict == "" or DesiredDistrict == "" or EUId == "":
                        st.error("Enter data in all the data fields.")
                    else:                       
                        if cnnOne:                        
                            cnnOne.run("INSERT INTO TrPosts (RecDte, Unme, BusContNo, SchLevel, SubjTaught, LvlTaughtTo, CurDist, DesiredDist, EnryUId) VALUES (:rdte, :unm, :bcontno, :sklvl, :sbjtaught, :lvltotto, :curdstrict, :dstrictsot, :entuid)",
                                rdte=RecDate, unm=UName, bcontno=BusContactNo, sklvl=SchoolLevel, sbjtaught=SubjectTaught, lvltotto=LevelTaughtTo, curdstrict=CurrentDistrict, dstrictsot=DesiredDistrict, entuid=EUId)                                       
                            #cnnOne.commit()
                            st.cache_data.clear() # Reset cache to show updated data                        
                            st.toast("Record successfully inserted.")           

if Tsk == "FIND MY SWOP MATCHES":

    SchLevel = st.selectbox("Enter SCHOOL LEVEL",  options=schoollevel)
    SubjTaught = st.selectbox("Select/Enter (full official description of) SUBJECT you teach", options=subjects)
    LvlTaughtTo = st.selectbox("Select LEVEL TO WHICH YOU TEACH subject", options=levelToWhichTught)
    CurDistrict = st.selectbox("Select/Enter CURRENT DISTRICT where you are working", options=districts)
    DesiredDistrict = st.selectbox("Select/Enter (full official description of) DISTRICT where you wish to go", options=districts)   

    ksl=''
    kst=''
    kltt=''
    kdd=''
    kcd=''

    if st.button("Find My Swop Matches"):
        query = "SELECT * FROM TrPosts WHERE SchLevel = :ksl and SubjTaught = :kst and LvlTaughtTo = :kltt and CurDist = :kdd and DesiredDist= :kcd"        
        matching_posts = cnnOne.run(query, ksl=SchLevel, kst=SubjTaught, kltt=LvlTaughtTo, kcd=CurDistrict, kdd=DesiredDistrict)          
       
        if matching_posts:         

            # initialize an empty list to store records
            matching_data = []

            # Populate the list using a for loop
            for matching_post in matching_posts:                
                matching_data.append({
                    'Date_Posted': matching_post[1],
                    'Username': matching_post[2],                                             
                    'Bus_Cont_No': matching_post[3],
                    'School_level': matching_post[4],
                    'Subject_Taught': matching_post[5],
                    'Taught_to_Level': matching_post[6],
                    'Current_District': matching_post[7],                               
                    'District_Desired': matching_post[8]                    
                    })
            st.write("")
            st.write(f"LIST OF MEMBERS WITH WHOM YOU MAY SWOP")
            
            pd.DataFrame()    
            # Create a DataFrame from the list
            matches_df = pd.DataFrame(matching_data)        
           
            # Display the DataFrame in Streamlit
            st.dataframe(matches_df)                             

        else:
           
            st.toast("No members with whom you may swop. Check again after some time when more posts have been added.")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Place 'View ALL Posts' logic here 
        
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

elif  Tsk == "DELETE MY ENTRIES":                
        EUId = st.text_input("Enter UNIQUE IDENTIFIER you submitted for this subject's entry")                              
        if st.button("Delete Entry"):                
            if EUId =="":
                st.error("Enter the UNIQUE IDENTIFIER of the post you want to delete.")
            else:
                refid_count = count_EUId()
                if refid_count < 1:
                    st.toast(f"Unique Identifier {EUId} not found.")
                else:
                    if cnnOne:                        
                        cnnOne.run("DELETE FROM TrPosts WHERE EnryUId = :pri", pri=EUId)
                        # cnnOne.commit()                                               
                        st.cache_data.clear() # Reset cache to show updated data
                        st.toast(f"Post with Unique Identifier {EUId} successfully deleted!")

if st.sidebar:
    st.sidebar.subheader("Welcome")    
    st.sidebar.write("1. Click on the 'Task' selection box (on right pane) to navigate through app.")    
    st.sidebar.write("2. Press Enter/Tab after entering data to apply.")
    st.sidebar.write("3. Very IMPORTANT:")
    st.sidebar.write("   Keep all your post's UNIQUE IDENTIFIERS in a safe place: You will need them when it's time to search for your matches, or to delete your posts.")
   
with st.sidebar:
    st.divider()
st.sidebar.subheader("App Developers Contact Info")
# 1. Initialize session state
if 'in_state' not in st.session_state:
    st.session_state.in_state = True 
# 2. Function to set state to True
def toggle_button():
    st.session_state.in_state = not st.session_state.in_state
        
# 3. Determine callback function to toggle state
button_label = "Show Contact Info" if st.session_state.in_state else "Close"
# 4. Render button with callback
st.sidebar.button(button_label, on_click=toggle_button)

if button_label == "Close":
    st.sidebar.write("instipuse@gmail.com")

with st.sidebar:
    st.divider()

## Optional: Show cuurent state
#st.sidebar.write(f"Current Status: {button_label}")
    
