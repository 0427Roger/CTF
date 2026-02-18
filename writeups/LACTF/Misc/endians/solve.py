import encodings
import pkgutil

# Get all available encodings
all_encodings = set()
for importer, module_name, is_package in pkgutil.iter_modules(encodings.__path__, ''):
    all_encodings.add(module_name)

# Read file and decode using default UTF-8
with open("chall.txt", "rb") as file:
    data = file.read()

text_str = data.decode()

# Try all encoding and decoding combinations
print(f"Testing {len(all_encodings)} encoding combinations...\n")

for encode_type in sorted(all_encodings):
    for decode_type in sorted(all_encodings):
        try:
            result = text_str.encode(encode_type).decode(decode_type)
            if "lactf{" in result:
                print(f"[FOUND] {encode_type} -> {decode_type}")
                print(f"Result: {result}\n")
        except Exception:
            pass
