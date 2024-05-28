import json
import asyncio
from flask import Flask, request, jsonify
from uagents import Model
from uagents.query import query
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

AGENT_ADDRESS = "agent1q293s8kxyjelr0tjks620aq6484rkvv5en6mwaya6ll6fq44c467jl92lql"
AGENT_URL="https://backend-uagents-k82dco92y-sumit-srimanis-projects.vercel.app/submit"

class TestRequest(Model):
    city_name: str
    state_code: str
    country_code: str

async def agent_query(city_name, state_code, country_code):
    req = TestRequest(city_name=city_name, state_code=state_code, country_code=country_code)
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15.0)
    data = json.loads(response.decode_payload())
    print(f"Data received from agent: {data}")
    return data

@app.route('/', methods=['POST'])
def get_weather():
    request_data = request.get_json()
    city = request_data['cityName']
    state = request_data['stateName']
    country = request_data['countryName']
    
    try:
        data = asyncio.run(agent_query(city, state, country))
        return jsonify(data)
    except Exception as e:
        print(f"Error sending query: {e}")
        return jsonify({"status": "fail", "message": "Error occurred while fetching weather data", "data": {}})

if __name__ == '__main__':
    app.run(debug=True)
