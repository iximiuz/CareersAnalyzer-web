from app import app, create_db_conn
from flask import request
import random
import json


@app.route('/api/skills')
def skills_view():
    conn = create_db_conn()
    q = request.args.get('q')
    result = []
    if q:
        sql = "SELECT skill.id, name FROM skill WHERE name LIKE ? LIMIT 5"
        try:
            result = [{'id': row[0], 'name': row[1]} for row in conn.execute(sql, (q + '%',))]
        finally:
            conn.close()

    return json.dumps(result)

@app.route('/api/skills/popular')
def popular_skills_view():
    conn = create_db_conn()
    sql = """SELECT skill.id, name, count(1) FROM job_skill LEFT JOIN skill ON job_skill.skill_id = skill.id
             GROUP BY name ORDER BY count(1) DESC LIMIT 30"""
    try:
        result = [{'id': row[0], 'name': row[1], 'count': row[2]} for row in conn.execute(sql)]
    except:
        result = []
    finally:
        conn.close()

    return json.dumps(result)


@app.route('/api/analyze')
def analyze_view():
    skills_ids = [int(s) for s in request.args.get('skills', '').split(',') if s.isdigit()]
    if not skills_ids:
        skills_ids = random.sample([s['id'] for s in json.loads(popular_skills_view())], 2)

    conn = create_db_conn()
    jobs = []
    related_skills = []
    selected_skills = []
    try:
        select_selected_skills_sql = "SELECT id, name FROM skill WHERE id IN (%s)" % (', '.join(['?']*len(skills_ids)))
        for row in conn.execute(select_selected_skills_sql, skills_ids):
            selected_skills.append({'id': row[0], 'name': row[1]})
        skills_ids = [s['id'] for s in selected_skills]

        select_jids_sql = "SELECT job_id FROM job_skill WHERE skill_id = ?"
        select_jids_sql = ' INTERSECT '.join([select_jids_sql]*len(skills_ids))
        job_ids = [row[0] for row in conn.execute(select_jids_sql, skills_ids)]

        select_jobs_sql = "SELECT id, name, url FROM job WHERE id IN (%s)" % (', '.join(['?']*len(job_ids)))
        for row in conn.execute(select_jobs_sql, job_ids):
            jobs.append({'id': row[0], 'name': row[1], 'url': row[2]})

        select_related_skills_sql = "SELECT id, name, count(1) FROM job_skill LEFT JOIN skill ON skill_id = id " \
                                    "WHERE job_id IN (%s) GROUP BY name" % (', '.join(['?']*len(jobs)))
        for row in conn.execute(select_related_skills_sql, [job['id'] for job in jobs]):
            if row[0] not in skills_ids:
                related_skills.append({'id': row[0], 'name': row[1], 'count': row[2]})

    finally:
        conn.close()

    return json.dumps({'jobs': jobs, 'relatedSkills': related_skills, 'skills': selected_skills})