#DB DRIVER CLASS
import logging
import math
from HWUtils import RecordNotFound
from HWUtils import DBVars
import psycopg2 as pg
from LobbyDBClient import *
logger= logging.getLogger('lobbyhw')


#IMPLEMENT THESE FUNCTIONS
class client:
    def __init__(self, override=False):
        # you add class variables here like
        # self.myvar="the greatest variable ever. the best"
        self.dbname="hw5"
        self.dbhost="127.0.0.1"
        self.dbport=5432
        self.dbusername="cappuser"
        self.dbpasswd="capp"
        self.conn = None

        #for grading do not modify
        if override:
            logger.info("Overriding DB connection params")
            self.dbname=DBVars.dbname
            self.dbhost=DBVars.dbhost
            self.dbport=DBVars.dbport
            self.dbusername=DBVars.dbusername
            self.dbpasswd=DBVars.dbpasswd

        pass

    # open a connection to a psql database, using the self.dbXX parameters
    def openConnection(self):
        '''
        Opens connection to the database
        '''
        logger.debug("Opening a Connection")
        
        try:
            self.conn = pg.connect(host= self.dbhost, 
                                    port = self.dbport,
                                    dbname = self.dbname, 
                                    user = self.dbusername,
                                    password = self.dbpasswd)

            connection = True

        except pg.error as error:
            print(error)

        return connection


    # Close any active connection(should be able to handle closing a closed conn)
    def closeConnection(self):
        '''
        Close connection to the database
        '''
        logger.debug("Closing Connection")

        try:
            self.conn.close()

        except pg.InterfaceError:
            pass

    def nan_to_none(self, dt):
        if type(dt) == float and math.isnan(dt):
            return None
        else:
            return dt



    def execute_sql(self, sql, params = None, mode = 'insert'):
        '''
        Open cursor, execute sql statement, close cursor

        Input:
            - sql: (string) sql query
            - params: (mix types) insert values
            - mode: (string) can either be 'insert' (default) or 'query'

        Output:
            - if mode: 'insert' => bool
            - if mode: 'query' => list of results
        '''
        try:
            cur = self.conn.cursor()

            if params: 
                cur.execute(sql, params) 
            else:
                cur.execute(sql)

            
            if mode == 'insert':
                

                self.conn.commit()
                cur.close()
                
                return True

            if mode == 'query':

                result_rows = []
                rows = list(cur.fetchall())

                cur.close()   

                if rows:
                            
                    for row in rows:
                       result_rows += [row]

                    return result_rows
                else:
                    raise RecordNotFound()

        except (Exception, pg.Error) as error:
            self.conn.rollback()

            


    ''' **************************
    ******* LOAD DATA FUNCITONS **
    *************************** '''

    # Note that a client may be loaded multiple times. Only load once per client_id and update if value changes
    # Return true if inserted or updated
    def loadClient(self, client_id, name, address1, address2, city, state, zip):

        sql = """INSERT INTO client (client_id, name, address1, address2, city, state, zip)
                  VALUES (%s, %s, %s, %s, %s, %s, %s) 
                  ON CONFLICT (client_id) DO UPDATE
                  SET name = EXCLUDED.name,
                      address1 = EXCLUDED.address1,
                      address2 = EXCLUDED.address2,
                      city = EXCLUDED.city,
                      state = EXCLUDED.state,
                      zip = EXCLUDED.zip;
              """

        entry = (self.nan_to_none(client_id), self.nan_to_none(name), self.nan_to_none(address1), self.nan_to_none(address2),
            self.nan_to_none(city), self.nan_to_none(state), self.nan_to_none(zip))

        result_sql = self.execute_sql(sql, params = entry)

        

    # Load an employer.
    # Note that an employer may get loaded multiple times. only load once per employer_id.
    # Only load once per client_id and update if value changes
    # Return True if inserted or updated
    def loadEmployer(self, employer_id, name, address1, address2, city, state, zip):

        sql = """INSERT INTO employer (employer_id, name, address1, address2, city, state, zip)
              VALUES (%s, %s, %s, %s, %s, %s, %s) 
              ON CONFLICT (employer_id) DO UPDATE
              SET name = EXCLUDED.name,
                  address1 = EXCLUDED.address1,
                  address2 = EXCLUDED.address2,
                  city = EXCLUDED.city,
                  state = EXCLUDED.state,
                  zip = EXCLUDED.zip;
              """

        entry = (self.nan_to_none(employer_id), self.nan_to_none(name), self.nan_to_none(address1),self.nan_to_none(address2),
            self.nan_to_none(city),self.nan_to_none(state),self.nan_to_none(zip))

        result_sql = self.execute_sql(sql, params = entry)

        return result_sql


    # Loads a lobbyist. Creates a connection for a lobbyist an employer and client
    # Note that this can be called multiple times per lobbyist. Load one Lobbyist per lobbyist_id.
    # Only load once per lobbyist_id and update if value changes
    # Each connection/relationship should be recorded.
    # This should be all or nothing - eg if one part of this process fails then no data changes should be made
    # Return True if inserted or updated
    def loadLobbyistAndCreateEmployerClientConnection(self, lobbyist_id, client_id, employer_id, lobbyist_salutation,lobbyist_first_name,lobbyist_last_name):
        sql_lobby = """INSERT INTO lobbyist (lobbyist_id, lobbyist_salutation, lobbyist_first_name,lobbyist_last_name)
                        VALUES (%s, %s, %s, %s) 
                        ON CONFLICT (lobbyist_id) DO UPDATE
                        SET lobbyist_salutation = EXCLUDED.lobbyist_salutation,
                          lobbyist_first_name = EXCLUDED.lobbyist_first_name,
                          lobbyist_last_name = EXCLUDED.lobbyist_last_name;
                    """
        sql_connect = """INSERT INTO connection (lobbyist_id, employer_id, client_id)
                    VALUES (%s, %s, %s);
              """


        entry_lobby = (self.nan_to_none(lobbyist_id),self.nan_to_none(lobbyist_salutation),
            self.nan_to_none(lobbyist_first_name), self.nan_to_none(lobbyist_last_name))

        result = self.execute_sql(sql_lobby, params = entry_lobby)

        entry_connect = (self.nan_to_none(lobbyist_id), self.nan_to_none(employer_id), 
            self.nan_to_none(client_id))

        result = self.execute_sql(sql_connect, params = entry_connect)

        return result


    ''' **********************************
    ******* MOD and READ DATA FUNCITONS **
    ********************************** '''

    # Insert an expenditure. IDs are ints. amount can be rounded to int.
    # Recipient is a string which can be limited to 250 characters
    # Return True if inserted
    def insertExpenditure(self, expenditure_id, lobbyist_id, action, amount, expenditure_date, purpose, recipient, client_id):
        sql = """INSERT INTO expenditures (expenditure_id, lobbyist_id, action, amount, expenditure_date, purpose, recipient, client_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (expenditure_id) 
                    DO UPDATE SET 
                        lobbyist_id = EXCLUDED.lobbyist_id,
                          action = EXCLUDED.action,
                          amount = EXCLUDED.amount,
                          expenditure_date = EXCLUDED.expenditure_date,
                          purpose = EXCLUDED.purpose,
                          recipient = EXCLUDED.recipient,
                          client_id = EXCLUDED.client_id;
                """

        entry = (self.nan_to_none(expenditure_id),self.nan_to_none(lobbyist_id),self.nan_to_none(action),self.nan_to_none(amount), 
           self.nan_to_none(expenditure_date),self.nan_to_none(purpose),self.nan_to_none(recipient),self.nan_to_none(client_id))

        result_sql = self.execute_sql(sql, params = entry)

        return result_sql


    # Return a record/tuple for expenditure if exists
    # Else raise RecordNotFound
    def readExpenditureById(self, expenditure_id):
        sql = """SELECT * FROM expenditures WHERE expenditure_id = %s
              """

        entry = (expenditure_id,)

        result_sql = self.execute_sql(sql, params = entry, mode = 'query')

        return result_sql


    # Return a list of records/tuples for expenditures by a lobbyist_id, if exists
    # Else raise RecordNotFound
    def readExpendituresByLobbyistId(self, lobbyist_id):
        sql = """SELECT * FROM expenditures WHERE lobbyist_id = %s
              """

        entry = (lobbyist_id,)

        result_sql = self.execute_sql(sql, params = entry, mode = 'query')

        return result_sql

    # Insert a compensation. IDs are ints, amount can be rounded to int.
    # Return true if inserted
    def insertCompensation(self, compensation_id, lobbyist_id, compensation_amount, client_id):
        sql = """INSERT INTO compensations (compensation_id, lobbyist_id, compensation_amount, client_id)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (compensation_id) 
                    DO UPDATE SET 
                        lobbyist_id = EXCLUDED.lobbyist_id,
                          compensation_amount = EXCLUDED.compensation_amount,
                          client_id = EXCLUDED.client_id;
                """

        entry = (self.nan_to_none(compensation_id),self.nan_to_none(lobbyist_id),
            self.nan_to_none(compensation_amount), self.nan_to_none(client_id))

        result_sql = self.execute_sql(sql, params = entry)

        return result_sql


    # Return a record/tuple for compensation if exists
    # Else raise RecordNotFound
    def readCompensationById(self, compensation_id):
        sql = """SELECT * FROM compensations WHERE compensation_id = %s
              """

        entry = (compensation_id,)

        result_sql = self.execute_sql(sql, params = entry, mode = 'query')

        return result_sql


    # Return all records/tuples for compensations by a client_id if exists
    # Else raise RecordNotFound
    def readCompensationsByClientId(self, client_id):
        sql = """SELECT * FROM compensations WHERE client_id = %s
              """

        entry = (client_id,)

        result_sql = self.execute_sql(sql, params = entry, mode = 'query')

        return result_sql
            

    # Return all records/tuples for compensations by that are within the amounts (inclusive)
    # Else raise RecordNotFound
    def readCompensationsInBetween(self, compensation_amount_min,compensation_amount_max):
        sql = """SELECT * FROM compensations WHERE lobbyist_id BETWEEN %s AND %s
              """

        entry = (float(compensation_amount_min),float(compensation_amount_max))

        result_sql = self.execute_sql(sql, params = entry, mode = 'query')

        return result_sql
            

    # Insert a lobbying activity. action sought and department can be truncated to 250 characters
    # Return true if inserted
    def insertActivity(self, lobbying_activity_id, action_sought, department, client_id, lobbyist_id):
        sql = """INSERT INTO activity (lobbying_activity_id, action_sought, department, client_id, lobbyist_id)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (lobbying_activity_id) DO UPDATE
                    SET action_sought = EXCLUDED.action_sought,
                          department = EXCLUDED.department,
                          client_id = EXCLUDED.client_id,
                          lobbyist_id = EXCLUDED.lobbyist_id;
                """

        entry = (self.nan_to_none(lobbying_activity_id),self.nan_to_none(action_sought),
            self.nan_to_none(department),self.nan_to_none(client_id),self.nan_to_none(lobbyist_id))

        result_sql = self.execute_sql(sql, params = entry)

        return result_sql
            
        

    # Read a lobbying activity by ID if exists
    # Else raise RecordNotFound
    def readActivityById(self, lobbying_activity_id):
        sql = """SELECT * FROM activity WHERE lobbying_activity_id = %s
              """

        entry = (lobbying_activity_id,)

        result_sql = self.execute_sql(sql, params = entry, mode = 'query')

        return result_sql
            


    ''' *****************************
    ******* ANALYZE DATA FUNCITONS **
    ***************************** '''

    # Return the count of lobvying activity on behalf of a client. 0 if none exists
    def countActivityByClientId(self, client_id):
        sql = """SELECT client_id, COUNT(lobbying_activity_id) AS num_active
                    FROM activity 
                    WHERE client_id = %s
                    GROUP BY client_id;
              """

        entry = (client_id,)

        result_sql = self.execute_sql(sql, params = entry, mode = 'query')

        return result_sql


    # Find the lobbyist (id,name) who has the most level of activity per dollar spent
    # (e.g. has highest count of activity per compensation dollar)
    def findMostProductiveLobbyist(self):
        sql = """
                WITH t_compensation AS(
                    SELECT lobbyist_id, SUM(compensation_amount) as tot_compensation
                        FROM compensations
                        GROUP BY lobbyist_id),
                    c_activity AS(
                        SELECT lobbyist_id, COUNT(lobbying_activity_id) as count_activity
                        FROM activity
                        GROUP BY lobbyist_id),
                    lobbysummary AS(
                        SELECT l.lobbyist_id, count_activity/tot_compensation as productivity, 
                            l.lobbyist_first_name||' '||l.lobbyist_last_name AS lobbyist_name
                        FROM lobbyist l, t_compensation tc, c_activity ca
                        WHERE l.lobbyist_id = tc.lobbyist_id 
                            AND l.lobbyist_id = ca.lobbyist_id 
                            AND tc.lobbyist_id = ca.lobbyist_id)
                SELECT lobbyist_id, lobbyist_name 
                    FROM lobbysummary
                    ORDER BY productivity DESC
                    LIMIT 1; 
            """

        result_sql = self.execute_sql(sql, mode = 'query')

        return result_sql


    # Return a list of client(ids) of clients who spent more than the average per client,
    # Rank these clients in the order of lowest amount of activity per dollar spent
    def findLeastEfficientClient(self):
        sql = """WITH spending AS(SELECT c.client_id, compensation_amount, amount
                    FROM compensations c
                        FULL OUTER JOIN expenditures e
                        ON c.client_id = e.client_id),
                spendingsum AS(SELECT client_id, SUM(compensation_amount) as tot_compensation, 
                        SUM(amount) as tot_expenditure
                    FROM spending
                    GROUP BY client_id),
                totspend AS(
                    SELECT client_id, tot_compensation+tot_expenditure as tot_spending
                    FROM spendingsum),
                aboveavgspend AS(
                    SELECT client_id, tot_spending
                    FROM totspend
                    WHERE tot_spending > (SELECT AVG(tot_spending) FROM totspend)),
                c_activity AS(
                    SELECT client_id, COUNT(lobbying_activity_id) as count_activity
                    FROM activity
                    GROUP BY client_id),
                spendsummary AS(
                    SELECT avg.client_id, count_activity/tot_spending as efficiency
                    FROM aboveavgspend avg 
                    LEFT JOIN c_activity ca ON avg.client_id = ca.client_id)
                SELECT client_id
                    FROM spendsummary
                    ORDER BY efficiency ASC;
              """

        result_sql = self.execute_sql(sql, mode = 'query')

        return result_sql


    ''' ******************************
    ******* VALIDATE DATA FUNCITONS **
    ****************************** '''
    # Return the count of records in a given entity_type
    # get the total number of records -- your table name maybe different
    def countRecords(self, entity):
        if entity == 'compensations':
            sql = """SELECT COUNT(*) FROM compensations;"""

            return self.execute_sql(sql, mode = 'query')

        elif entity == 'expenditures':
            sql = """SELECT COUNT(*) FROM expenditures;"""

            return self.execute_sql(sql, mode = 'query')

        elif entity == 'activity':
            sql = """SELECT COUNT(*) FROM activity;"""

            return self.execute_sql(sql, mode = 'query')
        
        elif entity == 'client':
            sql = """SELECT COUNT(*) FROM client;"""

            return self.execute_sql(sql, mode = 'query')
        
        elif entity == 'employer':
            sql = """SELECT COUNT(*) FROM employer;"""

            return self.execute_sql(sql, mode = 'query')
        
        elif entity == 'lobbyist':
            sql = """SELECT COUNT(*) FROM lobbyist;"""

            return self.execute_sql(sql, mode = 'query')

        else:
            logger.error( "Unknown entity : %s" % entity)
            return None
