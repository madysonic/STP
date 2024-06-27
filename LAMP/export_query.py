'''Query to be used within Flask app.
Connects with the LAMP database to export sample information, results and peak data from a specific run number.
Requires an input runid number than can be provided from the command line using the flag -r.
The output is a xlsx workbook that will be saved in the current working directory.
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import *
from app.queries import *
import pandas as pd


### Initialize App and Connect to Database ###

# URI='mssql+pyodbc:###Driver=ODBC Driver 17 for SQL Server'

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

### Query as a Function ##

def export_results(run_id):
    
    # Check if run complete
    comp_list = s.query(Runs.run_id, Runs.status).filter(Runs.run_id==run_id, Runs.status=='Complete').first()

    if not comp_list:
        print("Run not complete.")
    else:
        print("Run complete. Exporting...") 
        
    ### Get Results Data ### 

        final_results = s.query(Runs.run_id, Runs.run_name, Samples.tube_id, Samples.sample_name,Tests.plate_well, Analyte.analyte_id, Analyte.name, Patients.first_name,Patients.sur_name, Results.result_id, Results.checker_result, Results.checker_comment,Results.genotyper_result, Results.genotyper_comment, Qsresult.run_id)\
        .join(Qsresult, Qsresult.qs_result_id==Results.qs_result_id).filter(Qsresult.run_id==run_id)\
        .join(Tests, Tests.test_id==Qsresult.test_id)\
        .join(Samples, Samples.sample_id==Tests.sample_id)\
        .join(Patients, Patients.patient_id==Samples.patient_id)\
        .join(Analyte, Analyte.analyte_id==Tests.analyte_id)\
        .join(Runs, Runs.run_id==Qsresult.run_id).order_by(Samples.sample_name.asc()).all()
    
        exportResults = sorted(final_results, key=lambda final_results: int(final_results.plate_well[1:]))

    ### Get Raw Peak Data ###

        peak_data = s.query(Runs.run_name, Samples.tube_id, Tests.plate_well, Samples.sample_name, Analyte.analyte_id, Analyte.name, Patients.first_name, Patients.sur_name, Tests.plate_well, Raw_peaks.reading, Raw_peaks.temperature, Raw_peaks.fluorescence, Raw_peaks.derivative, Raw_peaks.peak)\
            .join(Qsresult, Qsresult.qs_result_id==Raw_peaks.qs_result_id).filter(Qsresult.run_id==run_id, Raw_peaks.peak == "PEAK")\
            .join(Tests, Tests.test_id==Qsresult.test_id)\
            .join(Samples, Samples.sample_id==Tests.sample_id)\
            .join(Patients, Patients.patient_id==Samples.patient_id)\
            .join(Analyte, Analyte.analyte_id==Tests.analyte_id)\
            .join(Runs, Runs.run_id==Qsresult.run_id).order_by(Samples.sample_name.asc()).all()
        
        peakData = sorted(peak_data, key=lambda peak_data: int(peak_data.plate_well[1:]))

        s.close()

    ### Get Sheets for Exporting ###

        resultsDict = [dict(row) for row in exportResults]
        resultsDF = pd.DataFrame(resultsDict)

        peakDict = [dict(row) for row in peak_data]
        peakDF = pd.DataFrame(peakDict)

        resultsDF.rename(columns={"name": "analyte_name", "run_name" : "worksheet_number"}, inplace=True)
        peakDF.rename(columns={"name": "analyte_name"}, inplace=True)

        # Create unique ID "Sample"
        resultsDF["sample"] = resultsDF["first_name"].str[0] + resultsDF["sur_name"].str[0] + "_" + resultsDF[["sample_name", "analyte_name", "worksheet_number", "plate_well"]].agg("_".join,axis=1)
        peakDF["Sample"] = peakDF["first_name"].str[0] + peakDF["sur_name"].str[0] + "_" + peakDF[["sample_name", "analyte_name", "run_name", "plate_well"]].agg("_".join,axis=1)

        # Split data into seperate worksheets
        genoDF = resultsDF[["sample", 
                            "worksheet_number",
                            "analyte_name", 
                            "genotyper_result", 
                            "genotyper_comment"]]
        
        checkerDF = resultsDF[["sample", 
                               "worksheet_number", 
                               "analyte_name", 
                               "checker_result", 
                               "checker_comment"]]
        
        sampleDF = resultsDF[["first_name", 
                              "sur_name", 
                              "sample_name", 
                              "worksheet_number"]]\
                                .drop_duplicates()
        
        peakDF = peakDF[["Sample", 
                         "plate_well", 
                         "analyte_name", 
                         "reading", 
                         "temperature", 
                         "fluorescence", 
                         "derivative", 
                         "peak"]]


    ### Export as Excel Workbook ###

        filename = ('~/lampapp/LAMP_export_run_' + str(run_id) + '.xlsx')

        xl_writer = pd.ExcelWriter(filename, engine='openpyxl')

        sampleDF.to_excel(xl_writer, sheet_name='Samples', index=False)
        genoDF.to_excel(xl_writer, sheet_name='Genotyper Results', index=False)
        checkerDF.to_excel(xl_writer, sheet_name='Checker Results', index=False)
        peakDF.to_excel(xl_writer, sheet_name='Peak Results', index=False)

        # Auto-adjust column widths
        sheets = ("Samples", "Genotyper Results", "Checker Results", "Peak Results")

        for sheet in sheets:

            for column in xl_writer.sheets[sheet].columns:
                column_letter = column[0].column_letter
                
                max_width = 0
                for cell in column:
                    if len(str(cell.value)) > max_width:
                        max_width = len(cell.value)

                adjusted_width = (max_width + 2) * 1.2

                xl_writer.sheets[sheet].column_dimensions[column_letter].width = adjusted_width
                
        xl_writer.close()

        print('Workbook saved as: ' + filename)  

### Test ###
# 17 complete, 16 "done", 27 not complete
# export_results(17)

s.close()