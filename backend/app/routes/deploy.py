
from flask import Blueprint, request, jsonify
from app.db import db, connect_db
from app.tasks.worker import deploy_task  

deploy_bp = Blueprint('deploy', __name__)

@deploy_bp.route('/', methods=['POST'])
def trigger_deployment():
    data = request.json
    user_id = data.get('user_id')
    repo_url = data.get('repo_url')
    ssh_details = data.get('ssh_details')

    if not all([user_id, repo_url, ssh_details]):
        return jsonify({"error": "Missing required fields"}), 400

    connect_db()

    try:
       
        deployment = db.deployment.create(data={
            'userId': user_id,
            'repo_url': repo_url,
            'server_ip_address': ssh_details.get('hostname'),
            'status': 'queued'
        })

        
        task = deploy_task.delay(
            deployment_id=deployment.id,
            repo_url=repo_url,
            ssh_details=ssh_details
        )

       
        db.deployment.update(
            where={'id': deployment.id},
            data={'celery_task_id': task.id}
        )

        return jsonify({
            "message": "Deployment queued successfully",
            "deployment_id": deployment.id,
            "status": "queued"
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@deploy_bp.route('/<user_id>', methods=['GET'])
def get_user_deployments(user_id):
    connect_db()
    deployments = db.deployment.find_many(
        where={'userId': user_id},
        order={'created_at': 'desc'}
    )
    return jsonify([d.model_dump() for d in deployments]), 200