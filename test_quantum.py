from logic import QuantumOmniTool, provider

# 1. Initialize the tool with the provider we created
tool = QuantumOmniTool(provider)

# 2. Generate a small 3x3 grid (9 qubits total)
# This should create a 3x3 grid of qubits for the simulation; expects generate_grid to accept 'count' as the grid size.
print("Generating 3x3 grid...")
tool.generate_grid(count=3)
print("Generating 3x3 grid...")
tool.generate_grid(count=3)
# 3. Run the simulation on the Rigetti Simulator
# The 'shielding' parameter controls the level of noise protection applied during the simulation (e.g., 0.5 means moderate shielding).
print("Submitting jobs to Rigetti Cloud...")
results = tool.run_simulation(shielding=0.5)
results = tool.run_simulation(shielding=0.5)

print(f"Simulation Complete! Results: {results}")