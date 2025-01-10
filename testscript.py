import pandas as pd
import sys 
import json

# Check which Python path is being used
# The path can be different if the script is run directly in Python vs from Node process
print(sys.path)

# Read data from stdin
data = sys.stdin.read()

# Parse the JSON string
array_received = json.loads(data)

print("Array received:", array_received)



# Create a DataFrame
df = pd.DataFrame(array_received)
print(df)

df.to_csv('test.csv', index=False) 



