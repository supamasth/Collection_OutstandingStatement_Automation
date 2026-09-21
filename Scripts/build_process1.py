import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from xaml_common import write_xaml

BASE = os.path.join(os.path.dirname(__file__), "..", "Process")

# ---------------------------------------------------------------------------
# ValidateCustomerIDFormat.xaml  (Section 3.1)
# ---------------------------------------------------------------------------
members = """    <x:Property Name="in_Config" Type="InArgument(scg:Dictionary(x:String, x:Object))" />
    <x:Property Name="in_Subject" Type="InArgument(x:String)" />
    <x:Property Name="in_Body" Type="InArgument(x:String)" />
    <x:Property Name="out_CustomerID" Type="OutArgument(x:String)" />
    <x:Property Name="out_IsValid" Type="OutArgument(x:Boolean)" />"""

body = r"""  <Sequence DisplayName="ValidateCustomerIDFormat">
    <Sequence.Variables>
      <Variable x:TypeArguments="srx:Match" Name="mSubject" />
      <Variable x:TypeArguments="srx:Match" Name="mBody" />
    </Sequence.Variables>
    <ui:LogMessage DisplayName="Log [3.1] Start" Level="Info" Message="[&quot;[3.1 CustomerIDFormat] Checking subject/body for a 9-digit Customer ID starting with 17...&quot;]" />
    <Assign DisplayName="Match Subject">
      <Assign.To>
        <OutArgument x:TypeArguments="srx:Match">[mSubject]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="srx:Match">[Regex.Match(If(in_Subject, ""), in_Config("CustomerIDPattern").ToString)]</InArgument>
      </Assign.Value>
    </Assign>
    <If Condition="[mSubject.Success]" DisplayName="If Found in Subject">
      <If.Then>
        <Sequence DisplayName="Use Subject Match">
          <Assign DisplayName="Set out_CustomerID (Subject)">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[out_CustomerID]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">[mSubject.Value]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_IsValid = True">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_IsValid]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">[True]</InArgument>
            </Assign.Value>
          </Assign>
        </Sequence>
      </If.Then>
      <If.Else>
        <Sequence DisplayName="Fallback to Body">
          <Assign DisplayName="Match Body">
            <Assign.To>
              <OutArgument x:TypeArguments="srx:Match">[mBody]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="srx:Match">[Regex.Match(If(in_Body, ""), in_Config("CustomerIDPattern").ToString)]</InArgument>
            </Assign.Value>
          </Assign>
          <If Condition="[mBody.Success]" DisplayName="If Found in Body">
            <If.Then>
              <Sequence DisplayName="Use Body Match">
                <Assign DisplayName="Set out_CustomerID (Body)">
                  <Assign.To>
                    <OutArgument x:TypeArguments="x:String">[out_CustomerID]</OutArgument>
                  </Assign.To>
                  <Assign.Value>
                    <InArgument x:TypeArguments="x:String">[mBody.Value]</InArgument>
                  </Assign.Value>
                </Assign>
                <Assign DisplayName="Set out_IsValid = True">
                  <Assign.To>
                    <OutArgument x:TypeArguments="x:Boolean">[out_IsValid]</OutArgument>
                  </Assign.To>
                  <Assign.Value>
                    <InArgument x:TypeArguments="x:Boolean">[True]</InArgument>
                  </Assign.Value>
                </Assign>
              </Sequence>
            </If.Then>
            <If.Else>
              <Sequence DisplayName="Not Found">
                <Assign DisplayName="Set out_CustomerID = Empty">
                  <Assign.To>
                    <OutArgument x:TypeArguments="x:String">[out_CustomerID]</OutArgument>
                  </Assign.To>
                  <Assign.Value>
                    <InArgument x:TypeArguments="x:String">[""]</InArgument>
                  </Assign.Value>
                </Assign>
                <Assign DisplayName="Set out_IsValid = False">
                  <Assign.To>
                    <OutArgument x:TypeArguments="x:Boolean">[out_IsValid]</OutArgument>
                  </Assign.To>
                  <Assign.Value>
                    <InArgument x:TypeArguments="x:Boolean">[False]</InArgument>
                  </Assign.Value>
                </Assign>
              </Sequence>
            </If.Else>
          </If>
        </Sequence>
      </If.Else>
    </If>
    <ui:LogMessage DisplayName="Log [3.1] Result" Level="Info" Message="[&quot;[3.1 CustomerIDFormat] IsValid=&quot; + out_IsValid.ToString + &quot; CustomerID=&quot; + out_CustomerID]" />
  </Sequence>"""

write_xaml(os.path.join(BASE, "ValidateCustomerIDFormat.xaml"), "ValidateCustomerIDFormat", members, body)

print("Process part 1 done.")
