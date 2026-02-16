import zipfile, os, plistlib, shutil
from pathlib import Path

def refactor():
    # Hitta IPA automatiskt
    input_ipa = next(Path(".").glob("*.ipa"))
    output_ipa = "AdBloX-MESH-Branded.ipa"
    
    if os.path.exists("extracted"): shutil.rmtree("extracted")
    with zipfile.ZipFile(input_ipa, 'r') as z: z.extractall("extracted")

    app_path = next(Path("extracted/Payload").glob("*.app"))
    
    # Fixa Huvudappen
    with open(app_path / "Info.plist", 'rb') as f:
        pl = plistlib.load(f)
    
    main_id = pl.get("CFBundleIdentifier", "com.adblox.mesh")
    pl['CFBundleDisplayName'] = "AdBloX MESH"
    
    with open(app_path / "Info.plist", 'wb') as f:
        plistlib.dump(pl, f)

    # Fixa VPN-motorn (Detta är vad som fixar ditt "Det gick inte att installera"-fel)
    ext_dir = app_path / "PlugIns"
    if ext_dir.exists():
        for ext in ext_dir.glob("*.appex"):
            with open(ext / "Info.plist", 'rb') as f:
                e_pl = plistlib.load(f)
            e_pl['CFBundleIdentifier'] = f"{main_id}.network" # Tvingar matchning
            with open(ext / "Info.plist", 'wb') as f:
                plistlib.dump(e_pl, f)

    shutil.make_archive("out", 'zip', "extracted")
    os.rename("out.zip", output_ipa)

if __name__ == "__main__":
    refactor()
