from io import BytesIO
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from psycopg.errors import UniqueViolation

from calculator import calculate_material
from materials import materials, get_material
from machines import get_machine
from compatibility import check_compatibility
from database import get_connection
from material_recommender import recommend_materials
from optimizer import optimize_coils
from production_planner import plan_production
from report_generator import generate_production_report


# ---------------------------------------
# CREATE SMARTROLL API
# ---------------------------------------

app = FastAPI(
    title="SmartRoll API",
    description="Intelligent Roll Forming Material Selection Software",
    version="1.3.0"
)


# ---------------------------------------
# ALLOW REACT FRONTEND CONNECTION
# ---------------------------------------

# Set FRONTEND_URL on the hosting platform to your deployed React URL.
# Multiple URLs can be supplied as a comma-separated list.
frontend_urls = os.getenv("FRONTEND_URL", "")
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
allowed_origins.extend(
    url.strip().rstrip("/")
    for url in frontend_urls.split(",")
    if url.strip()
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# ---------------------------------------
# HOME API
# ---------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to SmartRoll API",
        "status": "running"
    }


# ---------------------------------------
# HEALTH CHECK API
# ---------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "SmartRoll"
    }


# ---------------------------------------
# MATERIAL CALCULATION INPUT MODEL
# ---------------------------------------

class MaterialRequest(BaseModel):
    width_mm: float = Field(gt=0)
    thickness_mm: float = Field(gt=0)
    part_length_m: float = Field(gt=0)
    quantity: int = Field(gt=0)
    density: float = Field(gt=0)
    price_per_kg: float = Field(ge=0)
    waste_percentage: float = Field(ge=0, lt=100)


# ---------------------------------------
# MATERIAL CALCULATION API
# ---------------------------------------

@app.post("/calculate")
def calculate(request: MaterialRequest):
    result = calculate_material(
        width=request.width_mm,
        thickness=request.thickness_mm,
        length=request.part_length_m,
        quantity=request.quantity,
        density=request.density,
        price_per_kg=request.price_per_kg,
        waste_percent=request.waste_percentage
    )

    return {
        "message": "Material calculation successful",
        "result": result
    }


# ---------------------------------------
# LIST ALL MATERIALS
# ---------------------------------------

@app.get("/materials")
def list_materials():
    return {
        "message": "Available SmartRoll materials",
        "materials": materials
    }


# ---------------------------------------
# GET ONE MATERIAL
# ---------------------------------------

@app.get("/materials/{material_code}")
def material_details(material_code: str):
    material = get_material(material_code)

    if material is None:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    return {
        "material_code": material_code,
        "material": material
    }


# ---------------------------------------
# MACHINE COMPATIBILITY INPUT MODEL
# ---------------------------------------

class MachineCheckRequest(BaseModel):
    machine_code: str = Field(min_length=1)
    strip_width_mm: float = Field(gt=0)
    thickness_mm: float = Field(gt=0)


# ---------------------------------------
# MACHINE COMPATIBILITY API
# ---------------------------------------

@app.post("/check-machine")
def check_machine(request: MachineCheckRequest):
    machine = get_machine(request.machine_code)

    if machine is None:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    result = check_compatibility(
        machine,
        request.strip_width_mm,
        request.thickness_mm
    )

    return {
        "machine_code": request.machine_code,
        "machine_name": machine["name"],
        "compatibility": result
    }


# ---------------------------------------
# PRODUCTION ORDER INPUT MODEL
# ---------------------------------------

class ProductionOrderRequest(BaseModel):
    order_id: str = Field(min_length=1, max_length=50)
    material_code: str = Field(min_length=1, max_length=50)
    machine_code: str = Field(min_length=1, max_length=50)
    quantity: int = Field(gt=0)
    part_length: float = Field(gt=0)


# ---------------------------------------
# SAVE PRODUCTION ORDER API
# ---------------------------------------

@app.post("/orders", status_code=201)
def create_order(request: ProductionOrderRequest):
    material = get_material(request.material_code)

    if material is None:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    machine = get_machine(request.machine_code)

    if machine is None:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO production_orders
                    (order_id, material_code, machine_code,
                     quantity, part_length)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        request.order_id,
                        request.material_code,
                        request.machine_code,
                        request.quantity,
                        request.part_length
                    )
                )

                new_id = cursor.fetchone()[0]

    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Order ID already exists"
        ) from None

    return {
        "message": "Production order saved successfully",
        "id": new_id,
        "order_id": request.order_id
    }


# ---------------------------------------
# GET ALL PRODUCTION ORDERS
# ---------------------------------------

@app.get("/orders")
def get_orders():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, order_id, material_code,
                       machine_code, quantity, part_length
                FROM production_orders
                ORDER BY id
                """
            )

            orders = cursor.fetchall()

    result = []

    for order in orders:
        result.append({
            "id": order[0],
            "order_id": order[1],
            "material_code": order[2],
            "machine_code": order[3],
            "quantity": order[4],
            "part_length": float(order[5])
        })

    return {
        "total_orders": len(result),
        "orders": result
    }


# ---------------------------------------
# MATERIAL RECOMMENDATION INPUT MODEL
# ---------------------------------------

class MaterialRecommendationRequest(BaseModel):
    max_price: float = Field(gt=0)
    max_density: float = Field(gt=0)
    machine_code: str | None = None
    thickness_mm: float | None = Field(default=None, gt=0)
    strip_width_mm: float | None = Field(default=None, gt=0)
    min_yield_strength_mpa: float | None = Field(
        default=None,
        gt=0
    )


# ---------------------------------------
# INTELLIGENT MATERIAL RECOMMENDATION API
# ---------------------------------------

@app.post("/recommend-materials")
def get_material_recommendations(
    request: MaterialRecommendationRequest
):
    try:
        results = recommend_materials(
            max_price=request.max_price,
            max_density=request.max_density,
            machine_code=request.machine_code,
            thickness_mm=request.thickness_mm,
            strip_width_mm=request.strip_width_mm,
            min_yield_strength_mpa=request.min_yield_strength_mpa
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    return {
        "message": "SmartRoll Material Recommendations",
        "total_matches": len(results),
        "recommendations": results
    }


# ---------------------------------------
# COIL OPTIMIZATION INPUT MODEL
# ---------------------------------------

class CoilOptimizationRequest(BaseModel):
    required_weight: float = Field(
        gt=0,
        description="Total required material weight in kg"
    )

    price_per_kg: float = Field(
        ge=0,
        description="Material price per kilogram"
    )


# ---------------------------------------
# INTELLIGENT COIL OPTIMIZATION API
# ---------------------------------------

@app.post("/optimize-coils")
def optimize_coil_selection(
    request: CoilOptimizationRequest
):
    try:
        result = optimize_coils(
            required_weight=request.required_weight,
            price_per_kg=request.price_per_kg
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    return {
        "message": "SmartRoll Coil Optimization Successful",
        "result": result
    }


# ---------------------------------------
# PRODUCTION PLANNING INPUT MODEL
# ---------------------------------------

class ProductionPlanningRequest(BaseModel):
    quantity: int = Field(gt=0)
    part_length_m: float = Field(gt=0)
    strip_width_mm: float = Field(gt=0)
    thickness_mm: float = Field(gt=0)
    density: float = Field(gt=0)
    price_per_kg: float = Field(ge=0)
    production_speed_m_min: float = Field(gt=0)
    setup_time_min: float = Field(default=30, ge=0)
    waste_percentage: float = Field(default=5, ge=0, lt=100)


# ---------------------------------------
# SHARED PRODUCTION PLAN CALCULATION
# ---------------------------------------

def calculate_production_plan(request: ProductionPlanningRequest):
    try:
        return plan_production(
            quantity=request.quantity,
            part_length_m=request.part_length_m,
            strip_width_mm=request.strip_width_mm,
            thickness_mm=request.thickness_mm,
            density=request.density,
            price_per_kg=request.price_per_kg,
            production_speed_m_min=request.production_speed_m_min,
            setup_time_min=request.setup_time_min,
            waste_percentage=request.waste_percentage
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error


# ---------------------------------------
# PRODUCTION PLANNING API
# ---------------------------------------

@app.post("/plan-production")
def create_production_plan(
    request: ProductionPlanningRequest
):
    result = calculate_production_plan(request)

    return {
        "message": "SmartRoll Production Plan Generated",
        "result": result
    }


# ---------------------------------------
# DOWNLOAD PRODUCTION PLANNING PDF
# ---------------------------------------

@app.post("/production-report")
def download_production_report(
    request: ProductionPlanningRequest
):
    plan = calculate_production_plan(request)

    pdf_bytes = generate_production_report(plan)

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                'attachment; filename="SmartRoll_Production_Report.pdf"'
        }
    )
