# Database:testdb, Table: trial_sheet, Table_names= "Underscored"
import streamlit.components.v1 as components

import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
from Home import conn
from Home import master_table


if st.session_state["authentication_status"]:
    # with open('G:/Office Project/main pro/CSS/dashboardstyle.css') as f:
    #    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
    current_date=datetime.now()

    # Creating connection
    # onn=connect()
    cur = conn.cursor()

    database="stocks dashboard"
    #master_table="master_sheet_table"
    query_table="query_storage"
    filter_table="master_filter"

    private_columns=['date_time','lable','username']
    ignore_columns_parameter_list=['Name','BSE_Code','NSE_Code','Industry']



    # Date selection for sheet
    _="""
            SELECT date_time FROM master_sheet_table WHERE username='chetan';
    """
    q = "SELECT date_time FROM "+master_table+" WHERE username='"+st.session_state["username"]+"'"
    df_master_sheets_dates = pd.read_sql_query(q, conn)
    master_sheets_dates = df_master_sheets_dates.drop_duplicates()
    master_sheet_date = st.sidebar.selectbox("Select your sheet", options=master_sheets_dates)

    # Slecting all data from Master table
    _="""
            SELECT * FROM master_sheet_table WHERE username='chetan' and date_time='2022-07-26 16:34:56'
    """
    q = "SELECT * FROM "+master_table+" WHERE username='"+st.session_state["username"]+"' and date_time='"+str(master_sheet_date)+"'"
    df_master_table = pd.read_sql_query(q, conn)

    # user and selected date query
    priority_q = "username='"+st.session_state["username"]+"' and date_time='"+str(master_sheet_date)+"'"



    # columns extraction
    columns=[]
    for col in df_master_table.columns:
        columns.append(col)
        #print(columns)
    df_col=pd.DataFrame(columns)

    # Industry Names Extraction
    w = "SELECT DISTINCT Industry FROM "+master_table
    df_industry = pd.read_sql_query(w, conn)


    #--- Sidebar creation---

    # Industry Selection box
    st.sidebar.header("Select Sector")
    industry = st.sidebar.selectbox(label="",options=df_industry)

    # Company Names Extraction:Mysql Query:SELECT * FROM trial_sheet WHERE Industry='Chemicals'
    e = "SELECT Name FROM "+master_table+" WHERE Industry="+"'"+industry+"' and "+priority_q
    df_company = pd.read_sql_query(e, conn)
    #y = "SELECT * FROM trial_master_sheet WHERE Industry="+"'"+industry+"'"


    y2="SELECT Name,Current_Price,Market_Capitalization,Price_to_Earning,Industry_PE,EPS FROM "+master_table+" WHERE Industry="+"'"+industry+"' and "+priority_q
    df_company_data =pd.read_sql_query(y2,conn)
    print(df_company_data)

    #---Dashboard---#
    # All data of companies:
    st.header("{}".format(industry))
    st.write("{} results founded".format(len(df_company_data)))
    st._legacy_dataframe(df_company_data.sort_values(by='Market_Capitalization',ascending=False,ignore_index=True), height=2000,width=1500)

    st.markdown("""---""")

    #Companies information

    company_info=st.selectbox('Select Company', options=df_company_data.sort_values(by='Market_Capitalization',ascending=False))
    select_param=st.multiselect("Select parameters",options=df_col[7:])
    if len(select_param)==6:

            #SELECT 'Market_Capitalization' FROM master_sheet_table WHERE username='chetan' and date_time='2022-07-26 16:34:56' and Name='Divi's Lab.'
           #     above query gets affected by name='Divi's Lab' it considers "'" of i second "'" so it takes only name 'Divi' thats why take ' first then "
           # t = 'SELECT '+default_parameter1+' FROM '+table_name+' WHERE '+priority_q+' and Name="'+company_info+'"'
           # SELECT Market_Capitalization FROM master_sheet_table WHERE username='chetan' and date_time='2022-07-26 16:34:56' and Name="Divi's Lab."

        default_parameter1=select_param[0]
        t = 'SELECT '+default_parameter1+' FROM '+master_table+' WHERE '+priority_q+' and Name="'+company_info+'"'
        cur.execute(t)
        values=cur.fetchone()
        value1=float(values[0])

        default_parameter2=select_param[1]
        t = 'SELECT '+default_parameter2+' FROM '+master_table+' WHERE '+priority_q+' and Name="'+company_info+'"'
        cur.execute(t)
        values=cur.fetchone()
        value2=float(values[0])

        default_parameter3=select_param[2]
        t = 'SELECT '+default_parameter3+' FROM '+master_table+' WHERE '+priority_q+' and Name="'+company_info+'"'
        cur.execute(t)
        values=cur.fetchone()
        value3=float(values[0])

        default_parameter4=select_param[3]
        t = 'SELECT '+default_parameter4+' FROM '+master_table+' WHERE '+priority_q+' and Name="'+company_info+'"'
        cur.execute(t)
        values=cur.fetchone()
        value4=float(values[0])

        default_parameter5=select_param[4]
        t = 'SELECT '+default_parameter5+' FROM '+master_table+' WHERE '+priority_q+' and Name="'+company_info+'"'
        cur.execute(t)
        values=cur.fetchone()
        value5=float(values[0])

        default_parameter6=select_param[5]
        t = 'SELECT '+default_parameter6+' FROM '+master_table+' WHERE '+priority_q+' and Name="'+company_info+'"'
        cur.execute(t)
        values=cur.fetchone()
        value6=float(values[0])

        col1,col2,col3=st.columns(3)
        col1.metric(default_parameter1, value1)
        col2.metric(default_parameter2, value2)
        col3.metric(default_parameter3, value3)
        col4,col5,col6=st.columns(3)
        col4.metric(default_parameter4, value4)
        col5.metric(default_parameter5, value5)
        col6.metric(default_parameter6, value6)
    else:
        st.warning("Please select all 6 paramaeters")

    st.markdown("""---""")

    #Prameters Selection
    param = st.selectbox('Select Parameters:',options=df_col[7:])
    # All Prameters Data Extraction
        # Mysql Query to select parameter:SELECT NSE_Code,EPS FROM testdb.trial_sheet WHERE Industry='Chemicals'
    t = "SELECT Name,NSE_Code,"+param+" FROM "+master_table+" WHERE "+priority_q+" and Industry="+"'"+industry+"'"
    df_param_col=pd.read_sql_query(t,conn)
    print(df_param_col)
    #Pyplot creation
    fig = px.bar(df_param_col,y=df_param_col[param], x=df_param_col['NSE_Code'],text_auto='.2s', title=param+" of all Companies")
    st.plotly_chart(fig,use_container_width=True)

    st.markdown("""---""")
else:
    st.warning("Please login first.")