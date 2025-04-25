from flask import Flask, request, jsonify
from openai import OpenAI
from neo4j import GraphDatabase
import json
from flask_cors import CORS  # 添加这行

app = Flask(__name__)
CORS(app)  # 添加这行允许所有跨域请求

# Neo4j 数据库连接
uri = "bolt://localhost:7687"
username = "neo4j"
password = "qgys"

driver = GraphDatabase.driver(uri, auth=(username, password))

# OpenAI客户端配置
client = OpenAI(
    api_key="sk-bemrijlhcdtrnpuljdjtubflxwnkjwktlspysmnnylrbngbo",
    base_url="https://api.siliconflow.cn/v1"
)


# 将现有代码封装成函数
def get_cypher_query(natural_language_query):
    """使用LLM将自然语言问题转换为Cypher查询"""
    prompt = f"""
    你是一个Neo4j Cypher查询专家。根据下面的电影知识图谱结构，将自然语言问题转换为Cypher查询。

    知识图谱结构：
    - 节点类型: Movie ("id","did","name","year","directors","writers","actors","types","regions",
    "languages","release_date","runtime","alias","imdb","score","num","five","four","three","two","one","introduction","pic"), 
    type (mid,tid,degree), region (mid,rid,degree)
    - 关系: 
      - (:Movie)-[:HAS_TYPE]->(:Type)
      - (:Movie)-[:HAS_REGION]->(:Region)

    问题: "{natural_language_query}"

    请只返回Cypher查询语句，只能用给出的关系和节点属性查询。不要包含任何解释或额外文本。
    """

    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct",
        messages=[
            {"role": "system", "content": "你是一个专业的Neo4j Cypher查询转换器。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


def execute_cypher_query(cypher_query):
    """执行Cypher查询并返回结果"""
    with driver.session() as session:
        result = session.run(cypher_query)
        return [dict(record) for record in result]


def generate_natural_response(user_query, graph_results):
    """使用LLM生成自然语言回答"""
    prompt = f"""
    用户询问: {user_query}

    以下是来自知识图谱的原始数据:
    {graph_results}

    请根据上述数据，用自然语言生成一个友好、完整的回答。保持专业但口语化的语气。
    如果数据中包含多个结果，可以总结或列举主要信息。
    """

    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct",
        messages=[
            {"role": "system", "content": "你是一个电影知识专家，能够根据结构化数据生成流畅的自然语言回答。"},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )

    return response



@app.route('/movie/qa', methods=['POST'])
def movie_qa_endpoint():
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"error": "请求数据格式不正确"}), 400
            
        question = data['question']
        if not question or not isinstance(question, str):
            return jsonify({"error": "问题不能为空且必须是字符串"}), 400
            
        cypher_query = get_cypher_query(question)
        graph_results = execute_cypher_query(cypher_query)
        response = generate_natural_response(question, graph_results)
        
        answer = ""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content
                
        return jsonify({
            "cypherQuery": cypher_query,
            "answer": answer
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
