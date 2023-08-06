Simple Excel File Generator From Django Model.

Required Packages:

    pip install pandas

Usage :

    from django_model_to_excel import generate_excel_file

    def fun(request):
        queryset = User.objects.all().values()
        # all_to_excel accepts six parameter
        # queryset will be your model data
        # file_path : 'your absloute path' or None if it is None fill will store in your project Base Directory
        # file_name : 'string' or None
        # sheet_name : 'string' or None
        # index and header : Boolean
        generate_excel = generate_excel_file.all_to_excel(queryset, file_path, file_name, sheet_name, index, header)
        


