from logging import root
from re import search
import requests
import argparse
import ka_helpers
import queue

#username request URL
usernameRequest = "/User/Search/GlobalName/"

#set to enable debug logging
DEBUG = False

def postRequest( searchString ):
    """
    Requests search results in a POST request to Bungie.net API then returns
    the results as a dictionary object.
        RETURN a python dictionary of the search results
    """

    #search term
    body = {
        "displayNamePrefix" : searchString
    }

    #make url string
    requestString = ka_helpers.ROOTPATH + usernameRequest

    #create queue to store results in json format
    resultQueue = queue.SimpleQueue()

    #need to add all pages, not just 0 to a queue to process
    lastPage = False
    pageIndex = 0
    while not lastPage:
        ka_helpers.debugPrint(DEBUG, 'searching page ' + str(pageIndex))
        #make request 
        r = requests.post(requestString + str(pageIndex), headers=ka_helpers.HEADERS, json=body)
        #convert the json object we received into a Python dictionary object
        result = r.json()
        if result.get('ErrorCode', 0) == 1:
            #normal result add to queue
            ka_helpers.debugPrint(DEBUG, 'adding page ' + str(pageIndex) + ' to queue')
            resultQueue.put(result)
            pageIndex += 1
        else:
            ka_helpers.debugPrint(DEBUG, 'no more pages')
            lastPage = True
    
    #return the results
    return resultQueue


def processResult( result, nameCode, cliRequest ):
    """
    Process the result dictionary. If general search (no name-code) print all results.
    If specific search (name-code provided) only print single matching result.
      RETURN a string of the processed results
    """

    #get just the hits and list them
    hits = result['Response']['searchResults']
    searchSpecific = (nameCode != 0)
    outputString = ''
    for i in hits:
        foundSpecific = False
        # create emtpy dictionary
        resultsDict = {}
        # save global display name
        resultsDict['bungieGlobalDisplayName'] = i.get('bungieGlobalDisplayName', '')
        # save bungie membership ID
        resultsDict['bungieNetMembershipId'] = i.get('bungieNetMembershipId', 0)
        # save bungie global display name code
        resultsDict['bungieGlobalDisplayNameCode'] = i.get('bungieGlobalDisplayNameCode', 0)
        if i.get('bungieGlobalDisplayNameCode', 0) == nameCode:
            foundSpecific = True
        # create new dictionary for accounts
        accountsDict = {}
        # attach accounts by type and find primary account type
        for j in i['destinyMemberships']:
            accountDict = {}
            membershipType = j['membershipType']
            primaryAccountType = j['crossSaveOverride']
            if primaryAccountType == 0:
                # cross-save not active
                resultsDict['primary'] = membershipType
            else:
                # cross-save active
                resultsDict['primary'] = primaryAccountType
            membershipId = j['membershipId']
            displayName = j['displayName']

            # store new account
            accountDict['membershipType'] = membershipType
            accountDict['primaryAccountType'] = primaryAccountType
            accountDict['membershipId'] = membershipId
            accountDict['displayName'] = displayName
            accountsDict[membershipType] = accountDict
        resultsDict['accounts'] = accountsDict
            
        # only print multiple results if we're searching for every string
        if searchSpecific == False:
            if cliRequest:
                outputString += ka_helpers.hitToPrettyString(resultsDict)
            else:
                outputString += ka_helpers.hitToSimpleString(resultsDict)
        elif foundSpecific == True:
            if cliRequest:
                outputString = ka_helpers.hitToPrettyString(resultsDict)
            else:
                outputString = ka_helpers.hitToSimpleString(resultsDict)

    return outputString



# method to search via python method call (internal request)
def internal_search( search, nameCode = 0, cliRequest = False ):
    """
    Takes an internal method call to search for a Bungie ID from a string.
      RETURNS a string of the search results
    """

    resultQueue = postRequest( search )

    processResultString = ''

    #move through queue and process results
    while not resultQueue.empty():
        processResultString += processResult(resultQueue.get(), nameCode, cliRequest)

    return processResultString


# Main method to search via CLI
#   return HTML formatted string
def main():
    """
    External CLI request to search for a given Bungie name and optionally a name/ID pair.
    Prints results to output.
    """
    # create a parser object
    parser = argparse.ArgumentParser(description = "Search for bungie IDs by display name")
    
    # add argument
    parser.add_argument("-s", "--search", nargs = 1, metavar = "query", type = str,
                        help = "Display name to search for.")
    parser.add_argument("-id", "--id", nargs = 1, metavar = "id", type = int,
                        help = "Name Code to find a specific account.")

    # parse the arguments from standard input
    args = parser.parse_args()
    searchString = ''
    if args.search != None:
        searchString = args.search[0]
    else:
        print('Requires search term; see --help')
        exit()
    nameCode = 0
    if args.id != None:
        nameCode = args.id[0]

    result = internal_search( searchString, nameCode, True )

    print(ka_helpers.htmlFormatter(result))


if __name__ == "__main__":
    # calling the main function
    main()
