try:
    import MySQLdb
    import MySQLdb.cursors
    from credentials import gstar
except:
    print 'Warning: No MySQLdb found'

def connect():
    conn = {
        'host': 'mysql-server.cc.swin.edu.au',
        'port': 3306,
        'db': 'gstar_raw',
        'cursorclass': MySQLdb.cursors.DictCursor,
    }
    conn.update(gstar)
    db = MySQLdb.connect(**conn)
    cur = db.cursor()
    return cur

def query_users():
    cur = connect()
    cur.execute('SELECT * FROM user INNER JOIN user_institutions ON user.user_id=user_institutions.user_id INNER JOIN institution ON user_institutions.institution_id=institution.institution_id')
    return cur.fetchall()

def query_projects():
    cur = connect()
    cur.execute('SELECT * FROM project INNER JOIN user ON project.project_administrator=user.user_id')
    return cur.fetchall()

def query_project_members():
    cur = connect()
    cur.execute('SELECT project_code, email_address FROM project INNER JOIN user_projects ON user_projects.project_id=project.project_id INNER JOIN user ON user_projects.user_id=user.user_id')
    return cur.fetchall()

def query_project(proj_code):
    cur = connect()
    cur.execute('SELECT * FROM project WHERE project_code=\'%s\''%proj_code)
    info = cur.fetchone()
    cur.execute('SELECT title, firstname, lastname, institution_name FROM user INNER JOIN user_projects ON user.user_id=user_projects.user_id INNER JOIN user_institutions ON user.user_id=user_institutions.user_id INNER JOIN institution ON user_institutions.institution_id=institution.institution_id WHERE user_projects.project_id=%d'%info['project_id'])
    info['members'] = cur.fetchall()
    return info

if __name__ == '__main__':
    projs = query_all_projects()
    for p in projs:
        print p['project_code']
    print query_project('p014_swin')
