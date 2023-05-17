import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def _init_(self, value):
        self.value = value
        self.left = None
        self.right = None

class Compiler:
    def _init_(self, expression):
        self.expression = expression
        self.temp_count = 0
        self.code = []
        self.graph = nx.DiGraph()

    def generate_code_and_graph(self):
        self.temp_count = 0
        self.code = []
        self.graph = nx.DiGraph()
        self.root = self.expr()
        self.graph.add_node(self.root.value)
        self.traverse(self.root)

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def emit(self, op, arg1, arg2, result):
        self.code.append((op, arg1, arg2, result))

    def traverse(self, node):
        if node.left:
            self.graph.add_edge(node.value, node.left.value)
            self.traverse(node.left)
        if node.right:
            self.graph.add_edge(node.value, node.right.value)
            self.traverse(node.right)

    def expr(self):
        node = self.term()

        while self.expression and self.expression[0] in ('+', '-'):
            op = self.expression.pop(0)
            right = self.term()
            result = Node(self.new_temp())
            result.left = node
            result.right = right
            node = result
            self.emit(op, node.left.value, node.right.value, node.value)

        return node

    def term(self):
        node = self.factor()

        while self.expression and self.expression[0] in ('*', '/'):
            op = self.expression.pop(0)
            right = self.factor()
            result = Node(self.new_temp())
            result.left = node
            result.right = right
            node = result
            self.emit(op, node.left.value, node.right.value, node.value)

        return node

    def factor(self):
        if self.expression[0].isdigit():
            result = Node(self.expression.pop(0))
            return result
        elif self.expression[0] == '(':
            self.expression.pop(0)
            result = self.expr()
            self.expression.pop(0)
            return result
        else:
            raise ValueError("Invalid expression")

def main():
    expression = input("Enter an arithmetic expression: ")
    compiler = Compiler(list(expression))
    compiler.generate_code_and_graph()

    for op, arg1, arg2, result in compiler.code:
        if arg2 is not None:
            print(f"{result} = {arg1} {op} {arg2}")
        else:
            print(f"{result} = {op} {arg1}")

    nx.draw_networkx(compiler.graph, with_labels=True)
    plt.show()

if _name_ == '_main_':
    main()
