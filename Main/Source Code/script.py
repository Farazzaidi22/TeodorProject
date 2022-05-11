from asyncio.windows_events import NULL
from cmath import nan
from itertools import count
import os
from pathlib import Path
from importlib.resources import path
from tokenize import String
from weakref import ref
import pandas as pd
import numpy as np
import datetime


# cols_to_be_replaced = ['Kund: Namn', 'Kund: C/o', 'Kund: Telefonnr', 'Kund: Mobilnr', 'Boendetyp', 'BP']
# cols_to_be_replaced_with = ['Namn', 'CO', 'Fast telefon 1', 'Mobil 1', 'Hitta', ]

cols_to_be_replaced_with = [0, 1, 6, 7, 9, 10]
cols_to_be_replaced = [0, 6, 9, 10, 67, 68]


def Create_DF(file_path):
    print('Creating data frame of file ', file_path , '...')
    df = pd.read_excel(file_path)
    # print(df['Bearbetning: Start'])
    return df


def Save_Excel_File(df, filePath, ext, folderName, abs_path):
    file_name = Path(filePath).stem + ext
    file_path_to_be_saved_at = str(abs_path) + folderName + file_name

    path = Path(file_path_to_be_saved_at)
    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_excel(file_path_to_be_saved_at, index = 0)
    print(file_name, " saved at ", str(abs_path) + folderName)
    return file_path_to_be_saved_at

def Conact_DFs_for_ref(path_of_ref_dfs):
    frames = []

    for i in range(0, len(path_of_ref_dfs)):
        temp_df = Create_DF(path_of_ref_dfs[i])
        frames.append(temp_df)

    result_df = pd.concat(frames)
    print(result_df)
    return result_df

def Conact_DFs(df1, df2):
    
    frames = [df1, df2]
    result_df = pd.concat(frames)
    return result_df

def BJ_equals_N(df: pd.DataFrame, title, replace, nyinflyttade_df: pd.DataFrame):
    
    # df_BI_N = df.loc[ ( df['Bor_Kvar'] == "N") ]

    df_BI_N = df
    
    if not df_BI_N.empty:
        print(df_BI_N['Bor_Kvar'])

        for i in df_BI_N.index:

            if title == 'Har flyttat':
                df_BI_N.at[i,'Log'] = title
            else:
                df_BI_N.at[i,'Log'] = title + df_BI_N.at[i,'Kund: Namn'] + ")"

            print( df_BI_N.at[i,'Log'])

            if replace == True:
                cond1 = str(df_BI_N.at[i, 'Kund: Postadress'])
                cond2 = str(df_BI_N.at[i, 'Kund: Postort'])

                df2 = nyinflyttade_df.loc[(nyinflyttade_df['Postort'] == cond1) & (nyinflyttade_df['Boendeform'] == cond2)]
                
                df2.drop_duplicates(df2.drop_duplicates(subset=['Postort','Boendeform'], keep='first', inplace=True))
                if not df2.empty:
                    print(df2)
                    
                    for j in range(0,6):
                        df_BI_N.at[i, df_BI_N.columns[ cols_to_be_replaced[j] ] ] = df2[ df2.columns[cols_to_be_replaced_with[j]] ].iat[0]

        # final_df = Conact_DFs(df, df_BI_N)
        # final_df = final_df[~final_df.index.duplicated(keep='last')]
        return df_BI_N
    
    else:
        return df


def Handling_Duplicates(main_df: pd.DataFrame, dup_df: pd.DataFrame):

    print(len(main_df))


    for index, row in main_df.iterrows():
        df1 = dup_df.loc[(dup_df['Kund: Postadress'] == row['Kund: Postadress']) & (dup_df['Kund: Postort'] == row['Kund: Postort'])]

        dup_rows_array = []

        if not df1.empty:
            print (df1)

            columns = df1.columns.tolist()

            for i, r in df1.iterrows():
                dup_row_data = ""

                if not pd.isna(r['Log']):
                    print(str(r['Log']))
                    dup_rows_array.insert(0, str(r['Log']))

                for c in columns:
                    value = str(r[c])
                    if(value != "nan"):
                        dup_row_data += value

            
                dup_rows_array.append(dup_row_data)

            print(dup_rows_array)

            sorted_Log = ""
            
            for item in dup_rows_array:
                print(item)
                sorted_Log = sorted_Log + '\n' + str(item)
            
            print(sorted_Log)
            
            print(main_df.at[index, 'Log'])
            
            if pd.isna(row['Log']):
                main_df.at[index,'Log'] = sorted_Log
                print(main_df.at[index,'Log'])
            
            elif not pd.isna(row['Log']):
                print(row['Log'])
                main_df.at[index,'Log'] = '\n' + main_df.at[index,'Log'] + '\n' + sorted_Log


    final_df = Conact_DFs(main_df, dup_df)
    final_df = final_df[~final_df.index.duplicated(keep='last')]
    return final_df



def main(main_file_path, reference_files_list, nyinflyttade_file_path, ny_fil_med_avlidna_file_path, abs_path):
    
    main_df = Create_DF(main_file_path)
    print('Created data frame of ', main_file_path, ' !!!')
    
    ref_dfs = Conact_DFs_for_ref(reference_files_list)
    print('Created data frame of ', reference_files_list, ' !!!')

    nyinflyttade_df = Create_DF(nyinflyttade_file_path)
    print('Created data frame of ', nyinflyttade_file_path, ' !!!')

    ny_fil_med_avlidna_df = Create_DF(ny_fil_med_avlidna_file_path)
    print('Created data frame of ', ny_fil_med_avlidna_file_path, ' !!!')

    
    main_df.insert(loc=len(main_df.columns), column='BP', value="")
    main_df.insert(loc=len(main_df.columns), column='BQ', value="")


    #sorting by Bokning: Start Column
    main_df = main_df.sort_values(by=['Bokning: Start'], ascending=True)

    #finding all duplicate values
    dup_df_fil =  main_df[main_df.duplicated(subset=['Kund: Postadress','Kund: Postort'], keep=False)].sort_values('Kund: Postadress')
    
    #droping the first but keeping rest of the duplicates
    dup_df = dup_df_fil[dup_df_fil.duplicated(subset=['Kund: Postadress','Kund: Postort']) | ~dup_df_fil.duplicated(subset=['Kund: Postadress','Kund: Postort'], keep=False)].sort_values('Kund: Postadress')
    print(dup_df['Log'])

    m = dup_df.Bor_Kvar == "N"
    dup_df_not_whereN = dup_df[~m]
    dup_df_whereN = dup_df[m]

    dup_df_whereN = BJ_equals_N(dup_df_whereN, "Nyinflyttad (tidigare ägare ", True, nyinflyttade_df)
    dup_df = Conact_DFs(dup_df_whereN, dup_df_not_whereN)

    print(dup_df['Log'])

    #droping all duplicate from  original df and keeping with earliest date only
    main_df.drop_duplicates(main_df.drop_duplicates(subset=['Kund: Postadress','Kund: Postort'], keep='first', inplace=True))
    
    m = main_df.Bor_Kvar == "N"
    main_df_not_whereN = main_df[~m]
    main_df_whereN = main_df[m]

    # print(main_df_not_whereN['Bor_Kvar'])
    
    main_df_whereN = BJ_equals_N(main_df_whereN, "Har flyttat", False, nyinflyttade_df)

    main_df = Conact_DFs(main_df_whereN, main_df_not_whereN)
    # main_df = main_df[~main_df.index.duplicated(keep='last')]

    main_df = Handling_Duplicates(main_df, dup_df)
    print(main_df)

    # saved_path = Save_Excel_File(main_df, main_file_path, '(modified).xlsx', '/output/', abs_path)


    output = {'Log': []}

    for i in range(1,15):
        print('Checking Ufall ', i, ' ...')
        output['Ufall ' + str(i)] = []

    for index, row in main_df.iterrows():

    ########## Checking if AW = Avliden ##########

        title_for_ny_fil_med_avlidna_df = ""

        if(row['SPAR_Status'] == "Avliden"):
            title_for_ny_fil_med_avlidna_df = "Ny ägare (tidigare ägare " + row['Kund: Namn'] + " avliden)"

            cond1 = str(main_df.at[i, 'Kund: Postadress'])
            cond2 = str(main_df.at[i, 'Kund: Postort'])

            df2 = ny_fil_med_avlidna_df.loc[(ny_fil_med_avlidna_df['Postort'] == cond1) & (ny_fil_med_avlidna_df['Boendeform'] == cond2)]
                
            print(df2)
            df2.drop_duplicates(df2.drop_duplicates(subset=['Postort','Boendeform'], keep='first', inplace=True))
            if not df2.empty:
                print(df2)
                for j in range(0,6):
                    main_df.at[i, main_df.columns[ cols_to_be_replaced[j] ] ] = df2[ df2.columns[cols_to_be_replaced_with[j]] ].iat[0]



        strr = ''

        if( not (row['Bearbetning: Start'] ) is np.nan):
            strr = (row['Bearbetning: Start'] ) + ', '
        
        if( not (row['Bearbetning: Utfall']) is np.nan):
            if(strr != None):
               strr = strr + (row['Bearbetning: Utfall']) + ', '
            else:
                strr = (row['Bearbetning: Utfall']) + ', '
        
        if( not (row['Resurs: Namn']) is np.nan):
            if(strr != None):
               strr = strr + (row['Resurs: Namn']) + ', '
            else:
                strr = (row['Resurs: Namn']) + ', '
        
        if( not (row['Resurs: Notering']) is np.nan):
            if(strr != None):
               strr = strr + (row['Resurs: Notering'])
            else:
                strr = (row['Resurs: Notering'])

        AE_value = []
        
        print('saving value ', strr, ' in column Ufall 1...')
        
        output['Ufall 1'].append(strr)
        
        print('saved!!!')
        print('Adding in Log...')
        
        print(strr)
        AE_value.append(strr)
        
        print('Added!!!!')
        
        k = 2
        
        temp = ref_dfs.loc[row['Kund: Namn'] == ref_dfs['Kund: Namn']]

        for ind, row2 in temp.iterrows():
            if (row['Kund: Postadress'] ==  row2['Kund: Postadress']):
                strr_ref = ''

                if( not (row2['Bearbetning: Start'] ) is np.nan):
                    strr_ref = (row2['Bearbetning: Start'] ) + ', '

                if( not (row2['Projekt: Namn']) is np.nan):
                    if(strr_ref != None):
                        strr_ref = strr_ref + (row2['Projekt: Namn']) + ', '
                    else:
                        strr_ref = (row2['Projekt: Namn']) + ', '
                
                if( not (row2['Bearbetning: Utfall']) is np.nan):
                    if(strr_ref != None):
                        strr_ref = strr_ref + (row2['Bearbetning: Utfall']) + ', '
                    else:
                        strr_ref = (row2['Bearbetning: Utfall']) + ', '
                
                if( not (row2['Resurs: Namn']) is np.nan):
                    if(strr_ref != None):
                        strr_ref = strr_ref + (row2['Resurs: Namn']) + ', '
                    else:
                        strr_ref = (row2['Resurs: Namn']) + ', '
                
                if( not (row2['Resurs: Notering']) is np.nan):
                    if(strr_ref != None):
                        strr_ref = strr_ref + (row2['Resurs: Notering'])
                    else:
                        strr_ref = (row2['Resurs: Notering'])

                print('saving value ', strr_ref, 'in Ufall ', str(k), ' ...')
                
                output['Ufall ' + str(k)].append(strr_ref)
                
                print('saved!!!')
                print('Adding in Log...')
                
                AE_value.append(strr_ref) 
                
                print('Added!!!!')
                
                k += 1

        AE_value = sorted(AE_value, reverse=True ,key=lambda x: datetime.datetime.strptime(x.split(',')[0], '%Y-%m-%d %H:%M'))

        if not pd.isna(row['Log']):
            print(row['Log'])
            
            AE_value.insert(0, str(row['Log']))


        if title_for_ny_fil_med_avlidna_df:
            print(title_for_ny_fil_med_avlidna_df)
            AE_value.insert(0, title_for_ny_fil_med_avlidna_df)

        sorted_Log = ""
        print(sorted_Log)

        for item in AE_value:
            print(item)
            sorted_Log = sorted_Log + '\n' + item
        
        print(row['Bor_Kvar'])
        output['Log'].append(sorted_Log)

        print(output['Log'][-1])

        
        for rem in range(k, 15):
            output['Ufall ' + str(rem)].append("")


    print('Optimizing file....')
    outputdf = pd.DataFrame(data=output)
    outputdf = outputdf.replace(np.nan,"")

    main_df['Log'] = np.nan
    main_df["Log"] = outputdf["Log"]

    # print(main_df.loc[])

    for i in range(1, 15):
        main_df['Ufall ' + str(i)] = output['Ufall ' + str(i)]
    print('Optimzation Completed')

    main_df = main_df
    m = main_df.Bor_Kvar == "N"
    main_df_not_whereN = main_df[~m]
    main_df_whereN = main_df[m]

    for index, row in main_df_not_whereN.iterrows():

        if (not pd.isna(row['Log'])) and ('Har flyttat' in row['Log']):
            print(row['Bor_Kvar'])
            print(row['Log'])

            text = str(row['Log'])
            x = text.replace("Har flyttat", "")

            row['Log'] = x


    main_df = Conact_DFs(main_df_not_whereN, main_df_whereN)

    print('Saving file...')
    saved_path = Save_Excel_File(main_df, main_file_path, '(modified).xlsx', '/output/', abs_path)
    print('file saved at ',  saved_path)
    print('Finished!!!!')


def Start_Editing(main_file_path, reference_file1, reference_file2, Nyinflyttade_folder_path, Ny_fil_med_avlidna_folder_path):
    
    print('Started!!!!!')
    abs_path = Path(main_file_path).parent

    ref_file_list = []
    ref_file_list.append(reference_file1)
    ref_file_list.append(reference_file2)

    print(ref_file_list)


    main(main_file_path, ref_file_list, Nyinflyttade_folder_path, Ny_fil_med_avlidna_folder_path, abs_path)




# main_file_path = "E:\Freelance/teodor\Main\Input_output/attachments/Alla orginalbokningar _ info från Bisnode.xlsx"
# ref_file_list = [ "E:\Freelance/teodor\Main\Input_output/attachments/cross senast utfall (samtliga) 48228st (1).xlsx",  "E:\Freelance/teodor\Main\Input_output/attachments/retention senast utfall (samtliga) 33113st (1).xlsx"]
# nyinflyttade_file_path ="E:\Freelance/teodor\Main\Input_output/attachments/Nyinflyttade _ Kollad av Team Africa.xlsx"
# ny_fil_med_avlidna_file_path = "E:\Freelance/teodor\Main\Input_output/attachments/Ny fil med avlidna (ej kollad av Team Africa).xlsx"

# abs_path = Path(main_file_path).parent


# main(main_file_path, ref_file_list, nyinflyttade_file_path, ny_fil_med_avlidna_file_path, abs_path)