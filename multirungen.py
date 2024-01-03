import os

print("\n/// Generating SACS Multi run file...\n")

# Specify the folder where you want to search for .runx files
folder_path = os.getcwd()+os.sep+'GEN'  # Use the current working directory as the base folder

# Create a .runx file
runx_script_path = folder_path+os.sep+'run_all.runx'

# Open the .runx file for writing
with open(runx_script_path, 'w') as runx_file:
    runx_file.write('Rem RunParallel\n')
    runx_file.write('Rem Runmulti file run_all.runx\n')
    # Iterate through all directories and subdirectories in the specified folder
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # Check if the file ends with ".runx"
            if filename.endswith('.runx') and '_all' not in filename:
                # Get the full path of the .runx file
                runx_file_path = os.path.join(root, filename)
                # Generate the commands to run the .runx file and write them to the .runx script
                folder_name = os.path.basename(root)
                print('-- ',folder_name)
                runx_file.write(f'Echo "Running {runx_file_path}"\n')
                runx_file.write(f'call {runx_file_path}\n')
    runx_file.write('PAUSE')
print ('')
