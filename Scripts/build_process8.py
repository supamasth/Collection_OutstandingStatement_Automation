import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from xaml_common import write_xaml

BASE = os.path.join(os.path.dirname(__file__), "..", "Process")

# ---------------------------------------------------------------------------
# ForwardToCollectionTeam.xaml - new gate ahead of Section 3.1: replies/forwards
# to the robot's own emails are forwarded untouched to the Collection team
# instead of being run through validation or auto-replied to.
# ---------------------------------------------------------------------------
members = """    <x:Property Name="in_Config" Type="InArgument(scg:Dictionary(x:String, x:Object))" />
    <x:Property Name="in_MailItem" Type="InArgument(snm:MailMessage)" />
    <x:Property Name="in_SenderEmail" Type="InArgument(x:String)" />"""

body = r"""  <Sequence DisplayName="ForwardToCollectionTeam">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="strBody" />
    </Sequence.Variables>
    <ui:LogMessage DisplayName="Log [Forward] Start" Level="Info" Message="[&quot;[Forward] Reply/forward to a robot email detected (Subject does not start with '[Outstanding]') - forwarding to Collection team instead of processing as a new request. Sender=&quot; + in_SenderEmail + &quot; | Subject=&quot; + in_MailItem.Subject]" />
    <Assign DisplayName="Build strBody">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[strBody]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">["&lt;html&gt;&lt;body style='font-family:Arial;font-size:13px;'&gt;" + "&lt;p style='padding:10px;background-color:#f5f5f5;border-left:4px solid #C00000;'&gt;Forwarded automatically - reply/forward to an automated Outstanding Statement email, not a new request. Please review and respond directly if needed.&lt;/p&gt;" + "&lt;p&gt;&lt;b&gt;From:&lt;/b&gt; " + in_SenderEmail + "&lt;br/&gt;&lt;b&gt;Original Subject:&lt;/b&gt; " + in_MailItem.Subject + "&lt;/p&gt;" + "&lt;hr/&gt;" + "&lt;div&gt;" + in_MailItem.Body + "&lt;/div&gt;" + "&lt;/body&gt;&lt;/html&gt;"]</InArgument>
      </Assign.Value>
    </Assign>
    <ui:SendOutlookMail Account="[in_Config(&quot;MailAccount&quot;).ToString]" Body="[strBody]" DisplayName="Send Outlook Mail - Forward to Collection Team" IsBodyHtml="True" Subject="[&quot;FW: &quot; + in_MailItem.Subject]" To="[in_Config(&quot;Mail_Exception_CC&quot;).ToString]">
      <ui:SendOutlookMail.Files>
        <scg:List x:TypeArguments="InArgument(x:String)" Capacity="0" />
      </ui:SendOutlookMail.Files>
    </ui:SendOutlookMail>
    <ui:LogMessage DisplayName="Log [Forward] Done" Level="Info" Message="[&quot;[Forward] Forwarded to &quot; + in_Config(&quot;Mail_Exception_CC&quot;).ToString]" />
  </Sequence>"""

write_xaml(os.path.join(BASE, "ForwardToCollectionTeam.xaml"), "ForwardToCollectionTeam", members, body)

print("Process part 8 (ForwardToCollectionTeam) done.")
