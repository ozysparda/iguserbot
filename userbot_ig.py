import instaloader
import time
from instaloader.exceptions import ConnectionException

USERNAME = "yournextmistake"
PASSWORD = "ozyganteng132"

# Inisialisasi dan login
bot = instaloader.Instaloader()
bot.login(USERNAME, PASSWORD)

# Mengambil profil
profile = instaloader.Profile.from_username(bot.context, USERNAME)

def get_followers(profile):
    """Fungsi untuk mendapatkan daftar followers dengan penanganan exception."""
    while True:
        try:
            return {f.username for f in profile.get_followers()}
        except ConnectionException as e:
            print("Error saat mengambil followers:", e)
            print("Menunggu 5 menit sebelum mencoba lagi...")
            time.sleep(300)  # Tunggu 300 detik (5 menit)

def get_following(profile):
    """Fungsi untuk mendapatkan daftar yang di-follow dengan penanganan exception."""
    while True:
        try:
            return {f.username for f in profile.get_followees()}
        except ConnectionException as e:
            print("Error saat mengambil following:", e)
            print("Menunggu 5 menit sebelum mencoba lagi...")
            time.sleep(300)  # Tunggu 300 detik (5 menit)

# Ambil data followers dan following
print("Mengambil daftar followers...")
followers = get_followers(profile)
print(f"Ditemukan {len(followers)} followers.")

print("Mengambil daftar following...")
following = get_following(profile)
print(f"Ditemukan {len(following)} following.")

# Cari akun yang tidak follow balik
not_following_back = following - followers

print(f"Akan di-unfollow {len(not_following_back)} akun yang tidak follow balik.")

# Unfollow akun satu per satu dengan delay agar tidak kena rate limit
for username in not_following_back:
    print(f"Unfollowing: {username}")
    try:
        bot.context.username_unfollow(username)
        print(f"Berhasil unfollow {username}")
    except Exception as e:
        print(f"Gagal unfollow {username} karena: {e}")
    time.sleep(5)  # Delay 5 detik antar unfollow

print("✅ Selesai Unfollow yang Tidak Follow Balik!")
