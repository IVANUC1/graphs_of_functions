import json

functions = [
    {"funk": "2*sqrt(2)*sin(x)*cos(x)-cos(x)-sin(x)", "color": [255, 0, 0], "show": True},
    {"funk": "tanh(x)*2", "color": [0, 255, 0], "show": False},
    {"funk": "5*x", "color": [0, 0, 255], "show": False},
    {"funk": "x**2/25", "color": [255, 255, 0], "show": False}
]

with open('functions.json', 'w', encoding='utf-8') as f:
    json.dump(functions, f, ensure_ascii=False, indent=4)
