import zipfile
import os
import plistlib
import shutil

# Inställningar för din IPA
IPA_NAME = "AdBloX-MESH-v1.8.2 (3).ipa"
OUT_NAME = "AdBloX-MESH-Electric.ipa"
APP_PATH = "Payload/AdBloX.app"

def refactor():
    print(f"Extraherar {IPA_NAME}...")
    with zipfile.ZipFile(IPA_NAME, 'r') as zip_ref:
        zip_ref.extractall("extracted")

    # Sökväg till Info.plist
    plist_path = os.path.join("extracted", APP_PATH, "Info.plist")
    
    if os.path.exists(plist_path):
        print("Uppdaterar branding och färger i Info.plist...")
        with open(plist_path, 'rb') as f:
            pl = plistlib.load(f)
        
        # Injektion av Electric Blue och Branding
        pl['CFBundleDisplayName'] = "AdBloX MESH"
        pl['UIStatusBarStyle'] = "UIStatusBarStyleLightContent"
        pl['AdBloX_Theme_Color'] = "#00EAFF"
        
        with open(plist_path, 'wb') as f:
            plistlib.dump(pl, f)

    # Packa ihop till en ny IPA
    print(f"Skapar ny IPA: {OUT_NAME}...")
    shutil.make_archive("branded_app", 'zip', "extracted")
    os.rename("branded_app.zip", OUT_NAME)
    print("Klart!")

if __name__ == "__main__":
    refactor()
