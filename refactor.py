import zipfile
import os
import plistlib
import shutil

# Matchar exakt filen i ditt repo
IPA_NAME = "AdBloX-MESH-v1.8.2 (3).ipa"
OUT_NAME = "AdBloX-MESH-Electric.ipa"
APP_PATH = "Payload/AdBloX.app"
EXT_PATH = "Payload/AdBloX.app/PlugIns/AdBloXNetworkExtension.appex"

# Anpassat för ditt Apple ID
NEW_BUNDLE = "com.hampuz.adblox"
NEW_EXT_BUNDLE = "com.hampuz.adblox.network"

def refactor():
    print(f"Extraherar {IPA_NAME}...")
    if os.path.exists("extracted"):
        shutil.rmtree("extracted")
    with zipfile.ZipFile(IPA_NAME, 'r') as zip_ref:
        zip_ref.extractall("extracted")

    # 1. Fixa Huvudapp (Info.plist)
    main_plist = os.path.join("extracted", APP_PATH, "Info.plist")
    with open(main_plist, 'rb') as f:
        pl = plistlib.load(f)
    pl['CFBundleIdentifier'] = NEW_BUNDLE
    pl['CFBundleDisplayName'] = "AdBloX MESH"
    with open(main_plist, 'wb') as f:
        plistlib.dump(pl, f)

    # 2. Fixa Extension (Info.plist)
    ext_plist = os.path.join("extracted", EXT_PATH, "Info.plist")
    if os.path.exists(ext_plist):
        with open(ext_plist, 'rb') as f:
            e_pl = plistlib.load(f)
        e_pl['CFBundleIdentifier'] = NEW_EXT_BUNDLE
        # Länka till huvudappen
        if 'NSExtension' in e_pl:
            e_pl['NSExtension']['NSExtensionPrincipalClass'] = "AdBloXNetworkExtension.PacketTunnelProvider"
        with open(ext_plist, 'wb') as f:
            plistlib.dump(e_pl, f)

    # 3. Rensa ALL gamla signaturer så Sideloadly kan skriva nya
    for root, dirs, files in os.walk("extracted"):
        if "_CodeSignature" in dirs:
            shutil.rmtree(os.path.join(root, "_CodeSignature"))

    # 4. Packa ihop direkt i skriptet för att undvika YAML-fel
    shutil.make_archive("AdBloX-MESH-Electric", 'zip', "extracted")
    os.rename("AdBloX-MESH-Electric.zip", OUT_NAME)
    print(f"Klart! Fil skapad: {OUT_NAME}")

if __name__ == "__main__":
    refactor()
