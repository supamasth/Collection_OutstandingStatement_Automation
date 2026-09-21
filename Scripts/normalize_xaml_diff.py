import re, sys

def normalize(text):
    # Strip Studio-only cosmetic attributes (order-independent, don't affect logic)
    text = re.sub(r'\s+sap:VirtualizedContainerService\.HintSize="[^"]*"', '', text)
    text = re.sub(r'\s+sap2010:WorkflowViewState\.IdRef="[^"]*"', '', text)
    text = re.sub(r'\s+InformativeScreenshot="[^"]*"', '', text)
    text = re.sub(r'\s+Id="[^"]*"', '', text)
    # Strip whole ViewState dictionary blocks (IsExpanded/IsPinned/IsAnnotationDocked bookkeeping)
    text = re.sub(r'<sap:WorkflowViewStateService\.ViewState>.*?</sap:WorkflowViewStateService\.ViewState>\s*', '', text, flags=re.DOTALL)
    # Collapse whitespace differences
    text = re.sub(r'>\s+<', '><', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

a = normalize(open(sys.argv[1], encoding='utf-8').read())
b = normalize(open(sys.argv[2], encoding='utf-8').read())

if a == b:
    print(f"SEMANTICALLY IDENTICAL: {sys.argv[1]} vs {sys.argv[2]}")
else:
    print(f"DIFFERENCES FOUND: {sys.argv[1]} vs {sys.argv[2]}")
    # crude line-based diff after normalization, splitting on tag boundaries for readability
    import difflib
    al = a.replace('><', '>\n<').split('\n')
    bl = b.replace('><', '>\n<').split('\n')
    for line in difflib.unified_diff(al, bl, lineterm='', n=1):
        print(line)
