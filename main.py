import orjson
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# třída pro seriál
class SeriesRecord(BaseModel):
    title: str
    year: int
    rating: float
    station: str
    genre: str

    @staticmethod
    def from_dict(data: dict):
        record = SeriesRecord(**data)
        return record


class Problem(BaseModel):
    detail: str

# třída databáze
class Database:
    def __init__(self):
        self._data: list = []
    # načtení dat ze souboru
    def load_from_filename(self, filename: str):
        with open(filename, "rb") as f:
            data = orjson.loads(f.read())
            for record in data:
                obj = SeriesRecord.from_dict(record)
                self._data.append(obj)
    # onstranění seriálu
    def delete(self, id_series: int):
        if 0 < id_series >= len(self._data):
            return
        self._data.pop(id_series)
    # přidání seriálu
    def add(self, series: SeriesRecord):
        self._data.append(series)
    def get(self, id_series: int):
        if 0 < id_series >= len(self._data):
            return
        return self._data[id_series]
    def get_all(self) -> list[SeriesRecord]:
        return self._data
    # aktualizace seriálů
    def update(self, id_series: int, series: SeriesRecord):
        if 0 < id_series >= len(self._data):
            return
        self._data[id_series] = series

    def count(self) -> int:
        return len(self._data)

# naše databáze
db = Database()
db.load_from_filename('series.json')
app = FastAPI(title="Serialy API", version="0.1", docs_url="/docs")
app.is_shutdown = False

# vrátí všechny seriály
@app.get("/series", response_model=list[SeriesRecord], description="Vrátí seznam seriálů")
async def get_series():
    return db.get_all()


@app.get("/series/{id_series}", response_model=SeriesRecord)
async def get_series(id_series: int):
    return db.get(id_series)

# přidání seriálu
@app.post("/series", response_model=SeriesRecord, description="Přidáme seriál do databáze")
async def post_series(series: SeriesRecord):
    db.add(series)
    return series

# odstranění seriálu
@app.delete("/series/{id_series}", description="Odstraníme seriál", responses={
    404: {'model': Problem}
})
async def delete_series(id_series: int):
    series = db.get(id_series)
    if series is None:
        raise HTTPException(404, "Seriál neexistuje")
    db.delete(id_series)
    return {'status': 'smazano'}

# aktualizace seriálu
@app.patch("/series/{id_series}", description="Aktualizujeme seriál do databáze", responses={
    404: {'model': Problem}
})
async def update_series(id_series: int, updated_series: SeriesRecord):
    series = db.get(id_series)
    if series is None:
        raise HTTPException(404, "Seriál neexistuje")
    db.update(id_series, updated_series)
    return {'old': series, 'new': updated_series}
