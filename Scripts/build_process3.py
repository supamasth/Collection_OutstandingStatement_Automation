import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from xaml_common import write_xaml

BASE = os.path.join(os.path.dirname(__file__), "..", "Process")

TODO_NOTE = (
    "TODO (UI Explorer) - this selector is a placeholder. It could not be captured "
    "without a live SAP session for T-Code {tcode}. Open the T-Code in SAP GUI, "
    "use UiPath UI Explorer to capture the real element, and replace this selector "
    "before running."
)

# ---------------------------------------------------------------------------
# ExtractReport1_CustomerStatement.xaml  (Section 4, T-Code YFI_OC_GEN_I039)
# Selection-screen variant flow (Get Variant popup, Find Variant dialog,
# F8 execute, ReadStatusbar error check) is adapted from the verified,
# working pattern in Workflows\PB_GenerateSAPReport.xaml (same SAP GUI ALV
# report mechanism, standard toolbar positions). The Customer ID input field
# on this specific T-Code's selection screen is report-specific and NOT
# captured here - see the TODO annotation below.
#
# File output mechanism (corrected): YFI_OC_GEN_I039 exports automatically as
# part of F8 execution via the "Local Folder Path" selection-screen field
# (usr/ctxtP_LOCAL) - there is no separate interactive List/Export/Spreadsheet
# step. The robot only controls the destination FOLDER via that field; SAP
# generates the actual FILENAME itself as
# Summary_TH88_<CustomerID zero-padded to 10 digits>_<yyyyMMdd>.XLS and reports
# the full path in the status bar as "Download <size> <unit> <full path>"
# immediately after F8. The real path is therefore extracted from the status
# bar with a regex rather than constructed by the robot.
# ---------------------------------------------------------------------------
members = """    <x:Property Name="in_Config" Type="InArgument(scg:Dictionary(x:String, x:Object))" />
    <x:Property Name="in_SAP" Type="InArgument(ui:Window)" />
    <x:Property Name="in_CustomerID" Type="InArgument(x:String)" />
    <x:Property Name="in_OutputFolder" Type="InArgument(x:String)" />
    <x:Property Name="in_Timestamp" Type="InArgument(x:String)" />
    <x:Property Name="out_ReportFilePath" Type="OutArgument(x:String)" />
    <x:Property Name="out_CustomerName" Type="OutArgument(x:String)" />
    <x:Property Name="out_Account" Type="OutArgument(x:String)" />
    <x:Property Name="out_GeneratedOn" Type="OutArgument(x:String)" />
    <x:Property Name="out_TotalAllProducts" Type="OutArgument(x:String)" />
    <x:Property Name="out_BillDateLow" Type="OutArgument(x:String)" />
    <x:Property Name="out_BillDateHigh" Type="OutArgument(x:String)" />
    <x:Property Name="out_HasOutstandingItems" Type="OutArgument(x:Boolean)" />"""

body = r"""  <Sequence DisplayName="ExtractReport1_CustomerStatement">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="strStatusBar" />
      <Variable x:TypeArguments="x:String" Name="strStatusBarType" />
      <Variable x:TypeArguments="x:String" Name="strReport1FilePath" />
      <Variable x:TypeArguments="x:String" Name="strReport1FileName" />
      <Variable x:TypeArguments="sd:DataTable" Name="dtRaw" />
      <Variable x:TypeArguments="scg:List(s:DateTime)" Name="lstReport1Dates" />
      <Variable x:TypeArguments="x:Int32" Name="intReport1DateCandidates" />
      <Variable x:TypeArguments="s:DateTime" Name="dtReport1MinDate" />
      <Variable x:TypeArguments="s:DateTime" Name="dtReport1MaxDate" />
      <Variable x:TypeArguments="x:String" Name="strBillDateLow" />
      <Variable x:TypeArguments="x:String" Name="strBillDateHigh" />
    </Sequence.Variables>
    <ui:LogMessage DisplayName="Log [Report1] Start" Level="Info" Message="[&quot;[Report1] Extracting Customer Statement for &quot; + in_CustomerID + &quot; via &quot; + in_Config(&quot;SapTCode_Report1&quot;).ToString]" />
    <ui:CreateDirectory Path="[in_OutputFolder]" />
    <ui:InvokeWorkflowFile DisplayName="Invoke NavigateToTCode" WorkflowFileName="Workflows\NavigateToTCode.xaml">
      <ui:InvokeWorkflowFile.Arguments>
        <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[in_Config]</InArgument>
        <InArgument x:TypeArguments="ui:Window" x:Key="in_SapWindow">[in_SAP]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_TCode">[in_Config("SapTCode_Report1").ToString]</InArgument>
      </ui:InvokeWorkflowFile.Arguments>
    </ui:InvokeWorkflowFile>
    <ui:LogMessage DisplayName="Log [Report1] Applying Variant" Level="Info" Message="[&quot;[Report1] Applying SAP variant: &quot; + in_Config(&quot;SAP_Report1_Variant&quot;).ToString]" />
    <ui:Click sap2010:Annotation.AnnotationText="Adapted from Workflows\PB_GenerateSAPReport.xaml (verified working selector on a different Y/Z report's selection screen). tbar[1]/btn[17] is the standard 'Get Variant' toolbar position on ABAP report selection screens - re-verify with UI Explorer if it does not match on YFI_OC_GEN_I039." ClickType="CLICK_SINGLE" DisplayName="Click - Get Variant Button">
      <ui:Click.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='SAP_FRONTEND_SESSION' /&gt;&lt;sap id='tbar[1]/btn[17]' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:Click.Target>
    </ui:Click>
    <Delay DisplayName="Delay - Wait for Find Variant Dialog" Duration="[TimeSpan.FromSeconds(1)]" />
    <ui:TypeInto Activate="True" DisplayName="Type Into - Variant Name Field" EmptyField="True" Text="[in_Config(&quot;SAP_Report1_Variant&quot;).ToString]">
      <ui:TypeInto.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='#32770' title='Find Variant' idx='*' /&gt;&lt;sap id='usr/txtV-LOW' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:TypeInto.Target>
    </ui:TypeInto>
    <ui:Click ClickType="CLICK_SINGLE" DisplayName="Click - Execute in Find Variant Dialog">
      <ui:Click.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='#32770' title='Find Variant' idx='*' /&gt;&lt;sap id='tbar[0]/btn[8]' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:Click.Target>
    </ui:Click>
    <Delay DisplayName="Delay - Wait for Variant Applied" Duration="[TimeSpan.FromSeconds(1)]" />
    <ui:TypeInto sap2010:Annotation.AnnotationText="{todo}" Activate="True" DisplayName="Type Into - Customer ID Field (PLACEHOLDER SELECTOR)" EmptyField="True" Text="[in_CustomerID]">
      <ui:TypeInto.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='SAP_FRONTEND_SESSION' /&gt;&lt;sap id='usr/REPLACE_WITH_CUSTOMER_ID_FIELD_ID' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:TypeInto.Target>
    </ui:TypeInto>
    <ui:TypeInto Activate="True" DelayBetweenKeys="100" DisplayName="TypeInto — Save File Path" EmptyField="True" Text="[in_OutputFolder]">
      <ui:TypeInto.Target>
        <ui:Target Selector="&lt;wnd app='saplogon.exe' cls='SAP_FRONTEND_SESSION' title='GLT: Customer Statement' /&gt;&lt;sap id='usr/ctxtP_LOCAL' /&gt;">
          <ui:Target.TimeoutMS>
            <InArgument x:TypeArguments="x:Int32" />
          </ui:Target.TimeoutMS>
        </ui:Target>
      </ui:TypeInto.Target>
    </ui:TypeInto>
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
        <Throw DisplayName="Throw AppEx - SAP Error" Exception="[New Exception(&quot;[Report1] SAP error after F8: &quot; + strStatusBar)]" />
      </If.Then>
      <If.Else>
        <Sequence DisplayName="" />
      </If.Else>
    </If>
    <Assign DisplayName="Extract strReport1FilePath from SAP Status Bar (regex)">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[strReport1FilePath]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">[Regex.Match(strStatusBar, "[A-Za-z]:\\.*\.xlsx?|[A-Za-z]:\\.*\.XLS", RegexOptions.IgnoreCase).Value.Trim()]</InArgument>
      </Assign.Value>
    </Assign>
    <Assign DisplayName="Extract strReport1FileName from strReport1FilePath">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[strReport1FileName]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">[Path.GetFileName(strReport1FilePath)]</InArgument>
      </Assign.Value>
    </Assign>
    <If Condition="[String.IsNullOrWhiteSpace(strReport1FilePath) OrElse Not File.Exists(strReport1FilePath)]" DisplayName="If Report1 File Path Not Found - Throw System Exception">
      <If.Then>
        <Throw DisplayName="Throw AppEx - Cannot Extract Report1 File Path" Exception="[New Exception(&quot;[Report1] Could not extract a valid output file path from the SAP status bar after export. Raw status bar: &apos;&quot; + strStatusBar + &quot;&apos; | Extracted (if any): &apos;&quot; + strReport1FilePath + &quot;&apos;&quot;)]" />
      </If.Then>
      <If.Else>
        <Sequence DisplayName="" />
      </If.Else>
    </If>
    <Assign DisplayName="Set out_ReportFilePath = strReport1FilePath">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[out_ReportFilePath]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">[strReport1FilePath]</InArgument>
      </Assign.Value>
    </Assign>
    <ui:LogMessage DisplayName="Log [Report1] Extracted File Path from Status Bar" Level="Info" Message="[&quot;[Report1] SAP-generated file: &quot; + strReport1FileName + &quot; at &quot; + strReport1FilePath]" />
    <ui:LogMessage DisplayName="Log [Report1] Parsing Header and Deleting Column L" Level="Info" Message="[&quot;[Report1] Reading &quot; + out_ReportFilePath + &quot; to parse header block and remove Client/Brand column (L)&quot;]" />
    <ui:InvokeWorkflowFile DisplayName="Invoke ReadExcelToDatatable (raw grid)" WorkflowFileName="Common\ReadExcelToDatatable.xaml">
      <ui:InvokeWorkflowFile.Arguments>
        <InArgument x:TypeArguments="x:String" x:Key="in_SourceFile">[out_ReportFilePath]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_SheetName">[""]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_Range">[""]</InArgument>
        <InArgument x:TypeArguments="x:Boolean" x:Key="in_IsColumnName">[False]</InArgument>
        <OutArgument x:TypeArguments="sd:DataTable" x:Key="out_DtResult">[dtRaw]</OutArgument>
      </ui:InvokeWorkflowFile.Arguments>
    </ui:InvokeWorkflowFile>
    <Assign DisplayName="Set out_CustomerName (Row 3, Col B)">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[out_CustomerName]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">[dtRaw.Rows(2)(1).ToString.Trim]</InArgument>
      </Assign.Value>
    </Assign>
    <Assign DisplayName="Set out_Account (Row 4, Col B)">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[out_Account]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">[dtRaw.Rows(3)(1).ToString.Trim]</InArgument>
      </Assign.Value>
    </Assign>
    <Assign DisplayName="Set out_GeneratedOn (Row 5, Col B)">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[out_GeneratedOn]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">[dtRaw.Rows(4)(1).ToString.Trim]</InArgument>
      </Assign.Value>
    </Assign>
    <Assign DisplayName="Set out_TotalAllProducts (Last Row, Col H = Amount (THB), index 7)">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[out_TotalAllProducts]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">[dtRaw.Rows(dtRaw.Rows.Count - 1)(7).ToString.Trim]</InArgument>
      </Assign.Value>
    </Assign>
    <Assign DisplayName="Build lstReport1Dates from Column A, data rows only (Excel row 8+)">
      <Assign.To>
        <OutArgument x:TypeArguments="scg:List(s:DateTime)">[lstReport1Dates]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="scg:List(s:DateTime)">[dtRaw.AsEnumerable().Skip(7).Select(Function(r) If(TypeOf r(0) Is DateTime, CType(CType(r(0), DateTime), DateTime?), If(r(0) IsNot Nothing AndAlso Not IsDBNull(r(0)) AndAlso Not String.IsNullOrWhiteSpace(r(0).ToString) AndAlso Regex.IsMatch(r(0).ToString.Trim, "^\d{1,2}\.\d{1,2}\.\d{4}$") AndAlso CInt(r(0).ToString.Trim.Split("."c)(0)) &gt;= 1 AndAlso CInt(r(0).ToString.Trim.Split("."c)(0)) &lt;= 31 AndAlso CInt(r(0).ToString.Trim.Split("."c)(1)) &gt;= 1 AndAlso CInt(r(0).ToString.Trim.Split("."c)(1)) &lt;= 12, CType(DateTime.ParseExact(r(0).ToString.Trim, "dd.MM.yyyy", System.Globalization.CultureInfo.InvariantCulture), DateTime?), CType(Nothing, DateTime?)))).Where(Function(d) d.HasValue).Select(Function(d) d.Value).ToList()]</InArgument>
      </Assign.Value>
    </Assign>
    <Assign DisplayName="Count Non-Blank Date Candidates in Column A (for parse-failure warning)">
      <Assign.To>
        <OutArgument x:TypeArguments="x:Int32">[intReport1DateCandidates]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:Int32">[dtRaw.AsEnumerable().Skip(7).Count(Function(r) r(0) IsNot Nothing AndAlso Not IsDBNull(r(0)) AndAlso Not String.IsNullOrWhiteSpace(r(0).ToString))]</InArgument>
      </Assign.Value>
    </Assign>
    <If Condition="[lstReport1Dates.Count = 0]" DisplayName="If No Valid Dates Found - No Outstanding Items">
      <If.Then>
        <Sequence DisplayName="No Outstanding Items">
          <ui:LogMessage Level="Info" Message="[&quot;[Report1] No rows with a valid Date found for &quot; + in_CustomerID + &quot; - customer has no outstanding items.&quot;]" />
          <Assign DisplayName="Set out_HasOutstandingItems = False">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_HasOutstandingItems]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">False</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_BillDateLow = Empty">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[out_BillDateLow]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">""</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_BillDateHigh = Empty">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[out_BillDateHigh]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">""</InArgument>
            </Assign.Value>
          </Assign>
        </Sequence>
      </If.Then>
      <If.Else>
        <Sequence DisplayName="Compute Bill Date Range">
          <Assign DisplayName="Set out_HasOutstandingItems = True">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_HasOutstandingItems]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">True</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Compute dtReport1MinDate">
            <Assign.To>
              <OutArgument x:TypeArguments="s:DateTime">[dtReport1MinDate]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="s:DateTime">[lstReport1Dates.Min()]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Compute dtReport1MaxDate">
            <Assign.To>
              <OutArgument x:TypeArguments="s:DateTime">[dtReport1MaxDate]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="s:DateTime">[lstReport1Dates.Max()]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Format strBillDateLow">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[strBillDateLow]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">[dtReport1MinDate.ToString("dd.MM.yyyy")]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Format strBillDateHigh">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[strBillDateHigh]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">[dtReport1MaxDate.ToString("dd.MM.yyyy")]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_BillDateLow">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[out_BillDateLow]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">[strBillDateLow]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_BillDateHigh">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[out_BillDateHigh]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">[strBillDateHigh]</InArgument>
            </Assign.Value>
          </Assign>
          <ui:LogMessage Level="Info" Message="[&quot;[Report1] Bill Date range for &quot; + in_CustomerID + &quot;: &quot; + strBillDateLow + &quot; to &quot; + strBillDateHigh + &quot; (&quot; + lstReport1Dates.Count.ToString + &quot; row(s))&quot;]" />
          <If Condition="[(intReport1DateCandidates - lstReport1Dates.Count) &gt; 0]" DisplayName="If Some Dates Failed To Parse - Log Warning">
            <If.Then>
              <ui:LogMessage Level="Warn" Message="[&quot;[Report1] &quot; + (intReport1DateCandidates - lstReport1Dates.Count).ToString + &quot; row(s) had a non-blank Date in Column A that could not be parsed (expected format dd.MM.yyyy) and were skipped from the Bill Date range.&quot;]" />
            </If.Then>
            <If.Else>
              <Sequence DisplayName="" />
            </If.Else>
          </If>
        </Sequence>
      </If.Else>
    </If>
    <InvokeMethod DisplayName="Remove Column L (Client/Brand, 0-based index 11)" MethodName="RemoveAt">
      <InvokeMethod.TargetObject>
        <InArgument x:TypeArguments="sd:DataColumnCollection">[dtRaw.Columns]</InArgument>
      </InvokeMethod.TargetObject>
      <InArgument x:TypeArguments="x:Int32">11</InArgument>
    </InvokeMethod>
    <ui:InvokeWorkflowFile sap2010:Annotation.AnnotationText="Rewrites the sheet as a plain value grid starting at A1. This preserves all row data (no rows are dropped) but does not preserve the original cell formatting/number formats from the SAP export - flag to the business if that matters; if so this step should be redone as an in-place NPOI/COM column delete instead." DisplayName="Invoke WriteRangeOverwrite (save without Column L)" WorkflowFileName="Common\WriteRangeOverwrite.xaml">
      <ui:InvokeWorkflowFile.Arguments>
        <InArgument x:TypeArguments="x:String" x:Key="in_SourceFile">[out_ReportFilePath]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_SheetName">Sheet1</InArgument>
        <InArgument x:TypeArguments="sd:DataTable" x:Key="in_Datatable">[dtRaw]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_StartingCell">A1</InArgument>
      </ui:InvokeWorkflowFile.Arguments>
    </ui:InvokeWorkflowFile>
    <ui:LogMessage DisplayName="Log [Report1] Done" Level="Info" Message="[&quot;[Report1] Done. File=&quot; + out_ReportFilePath + &quot; | Customer=&quot; + out_CustomerName + &quot; | TotalAllProducts=&quot; + out_TotalAllProducts]" />
  </Sequence>""".replace("{todo}", TODO_NOTE.format(tcode="YFI_OC_GEN_I039"))

write_xaml(os.path.join(BASE, "ExtractReport1_CustomerStatement.xaml"), "ExtractReport1_CustomerStatement", members, body)

print("Process part 3 done.")
