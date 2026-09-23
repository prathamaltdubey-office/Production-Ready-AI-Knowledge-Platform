from agent.tools.python_repl import python_repl

# Test 1: Should work fine — safe calculation
print("=== TEST 1: Safe calculation ===")
result = python_repl.invoke({"code": "result = sum([x**2 for x in range(1, 11)])"})
print(result)

# Test 2: Should be BLOCKED — file access attempt
print("\n=== TEST 2: Blocked file access ===")
result = python_repl.invoke({"code": "result = open('secrets.txt').read()"})
print(result)

# Test 3: Should be BLOCKED — import attempt
print("\n=== TEST 3: Blocked import ===")
result = python_repl.invoke({"code": "import os\nresult = os.getcwd()"})
print(result)

# Test 4: Should be BLOCKED — os module reference
print("\n=== TEST 4: Blocked os reference ===")
result = python_repl.invoke({"code": "result = os.system('dir')"})
print(result)
