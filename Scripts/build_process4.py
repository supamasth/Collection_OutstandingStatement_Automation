import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from xaml_common import write_xaml

BASE = os.path.join(os.path.dirname(__file__), "..", "Process")

TODO = (
    "TODO (UI Explorer) - placeholder selector, not captured from a live SAP "
    "session for T-Code ZTHSD_OC_GEN_R023. Capture the real element with UI "
    "Explorer before running."
)

members = """    <x:Property Name="in_Config" Type="InArgument(scg:Dictionary(x:String, x:Object))" />
    <x:Property Name="in_SAP" Type="InArgument(ui:Window)" />
    <x:Property Name="in_CustomerID" Type="InArgument(x:String)" />
    <x:Property Name="in_MatGroup" Type="InArgument(x:String)" />
    <x:Property Name="in_MatGroup4" Type="InArgument(x:String)" />
    <x:Property Name="in_Report1FilePath" Type="InArgument(x:String)" />
    <x:Property Name="in_BillDateLow" Type="InArgument(x:String)" />
    <x:Property Name="in_BillDateHigh" Type="InArgument(x:String)" />
    <x:Property Name="in_OutputFolder" Type="InArgument(x:String)" />
    <x:Property Name="in_Timestamp" Type="InArgument(x:String)" />
    <x:Property Name="out_ReportFilePath" Type="OutArgument(x:String)" />
    <x:Property Name="out_TotalYourBrand" Type="OutArgument(x:String)" />"""

body = r"""  <Sequence DisplayName="ExtractReport2_DailySalesReport">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="strFileName" />
      <Variable x:TypeArguments="x:String" Name="strStatusBar" />
      <Variable x:TypeArguments="x:String" Name="strStatusBarType" />
      <Variable x:TypeArguments="sd:DataTable" Name="dtReport1" />
      <Variable x:TypeArguments="sd:DataTable" Name="dtReport2" />
      <Variable x:TypeArguments="scg:List(x:String)" Name="lstDocNos" />
      <Variable x:TypeArguments="x:String" Name="strClipboardText" />
    </Sequence.Variables>
    <ui:LogMessage DisplayName="Log [Report2] Start" Level="Info" Message="[&quot;[Report2] Extracting Daily Sales Report for &quot; + in_CustomerID + &quot; (MatGroup=&quot; + in_MatGroup + &quot;) via &quot; + in_Config(&quot;SapTCode_Report2&quot;).ToString]" />
    <Assign DisplayName="Build strFileName">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[strFileName]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">["DailySalesReport_" + in_CustomerID + "_" + in_Timestamp + ".xlsx"]</InArgument>
      </Assign.Value>
    </Assign>
    <Assign DisplayName="Set out_ReportFilePath">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[out_ReportFilePath]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">[Path.Combine(in_OutputFolder, strFileName)]</InArgument>
      </Assign.Value>
    </Assign>
    <ui:LogMessage DisplayName="Log [Report2] Copying Document Numbers" Level="Info" Message="[&quot;[Report2] Reading Report 1 output to copy Column B (Document no) to clipboard: &quot; + in_Report1FilePath]" />
    <ui:InvokeWorkflowFile DisplayName="Invoke ReadExcelToDatatable (Report1 raw grid)" WorkflowFileName="Common\ReadExcelToDatatable.xaml">
      <ui:InvokeWorkflowFile.Arguments>
        <InArgument x:TypeArguments="x:String" x:Key="in_SourceFile">[in_Report1FilePath]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_SheetName">[""]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_Range">[""]</InArgument>
        <InArgument x:TypeArguments="x:Boolean" x:Key="in_IsColumnName">[False]</InArgument>
        <OutArgument x:TypeArguments="sd:DataTable" x:Key="out_DtResult">[dtReport1]</OutArgument>
      </ui:InvokeWorkflowFile.Arguments>
    </ui:InvokeWorkflowFile>
    <Assign sap2010:Annotation.AnnotationText="Filters on 'is purely digits' rather than relying only on Skip(7) to land past the header row - a real Document No. is always numeric, so this excludes the 'Document no' header label (and any other stray text row) regardless of exactly how many metadata/header rows precede the data in the resaved file. Skip(7) is kept as a coarse first pass for performance, not as the correctness guarantee." DisplayName="Build lstDocNos from Column B, numeric values only">
      <Assign.To>
        <OutArgument x:TypeArguments="scg:List(x:String)">[lstDocNos]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="scg:List(x:String)">[dtReport1.AsEnumerable().Skip(7).Select(Function(r) r(1).ToString.Trim).Where(Function(s) Not String.IsNullOrEmpty(s) AndAlso s.All(AddressOf Char.IsDigit)).Distinct().ToList()]</InArgument>
      </Assign.Value>
    </Assign>
    <Assign DisplayName="Build strClipboardText">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[strClipboardText]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">[String.Join(Environment.NewLine, lstDocNos)]</InArgument>
      </Assign.Value>
    </Assign>
    <ui:LogMessage DisplayName="Log [Report2] Document Count" Level="Info" Message="[&quot;[Report2] &quot; + lstDocNos.Count.ToString + &quot; distinct document number(s) to upload via multi-selection&quot;]" />
    <ui:SetToClipboard sap2010:Annotation.AnnotationText="ASSUMPTION - verify the exact 'Set Clipboard Text' activity name/property against the installed UiPath.System.Activities version (it may be SetToClipboard, or the newer System > Clipboard scope activity)." DisplayName="Set Clipboard Text - Document Numbers" Text="[strClipboardText]" />
    <ui:InvokeWorkflowFile DisplayName="Invoke NavigateToTCode" WorkflowFileName="Workflows\NavigateToTCode.xaml">
      <ui:InvokeWorkflowFile.Arguments>
        <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[in_Config]</InArgument>
        <InArgument x:TypeArguments="ui:Window" x:Key="in_SapWindow">[in_SAP]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_TCode">[in_Config("SapTCode_Report2").ToString]</InArgument>
      </ui:InvokeWorkflowFile.Arguments>
    </ui:InvokeWorkflowFile>
    <ui:TypeInto sap2010:Annotation.AnnotationText="{todo}" Activate="True" DisplayName="Type Into - Sales Organization Field (PLACEHOLDER)" EmptyField="True" Text="[in_Config(&quot;SAP_Report2_SalesOrg&quot;).ToString]">
      <ui:TypeInto.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='SAP_FRONTEND_SESSION' /&gt;&lt;sap id='usr/REPLACE_WITH_SALES_ORG_FIELD_ID' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:TypeInto.Target>
    </ui:TypeInto>
    <ui:TypeInto sap2010:Annotation.AnnotationText="{todo}" Activate="True" DisplayName="Type Into - Material Gr. Field (PLACEHOLDER)" EmptyField="True" Text="[in_MatGroup]">
      <ui:TypeInto.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='SAP_FRONTEND_SESSION' /&gt;&lt;sap id='usr/REPLACE_WITH_MATERIAL_GR_FIELD_ID' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:TypeInto.Target>
    </ui:TypeInto>
    <ui:TypeInto sap2010:Annotation.AnnotationText="{todo}" Activate="True" DisplayName="Type Into - Customer Field (PLACEHOLDER)" EmptyField="True" Text="[in_CustomerID]">
      <ui:TypeInto.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='SAP_FRONTEND_SESSION' /&gt;&lt;sap id='usr/REPLACE_WITH_CUSTOMER_FIELD_ID' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:TypeInto.Target>
    </ui:TypeInto>
    <ui:TypeInto Activate="True" DisplayName="Type Into - Bill Date From Field" EmptyField="True" Text="[in_BillDateLow]">
      <ui:TypeInto.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='SAP_FRONTEND_SESSION' title='TH: Daily Sales Report' /&gt;&lt;sap id='usr/ctxtS_FKDAT-LOW' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:TypeInto.Target>
    </ui:TypeInto>
    <ui:TypeInto Activate="True" DisplayName="Type Into - Bill Date To Field" EmptyField="True" Text="[in_BillDateHigh]">
      <ui:TypeInto.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='SAP_FRONTEND_SESSION' title='TH: Daily Sales Report' /&gt;&lt;sap id='usr/ctxtS_FKDAT-HIGH' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:TypeInto.Target>
    </ui:TypeInto>
    <ui:Click sap2010:Annotation.AnnotationText="{todo} This is the small multi-selection (yellow arrow) icon at the right edge of the Bill No. input field." ClickType="CLICK_SINGLE" DisplayName="Click - Multi Selection Icon on Bill No. Field (PLACEHOLDER)">
      <ui:Click.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='SAP_FRONTEND_SESSION' /&gt;&lt;sap id='usr/REPLACE_WITH_BILLNO_MULTISELECT_BUTTON_ID' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:Click.Target>
    </ui:Click>
    <Delay DisplayName="Delay - Wait for Multi Selection Popup" Duration="[TimeSpan.FromSeconds(1.5)]" />
    <ui:LogMessage DisplayName="Log [Report2] Uploading from Clipboard" Level="Info" Message="[&quot;[Report2] Multi-selection popup open - uploading document numbers from clipboard (Shift+F12)&quot;]" />
    <ui:SendHotkey Activate="True" DisplayName="Send Hotkey - Shift+F12 (Upload from Clipboard)" Key="f12" KeyModifiers="Shift" SpecialKey="True">
      <ui:SendHotkey.Target>
        <ui:Target>
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:SendHotkey.Target>
    </ui:SendHotkey>
    <Delay DisplayName="Delay - Wait for Upload" Duration="[TimeSpan.FromSeconds(1)]" />
    <ui:SendHotkey Activate="True" DisplayName="Send Hotkey - F8 (Copy/Confirm Popup)" Key="f8" KeyModifiers="None" SpecialKey="True">
      <ui:SendHotkey.Target>
        <ui:Target>
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:SendHotkey.Target>
    </ui:SendHotkey>
    <Delay DisplayName="Delay - Wait for Popup Close" Duration="[TimeSpan.FromSeconds(1)]" />
    <ui:LogMessage DisplayName="Log [Report2] Executing" Level="Info" Message="[&quot;[Report2] Back on main screen - executing (F8)&quot;]" />
    <ui:SendHotkey Activate="True" DisplayName="Send Hotkey - F8 (Execute Report)" Key="f8" KeyModifiers="None" SpecialKey="True">
      <ui:SendHotkey.Target>
        <ui:Target>
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:SendHotkey.Target>
    </ui:SendHotkey>
    <Delay DisplayName="Delay - Wait for Report to Render" Duration="[TimeSpan.FromSeconds(3)]" />
    <ucas:ReadStatusbar DisplayName="ReadStatusbar - Check SAP Status After Execute" MessageText="[strStatusBar]" MessageType="[strStatusBarType]">
      <ucas:ReadStatusbar.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='SAP_FRONTEND_SESSION' /&gt;&lt;sap id='sbar/pane[0]' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ucas:ReadStatusbar.Target>
    </ucas:ReadStatusbar>
    <If Condition="[strStatusBarType = &quot;E&quot; OrElse (Not String.IsNullOrEmpty(strStatusBar) AndAlso (strStatusBar.Contains(&quot;Error&quot;) OrElse strStatusBar.Contains(&quot;error&quot;) OrElse strStatusBar.Contains(&quot;ไม่&quot;)))]" DisplayName="If SAP Status Shows Error - Throw BRE">
      <If.Then>
        <Throw DisplayName="Throw AppEx - SAP Error" Exception="[New Exception(&quot;[Report2] SAP error after F8: &quot; + strStatusBar)]" />
      </If.Then>
      <If.Else>
        <Sequence DisplayName="" />
      </If.Else>
    </If>
    <ui:LogMessage DisplayName="Log [Report2] Exporting" Level="Info" Message="[&quot;[Report2] Exporting via Ctrl+Shift+F7&quot;]" />
    <ui:SendHotkey Activate="True" DisplayName="Send Hotkey - Ctrl+Shift+F7 (Export)" Key="f7" KeyModifiers="Ctrl, Shift" SpecialKey="True">
      <ui:SendHotkey.Target>
        <ui:Target>
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:SendHotkey.Target>
    </ui:SendHotkey>
    <Delay DisplayName="Delay - Wait for Save File Dialog" Duration="[TimeSpan.FromSeconds(3)]" />
    <ui:TypeInto Activate="True" DisplayName="Type Into - Save Dialog Folder" EmptyField="True" Text="[in_OutputFolder]">
      <ui:TypeInto.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='#32770' title='Save File' idx='*' /&gt;&lt;sap id='usr/ctxtDY_PATH' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:TypeInto.Target>
    </ui:TypeInto>
    <ui:TypeInto Activate="True" DisplayName="Type Into - Save Dialog File Name" EmptyField="True" Text="[strFileName]">
      <ui:TypeInto.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='#32770' title='Save File' idx='*' /&gt;&lt;sap id='usr/ctxtDY_FILENAME' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:TypeInto.Target>
    </ui:TypeInto>
    <ui:Click ClickType="CLICK_SINGLE" DisplayName="Click - Replace/Generate Button">
      <ui:Click.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='#32770' title='Save File' idx='*' /&gt;&lt;sap id='tbar[0]/btn[11]' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:Click.Target>
    </ui:Click>
    <Delay DisplayName="Delay - Wait for File Write" Duration="[TimeSpan.FromSeconds(2)]" />
    <If Condition="[Not File.Exists(out_ReportFilePath)]" DisplayName="If File Not Found - Throw BRE">
      <If.Then>
        <Throw DisplayName="Throw AppEx - Export File Missing" Exception="[New Exception(&quot;[Report2] Export completed but file not found at: &quot; + out_ReportFilePath)]" />
      </If.Then>
      <If.Else>
        <Sequence DisplayName="" />
      </If.Else>
    </If>
    <ui:LogMessage DisplayName="Log [Report2] Parsing Sales Amt. Total" Level="Info" Message="[&quot;[Report2] Reading &quot; + out_ReportFilePath + &quot; to extract the last row's Sales Amt. total by header name&quot;]" />
    <ui:InvokeWorkflowFile DisplayName="Invoke ReadExcelToDatatable (headers at row 1)" WorkflowFileName="Common\ReadExcelToDatatable.xaml">
      <ui:InvokeWorkflowFile.Arguments>
        <InArgument x:TypeArguments="x:String" x:Key="in_SourceFile">[out_ReportFilePath]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_SheetName">[""]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_Range">[""]</InArgument>
        <InArgument x:TypeArguments="x:Boolean" x:Key="in_IsColumnName">[True]</InArgument>
        <OutArgument x:TypeArguments="sd:DataTable" x:Key="out_DtResult">[dtReport2]</OutArgument>
      </ui:InvokeWorkflowFile.Arguments>
    </ui:InvokeWorkflowFile>
    <If Condition="[dtReport2.Columns.Contains(&quot;Sales Amt.&quot;) AndAlso dtReport2.Rows.Count &gt; 0]" DisplayName="If Sales Amt. Column and Rows Exist">
      <If.Then>
        <Assign DisplayName="Set out_TotalYourBrand (last row, Sales Amt. column, by header name)">
          <Assign.To>
            <OutArgument x:TypeArguments="x:String">[out_TotalYourBrand]</OutArgument>
          </Assign.To>
          <Assign.Value>
            <InArgument x:TypeArguments="x:String">[dtReport2.Rows(dtReport2.Rows.Count - 1)("Sales Amt.").ToString.Trim]</InArgument>
          </Assign.Value>
        </Assign>
      </If.Then>
      <If.Else>
        <Sequence DisplayName="Sales Amt. Column Not Found - Throw BRE">
          <Throw DisplayName="Throw AppEx - Sales Amt. Column Missing" Exception="[New Exception(&quot;[Report2] Expected header 'Sales Amt.' not found in exported file, or file has no data rows. Actual columns: &quot; + String.Join(&quot;, &quot;, dtReport2.Columns.Cast(Of DataColumn)().Select(Function(c) c.ColumnName)))]" />
        </Sequence>
      </If.Else>
    </If>
    <ui:LogMessage DisplayName="Log [Report2] Done" Level="Info" Message="[&quot;[Report2] Done. File=&quot; + out_ReportFilePath + &quot; | TotalYourBrand=&quot; + out_TotalYourBrand]" />
  </Sequence>""".replace("{todo}", TODO)

write_xaml(os.path.join(BASE, "ExtractReport2_DailySalesReport.xaml"), "ExtractReport2_DailySalesReport", members, body)

print("Process part 4 done.")
