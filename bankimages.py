import os
import subprocess

assets_dir = r"C:\Users\algorithm\AndroidStudioProjects\opay\app\src\main\res\mipmap-xxhdpi\bankassets"
pngquant_path = r"C:\Users\algorithm\Downloads\pngquant-windows\pngquant.exe"
oxipng_path = r"C:\Users\algorithm\Downloads\oxipng-9.1.5-x86_64-pc-windows-msvc\oxipng.exe"

# Verify that both tools exist
for name, path in [("pngquant", pngquant_path), ("oxipng", oxipng_path)]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"{name} not found at: {path}")

for filename in os.listdir(assets_dir):
    if filename.lower().endswith(".png"):
        filepath = os.path.join(assets_dir, filename)
        original_size_kb = os.path.getsize(filepath) / 1024
        print(f"\nCompressing: {filename} ({int(original_size_kb)} KB)")
        temp_output = filepath + ".tmp"

        # Step 1: pngquant lossy compression
        result = subprocess.run([
            pngquant_path,
            "--quality=20-50",
            "--speed", "1",
            "--strip",
            "--output", temp_output,
            "--force",
            filepath
        ], capture_output=True)

        if result.returncode == 0 and os.path.exists(temp_output):
            os.replace(temp_output, filepath)
            print("  ✔ pngquant compression done")
        else:
            print("  ✘ pngquant failed:\n", result.stderr.decode().strip())
            continue  # Skip oxipng if pngquant fails

        # Step 2: oxipng lossless optimization
        oxi_result = subprocess.run([
            oxipng_path,
            "-o", "4",
            "--strip", "all",
            filepath
        ], capture_output=True)

        if oxi_result.returncode == 0:
            new_size_kb = os.path.getsize(filepath) / 1024
            print(f"  ✔ oxipng polish done → new size: {int(new_size_kb)} KB")
        else:
            print("  ✘ oxipng failed:\n", oxi_result.stderr.decode().strip())

print("\n✅ All PNG files processed.")
