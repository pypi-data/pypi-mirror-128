import pandas as pd
from datetime import datetime, date
from itertools import chain

from django.conf import settings

def all_to_excel(model_data, file_path, file_name, sheet_name, index, header):

    item = model_data.values()

    keys = set(chain(*[dic.keys() for dic in item ]))
    final_dict = {key : [str(dic[key]) if isinstance(dic[key], date) else dic[key] for dic in item if key in dic] for key in keys }
    df = pd.DataFrame(final_dict)

    header_value = True
    if header == True or 'True':
        header_value = True
    elif header == False or 'False':
        header_value = False
    else:
        header_value = True


    index_value = False
    if index == True or 'True':
        index_value = True
    elif index == False or 'False':
        index_value = False
    else:
        index_value = False


    if file_path and file_name:

        if file_path[-1] == '/' or '\/':
            file_path = file_path[:-1]
        elif file_path[-1] == '//' or '\\':
            file_path = file_path[:-2]


        if sheet_name:
            df.to_excel(file_path+'\/'+file_name+'.xlsx', sheet_name= sheet_name, index=index_value, header=header_value)
        else:
            df.to_excel(file_path+'\/'+file_name+'.xlsx', index=index_value, header=header_value)

    else:
        if sheet_name:
            df.to_excel(str(settings.BASE_DIR)+'\/excel_file'+str(datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))+'.xlsx', sheet_name= sheet_name, index=index_value, header=header_value)
        else:
            df.to_excel(str(settings.BASE_DIR)+'\/excel_file'+str(datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))+'.xlsx', index=index_value, header=header_value)


    return True