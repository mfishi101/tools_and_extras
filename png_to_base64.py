import base64
from pathlib import Path

def png_jpg_to_base64_src(file_path):
    """
    Load a PNG/JPG file and return its contents as a base64 string ready for HTML img src.
    
    Args:
        file_path (str): Path to the PNG/JPG file
        
    Returns:
        str: The base64 string formatted for HTML img src, or None if error occurs
    """
    try:
        path = Path(file_path)
        if not path.exists():
            print(f"Error: File '{file_path}' not found.")
            return None

            
        with open(path, 'rb') as file:
            bytes_data = file.read()
            base64_data = base64.b64encode(bytes_data).decode('ascii')
            return f"data:image/png;base64,{base64_data}"
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

def main():
    
    file_path = 'tfs1.png'
    base64_src = png_jpg_to_base64_src(file_path)
    
    if base64_src:
        print("Write image to file:")
        with open('output.txt', 'w') as file:
            file.write(base64_src)

if __name__ == "__main__":
    main()