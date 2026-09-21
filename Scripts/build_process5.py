import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from xaml_common import write_xaml

BASE = os.path.join(os.path.dirname(__file__), "..", "Process")

# ---------------------------------------------------------------------------
# MoveAndMarkEmail.xaml
# ---------------------------------------------------------------------------
members = """    <x:Property Name="in_MailItem" Type="InArgument(snm:MailMessage)" />
    <x:Property Name="in_TargetFolder" Type="InArgument(x:String)" />"""

body = r"""  <Sequence DisplayName="MoveAndMarkEmail">
    <ui:LogMessage DisplayName="Log [Move] Start" Level="Info" Message="[&quot;[Move] Moving to: &quot; + in_TargetFolder]" />
    <ui:MoveOutlookMessage sap2010:Annotation.AnnotationText="Confirmed via Studio Activities panel (real class is MoveOutlookMessage, not MoveOutlookMailMessage; the mail argument is MailMessage, not Mail). Account left default/null - set it explicitly if the robot's Outlook profile has more than one account configured. There is no separate mark-as-read step here - Framework\GetTransactionData.xaml already marks every fetched item as read (MarkAsRead=True) since every item ends up moved to Processed or Exception by the end of Process.xaml." Account="{x:Null}" DisplayName="Move Outlook Mail Message" MailFolder="[in_TargetFolder]" MailMessage="[in_MailItem]" />
    <ui:LogMessage DisplayName="Log [Move] Done" Level="Info" Message="[&quot;[Move] Done.&quot;]" />
  </Sequence>"""

write_xaml(os.path.join(BASE, "MoveAndMarkEmail.xaml"), "MoveAndMarkEmail", members, body)

# ---------------------------------------------------------------------------
# SendSuccessReply.xaml  (Section 6.1)
# ---------------------------------------------------------------------------
members = """    <x:Property Name="in_Config" Type="InArgument(scg:Dictionary(x:String, x:Object))" />
    <x:Property Name="in_MailItem" Type="InArgument(snm:MailMessage)" />
    <x:Property Name="in_SenderEmail" Type="InArgument(x:String)" />
    <x:Property Name="in_CustomerName" Type="InArgument(x:String)" />
    <x:Property Name="in_Account" Type="InArgument(x:String)" />
    <x:Property Name="in_GeneratedOn" Type="InArgument(x:String)" />
    <x:Property Name="in_TotalAllProducts" Type="InArgument(x:String)" />
    <x:Property Name="in_TotalYourBrand" Type="InArgument(x:String)" />
    <x:Property Name="in_Report1FilePath" Type="InArgument(x:String)" />
    <x:Property Name="in_Report2FilePath" Type="InArgument(x:String)" />"""

body = r"""  <Sequence DisplayName="SendSuccessReply">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="strTo" />
      <Variable x:TypeArguments="x:String" Name="strBody" />
      <Variable x:TypeArguments="scg:List(x:String)" Name="listAttachments" />
    </Sequence.Variables>
    <ui:LogMessage DisplayName="Log [6.1 Success] Start" Level="Info" Message="[&quot;[6.1 Success] Sending success reply to &quot; + in_SenderEmail]" />
    <Assign DisplayName="Build strTo (requester + distribution list)">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[strTo]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">[in_SenderEmail + ";" + in_Config("Mail_Success_To_Extra").ToString]</InArgument>
      </Assign.Value>
    </Assign>
    <Assign DisplayName="Init listAttachments">
      <Assign.To>
        <OutArgument x:TypeArguments="scg:List(x:String)">[listAttachments]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="scg:List(x:String)">[New List(Of String) From {in_Report1FilePath, in_Report2FilePath}]</InArgument>
      </Assign.Value>
    </Assign>
    <Assign DisplayName="Build strBody (HTML table)">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[strBody]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">["&lt;html&gt;&lt;body style='font-family:Arial;font-size:13px;'&gt;" + "&lt;p&gt;Dear Customer,&lt;/p&gt;" + "&lt;p&gt;Please find your requested Outstanding Statement below and attached.&lt;/p&gt;" + "&lt;table style='border-collapse:collapse;font-family:Arial;font-size:13px;' border='1' cellpadding='8' cellspacing='0'&gt;" + "&lt;tr&gt;&lt;td style='background-color:#C00000;color:white;font-weight:bold;width:260px;'&gt;Customer&lt;/td&gt;&lt;td&gt;" + in_CustomerName + "&lt;/td&gt;&lt;/tr&gt;" + "&lt;tr&gt;&lt;td style='background-color:#C00000;color:white;font-weight:bold;'&gt;Account&lt;/td&gt;&lt;td&gt;" + in_Account + "&lt;/td&gt;&lt;/tr&gt;" + "&lt;tr&gt;&lt;td style='background-color:#C00000;color:white;font-weight:bold;'&gt;Generated on&lt;/td&gt;&lt;td&gt;" + in_GeneratedOn + "&lt;/td&gt;&lt;/tr&gt;" + "&lt;tr&gt;&lt;td style='background-color:#C00000;color:white;font-weight:bold;'&gt;Total Outstanding - All Products (Account Level)&lt;/td&gt;&lt;td&gt;THB " + in_TotalAllProducts + "&lt;/td&gt;&lt;/tr&gt;" + "&lt;tr&gt;&lt;td style='background-color:#C00000;color:white;font-weight:bold;'&gt;Total Outstanding - Your Registered Brand&lt;/td&gt;&lt;td&gt;THB " + in_TotalYourBrand + "&lt;/td&gt;&lt;/tr&gt;" + "&lt;/table&gt;" + "&lt;p&gt;Attached: &lt;br/&gt;- &quot; + Path.GetFileName(in_Report1FilePath) + &quot;&lt;br/&gt;- &quot; + Path.GetFileName(in_Report2FilePath) + &quot;&lt;/p&gt;" + "&lt;p&gt;Best regards,&lt;br/&gt;DKSH Collection RPA Bot&lt;/p&gt;" + "&lt;/body&gt;&lt;/html&gt;"]</InArgument>
      </Assign.Value>
    </Assign>
    <ui:SendOutlookMail Account="[in_Config(&quot;MailAccount&quot;).ToString]" AttachmentsCollection="[listAttachments.ToArray()]" Body="[strBody]" Cc="[in_Config(&quot;Mail_Success_CC&quot;).ToString]" DisplayName="Send Outlook Mail - Success Reply" IsBodyHtml="True" Subject="[&quot;RE: &quot; + in_MailItem.Subject]" To="[strTo]">
      <ui:SendOutlookMail.Files>
        <scg:List x:TypeArguments="InArgument(x:String)" Capacity="0" />
      </ui:SendOutlookMail.Files>
    </ui:SendOutlookMail>
    <ui:LogMessage DisplayName="Log [6.1 Success] Done" Level="Info" Message="[&quot;[6.1 Success] Reply sent to &quot; + strTo]" />
  </Sequence>"""

write_xaml(os.path.join(BASE, "SendSuccessReply.xaml"), "SendSuccessReply", members, body)

print("Process part 5 done.")
