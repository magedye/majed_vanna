import sys, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path: sys.path.insert(0,ROOT)

from fastapi import FastAPI
from vanna.servers.fastapi import VannaFastAPIServer
from app.agent.builder import agent
from app.agent.port_guard import find_available_port
from app.api.router import api_router
from app.config import HOST, PORT

def start():
    config={
      "cors":{"enabled":True,"allow_origins":["*"],"allow_credentials":True,"allow_methods":["*"],"allow_headers":["*"]},
      "dev_mode":False,
      "static_folder":"static"
    }
    server=VannaFastAPIServer(agent=agent, config=config)
    app=server.create_app()
    app.include_router(api_router, prefix="/api")
    port=find_available_port(PORT)
    server.run(host=HOST, port=port)

if __name__=="__main__":
    start()
