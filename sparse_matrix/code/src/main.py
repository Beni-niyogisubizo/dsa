from sparse_matrix import SparseMatrix
import os

def get_input_path(filename):
    """Get correct path to sample_inputs, handling both full and relative paths"""
    # Remove any leading/trailing quotes or spaces
    filename = filename.strip('"\' ')
    
    # If user provides full path, use it directly
    if os.path.isabs(filename):
        return filename
    
    # If path already contains 'sample_inputs', use it as-is
    if 'sample_inputs' in filename.replace('\\', '/'):
        return os.path.normpath(filename)
    
    # Otherwise, resolve relative to sample_inputs folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_dir = os.path.join(project_root, "sample_inputs")
    return os.path.join(input_dir, filename)

def main():
    print("1. Add\n2. Subtract\n3. Multiply")
    choice = input("Choose operation (1-3): ")

    file1 = input("Enter first matrix filename or path (e.g., easy_sample_01_2.txt): ")
    file2 = input("Enter second matrix filename or path (e.g., easy_sample_01_2.txt): ")
    
    pathA = get_input_path(file1)
    pathB = get_input_path(file2)

    print(f"\nResolved paths:")
    print(f"- File 1: {pathA}")
    print(f"- File 2: {pathB}\n")

    try:
        A = SparseMatrix.from_file(pathA)
        B = SparseMatrix.from_file(pathB)

        if choice == "1":
            result = A.add(B)
        elif choice == "2":
            result = A.subtract(B)
        elif choice == "3":
            result = A.multiply(B)
        else:
            print("❌ Invalid choice.")
            return

        output_path = input("Enter output filename (e.g., result.txt): ").strip()
        output_path = os.path.join(os.path.dirname(__file__), output_path)
        
        result.save_to_file(output_path)
        print(f"✅ Result saved to {os.path.abspath(output_path)}")

    except ValueError as ve:
        print(f"❌ Error: {ve}")
    except FileNotFoundError:
        print(f"❌ File not found. Verify these paths exist:\n{pathA}\n{pathB}")
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    main()