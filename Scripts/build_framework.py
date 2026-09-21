import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from xaml_common import write_xaml

BASE = os.path.join(os.path.dirname(__file__), "..", "Framework")

# ---------------------------------------------------------------------------
# InitAllApplications.xaml
# ---------------------------------------------------------------------------
members = """    <x:Property Name="out_Config" Type="OutArgument(scg:Dictionary(x:String, x:Object))" />
    <x:Property Name="out_SAP" Type="OutArgument(ui:Window)" />
    <x:Property Name="out_dtCustomerMaster" Type="OutArgument(sd:DataTable)" />
    <x:Property Name="out_dtMasterExcel" Type="OutArgument(sd:DataTable)" />"""

body = r"""  <Sequence DisplayName="InitAllApplications">
    <Sequence.Variables>
      <Variable x:TypeArguments="sd:DataTable" Name="dt_Sheet" />
      <Variable x:TypeArguments="scg:List(x:String)" Name="lstSapError" />
      <Variable x:TypeArguments="x:String" Name="strSapUsername" />
    </Sequence.Variables>
    <ui:LogMessage DisplayName="Log [Init] Process Started" Level="Info" Message="[&quot;[Init] Process started - &quot; + Now.ToString(&quot;yyyy-MM-dd HH:mm:ss&quot;)]" />
    <Assign DisplayName="Initialize Config Dictionary">
      <Assign.To>
        <OutArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)">[out_Config]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)">[New Dictionary(Of String, Object)]</InArgument>
      </Assign.Value>
    </Assign>
    <ui:ReadRange AddHeaders="True" DataTable="[dt_Sheet]" DisplayName="Read Range - Settings" SheetName="Settings" WorkbookPath="Data\Config.xlsx" />
    <ui:ForEachRow DataTable="[dt_Sheet]" DisplayName="For Each Row in Settings">
      <ui:ForEachRow.Body>
        <ActivityAction x:TypeArguments="sd:DataRow">
          <ActivityAction.Argument>
            <DelegateInArgument x:TypeArguments="sd:DataRow" Name="Row" />
          </ActivityAction.Argument>
          <If Condition="[Not String.IsNullOrWhiteSpace(Row(0).ToString.Trim)]" DisplayName="If Key Not Empty">
            <If.Then>
              <Assign DisplayName="Add Settings Key to Config">
                <Assign.To>
                  <OutArgument x:TypeArguments="x:Object">[out_Config(Row(0).ToString.Trim)]</OutArgument>
                </Assign.To>
                <Assign.Value>
                  <InArgument x:TypeArguments="x:Object">[If(Row(1) Is Nothing OrElse IsDBNull(Row(1)), "", Row(1).ToString)]</InArgument>
                </Assign.Value>
              </Assign>
            </If.Then>
            <If.Else>
              <Sequence DisplayName="" />
            </If.Else>
          </If>
        </ActivityAction>
      </ui:ForEachRow.Body>
    </ui:ForEachRow>
    <ui:ReadRange AddHeaders="True" DataTable="[dt_Sheet]" DisplayName="Read Range - Assets" SheetName="Assets" WorkbookPath="Data\Config.xlsx" />
    <ui:ForEachRow DataTable="[dt_Sheet]" DisplayName="For Each Row in Assets">
      <ui:ForEachRow.Body>
        <ActivityAction x:TypeArguments="sd:DataRow">
          <ActivityAction.Argument>
            <DelegateInArgument x:TypeArguments="sd:DataRow" Name="Row" />
          </ActivityAction.Argument>
          <If Condition="[Not String.IsNullOrWhiteSpace(Row(0).ToString.Trim)]" DisplayName="If Key Not Empty">
            <If.Then>
              <Assign DisplayName="Add Asset Key to Config">
                <Assign.To>
                  <OutArgument x:TypeArguments="x:Object">[out_Config(Row(0).ToString.Trim)]</OutArgument>
                </Assign.To>
                <Assign.Value>
                  <InArgument x:TypeArguments="x:Object">[If(Row(1) Is Nothing OrElse IsDBNull(Row(1)), "", Row(1).ToString)]</InArgument>
                </Assign.Value>
              </Assign>
            </If.Then>
            <If.Else>
              <Sequence DisplayName="" />
            </If.Else>
          </If>
        </ActivityAction>
      </ui:ForEachRow.Body>
    </ui:ForEachRow>
    <ui:InvokeWorkflowFile DisplayName="Invoke KillAllProcesses (EXCEL)" WorkflowFileName="Framework\KillAllProcesses.xaml">
      <ui:InvokeWorkflowFile.Arguments>
        <InArgument x:TypeArguments="x:String" x:Key="in_ProcessName">EXCEL</InArgument>
      </ui:InvokeWorkflowFile.Arguments>
    </ui:InvokeWorkflowFile>
    <Assign DisplayName="Initialize lstSapError">
      <Assign.To>
        <OutArgument x:TypeArguments="scg:List(x:String)">[lstSapError]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="scg:List(x:String)">[New List(Of String)()]</InArgument>
      </Assign.Value>
    </Assign>
    <ui:LogMessage DisplayName="Log [Init] Logging into SAP" Level="Info" Message="[&quot;[Init] Logging into SAP...&quot;]" />
    <ui:InvokeWorkflowFile DisplayName="Invoke LoginSAP" WorkflowFileName="Workflows\LoginSAP.xaml">
      <ui:InvokeWorkflowFile.Arguments>
        <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[out_Config]</InArgument>
        <InOutArgument x:TypeArguments="scg:List(x:String)" x:Key="io_lstError">[lstSapError]</InOutArgument>
        <OutArgument x:TypeArguments="ui:Window" x:Key="out_SAP">[out_SAP]</OutArgument>
        <OutArgument x:TypeArguments="x:String" x:Key="out_SapUsername">[strSapUsername]</OutArgument>
      </ui:InvokeWorkflowFile.Arguments>
    </ui:InvokeWorkflowFile>
    <ui:LogMessage DisplayName="Log [Init] SAP Login Done" Level="Info" Message="[&quot;[Init] SAP login OK. User=&quot; + strSapUsername]" />
    <ui:LogMessage DisplayName="Log [Init] Loading Customer Master CSV" Level="Info" Message="[&quot;[Init] Loading customer master: &quot; + out_Config(&quot;DKSHCustomerCsvPath&quot;).ToString]" />
    <ui:InvokeWorkflowFile sap2010:Annotation.AnnotationText="Excel Application Scope can open .csv files directly, so this reuses the already-verified ReadExcelToDatatable.xaml instead of a dedicated Read CSV activity (not present in this project's installed UiPath.System.Activities version)." DisplayName="Invoke ReadExcelToDatatable - DKSH_Customer.csv" WorkflowFileName="Common\ReadExcelToDatatable.xaml">
      <ui:InvokeWorkflowFile.Arguments>
        <InArgument x:TypeArguments="x:String" x:Key="in_SourceFile">[out_Config("DKSHCustomerCsvPath").ToString]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_SheetName">[Path.GetFileNameWithoutExtension(out_Config("DKSHCustomerCsvPath").ToString)]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_Range">[""]</InArgument>
        <InArgument x:TypeArguments="x:Boolean" x:Key="in_IsColumnName">[True]</InArgument>
        <OutArgument x:TypeArguments="sd:DataTable" x:Key="out_DtResult">[out_dtCustomerMaster]</OutArgument>
      </ui:InvokeWorkflowFile.Arguments>
    </ui:InvokeWorkflowFile>
    <ui:LogMessage DisplayName="Log [Init] Customer Master Loaded" Level="Info" Message="[&quot;[Init] Customer master loaded. Rows=&quot; + out_dtCustomerMaster.Rows.Count.ToString]" />
    <ui:LogMessage DisplayName="Log [Init] Loading Master Excel" Level="Info" Message="[&quot;[Init] Loading Client Access DB: &quot; + out_Config(&quot;MasterExcelPath&quot;).ToString]" />
    <ui:InvokeWorkflowFile DisplayName="Invoke ReadExcelToDatatable - Master Excel" WorkflowFileName="Common\ReadExcelToDatatable.xaml">
      <ui:InvokeWorkflowFile.Arguments>
        <InArgument x:TypeArguments="x:String" x:Key="in_SourceFile">[out_Config("MasterExcelPath").ToString]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_SheetName">ClientAccess</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_Range">[""]</InArgument>
        <InArgument x:TypeArguments="x:Boolean" x:Key="in_IsColumnName">[True]</InArgument>
        <OutArgument x:TypeArguments="sd:DataTable" x:Key="out_DtResult">[out_dtMasterExcel]</OutArgument>
      </ui:InvokeWorkflowFile.Arguments>
    </ui:InvokeWorkflowFile>
    <ui:LogMessage DisplayName="Log [Init] Config Loaded" Level="Info" Message="[&quot;[Init] Config loaded. Intake folder=&quot; + out_Config(&quot;OutlookFolder_Intake&quot;).ToString + &quot; | SAP user=&quot; + strSapUsername + &quot; | CustomerMasterRows=&quot; + out_dtCustomerMaster.Rows.Count.ToString + &quot; | ClientAccessRows=&quot; + out_dtMasterExcel.Rows.Count.ToString]" />
  </Sequence>"""

write_xaml(os.path.join(BASE, "InitAllApplications.xaml"), "InitAllApplications", members, body)

# ---------------------------------------------------------------------------
# CloseAllApplications.xaml
# ---------------------------------------------------------------------------
members = """    <x:Property Name="in_Config" Type="InArgument(scg:Dictionary(x:String, x:Object))" />
    <x:Property Name="in_SAP" Type="InArgument(ui:Window)" />"""

body = r"""  <Sequence DisplayName="CloseAllApplications">
    <Sequence.Variables>
      <Variable x:TypeArguments="scg:List(x:String)" Name="lstCloseError" />
    </Sequence.Variables>
    <ui:LogMessage DisplayName="Log [CloseAll] Start" Level="Info" Message="[&quot;[CloseAll] Closing all applications...&quot;]" />
    <Assign DisplayName="Initialize lstCloseError">
      <Assign.To>
        <OutArgument x:TypeArguments="scg:List(x:String)">[lstCloseError]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="scg:List(x:String)">[New List(Of String)()]</InArgument>
      </Assign.Value>
    </Assign>
    <TryCatch DisplayName="Try Close SAP">
      <TryCatch.Try>
        <ui:InvokeWorkflowFile DisplayName="Invoke CloseSAP" WorkflowFileName="Workflows\CloseSAP.xaml">
          <ui:InvokeWorkflowFile.Arguments>
            <InArgument x:TypeArguments="ui:Window" x:Key="in_SAP">[in_SAP]</InArgument>
            <InOutArgument x:TypeArguments="scg:List(x:String)" x:Key="io_lstError">[lstCloseError]</InOutArgument>
          </ui:InvokeWorkflowFile.Arguments>
        </ui:InvokeWorkflowFile>
      </TryCatch.Try>
      <TryCatch.Catches>
        <Catch x:TypeArguments="s:Exception">
          <ActivityAction x:TypeArguments="s:Exception">
            <ActivityAction.Argument>
              <DelegateInArgument x:TypeArguments="s:Exception" Name="ex" />
            </ActivityAction.Argument>
            <ui:LogMessage DisplayName="Log - SAP close skipped (ignored)" Level="Trace" Message="[&quot;[CloseAll] SAP close skipped: &quot; + ex.Message]" />
          </ActivityAction>
        </Catch>
      </TryCatch.Catches>
    </TryCatch>
    <TryCatch DisplayName="Try Kill EXCEL">
      <TryCatch.Try>
        <ui:KillProcess ContinueOnError="True" DisplayName="Kill Process - EXCEL" ProcessName="EXCEL" />
      </TryCatch.Try>
      <TryCatch.Catches>
        <Catch x:TypeArguments="s:Exception">
          <ActivityAction x:TypeArguments="s:Exception">
            <ActivityAction.Argument>
              <DelegateInArgument x:TypeArguments="s:Exception" Name="ex" />
            </ActivityAction.Argument>
            <ui:LogMessage DisplayName="Log - EXCEL not running (ignored)" Level="Trace" Message="[&quot;[CloseAll] EXCEL kill skipped: &quot; + ex.Message]" />
          </ActivityAction>
        </Catch>
      </TryCatch.Catches>
    </TryCatch>
    <ui:LogMessage DisplayName="Log [CloseAll] Done" Level="Info" Message="[&quot;[CloseAll] Applications closed. Outlook is left open (robot only reads/moves within the mailbox).&quot;]" />
  </Sequence>"""

write_xaml(os.path.join(BASE, "CloseAllApplications.xaml"), "CloseAllApplications", members, body)

print("Framework core files done.")
