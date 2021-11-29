# Could use shebang but avoided because python3 location not consistent across Mac and Linux
import data_service
import textwrap

def printWelcomeMenu():
    print('Welcome to ZCC CLI')

def printMainMenu():
    print('\n')
    print('Type \'ls\' to view all tickets')
    print('Type ticket number to view a ticket')
    print('Type \'quit\' to exit')

def formatTicketRow(ticket):
    return '{:6} {:50} {:10} {:20}'.format(ticket['id'], ticket['subject'], ticket['status'], ticket['updated_at'])

def formatTicketExpanded(ticket):
    formattedString =  """
Id: {} 
Subject: {}
Created At: {} 
Updated At: {} 
Requester Id: {} 
URL: {} 
Description: \n{}
"""
    
    ticketString = formattedString.format(
        ticket['id'], 
        textwrap.fill(ticket['subject'], 80), 
        ticket['created_at'], 
        ticket['updated_at'], 
        ticket['requester_id'], 
        textwrap.fill(ticket['url']),
        textwrap.fill(ticket['description']))

    return ticketString

def handleLs():
    respJson = data_service.fetchAll()

    # Printing Header
    print(formatTicketRow({
        'id': 'Id', 
        'subject': 'Subject',
        'status' : 'Status',
        'updated_at': 'Updated'
        }))
    print(100 * '-')

    # Printing tickets
    for ticket in respJson['tickets']:
        print(formatTicketRow(ticket))
    
    more_to_display = respJson['meta']['has_more']

    while(more_to_display):
        print('Type (N)ext, (P)revious, (S)top')
        respChoice = input()

        if(respChoice[0].upper() == 'N'):
            respJson = data_service.fetchPage(respJson['links']['next'])
            # Printing tickets
            for ticket in respJson['tickets']:
                print(formatTicketRow(ticket))
            more_to_display = respJson['meta']['has_more']
        elif(respChoice[0].upper() == 'P'):
            respJson = data_service.fetchPage(respJson['links']['prev'])
            # Printing tickets
            for ticket in respJson['tickets']:
                print(formatTicketRow(ticket))
            more_to_display = respJson['meta']['has_more']
        elif(respChoice[0].upper() == 'S'):
            more_to_display = False
        else:
            print('Invalid Input')

def handleTicketNumber(ticket_number):
    respJson = data_service.fetchTicket(ticket_number)

    if 'ticket' in respJson:
        print(formatTicketExpanded(respJson['ticket']))
    else:
        print('Ticket not found')


if(__name__ == '__main__'):
    printWelcomeMenu()

    while True:
        printMainMenu()

        inputString = input()

        if (inputString == 'ls'):
            print('Fetching tickets...')
            handleLs()
        elif (inputString == 'quit'):
            print('Thank you for using ZCC CLI. Have a good day :)')
            exit()
        else: 
            # Checking if it is int or invalid string.
            # A measure against possible injection
            isInt = True

            try:
                # converting to integer
                int(inputString)
            except ValueError:
                isInt = False
            
            if isInt:
                print('Fetching ticket...')
                handleTicketNumber(int(inputString))
            else:
                print('Invalid input')
                exit()