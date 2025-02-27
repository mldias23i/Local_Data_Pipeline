# Local Data Pipeline with ETL, Testing, and Automation

This project aims to build a local data pipeline that performs the extraction, transformation, and loading (ETL) of data using two Kaggle datasets. The pipeline includes data cleaning, merging terrorism data with country information, testing and version control using Git and Pytest.

## Datasets Used
- **Global Terrorism Dataset**: [Link to Kaggle](https://www.kaggle.com/datasets/ashraykothari/globalterrorismdataset)
- **Countries of the World 2023 Dataset**: [Link to Kaggle](https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023)

## Project Structure
The project is structured into several steps, following the ETL approach:

1. **Extract**: Extract data from CSV files provided by the Kaggle datasets.
2. **Transform**: Clean and transform the data, including merging terrorism data with country information.
3. **Load**: Load the transformed data into a new CSV file.
4. **Testing**: Use Pytest for unit tests related to the functions created.

## How to Run the Project

### 1. Environment Setup
It is recommended to use a virtual environment to ensure that dependencies are managed correctly.

With virtualenv:

```bash
# Install virtualenv
python3 -m venv <virtual_environment_name>

# Create a new virtual environment
source <virtual_environment_name>/bin/activate

# Install dependencies
pip install -r requirements.txt

### 2. Running the Pipeline
After setting up the environment, you can run the pipeline with the following command:

```bash
python kaggle.py

The code will extract the data, transform it, and save the results in a CSV file.

### 3. Running the Tests
To run the tests with Pytest, execute the following command:

```bash
pytest tests.py

This will run the unit tests defined in the tests.py file.

Code Structure
    Important Files:
        kaggle.py: Contains the main ETL code (extraction, transformation, and loading).
        tests.py: File with unit tests to verify the integrity of the code and data.
        requirements.txt: Lists the project dependencies (pandas and pytest).
        .gitignore: File to ignore unwanted files in version control, such as temporary files or the venv directory.

ETL Functionality
    Extract Phase
        The extraction function loads data from the Kaggle-provided CSV datasets (downloaded previously).
        Uses pandas to read CSV files.
    
    Transform Phase
        The transformation phase includes data cleaning, such as removing null values, transforming some columns, and merging terrorism data with country information.

    Load Phase
        The transformed data is written to a new CSV file.
        The load function ensures that the data is readable and well-formatted for other processes or analyses.
    
    Testing
        The project includes automated tests to ensure that the ETL functionality is working correctly.

    Version Control with Git
        The project code is under version control with Git. Below are the basic commands to manage the repository.

        Basic Git Commands
            Add files to the repository:
                ```bash
                git add .
            
            Commit changes:
                ```bash
                git commit -m "Commit message"
        
            Push changes to the remote repository:
                ```bash
                git push origin master
            
            Create a new branch:
                ```bash
                git checkout -b <branch_name>
                
This README provides an overview of your project, how to set it up, run it, and test it. It also covers basic Git usage.