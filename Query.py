import mysql.connector
from Encryption import encrypt_song
from Decryption import decrypt_song

def get_song_data(song_id):
    # Kết nối đến cơ sở dữ liệu
    connection = mysql.connector.connect(
        host="your_mysql_host",
        user="your_mysql_user",
        password="your_mysql_password",
        database="your_mysql_database"
    )
    cursor = connection.cursor()

    # Truy vấn dữ liệu bài hát từ cơ sở dữ liệu
    select_query = "SELECT dataPath FROM AudioFile WHERE songID = %s"
    cursor.execute(select_query, (song_id,))
    result = cursor.fetchone()

    connection.close()

    return result[0] if result else None

def main():
    # Người dùng chọn ID của bài hát
    song_id = int(input("Nhập ID của bài hát: "))

    # Lấy đường dẫn đến file âm thanh từ cơ sở dữ liệu
    audio_file_path = get_song_data(song_id)

    if audio_file_path:
        # Mã hoá bài hát
        key = generate_key()
        with open(audio_file_path, "rb") as file:
            plaintext_data = file.read()

        # Tách thành các chunk và mã hoá từng chunk
        chunks = [plaintext_data[i:i + 1024] for i in range(0, len(plaintext_data), 1024)]
        encrypted_chunks = [encrypt_song(key, chunk) for chunk in chunks]

        # Gửi key và bản mã theo từng chunk đến người dùng
        for i, encrypted_chunk in enumerate(encrypted_chunks):
            print(f"Chunk {i + 1} - Encrypted: {encrypted_chunk}")

        # Người dùng giải mã và nghe bài hát ở đây

    else:
        print("Không tìm thấy bài hát.")

if __name__ == "__main__":
    main()
