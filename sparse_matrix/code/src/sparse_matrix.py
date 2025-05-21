import os

class SparseMatrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = {}  # key: (row, col), value: non-zero integer

    @staticmethod
    def from_file(filepath):
        try:
            with open(filepath, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]
                if len(lines) < 2 or not lines[0].startswith("rows=") or not lines[1].startswith("cols="):
                    raise ValueError("Input file has wrong format")

                rows = int(lines[0].split("=")[1])
                cols = int(lines[1].split("=")[1])
                matrix = SparseMatrix(rows, cols)

                for line in lines[2:]:
                    line = line.strip()
                    if not (line.startswith("(") and line.endswith(")")):
                        raise ValueError("Input file has wrong format")
                    
                    parts = line[1:-1].split(",")
                    if len(parts) != 3:
                        raise ValueError("Input file has wrong format")
                    
                    r, c, v = map(int, [part.strip() for part in parts])
                    matrix.set_element(r, c, v)
                
                return matrix
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except Exception as e:
            raise ValueError(f"Error reading matrix file: {str(e)}") from e

    def set_element(self, row, col, value):
        if value != 0:
            self.data[(row, col)] = value
        elif (row, col) in self.data:
            del self.data[(row, col)]

    def get_element(self, row, col):
        return self.data.get((row, col), 0)

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match")
        result = SparseMatrix(self.rows, self.cols)
        for key, val in self.data.items():
            result.set_element(*key, val)
        for key, val in other.data.items():
            result.set_element(*key, result.get_element(*key) + val)
        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match")
        result = SparseMatrix(self.rows, self.cols)
        for key, val in self.data.items():
            result.set_element(*key, val)
        for key, val in other.data.items():
            result.set_element(*key, result.get_element(*key) - val)
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions do not allow multiplication")
        result = SparseMatrix(self.rows, other.cols)
        for (r1, c1), v1 in self.data.items():
            for c2 in range(other.cols):
                v2 = other.get_element(c1, c2)
                if v2 != 0:
                    current = result.get_element(r1, c2)
                    result.set_element(r1, c2, current + v1 * v2)
        return result

    def save_to_file(self, filepath):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(f"rows={self.rows}\n")
                f.write(f"cols={self.cols}\n")
                for (r, c), v in sorted(self.data.items()):
                    f.write(f"({r}, {c}, {v})\n")
        except Exception as e:
            raise ValueError(f"Error saving matrix to file: {str(e)}") from e