"""
Lab Interpretation Engine
==========================
Core rules-based engine for interpreting lab results.

COMPLIANCE PRINCIPLES:
- All logic is deterministic and auditable
- No probabilistic AI models used
- Template-based explanations only
- Safety classifications are conservative
- Critical results are flagged with urgency

PHASE 1 LIMITATIONS:
- Adults only (age >= 18)
- No AI/ML models
- No diagnosis or treatment advice
"""

from typing import Dict, List, Any, Optional
from enum import Enum


# SAFETY CONSTANTS - Critical result messaging
CRITICAL_EXPLANATION = "This result is outside the safe range and requires immediate medical attention."
CRITICAL_WHY_IT_MATTERS = "Values at this level may indicate a serious medical condition."
CRITICAL_NEXT_STEPS = "Seek urgent medical attention immediately. Contact your healthcare provider or go to the nearest emergency facility."

# COMPLIANCE CONSTANT - Medical disclaimer
MEDICAL_DISCLAIMER = (
    "This information is for educational purposes only and does not replace "
    "professional medical advice, diagnosis, or treatment. Always consult a "
    "qualified healthcare provider with questions about your health or lab results."
)

# AGE VALIDATION CONSTANTS
MIN_SUPPORTED_AGE = 18
PEDIATRIC_ERROR_MESSAGE = "Pediatric lab interpretation is not supported in Phase 1. This system is designed for adult patients only (age 18+)."


class Status(str, Enum):
    """Value status relative to reference range."""
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class Severity(str, Enum):
    """Clinical severity classification."""
    NORMAL = "NORMAL"
    BORDERLINE = "BORDERLINE"
    ABNORMAL = "ABNORMAL"
    CRITICAL = "CRITICAL"


class LabInterpretationEngine:
    """
    Rules-based engine for lab result interpretation.
    
    This engine:
    1. Classifies results against reference ranges
    2. Applies critical threshold logic
    3. Generates patient-friendly explanations
    4. Maintains audit trail through structured output
    """
    
    def __init__(self, test_registry: Dict[str, Any]):
        """
        Initialize the interpretation engine.
        
        Args:
            test_registry: Dictionary of test definitions with ranges and templates
        """
        self.test_registry = test_registry
    
    def interpret_result(
        self,
        test_code: str,
        value: float,
        patient_sex: str,
        patient_age: int
    ) -> Dict[str, Any]:
        """
        Interpret a single lab result using deterministic, rules-based logic.
        
        PHASE 1 SAFETY LOGIC:
        1. Validate patient age (adults only: age >= 18)
        2. Check critical thresholds FIRST (highest priority)
        3. For CRITICAL results: use restricted safety messaging only
        4. For non-critical: check borderline ranges if applicable
        5. Check normal reference ranges
        6. Classify severity conservatively
        
        CRITICAL RESULT RESTRICTION:
        When severity = CRITICAL, detailed explanations are NOT returned.
        Only fixed, safety-first language is used to ensure urgent action.
        
        Args:
            test_code: Standardized test code (e.g., 'HB', 'FBG')
            value: Numeric test result
            patient_sex: Patient biological sex ('male' or 'female')
            patient_age: Patient age in years (must be >= 18)
        
        Returns:
            Structured interpretation with status, severity, and explanations
            
        Raises:
            ValueError: If patient age < 18 (pediatric not supported in Phase 1)
        """
        # PHASE 1 SAFETY GUARDRAIL: Adults only
        # CRITICAL: Do not interpret pediatric results
        if patient_age < MIN_SUPPORTED_AGE:
            raise ValueError(PEDIATRIC_ERROR_MESSAGE)
        
        # Get test definition
        test_def = self.test_registry[test_code]
        
        # Step 1: Determine reference range (sex-specific if applicable)
        reference_range = self._get_reference_range(test_def, patient_sex)
        
        # Step 2: Check critical thresholds FIRST (safety priority)
        is_critical, critical_direction = self._check_critical_thresholds(
            value, test_def
        )
        
        # Step 3: Determine status (LOW, NORMAL, HIGH)
        status = self._determine_status(value, reference_range)
        
        # Step 4: Determine severity (NORMAL, BORDERLINE, ABNORMAL, CRITICAL)
        severity = self._determine_severity(
            value,
            reference_range,
            test_def,
            is_critical
        )
        
        # Step 5: Format reference range for display
        ref_range_str = self._format_reference_range(
            reference_range, test_def["unit"]
        )
        
        # Step 6: Get appropriate explanations
        # CRITICAL SAFETY RESTRICTION: Use fixed messaging for critical results
        if severity == Severity.CRITICAL:
            # SAFETY DECISION: Critical results get minimal, action-oriented text only
            # This prevents false reassurance and ensures urgent action
            # Placeholder for structured logging: would log critical result here
            explanation = CRITICAL_EXPLANATION
            why_it_matters = CRITICAL_WHY_IT_MATTERS
            next_steps = CRITICAL_NEXT_STEPS
        else:
            # Non-critical results use template-based explanations
            explanation_key = self._get_explanation_key(
                status, severity, critical_direction
            )
            explanations = test_def["interpretations"][explanation_key]
            explanation = explanations["explanation"]
            why_it_matters = explanations["why_it_matters"]
            next_steps = explanations["next_steps"]
        
        # Step 7: Build structured output
        return {
            "test_code": test_code,
            "test_name": test_def["name"],
            "value": value,
            "unit": test_def["unit"],
            "status": status.value,
            "severity": severity.value,
            "reference_range": ref_range_str,
            "explanation": explanation,
            "why_it_matters": why_it_matters,
            "next_steps": next_steps
        }
    
    def _get_reference_range(
        self,
        test_def: Dict[str, Any],
        patient_sex: str
    ) -> Dict[str, float]:
        """
        Get appropriate reference range based on patient sex.
        
        LOGIC:
        - If test is sex-specific, use sex-appropriate range
        - Otherwise, use default range
        - This ensures clinical accuracy for sex-dimorphic tests
        """
        if test_def.get("sex_specific", False):
            return test_def["reference_ranges"][patient_sex]
        else:
            return test_def["reference_ranges"]["default"]
    
    def _check_critical_thresholds(
        self,
        value: float,
        test_def: Dict[str, Any]
    ) -> tuple[bool, Optional[str]]:
        """
        Check if value exceeds critical thresholds.
        
        SAFETY PRIORITY:
        Critical thresholds are checked BEFORE normal ranges.
        This ensures urgent situations are flagged immediately.
        
        Returns:
            (is_critical, direction) where direction is 'low', 'high', or None
        """
        critical_low = test_def["critical_thresholds"].get("critical_low")
        critical_high = test_def["critical_thresholds"].get("critical_high")
        
        # Check critical low
        if critical_low is not None and value <= critical_low:
            return (True, "low")
        
        # Check critical high
        if critical_high is not None and value >= critical_high:
            return (True, "high")
        
        return (False, None)
    
    def _determine_status(
        self,
        value: float,
        reference_range: Dict[str, float]
    ) -> Status:
        """
        Determine if value is LOW, NORMAL, or HIGH.
        
        CLASSIFICATION LOGIC:
        - Below low threshold → LOW
        - Between low and high → NORMAL
        - Above high threshold → HIGH
        """
        if value < reference_range["low"]:
            return Status.LOW
        elif value <= reference_range["high"]:
            return Status.NORMAL
        else:
            return Status.HIGH
    
    def _determine_severity(
        self,
        value: float,
        reference_range: Dict[str, float],
        test_def: Dict[str, Any],
        is_critical: bool
    ) -> Severity:
        """
        Determine severity classification.
        
        SEVERITY HIERARCHY (highest to lowest priority):
        1. CRITICAL - exceeds critical thresholds (life-threatening)
        2. BORDERLINE - in borderline range (if defined)
        3. ABNORMAL - outside normal range but not critical
        4. NORMAL - within normal range
        
        SAFETY LOGIC:
        - Critical values ALWAYS get CRITICAL severity
        - Borderline ranges are only checked for specific tests (e.g., glucose, cholesterol)
        - This conservative approach ensures patient safety
        """
        # Priority 1: Critical thresholds
        if is_critical:
            return Severity.CRITICAL
        
        # Priority 2: Check for borderline ranges (specific tests only)
        borderline_ranges = test_def.get("borderline_ranges", {})
        if borderline_ranges:
            borderline_range = borderline_ranges.get("default", borderline_ranges.get("male"))
            if borderline_range:
                # Check if value falls in borderline range
                # Borderline is typically ABOVE normal high but BELOW definitely abnormal
                if (value > reference_range["high"] and 
                    value >= borderline_range["low"] and 
                    value <= borderline_range["high"]):
                    return Severity.BORDERLINE
        
        # Priority 3: Abnormal (outside normal range)
        if value < reference_range["low"] or value > reference_range["high"]:
            return Severity.ABNORMAL
        
        # Priority 4: Normal
        return Severity.NORMAL
    
    def _get_explanation_key(
        self,
        status: Status,
        severity: Severity,
        critical_direction: Optional[str]
    ) -> str:
        """
        Determine which explanation template to use.
        
        TEMPLATE SELECTION LOGIC:
        - Critical results use critical-specific templates
        - Borderline results use borderline template
        - Otherwise use status-based template (low/normal/high)
        """
        # Critical results have priority
        if severity == Severity.CRITICAL:
            if critical_direction == "low":
                return "critical_low"
            else:
                return "critical_high"
        
        # Borderline has its own template
        if severity == Severity.BORDERLINE:
            return "borderline"
        
        # Standard templates based on status
        if status == Status.LOW:
            return "low"
        elif status == Status.HIGH:
            return "high"
        else:
            return "normal"
    
    def _format_reference_range(
        self,
        reference_range: Dict[str, float],
        unit: str
    ) -> str:
        """
        Format reference range for patient display.
        
        Example outputs:
        - "12.0 - 15.5 g/dL"
        - "70 - 99 mg/dL"
        """
        low = reference_range["low"]
        high = reference_range["high"]
        
        # Format numbers appropriately (remove unnecessary decimals)
        if low == int(low):
            low_str = str(int(low))
        else:
            low_str = f"{low:.1f}"
        
        if high == int(high):
            high_str = str(int(high))
        else:
            high_str = f"{high:.1f}"
        
        return f"{low_str} - {high_str} {unit}"
    
    def generate_summary(
        self,
        interpretations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate overall summary of all test results.
        
        SUMMARY LOGIC:
        - overall_flag takes the HIGHEST severity level found
        - critical_alert is True if ANY result is CRITICAL
        - Counts are provided for transparency
        
        SEVERITY PRIORITY (highest to lowest):
        CRITICAL > ABNORMAL > BORDERLINE > NORMAL
        """
        # Count by severity
        severity_counts = {
            "CRITICAL": 0,
            "ABNORMAL": 0,
            "BORDERLINE": 0,
            "NORMAL": 0
        }
        
        for interp in interpretations:
            severity = interp["severity"]
            severity_counts[severity] += 1
        
        # Determine overall flag (highest severity wins)
        # COMPLIANCE: Conservative approach - alert to worst finding
        if severity_counts["CRITICAL"] > 0:
            overall_flag = "CRITICAL"
            critical_alert = True
        elif severity_counts["ABNORMAL"] > 0:
            overall_flag = "ABNORMAL"
            critical_alert = False
        elif severity_counts["BORDERLINE"] > 0:
            overall_flag = "BORDERLINE"
            critical_alert = False
        else:
            overall_flag = "NORMAL"
            critical_alert = False
        
        return {
            "overall_flag": overall_flag,
            "critical_alert": critical_alert,
            "critical_count": severity_counts["CRITICAL"],
            "abnormal_count": severity_counts["ABNORMAL"],
            "borderline_count": severity_counts["BORDERLINE"],
            "normal_count": severity_counts["NORMAL"]
        }
