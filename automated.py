# automated.py
import os
import datetime

def create_project_structure():
    """
    This script automatically generates the empty folder and file structure
    for the Traffic Light Detection project.

    Generated at: Kattankulathur, Tamil Nadu
    """
    
    project_name = "traffic-light-detection"
    
    # Define the directory structure
    directories = [
        project_name,
        os.path.join(project_name, "src"),
        os.path.join(project_name, "templates"),
        os.path.join(project_name, "data", "videos")
    ]
    
    # Define the empty files to be created within the structure
    empty_files = [
        os.path.join(project_name, ".gitignore"),
        os.path.join(project_name, "Dockerfile"),
        os.path.join(project_name, "README.md"),
        os.path.join(project_name, "requirements.txt"),
        os.path.join(project_name, "src", "__init__.py"),
        os.path.join(project_name, "src", "detector.py"),
        os.path.join(project_name, "src", "app.py"),
        os.path.join(project_name, "templates", "index.html")
    ]
    
    # --- Script Execution ---
    
    print(f"Initializing project scaffolding for '{project_name}'...")
    timestamp = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    print(f"Timestamp: {timestamp} (IST)")
    print("-" * 40)

    # Create directories
    for dir_path in directories:
        try:
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created directory: {dir_path}")
        except OSError as e:
            print(f"Error creating directory {dir_path}: {e}")
            return # Stop execution if a directory can't be made

    # Create empty files
    for file_path in empty_files:
        try:
            # open() in 'w' mode creates a file if it doesn't exist.
            # The 'with' statement ensures it's properly closed.
            with open(file_path, 'w') as f:
                pass # The file is created empty
            print(f"Created empty file:  {file_path}")
        except IOError as e:
            print(f"Error creating file {file_path}: {e}")

    print("-" * 40)
    print("Project structure created successfully!")
    print("\nYou can now start adding your code to the generated files.")


if __name__ == "__main__":
    create_project_structure()