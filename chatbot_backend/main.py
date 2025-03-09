from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app.chatgpt import chat_with_gpt
from app.deepseek import chat_with_deepseek
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuração do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = os.getenv('SECRET_KEY') or "sua_chave_secreta"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

class ChatSession(db.Model):
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, db.ForeignKey('chat_session.id'), nullable=False)
    sender = db.Column(db.String, nullable=False)  # 'user' ou 'bot'
    content = db.Column(db.Text, nullable=False)

try:
    urlsvr = os.getenv('SQLALCHEMY_DATABASE_URI')
    print("URL DO SERVER: ",urlsvr)
    with app.app_context():
        db.create_all()
except Exception as e:
    print("URL DO SERVER: ",urlsvr)
    print(f"Erro ao inicializar o banco: {e}")

chat_sessions = {}
    
@app.route("/gpt/chat", methods=["POST"])
def gpt_chat():
    
    data = request.json
    user_input = data.get("message")
    print("MENSAGEM RECEBIDA: ",user_input)
    history = data.get("history", [])
    session_id = data.get("session_id")

    if not user_input:
        return jsonify({"error": "Mensagem não fornecida"}), 400

    response_text = chat_with_gpt(user_input, history)

    # Salva no banco
    session = ChatSession.query.get(session_id)
    if not session:
        return jsonify({"error": "Sessão não encontrada"}), 404

    # Salva a mensagem
    new_message_user = Message(session_id=session_id, sender="user", content=user_input)
    new_message_bot = Message(session_id=session_id, sender="bot", content=response_text)
    db.session.add(new_message_user)
    db.session.add(new_message_bot)
    db.session.commit()

    return jsonify({"response": response_text, "session_id": session_id})


@app.route("/deepseek/chat", methods=["POST"])
def deepseek_chat():
    """Handles DeepSeek Chat"""
    data = request.json
    user_input = data.get("message")
    history = data.get("history", [])
    session_id = data.get("session_id")

    if not user_input:
        return jsonify({"error": "Mensagem não fornecida"}), 400

    response_text = chat_with_deepseek(user_input, history)

    # Save message history
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    chat_sessions[session_id].append({"user": user_input, "bot": response_text})

    return jsonify({"response": response_text, "session_id": session_id})


@app.route("/chat/history", methods=["GET"])
def get_chat_history():
    """Returns all chat sessions"""
    return jsonify(chat_sessions)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    print("CAIU NO REGISTER: ",data.get("email"))
    hashed_password = generate_password_hash(data.get("password"))
    new_user = User(id=str(datetime.datetime.utcnow().timestamp()), email=data.get("email"), password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuário registrado com sucesso"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    print("CAIU NO REGISTER: ",data.get("email"))
    print("Data recebida:", data)  # Verifique o que o frontend está enviando

    user = User.query.filter_by(email=data.get("email")).first()
    print("Usuário encontrado:", user.email if user else "Nenhum usuário encontrado")

    if user:
        print("Hash no banco:", user.password)
        print("Senha enviada:", data.get("password"))
        print("Verificação:", check_password_hash(user.password, data.get("password")))

    if user and check_password_hash(user.password, data.get("password")):
        token = jwt.encode({"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token, "user": {"id": user.id, "email": user.email}})
    return jsonify({"error": "Credenciais inválidas"}), 401

@app.route("/sessions", methods=["GET"])
def get_sessions():
    token = request.headers.get('Authorization').split()[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded.get("user_id")
    except:
        return jsonify({"error": "Token inválido"}), 401
    sessions = ChatSession.query.filter_by(user_id=user_id).all()
    result = []
    for s in sessions:
        messages = Message.query.filter_by(session_id=s.id).all()
        msg_list = [{"user": msg.content if msg.sender == "user" else "", "bot": msg.content if msg.sender == "bot" else ""} for msg in messages]
        result.append({"id": s.id, "name": s.name, "model": s.model, "messages": msg_list})
    return jsonify(result)

@app.route("/sessions", methods=["POST"])
def create_session():
    token = request.headers.get('Authorization').split()[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return jsonify({"error": "Token inválido"}), 401
    data = request.json
    new_session = ChatSession(id=data["id"], user_id=decoded.get("user_id"), name=data["name"], model=data["model"])
    db.session.add(new_session)
    db.session.commit()
    return jsonify({"message": "Sessão criada"}), 201

@app.route("/sessions/<session_id>", methods=["PUT"])
def update_session(session_id):
    token = request.headers.get('Authorization').split()[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return jsonify({"error": "Token inválido"}), 401
    data = request.json
    Message.query.filter_by(session_id=session_id).delete()
    for msg in data["messages"]:
        new_message = Message(session_id=session_id, sender="user" if msg["user"] else "bot", content=msg["user"] or msg["bot"])
        db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Sessão atualizada"}), 200

@app.route("/sessions/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    token = request.headers.get('Authorization').split()[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return jsonify({"error": "Token inválido"}), 401
    Message.query.filter_by(session_id=session_id).delete()
    session = ChatSession.query.get(session_id)
    db.session.delete(session)
    db.session.commit()
    return jsonify({"message": "Sessão deletada"}), 200

@app.route("/sessions/<session_id>/rename", methods=["PUT"])
def rename_session(session_id):
    token = request.headers.get('Authorization').split()[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return jsonify({"error": "Token inválido"}), 401
    data = request.json
    session = ChatSession.query.get(session_id)
    if not session:
        return jsonify({"error": "Sessão não encontrada"}), 404
    session.name = data.get("name")
    db.session.commit()
    return jsonify({"message": "Nome da sessão atualizado"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
