from sparse_matrix import SparseMatrix
import os

def main():
    print("1. Add\n2. Subtract\n3. Multiply")
    choice = input("Choose operation (1-3): ")

    pathA = input("Enter path to first matrix file: ").strip()
    pathB = input("Enter path to second matrix file: ").strip()

    # Normalize paths for cross-platform compatibility
    pathA = os.path.normpath(pathA)
    pathB = os.path.normpath(pathB)

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

        output_path = input("Enter the path to save the result (e.g., output.txt): ").strip()
        output_path = os.path.normpath(output_path)
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        result.save_to_file(output_path)
        print(f"✅ Result saved to {output_path}")

    except ValueError as ve:
        print("❌ Error:", ve)
    except FileNotFoundError:
        print("❌ One of the input files was not found.")
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
if __name__ == "__main__":
    main()