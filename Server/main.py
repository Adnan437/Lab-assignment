import os
import shutil
import zipfile
import subprocess

source_directory = 'source_directory'
destination_directory = 'destination_directory'

# Copying files and modifying line count
for root, dirs, files in os.walk(source_directory):
    for filename in files:
        if filename.endswith('.txt'):
            src_path = os.path.join(root, filename)
            dst_path = os.path.join(destination_directory, filename)

            # Count the lines in the source file
            with open(src_path, 'r') as src_file:
                line_count = sum(1 for _ in src_file)

            # Create new file with modified line count
            with open(dst_path, 'w') as dst_file:
                for i in range(line_count, 0, -10):
                    dst_file.write(f'Line {i}\n')

        elif filename.endswith('.py'):
            file_path = os.path.join(root, filename)

            # Run Python files and capture output and errors
            try:
                result = subprocess.run(['python', file_path], capture_output=True, text=True, check=True)
                output = result.stdout
                errors = result.stderr
            except subprocess.CalledProcessError as e:
                output = ''
                errors = e.stderr

            # Save output and errors to files
            output_path = os.path.join(destination_directory, f'{filename}_output.txt')
            errors_path = os.path.join(destination_directory, f'{filename}_errors.txt')

            with open(output_path, 'w') as output_file:
                output_file.write(output)

            with open(errors_path, 'w') as errors_file:
                errors_file.write(errors)

# Create a ZIP file of the destination directory
zip_path = os.path.join(destination_directory, 'converted_files.zip')
with zipfile.ZipFile(zip_path, 'w') as zip_file:
    for root, dirs, files in os.walk(destination_directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            zip_file.write(file_path, os.path.relpath(file_path, destination_directory))

# Unzip the ZIP file in the destination directory
unzip_directory = os.path.join(destination_directory, 'unzipped_files')
with zipfile.ZipFile(zip_path, 'r') as zip_file:
    zip_file.extractall(unzip_directory)
