import pymysql
from .config import config


class ConnectDatabase:
    def connect():
        """ Connect to the database server """
        conn = None
        try:
            # read connection parameters
            params = config()
    
            # connect to the SQL server
            print('Connecting to the database...')
            conn = pymysql.connect(**params)
    
            # create a cursor
            cur = conn.cursor()
            conn.autocommit = True

            # execute a statement
            print('SQL database version:')
            cur.execute('SELECT version()')
    
            # display the SQL database server version
            db_version = cur.fetchone()
            print(db_version)
        
            # close the communication with the SQL
            cur.close()
        except (Exception, pymysql.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

    def insertAnswer(qid, code, answer, sortorder, assessment_value, language, scale_id):
        """ Connect to the SQL database server """
        conn = None
        try:
            # read connection parameters
            params = config()
            # connect to the SQL server
            print('Connecting to the SQL database...')
            conn = pymysql.connect(**params)
            conn.autocommit = True

            # create a cursor
            cur = conn.cursor()
            
            # execute a statement
            print('Inserting Answers')
            cur.execute("""INSERT INTO answers(qid, code, answer, sortorder, assessment_value, language, scale_id) VALUES (%s, %s, %s, %s, %s, %s, %s);""", 
            (qid, code, answer, sortorder, assessment_value, language, scale_id))
            # close the communication with the SQL
            cur.close()

        except (Exception, pymysql.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

    def queryAnswer(qid):
        """ Connect to the SQL database server """
        conn = None
        query = []
        try:
            # read connection parameters
            params = config()
            # connect to the SQL server
            print('Connecting to the SQL database...')
            conn = pymysql.connect(**params)
            conn.autocommit = True

            # create a cursor
            cur = conn.cursor()
            
            # execute a statement

            cur.execute("""SELECT answer,code FROM limesurvey.answers WHERE qid=%s;""", (qid))
            query = cur.fetchall()
            # close the communication with the SQL
            cur.close()

        except (Exception, pymysql.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        return query

    def queryAnswer(qid):
        """ Connect to the SQL database server """
        conn = None
        query = []
        try:
            # read connection parameters
            params = config()
            # connect to the SQL server
            print('Connecting to the SQL database...')
            conn = pymysql.connect(**params)
            conn.autocommit = True

            # create a cursor
            cur = conn.cursor()
            
            # execute a statement

            cur.execute("""SELECT answer,code FROM limesurvey.answers WHERE qid=%s;""", (qid))
            query = cur.fetchall()
            # close the communication with the SQL
            cur.close()

        except (Exception, pymysql.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        return query

    def queryAnswerServiceOther(survey_id):
        """ Connect to the SQL database server """
        conn = None
        query = []
        try:
            # read connection parameters
            params = config()
            # connect to the SQL server
            print('Connecting to the SQL database...')
            conn = pymysql.connect(**params)
            conn.autocommit = True
            survey_id = "survey_" + survey_id
            # create a cursor
            cur = conn.cursor(pymysql.cursors.DictCursor)
            
            # execute a statement

            cur.execute("SELECT * FROM limesurvey." + survey_id + ";")
            query = cur.fetchall()
            # close the communication with the SQL
            cur.close()

        except (Exception, pymysql.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        return query

    def updateQueryAnsware(survey_id, answare_id, servico_id):
        """ Connect to the SQL database server """
        conn = None
        query = []
        errorstate = None
        try:
            # read connection parameters
            params = config()
            # connect to the SQL server
            print('Connecting to the SQL database...')
            conn = pymysql.connect(**params)
            conn.autocommit = True
            # survey_id = "survey_" + survey_id
            # create a cursor
            cur = conn.cursor(pymysql.cursors.DictCursor)
            
            # execute a statement
            survey_id = survey_id.strip()
            cur.execute('UPDATE limesurvey.survey_' + survey_id + ' SET ' + survey_id + 'X1X3="' + str(servico_id) + '", ' + survey_id + 'X1X3other="" WHERE id="'+ answare_id +'";')
            query = cur.fetchall()
            # close the communication with the SQL
            cur.close()

        except (Exception, pymysql.DatabaseError) as error:
            print(error)
            errorstate = error
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

        if errorstate:
            return errorstate
        else:
            return None

if __name__ == '__main__':
    print((ConnectDatabase.queryAnswerServiceOther('311832')))

# cur.execute("""UPDATE limesurvey.survey_311832 SET seed="321" WHERE id=6""")
