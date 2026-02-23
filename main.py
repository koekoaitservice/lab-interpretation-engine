"""
Lab Result Interpretation Engine
=================================
A compliance-safe, rules-based system for patient-facing lab result explanations.

CRITICAL COMPLIANCE NOTES:
- This is NOT a diagnostic system
- No disease diagnosis is provided
- No treatment recommendations are made
- All logic is deterministic and auditable
- Output is educational only

PHASE 1 LIMITATIONS:
- Adults only (age >= 18)
- No AI/ML models
- No OCR, image upload, or PDF parsing
- No diagnosis or treatment advice
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal, Dict
from enum import Enum

from test_registry import TEST_REGISTRY, SUPPORTED_UNIT_CONVERSIONS, convert_unit
from interpretation_engine import (
    LabInterpretationEngine, 
    MEDICAL_DISCLAIMER,
    MIN_SUPPORTED_AGE,
    PEDIATRIC_ERROR_MESSAGE
)


app = FastAPI(
    title="Lab Result Interpretation Engine",
    description="Rules-based lab result interpretation for patient education",
    version="1.0.0"
)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class PatientInfo(BaseModel):
    """Patient demographic information required for interpretation."""
    age: int = Field(..., ge=0, le=120, description="Patient age in years")
    sex: Literal["male", "female"] = Field(..., description="Biological sex")

    @validator('age')
    def validate_age(cls, v):
        """
        PHASE 1 SAFETY GUARDRAIL: Adults only (age >= 18)
        
        Pediatric lab interpretation requires different reference ranges
        and is not supported in Phase 1 to ensure patient safety.
        """
        if v < MIN_SUPPORTED_AGE:
            raise ValueError(PEDIATRIC_ERROR_MESSAGE)
        if v > 120:
            raise ValueError("Age must be 120 or less")
        return v


class LabResult(BaseModel):
    """Individual lab test result."""
    test_code: str = Field(..., description="Standardized test code (e.g., 'HB', 'FBG')")
    value: float = Field(..., description="Numeric test result value")
    unit: str = Field(..., description="Unit of measurement (e.g., 'g/dL', 'mg/dL')")

    @validator('test_code')
    def validate_test_code(cls, v):
        # Convert to uppercase for consistency
        return v.upper()


class InterpretationRequest(BaseModel):
    """Complete interpretation request payload."""
    patient: PatientInfo
    results: List[LabResult] = Field(..., min_items=1, description="List of lab results to interpret")


class InterpretationOutput(BaseModel):
    """Interpretation for a single test result."""
    test_code: str
    test_name: str
    value: float
    unit: str
    status: Literal["LOW", "NORMAL", "HIGH"]
    severity: Literal["NORMAL", "BORDERLINE", "ABNORMAL", "CRITICAL"]
    reference_range: str
    explanation: str
    why_it_matters: str
    next_steps: str


class SummaryOutput(BaseModel):
    """Overall summary of all test results."""
    overall_flag: Literal["NORMAL", "BORDERLINE", "ABNORMAL", "CRITICAL"]
    critical_alert: bool
    critical_count: int
    abnormal_count: int
    borderline_count: int
    normal_count: int


class WarningsOutput(BaseModel):
    """Warnings about unsupported or problematic inputs."""
    unsupported_tests: List[str] = Field(
        default_factory=list,
        description="Test codes that are not supported in Phase 1"
    )


class InterpretationResponse(BaseModel):
    """Complete API response."""
    summary: SummaryOutput
    interpretations: List[InterpretationOutput]
    warnings: Optional[WarningsOutput] = None
    disclaimer: str


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "service": "Lab Result Interpretation Engine",
        "status": "operational",
        "version": "1.0.0",
        "compliance": "Educational use only - not for diagnosis"
    }


@app.get("/tests")
def list_supported_tests():
    """List all supported test codes and their details."""
    tests = []
    for code, definition in TEST_REGISTRY.items():
        tests.append({
            "code": code,
            "name": definition["name"],
            "category": definition["category"],
            "unit": definition["unit"],
            "sex_specific": definition.get("sex_specific", False)
        })
    return {"supported_tests": tests, "count": len(tests)}


@app.post("/interpret", response_model=InterpretationResponse)
def interpret_lab_results(request: InterpretationRequest):
    """
    Interpret lab results and provide patient-facing explanations.
    
    PHASE 1 COMPLIANCE SAFEGUARDS:
    - Validates all inputs strictly (age >= 18 required)
    - Uses only deterministic, rules-based logic
    - Tracks unsupported test codes (returned in warnings)
    - Handles unit conversion for explicitly supported alternatives
    - Provides educational information only
    - Includes medical disclaimer
    - Flags critical results appropriately
    
    CRITICAL RESULT HANDLING:
    When a result is CRITICAL, only minimal safety-first messaging is returned.
    Detailed explanations are withheld to ensure urgent medical action.
    """
    try:
        # Initialize interpretation engine
        engine = LabInterpretationEngine(TEST_REGISTRY)
        
        # Process all results
        interpretations = []
        unsupported_tests = []
        
        for result in request.results:
            # PHASE 1 RESTRICTION: Track unsupported test codes
            # Do not silently ignore - must inform user
            if result.test_code not in TEST_REGISTRY:
                unsupported_tests.append(result.test_code)
                # Placeholder for structured logging: would log unsupported test here
                continue
            
            # Get expected unit for this test
            expected_unit = TEST_REGISTRY[result.test_code]["unit"]
            converted_value = result.value
            
            # PHASE 1 UNIT HANDLING: Convert alternative units if supported
            if result.unit != expected_unit:
                try:
                    # Attempt deterministic unit conversion
                    converted_value = convert_unit(
                        test_code=result.test_code,
                        value=result.value,
                        from_unit=result.unit,
                        to_unit=expected_unit
                    )
                    # Placeholder for structured logging: would log unit conversion here
                except ValueError as e:
                    # Unit conversion not supported - reject with clear error
                    raise HTTPException(
                        status_code=400,
                        detail=str(e)
                    )
            
            # Interpret the result using converted value
            # SAFETY: This will raise ValueError if patient age < 18
            interpretation = engine.interpret_result(
                test_code=result.test_code,
                value=converted_value,
                patient_sex=request.patient.sex,
                patient_age=request.patient.age
            )
            
            interpretations.append(interpretation)
        
        # Generate summary (only from interpreted results)
        if interpretations:
            summary = engine.generate_summary(interpretations)
        else:
            # All tests were unsupported - return empty summary
            summary = {
                "overall_flag": "NORMAL",
                "critical_alert": False,
                "critical_count": 0,
                "abnormal_count": 0,
                "borderline_count": 0,
                "normal_count": 0
            }
        
        # Build warnings object if there are unsupported tests
        warnings = None
        if unsupported_tests:
            warnings = WarningsOutput(unsupported_tests=unsupported_tests)
        
        # Use constant for disclaimer (compliance requirement)
        return InterpretationResponse(
            summary=summary,
            interpretations=interpretations,
            warnings=warnings,
            disclaimer=MEDICAL_DISCLAIMER
        )
    
    except ValueError as e:
        # Handle age validation and other value errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Placeholder for structured logging: would log unexpected error here
        raise HTTPException(
            status_code=500,
            detail="An error occurred processing your request. Please try again."
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global error handler for compliance logging."""
    # In production: log to monitoring system
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Unable to process request. Please contact support."
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
