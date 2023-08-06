
import jaydebeapi
import pandas as pd
import itertools
import os

def execute_metadata(host,port,userid,password,excel_sheet,driver_class,jar_file):
# Data Virtuality Server Details
    host = str(host)
    port = str(port)
    uid = str(userid)
    pwd = str(password)

    # Data Virtuality JDBC class names
    driver_class = str(driver_class)
    # Data Virtuality Server driver file (full path)
    driver_file = jar_file

    # JDBC connection stringss
    connection_string='jdbc:zetaris:lightning@'+ host +':'+ port

    # Establish JDBC connection
    con = jaydebeapi.connect(driver_class, connection_string, [uid, pwd], driver_file,)
    print("Connection Done")

    #Create connection objesct
    curs = con.cursor()

    sql_str = "SHOW DATASOURCES"
    curs.execute(sql_str)
    result = curs.fetchall()

    datasource_list=[]

    for i in range(len(result)):
        datasource_list.append(result[i][0])

    datasource_list = [each_string.lower() for each_string in datasource_list]

    filename, file_extension = os.path.splitext(excel_sheet)
    if(file_extension=='.xlsx'):
        df=pd.read_excel(excel_sheet)
    if(file_extension=='.csv'):
        df=pd.read_csv(excel_sheet)
    df["Database Name"] = df["Database Name"].str.lower()
    df["Table Name"] = df["Table Name"].str.lower()
    df["Column Name"] = df["Column Name"].str.lower()
    df["Description"] = df["Description"].str.lower()
    df["Database Name"] = df["Database Name"].str.strip()
    df["Table Name"] = df["Table Name"].str.strip()
    df["Column Name"] = df["Column Name"].str.strip()
    df["Description"] = df["Description"].str.strip()

    df2 = pd.DataFrame(columns=df.columns)

    dataframe_column_list=[]

    for j1 in df.columns:
        dataframe_column_list.append(j1)

    #Index for column Named ' column name '
    dataframe_column_name_index = dataframe_column_list.index('Description')

    #Length of the list containing column names
    dataframe_columns_list_len = len(dataframe_column_list)

    #Variable to store the number of times query executed
    count_of_queries_executed = 0

    #Variable to store the total number of rows in the dataset
    Total_Count_of_rows = len(df)

    #Store the datasource list 
    database_final_list=[]

    for i in df['Database Name']:
        matching = [s for s in datasource_list if i in s]
        database_final_list.append(matching)

    database_final_list = list(itertools.chain.from_iterable(database_final_list))
    database_final_list = list(set(database_final_list))

    #Storing the datasource name, table name and columns in the dictionary as the key value pairs
    list_of_tables_in_each_database={}

    #Fetch Columns for every tables in the data source
    for d in database_final_list:
        sql_new_str = "show datasource tables %s" %(d)
        curs.execute(sql_new_str)
        result_tables = curs.fetchall()
        for t in range(len(result_tables)):
            if not(d in list_of_tables_in_each_database):
                col_sql_str = "SHOW COLUMNS FROM %s.%s" %(d,result_tables[t][0])
                curs.execute(col_sql_str)
                result_col = curs.fetchall()
                temp_col = []
                for z in result_col:
                    temp_col.append(z[0])
                temp_col_dict={}
                temp_col_dict[result_tables[t][0]] = temp_col
                list_of_tables_in_each_database[d] = [temp_col_dict]
            else:
                col_sql_str = "SHOW COLUMNS FROM %s.%s" %(d,result_tables[t][0])
                curs.execute(col_sql_str)
                result_col = curs.fetchall()
                temp_col = []
                for z in result_col:
                    temp_col.append(z[0])
                temp_col_dict={}
                temp_col_dict[result_tables[t][0]] = temp_col
                list_of_tables_in_each_database[d].append(temp_col_dict)

    for har in list_of_tables_in_each_database:
        for ris in range(len(list_of_tables_in_each_database[har])):
            list_of_tables_in_each_database[har][ris] =  {kk.lower(): vv for kk, vv in list_of_tables_in_each_database[har][ris].items()}

    #Update the meta data for the respective columns
    for k1 in range(len(df)):
        print("Updating for Row Number " +str(k1+1))
        matching = [s for s in datasource_list if df['Database Name'][k1] in s]
        if(matching):  
            for x in matching:
                x = x.lower() 
                tempkeylist=[]
                for ing in list_of_tables_in_each_database[x]:
                    name = list(ing.keys())[0]
                    tempkeylist.append(name.lower())
                if(df['Table Name'][k1] in tempkeylist):
                    tempvallist=[]
                    tp = next((i for i,d in enumerate (list_of_tables_in_each_database[x]) if df['Table Name'][k1] in d), None)
                    for tempval in list_of_tables_in_each_database[x][tp].values():
                        tempvallist.append(tempval)
                    tempvallist[0] = [abc.lower() for abc in tempvallist[0]]
                    if(df['Column Name'][k1]in tempvallist[0]):
                        for m_c in range(dataframe_columns_list_len):
                            if(m_c>dataframe_column_name_index):
                                    if not(str(df[dataframe_column_list[m_c]][k1]).isspace()):
                                        if not(pd.isnull(df[dataframe_column_list[m_c]][k1])):
                                            try:
                                                final_sql_str = "UPDATE DATASOURCE TABLE SET %s.%s OPTIONS(column_tag '%s',column_tag_value '%s')" %(x,df['Table Name'][k1],df['Column Name'][k1],(str(df[dataframe_column_list[m_c]][k1]).capitalize()))
                                                curs.execute(final_sql_str)
                                                count_of_queries_executed+=1
                                            except:
                                                continue
                            elif (m_c==dataframe_column_name_index):
                                    if not(str(df[dataframe_column_list[m_c]][k1]).isspace()):
                                        if not(pd.isnull(df[dataframe_column_list[m_c]][k1])):
                                            try:
                                                final_sql_str = "UPDATE DATASOURCE TABLE SET %s.%s OPTIONS(column_description '%s',column_description_value '%s')" %(x,df['Table Name'][k1],df['Column Name'][k1],(str(df[dataframe_column_list[m_c]][k1]).capitalize()))
                                                curs.execute(final_sql_str)
                                                count_of_queries_executed+=1
                                            except:
                                                continue
                    else:
                        ris = df.iloc[k1]
                        ris['Database Name'] = str(x) + " "
                        df2 = df2.append(ris)
                else:
                    ris = df.iloc[k1]
                    ris['Database Name'] = str(x) + " "
                    df2 = df2.append(ris)
        else:
            df2 = df2.append(df.iloc[k1])
                                
    #Print the Total Number of Times Query has been executed      
    print('Total Number of Queries Executed: '+str(count_of_queries_executed))

    #Export the csv with the rows which are not updated (the columns names are empty) (rows may be doubled (eg:stg and dwh both))
    df2 = df2.drop_duplicates()
    df2.to_csv('Not_Updated_File.csv',index=False)
                            
                            
                            
                            
                            

