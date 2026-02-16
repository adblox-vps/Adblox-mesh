import zipfile
import os
import plistlib
import shutil
from pathlib import Path

# Inställningar
INPUT_IPA = "AdBloX-MESH-v1.8.2 (3).ipa"
OUTPUT_IPA = "AdBloX-MESH-Branded.ipa"
APP_NAME = "AdBloX.app"

def refactor():
    if os.path.exists("extracted"):
        shutil.rmtree("extracted")
    
    with zipfile.ZipFile(INPUT_IPA, 'r') as zip_ref:
        zip_ref.extractall("extracted")

    app_path = Path("extracted/Payload") / APP_NAME
    app_info_path = app_path / "Info.plist"
    
    # 1. Hämta huvud-ID
    with open(app_info_path, 'rb') as f:
        app_plist = plistlib.load(f)
    
    main_bundle_id = app_plist.get("CFBundleIdentifier", "com.adblox.mesh")
    app_plist['CFBundleDisplayName'] = "AdBloX MESH"
    app_plist['UIStatusBarStyle'] = "UIStatusBarStyleLightContent"
    
    with open(app_info_path, 'wb') as f:
        plistlib.dump(app_plist, f)

    # 2. Fixa Extension så den matchar (Viktigt för KravaSigner!)
    ext_dir = app_path / "PlugIns"
    if ext_dir.exists():
        for ext in ext_dir.glob("*.appex"):
            ext_info_path = ext / "Info.plist"
            with open(ext_info_path, 'rb') as f:
                ext_plist = plistlib.load(f)
            
            # Tvingar extension-ID att vara en del av huvudappen
            ext_plist['CFBundleIdentifier'] = f"{main_bundle_id}.extension"
            
            with open(ext_info_path, 'wb') as f:
                plistlib.dump(ext_plist, f)

    # 3. Packa ihop
    shutil.make_archive("temp_zip", 'zip', "extracted")
    os.rename("temp_zip.zip", OUTPUT_IPA)
    print(f"Refactor klar: {OUTPUT_IPA}")

if __name__ == "__main__":
    refactor()
