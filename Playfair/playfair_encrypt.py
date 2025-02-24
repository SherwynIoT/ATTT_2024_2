# Hàm chuyển đổi chuỗi thành chữ thường
def to_lower_case(text):
    return text.lower()

# Hàm loại bỏ tất cả các dấu cách trong chuỗi
def remove_spaces(text):
    new_text = ""
    for char in text:
        if char == " ":
            continue
        else:
            new_text = new_text + char
    return new_text

# Hàm chia chuỗi thành các cặp chữ cái (digraphs)
def create_diagraphs(text):
    digraphs = []
    group_start = 0
    for i in range(2, len(text), 2):
        digraphs.append(text[group_start:i])  # Tạo cặp chữ cái từ chuỗi
        group_start = i
    digraphs.append(text[group_start:])  # Thêm cặp cuối nếu còn lại 1 ký tự
    return digraphs

# Hàm chèn ký tự phụ ('x') vào giữa các chữ cái trùng lặp trong một cặp
def insert_filler_letter(text):
    length = len(text)
    if length % 2 == 0:  # Nếu chuỗi có số lượng ký tự chẵn
        for i in range(0, length, 2):
            if text[i] == text[i+1]:  # Nếu hai ký tự trùng nhau
                new_text = text[:i+1] + 'x' + text[i+1:]  # Thêm 'x' vào giữa
                return insert_filler_letter(new_text)  # Kiểm tra lại
            else:
                return text
    else:  # Nếu chuỗi có số lượng ký tự lẻ
        for i in range(0, length - 1, 2):
            if text[i] == text[i+1]:  # Nếu hai ký tự trùng nhau
                new_text = text[:i+1] + 'x' + text[i+1:]  # Thêm 'x' vào giữa
                return insert_filler_letter(new_text)  # Kiểm tra lại
            else:
                return text
    return text

# Danh sách các ký tự trong bảng chữ cái (trừ 'j')
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Hàm tạo ma trận 5x5 từ khóa
def generate_key_table(keyword, alphabet):
    unique_letters = []  # Danh sách các ký tự duy nhất từ khóa
    for char in keyword:
        if char not in unique_letters:
            unique_letters.append(char)  # Thêm ký tự vào danh sách nếu chưa có

    remaining_letters = []  # Danh sách các ký tự còn lại trong bảng chữ cái
    for char in unique_letters:
        if char not in remaining_letters:
            remaining_letters.append(char)  # Thêm ký tự từ khóa vào
    for char in alphabet:
        if char not in remaining_letters:
            remaining_letters.append(char)  # Thêm các ký tự còn lại vào

    matrix = []  # Ma trận 5x5
    while remaining_letters:
        matrix.append(remaining_letters[:5])  # Chia các ký tự thành các hàng
        remaining_letters = remaining_letters[5:]  # Cắt 5 ký tự sau khi đã thêm vào một hàng

    return matrix

# Hàm tìm vị trí của một ký tự trong ma trận
def search_in_matrix(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:  # Nếu tìm thấy ký tự trong ma trận
                return row, col

# Hàm mã hóa theo quy tắc cùng hàng trong ma trận
def encrypt_row_rule(matrix, row1, col1, row2, col2):
    char1 = matrix[row1][(col1 + 1) % 5]  # Di chuyển sang cột tiếp theo (vòng lại nếu cần)
    char2 = matrix[row2][(col2 + 1) % 5]  # Di chuyển sang cột tiếp theo (vòng lại nếu cần)
    return char1, char2

# Hàm mã hóa theo quy tắc cùng cột trong ma trận
def encrypt_column_rule(matrix, row1, col1, row2, col2):
    char1 = matrix[(row1 + 1) % 5][col1]  # Di chuyển xuống hàng tiếp theo (vòng lại nếu cần)
    char2 = matrix[(row2 + 1) % 5][col2]  # Di chuyển xuống hàng tiếp theo (vòng lại nếu cần)
    return char1, char2

# Hàm mã hóa theo quy tắc hình chữ nhật trong ma trận
def encrypt_rectangle_rule(matrix, row1, col1, row2, col2):
    char1 = matrix[row1][col2]  # Ký tự ở góc đối diện trên cùng hàng
    char2 = matrix[row2][col1]  # Ký tự ở góc đối diện trên cùng cột
    return char1, char2

# Hàm mã hóa văn bản theo Playfair Cipher
def playfair_encrypt(matrix, digraphs):
    ciphertext = []  # Danh sách chứa các ký tự mã hóa
    for pair in digraphs:  # Duyệt qua từng cặp chữ cái
        row1, col1 = search_in_matrix(matrix, pair[0])  # Tìm vị trí của chữ cái đầu tiên
        row2, col2 = search_in_matrix(matrix, pair[1])  # Tìm vị trí của chữ cái thứ hai

        if row1 == row2:  # Nếu hai chữ cái nằm cùng hàng
            char1, char2 = encrypt_row_rule(matrix, row1, col1, row2, col2)
        elif col1 == col2:  # Nếu hai chữ cái nằm cùng cột
            char1, char2 = encrypt_column_rule(matrix, row1, col1, row2, col2)
        else:  # Nếu hai chữ cái tạo thành một hình chữ nhật
            char1, char2 = encrypt_rectangle_rule(matrix, row1, col1, row2, col2)

        ciphertext.append(char1 + char2)  # Thêm cặp mã hóa vào danh sách

    return ciphertext

# Nhập văn bản gốc
plaintext = 'happybirdthday'
plaintext = remove_spaces(to_lower_case(plaintext))  # Chuyển sang chữ thường và loại bỏ khoảng trắng
digraphs = create_diagraphs(insert_filler_letter(plaintext))  # Tạo các cặp chữ cái

# Đảm bảo cặp cuối cùng có đủ 2 ký tự
if len(digraphs[-1]) != 2:
    digraphs[-1] += 'z'

# Khóa để tạo ma trận
key = "Cake"
key = to_lower_case(key)

# Tạo ma trận khóa
key_matrix = generate_key_table(key, alphabet)

# Mã hóa văn bản gốc
ciphertext_list = playfair_encrypt(key_matrix, digraphs)

# Kết quả mã hóa
ciphertext = ''.join(ciphertext_list)

# In ra kết quả
print("Khóa:", key)
print("Văn bản gốc:", plaintext)
print("Văn bản mã hóa:", ciphertext)
