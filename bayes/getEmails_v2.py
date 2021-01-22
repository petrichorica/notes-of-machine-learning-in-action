import win32com.client
import win32com


def emailleri_al(folder):
    global count

    messages = folder.Items
    a=len(messages)
    num = 160
    if num>0:
        for message in messages:
            if count >= num:
                break
            try:
                sender = message.SenderEmailAddress
                if sender != "":
                    with open("%d.txt"%count, "w") as f:
                        f.write(sender + '\n')
                    # print(sender, file=f)
            except:
                continue

            try:
                body = message.Body
                with open("%d.txt"%count, "a") as f:
                    f.write(body)
                message.Close(0)
                count += 1
            except:
                continue


if __name__ == '__main__':
    outlook = win32com.client.Dispatch("Outlook.Application").GetNameSpace("MAPI")
    accounts = win32com.client.Dispatch("Outlook.Application").Session.Accounts
    # filename = "testfile.txt"
    count = 0

    for account in accounts:
        inbox = outlook.Folders(account.DeliveryStore.DisplayName)
        folders = inbox.Folders
        for folder in folders:
            emailleri_al(folder)
            a = len(folder.folders)