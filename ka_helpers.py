import os
from dotenv import load_dotenv

load_dotenv()

# constants
#dictionary to hold extra headers
HEADERS = {"X-API-Key" : os.getenv('X_API_KEY')}

#root path
ROOTPATH = "https://www.bungie.net/Platform"

#account enum
#needs empty entry to fix off-by-one error
ACCOUNT_TYPE = ["", "XBL", "PS", "PC", "Battle.Net", "Stadia"]


def accountToPrettyString( dict ):
    returnMe = ""
    membershipType = dict.get('membershipType', 0)

    returnMe += "  *" + ACCOUNT_TYPE[membershipType] + "*\n"

    returnMe += "    Display Name: " + dict.get('displayName', '') + "\n"
    returnMe += "    Id: " + dict.get('membershipId', '0') + "\n"

    return returnMe


def hitToPrettyString( dict ):
    returnMe = " == " + dict.get('bungieGlobalDisplayName', '') + \
        "#" + "{0:0>4}".format(dict.get('bungieGlobalDisplayNameCode', 0)) + \
        " | " + str(dict.get('bungieNetMembershipId', '')) + " == " + \
        "\n"

    "{0:0>4}".format(dict.get('bungieGlobalDisplayNameCode', 0))

    #find primary account if it exists
    primaryAcctType = dict.get('primary', 0)
    if primaryAcctType != 0:
        primaryAcctDict = dict['accounts'][primaryAcctType]
        returnMe += "Primary: " + str(primaryAcctDict['membershipType']) + "|" + primaryAcctDict['membershipId'] + "\n"
    else:
        returnMe += "Cross-save not active (inactive player)\n"

    accounts = dict['accounts']

    #append each account
    for account in accounts:
        # 'account' is the key so we need to send the value to the formatter
        returnMe += accountToPrettyString(accounts[account])

    return returnMe + '\n\n\n'


def htmlFormatter( input ):
    #convert any '\n' into '<br />' for web display
    return '<br />'.join(input.splitlines())


def accountToSimpleString( dict ):
    returnMe = ""
    membershipType = dict.get('membershipType', 0)
    primaryAccountType = dict.get('primaryAccountType', 0)
    returnMe += ('*' if primaryAccountType == membershipType else "")
    returnMe += ACCOUNT_TYPE[membershipType] + " | " + dict.get('displayName', "") + "\n"

    return returnMe


def hitToSimpleString( dict ):
    returnMe = dict.get('bungieGlobalDisplayName', '') + \
        "#" + "{0:0>4}".format(dict.get('bungieGlobalDisplayNameCode', 0)) + \
        " | " + str(dict.get('bungieNetMembershipId', '')) + \
        "\n"
    #find primary account if it exists
    primaryAcctType = dict.get('primary', 0)
    if primaryAcctType != 0:
        primaryAcctDict = dict['accounts'][primaryAcctType]
        returnMe += primaryAcctDict['membershipId'] + "\n"
    else:
        returnMe += "Cross-save not active (inactive player)\n"

    accounts = dict['accounts']
    #append each account
    for account in accounts:
        # 'account' is the key so we need to send the value to the formatter
        returnMe += accountToSimpleString(accounts[account])

    return returnMe + '\n'
