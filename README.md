# PrinterConnect

## Democratizing access to 3D printers

PrinterConnect is a web application connecting hardware designers,
makers, engineers with 3D printers wherever they are.

It is presently a work in progress.

Long term, PrinterConnects hopes to democratize access to high-resolution 3D printers for just about anybody who has a 
3D model, access to a web browser, and patience to wait for the printing and shipping of their components.

## Contribution

Until the primary features are built, contributing to this repository will be solely done by me.

## Running

For unix computers: 
1. Clone the repo and `cd` into the project directory
2. Create a virtual environment: `virtualenv venv --python=python3.8`
3. Activate virtual environment: `source venv/bin/activate`
4. Install project dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`
4. API endpoints: `GET /documentation` for a list of the API endpoints

## Dependencies

PrinterConnect, in its current state, is a Flask application and depends on several Flask extensions to implement 
its features. These dependencies are listed in `requirements.txt`.
Its first version will be built in Python 3.8

## Usage (WIP)
GET `/documentation` previews some of PrinterConnect's APIs. They will be updated over time. 
