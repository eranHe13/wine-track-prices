from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import scraping_script
import crud_api
import uvicorn

'''
API for requests from clients to the server
'''

app = FastAPI()

# Setup CORS
origins = [
    "http://localhost:3000",  # Adjust based on the front-end's port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint: Login
@app.post("/login/")
async def check_log_in(user_data: dict = Body(...)):
    try:
        res = crud_api.fetch_user_login_details_with_wines(user_data["email"], user_data["password"])
        return {"user": res}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# Endpoint: Get User Details
@app.post("/details/")
async def get_user_details(user_id: dict = Body(...)):
    try:
        res = crud_api.fetch_user_wine_list(user_id["userID"])
        return {"data": res}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# Endpoint: Add Wine to User List
@app.post("/addwine/")
async def add_wine_for_user(data: dict = Body(...)):
    try:
        res = crud_api.add_wine_to_user_list(data["user_id"], data["wine_name"], data["price"])
        return {"message": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint: Remove Wine from User List
@app.post("/removewine/")
async def remove_wine_for_user(data: dict = Body(...)):
    try:
        res = crud_api.remove_wine_from_user_list(data["user_id"], data["wine_name"])
        return {"message": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint: Scrape Wine Data and Save by Site
@app.post("/scrape/")
async def scrape_and_save(data: dict = Body(...)):
    try:
        wine_name = data["wine_name"]
        result = scraping_script.save_scraped_data_by_site(wine_name)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint: Register a New User
@app.post("/register/")
async def register(user_data: dict = Body(...)):
    try:
        res = crud_api.add_user(user_data["username"], user_data["email"], user_data["password"])
        return {"message": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint: Update Product Prices
@app.post("/updateprices/")
async def update_prices():
    try:
        wines = crud_api.get_all_wines()
        for wine in wines:
            scraping_script.save_scraped_data_by_site(wine[1])  # Assuming wine[1] is the wine name
        return {"message": "Prices updated successfully for all wines."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
