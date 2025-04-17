import re
import math
import operator as op

# 演算子（加減乘除、べき乗）を定義
operators = {
    "+" : op.add,
    "-" : op.sub,
    "*" : op.mul,
    "/" : op.truediv,
    "**" : op.pow
}

# 数学関数（三角関数、平方根、対数、指数）を定義
math_functions = {
    "sin" : math.sin,
    "cos" : math.cos,
    "tan" : math.tan,
    "sqrt" : math.sqrt,
    "log" : math.log,
    "log10" : math.log10,
    "exp" : math.exp
}

# 数式を評価して結果を返す関数
def calculate_expression(expression):
    try:
        # 式中の空白をすべて削除
        expression = expression.replace(" ", "")

        # パーセンテージ（%）を小数に変換（例：50% → 0.5）
        expression = re.sub(r'(\d+)%', lambda m: str(float(m.group(1)) / 100), expression)

        # "of" を乗算（*）に置き換え（例：50% of 200 → 0.5 * 200）
        expression = expression.replace("of", "*")

        # 数式の形式が正しいかをチェック（英字や記号が許可されたものだけかどうか）
        if not re.match(r'^[\d+\-*/().% sqrt sincostanlog]+$', expression):
            return "Error: Invalid expression format."

        # eval 関数で式を評価（安全のためビルトイン関数は無効化）
        result = eval(expression, {"__builtins__": None}, {**operators, **math_functions})
        return f"Result: {result}"
    
    # 0 で割った場合のエラー処理
    except ZeroDivisionError:
        return "Error: Unable to divide by zero."
    
    # その他のエラー処理
    except Exception as e:
        return f"Error in calculation: {str(e)}"
