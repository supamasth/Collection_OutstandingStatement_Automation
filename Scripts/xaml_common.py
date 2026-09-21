# Shared header/footer for hand-authored REFramework XAML files in this project.
# Namespace / assembly lists are the UNION of what real, verified XAML files in
# MyRPA\Collection_GFMIS_Automation actually declare (Main.xaml, InitAllSettings.xaml,
# SendAlertEmail.xaml, NavigateToTCode.xaml, PB_GenerateSAPReport.xaml,
# ReadExcelToDatatable.xaml, TakeScreenshot.xaml, KillAllProcesses.xaml) -- nothing
# invented, so every referenced assembly is guaranteed to already be a project
# dependency (UiPath.Excel.Activities, UiPath.Mail.Activities, UiPath.System.Activities,
# UiPath.UIAutomation.Activities -- see project.json).

ROOT_OPEN = (
    '<Activity mc:Ignorable="sap sap2010" x:Class="{cls}" '
    'xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities" '
    'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
    'xmlns:s="clr-namespace:System;assembly=System.Private.CoreLib" '
    'xmlns:sap="http://schemas.microsoft.com/netfx/2009/xaml/activities/presentation" '
    'xmlns:sap2010="http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation" '
    'xmlns:scg="clr-namespace:System.Collections.Generic;assembly=System.Private.CoreLib" '
    'xmlns:sco="clr-namespace:System.Collections.ObjectModel;assembly=System.Private.CoreLib" '
    'xmlns:sd="clr-namespace:System.Data;assembly=System.Data.Common" '
    'xmlns:si="clr-namespace:System.IO;assembly=System.Private.CoreLib" '
    'xmlns:snm="clr-namespace:System.Net.Mail;assembly=System.Net.Mail" '
    'xmlns:srx="clr-namespace:System.Text.RegularExpressions;assembly=System.Text.RegularExpressions" '
    'xmlns:ucas="clr-namespace:UiPath.Core.Activities.SAP;assembly=UiPath.UiAutomation.Activities" '
    'xmlns:ui="http://schemas.uipath.com/workflow/activities" '
    'xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">'
)

NAMESPACES = [
    "Microsoft.VisualBasic", "Microsoft.VisualBasic.Activities", "Microsoft.VisualBasic.CompilerServices",
    "System", "System.Activities", "System.Activities.Expressions", "System.Activities.Statements",
    "System.Activities.Validation", "System.Activities.XamlIntegration", "System.Activities.Runtime.Collections",
    "System.Collections", "System.Collections.Generic", "System.Collections.ObjectModel",
    "System.ComponentModel", "System.Data", "System.Diagnostics", "System.Drawing", "System.IO",
    "System.Linq", "System.Net.Mail", "System.Reflection", "System.Runtime.InteropServices",
    "System.Runtime.Serialization", "System.Text.RegularExpressions",
    "System.Windows.Markup", "System.Xml", "System.Xml.Linq",
    "System.Xml.Serialization", "UiPath.Core", "UiPath.Core.Activities", "UiPath.Core.Activities.SAP",
    "UiPath.Excel", "UiPath.Excel.Activities", "UiPath.Mail", "UiPath.Mail.Activities",
    "UiPath.Mail.Outlook.Activities", "UiPath.Shared.Activities", "UiPath.Platform.ObjectLibrary",
    "UiPath.UIAutomationCore.Contracts", "UiPath.UIAutomationNext.Activities", "UiPath.UIAutomationNext.Enums",
    "GlobalVariablesNamespace", "GlobalConstantsNamespace",
]

ASSEMBLIES = [
    "Microsoft.VisualBasic", "Microsoft.VisualBasic.Core", "Microsoft.VisualBasic.Forms",
    "Microsoft.Win32.Primitives", "mscorlib", "NPOI", "PresentationCore", "PresentationFramework",
    "System", "System.Activities", "System.Collections", "System.Collections.NonGeneric",
    "System.Collections.Immutable", "System.ComponentModel", "System.ComponentModel.Composition",
    "System.ComponentModel.EventBasedAsync", "System.ComponentModel.Primitives",
    "System.ComponentModel.TypeConverter", "System.Configuration.ConfigurationManager", "System.Console",
    "System.Core", "System.Data", "System.Data.Common", "System.Data.DataSetExtensions",
    "System.Data.SqlClient", "System.Diagnostics.Process", "System.Drawing", "System.Drawing.Common",
    "System.Drawing.Primitives", "System.IO.FileSystem", "System.IO.FileSystem.AccessControl",
    "System.IO.FileSystem.DriveInfo", "System.IO.FileSystem.Watcher", "System.IO.Packaging", "System.Linq",
    "System.Linq.Expressions", "System.Linq.Parallel", "System.Linq.Queryable", "System.Memory",
    "System.Memory.Data", "System.Net.Mail", "System.ObjectModel", "System.Private.CoreLib",
    "System.Private.DataContractSerialization", "System.Private.ServiceModel", "System.Private.Uri",
    "System.Private.Xml", "System.Reflection.DispatchProxy", "System.Reflection.Metadata",
    "System.Reflection.TypeExtensions", "System.Runtime.Serialization.Formatters",
    "System.Runtime.Serialization.Primitives", "System.Security.Permissions", "System.ServiceModel",
    "System.Text.RegularExpressions",
    "System.ValueTuple", "System.Xaml", "System.Xml", "System.Xml.Linq", "UiPath.Excel",
    "UiPath.Excel.Activities", "UiPath.Excel.Activities.Design", "UiPath.Mail", "UiPath.Mail.Activities",
    "UiPath.Mail.Activities.Design", "UiPath.OCR.Activities", "UiPath.OCR.Activities.Design",
    "UiPath.Platform", "UiPath.Studio.Constants", "UiPath.System.Activities",
    "UiPath.System.Activities.Design", "UiPath.System.Activities.ViewModels", "UiPath.UiAutomation.Activities",
    "UiPath.UIAutomationCore", "UiPath.UIAutomationNext", "UiPath.UIAutomationNext.Activities",
    "UiPath.Workflow", "WindowsBase",
]


def build_xaml(cls, members_xml, body_xml):
    ns_xml = "\n".join(f"      <x:String>{n}</x:String>" for n in NAMESPACES)
    asm_xml = "\n".join(f"      <AssemblyReference>{a}</AssemblyReference>" for a in ASSEMBLIES)
    members_block = ""
    if members_xml.strip():
        members_block = f"  <x:Members>\n{members_xml}\n  </x:Members>\n"
    return (
        ROOT_OPEN.format(cls=cls) + "\n"
        + members_block
        + '  <VisualBasic.Settings>\n    <x:Null />\n  </VisualBasic.Settings>\n'
        + '  <TextExpression.NamespacesForImplementation>\n'
        + f'    <sco:Collection x:TypeArguments="x:String">\n{ns_xml}\n    </sco:Collection>\n'
        + '  </TextExpression.NamespacesForImplementation>\n'
        + '  <TextExpression.ReferencesForImplementation>\n'
        + f'    <scg:List x:TypeArguments="AssemblyReference" Capacity="{len(ASSEMBLIES)}">\n{asm_xml}\n    </scg:List>\n'
        + '  </TextExpression.ReferencesForImplementation>\n'
        + body_xml + "\n"
        + "</Activity>\n"
    )


def write_xaml(path, cls, members_xml, body_xml):
    content = build_xaml(cls, members_xml, body_xml)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"wrote {path}")
