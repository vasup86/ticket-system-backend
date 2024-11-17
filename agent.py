
def getAgentAllTickets(agentID):
    try:
        import pymysql
        from dotenv import load_dotenv
        import os

        load_dotenv()


        timeout = 10

        conn = pymysql.connect(
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db="ticketsystem",
            host=f"{os.getenv('DATABASE_URL')}",
            password=f"{os.getenv('DATABASE_PASSWORD')}",
            read_timeout=timeout,
            port=13361,
            user=f"{os.getenv('DATABASE_USER')}",
            write_timeout=timeout,
        )
        
        cursor = conn.cursor()

        # Get users all the unique tickets ids
        query = """
        SELECT t.ticket_id, CONVERT(t.created_at, CHAR) as created_at, t.message, t.user_id, t.agent_id
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
        cursor.execute(query, (agentID, agentID,))
        tickets = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return tickets
    
    except: 
        return "error"
    

def getTicketMessages(ticketID):
    try:
        import pymysql
        from dotenv import load_dotenv
        import os

        load_dotenv()

        timeout = 10

        conn = pymysql.connect(
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db="ticketsystem",
            host=f"{os.getenv('DATABASE_URL')}",
            password=f"{os.getenv('DATABASE_PASSWORD')}",
            read_timeout=timeout,
            port=13361,
            user=f"{os.getenv('DATABASE_USER')}",
            write_timeout=timeout,
        )
        
        cursor = conn.cursor()

        # Get users all the unique tickets ids
        query = """
        SELECT creator, message, CONVERT(created_at, CHAR) as created_at 
        FROM ticketsystem.tickets 
        WHERE ticket_id = %s;
        """

        cursor.execute(query, (ticketID,))
        tickets = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return tickets
    
    except: 
        return "error"
    

def insertMessage(ticketID, userID, agentID, creator, message):

    try:
        import pymysql
        from dotenv import load_dotenv
        import os

        load_dotenv()


        timeout = 10

        conn = pymysql.connect(
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db="ticketsystem",
            host=f"{os.getenv('DATABASE_URL')}",
            password=f"{os.getenv('DATABASE_PASSWORD')}",
            read_timeout=timeout,
            port=13361,
            user=f"{os.getenv('DATABASE_USER')}",
            write_timeout=timeout,
        )
        
        cursor = conn.cursor()

        query = "INSERT INTO ticketsystem.tickets (ticket_id, user_id, agent_id, creator,  message) VALUES (%s, %s, %s, %s, %s)"
        values = (ticketID, userID, agentID, creator, message)
        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()
        
        return "success"

    except: 
        return "error"