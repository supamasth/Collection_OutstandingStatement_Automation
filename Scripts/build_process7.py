import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from xaml_common import write_xaml

BASE = os.path.join(os.path.dirname(__file__), "..", "Process")

members = """    <x:Property Name="in_Config" Type="InArgument(scg:Dictionary(x:String, x:Object))" />
    <x:Property Name="in_SAP" Type="InArgument(ui:Window)" />
    <x:Property Name="in_dtCustomerMaster" Type="InArgument(sd:DataTable)" />
    <x:Property Name="in_dtMasterExcel" Type="InArgument(sd:DataTable)" />
    <x:Property Name="in_MailItem" Type="InArgument(snm:MailMessage)" />
    <x:Property Name="in_TransactionID" Type="InArgument(x:String)" />
    <x:Property Name="out_TransactionStatus" Type="OutArgument(x:String)" />"""

body = r"""  <Sequence DisplayName="Process">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="strSubject" />
      <Variable x:TypeArguments="x:String" Name="strBody" />
      <Variable x:TypeArguments="x:String" Name="strSenderEmail" />
      <Variable x:TypeArguments="x:String" Name="strCustomerID" />
      <Variable x:TypeArguments="x:Boolean" Name="blnIDValid" />
      <Variable x:TypeArguments="x:Boolean" Name="blnFound" />
      <Variable x:TypeArguments="x:Boolean" Name="blnActive" />
      <Variable x:TypeArguments="x:Boolean" Name="blnExcluded" />
      <Variable x:TypeArguments="x:Boolean" Name="blnAuthorized" />
      <Variable x:TypeArguments="x:String" Name="strMatGroup" />
      <Variable x:TypeArguments="x:String" Name="strMatGroup4" />
      <Variable x:TypeArguments="x:Boolean" Default="True" Name="blnContinue" />
      <Variable x:TypeArguments="x:String" Name="strTimestamp" />
      <Variable x:TypeArguments="x:String" Name="strOutputFolder" />
      <Variable x:TypeArguments="x:String" Name="strReport1Path" />
      <Variable x:TypeArguments="x:String" Name="strCustomerName" />
      <Variable x:TypeArguments="x:String" Name="strAccount" />
      <Variable x:TypeArguments="x:String" Name="strGeneratedOn" />
      <Variable x:TypeArguments="x:String" Name="strTotalAllProducts" />
      <Variable x:TypeArguments="x:String" Name="strBillDateLow" />
      <Variable x:TypeArguments="x:String" Name="strBillDateHigh" />
      <Variable x:TypeArguments="x:Boolean" Name="blnHasOutstandingItems" />
      <Variable x:TypeArguments="x:String" Name="strReport2Path" />
      <Variable x:TypeArguments="x:String" Name="strTotalYourBrand" />
    </Sequence.Variables>
    <ui:LogMessage DisplayName="Log [Process] Start" Level="Info" Message="[&quot;[Process] Start Transaction #&quot; + in_TransactionID + &quot; | Subject=&quot; + in_MailItem.Subject]" />
    <Assign DisplayName="Extract Subject/Body/Sender">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[strSubject]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">[If(in_MailItem.Subject, "")]</InArgument>
      </Assign.Value>
    </Assign>
    <Assign DisplayName="Extract Body">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[strBody]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">[If(in_MailItem.Body, "")]</InArgument>
      </Assign.Value>
    </Assign>
    <Assign DisplayName="Extract Sender Email">
      <Assign.To>
        <OutArgument x:TypeArguments="x:String">[strSenderEmail]</OutArgument>
      </Assign.To>
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">[If(in_MailItem.From IsNot Nothing, in_MailItem.From.Address, "")]</InArgument>
      </Assign.Value>
    </Assign>
    <ui:InvokeWorkflowFile DisplayName="Invoke ValidateCustomerIDFormat (3.1)" WorkflowFileName="Process\ValidateCustomerIDFormat.xaml">
      <ui:InvokeWorkflowFile.Arguments>
        <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[in_Config]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_Subject">[strSubject]</InArgument>
        <InArgument x:TypeArguments="x:String" x:Key="in_Body">[strBody]</InArgument>
        <OutArgument x:TypeArguments="x:String" x:Key="out_CustomerID">[strCustomerID]</OutArgument>
        <OutArgument x:TypeArguments="x:Boolean" x:Key="out_IsValid">[blnIDValid]</OutArgument>
      </ui:InvokeWorkflowFile.Arguments>
    </ui:InvokeWorkflowFile>
    <If Condition="[Not blnIDValid]" DisplayName="If 3.1 Failed - Invalid/Missing Customer ID">
      <If.Then>
        <Sequence DisplayName="Reply InvalidFormat and Stop">
          <ui:InvokeWorkflowFile DisplayName="Invoke SendExceptionReply (InvalidFormat)" WorkflowFileName="Process\SendExceptionReply.xaml">
            <ui:InvokeWorkflowFile.Arguments>
              <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[in_Config]</InArgument>
              <InArgument x:TypeArguments="snm:MailMessage" x:Key="in_MailItem">[in_MailItem]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_SenderEmail">[strSenderEmail]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_Reason">InvalidFormat</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_CustomerID">[strCustomerID]</InArgument>
            </ui:InvokeWorkflowFile.Arguments>
          </ui:InvokeWorkflowFile>
          <ui:InvokeWorkflowFile DisplayName="Invoke MoveAndMarkEmail (Exception)" WorkflowFileName="Process\MoveAndMarkEmail.xaml">
            <ui:InvokeWorkflowFile.Arguments>
              <InArgument x:TypeArguments="snm:MailMessage" x:Key="in_MailItem">[in_MailItem]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_TargetFolder">[in_Config("OutlookFolder_Exception").ToString]</InArgument>
            </ui:InvokeWorkflowFile.Arguments>
          </ui:InvokeWorkflowFile>
          <Assign DisplayName="Set Status = BusinessException">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[out_TransactionStatus]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">BusinessException</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Set blnContinue = False">
            <Assign.To>
              <OutArgument x:TypeArguments="x:Boolean">[blnContinue]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:Boolean">[False]</InArgument>
            </Assign.Value>
          </Assign>
        </Sequence>
      </If.Then>
      <If.Else>
        <Sequence DisplayName="" />
      </If.Else>
    </If>
    <If Condition="[blnContinue]" DisplayName="If Continue - Run 3.2 Customer Master Lookup">
      <If.Then>
        <Sequence DisplayName="3.2 Customer Master Lookup">
          <ui:InvokeWorkflowFile DisplayName="Invoke LookupCustomerMaster (3.2)" WorkflowFileName="Process\LookupCustomerMaster.xaml">
            <ui:InvokeWorkflowFile.Arguments>
              <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[in_Config]</InArgument>
              <InArgument x:TypeArguments="sd:DataTable" x:Key="in_dtCustomerMaster">[in_dtCustomerMaster]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_CustomerID">[strCustomerID]</InArgument>
              <OutArgument x:TypeArguments="x:Boolean" x:Key="out_Found">[blnFound]</OutArgument>
              <OutArgument x:TypeArguments="x:Boolean" x:Key="out_Active">[blnActive]</OutArgument>
              <OutArgument x:TypeArguments="x:Boolean" x:Key="out_Excluded">[blnExcluded]</OutArgument>
            </ui:InvokeWorkflowFile.Arguments>
          </ui:InvokeWorkflowFile>
          <If Condition="[Not blnFound]" DisplayName="If Not Found">
            <If.Then>
              <Sequence DisplayName="Reply NotFound and Stop">
                <ui:InvokeWorkflowFile DisplayName="Invoke SendExceptionReply (NotFound)" WorkflowFileName="Process\SendExceptionReply.xaml">
                  <ui:InvokeWorkflowFile.Arguments>
                    <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[in_Config]</InArgument>
                    <InArgument x:TypeArguments="snm:MailMessage" x:Key="in_MailItem">[in_MailItem]</InArgument>
                    <InArgument x:TypeArguments="x:String" x:Key="in_SenderEmail">[strSenderEmail]</InArgument>
                    <InArgument x:TypeArguments="x:String" x:Key="in_Reason">NotFound</InArgument>
                    <InArgument x:TypeArguments="x:String" x:Key="in_CustomerID">[strCustomerID]</InArgument>
                  </ui:InvokeWorkflowFile.Arguments>
                </ui:InvokeWorkflowFile>
                <ui:InvokeWorkflowFile DisplayName="Invoke MoveAndMarkEmail (Exception)" WorkflowFileName="Process\MoveAndMarkEmail.xaml">
                  <ui:InvokeWorkflowFile.Arguments>
                    <InArgument x:TypeArguments="snm:MailMessage" x:Key="in_MailItem">[in_MailItem]</InArgument>
                    <InArgument x:TypeArguments="x:String" x:Key="in_TargetFolder">[in_Config("OutlookFolder_Exception").ToString]</InArgument>
                  </ui:InvokeWorkflowFile.Arguments>
                </ui:InvokeWorkflowFile>
                <Assign DisplayName="Set Status = BusinessException">
                  <Assign.To>
                    <OutArgument x:TypeArguments="x:String">[out_TransactionStatus]</OutArgument>
                  </Assign.To>
                  <Assign.Value>
                    <InArgument x:TypeArguments="x:String">BusinessException</InArgument>
                  </Assign.Value>
                </Assign>
                <Assign DisplayName="Set blnContinue = False">
                  <Assign.To>
                    <OutArgument x:TypeArguments="x:Boolean">[blnContinue]</OutArgument>
                  </Assign.To>
                  <Assign.Value>
                    <InArgument x:TypeArguments="x:Boolean">[False]</InArgument>
                  </Assign.Value>
                </Assign>
              </Sequence>
            </If.Then>
            <If.Else>
              <If Condition="[Not blnActive]" DisplayName="If Not Active">
                <If.Then>
                  <Sequence DisplayName="Reply Inactive and Stop">
                    <ui:InvokeWorkflowFile DisplayName="Invoke SendExceptionReply (Inactive)" WorkflowFileName="Process\SendExceptionReply.xaml">
                      <ui:InvokeWorkflowFile.Arguments>
                        <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[in_Config]</InArgument>
                        <InArgument x:TypeArguments="snm:MailMessage" x:Key="in_MailItem">[in_MailItem]</InArgument>
                        <InArgument x:TypeArguments="x:String" x:Key="in_SenderEmail">[strSenderEmail]</InArgument>
                        <InArgument x:TypeArguments="x:String" x:Key="in_Reason">Inactive</InArgument>
                        <InArgument x:TypeArguments="x:String" x:Key="in_CustomerID">[strCustomerID]</InArgument>
                      </ui:InvokeWorkflowFile.Arguments>
                    </ui:InvokeWorkflowFile>
                    <ui:InvokeWorkflowFile DisplayName="Invoke MoveAndMarkEmail (Exception)" WorkflowFileName="Process\MoveAndMarkEmail.xaml">
                      <ui:InvokeWorkflowFile.Arguments>
                        <InArgument x:TypeArguments="snm:MailMessage" x:Key="in_MailItem">[in_MailItem]</InArgument>
                        <InArgument x:TypeArguments="x:String" x:Key="in_TargetFolder">[in_Config("OutlookFolder_Exception").ToString]</InArgument>
                      </ui:InvokeWorkflowFile.Arguments>
                    </ui:InvokeWorkflowFile>
                    <Assign DisplayName="Set Status = BusinessException">
                      <Assign.To>
                        <OutArgument x:TypeArguments="x:String">[out_TransactionStatus]</OutArgument>
                      </Assign.To>
                      <Assign.Value>
                        <InArgument x:TypeArguments="x:String">BusinessException</InArgument>
                      </Assign.Value>
                    </Assign>
                    <Assign DisplayName="Set blnContinue = False">
                      <Assign.To>
                        <OutArgument x:TypeArguments="x:Boolean">[blnContinue]</OutArgument>
                      </Assign.To>
                      <Assign.Value>
                        <InArgument x:TypeArguments="x:Boolean">[False]</InArgument>
                      </Assign.Value>
                    </Assign>
                  </Sequence>
                </If.Then>
                <If.Else>
                  <If Condition="[blnExcluded]" DisplayName="If Excluded">
                    <If.Then>
                      <Sequence DisplayName="Reply Excluded and Stop">
                        <ui:InvokeWorkflowFile DisplayName="Invoke SendExceptionReply (Excluded)" WorkflowFileName="Process\SendExceptionReply.xaml">
                          <ui:InvokeWorkflowFile.Arguments>
                            <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[in_Config]</InArgument>
                            <InArgument x:TypeArguments="snm:MailMessage" x:Key="in_MailItem">[in_MailItem]</InArgument>
                            <InArgument x:TypeArguments="x:String" x:Key="in_SenderEmail">[strSenderEmail]</InArgument>
                            <InArgument x:TypeArguments="x:String" x:Key="in_Reason">Excluded</InArgument>
                            <InArgument x:TypeArguments="x:String" x:Key="in_CustomerID">[strCustomerID]</InArgument>
                          </ui:InvokeWorkflowFile.Arguments>
                        </ui:InvokeWorkflowFile>
                        <ui:InvokeWorkflowFile DisplayName="Invoke MoveAndMarkEmail (Exception)" WorkflowFileName="Process\MoveAndMarkEmail.xaml">
                          <ui:InvokeWorkflowFile.Arguments>
                            <InArgument x:TypeArguments="snm:MailMessage" x:Key="in_MailItem">[in_MailItem]</InArgument>
                            <InArgument x:TypeArguments="x:String" x:Key="in_TargetFolder">[in_Config("OutlookFolder_Exception").ToString]</InArgument>
                          </ui:InvokeWorkflowFile.Arguments>
                        </ui:InvokeWorkflowFile>
                        <Assign DisplayName="Set Status = BusinessException">
                          <Assign.To>
                            <OutArgument x:TypeArguments="x:String">[out_TransactionStatus]</OutArgument>
                          </Assign.To>
                          <Assign.Value>
                            <InArgument x:TypeArguments="x:String">BusinessException</InArgument>
                          </Assign.Value>
                        </Assign>
                        <Assign DisplayName="Set blnContinue = False">
                          <Assign.To>
                            <OutArgument x:TypeArguments="x:Boolean">[blnContinue]</OutArgument>
                          </Assign.To>
                          <Assign.Value>
                            <InArgument x:TypeArguments="x:Boolean">[False]</InArgument>
                          </Assign.Value>
                        </Assign>
                      </Sequence>
                    </If.Then>
                    <If.Else>
                      <Sequence DisplayName="" />
                    </If.Else>
                  </If>
                </If.Else>
              </If>
            </If.Else>
          </If>
        </Sequence>
      </If.Then>
      <If.Else>
        <Sequence DisplayName="" />
      </If.Else>
    </If>
    <If Condition="[blnContinue]" DisplayName="If Continue - Run 3.3 Sender Authorization">
      <If.Then>
        <Sequence DisplayName="3.3 Sender Authorization">
          <ui:InvokeWorkflowFile DisplayName="Invoke LookupSenderAuthorization (3.3)" WorkflowFileName="Process\LookupSenderAuthorization.xaml">
            <ui:InvokeWorkflowFile.Arguments>
              <InArgument x:TypeArguments="sd:DataTable" x:Key="in_dtMasterExcel">[in_dtMasterExcel]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_SenderEmail">[strSenderEmail]</InArgument>
              <OutArgument x:TypeArguments="x:Boolean" x:Key="out_Authorized">[blnAuthorized]</OutArgument>
              <OutArgument x:TypeArguments="x:String" x:Key="out_MatGroup">[strMatGroup]</OutArgument>
              <OutArgument x:TypeArguments="x:String" x:Key="out_MatGroup4">[strMatGroup4]</OutArgument>
            </ui:InvokeWorkflowFile.Arguments>
          </ui:InvokeWorkflowFile>
          <If Condition="[Not blnAuthorized]" DisplayName="If Not Authorized">
            <If.Then>
              <Sequence DisplayName="Reply NotAuthorized and Stop">
                <ui:InvokeWorkflowFile DisplayName="Invoke SendExceptionReply (NotAuthorized)" WorkflowFileName="Process\SendExceptionReply.xaml">
                  <ui:InvokeWorkflowFile.Arguments>
                    <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[in_Config]</InArgument>
                    <InArgument x:TypeArguments="snm:MailMessage" x:Key="in_MailItem">[in_MailItem]</InArgument>
                    <InArgument x:TypeArguments="x:String" x:Key="in_SenderEmail">[strSenderEmail]</InArgument>
                    <InArgument x:TypeArguments="x:String" x:Key="in_Reason">NotAuthorized</InArgument>
                    <InArgument x:TypeArguments="x:String" x:Key="in_CustomerID">[strCustomerID]</InArgument>
                  </ui:InvokeWorkflowFile.Arguments>
                </ui:InvokeWorkflowFile>
                <ui:InvokeWorkflowFile DisplayName="Invoke MoveAndMarkEmail (Exception)" WorkflowFileName="Process\MoveAndMarkEmail.xaml">
                  <ui:InvokeWorkflowFile.Arguments>
                    <InArgument x:TypeArguments="snm:MailMessage" x:Key="in_MailItem">[in_MailItem]</InArgument>
                    <InArgument x:TypeArguments="x:String" x:Key="in_TargetFolder">[in_Config("OutlookFolder_Exception").ToString]</InArgument>
                  </ui:InvokeWorkflowFile.Arguments>
                </ui:InvokeWorkflowFile>
                <Assign DisplayName="Set Status = BusinessException">
                  <Assign.To>
                    <OutArgument x:TypeArguments="x:String">[out_TransactionStatus]</OutArgument>
                  </Assign.To>
                  <Assign.Value>
                    <InArgument x:TypeArguments="x:String">BusinessException</InArgument>
                  </Assign.Value>
                </Assign>
                <Assign DisplayName="Set blnContinue = False">
                  <Assign.To>
                    <OutArgument x:TypeArguments="x:Boolean">[blnContinue]</OutArgument>
                  </Assign.To>
                  <Assign.Value>
                    <InArgument x:TypeArguments="x:Boolean">[False]</InArgument>
                  </Assign.Value>
                </Assign>
              </Sequence>
            </If.Then>
            <If.Else>
              <Sequence DisplayName="" />
            </If.Else>
          </If>
        </Sequence>
      </If.Then>
      <If.Else>
        <Sequence DisplayName="" />
      </If.Else>
    </If>
    <If Condition="[blnContinue]" DisplayName="If Continue - Extract SAP Reports and Reply Success">
      <If.Then>
        <Sequence DisplayName="Section 4/5/6.1 - Extract and Reply">
          <Assign DisplayName="Build strTimestamp (shared by Report1 and Report2)">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[strTimestamp]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">[Now.ToString("yyyyMMdd_HHmmss")]</InArgument>
            </Assign.Value>
          </Assign>
          <Assign DisplayName="Build strOutputFolder">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[strOutputFolder]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">[Path.Combine(in_Config("OutputBasePath").ToString, strCustomerID + "_" + strTimestamp) + "\"]</InArgument>
            </Assign.Value>
          </Assign>
          <ui:InvokeWorkflowFile DisplayName="Invoke ExtractReport1_CustomerStatement (Section 4)" WorkflowFileName="Process\ExtractReport1_CustomerStatement.xaml">
            <ui:InvokeWorkflowFile.Arguments>
              <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[in_Config]</InArgument>
              <InArgument x:TypeArguments="ui:Window" x:Key="in_SAP">[in_SAP]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_CustomerID">[strCustomerID]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_OutputFolder">[strOutputFolder]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_Timestamp">[strTimestamp]</InArgument>
              <OutArgument x:TypeArguments="x:String" x:Key="out_ReportFilePath">[strReport1Path]</OutArgument>
              <OutArgument x:TypeArguments="x:String" x:Key="out_CustomerName">[strCustomerName]</OutArgument>
              <OutArgument x:TypeArguments="x:String" x:Key="out_Account">[strAccount]</OutArgument>
              <OutArgument x:TypeArguments="x:String" x:Key="out_GeneratedOn">[strGeneratedOn]</OutArgument>
              <OutArgument x:TypeArguments="x:String" x:Key="out_TotalAllProducts">[strTotalAllProducts]</OutArgument>
              <OutArgument x:TypeArguments="x:String" x:Key="out_BillDateLow">[strBillDateLow]</OutArgument>
              <OutArgument x:TypeArguments="x:String" x:Key="out_BillDateHigh">[strBillDateHigh]</OutArgument>
              <OutArgument x:TypeArguments="x:Boolean" x:Key="out_HasOutstandingItems">[blnHasOutstandingItems]</OutArgument>
            </ui:InvokeWorkflowFile.Arguments>
          </ui:InvokeWorkflowFile>
          <ui:InvokeWorkflowFile DisplayName="Invoke ExtractReport2_DailySalesReport (Section 5)" WorkflowFileName="Process\ExtractReport2_DailySalesReport.xaml">
            <ui:InvokeWorkflowFile.Arguments>
              <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[in_Config]</InArgument>
              <InArgument x:TypeArguments="ui:Window" x:Key="in_SAP">[in_SAP]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_CustomerID">[strCustomerID]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_MatGroup">[strMatGroup]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_MatGroup4">[strMatGroup4]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_Report1FilePath">[strReport1Path]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_BillDateLow">[strBillDateLow]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_BillDateHigh">[strBillDateHigh]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_OutputFolder">[strOutputFolder]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_Timestamp">[strTimestamp]</InArgument>
              <OutArgument x:TypeArguments="x:String" x:Key="out_ReportFilePath">[strReport2Path]</OutArgument>
              <OutArgument x:TypeArguments="x:String" x:Key="out_TotalYourBrand">[strTotalYourBrand]</OutArgument>
            </ui:InvokeWorkflowFile.Arguments>
          </ui:InvokeWorkflowFile>
          <ui:InvokeWorkflowFile DisplayName="Invoke SendSuccessReply (Section 6.1)" WorkflowFileName="Process\SendSuccessReply.xaml">
            <ui:InvokeWorkflowFile.Arguments>
              <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[in_Config]</InArgument>
              <InArgument x:TypeArguments="snm:MailMessage" x:Key="in_MailItem">[in_MailItem]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_SenderEmail">[strSenderEmail]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_CustomerName">[strCustomerName]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_Account">[strAccount]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_GeneratedOn">[strGeneratedOn]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_TotalAllProducts">[strTotalAllProducts]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_TotalYourBrand">[strTotalYourBrand]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_Report1FilePath">[strReport1Path]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_Report2FilePath">[strReport2Path]</InArgument>
            </ui:InvokeWorkflowFile.Arguments>
          </ui:InvokeWorkflowFile>
          <ui:InvokeWorkflowFile DisplayName="Invoke MoveAndMarkEmail (Processed)" WorkflowFileName="Process\MoveAndMarkEmail.xaml">
            <ui:InvokeWorkflowFile.Arguments>
              <InArgument x:TypeArguments="snm:MailMessage" x:Key="in_MailItem">[in_MailItem]</InArgument>
              <InArgument x:TypeArguments="x:String" x:Key="in_TargetFolder">[in_Config("OutlookFolder_Processed").ToString]</InArgument>
            </ui:InvokeWorkflowFile.Arguments>
          </ui:InvokeWorkflowFile>
          <Assign DisplayName="Set Status = Successful">
            <Assign.To>
              <OutArgument x:TypeArguments="x:String">[out_TransactionStatus]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">Successful</InArgument>
            </Assign.Value>
          </Assign>
        </Sequence>
      </If.Then>
      <If.Else>
        <Sequence DisplayName="" />
      </If.Else>
    </If>
    <ui:LogMessage DisplayName="Log [Process] Done" Level="Info" Message="[&quot;[Process] Done Transaction #&quot; + in_TransactionID + &quot; | Status=&quot; + out_TransactionStatus + &quot; | CustomerID=&quot; + strCustomerID]" />
  </Sequence>"""

write_xaml(os.path.join(BASE, "Process.xaml"), "Process", members, body)

print("Process part 7 (orchestrator) done.")
