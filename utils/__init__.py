cookies = {}
with open(".env") as f:
    for line in f:
        name, value = line.strip().split("=", 1)
        cookies[name] = value
