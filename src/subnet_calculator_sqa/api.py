from fastapi import FastAPI, HTTPException, Query

from subnet_calculator_sqa.calc import hitung_subnet

app = FastAPI(title="Kalkulator Subnet")


@app.get("/subnet")
def subnet(ip: str, prefix: int = Query(ge=0, le=32)):
    try:
        return hitung_subnet(ip, prefix)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))