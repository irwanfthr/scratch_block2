import tkinter as tk
from pathlib import Path
from PIL import Image, ImageDraw, ImageTk
import random
import math
import time

# ==================================================
# PENGATURAN PROGRAM
# ==================================================

FOLDER_PROGRAM = Path(__file__).resolve().parent
FOLDER_GAMBAR = FOLDER_PROGRAM / "images"

UKURAN_RODA = 600
TENGAH = UKURAN_RODA // 2
JARI_JARI = 265
DURASI_SPIN = 4.5

FORMAT_GAMBAR = {
    ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"
}

WARNA_RODA = [
    "#B8D8E8",  # biru muda
    "#F2D6A2",  # krem hangat
    "#E8B7C8",  # dusty pink
    "#C7D8C0",  # sage green
    "#D0C5E8",  # lavender
    "#E9C4A8",  # peach
    "#B7DAD5",  # teal muda
    "#D5DCE8",  # abu kebiruan
]

WARNA_LATAR = "#F5F7FA"
WARNA_PANEL = "#FFFFFF"
WARNA_TEKSTO = "#26364A"
WARNA_SEKUNDER = "#65758B"
WARNA_TOMBOL = "#26364A"
WARNA_TOMBOL_HOVER = "#3C526F"
WARNA_TOMBOL_NONAKTIF = "#AAB5C3"
WARNA_JARUM = "#D94F58"


def baca_gambar():
    """."""
    FOLDER_GAMBAR.mkdir(exist_ok=True)
    daftar_gambar = []

    semua_file = sorted(
        FOLDER_GAMBAR.iterdir(),
        key=lambda file: file.name.lower()
    )

    for file in semua_file:
        if file.suffix.lower() not in FORMAT_GAMBAR:
            continue

        try:
            gambar = Image.open(file).convert("RGBA")
            gambar_hasil = gambar.copy()

            thumbnail = gambar.copy()
            thumbnail.thumbnail((52, 52), Image.Resampling.LANCZOS)

            daftar_gambar.append({
                "file": file,
                "thumbnail": thumbnail,
                "gambar_hasil": gambar_hasil,
            })
        except Exception as error:
            print(f"Gambar gagal dibaca: {file.name}")
            print(f"Alasan: {error}")

    return daftar_gambar


class SpinWheel:
    def __init__(self, root):
        self.root = root
        self.root.title("Spin Wheel - Scratch Chapter 1")
        self.root.geometry("1200x760")
        self.root.minsize(1000, 680)
        self.root.configure(bg=WARNA_LATAR)

        self.daftar_gambar = baca_gambar()
        self.sudut_roda = 0.0
        self.sedang_spin = False
        self.gambar_roda_tk = None
        self.gambar_hasil_tk = None

        self.buat_tampilan()
        self.gambar_roda()

    def buat_tampilan(self):
        tk.Label(
            self.root,
            text="SPIN THE WHEEL",
            font=("Arial", 30, "bold"),
            bg=WARNA_LATAR,
            fg=WARNA_TEKSTO
        ).pack(pady=(15, 3))

        tk.Label(
            self.root,
            text="Examination Chapter I",
            font=("Arial", 15, "bold"),
            bg=WARNA_LATAR,
            fg=WARNA_SEKUNDER
        ).pack(pady=(0, 10))

        bagian_utama = tk.Frame(self.root, bg=WARNA_LATAR)
        bagian_utama.pack(fill="both", expand=True, padx=18, pady=5)

        area_roda = tk.Frame(bagian_utama, bg=WARNA_LATAR)
        area_roda.pack(side="left", padx=(0, 16), pady=8)

        self.canvas = tk.Canvas(
            area_roda,
            width=UKURAN_RODA,
            height=UKURAN_RODA,
            bg=WARNA_LATAR,
            highlightthickness=0
        )
        self.canvas.pack()

        panel_hasil = tk.Frame(
            bagian_utama,
            bg=WARNA_PANEL,
            highlightbackground="#DCE3EC",
            highlightthickness=1
        )
        panel_hasil.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=24
        )

        tk.Label(
            panel_hasil,
            text="HASIL SPIN",
            font=("Arial", 20, "bold"),
            bg=WARNA_PANEL,
            fg=WARNA_TEKSTO
        ).pack(pady=(24, 12))

        self.area_hasil = tk.Frame(
            panel_hasil,
            width=400,
            height=320,
            bg="#EEF2F7"
        )
        self.area_hasil.pack(pady=8, padx=18)
        self.area_hasil.pack_propagate(False)

        self.label_gambar_hasil = tk.Label(
            self.area_hasil,
            text="?",
            font=("Arial", 58, "bold"),
            bg="#EEF2F7",
            fg=WARNA_SEKUNDER
        )
        self.label_gambar_hasil.pack(fill="both", expand=True)

        if self.daftar_gambar:
            teks_awal = "Klik SPIN! untuk memilih gambar."
        else:
            teks_awal = "Folder images masih kosong.\nMasukkan gambar terlebih dahulu."

        self.label_nama_hasil = tk.Label(
            panel_hasil,
            text=teks_awal,
            font=("Arial", 13, "bold"),
            bg=WARNA_PANEL,
            fg=WARNA_TEKSTO,
            wraplength=340,
            justify="center"
        )
        self.label_nama_hasil.pack(padx=18, pady=(14, 10))

        # Tombol dibuat dari Frame + Label agar warna tampil konsisten di macOS.
        # Tkinter Button biasa dapat mengikuti tampilan Aqua dan mengabaikan warna bg.
        self.tombol_spin = tk.Frame(
            panel_hasil,
            bg=(WARNA_TOMBOL if self.daftar_gambar else WARNA_TOMBOL_NONAKTIF),
            cursor=("hand2" if self.daftar_gambar else "arrow")
        )
        self.tombol_spin.pack(pady=(8, 5))

        self.label_tombol_spin = tk.Label(
            self.tombol_spin,
            text="SPIN!",
            font=("Arial", 16, "bold"),
            bg=(WARNA_TOMBOL if self.daftar_gambar else WARNA_TOMBOL_NONAKTIF),
            fg="white",
            padx=48,
            pady=12,
            cursor=("hand2" if self.daftar_gambar else "arrow")
        )
        self.label_tombol_spin.pack()

        if self.daftar_gambar:
            self.tombol_spin.bind("<Button-1>", self._klik_spin)
            self.label_tombol_spin.bind("<Button-1>", self._klik_spin)
            self.tombol_spin.bind("<Enter>", self._hover_masuk)
            self.label_tombol_spin.bind("<Enter>", self._hover_masuk)
            self.tombol_spin.bind("<Leave>", self._hover_keluar)
            self.label_tombol_spin.bind("<Leave>", self._hover_keluar)

        tk.Label(
            panel_hasil,
            text=f"Jumlah gambar: {len(self.daftar_gambar)}",
            font=("Arial", 10),
            bg=WARNA_PANEL,
            fg=WARNA_SEKUNDER
        ).pack(pady=(8, 12))

    def _klik_spin(self, event=None):
        self.mulai_spin()

    def _hover_masuk(self, event=None):
        if not self.sedang_spin and self.daftar_gambar:
            self.tombol_spin.configure(bg=WARNA_TOMBOL_HOVER)
            self.label_tombol_spin.configure(bg=WARNA_TOMBOL_HOVER)

    def _hover_keluar(self, event=None):
        if not self.sedang_spin and self.daftar_gambar:
            self.tombol_spin.configure(bg=WARNA_TOMBOL)
            self.label_tombol_spin.configure(bg=WARNA_TOMBOL)

    def atur_status_tombol(self, aktif):
        if aktif:
            warna = WARNA_TOMBOL
            self.tombol_spin.configure(cursor="hand2")
            self.label_tombol_spin.configure(cursor="hand2")
            self.tombol_spin.bind("<Button-1>", self._klik_spin)
            self.label_tombol_spin.bind("<Button-1>", self._klik_spin)
        else:
            warna = WARNA_TOMBOL_NONAKTIF
            self.tombol_spin.configure(cursor="arrow")
            self.label_tombol_spin.configure(cursor="arrow")
            self.tombol_spin.unbind("<Button-1>")
            self.label_tombol_spin.unbind("<Button-1>")

        self.tombol_spin.configure(bg=warna)
        self.label_tombol_spin.configure(bg=warna)

    def gambar_roda(self):
        self.canvas.delete("all")
        jumlah = len(self.daftar_gambar)

        if jumlah == 0:
            self.canvas.create_oval(
                TENGAH - JARI_JARI, TENGAH - JARI_JARI,
                TENGAH + JARI_JARI, TENGAH + JARI_JARI,
                fill="#E6EBF2", outline=WARNA_TEKSTO, width=4
            )
            self.canvas.create_text(
                TENGAH, TENGAH,
                text="MASUKKAN GAMBAR\nKE FOLDER images",
                font=("Arial", 18, "bold"),
                fill=WARNA_TEKSTO,
                justify="center"
            )
            self.gambar_jarum()
            return

        skala = 2
        ukuran_besar = UKURAN_RODA * skala
        roda = Image.new("RGBA", (ukuran_besar, ukuran_besar), (0, 0, 0, 0))
        gambar = ImageDraw.Draw(roda)

        tengah = TENGAH * skala
        radius = JARI_JARI * skala
        sudut_sektor = 360 / jumlah

        for i, item in enumerate(self.daftar_gambar):
            sudut_tengah = -90 + self.sudut_roda + i * sudut_sektor
            sudut_awal = sudut_tengah - sudut_sektor / 2
            sudut_akhir = sudut_tengah + sudut_sektor / 2

            kotak = (
                tengah - radius, tengah - radius,
                tengah + radius, tengah + radius
            )
            gambar.pieslice(
                kotak,
                start=sudut_awal,
                end=sudut_akhir,
                fill=WARNA_RODA[i % len(WARNA_RODA)],
                outline="white",
                width=3 * skala
            )

            jarak = JARI_JARI * 0.68
            radian = math.radians(sudut_tengah)
            x = int(tengah + math.cos(radian) * jarak * skala)
            y = int(tengah + math.sin(radian) * jarak * skala)

            thumbnail = item["thumbnail"]
            radius_latar = 30 * skala
            gambar.ellipse(
                (
                    x - radius_latar, y - radius_latar,
                    x + radius_latar, y + radius_latar
                ),
                fill="white",
                outline="white"
            )

            roda.alpha_composite(
                thumbnail,
                (x - thumbnail.width // 2, y - thumbnail.height // 2)
            )

        # Garis luar saja. Lingkaran tengah berwarna gelap dihapus.
        gambar.ellipse(
            (
                tengah - radius, tengah - radius,
                tengah + radius, tengah + radius
            ),
            outline=WARNA_TEKSTO,
            width=7 * skala
        )

        roda = roda.resize(
            (UKURAN_RODA, UKURAN_RODA),
            Image.Resampling.LANCZOS
        )
        self.gambar_roda_tk = ImageTk.PhotoImage(roda)
        self.canvas.create_image(
            0, 0, image=self.gambar_roda_tk, anchor="nw"
        )
        self.gambar_jarum()

    def gambar_jarum(self):
        self.canvas.create_polygon(
            TENGAH - 22, 5,
            TENGAH + 22, 5,
            TENGAH, 58,
            fill=WARNA_JARUM,
            outline="white",
            width=2
        )

    def mulai_spin(self):
        if self.sedang_spin or not self.daftar_gambar:
            return

        self.sedang_spin = True
        self.atur_status_tombol(False)

        self.label_nama_hasil.config(text="Roda sedang berputar...")
        self.label_gambar_hasil.config(image="", text="...")
        self.label_gambar_hasil.image = None
        self.gambar_hasil_tk = None

        jumlah = len(self.daftar_gambar)
        self.indeks_terpilih = random.randrange(jumlah)

        sudut_sektor = 360 / jumlah
        sudut_target = (self.indeks_terpilih * sudut_sektor) % 360
        sudut_sekarang = self.sudut_roda % 360
        tambahan_putaran = (sudut_target - sudut_sekarang) % 360

        putaran_penuh = random.randint(5, 8) * 360
        self.sudut_awal = self.sudut_roda
        self.total_putaran = putaran_penuh + tambahan_putaran
        self.waktu_mulai = time.perf_counter()

        self.animasi_spin()

    def animasi_spin(self):
        waktu_berjalan = time.perf_counter() - self.waktu_mulai
        progress = min(waktu_berjalan / DURASI_SPIN, 1.0)
        progress_halus = 1 - (1 - progress) ** 4

        self.sudut_roda = (
            self.sudut_awal + self.total_putaran * progress_halus
        )
        self.gambar_roda()

        if progress < 1:
            self.root.after(20, self.animasi_spin)
        else:
            self.sudut_roda = (
                self.sudut_awal + self.total_putaran
            ) % 360
            self.gambar_roda()

            self.sedang_spin = False
            self.tampilkan_hasil()
            self.atur_status_tombol(True)

    def tampilkan_hasil(self):
        item = self.daftar_gambar[self.indeks_terpilih]
        gambar = item["gambar_hasil"].copy()
        gambar.thumbnail((400, 400), Image.Resampling.LANCZOS)

        self.gambar_hasil_tk = ImageTk.PhotoImage(gambar)
        self.label_gambar_hasil.config(
            image=self.gambar_hasil_tk,
            text="",
            bg="#EEF2F7"
        )
        self.label_gambar_hasil.image = self.gambar_hasil_tk

        # Tidak menampilkan nama file maupun teks "Gambar terpilih".
        self.label_nama_hasil.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    aplikasi = SpinWheel(root)
    root.mainloop()