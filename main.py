from fastapi import FastAPI
import json
import os

app = FastAPI()

@app.get("/products")
def read_products():
    file_path = 'data.json'
    products = []
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                products.append(json.loads(line))
    else:
        return {"message": "No products found."}  # Handle case where file doesn't exist

    return products

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
