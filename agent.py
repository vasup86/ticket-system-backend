
def getAgentAllTickets(userID):
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
            WHERE agent_id = %s
            GROUP BY ticket_id
        ) AS oldest_tickets
        ON t.ticket_id = oldest_tickets.ticket_id 
        AND t.created_at = oldest_tickets.created_at
        WHERE t.agent_id = %s
        ORDER BY t.created_at DESC;
        """
        cursor.execute(query, (userID, userID,))
        tickets = cursor.fetchall()

        print(tickets)

        cursor.close()
        conn.close()
        
        return tickets
    
    except: 
        return "error"