def add(a, b):
    """
    Add two numbers together.
    
    Args:
        a (int): The first number.
        b (int): The second number.
    
    Returns:
        int: The sum of the two numbers.
    """
    return a + b

def subtract(a, b):
    """
    Subtract one number from another.
    
    Args:
        a (int): The number to subtract from.
        b (int): The number to subtract.
    
    Returns:
        int: The difference of the two numbers.
    """
    return a - b

def multiply(a, b):
    """
    Multiply two numbers together.
    
    Args:
        a (int): The first number.
        b (int): The second number.
    
    Returns:
        int: The product of the two numbers.
    """
    return a * b

def divide(a, b):
    """
    Divide one number by another.
    
    Args:
        a (int): The number to divide.
        b (int): The number to divide by.
    
    Returns:
        float: The quotient of the two numbers.
    
    Raises:
        ValueError: If the second number is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    print("Addition of 5 and 3 is:", add(5, 3))
    print("Subtraction of 5 from 8 is:", subtract(8, 5))
    print("Multiplication of 5 and 3 is:", multiply(5, 3))
    print("Division of 10 by 2 is:", divide(10, 2))
