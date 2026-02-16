import zipfile, os, plistlib, shutil

IPA_NAME = "AdBloX-MESH-v1.8.2 (3).ipa"
OUT_NAME = "AdBloX-MESH-Electric.ipa"
APP_PATH = "Payload/AdBloX.app"
EXT_PATH = "Payload/AdBloX.app/PlugIns/AdBloXNetworkExtension.appex"

def refactor():
    if os.path.exists("extracted"): shutil.rmtree("extracted")
    with zipfile.ZipFile(IPA_NAME, 'r') as z: z.extractall("extracted")

    # Nyckeln är att använda samma Team ID-struktur
    NEW_BUNDLE = "com.hampuz.adblox"
    NEW_EXT_BUNDLE = "com.hampuz.adblox.network"

    # Fixa huvudappen
    main_plist = os.path.join("extracted", APP_PATH, "Info.plist")
    with open(main_plist, 'rb') as f: pl = plistlib.load(f)
    pl['CFBundleIdentifier'] = NEW_BUNDLE
    pl['CFBundleDisplayName'] = "AdBloX MESH"
    # Ta bort gamla grupp-referenser som blockerar tunneln
    pl.pop('com.apple.security.application-groups', None)
    with open(main_plist, 'wb') as f: plistlib.dump(pl, f)

    # Fixa tunnel-motorn (Sideloadly behöver denna intakt)
    ext_plist = os.path.join("extracted", EXT_PATH, "Info.plist")
    if os.path.exists(ext_plist):
        with open(ext_plist, 'rb') as f: e_pl = plistlib.load(f)
        e_pl['CFBundleIdentifier'] = NEW_EXT_BUNDLE
        # Denna rad är avgörande för att iOS ska tillåta tunnel-start
        if 'NSExtension' in e_pl:
            e_pl['NSExtension']['NSExtensionPointIdentifier'] = "com.apple.networkextension.packet-tunnel"
        with open(ext_plist, 'wb') as f: plistlib.dump(e_pl, f)

    # Rensa signaturer men BEHÅLL PlugIns-mappen
    for r, d, f in os.walk("extracted"):
        if "_CodeSignature" in d: shutil.rmtree(os.path.join(r, "_CodeSignature"))

    shutil.make_archive("final", 'zip', "extracted")
    os.rename("final.zip", OUT_NAME)

if __name__ == "__main__": refactor()
