# ICC Composer

**ICC Composer** is a software developed in collaboration with Inmetro researcher Mauro Vieira de Lima. 

The tool automates access to the BIPM Time Department API Web Service and merges collected JSON data with laboratory administrative data to create a WORD/PDF file compliant with the ICC (Inmetro Calibration Certificate). 
The Inmetro calibration certificate template is defined and maintained by the Inmetro Quality System, which has a Microsoft WORD template of this model. The software we developed uses a Python library called ***docxtpl*** to populate the Inmetro Calibration Certificate WORD template with the combined data and, as a result, automatically generates a PDF file of the Inmetro Calibration Certificate that is in full compliance with the definitions of the Inmetro Quality System.

***Note: Due to security concerns, this code do not contain the full features used in laboratory***

# Getting Started

## Install and Run Dependencies

If you have just downloaded the project and it fails due to missing modules, you may need to install its requirements first:

1. Install dependencies: python -m pip install -r requirements.txt.
2. Run the script: python ICC_Composer_From_Template.py
