import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("Dark")  # Dark Mode
ctk.set_default_color_theme("green")  # Grün als Akzent

# ---------- STL HELPERS ----------
def write_facet(f, v1, v2, v3):
    f.write("  facet normal 0 0 0\n")
    f.write("    outer loop\n")
    f.write(f"      vertex {v1[0]} {v1[1]} {v1[2]}\n")
    f.write(f"      vertex {v2[0]} {v2[1]} {v2[2]}\n")
    f.write(f"      vertex {v3[0]} {v3[1]} {v3[2]}\n")
    f.write("    endloop\n")
    f.write("  endfacet\n")

def box_faces_open_top(invert=False):
    faces = [
        (0,1,2),(0,2,3),   # Boden
        (0,1,5),(0,5,4),   # Vorderseite
        (1,2,6),(1,6,5),   # Rechts
        (2,3,7),(2,7,6),   # Hinten
        (3,0,4),(3,4,7)    # Links
    ]
    return [(c,b,a) if invert else (a,b,c) for a,b,c in faces]

def create_open_box_stl(file, lx, ly, lz, wall):
    outer = [
        (0,0,0),(lx,0,0),(lx,ly,0),(0,ly,0),
        (0,0,lz),(lx,0,lz),(lx,ly,lz),(0,ly,lz)
    ]
    inner = [
        (wall,wall,wall),
        (lx-wall,wall,wall),
        (lx-wall,ly-wall,wall),
        (wall,ly-wall,wall),
        (wall,wall,lz),
        (lx-wall,wall,lz),
        (lx-wall,ly-wall,lz),
        (wall,ly-wall,lz)
    ]
    with open(file, "w") as f:
        f.write("solid open_box\n")
        for a,b,c in box_faces_open_top():
            write_facet(f, outer[a], outer[b], outer[c])
        for a,b,c in box_faces_open_top(invert=True):
            write_facet(f, inner[a], inner[b], inner[c])
        f.write("endsolid open_box\n")

# ---------- GUI ----------
def build():
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = float(entry_z.get())
        w = float(entry_w.get())
        if w <= 0 or w*2 >= min(x, y):
            raise ValueError

        file = filedialog.asksaveasfilename(
            defaultextension=".stl",
            filetypes=[("STL Datei", "*.stl")]
        )
        if file:
            create_open_box_stl(file, x, y, z, w)
            messagebox.showinfo("Fertig", "Offene Box erfolgreich erstellt!")

    except:
        messagebox.showerror("Fehler", "Ungültige Werte! (Wandstärke zu groß?)")

# ---------- CustomTkinter Fenster ----------
root = ctk.CTk()
root.title("Hohle Open-Box Builder")
root.geometry("400x380")

ctk.CTkLabel(root, text="📦 Hohle Aufbewahrungsbox (oben offen)", font=("Arial", 16, "bold")).pack(pady=15)

frame = ctk.CTkFrame(root)
frame.pack(pady=10, padx=20, fill="both", expand=True)

labels = ["Länge (X)", "Breite (Y)", "Höhe (Z)", "Wandstärke"]
entries = []

for i, txt in enumerate(labels):
    ctk.CTkLabel(frame, text=txt, anchor="w").grid(row=i, column=0, pady=8, padx=10, sticky="w")
    e = ctk.CTkEntry(frame, placeholder_text="mm")
    e.grid(row=i, column=1, pady=8, padx=10, sticky="ew")
    entries.append(e)

entry_x, entry_y, entry_z, entry_w = entries
frame.grid_columnconfigure(1, weight=1)

ctk.CTkButton(root, text="STL erstellen", command=build, font=("Arial", 14, "bold")).pack(pady=25)

root.mainloop()
