import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from xaml_common import write_xaml

BASE = os.path.join(os.path.dirname(__file__), "..", "Framework")

# ---------------------------------------------------------------------------
# GetTransactionData.xaml
# ---------------------------------------------------------------------------
members = """    <x:Property Name="in_Config" Type="InArgument(scg:Dictionary(x:String, x:Object))" />
    <x:Property Name="io_listMails" Type="InOutArgument(scg:List(snm:MailMessage))" />
    <x:Property Name="io_intTransactionNumber" Type="InOutArgument(x:Int32)" />
    <x:Property Name="out_MailItem" Type="OutArgument(snm:MailMessage)" />
    <x:Property Name="out_TransactionID" Type="OutArgument(x:String)" />
    <x:Property Name="out_NoItemsLeft" Type="OutArgument(x:Boolean)" />"""

body = r"""  <Sequence DisplayName="GetTransactionData">
    <If Condition="[io_intTransactionNumber = 0]" DisplayName="If First Call - Fetch Unread Mails">
      <If.Then>
        <Sequence DisplayName="Fetch Unread Mails">
          <ui:LogMessage DisplayName="Log [GetTxn] Fetching Unread Mails" Level="Info" Message="[&quot;[GetTxn] Fetching unread items from folder: &quot; + in_Config(&quot;OutlookFolder_Intake&quot;).ToString]" />
          <ui:GetOutlookMailMessages sap2010:Annotation.AnnotationText="ASSUMPTION - verify property names (Account, MailFolder, Top, OnlyUnreadMessages, MarkAsRead, Filter, Messages) against the installed UiPath.Mail.Activities version in Studio's Properties panel before running; drag a fresh copy of the activity and compare if any property fails to bind. MarkAsRead=True here (rather than a separate Mark-as-read activity, which does not exist in this package) is safe because every fetched item is moved out of the intake folder to either Processed or Exception by the end of Process.xaml - none are left read-but-unhandled." DisplayName="Get Outlook Mail Messages - OutstandingRequest (Unread)" MailFolder="[in_Config(&quot;OutlookFolder_Intake&quot;).ToString]" OnlyUnreadMessages="True" MarkAsRead="True" Top="200" Messages="[io_listMails]" />
          <ui:LogMessage DisplayName="Log [GetTxn] Mail Count" Level="Info" Message="[&quot;[GetTxn] Found &quot; + io_listMails.Count.ToString + &quot; unread item(s)&quot;]" />
        </Sequence>
      </If.Then>
      <If.Else>
        <Sequence DisplayName="" />
      </If.Else>
    </If>
    <If Condition="[io_intTransactionNumber &lt; io_listMails.Count]" DisplayName="If Items Remain">
      <If.Then>
        <Sequence DisplayName="Return Next Transaction">
          <Assign DisplayName="Set out_MailItem">
            <Assign.To>
              <OutArgument x:TypeArguments="snm:MailMessage">[out_MailItem]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="snm:MailMessage">[io_listMails(io_intTransactionNumber)]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_TransactionID">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[out_TransactionID]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">[(io_intTransactionNumber + 1).ToString]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_NoItemsLeft = False">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_NoItemsLeft]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">[False]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Increment io_intTransactionNumber">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Int32">[io_intTransactionNumber]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Int32">[io_intTransactionNumber + 1]</InArgument>
            </Assign.Value>
          </Assign>
          <ui:LogMessage DisplayName="Log [GetTxn] Transaction Retrieved" Level="Info" Message="[&quot;[GetTxn] Transaction #&quot; + out_TransactionID + &quot; retrieved. Subject=&quot; + out_MailItem.Subject]" />
        </Sequence>
      </If.Then>
      <If.Else>
        <Sequence DisplayName="No More Items">
          <Assign DisplayName="Set out_NoItemsLeft = True">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_NoItemsLeft]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">[True]</InArgument>
            </Assign.Value>
          </Assign>
          <ui:LogMessage DisplayName="Log [GetTxn] No More Items" Level="Info" Message="[&quot;[GetTxn] No more items. Total processed: &quot; + io_intTransactionNumber.ToString]" />
        </Sequence>
      </If.Else>
    </If>
  </Sequence>"""

write_xaml(os.path.join(BASE, "GetTransactionData.xaml"), "GetTransactionData", members, body)

# ---------------------------------------------------------------------------
# SetTransactionStatus.xaml
# ---------------------------------------------------------------------------
members = """    <x:Property Name="in_TransactionID" Type="InArgument(x:String)" />
    <x:Property Name="in_Status" Type="InArgument(x:String)" />
    <x:Property Name="io_intSuccessCount" Type="InOutArgument(x:Int32)" />
    <x:Property Name="io_intBusinessExceptionCount" Type="InOutArgument(x:Int32)" />
    <x:Property Name="io_intSystemExceptionCount" Type="InOutArgument(x:Int32)" />"""

body = r"""  <Sequence DisplayName="SetTransactionStatus">
    <Switch x:TypeArguments="x:String" DisplayName="Switch on Status" Expression="[in_Status]">
      <Sequence x:Key="Successful" DisplayName="Successful">
        <Assign DisplayName="Increment Success Count">
          <Assign.To>
            <OutArgument x:TypeArguments="x:Int32">[io_intSuccessCount]</OutArgument>
          </Assign.To>
          <Assign.Value>
            <InArgument x:TypeArguments="x:Int32">[io_intSuccessCount + 1]</InArgument>
          </Assign.Value>
        </Assign>
        <ui:LogMessage DisplayName="Log [SetStatus] Successful" Level="Info" Message="[&quot;[SetStatus] Transaction #&quot; + in_TransactionID + &quot; = Successful&quot;]" />
      </Sequence>
      <Sequence x:Key="BusinessException" DisplayName="BusinessException">
        <Assign DisplayName="Increment BusinessException Count">
          <Assign.To>
            <OutArgument x:TypeArguments="x:Int32">[io_intBusinessExceptionCount]</OutArgument>
          </Assign.To>
          <Assign.Value>
            <InArgument x:TypeArguments="x:Int32">[io_intBusinessExceptionCount + 1]</InArgument>
          </Assign.Value>
        </Assign>
        <ui:LogMessage DisplayName="Log [SetStatus] BusinessException" Level="Warn" Message="[&quot;[SetStatus] Transaction #&quot; + in_TransactionID + &quot; = BusinessException (no retry)&quot;]" />
      </Sequence>
      <Sequence x:Key="SystemException" DisplayName="SystemException">
        <Assign DisplayName="Increment SystemException Count">
          <Assign.To>
            <OutArgument x:TypeArguments="x:Int32">[io_intSystemExceptionCount]</OutArgument>
          </Assign.To>
          <Assign.Value>
            <InArgument x:TypeArguments="x:Int32">[io_intSystemExceptionCount + 1]</InArgument>
          </Assign.Value>
        </Assign>
        <ui:LogMessage DisplayName="Log [SetStatus] SystemException" Level="Error" Message="[&quot;[SetStatus] Transaction #&quot; + in_TransactionID + &quot; = SystemException (retries exhausted)&quot;]" />
      </Sequence>
    </Switch>
  </Sequence>"""

write_xaml(os.path.join(BASE, "SetTransactionStatus.xaml"), "SetTransactionStatus", members, body)

print("Framework part 2 done.")
