import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from xaml_common import write_xaml

BASE = os.path.join(os.path.dirname(__file__), "..", "Framework")

# ---------------------------------------------------------------------------
# SendAlertEmail.xaml  -- System Exception email only (build brief Section 6.3).
# Per-transaction Success/Exception replies live in Process\SendSuccessReply.xaml
# and Process\SendExceptionReply.xaml since their recipients/attachments differ
# per specific validation failure reason.
# ---------------------------------------------------------------------------
members = """    <x:Property Name="in_Config" Type="InArgument(scg:Dictionary(x:String, x:Object))" />
    <x:Property Name="in_TransactionID" Type="InArgument(x:String)" />
    <x:Property Name="in_SenderEmail" Type="InArgument(x:String)" />
    <x:Property Name="in_CustomerID" Type="InArgument(x:String)" />
    <x:Property Name="in_ExceptionType" Type="InArgument(x:String)" />
    <x:Property Name="in_ExceptionMessage" Type="InArgument(x:String)" />
    <x:Property Name="in_ScreenshotPath" Type="InArgument(x:String)" />"""

body = r"""  <Sequence DisplayName="SendAlertEmail (System Exception)">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="strBody" />
      <Variable x:TypeArguments="scg:List(x:String)" Name="listAttachments" />
    </Sequence.Variables>
    <ui:LogMessage DisplayName="Log [Email] Start" Level="Info" Message="[&quot;[Email] SystemException alert | Transaction #&quot; + in_TransactionID]" />
    <TryCatch DisplayName="TryCatch Send Email">
      <TryCatch.Try>
        <Sequence DisplayName="Build and Send">
          <Assign DisplayName="Init listAttachments">
            <Assign.To>
              <OutArgument x:TypeArguments="scg:List(x:String)">[listAttachments]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="scg:List(x:String)">[New List(Of String)()]</InArgument>
            </Assign.Value>
          </Assign>
          <If Condition="[Not String.IsNullOrEmpty(in_ScreenshotPath) AndAlso File.Exists(in_ScreenshotPath)]" DisplayName="If Screenshot Exists">
            <If.Then>
              <InvokeMethod DisplayName="Add Screenshot" MethodName="Add">
                <InvokeMethod.TargetObject>
                  <InArgument x:TypeArguments="scg:List(x:String)">[listAttachments]</InArgument>
                </InvokeMethod.TargetObject>
                <InArgument x:TypeArguments="x:String">[in_ScreenshotPath]</InArgument>
              </InvokeMethod>
            </If.Then>
            <If.Else>
              <Sequence DisplayName="" />
            </If.Else>
          </If>
          <Assign DisplayName="Build strBody">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[strBody]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">["&lt;html&gt;&lt;body style='font-family:Arial;font-size:13px;'&gt;" + "&lt;p&gt;A transaction in Collection_OutstandingStatement_Automation failed after exhausting all retries and requires manual attention.&lt;/p&gt;" + "&lt;table style='border-collapse:collapse;font-family:Arial;font-size:13px;' border='1' cellpadding='6' cellspacing='0'&gt;" + "&lt;tr&gt;&lt;td style='background-color:#C00000;color:white;font-weight:bold;'&gt;Transaction #&lt;/td&gt;&lt;td&gt;" + in_TransactionID + "&lt;/td&gt;&lt;/tr&gt;" + "&lt;tr&gt;&lt;td style='background-color:#C00000;color:white;font-weight:bold;'&gt;Sender&lt;/td&gt;&lt;td&gt;" + in_SenderEmail + "&lt;/td&gt;&lt;/tr&gt;" + "&lt;tr&gt;&lt;td style='background-color:#C00000;color:white;font-weight:bold;'&gt;Customer ID&lt;/td&gt;&lt;td&gt;" + If(String.IsNullOrEmpty(in_CustomerID), "(not yet extracted)", in_CustomerID) + "&lt;/td&gt;&lt;/tr&gt;" + "&lt;tr&gt;&lt;td style='background-color:#C00000;color:white;font-weight:bold;'&gt;Exception Type&lt;/td&gt;&lt;td&gt;" + in_ExceptionType + "&lt;/td&gt;&lt;/tr&gt;" + "&lt;tr&gt;&lt;td style='background-color:#C00000;color:white;font-weight:bold;'&gt;Timestamp&lt;/td&gt;&lt;td&gt;" + DateTime.Now.ToString("dd/MM/yyyy HH:mm:ss") + "&lt;/td&gt;&lt;/tr&gt;" + "&lt;tr&gt;&lt;td style='background-color:#C00000;color:white;font-weight:bold;'&gt;Message&lt;/td&gt;&lt;td&gt;" + in_ExceptionMessage + "&lt;/td&gt;&lt;/tr&gt;" + "&lt;/table&gt;" + "&lt;p&gt;This email was sent only to the RPA administrator per Section 6.3 of the build brief - the requester and Collection team are not notified of technical failures.&lt;/p&gt;" + "&lt;/body&gt;&lt;/html&gt;"]</InArgument>
            </Assign.Value>
          </Assign>
          <ui:SendOutlookMail Account="[in_Config(&quot;MailAccount&quot;).ToString]" AttachmentsCollection="[listAttachments.ToArray()]" Body="[strBody]" DisplayName="Send Outlook Mail - System Exception" IsBodyHtml="True" Subject="[&quot;[DKSH RPA][System Exception] Collection_OutstandingStatement_Automation - Transaction #&quot; + in_TransactionID]" To="[in_Config(&quot;RPAAdminEmail&quot;).ToString]">
            <ui:SendOutlookMail.Files>
              <scg:List x:TypeArguments="InArgument(x:String)" Capacity="0" />
            </ui:SendOutlookMail.Files>
          </ui:SendOutlookMail>
        </Sequence>
      </TryCatch.Try>
      <TryCatch.Catches>
        <Catch x:TypeArguments="s:Exception">
          <ActivityAction x:TypeArguments="s:Exception">
            <ActivityAction.Argument>
              <DelegateInArgument x:TypeArguments="s:Exception" Name="ex" />
            </ActivityAction.Argument>
            <ui:LogMessage DisplayName="Log [Email] Failed" Level="Error" Message="[&quot;[Email] Failed to send SystemException alert: &quot; + ex.Message]" />
          </ActivityAction>
        </Catch>
      </TryCatch.Catches>
    </TryCatch>
    <ui:LogMessage DisplayName="Log [Email] Done" Level="Info" Message="[&quot;[Email] SystemException alert done for Transaction #&quot; + in_TransactionID]" />
  </Sequence>"""

write_xaml(os.path.join(BASE, "SendAlertEmail.xaml"), "SendAlertEmail", members, body)

# ---------------------------------------------------------------------------
# EndProcess.xaml
# ---------------------------------------------------------------------------
members = """    <x:Property Name="in_intSuccessCount" Type="InArgument(x:Int32)" />
    <x:Property Name="in_intBusinessExceptionCount" Type="InArgument(x:Int32)" />
    <x:Property Name="in_intSystemExceptionCount" Type="InArgument(x:Int32)" />"""

body = r"""  <Sequence DisplayName="EndProcess">
    <ui:LogMessage DisplayName="Log [EndProcess] Completed" Level="Info" Message="[&quot;[EndProcess] Completed. Success=&quot; + in_intSuccessCount.ToString + &quot; Failed=&quot; + in_intBusinessExceptionCount.ToString + &quot; Skipped=&quot; + in_intSystemExceptionCount.ToString]" />
  </Sequence>"""

write_xaml(os.path.join(BASE, "EndProcess.xaml"), "EndProcess", members, body)

print("Framework part 3 done.")
