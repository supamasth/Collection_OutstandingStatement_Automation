import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from xaml_common import write_xaml

BASE = os.path.join(os.path.dirname(__file__), "..")

members = ""

body = r"""  <Sequence DisplayName="Main - Collection_OutstandingStatement_Automation">
    <Sequence.Variables>
      <Variable x:TypeArguments="scg:Dictionary(x:String, x:Object)" Name="Config" />
      <Variable x:TypeArguments="ui:Window" Name="SAP" />
      <Variable x:TypeArguments="sd:DataTable" Name="dtCustomerMaster" />
      <Variable x:TypeArguments="sd:DataTable" Name="dtMasterExcel" />
      <Variable x:TypeArguments="scg:List(snm:MailMessage)" Name="listMails" />
      <Variable x:TypeArguments="x:Int32" Default="0" Name="intTransactionNumber" />
      <Variable x:TypeArguments="x:Boolean" Default="False" Name="blnNoItemsLeft" />
      <Variable x:TypeArguments="snm:MailMessage" Name="currentMail" />
      <Variable x:TypeArguments="x:String" Name="strTransactionID" />
      <Variable x:TypeArguments="x:Int32" Default="0" Name="intSuccessCount" />
      <Variable x:TypeArguments="x:Int32" Default="0" Name="intBusinessExceptionCount" />
      <Variable x:TypeArguments="x:Int32" Default="0" Name="intSystemExceptionCount" />
      <Variable x:TypeArguments="x:String" Name="strTransactionStatus" />
      <Variable x:TypeArguments="x:Int32" Name="intRetryCount" />
      <Variable x:TypeArguments="x:Boolean" Name="blnTransactionDone" />
      <Variable x:TypeArguments="x:String" Name="strScreenshotPath" />
    </Sequence.Variables>
    <TryCatch DisplayName="Main Process TryCatch">
      <TryCatch.Try>
        <Sequence DisplayName="REFramework Loop (Init - GetTxn/Process while items remain - EndProcess)">
          <ui:LogMessage DisplayName="Log [Main] Process Started" Level="Info" Message="[&quot;[Main] Collection_OutstandingStatement_Automation started - &quot; + Now.ToString(&quot;yyyy-MM-dd HH:mm:ss&quot;)]" />
          <ui:InvokeWorkflowFile DisplayName="Invoke InitAllApplications" WorkflowFileName="Framework\InitAllApplications.xaml">
            <ui:InvokeWorkflowFile.Arguments>
              <OutArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="out_Config">[Config]</OutArgument>
              <OutArgument x:TypeArguments="ui:Window" x:Key="out_SAP">[SAP]</OutArgument>
              <OutArgument x:TypeArguments="sd:DataTable" x:Key="out_dtCustomerMaster">[dtCustomerMaster]</OutArgument>
              <OutArgument x:TypeArguments="sd:DataTable" x:Key="out_dtMasterExcel">[dtMasterExcel]</OutArgument>
            </ui:InvokeWorkflowFile.Arguments>
          </ui:InvokeWorkflowFile>
          <Assign DisplayName="Initialize listMails">
            <Assign.To>
              <OutArgument x:TypeArguments="scg:List(snm:MailMessage)">[listMails]</OutArgument>
            </Assign.To>
            <Assign.Value>
              <InArgument x:TypeArguments="scg:List(snm:MailMessage)">[New List(Of MailMessage)()]</InArgument>
            </Assign.Value>
          </Assign>
          <While Condition="[Not blnNoItemsLeft]" DisplayName="While Items Remain (Get Transaction Data / Process Transaction)">
            <Sequence DisplayName="One Iteration">
              <ui:InvokeWorkflowFile DisplayName="Invoke GetTransactionData" WorkflowFileName="Framework\GetTransactionData.xaml">
                <ui:InvokeWorkflowFile.Arguments>
                  <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[Config]</InArgument>
                  <InOutArgument x:TypeArguments="scg:List(snm:MailMessage)" x:Key="io_listMails">[listMails]</InOutArgument>
                  <InOutArgument x:TypeArguments="x:Int32" x:Key="io_intTransactionNumber">[intTransactionNumber]</InOutArgument>
                  <OutArgument x:TypeArguments="snm:MailMessage" x:Key="out_MailItem">[currentMail]</OutArgument>
                  <OutArgument x:TypeArguments="x:String" x:Key="out_TransactionID">[strTransactionID]</OutArgument>
                  <OutArgument x:TypeArguments="x:Boolean" x:Key="out_NoItemsLeft">[blnNoItemsLeft]</OutArgument>
                </ui:InvokeWorkflowFile.Arguments>
              </ui:InvokeWorkflowFile>
              <If Condition="[Not blnNoItemsLeft]" DisplayName="If Has Item - Process Transaction (with Retry)">
                <If.Then>
                  <Sequence DisplayName="Process Transaction with Retry">
                    <Assign DisplayName="Reset intRetryCount">
                      <Assign.To>
                        <OutArgument x:TypeArguments="x:Int32">[intRetryCount]</OutArgument>
                      </Assign.To>
                      <Assign.Value>
                        <InArgument x:TypeArguments="x:Int32">[0]</InArgument>
                      </Assign.Value>
                    </Assign>
                    <Assign DisplayName="Reset blnTransactionDone">
                      <Assign.To>
                        <OutArgument x:TypeArguments="x:Boolean">[blnTransactionDone]</OutArgument>
                      </Assign.To>
                      <Assign.Value>
                        <InArgument x:TypeArguments="x:Boolean">[False]</InArgument>
                      </Assign.Value>
                    </Assign>
                    <While Condition="[Not blnTransactionDone]" DisplayName="While Not Done (BusinessRuleException = no retry via Process.xaml; unhandled Exception = retry up to MaxRetryNumber)">
                      <TryCatch DisplayName="TryCatch Process Transaction">
                        <TryCatch.Try>
                          <Sequence DisplayName="Try Process">
                            <ui:InvokeWorkflowFile DisplayName="Invoke Process" WorkflowFileName="Process\Process.xaml">
                              <ui:InvokeWorkflowFile.Arguments>
                                <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[Config]</InArgument>
                                <InArgument x:TypeArguments="ui:Window" x:Key="in_SAP">[SAP]</InArgument>
                                <InArgument x:TypeArguments="sd:DataTable" x:Key="in_dtCustomerMaster">[dtCustomerMaster]</InArgument>
                                <InArgument x:TypeArguments="sd:DataTable" x:Key="in_dtMasterExcel">[dtMasterExcel]</InArgument>
                                <InArgument x:TypeArguments="snm:MailMessage" x:Key="in_MailItem">[currentMail]</InArgument>
                                <InArgument x:TypeArguments="x:String" x:Key="in_TransactionID">[strTransactionID]</InArgument>
                                <OutArgument x:TypeArguments="x:String" x:Key="out_TransactionStatus">[strTransactionStatus]</OutArgument>
                              </ui:InvokeWorkflowFile.Arguments>
                            </ui:InvokeWorkflowFile>
                            <Assign DisplayName="Set blnTransactionDone = True">
                              <Assign.To>
                                <OutArgument x:TypeArguments="x:Boolean">[blnTransactionDone]</OutArgument>
                              </Assign.To>
                              <Assign.Value>
                                <InArgument x:TypeArguments="x:Boolean">[True]</InArgument>
                              </Assign.Value>
                            </Assign>
                          </Sequence>
                        </TryCatch.Try>
                        <TryCatch.Catches>
                          <Catch x:TypeArguments="s:Exception">
                            <ActivityAction x:TypeArguments="s:Exception">
                              <ActivityAction.Argument>
                                <DelegateInArgument x:TypeArguments="s:Exception" Name="ex" />
                              </ActivityAction.Argument>
                              <Sequence DisplayName="Handle ApplicationException">
                                <Assign DisplayName="Increment intRetryCount">
                                  <Assign.To>
                                    <OutArgument x:TypeArguments="x:Int32">[intRetryCount]</OutArgument>
                                  </Assign.To>
                                  <Assign.Value>
                                    <InArgument x:TypeArguments="x:Int32">[intRetryCount + 1]</InArgument>
                                  </Assign.Value>
                                </Assign>
                                <ui:LogMessage DisplayName="Log [AppEx] Retry" Level="Warn" Message="[&quot;[AppEx] Transaction #&quot; + strTransactionID + &quot; failed (attempt &quot; + intRetryCount.ToString + &quot; of &quot; + Config(&quot;MaxRetryNumber&quot;).ToString + &quot;): &quot; + ex.Message]" />
                                <If Condition="[intRetryCount &gt; CInt(Config(&quot;MaxRetryNumber&quot;).ToString)]" DisplayName="If Retries Exhausted - SystemException">
                                  <If.Then>
                                    <Sequence DisplayName="Escalate as SystemException">
                                      <Assign DisplayName="Set strTransactionStatus = SystemException">
                                        <Assign.To>
                                          <OutArgument x:TypeArguments="x:String">[strTransactionStatus]</OutArgument>
                                        </Assign.To>
                                        <Assign.Value>
                                          <InArgument x:TypeArguments="x:String">SystemException</InArgument>
                                        </Assign.Value>
                                      </Assign>
                                      <Assign DisplayName="Build strScreenshotPath">
                                        <Assign.To>
                                          <OutArgument x:TypeArguments="x:String">[strScreenshotPath]</OutArgument>
                                        </Assign.To>
                                        <Assign.Value>
                                          <InArgument x:TypeArguments="x:String">[Path.Combine(Config("ScreenshotFolder").ToString, "SystemException_" + strTransactionID + "_" + Now.ToString("yyyyMMdd_HHmmss") + ".png")]</InArgument>
                                        </Assign.Value>
                                      </Assign>
                                      <ui:InvokeWorkflowFile DisplayName="Invoke TakeScreenshot" WorkflowFileName="Framework\TakeScreenshot.xaml">
                                        <ui:InvokeWorkflowFile.Arguments>
                                          <InArgument x:TypeArguments="x:String" x:Key="in_Folder">[Config("ScreenshotFolder").ToString]</InArgument>
                                          <InOutArgument x:TypeArguments="x:String" x:Key="io_FilePath">[strScreenshotPath]</InOutArgument>
                                        </ui:InvokeWorkflowFile.Arguments>
                                      </ui:InvokeWorkflowFile>
                                      <ui:InvokeWorkflowFile DisplayName="Invoke SendAlertEmail (Section 6.3 System Exception)" WorkflowFileName="Framework\SendAlertEmail.xaml">
                                        <ui:InvokeWorkflowFile.Arguments>
                                          <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[Config]</InArgument>
                                          <InArgument x:TypeArguments="x:String" x:Key="in_TransactionID">[strTransactionID]</InArgument>
                                          <InArgument x:TypeArguments="x:String" x:Key="in_SenderEmail">[If(currentMail IsNot Nothing AndAlso currentMail.From IsNot Nothing, currentMail.From.Address, "")]</InArgument>
                                          <InArgument x:TypeArguments="x:String" x:Key="in_CustomerID">[""]</InArgument>
                                          <InArgument x:TypeArguments="x:String" x:Key="in_ExceptionType">[ex.GetType.Name]</InArgument>
                                          <InArgument x:TypeArguments="x:String" x:Key="in_ExceptionMessage">[ex.ToString]</InArgument>
                                          <InArgument x:TypeArguments="x:String" x:Key="in_ScreenshotPath">[strScreenshotPath]</InArgument>
                                        </ui:InvokeWorkflowFile.Arguments>
                                      </ui:InvokeWorkflowFile>
                                      <Assign DisplayName="Set blnTransactionDone = True">
                                        <Assign.To>
                                          <OutArgument x:TypeArguments="x:Boolean">[blnTransactionDone]</OutArgument>
                                        </Assign.To>
                                        <Assign.Value>
                                          <InArgument x:TypeArguments="x:Boolean">[True]</InArgument>
                                        </Assign.Value>
                                      </Assign>
                                    </Sequence>
                                  </If.Then>
                                  <If.Else>
                                    <Delay DisplayName="Delay Before Retry" Duration="[TimeSpan.FromSeconds(CInt(Config(&quot;RetryDelaySeconds&quot;).ToString))]" />
                                  </If.Else>
                                </If>
                              </Sequence>
                            </ActivityAction>
                          </Catch>
                        </TryCatch.Catches>
                      </TryCatch>
                    </While>
                    <ui:InvokeWorkflowFile DisplayName="Invoke SetTransactionStatus" WorkflowFileName="Framework\SetTransactionStatus.xaml">
                      <ui:InvokeWorkflowFile.Arguments>
                        <InArgument x:TypeArguments="x:String" x:Key="in_TransactionID">[strTransactionID]</InArgument>
                        <InArgument x:TypeArguments="x:String" x:Key="in_Status">[strTransactionStatus]</InArgument>
                        <InOutArgument x:TypeArguments="x:Int32" x:Key="io_intSuccessCount">[intSuccessCount]</InOutArgument>
                        <InOutArgument x:TypeArguments="x:Int32" x:Key="io_intBusinessExceptionCount">[intBusinessExceptionCount]</InOutArgument>
                        <InOutArgument x:TypeArguments="x:Int32" x:Key="io_intSystemExceptionCount">[intSystemExceptionCount]</InOutArgument>
                      </ui:InvokeWorkflowFile.Arguments>
                    </ui:InvokeWorkflowFile>
                  </Sequence>
                </If.Then>
                <If.Else>
                  <Sequence DisplayName="" />
                </If.Else>
              </If>
            </Sequence>
          </While>
          <ui:InvokeWorkflowFile DisplayName="Invoke EndProcess" WorkflowFileName="Framework\EndProcess.xaml">
            <ui:InvokeWorkflowFile.Arguments>
              <InArgument x:TypeArguments="x:Int32" x:Key="in_intSuccessCount">[intSuccessCount]</InArgument>
              <InArgument x:TypeArguments="x:Int32" x:Key="in_intBusinessExceptionCount">[intBusinessExceptionCount]</InArgument>
              <InArgument x:TypeArguments="x:Int32" x:Key="in_intSystemExceptionCount">[intSystemExceptionCount]</InArgument>
            </ui:InvokeWorkflowFile.Arguments>
          </ui:InvokeWorkflowFile>
        </Sequence>
      </TryCatch.Try>
      <TryCatch.Catches>
        <Catch x:TypeArguments="s:Exception">
          <ActivityAction x:TypeArguments="s:Exception">
            <ActivityAction.Argument>
              <DelegateInArgument x:TypeArguments="s:Exception" Name="exMain" />
            </ActivityAction.Argument>
            <ui:LogMessage DisplayName="Log [Main] Fatal Error" Level="Error" Message="[&quot;[Main] Fatal error outside the transaction loop (Init/EndProcess): &quot; + exMain.ToString]" />
          </ActivityAction>
        </Catch>
      </TryCatch.Catches>
      <TryCatch.Finally>
        <Sequence DisplayName="Always Close Applications">
          <ui:InvokeWorkflowFile DisplayName="Invoke CloseAllApplications" WorkflowFileName="Framework\CloseAllApplications.xaml">
            <ui:InvokeWorkflowFile.Arguments>
              <InArgument x:TypeArguments="scg:Dictionary(x:String, x:Object)" x:Key="in_Config">[Config]</InArgument>
              <InArgument x:TypeArguments="ui:Window" x:Key="in_SAP">[SAP]</InArgument>
            </ui:InvokeWorkflowFile.Arguments>
          </ui:InvokeWorkflowFile>
        </Sequence>
      </TryCatch.Finally>
    </TryCatch>
  </Sequence>"""

write_xaml(os.path.join(BASE, "Main.xaml"), "Main", members, body)

print("Main.xaml done.")
