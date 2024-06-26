from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import *
from app.queries import *
import pandas as pd
import argparse
from datetime import datetime
import os

# Run script with flag to specify the output Excel filename
parser = argparse.ArgumentParser()
parser.add_argument('--filename', '-f', 
                    type=str, 
                    help='The desired name of the output Excel file as a string. If not provided, the default filename will be \'LAMP_Export_\' followed by the date generated.',
                    default = 'LAMP_Export_' + datetime.now().strftime("%d%m%y"))
args = parser.parse_args()

# Filename for saving exported Excel Workbook
filename = ('~/lampapp/' + args.filename + '.xlsx')

### Initialize App and Connect to Database ###

# URI = ''

app = Flask(__name__)
app.debug=True
app.secret_key = 'BAD_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_POOL_SIZE'] = 20
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV']='development'


db = SQLAlchemy(app)

s = db.session
s.permanent=True

### Retrieve Data ### 

def all_results():
    comp_list = s.query(Runs.run_id).filter(Runs.status=='Complete')

    final_results = s.query(Runs.run_id, Runs.run_name, Samples.tube_id, Tests.plate_well, Samples.sample_name, Analyte.analyte_id, Analyte.name, Patients.first_name, Patients.sur_name, Results.result_id, Results.checker_result, Results.checker_comment, Results.genotyper_result, Results.genotyper_comment,Results.genotyper_result_updated, Results.checker_result_updated, Qsresult.run_id)\
    .join(Qsresult, Qsresult.qs_result_id==Results.qs_result_id).filter(Qsresult.run_id.in_(comp_list))\
    .join(Tests, Tests.test_id==Qsresult.test_id)\
    .join(Samples, Samples.sample_id==Tests.sample_id)\
    .join(Patients, Patients.patient_id==Samples.patient_id)\
    .join(Analyte, Analyte.analyte_id==Tests.analyte_id)\
    .join(Runs, Runs.run_id==Qsresult.run_id).order_by(Samples.sample_name.asc()).all()
    sorted_objects = sorted(final_results, key=lambda final_results: int(final_results.plate_well[1:]))

    s.close()
    return sorted_objects

allResults = all_results()

# Convert to Pandas Dataframe
resultsDict = [dict(row) for row in allResults]
resultsDF = pd.DataFrame(resultsDict)

# Rename columns
resultsDF.rename(columns={"name": "analyte_name", "run_name" : "worksheet_number"}, inplace=True)

# Create unique ID "Sample"
resultsDF["sample"] = resultsDF["first_name"].str[0] + resultsDF["sur_name"].str[0] + "_" + resultsDF[["sample_name", "analyte_name", "worksheet_number", "plate_well"]].agg("_".join,axis=1)

# Split data into seperate worksheets
genoDF = resultsDF[["sample", "worksheet_number","analyte_name", "genotyper_result", "genotyper_comment", "genotyper_result_updated"]]#.sort_values(by=["worksheet_number", "sample"])
checkerDF = resultsDF[["sample", "worksheet_number", "analyte_name", "checker_result", "checker_comment", "checker_result_updated"]]#.sort_values(by=["worksheet_number", "sample"])
sampleDF = resultsDF[["first_name", "sur_name", "sample_name", "worksheet_number"]].drop_duplicates()#.sort_values(by=["worksheet_number", "sample_name"])


### Export as Excel Workbook ###

# Error if file exists, else save each dataframe as independent Excel sheets in same workbook
exists = os.path.isfile(filename)

if exists:
    print(filename + ' already exists. Workbook not saved.')

else: 
    xl_writer = pd.ExcelWriter(filename, engine='openpyxl')

    sampleDF.to_excel(xl_writer, sheet_name='Samples', index=False)
    genoDF.to_excel(xl_writer, sheet_name='Genotyper Results', index=False)
    checkerDF.to_excel(xl_writer, sheet_name='Checker Results', index=False)

# Reformat column widths
    sheets = ("Samples", "Genotyper Results", "Checker Results")
    for sheet in sheets:
        for column in xl_writer.sheets[sheet].columns:
            column_letter = column[0].column_letter
            max_length = 0
            for cell in column:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)

            adjusted_width = (max_length + 2) * 1.2
            xl_writer.sheets[sheet].column_dimensions[column_letter].width = adjusted_width
        
    xl_writer.close()
    print('Workbook saved as: '+filename)  



s.close()