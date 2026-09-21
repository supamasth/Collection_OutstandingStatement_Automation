import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from xaml_common import write_xaml

BASE = os.path.join(os.path.dirname(__file__), "..", "Process")

# ---------------------------------------------------------------------------
# SendExceptionReply.xaml  (Section 6.2)
# in_Reason one of: InvalidFormat | NotFound | Inactive | Excluded | NotAuthorized
# ---------------------------------------------------------------------------
members = """    <x:Property Name="in_Config" Type="InArgument(scg:Dictionary(x:String, x:Object))" />
    <x:Property Name="in_MailItem" Type="InArgument(snm:MailMessage)" />
    <x:Property Name="in_SenderEmail" Type="InArgument(x:String)" />
    <x:Property Name="in_Reason" Type="InArgument(x:String)" />
    <x:Property Name="in_CustomerID" Type="InArgument(x:String)" />"""

body = r"""  <Sequence DisplayName="SendExceptionReply">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="strReasonText" />
      <Variable x:TypeArguments="x:String" Name="strBody" />
    </Sequence.Variables>
    <ui:LogMessage DisplayName="Log [6.2 Exception] Start" Level="Info" Message="[&quot;[6.2 Exception] Reason=&quot; + in_Reason + &quot; | Sender=&quot; + in_SenderEmail + &quot; | CustomerID=&quot; + in_CustomerID]" />
    <Switch x:TypeArguments="x:String" DisplayName="Switch on Reason" Expression="[in_Reason]">
      <Assign x:Key="InvalidFormat" DisplayName="InvalidFormat">
        <Assign.To>
          <OutArgument x:TypeArguments="x:String">[strReasonText]</OutArgument>
        </Assign.To>
        <Assign.Value>
          <InArgument x:TypeArguments="x:String">["We could not find a valid Customer ID in your request. Please resubmit using the correct format: a 9-digit Customer ID starting with 17, included in the subject line or body of your email (see the Outstanding Statement Request template)."]</InArgument>
        </Assign.Value>
      </Assign>
      <Assign x:Key="NotFound" DisplayName="NotFound">
        <Assign.To>
          <OutArgument x:TypeArguments="x:String">[strReasonText]</OutArgument>
        </Assign.To>
        <Assign.Value>
          <InArgument x:TypeArguments="x:String">["Customer ID " + in_CustomerID + " was not found in DKSH's customer records. Please verify the Customer ID and resubmit your request, or contact the Collection team for assistance."]</InArgument>
        </Assign.Value>
      </Assign>
      <!-- Currently unreachable: Process.xaml's Status='X' check (Section 3.2) that used
           to route to this Inactive case is disabled - see the note above the disabled
           Assign in Process\LookupCustomerMaster.xaml. Kept here per instruction so the
           template is ready to go the moment that check is re-enabled. -->
      <Assign x:Key="Inactive" DisplayName="Inactive">
        <Assign.To>
          <OutArgument x:TypeArguments="x:String">[strReasonText]</OutArgument>
        </Assign.To>
        <Assign.Value>
          <InArgument x:TypeArguments="x:String">["Customer ID " + in_CustomerID + " is not active / has expired in DKSH. Please contact the Collection team for assistance with this account."]</InArgument>
        </Assign.Value>
      </Assign>
      <Assign x:Key="Excluded" DisplayName="Excluded">
        <Assign.To>
          <OutArgument x:TypeArguments="x:String">[strReasonText]</OutArgument>
        </Assign.To>
        <Assign.Value>
          <InArgument x:TypeArguments="x:String">["Customer ID " + in_CustomerID + " belongs to a customer group that is excluded from the automated Outstanding Statement process (e.g. educational institution, government/military/private hospital, inter-company, or third-party tender account). Please contact the Collection team directly for this request."]</InArgument>
        </Assign.Value>
      </Assign>
      <Assign x:Key="NotAuthorized" DisplayName="NotAuthorized">
        <Assign.To>
          <OutArgument x:TypeArguments="x:String">[strReasonText]</OutArgument>
        </Assign.To>
        <Assign.Value>
          <InArgument x:TypeArguments="x:String">["Your email address is not registered for automated access to Outstanding Statement requests. Please contact the Collection team to register access."]</InArgument>
        </Assign.Value>
      </Assign>
    </Switch>
    <Assign DisplayName="Build strBody">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[strBody]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">["&lt;html&gt;&lt;body style='font-family:Arial;font-size:13px;'&gt;" + "&lt;p&gt;Dear Customer,&lt;/p&gt;" + "&lt;p&gt;We are unable to process your Outstanding Statement request:&lt;/p&gt;" + "&lt;p style='padding:10px;background-color:#f5f5f5;border-left:4px solid #C00000;'&gt;" + strReasonText + "&lt;/p&gt;" + "&lt;p&gt;Best regards,&lt;br/&gt;DKSH Collection RPA Bot&lt;/p&gt;" + "&lt;/body&gt;&lt;/html&gt;"]</InArgument>
      </Assign.Value>
    </Assign>
    <ui:SendOutlookMail Account="[in_Config(&quot;MailAccount&quot;).ToString]" Body="[strBody]" Cc="[in_Config(&quot;Mail_Exception_CC&quot;).ToString]" DisplayName="Send Outlook Mail - Exception Reply" IsBodyHtml="True" Subject="[&quot;RE: &quot; + in_MailItem.Subject]" To="[in_SenderEmail]">
      <ui:SendOutlookMail.Files>
        <scg:List x:TypeArguments="InArgument(x:String)" Capacity="0" />
      </ui:SendOutlookMail.Files>
    </ui:SendOutlookMail>
    <ui:LogMessage DisplayName="Log [6.2 Exception] Done" Level="Info" Message="[&quot;[6.2 Exception] Reply sent to &quot; + in_SenderEmail + &quot; (CC &quot; + in_Config(&quot;Mail_Exception_CC&quot;).ToString + &quot;)&quot;]" />
  </Sequence>"""

write_xaml(os.path.join(BASE, "SendExceptionReply.xaml"), "SendExceptionReply", members, body)

print("Process part 6 done.")
