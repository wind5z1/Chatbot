import re
import math
import operator as op

operators = {
    "+" : op.add,
    "-" : op.sub,
    "*" : op.mul,
    "/" : op.truediv,
    "**" : op.pow
}
math_functions = {
    "sin" : math.sin,
    "cos" : math.cos,
    "tan" : math.tan,
    "sqrt" : math.sqrt,
    "log" : math.log,
    "log10" : math.log10,
    "exp" : math.exp
}

def calculate_expression(expression):
    try:
        expression = expression.replace(" ", "")  # 去掉所有空格

        # 將百分比轉換為小數
        expression = re.sub(r'(\d+)%', lambda m: str(float(m.group(1)) / 100), expression)
        
        # 將 "of" 轉換為 "*"
        expression = expression.replace("of", "*")
        
        if not re.match(r'^[\d+\-*/().% sqrt sincostanlog]+$', expression):
            return "Invalid expression. Please enter a valid mathematical expression."

        # 使用 eval 進行計算
        result = eval(expression, {"__builtins__": None}, {**operators, **math_functions})
        return f"The result is: {result}"
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        return f"Error calculating expression: {str(e)}"
