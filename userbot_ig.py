import instaloader
import time
import os
import json
from instaloader.exceptions import ConnectionException

# ============== CONFIG ==============
USERNAME = "yournextmistake"
PASSWORD = "ozyganteng132"
WHITELIST_FILE = "whitelist.json"
# ====================================

# Inisialisasi
bot = instaloader.Instaloader()

# Load whitelist jika ada
def load_whitelist():
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, 'r') as f:
            return json.load(f)
    return []

def save_whitelist(whitelist):
    with open(WHITELIST_FILE, 'w') as f:
        json.dump(whitelist, f)

def login():
    try:
        bot.login(USERNAME, PASSWORD)
        print("✓ Login berhasil!")
        return True
    except Exception as e:
        print(f"✗ Login gagal: {e}")
        return False

def get_profile():
    return instaloader.Profile.from_username(bot.context, USERNAME)

def get_followers(profile):
    while True:
        try:
            return {f.username for f in profile.get_followers()}
        except ConnectionException as e:
            print("Error:", e)
            print("Menunggu 5 menit...")
            time.sleep(300)

def get_following(profile):
    while True:
        try:
            return {f.username for f in profile.get_followees()}
        except ConnectionException as e:
            print("Error:", e)
            print("Menunggu 5 menit...")
            time.sleep(300)

def show_menu():
    print("\n" + "="*40)
    print("       IG USERBOT")
    print("="*40)
    print("1. Lihat yang tidak follow back")
    print("2. Unfollow yang tidak follow back")
    print("3. Whitelist (akun aman)")
    print("4. Statistik")
    print("5. Refresh data")
    print("6. Keluar")
    print("="*40)

def show_not_following_back(not_following, whitelist):
    print(f"\n{'='*40}")
    print(f"  AKUN TIDAK FOLLOW BACK ({len(not_following)})")
    print(f"{'='*40}")
    
    count = 0
    for username in sorted(not_following):
        if username not in whitelist:
            count += 1
            print(f"  {count}. @{username}")
    
    print(f"\n  Total: {count} akun (dari {len(not_following)} tidak follow back)")
    print(f"  Whitelist: {len(whitelist)} akun")

def unfollow_accounts(not_following, whitelist, dry_run=False):
    to_unfollow = [u for u in not_following if u not in whitelist]
    
    if not to_unfollow:
        print("\n✓ Tidak ada akun yang perlu di-unfollow!")
        return
    
    print(f"\n{'='*40}")
    if dry_run:
        print(f"  DRY RUN - {len(to_unfollow)} akun akan di-unfollow")
    else:
        print(f"  UNFOLLOW - {len(to_unfollow)} akun")
    print(f"{'='*40}")
    
    for i, username in enumerate(to_unfollow, 1):
        print(f"  [{i}/{len(to_unfollow)}] @{username}", end="")
        
        if not dry_run:
            try:
                bot.context.username_unfollow(username)
                print(" ✓")
            except Exception as e:
                print(f" ✗ {e}")
            time.sleep(5)
        else:
            print(" (skip)")
    
    if not dry_run:
        print(f"\n✓ Selesai unfollow {len(to_unfollow)} akun!")
    else:
        print(f"\n✓ Dry run selesai. Tidak ada yang di-unfollow.")

def manage_whitelist(not_following, whitelist):
    while True:
        print(f"\n{'='*40}")
        print(f"  WHITELIST MANAGEMENT")
        print(f"{'='*40}")
        print(f"  Whitelist saat ini: {len(whitelist)} akun")
        if whitelist:
            for u in sorted(whitelist):
                print(f"    - @{u}")
        print(f"{'='*40}")
        print("1. Tambah ke whitelist")
        print("2. Hapus dari whitelist")
        print("3. Kembali")
        
        choice = input("\nPilihan: ").strip()
        
        if choice == "1":
            username = input("Username (tanpa @): ").strip()
            if username and username not in whitelist:
                whitelist.append(username)
                save_whitelist(whitelist)
                print(f"✓ @{username} ditambahkan ke whitelist")
            else:
                print("✗ Username sudah ada atau invalid")
        
        elif choice == "2":
            username = input("Username (tanpa @): ").strip()
            if username in whitelist:
                whitelist.remove(username)
                save_whitelist(whitelist)
                print(f"✓ @{username} dihapus dari whitelist")
            else:
                print("✗ Username tidak ada di whitelist")
        
        elif choice == "3":
            break

def show_stats(followers, following, not_following, whitelist):
    safe_unfollow = len(not_following) - len([u for u in not_following if u in whitelist])
    
    print(f"\n{'='*40}")
    print(f"  STATISTIK AKUN")
    print(f"{'='*40}")
    print(f"  Followers      : {len(followers)}")
    print(f"  Following      : {len(following)}")
    print(f"  Tidak FB       : {len(not_following)}")
    print(f"  Whitelist      : {len(whitelist)}")
    print(f"  Bisa Unfollow  : {safe_unfollow}")
    
    ratio = len(followers) / len(following) * 100 if following else 0
    print(f"  Rasio Follow   : {ratio:.1f}%")
    print(f"{'='*40}")

def main():
    print("="*40)
    print("       IG USERBOT")
    print("="*40)
    print("Loading...")
    
    if not login():
        return
    
    profile = get_profile()
    
    # Load whitelist
    whitelist = load_whitelist()
    
    # Ambil data awal
    print("\nMengambil data...")
    followers = get_followers(profile)
    following = get_following(profile)
    not_following = following - followers
    
    print(f"✓ Followers: {len(followers)}")
    print(f"✓ Following: {len(following)}")
    print(f"✓ Tidak FB: {len(not_following)}")
    
    while True:
        show_menu()
        choice = input("Pilihan: ").strip()
        
        if choice == "1":
            show_not_following_back(not_following, whitelist)
        
        elif choice == "2":
            print("\n1. Dry run (lihat saja)")
            print("2. Unfollow langsung")
            sub = input("Pilihan: ").strip()
            
            if sub == "1":
                unfollow_accounts(not_following, whitelist, dry_run=True)
            elif sub == "2":
                confirm = input(f"Yakin unfollow {len([u for u in not_following if u not in whitelist])} akun? (y/n): ").strip()
                if confirm.lower() == 'y':
                    unfollow_accounts(not_following, whitelist, dry_run=False)
        
        elif choice == "3":
            manage_whitelist(not_following, whitelist)
        
        elif choice == "4":
            show_stats(followers, following, not_following, whitelist)
        
        elif choice == "5":
            print("\nRefreshing data...")
            followers = get_followers(profile)
            following = get_following(profile)
            not_following = following - followers
            print(f"✓ Data di-refresh!")
            print(f"  Followers: {len(followers)}")
            print(f"  Following: {len(following)}")
            print(f"  Tidak FB: {len(not_following)}")
        
        elif choice == "6":
            print("\n✓ Sampai jumpa!")
            break
        
        else:
            print("✗ Pilihan tidak valid")

if __name__ == "__main__":
    main()
