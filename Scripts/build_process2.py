import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from xaml_common import write_xaml

BASE = os.path.join(os.path.dirname(__file__), "..", "Process")

# ---------------------------------------------------------------------------
# LookupCustomerMaster.xaml  (Section 3.2)
# ---------------------------------------------------------------------------
members = """    <x:Property Name="in_Config" Type="InArgument(scg:Dictionary(x:String, x:Object))" />
    <x:Property Name="in_dtCustomerMaster" Type="InArgument(sd:DataTable)" />
    <x:Property Name="in_CustomerID" Type="InArgument(x:String)" />
    <x:Property Name="out_Found" Type="OutArgument(x:Boolean)" />
    <x:Property Name="out_Active" Type="OutArgument(x:Boolean)" />
    <x:Property Name="out_Excluded" Type="OutArgument(x:Boolean)" />"""

body = r"""  <Sequence DisplayName="LookupCustomerMaster">
    <Sequence.Variables>
      <Variable x:TypeArguments="scg:List(sd:DataRow)" Name="matchingRows" />
      <Variable x:TypeArguments="scg:IEnumerable(x:String)" Name="arrExclusion" />
    </Sequence.Variables>
    <ui:LogMessage DisplayName="Log [3.2] Start" Level="Info" Message="[&quot;[3.2 CustomerMaster] Looking up Customer ID &quot; + in_CustomerID + &quot; in DKSH_Customer.csv (&quot; + in_dtCustomerMaster.Rows.Count.ToString + &quot; rows)...&quot;]" />
    <Assign DisplayName="Find All Matching Rows (CustCode not unique)">
      <Assign.To>
        <OutArgument x:TypeArguments="scg:List(sd:DataRow)">[matchingRows]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="scg:List(sd:DataRow)">[in_dtCustomerMaster.AsEnumerable().Where(Function(r) r("CustCode").ToString.Trim = in_CustomerID).ToList()]</InArgument>
      </Assign.Value>
    </Assign>
    <If Condition="[matchingRows.Count &gt; 0]" DisplayName="If Any Row Found">
      <If.Then>
        <Sequence DisplayName="Evaluate Status and Exclusion Across All Matching Rows">
          <Assign DisplayName="Set out_Found = True">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_Found]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">[True]</InArgument>
            </Assign.Value>
          </Assign>
          <!-- Disabled 2026-09-16: requirement retracted - meaning of Status='X' in
               DKSH_Customer.csv has not been confirmed with CM/business. A Status='X'
               customer currently passes through to the next check (exclusion list) as
               if active. Re-enable once the correct definition is confirmed.
          <Assign DisplayName="Set out_Active (False if ANY row has Status = X)">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_Active]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">[Not matchingRows.Any(Function(r) r("Status").ToString.Trim.ToUpper = "X")]</InArgument>
            </Assign.Value>
          </Assign>
          -->
          <Assign DisplayName="Set out_Active = True (Status=X check temporarily disabled, see comment above)">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_Active]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">[True]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Split Exclusion List from Config">
            <Assign.To>
              <OutArgument x:TypeArguments="scg:IEnumerable(x:String)">[arrExclusion]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="scg:IEnumerable(x:String)">[in_Config("CustGroupExclusionList").ToString.Split("|"c).Select(Function(x) x.Trim.ToUpper)]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_Excluded (True if ANY row's CustGroup is excluded)">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_Excluded]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">[matchingRows.Any(Function(r) arrExclusion.Contains(r("CustGroup_Description").ToString.Trim.ToUpper))]</InArgument>
            </Assign.Value>
          </Assign>
        </Sequence>
      </If.Then>
      <If.Else>
        <Sequence DisplayName="Not Found">
          <Assign DisplayName="Set out_Found = False">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_Found]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">[False]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_Active = False">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_Active]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">[False]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_Excluded = False">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_Excluded]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">[False]</InArgument>
            </Assign.Value>
          </Assign>
        </Sequence>
      </If.Else>
    </If>
    <ui:LogMessage DisplayName="Log [3.2] Result" Level="Info" Message="[&quot;[3.2 CustomerMaster] Found=&quot; + out_Found.ToString + &quot; Active=&quot; + out_Active.ToString + &quot; Excluded=&quot; + out_Excluded.ToString + &quot; MatchingRows=&quot; + matchingRows.Count.ToString]" />
  </Sequence>"""

write_xaml(os.path.join(BASE, "LookupCustomerMaster.xaml"), "LookupCustomerMaster", members, body)

# ---------------------------------------------------------------------------
# LookupSenderAuthorization.xaml  (Section 3.3)
# ---------------------------------------------------------------------------
members = """    <x:Property Name="in_dtMasterExcel" Type="InArgument(sd:DataTable)" />
    <x:Property Name="in_SenderEmail" Type="InArgument(x:String)" />
    <x:Property Name="out_Authorized" Type="OutArgument(x:Boolean)" />
    <x:Property Name="out_MatGroup" Type="OutArgument(x:String)" />
    <x:Property Name="out_MatGroup4" Type="OutArgument(x:String)" />"""

body = r"""  <Sequence DisplayName="LookupSenderAuthorization">
    <Sequence.Variables>
      <Variable x:TypeArguments="scg:List(sd:DataRow)" Name="matchingRows" />
    </Sequence.Variables>
    <ui:LogMessage DisplayName="Log [3.3] Start" Level="Info" Message="[&quot;[3.3 SenderAuth] Looking up sender &quot; + in_SenderEmail + &quot; in Client Access DB...&quot;]" />
    <Assign DisplayName="Find Active Matching Rows for Sender">
      <Assign.To>
        <OutArgument x:TypeArguments="scg:List(sd:DataRow)">[matchingRows]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="scg:List(sd:DataRow)">[in_dtMasterExcel.AsEnumerable().Where(Function(r) r("Client Email").ToString.Trim.ToUpper = in_SenderEmail.Trim.ToUpper AndAlso r("Status").ToString.Trim.ToUpper = "ACTIVE").ToList()]</InArgument>
      </Assign.Value>
    </Assign>
    <If Condition="[matchingRows.Count &gt; 0]" DisplayName="If Authorized Row Found">
      <If.Then>
        <Sequence DisplayName="Use First Matching Row">
          <If Condition="[matchingRows.Count &gt; 1]" DisplayName="If Multiple Brands Registered - Warn">
            <If.Then>
              <ui:LogMessage DisplayName="Log [3.3] Multiple Brands Warning" Level="Warn" Message="[&quot;[3.3 SenderAuth] Sender &quot; + in_SenderEmail + &quot; has &quot; + matchingRows.Count.ToString + &quot; active brand registrations. Build brief Section 3.3 does not specify disambiguation - using the first row (MatGroup=&quot; + matchingRows(0)(&quot;MatGroup&quot;).ToString.Trim + &quot;, MatGroup4=&quot; + matchingRows(0)(&quot;MatGroup4&quot;).ToString.Trim + &quot;). Confirm with Collection team whether this needs a tie-break rule (e.g. brand named in the email body).&quot;]" />
            </If.Then>
            <If.Else>
              <Sequence DisplayName="" />
            </If.Else>
          </If>
          <Assign DisplayName="Set out_Authorized = True">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_Authorized]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">[True]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_MatGroup">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[out_MatGroup]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">[matchingRows(0)("MatGroup").ToString.Trim]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_MatGroup4">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[out_MatGroup4]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">[matchingRows(0)("MatGroup4").ToString.Trim]</InArgument>
            </Assign.Value>
          </Assign>
        </Sequence>
      </If.Then>
      <If.Else>
        <Sequence DisplayName="Not Authorized">
          <Assign DisplayName="Set out_Authorized = False">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[out_Authorized]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">[False]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_MatGroup = Empty">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[out_MatGroup]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">[""]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set out_MatGroup4 = Empty">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[out_MatGroup4]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">[""]</InArgument>
            </Assign.Value>
          </Assign>
        </Sequence>
      </If.Else>
    </If>
    <ui:LogMessage DisplayName="Log [3.3] Result" Level="Info" Message="[&quot;[3.3 SenderAuth] Authorized=&quot; + out_Authorized.ToString + &quot; MatGroup=&quot; + out_MatGroup + &quot; MatGroup4=&quot; + out_MatGroup4]" />
  </Sequence>"""

write_xaml(os.path.join(BASE, "LookupSenderAuthorization.xaml"), "LookupSenderAuthorization", members, body)

print("Process part 2 done.")
