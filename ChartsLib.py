from psdi.mbo import MboConstants
from psdi.server import MXServer
import io
import sys
import os
import tempfile

mxServer = MXServer.getMXServer()
userInfo = mxServer.getUserInfo("MAXADMIN")

PropSet = MXServer.getMXServer().getMboSet("maxpropvalue", userInfo)
PropSet.setWhere("PROPNAME = 'mxe.pylib.path'")
PropSet.reset()
if PropSet.isEmpty() == False:
    propMbo = PropSet.getMbo(0)
    libpath = str(propMbo.getString("PROPVALUE"))

sys.path.append(libpath)

import matplotlib.pyplot as plt
import numpy as np

def generateAssetCharts(assetMbo):
    try:
        # Generate chart data
        chartData = genChartData(assetMbo)
        
        if chartData:
            # Generate and save chart images
            cdf_image_path = generateChartImage(chartData, 'CDF')
            pdf_image_path = generateChartImage(chartData, 'PDF')
            
            # Attach images to asset
            cdf_attachment_url = attachImageToAsset(assetMbo, cdf_image_path, 'CDF_Chart.png')
            pdf_attachment_url = attachImageToAsset(assetMbo, pdf_image_path, 'PDF_Chart.png')
            
            # Create HTML content with attachment URLs
            htmlContent = """
            <html>
            <head>
                <title>Asset Charts</title>
            </head>
            <body>
                <h1>Asset Charts</h1>
                <h2>Cumulative Distribution Function (CDF)</h2>
                <img src="{cdf_attachment_url}" alt="CDF Chart">
                <h2>Probability Density Function (PDF)</h2>
                <img src="{pdf_attachment_url}" alt="PDF Chart">
            </body>
            </html>
            """.format(cdf_attachment_url=cdf_attachment_url, pdf_attachment_url=pdf_attachment_url)
            
            # Insert HTML content into CHART attribute
            insertHTMLIntoChildTable(assetMbo, htmlContent)
            print("Chart HTML inserted successfully.")
        else:
            print("Chart data is empty. Data insertion skipped.")
    except Exception as e:
        print("Error:", str(e))

def genChartData(assetMbo):
    try:
        # Retrieve data from child table
        futDatesMboSet = assetMbo.getMboSet("AQS_PNOW_FUTDATES")
        futDatesMboSet.setOrderBy("AQS_FUTUREDATE ASC")
        
        # Extract data from child table
        x_values = []
        y1_values = []
        y2_values = []
        for i in range(futDatesMboSet.count()):
            futDateMbo = futDatesMboSet.getMbo(i)
            x_values.append(futDateMbo.getDate("AQS_FUTUREDATE"))
            y1_values.append(futDateMbo.getDouble("AQS_CDF"))
            y2_values.append(futDateMbo.getDouble("AQS_PDF"))
        
        # Prepare chart data
        chartData = {'x': np.array(x_values), 'y1': np.array(y1_values), 'y2': np.array(y2_values)}
        return chartData
    except Exception as e:
        print("Error generating chart data:", str(e))
        return {}

def generateChartImage(chartData, chartType):
    try:
        # Create a new figure
        plt.figure(figsize=(6, 4))
        
        # Plot the data
        plt.plot(chartData['x'], chartData['y1'], label='CDF' if chartType == 'CDF' else 'PDF')
        
        # Add title and labels
        plt.title('{} Chart'.format(chartType))
        plt.xlabel('Date')
        plt.ylabel('Value')
        
        # Add legend
        plt.legend()
        
        # Save the figure to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(temp_file.name)
        plt.close()
        
        return temp_file.name
    except Exception as e:
        print("Error generating {} chart image:".format(chartType), str(e))
        return ''

def attachImageToAsset(assetMbo, image_path, image_name):
    try:
        # Get the attachment set for the asset
        docLinksSet = assetMbo.getMboSet("DOCLINKS")
        docLinksSet.setWhere("OWNERTABLE = 'ASSET' AND OWNERID = {}".format(assetMbo.getLong("ASSETID")))
        docLinksSet.reset()
        
        # Add a new document link
        docLink = docLinksSet.add()
        docLink.setValue("OWNERTABLE", "ASSET")
        docLink.setValue("OWNERID", assetMbo.getLong("ASSETID"))
        docLink.setValue("DOCTYPE", "ATTACHMENT")
        docLink.setValue("URLNAME", image_name)
        
        # Save the attachment file
        with open(image_path, 'rb') as f:
            file_content = f.read()
            docLink.setValue("DOCUMENTDATA", file_content)
        
        docLinksSet.save()
        
        # Return the attachment URL
        return docLink.getString("URLNAME")
    except Exception as e:
        print("Error attaching image to asset:", str(e))
        return ''

def insertHTMLIntoChildTable(assetMbo, htmlContent):
    try:
        if htmlContent:
            # Delete existing records in the child table
            chartTable = assetMbo.getMboSet("AQS_PNOW_CHARTS")
            chartTable.deleteAll()
            
            # Insert HTML content into child table
            chartMbo = chartTable.add()
            chartMbo.setValue("ASSETNUM", assetMbo.getString("ASSETNUM"))
            chartMbo.setValue("SITEID", assetMbo.getString("SITEID"))
            chartMbo.setValue("ORGID", assetMbo.getString("ORGID"))
            chartMbo.setValue("CHART", htmlContent, MboConstants.NOACCESSCHECK)
            chartTable.save()
        else:
            print("HTML content is empty. Skipping data insertion.")
    except Exception as e:
        print("Error inserting HTML into child table:", str(e))

# Call the main function
generateAssetCharts(mbo)
