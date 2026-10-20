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

