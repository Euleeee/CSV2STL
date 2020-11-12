#Author-Nathan Hardenberg and Jonathan Mueller
#Description-Import parameters from a .csv file and create a .stl model with the new parameters 

import adsk.core, adsk.fusion, traceback
import io
import csv

def run(context):
    ui = None
    try:
        # define variables
        app = adsk.core.Application.get() 
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        product = app.activeProduct
        rootComp = design.rootComponent

         # create a explorer window to choose a .csv file
        dlg = ui.createFileDialog() 
        dlg.title = 'Open CSV File'  
        dlg.filter = 'Comma Separated Values (*.csv);;All Files (*.*)'

        # if the user chose 'Cancel' -> return 
        if dlg.showOpen() != adsk.core.DialogResults.DialogOK :  
            ui.messageBox('Canceld. Start the script again.')
            return

        # extract filename
        filename = dlg.filename  

        # read csv file and copy the parameters to a new variable
        contentCSV = []
        with open(filename) as csvdatei:  
            parameterCSV = csv.reader(csvdatei)
            for row in parameterCSV:  
                contentCSV.append(row)
        
        # change parameters of the part
        for row in contentCSV:
            try:
                paramName = row[0]
                paramVal = row[1]
                design.allParameters.itemByName(paramName).expression = paramVal
            except:
                pass
            
        # export new part as stl file
        filenameNew = filename[:-3] + 'stl'
        exportMgr = adsk.fusion.ExportManager.cast(design.exportManager)
        stlOptions = exportMgr.createSTLExportOptions(rootComp)
        stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        stlOptions.filename = filenameNew
        exportMgr.execute(stlOptions)
                
        ui.messageBox('Finished.')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))