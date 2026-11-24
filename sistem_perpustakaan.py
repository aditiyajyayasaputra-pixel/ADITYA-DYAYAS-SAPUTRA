"""
Project OOP Python: Sistem Perpustakaan Sederhana

Konsep OOP yang diterapkan:
1. Minimal 2 class        -> Buku, Anggota, Perpustakaan
2. Object dari class      -> dibuat di fungsi main()
3. Constructor __init__() -> di setiap class
4. Attribute dan method   -> di setiap class
5. Encapsulation          -> attribute private (diawali __)
6. Property/setter        -> @property dan @<nama>.setter
7. Class method           -> @classmethod (Buku.dari_string, Anggota.jumlah_anggota)
8. Static method          -> @staticmethod (Perpustakaan.validasi_id)
"""


class Buku:
    """Class yang merepresentasikan sebuah buku di perpustakaan."""

    # Class attribute: menghitung total buku yang pernah dibuat
    total_buku = 0

    def __init__(self, kode, judul, penulis, stok):
        self.__kode = kode            # private attribute
        self.__judul = judul
        self.__penulis = penulis
        self.__stok = 0
        self.stok = stok              # memakai setter (ada validasi)
        Buku.total_buku += 1

    # ---------- Property (getter) ----------
    @property
    def kode(self):
        return self.__kode

    @property
    def judul(self):
        return self.__judul

    @property
    def penulis(self):
        return self.__penulis

    @property
    def stok(self):
        return self.__stok

    # ---------- Setter dengan validasi ----------
    @stok.setter
    def stok(self, nilai):
        if not isinstance(nilai, int) or nilai < 0:
            raise ValueError("Stok harus berupa bilangan bulat >= 0")
        self.__stok = nilai

    # ---------- Method biasa ----------
    def kurangi_stok(self):
        if self.__stok > 0:
            self.__stok -= 1
            return True
        return False

    def tambah_stok(self):
        self.__stok += 1

    def tampilkan_info(self):
        print(f"[{self.__kode}] {self.__judul} - {self.__penulis} (Stok: {self.__stok})")

    # ---------- Class method ----------
    @classmethod
    def dari_string(cls, data):
        """Membuat objek Buku dari string 'kode;judul;penulis;stok'."""
        kode, judul, penulis, stok = data.split(";")
        return cls(kode, judul, penulis, int(stok))

    @classmethod
    def jumlah_buku(cls):
        return cls.total_buku


class Anggota:
    """Class yang merepresentasikan anggota perpustakaan."""

    MAKS_PINJAM = 3  # class attribute: batas peminjaman

    def __init__(self, id_anggota, nama):
        self.__id_anggota = id_anggota
        self.__nama = nama
        self.__daftar_pinjam = []     # private list berisi objek Buku

    @property
    def id_anggota(self):
        return self.__id_anggota

    @property
    def nama(self):
        return self.__nama

    @nama.setter
    def nama(self, nilai):
        if not nilai.strip():
            raise ValueError("Nama tidak boleh kosong")
        self.__nama = nilai

    @property
    def daftar_pinjam(self):
        # Mengembalikan salinan agar list asli tidak bisa diubah dari luar
        return list(self.__daftar_pinjam)

    def pinjam(self, buku):
        if len(self.__daftar_pinjam) >= Anggota.MAKS_PINJAM:
            print(f"  ! {self.__nama} sudah mencapai batas pinjam ({Anggota.MAKS_PINJAM} buku).")
            return False
        if buku in self.__daftar_pinjam:
            print(f"  ! {self.__nama} sudah meminjam buku '{buku.judul}'.")
            return False
        if not buku.kurangi_stok():
            print(f"  ! Stok buku '{buku.judul}' habis.")
            return False
        self.__daftar_pinjam.append(buku)
        print(f"  + {self.__nama} berhasil meminjam '{buku.judul}'.")
        return True

    def kembalikan(self, buku):
        if buku not in self.__daftar_pinjam:
            print(f"  ! {self.__nama} tidak meminjam buku '{buku.judul}'.")
            return False
        self.__daftar_pinjam.remove(buku)
        buku.tambah_stok()
        print(f"  + {self.__nama} mengembalikan '{buku.judul}'.")
        return True

    def tampilkan_info(self):
        print(f"Anggota [{self.__id_anggota}] {self.__nama}")
        if self.__daftar_pinjam:
            for b in self.__daftar_pinjam:
                print(f"   - {b.judul}")
        else:
            print("   (tidak ada buku yang dipinjam)")


class Perpustakaan:
    """Class pengelola data buku dan anggota."""

    def __init__(self, nama):
        self.nama = nama
        self.__buku = {}      # kode -> Buku
        self.__anggota = {}   # id -> Anggota

    # ---------- Static method ----------
    @staticmethod
    def validasi_id(id_anggota):
        """ID anggota valid jika diawali 'A' diikuti 3 digit, contoh: A001."""
        return (
            len(id_anggota) == 4
            and id_anggota[0] == "A"
            and id_anggota[1:].isdigit()
        )

    # ---------- Manajemen buku ----------
    def tambah_buku(self, buku):
        self.__buku[buku.kode] = buku

    def cari_buku(self, kode):
        return self.__buku.get(kode)

    def tampilkan_semua_buku(self):
        print(f"\n=== Daftar Buku {self.nama} ===")
        for buku in self.__buku.values():
            buku.tampilkan_info()

    # ---------- Manajemen anggota ----------
    def daftar_anggota(self, anggota):
        if not Perpustakaan.validasi_id(anggota.id_anggota):
            print(f"  ! ID '{anggota.id_anggota}' tidak valid (format: A001).")
            return False
        self.__anggota[anggota.id_anggota] = anggota
        print(f"  + Anggota {anggota.nama} terdaftar.")
        return True

    def cari_anggota(self, id_anggota):
        return self.__anggota.get(id_anggota)

    # ---------- Transaksi ----------
    def proses_pinjam(self, id_anggota, kode_buku):
        anggota = self.cari_anggota(id_anggota)
        buku = self.cari_buku(kode_buku)
        if anggota is None or buku is None:
            print("  ! Data anggota atau buku tidak ditemukan.")
            return False
        return anggota.pinjam(buku)

    def proses_kembali(self, id_anggota, kode_buku):
        anggota = self.cari_anggota(id_anggota)
        buku = self.cari_buku(kode_buku)
        if anggota is None or buku is None:
            print("  ! Data anggota atau buku tidak ditemukan.")
            return False
        return anggota.kembalikan(buku)


def main():
    # Membuat object Perpustakaan
    perpus = Perpustakaan("Perpustakaan Kampus")

    # Membuat object Buku (constructor biasa)
    perpus.tambah_buku(Buku("B01", "Pemrograman Python", "Budi Raharjo", 2))
    perpus.tambah_buku(Buku("B02", "Struktur Data", "Rinaldi Munir", 1))

    # Membuat object Buku memakai class method
    perpus.tambah_buku(Buku.dari_string("B03;Basis Data;Fathansyah;3"))

    # Membuat object Anggota
    a1 = Anggota("A001", "Andi")
    a2 = Anggota("A002", "Siti")
    a3 = Anggota("X99", "Rudi")  # ID tidak valid

    print("=== Pendaftaran Anggota ===")
    perpus.daftar_anggota(a1)
    perpus.daftar_anggota(a2)
    perpus.daftar_anggota(a3)

    perpus.tampilkan_semua_buku()

    print("\n=== Transaksi Peminjaman ===")
    perpus.proses_pinjam("A001", "B01")
    perpus.proses_pinjam("A001", "B02")
    perpus.proses_pinjam("A002", "B02")   # stok habis
    perpus.proses_pinjam("A001", "B01")   # sudah dipinjam

    print("\n=== Transaksi Pengembalian ===")
    perpus.proses_kembali("A001", "B02")
    perpus.proses_pinjam("A002", "B02")   # sekarang berhasil

    perpus.tampilkan_semua_buku()

    print("\n=== Data Anggota ===")
    a1.tampilkan_info()
    a2.tampilkan_info()

    # Demo property/setter
    print("\n=== Demo Property & Setter ===")
    a1.nama = "Andi Pratama"
    print("Nama baru:", a1.nama)
    try:
        perpus.cari_buku("B01").stok = -5
    except ValueError as e:
        print("Error:", e)

    # Demo encapsulation: attribute private tidak bisa diakses langsung
    try:
        print(a1.__nama)
    except AttributeError:
        print("Error: attribute private '__nama' tidak dapat diakses langsung")

    # Demo class method
    print("\nTotal buku yang dibuat:", Buku.jumlah_buku())


if __name__ == "__main__":
    main()
