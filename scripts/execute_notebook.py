import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

notebook_path = '/Users/ashok/Documents/CLV/kenvue_analytics_master_project.ipynb'

def run_notebook():
    try:
        print(f"Reading notebook: {notebook_path}")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        # Configure the execution preprocessor
        # timeout=-1 means no timeout
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

        print("Executing notebook... this may take a moment.")
        # Run the notebook in the context of its own directory
        ep.preprocess(nb, {'metadata': {'path': '/Users/ashok/Documents/CLV'}})

        print(f"Writing executed notebook back to: {notebook_path}")
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        
        print("Notebook execution complete. Outputs populated.")

    except Exception as e:
        print(f"Error executing notebook: {e}")
        # If execution fails, it might be due to missing dependencies in the environment
        # or data paths. We've already verified the script run, so this is just for 
        # populating the UI.

if __name__ == '__main__':
    run_notebook()
