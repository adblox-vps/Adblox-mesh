import zipfile
import os
import plistlib
import shutil

IPA_NAME = "AdBloX-MESH-v1.8.2 (3).ipa"
OUT_NAME = "AdBloX-MESH-Electric.ipa"
APP_PATH = "Payload/AdBloX.app"
EXT_PATH = "Payload/AdBloX.app/PlugIns/AdBloXNetworkExtension.appex"

# ÄNDRA DETTA till något personligt (inga mellanslag, bara bokstäver)
MY_PREFIX = "hampuz" 
NEW_BASE_BUNDLE = f"com.{MY_PREFIX}.adblox"
NEW_EXT_BUNDLE = f"{NEW_BASE_BUNDLE}.network"

def refactor():
    print(f"Extraherar {IPA_NAME}...")
    if os.path.exists("extracted"):
        shutil.rmtree("extracted")
    with zipfile.ZipFile(IPA_NAME, 'r') as zip_ref:
        zip_ref.extractall("extracted")

    # 1. Uppdatera Huvudappens Info.plist
    main_plist = os.path.join("extracted", APP_PATH, "Info.plist")
    with open(main_plist, 'rb') as f:
        pl = plistlib.load(f)
    pl['CFBundleIdentifier'] = NEW_BASE_BUNDLE
    pl['CFBundleDisplayName'] = "AdBloX MESH"
    with open(main_plist, 'wb') as f:
        plistlib.dump(pl, f)

    # 2. Uppdatera Extensionens Info.plist
    ext_plist = os.path.join("extracted", EXT_PATH, "Info.plist")
    if os.path.exists(ext_plist):
        with open(ext_plist, 'rb') as f:
            e_pl = plistlib.load(f)
        e_pl['CFBundleIdentifier'] = NEW_EXT_BUNDLE
        # Viktigt: Koppla ihop dem i NSExtension-inställningarna
        if 'NSExtension' in e_pl:
            e_pl['NSExtension']['NSExtensionPrincipalClass'] = "AdBloXNetworkExtension.PacketTunnelProvider"
        with open(ext_plist, 'wb') as f:
            plistlib.dump(e_pl, f)

    # 3. Rensa gamla signaturer (Viktigt för Sideloadly!)
    for root, dirs, files in os.walk("extracted"):
        if "_CodeSignature" in dirs:
            shutil.rmtree(os.path.join(root, "_CodeSignature"))

    print(f"Klart! Ny Bundle ID: {NEW_BASE_BUNDLE}")

if __name__ == "__main__":
    refactor()
