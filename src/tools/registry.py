from .python_tool import python_tool
from .calculator_tool import calculator_tool
from .memory_tool import memory_tool

TOOL_REGISTRY = {
    "python": python_tool,
    "calculator": calculator_tool,
    "memory": memory_tool,
}