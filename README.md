# PrinterConnect

## Democratizing access to 3D printers

PrinterConnect is a web application connecting hardware designers,
makers, engineers with 3D printers wherever they are.

It is presently a work in progress and will be available on www.printerconnect.com or www.printerconnect.org.

Long term, PrinterConnects hopes to democratize access to high-resolution 3D printers for just about anybody who has a 
3D model, access to a web browser, and patience to wait for the printing and shipping of their components.

## Contribution

Until the primary features are built, contributing to this repository will be solely done by me.
com).

## Running

For unix computers: 
1. Create a virtual environment: `virtualenv venv --python=python3.8`
2. Run the app: `python app.py`
3. API endpoints: 

## Dependencies

PrinterConnect, in its current state, is a Flask application and depends on several Flask extensions to implement 
its features. These dependencies are listed in ```requirements.txt```.
Its first version will be built in Python 3.8

## Usage
GET `/documentation` lists the REST API description for PrinterConnect
