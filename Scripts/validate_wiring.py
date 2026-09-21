import re, os, glob

ROOT = os.path.join(os.path.dirname(__file__), "..")

MEMBER_RE = re.compile(r'<x:Property\s+(?:sap2010:Annotation\.AnnotationText="[^"]*"\s+)?Name="([^"]+)"\s+Type="(?:In|Out|InOut)Argument\((.*?)\)"')
INVOKE_RE = re.compile(
    r'<ui:InvokeWorkflowFile\b[^>]*?WorkflowFileName="([^"]+)"(.*?)</ui:InvokeWorkflowFile>',
    re.DOTALL,
)
ARG_KEY_RE = re.compile(r'<(?:In|Out|InOut)Argument\s+x:TypeArguments="([^"]*)"\s+x:Key="([^"]+)"')

def get_members(path):
    if not os.path.exists(path):
        return None
    text = open(path, encoding="utf-8").read()
    return {m.group(1): m.group(2) for m in MEMBER_RE.finditer(text)}

errors = []
files = glob.glob(os.path.join(ROOT, "**", "*.xaml"), recursive=True)
for f in files:
    text = open(f, encoding="utf-8").read()
    relf = os.path.relpath(f, ROOT)
    for m in INVOKE_RE.finditer(text):
        wf_rel = m.group(1)
        args_block = m.group(2)
        target_path = os.path.join(ROOT, wf_rel)
        target_members = get_members(target_path)
        if target_members is None:
            errors.append(f"{relf}: invokes MISSING file '{wf_rel}'")
            continue
        used_keys = {}
        for am in ARG_KEY_RE.finditer(args_block):
            used_keys[am.group(2)] = am.group(1)
        for key, typearg in used_keys.items():
            if key not in target_members:
                errors.append(f"{relf}: invokes '{wf_rel}' with unknown arg key '{key}'")
        # required members not supplied (only flag In/InOut - OutArgument-only quietly optional is fine but let's flag all missing too)
        for mname in target_members:
            if mname not in used_keys:
                errors.append(f"{relf}: invokes '{wf_rel}' but does NOT supply declared arg '{mname}'")

if errors:
    print(f"{len(errors)} wiring issue(s):")
    for e in errors:
        print(" -", e)
else:
    print("Wiring OK: all InvokeWorkflowFile targets exist and argument keys match declared members.")
