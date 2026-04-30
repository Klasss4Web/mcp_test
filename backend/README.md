# To run the FastAPI app, use:
# uvicorn main:app --reload

# To run the FastAPI app on Render, use:
# uvicorn main:app --host 0.0.0.0 --port $PORT
# (or)
# gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
