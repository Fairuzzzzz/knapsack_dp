"""
Penentuan Pilihan Belanja Optimal dengan Budget Terbatas
Metode: Dynamic Programming (Knapsack 0/1)
"""

def knapsack(W, barang):
    """
    Menyelesaikan knapsack dengan dynamic Programming
    barang: list of (nama, harga, nilai)
    return: (manfaat_maks, daftar_terpilih, total_harga, tabel_dp)
    """

    n = len(barang)

    # Inisialisasi tabel dp[0..n][0..W] dengan 0
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    # Isi tabel: dp[i][w] = manfaat maksimal dengan i barang pertama dan budget w
    for i in range(1, n + 1):
        nama, harga, nilai = barang[i - 1]
        for w in range(W + 1):
            if harga > w:
                # Barang tidak muat -> salin hasil sebelumnya
                dp[i][w] = dp[i - 1][w]
            else:
                tidak_ambil = dp[i - 1][w]
                ambil = dp[i - 1][w - harga] + nilai
                dp[i][w] = max(tidak_ambil, ambil)

    # Telusuri balik untuk mencari barang yang terpilih
    terpilih = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]: # nilai berubah -> barang i diambil 
            terpilih.append(barang[i - 1])
            w -= barang[i - 1][1]
    terpilih.reverse()

    total_harga = sum(b[1] for b in terpilih)
    return dp[n][W], terpilih, total_harga, dp

def print_tabel_dp(dp, barang, W, step):
    """Menampilkan sebagian tabel dp (kolom budget kelipatan 'step')."""
    kolom = list(range(0, W + 1, step))
    print("  Tabel DP (baris = barang, kolom = budget):")
    print("    " + f"{'':<12}" + "".join(f"{w:>6}" for w in kolom))
    for i in range(len(dp)):
        label = "(awal)" if i == 0 else barang[i - 1][0]
        print("    " + f"{label:<12}" + "".join(f"{dp[i][w]:>6}" for w in kolom))
    print()

def run_usecase(judul, W, barang, tampil_tabel=False, step=10):
    print(judul) 
    print(f"Budget: {W}")
    print(f"{'Barang':<16}{'Harga':>8}{'Nilai':>8}")
    for nama, harga, nilai in barang:
        print(f"{nama:<16}{harga:>8}{nilai:>8}")
    print()

    manfaat, terpilih, total_harga, dp = knapsack(W, barang)

    if tampil_tabel:
        print_tabel_dp(dp, barang, W, step)

    print("  HASIL:")
    print(f"    Manfaat maksimal : {manfaat}")
    print(f"    Total harga      : {total_harga}")
    print(f"    Sisa budget      : {W - total_harga}")
    if terpilih:
        print("    Barang dipilih   : " + ", ".join(b[0] for b in terpilih))
    else:
        print("    Barang dipilih   : (tidak ada)")
    print()

def manual_input():
    """Kode untuk input manual"""
    W = int(input("Masukkan budget (ribu rupiah): "))
    n = int(input("Jumlah barang: "))
    barang = []
    for i in range(1, n + 1):
        nama = input(f"Barang {i} - nama  : ")
        harga = int(input(f"Barang {i} - harga : "))
        nilai = int(input(f"Barang {i} - nilai : "))
        barang.append((nama, harga, nilai))
    run_usecase("HASIL INPUT MANUAL", W, barang)

def main():
    run_usecase(
        "KASUS 1: Kasus dasar (3 barang) + tabel DP", 50,
        [("Buku", 10, 60), ("Flashdisk", 20, 100), ("Headset", 30, 120)],
        tampil_tabel=True, step=10)
    run_usecase(
        "KASUS 2: Budget 0", 0,
        [("Buku", 10, 60), ("Flashdisk", 20, 100)])
    run_usecase(
        "KASUS 3: Semua barang lebih mahal dari budget", 5,
        [("Buku", 10, 60), ("Flashdisk", 20, 100)])
    run_usecase(
        "KASUS 4: Budget cukup untuk semua barang", 100,
        [("Buku", 10, 60), ("Flashdisk", 20, 100), ("Headset", 30, 120)])
    run_usecase(
        "KASUS 5: Belanja mahasiswa (6 barang)", 100,
        [("Buku", 25, 70), ("Pulpen", 5, 20), ("Flashdisk", 30, 60),
         ("Headset", 45, 85), ("Tas", 50, 90), ("Lampu belajar", 35, 65)])

    pilih = input("Coba input manual? (y/n): ").strip().lower()
    if pilih == "y":
        manual_input()

if __name__ == "__main__":
    main()
