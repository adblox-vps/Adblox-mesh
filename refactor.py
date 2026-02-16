import zipfile, os, plistlib, shutil

IPA_NAME = "AdBloX-MESH-v1.8.2 (3).ipa"
OUT_NAME = "AdBloX-MESH-Electric.ipa"
APP_PATH = "Payload/AdBloX.app"
EXT_PATH = "Payload/AdBloX.app/PlugIns/AdBloXNetworkExtension.appex"

def refactor():
    if os.path.exists("extracted"): shutil.rmtree("extracted")
    with zipfile.ZipFile(IPA_NAME, 'r') as z: z.extractall("extracted")

    # Viktigt: Använd ditt Apple-ID-prefix eller liknande
    GROUP_ID = "group.com.hampuz.adblox"
    NEW_BUNDLE = "com.hampuz.adblox"
    NEW_EXT_BUNDLE = "com.hampuz.adblox.network"

    paths = [APP_PATH, EXT_PATH]
    ids = [NEW_BUNDLE, NEW_EXT_BUNDLE]

    for path, b_id in zip(paths, ids):
        p_list = os.path.join("extracted", path, "Info.plist")
        if os.path.exists(p_list):
            with open(p_list, 'rb') as f: pl = plistlib.load(f)
            pl['CFBundleIdentifier'] = b_id
            pl['CFBundleDisplayName'] = "AdBloX MESH"
            # Skapa den delade gruppen som krävs för VPN
            pl['com.apple.security.application-groups'] = [GROUP_ID]
            with open(p_list, 'wb') as f: plistlib.dump(pl, f)

    # Rensa signaturer
    for r, d, f in os.walk("extracted"):
        if "_CodeSignature" in d: shutil.rmtree(os.path.join(r, "_CodeSignature"))

    shutil.make_archive("final", 'zip', "extracted")
    os.rename("final.zip", OUT_NAME)

if __name__ == "__main__": refactor()
