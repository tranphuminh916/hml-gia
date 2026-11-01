import json, os, glob, sys
root = "/home/claude"
b = {}
for p in sorted(glob.glob(root + "/tvbt/*.py")):
    if os.path.basename(p) == "kiemtra.py":
        continue
    b["tvbt/" + os.path.basename(p)] = open(p, encoding="utf-8").read()
lp = "/usr/local/lib/python3.13/site-packages/lunar_python"
for dp, dn, fn in os.walk(lp):
    for f in fn:
        if f.endswith(".py"):
            full = os.path.join(dp, f)
            b["lunar_python/" + os.path.relpath(full, lp)] = open(full, encoding="utf-8").read()
b["app_run.py"] = open("app_run.py", encoding="utf-8").read()
json.dump(b, open("py-bundle.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(len(b), "files", os.path.getsize("py-bundle.json"), "bytes")
