import json

print(json.dumps([(x*2+25, y*2+13) for x in range(3) for y in range(4)]))