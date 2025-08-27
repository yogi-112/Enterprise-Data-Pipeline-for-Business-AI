from pydantic import BaseModel
from typing import Optional
import yaml

class Paths(BaseModel):
    raw: str
    interim: str
    processed: str
    models: str
    feature_db: str

class IFConfig(BaseModel):
    contamination: float
    n_estimators: int

class Modeling(BaseModel):
    pca_components: int
    isolation_forest: IFConfig

class Settings(BaseModel):
    seed: int
    n_customers: int
    n_products: int
    n_orders: int
    n_invoices: int
    n_tickets: int
    paths: Paths
    modeling: Modeling

def load_config(path: str = "configs/config.yaml") -> Settings:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return Settings(**data)
