def createTicket(userID, message):

    try:
        import mysql.connector
        import random

        conn = mysql.connector.connect(host="localhost", user="root", passwd="admin")

        cursor = conn.cursor(dictionary=True)

        # Get all the agents
        query = "SELECT * FROM ticketsystem.agents"
        cursor.execute(query)
        agents = cursor.fetchall()

        # pick a random agent and assign the ticket
        agent = random.choice(agents)

        # Get all the ticket
        query = "SELECT ticket_id FROM ticketsystem.tickets"
        cursor.execute(query)
        ticketNums = cursor.fetchall()
        ticketNums = set([i['ticket_id'] for i in ticketNums])


        # generate a ticket number that does not exist
        ticketNum = random.randint(0, 10000)
        while ticketNum in ticketNums:
            ticketNum = random.randint(0, 10000)

        query ="INSERT INTO ticketsystem.tickets (ticket_id, user_id, agent_id, creator,  message) VALUES (%s, %s, %s, %s, %s)"

        print(query)
        values = (ticketNum, userID, agent['agent_id'], "user", message)
        cursor.execute(query, values)
        conn.commit()


        cursor.close()
        conn.close()
        
        return "success"

    except: 
        return "error"
    


def getUserAllTickets(userID):
    try:
        import mysql.connector

        conn = mysql.connector.connect(host="localhost", user="root", passwd="admin")

        cursor = conn.cursor(dictionary=True)

        # Get users all the unique tickets ids
        query = """
        SELECT t.ticket_id, CONVERT(t.created_at, CHAR) as created_at, t.message
        FROM ticketsystem.tickets t
        INNER JOIN (
            SELECT ticket_id, MIN(created_at) AS created_at
            FROM ticketsystem.tickets
            WHERE user_id = %s
            GROUP BY ticket_id
        ) AS oldest_tickets
        ON t.ticket_id = oldest_tickets.ticket_id 
        AND t.created_at = oldest_tickets.created_at
        WHERE t.user_id = %s
        ORDER BY t.created_at DESC;
        """
        cursor.execute(query, (userID, userID,))
        tickets = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return tickets

    except: 
        return "error"
    