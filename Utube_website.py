import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_tags import st_tags
import youtube_extractor as yt
from youtube_extractor import check_api_key
from annotated_text import annotated_text
import data_con as my_sql
import pandas as pd
import logging

logging.basicConfig(filename="Utube_website.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
log = logging.getLogger()
log.setLevel(logging.DEBUG)

API_key = None
SQL_host = '192.168.0.114'
SQL_port = 3307
SQL_user = 'root'
SQL_pswd = '1king#lanka'
SQL_DB = 'Utube_DHW4'

if "API_key" not in st.session_state:
    st.session_state["API_key"] = "AIzaSyDTWL7cVqvBC4lmGjr3RJUeC6CvYktcr6w"
if "API_key_pass" not in st.session_state:
    st.session_state["API_key_pass"] = False
if "Active_SQL_connection" not in st.session_state:
    st.session_state["Active_SQL_connection"] = False
if "keywords" not in st.session_state:
    st.session_state["keywords"] = []
if "config" not in st.session_state:
    st.session_state["config"] = config = {
        'SQL_host': SQL_host,
        'SQL_port': SQL_port,
        'SQL_user': SQL_user,
        'SQL_pswd': SQL_pswd,
        'SQL_DB': SQL_DB
    }

st.set_page_config(
    page_title="Utube DHW 4",
    page_icon=r"Icons/Calendula.ico",
    layout='wide',
)
st.title("YouTube Data Harvesting and Warehousing using SQL and Streamlit")
annotated_text('by ', ('[Elamparithi T](https://www.linkedin.com/in/elamparithi-t/)', 'Data Scientist', "#8ef"))

with st.sidebar:
    selected_option = option_menu('Menu', ["Config", "Home", "Analyze", "About"],
                                  icons=['gear', 'house', "list-task", 'info-square'],
                                  default_index=1, menu_icon="cast")  # orientation="horizontal"

if selected_option == "Config":
    # here I made Streamlit configuration page for getting apikey and SQL connection data.
    st.subheader("Config")

    # Form 1 for getting API key and validating it.
    with st.form(key='API_form'):
        API_key = st.text_input("API key:", type="password", key="API_key",
                                value=st.session_state["API_key"])
        if st.form_submit_button(label='Verify'):
            if check_api_key(API_key):
                st.session_state["API_key_pass"] = True
                st.success("API key passed", icon="✅")
                tube = yt.YouTubeDataExtractor(API_key)
                log.info(f'Tube loaded, API key = {API_key}')
            else:
                st.session_state["API_key_pass"] = False
                st.error("Invalid API key !!!")
                log.info(f'API key failed, API key = {API_key}')
    """
    by default for youtube data extraction API key is a must for extracting the data and uploading to sql and then processing it. 
    still, if you skip sql-host details you still can get the Extracted data as Json file with channel name as its filename.
    but you will loose Analytics page.
    """
    # Form 2 for getting MySQL configuration.
    with st.form(key='MySQL_cred_form'):
        st.write("Enter MySQL Host details:")
        SQL_host = st.text_input("Hostname/ IP:", key="SQL_host", value=st.session_state['config']['SQL_host'])
        SQL_port = st.text_input("SQL port no :", key="SQL_port", value=st.session_state['config']['SQL_port'])
        SQL_user = st.text_input("SQL Username:", key="SQL_user", value=st.session_state['config']['SQL_user'])
        SQL_pswd = st.text_input("SQL password:", key="SQL_pswd", value=st.session_state['config']['SQL_pswd'], type="password")
        SQL_DB = st.text_input("SQL Database:", key="SQL_DB", value=st.session_state['config']['SQL_DB'])
        if st.form_submit_button(label='Verify'):
            if my_sql.check_database_availability(SQL_host, SQL_port, SQL_user, SQL_pswd, SQL_DB):
                st.success("SQL credentials working", icon="✅")
                st.write(f"✔️ Hostname/ IP: {SQL_host}")
                st.write(f"✔️ Host port no: {SQL_port}")
                st.write(f"✔️ SQL Username: {SQL_user}")
                st.write(f"✔️ SQL password: ", "*" * len(SQL_pswd))
                st.write(f"✔️ SQL Database: {SQL_DB}")
                st.session_state['config'] = {
                    'SQL_host': SQL_host,
                    'SQL_port': SQL_port,
                    'SQL_user': SQL_user,
                    'SQL_pswd': SQL_pswd,
                    'SQL_DB': SQL_DB
                }
                st.session_state["Active_SQL_connection"] = True
    st.success(st.session_state)

    if st.session_state["API_key_pass"]:
        st.write("API_key_pass")

    if st.session_state["Active_SQL_connection"]:
        st.write("Active_SQL_connection")
        df = pd.DataFrame(st.session_state)
        st.write(df)

    if st.button("reset"):
        for keys in st.session_state.keys():
            del st.session_state[keys]
            log.info('session state initiated.')

elif selected_option == "Home":
    """
    This is the Home page here you enter channel name/ID and get details.
    """

    if st.session_state["API_key_pass"]:
        st.success(f'✔️ API key is valid. {st.session_state["API_key"]}')
    else:
        st.error(f'❌ API key is invalid. {st.session_state["API_key"]}')

    st.subheader("Home")
    with (st.form(key="ChannelID_names")):
        keywords = st_tags(label="Channel ID/names (max10):", maxtags=10, key="keywords",
                           value=['madras foodie', 'UCgLnPO7GYxq47FzF5j3TSlA'])
        if st.form_submit_button("proceed"):
            # Upload data for each keyword
            log.info(f"proceed button pressed. {keywords}")
            chid_list = []  # Under10
            channel_id = None
            tube = yt.YouTubeDataExtractor(API_key)
            for item in keywords:
                if not tube.check_input_type(check_text=item):
                    # False if it is a channel name: convert it to channel ID
                    try:
                        channel_id = tube.get_channel_id(item)
                    except AttributeError as e:
                        log.debug(e)
                        print(e)
                else:  # True if it is a channel ID
                    channel_id = item
                st.write(channel_id)
                chid_list.append(channel_id)
            st.success(chid_list)
            log.info(chid_list)
    st.write(st.session_state['keywords'])


elif selected_option == "Analyze":
    """
    In this page instead of getting the data directly it will get the last 10 data from the MySQL DB
    which is extracted from Home page and stored in the database mentioned above.            
    """
    st.subheader("Analyze")

elif selected_option == "About":
    """
    Here I just showing my details for users to get a glance and then how to use this app.
    """
    st.subheader("About")


    def about_section():
        st.write("""
            My name is Elamparithi, and I'm a Data Scientist based in Chennai, Tamil Nadu. Here's a bit about me:
        """)

        st.subheader("Profile:")
        st.write("""
            Leveraging a robust skill set honed through intensive GUVI coursework in Data Science. Proficient in Machine Learning and AI, I excel in
            uncovering actionable insights and solving intricate challenges. Mastery of data visualization tools such as Tableau and PowerBI enhances
            my ability to present findings effectively. Continual learning through Linked Learning and certification attainment underscores my
            commitment to staying abreast of emerging trends and technologies. With a track record of delivering solutions that drive results, I bring a
            blend of expertise and adaptability to every project, resulting in a 20% increase in predictive accuracy and 30% improvement in
            decision-making efficiency.
        """)

        st.subheader("Skills:")
        st.write("""
            - Data Visualization
            - Machine Learning
            - Deep Learning
            - Tableau
            - SQL
            - Scikit-learn
            - TensorFlow
            - PyTorch
            - NLP
            - AWS
            - ETL
            - System Administration
            - Docker
            - Podman
            - Linux
            - Windows server
            - Matplotlib
            - MongoDB
            - Seaborn
            - pandas
            - NumPy
            - prompt Engineering
        """)

        st.subheader("Professional Experience:")
        st.write("""
            **IT Executive - Desktop Support Engineer**  
            *Feb 2023 - Sep 2023*  
            DEFTUNITY SOLUTIONS - Chennai, TN  
            - Created an automation process that improved user's uptime by deploying automation tasks in FreshDesk application.
            - Build, manage, and develop a IT executive team comprised of 3 personnel, provide coaching and mentorship, conduct
              performance evaluations, and establish inclusive work cultures.
            - Coordinate with cross-functional teams to identify process gaps and develop solutions, resulting in lower Active directory
              downtime, MS365 and GCP downtimes, hardware downtimes.
            - Communicate with diverse non-IT teams, build reports on user experience and downtime and required development.
        """)

        st.subheader("Education:")
        st.write("""
            - **IIT-M Advanced programming Professional & Master Data Science**  
              *Aug 2023 - Oct 2023* | Chennai, TN
            - **Diploma in Electronics and Communication Engineering**  
              *Apr 2019* | Vellathur, TN  
              786 C.M.Annamalai Polytechnic college
        """)

        st.subheader("Contact:")
        st.write("""
            - **Email:** elamp**************@gmail.com  
            - **Phone:** +91 *******512  
            - **Location:** Chennai, TN  
            - **LinkedIn:** [LinkedIN](https://www.linkedin.com/)
        """)


    # Display the About section
    about_section()
