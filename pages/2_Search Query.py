import streamlit as st
import pandas as pd  # to read the uploaded csv
from datetime import datetime
from Home import conn
from Home import cur
from Home import master_table
from Home import query_table

if st.session_state["authentication_status"]:
    current_date=datetime.now()

    with open('G:/Office Project/main pro/CSS/create_query.css') as f:
        st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
    # Instantiating cursor


    # Date selection for sheet
    _="""
            SELECT date_time FROM master_sheet_table WHERE username='chetan';
    """
    q = "SELECT date_time FROM "+master_table+" WHERE username='"+st.session_state["username"]+"'"
    df_master_sheets_dates= pd.read_sql_query(q, conn)
    master_sheets_dates=df_master_sheets_dates.drop_duplicates()
    master_sheet_date=st.sidebar.selectbox("Select your sheet",options=master_sheets_dates)

    # Slecting all data from Master table
    _="""
        SELECT * FROM master_sheet_table WHERE username='chetan' and date_time='2022-07-26 16:34:56'
    """
    q = "SELECT * FROM "+master_table+" WHERE username='"+st.session_state["username"]+"' and date_time='"+str(master_sheet_date)+"'"
    df_master_table = pd.read_sql_query(q, conn)
    df_drop_master_sheet_table=df_master_table.drop(['date_time','lable','username'],axis=1)

    # user and selected date query
    priority_q = "username='" + st.session_state["username"] + "' and date_time='" + str(master_sheet_date) + "'"

    # columns extraction
    columns=[]
    for col in df_master_table.columns:
        columns.append(col)
    df_col=pd.DataFrame(columns)

    parameters_list = df_col[7:]

    st.title('Create Query:')

    if 'string' not in st.session_state:
        st.session_state.string = " "

    def query_evaluate(q,connection):
        s_query=str(q)
        y2 = "SELECT Name,Current_Price,Price_to_Earning,Industry_PE,Market_Capitalization," \
             "EPS FROM "+master_table+" WHERE "+s_query+" and "+priority_q
        df=pd.read_sql_query(y2,connection)
        return df

    q_col1,q_col2,q_col3=st.columns(3)
    query_string=q_col1.text_area("Write query:",value=st.session_state.string,height=200)
    save_string=q_col2.text_area("Save Query:", value=query_string,height=200,help="write query in 'write query' box it will reflect here!")

    with q_col3:
        st.markdown("---")
        if q_col3.button("Clear",help="Clear Query"):
            st.session_state.string =""
            query_string = ""
            save_string = ""
            st.experimental_rerun()

        if q_col3.button("Save Query",help="Save your Query"):
            #col3.write("Username:{}".format(user))
            add_query = 'insert into '+query_table+'(`username`,`date_time`,`query`)VALUES(%s,%s,%s)'
            cur.execute(add_query, (st.session_state["username"], current_date, query_string))
            conn.commit()
            q_col3.success("Successfully saved.")
            #st.experimental_rerun()

    tab1,tab2 ,tab3,tab4 = st.tabs(["Selected sheet","Select operator and parameters","Query Results","Saved Query's"])

    with tab1:
        st.subheader("Your selected sheet")
        st.write(master_sheet_date)
        st._legacy_dataframe(df_drop_master_sheet_table)
    with tab2:
        # Operator Buttons
        st.write('Operators')
        box=st.columns((1,2,3,4,5,6,7,8,9,10,11,12,13,14))
        if box[1].button('AND'):
            st.session_state.string += ' AND '
            st.experimental_rerun()

        if box[4].button('OR'):
            st.session_state.string += ' OR '
            st.experimental_rerun()

        if box[6].button('='):
            st.session_state.string += ' = '
            st.experimental_rerun()

        if box[7].button('>'):
            st.session_state.string += ' > '
            st.experimental_rerun()

        if box[8].button('<'):
            st.session_state.string += ' < '
            st.experimental_rerun()

        value = box[11].number_input("Enter Value",)
        if box[13].button("^"):
            st.session_state.string += str(value)
            st.experimental_rerun()

        # parameter buttons
        parameters_button_list = columns[7:]
        halfs_list = parameters_button_list[:int(len(parameters_button_list) / 2)]
        second_half_list = parameters_button_list[int(len(parameters_button_list) / 2):len(parameters_button_list)]

        with st.form("Parameters"):
            st.write("Parameters:")
            par_but_col1,par_but_col2=st.columns(2,gap="small")
            with par_but_col1:
                for par in halfs_list:
                    if st.form_submit_button('{}'.format(par)):
                        st.session_state.string+=par
                        st.experimental_rerun()
            with par_but_col2:
                for par in second_half_list:
                    if st.form_submit_button('{}'.format(par)):
                        st.session_state.string+=par
                        st.experimental_rerun()

    with tab3:
        if q_col3.button("Run Query",help="Run Query and see result below 'Result' tab"):
                #if query_evaluate(query_string,conn).sort_values('Market_Capitalization',ascending=False,ignore_index=True):
                sort_list=query_evaluate(query_string,conn).sort_values('Market_Capitalization',ascending=False,ignore_index=True)
                st.subheader("Query Results")
                q_col3.success("{} results found".format(len(sort_list)))
                st._legacy_dataframe(sort_list,height=1000)

    with tab4:
        q = "SELECT date_time,query FROM "+query_table+" WHERE username='"+st.session_state["username"]+"'"
        df_saved_querys_table = pd.read_sql_query(q, conn)
        querys_dates=df_saved_querys_table['date_time'].drop_duplicates()
        selected_date=st.selectbox("Select date:",options=querys_dates)
        querrys_q = "SELECT query FROM "+query_table+" WHERE username='"+st.session_state["username"]+"' and date_time='"+str(selected_date)+"'"
        df_saved_querys = pd.read_sql_query(querrys_q,conn)
        st._legacy_dataframe(df_saved_querys,width=1000)
        st.write(st.session_state["username"])
        if st.button("Delete"):
            q="DELETE FROM "+query_table+" WHERE username='" + st.session_state["username"] + "' and date_time='" + str(selected_date) + "'"
            cur.execute(q)
            conn.commit()
            st.success("Query Deleted")
            st.experimental_rerun()
else:
    st.warning("Please login first.")

