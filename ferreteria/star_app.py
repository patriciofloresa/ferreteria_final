# star_app.py
from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn
import ssl

app = Starlette()


@app.route("/")
async def homepage(request):
    return JSONResponse({"hello": "world"})


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        ssl_version=ssl.PROTOCOL_SSLv23,
        cert_reqs=ssl.CERT_OPTIONAL,
        ssl_certfile="/home/buho/example.com+4.pem",  # Note that the generated certificates
        ssl_keyfile="/home/buho/example.com+4-key.pem",  # are used here
    )
