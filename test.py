def read_file(filename):
    data = ""
    with open(filename, "r") as file_obj:
        data = file_obj.read()
    return data

file_data = ["", ""]
print("Hello, world!")

file_data[0] = read_file("test")
for i in range(0, 20):
    val = hex(ord(file_data[0][i]))[2:]
    if len(val) < 2:
        val = '0' + val

    if val == "00":
        print("SAME: " + val)
    else:
        print(val)
