"""
Lab Test Registry
=================
Centralized registry of all supported lab tests with reference ranges,
critical thresholds, and interpretation templates.

MEDICAL ACCURACY NOTES:
- Reference ranges are based on standard clinical guidelines
- Values may vary slightly between laboratories
- Critical thresholds are conservative for safety
- Sex-specific ranges are implemented where clinically relevant

PHASE 1 UNIT HANDLING:
- Primary units are defined for each test
- Limited alternative units are supported with deterministic conversion
- Only explicitly defined conversions are allowed (no generic conversion)
"""

# UNIT CONVERSION REGISTRY
# SAFETY: Only explicitly defined, deterministic conversions are allowed
# Format: {test_code: {alternative_unit: (conversion_factor, conversion_type)}}
SUPPORTED_UNIT_CONVERSIONS = {
    "FBG": {
        # Fasting Blood Glucose: mg/dL (primary) <-> mmol/L (alternative)
        "mmol/L": (18.0, "multiply")  # mmol/L * 18 = mg/dL
    },
    "HBA1C": {
        # HbA1c: % (primary) <-> mmol/mol (alternative)  
        "mmol/mol": (0.0915, "mmol_to_percent")  # Special conversion for HbA1c
    },
    "TCHOL": {
        # Total Cholesterol: mg/dL (primary) <-> mmol/L (alternative)
        "mmol/L": (38.67, "multiply")  # mmol/L * 38.67 = mg/dL
    },
    "LDL": {
        # LDL Cholesterol: mg/dL (primary) <-> mmol/L (alternative)
        "mmol/L": (38.67, "multiply")
    },
    "HDL": {
        # HDL Cholesterol: mg/dL (primary) <-> mmol/L (alternative)
        "mmol/L": (38.67, "multiply")
    },
    "TRIG": {
        # Triglycerides: mg/dL (primary) <-> mmol/L (alternative)
        "mmol/L": (88.57, "multiply")  # mmol/L * 88.57 = mg/dL
    },
    "CREAT": {
        # Creatinine: mg/dL (primary) <-> µmol/L (alternative)
        "µmol/L": (0.0113, "multiply"),  # µmol/L * 0.0113 = mg/dL
        "umol/L": (0.0113, "multiply")   # Alternative spelling
    },
    "UREA": {
        # Urea: mg/dL (primary) <-> mmol/L (alternative)
        "mmol/L": (2.8, "multiply")  # mmol/L * 2.8 = mg/dL
    }
}


def convert_unit(test_code: str, value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert lab test value from alternative unit to primary unit.
    
    SAFETY RULES:
    - Only explicitly defined conversions are allowed
    - All conversions are deterministic (no estimation)
    - Unknown conversions raise ValueError
    
    Args:
        test_code: Test code (e.g., 'FBG')
        value: Numeric value in from_unit
        from_unit: Unit to convert from
        to_unit: Unit to convert to (must be primary unit)
        
    Returns:
        Converted value in primary unit
        
    Raises:
        ValueError: If conversion is not supported
    """
    # Check if test supports any unit conversions
    if test_code not in SUPPORTED_UNIT_CONVERSIONS:
        raise ValueError(
            f"Unit conversion not supported for {test_code}. "
            f"Expected unit: {to_unit}, received: {from_unit}"
        )
    
    # Check if specific conversion is defined
    if from_unit not in SUPPORTED_UNIT_CONVERSIONS[test_code]:
        raise ValueError(
            f"Cannot convert {from_unit} to {to_unit} for {test_code}. "
            f"Supported units: {to_unit}, {', '.join(SUPPORTED_UNIT_CONVERSIONS[test_code].keys())}"
        )
    
    # Perform conversion
    conversion_factor, conversion_type = SUPPORTED_UNIT_CONVERSIONS[test_code][from_unit]
    
    if conversion_type == "multiply":
        # Simple multiplication conversion
        return value * conversion_factor
    elif conversion_type == "mmol_to_percent":
        # Special HbA1c conversion: mmol/mol to %
        # Formula: % = (mmol/mol * 0.0915) + 2.15
        return (value * conversion_factor) + 2.15
    else:
        raise ValueError(f"Unknown conversion type: {conversion_type}")


# ============================================================================
# TEST REGISTRY
# ============================================================================

TEST_REGISTRY = {
    
    # ========================================================================
    # HEMATOLOGY
    # ========================================================================
    
    "HB": {
        "name": "Hemoglobin",
        "category": "Hematology",
        "unit": "g/dL",
        "sex_specific": True,
        "reference_ranges": {
            "male": {"low": 13.5, "high": 17.5},
            "female": {"low": 12.0, "high": 15.5}
        },
        "critical_thresholds": {
            "critical_low": 7.0,    # Severe anemia - urgent
            "critical_high": 20.0   # Severe polycythemia - urgent
        },
        "interpretations": {
            "low": {
                "explanation": "Hemoglobin is lower than the typical range. Hemoglobin is the protein in red blood cells that carries oxygen throughout your body.",
                "why_it_matters": "Lower levels may be associated with tiredness, weakness, or shortness of breath.",
                "next_steps": "Consider discussing this result with a healthcare professional to understand possible causes."
            },
            "normal": {
                "explanation": "Hemoglobin is within the typical healthy range. This protein helps carry oxygen in your blood.",
                "why_it_matters": "Normal hemoglobin suggests your blood is carrying oxygen effectively.",
                "next_steps": "No immediate action needed for this test."
            },
            "high": {
                "explanation": "Hemoglobin is higher than the typical range.",
                "why_it_matters": "Elevated levels may warrant further investigation.",
                "next_steps": "Consider discussing this result with a healthcare professional."
            },
            "critical_low": {
                "explanation": "Hemoglobin is significantly below normal range.",
                "why_it_matters": "This requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            },
            "critical_high": {
                "explanation": "Hemoglobin is significantly above normal range.",
                "why_it_matters": "This requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    },
    
    "PCV": {
        "name": "Packed Cell Volume (Hematocrit)",
        "category": "Hematology",
        "unit": "%",
        "sex_specific": True,
        "reference_ranges": {
            "male": {"low": 40.0, "high": 54.0},
            "female": {"low": 36.0, "high": 48.0}
        },
        "critical_thresholds": {
            "critical_low": 20.0,
            "critical_high": 60.0
        },
        "interpretations": {
            "low": {
                "explanation": "Packed Cell Volume (PCV) is lower than the typical range. PCV measures the percentage of your blood made up of red blood cells.",
                "why_it_matters": "Lower values may indicate reduced oxygen-carrying capacity.",
                "next_steps": "Consider discussing this result with a healthcare professional."
            },
            "normal": {
                "explanation": "Packed Cell Volume (PCV) is within the typical healthy range.",
                "why_it_matters": "Normal PCV suggests a healthy proportion of red blood cells in your blood.",
                "next_steps": "No immediate action needed for this test."
            },
            "high": {
                "explanation": "Packed Cell Volume (PCV) is higher than the typical range.",
                "why_it_matters": "Elevated values may warrant further evaluation.",
                "next_steps": "Consider discussing this result with a healthcare professional."
            },
            "critical_low": {
                "explanation": "Packed Cell Volume is significantly below normal range.",
                "why_it_matters": "This requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            },
            "critical_high": {
                "explanation": "Packed Cell Volume is significantly above normal range.",
                "why_it_matters": "This requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    },
    
    "WBC": {
        "name": "White Blood Cell Count",
        "category": "Hematology",
        "unit": "×10³/µL",
        "sex_specific": False,
        "reference_ranges": {
            "default": {"low": 4.0, "high": 11.0}
        },
        "critical_thresholds": {
            "critical_low": 2.0,    # Severe leukopenia
            "critical_high": 30.0   # Severe leukocytosis
        },
        "interpretations": {
            "low": {
                "explanation": "White Blood Cell count is lower than the typical range. White blood cells help your body fight infections.",
                "why_it_matters": "Lower counts may affect your body's ability to fight infections.",
                "next_steps": "Consider discussing this result with a healthcare professional."
            },
            "normal": {
                "explanation": "White Blood Cell count is within the typical healthy range.",
                "why_it_matters": "Normal WBC count suggests your immune system has an appropriate number of infection-fighting cells.",
                "next_steps": "No immediate action needed for this test."
            },
            "high": {
                "explanation": "White Blood Cell count is higher than the typical range.",
                "why_it_matters": "Elevated counts may indicate your body is responding to various conditions.",
                "next_steps": "Consider discussing this result with a healthcare professional."
            },
            "critical_low": {
                "explanation": "White Blood Cell count is significantly below normal range.",
                "why_it_matters": "This requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            },
            "critical_high": {
                "explanation": "White Blood Cell count is significantly above normal range.",
                "why_it_matters": "This requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    },
    
    "PLT": {
        "name": "Platelet Count",
        "category": "Hematology",
        "unit": "×10³/µL",
        "sex_specific": False,
        "reference_ranges": {
            "default": {"low": 150.0, "high": 400.0}
        },
        "critical_thresholds": {
            "critical_low": 50.0,   # Risk of bleeding
            "critical_high": 1000.0  # Risk of clotting
        },
        "interpretations": {
            "low": {
                "explanation": "Platelet count is lower than the typical range. Platelets help your blood clot.",
                "why_it_matters": "Lower platelet counts may affect blood clotting ability.",
                "next_steps": "Consider discussing this result with a healthcare professional."
            },
            "normal": {
                "explanation": "Platelet count is within the typical healthy range.",
                "why_it_matters": "Normal platelet count suggests adequate blood clotting function.",
                "next_steps": "No immediate action needed for this test."
            },
            "high": {
                "explanation": "Platelet count is higher than the typical range.",
                "why_it_matters": "Elevated platelet counts may warrant further evaluation.",
                "next_steps": "Consider discussing this result with a healthcare professional."
            },
            "critical_low": {
                "explanation": "Platelet count is significantly below normal range.",
                "why_it_matters": "This requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            },
            "critical_high": {
                "explanation": "Platelet count is significantly above normal range.",
                "why_it_matters": "This requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    },
    
    # ========================================================================
    # METABOLIC
    # ========================================================================
    
    "FBG": {
        "name": "Fasting Blood Glucose",
        "category": "Metabolic",
        "unit": "mg/dL",
        "sex_specific": False,
        "reference_ranges": {
            "default": {"low": 70.0, "high": 99.0}  # Normal fasting
        },
        "borderline_ranges": {
            "default": {"low": 100.0, "high": 125.0}  # Prediabetes range
        },
        "critical_thresholds": {
            "critical_low": 54.0,   # Severe hypoglycemia
            "critical_high": 400.0  # Severe hyperglycemia
        },
        "interpretations": {
            "low": {
                "explanation": "Fasting blood glucose is lower than the typical range. Glucose (sugar) is your body's main source of energy.",
                "why_it_matters": "Low blood sugar may cause symptoms like shakiness, sweating, or confusion.",
                "next_steps": "If you experience symptoms, speak with a healthcare professional about blood sugar management."
            },
            "normal": {
                "explanation": "Fasting blood glucose is within the typical healthy range.",
                "why_it_matters": "Normal fasting glucose suggests your body is managing blood sugar well.",
                "next_steps": "Maintain healthy lifestyle habits. No immediate action needed for this test."
            },
            "borderline": {
                "explanation": "Fasting blood glucose is in the borderline range (100-125 mg/dL).",
                "why_it_matters": "This range may indicate prediabetes, which means higher risk for developing diabetes.",
                "next_steps": "Discuss this result with a healthcare professional. Lifestyle changes may be beneficial."
            },
            "high": {
                "explanation": "Fasting blood glucose is higher than the typical range.",
                "why_it_matters": "Elevated fasting glucose may indicate diabetes and requires professional evaluation.",
                "next_steps": "Consult with a healthcare professional for further assessment and guidance."
            },
            "critical_low": {
                "explanation": "Blood glucose is significantly below normal range.",
                "why_it_matters": "This requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            },
            "critical_high": {
                "explanation": "Blood glucose is significantly above normal range.",
                "why_it_matters": "This requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    },
    
    "HBA1C": {
        "name": "Hemoglobin A1c",
        "category": "Metabolic",
        "unit": "%",
        "sex_specific": False,
        "reference_ranges": {
            "default": {"low": 4.0, "high": 5.6}  # Normal
        },
        "borderline_ranges": {
            "default": {"low": 5.7, "high": 6.4}  # Prediabetes range
        },
        "critical_thresholds": {
            "critical_low": None,  # No critical low for HbA1c
            "critical_high": 10.0   # Very poor control
        },
        "interpretations": {
            "low": {
                "explanation": "HbA1c is lower than typical. This test measures your average blood sugar over the past 2-3 months.",
                "why_it_matters": "Very low values are uncommon and may warrant discussion.",
                "next_steps": "If you have questions about this result, speak with a healthcare professional."
            },
            "normal": {
                "explanation": "HbA1c is within the typical healthy range. This test reflects your average blood sugar over the past 2-3 months.",
                "why_it_matters": "Normal HbA1c suggests good long-term blood sugar control.",
                "next_steps": "Continue healthy lifestyle habits. No immediate action needed for this test."
            },
            "borderline": {
                "explanation": "HbA1c is in the borderline range (5.7-6.4%).",
                "why_it_matters": "This range may indicate prediabetes, meaning higher risk for developing diabetes.",
                "next_steps": "Discuss this result with a healthcare professional. Lifestyle modifications may help."
            },
            "high": {
                "explanation": "HbA1c is higher than the typical range.",
                "why_it_matters": "Elevated HbA1c indicates higher average blood sugar over recent months.",
                "next_steps": "Consult with a healthcare professional for evaluation and blood sugar management strategies."
            },
            "critical_low": {
                "explanation": "HbA1c is unusually low.",
                "why_it_matters": "This may require further evaluation.",
                "next_steps": "Discuss this result with a healthcare professional."
            },
            "critical_high": {
                "explanation": "HbA1c is significantly above normal range.",
                "why_it_matters": "This requires prompt medical attention for blood sugar management.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    },
    
    # ========================================================================
    # RENAL (KIDNEY)
    # ========================================================================
    
    "CREAT": {
        "name": "Creatinine",
        "category": "Renal",
        "unit": "mg/dL",
        "sex_specific": True,
        "reference_ranges": {
            "male": {"low": 0.7, "high": 1.3},
            "female": {"low": 0.6, "high": 1.1}
        },
        "critical_thresholds": {
            "critical_low": None,  # Low creatinine rarely critical
            "critical_high": 5.0   # Severe kidney impairment
        },
        "interpretations": {
            "low": {
                "explanation": "Creatinine is lower than the typical range. Creatinine is a waste product filtered by your kidneys.",
                "why_it_matters": "Lower levels are usually not concerning but may relate to muscle mass.",
                "next_steps": "If you have questions about this result, speak with a healthcare professional."
            },
            "normal": {
                "explanation": "Creatinine is within the typical healthy range. Creatinine is a waste product your kidneys filter from your blood.",
                "why_it_matters": "Normal creatinine suggests your kidneys are filtering waste effectively.",
                "next_steps": "No immediate action needed for this test."
            },
            "high": {
                "explanation": "Creatinine is higher than the typical range.",
                "why_it_matters": "Elevated creatinine may indicate reduced kidney function and requires evaluation.",
                "next_steps": "Consult with a healthcare professional for kidney function assessment."
            },
            "critical_low": {
                "explanation": "Creatinine is unusually low.",
                "why_it_matters": "This may warrant discussion with a healthcare provider.",
                "next_steps": "Speak with a healthcare professional if you have concerns."
            },
            "critical_high": {
                "explanation": "Creatinine is significantly above normal range.",
                "why_it_matters": "This indicates severely reduced kidney function and requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    },
    
    "UREA": {
        "name": "Blood Urea Nitrogen (BUN)",
        "category": "Renal",
        "unit": "mg/dL",
        "sex_specific": False,
        "reference_ranges": {
            "default": {"low": 7.0, "high": 20.0}
        },
        "critical_thresholds": {
            "critical_low": None,  # Low BUN rarely critical
            "critical_high": 100.0  # Severe kidney impairment
        },
        "interpretations": {
            "low": {
                "explanation": "Blood urea is lower than the typical range. Urea is a waste product processed by your kidneys.",
                "why_it_matters": "Low levels are usually not concerning but may relate to diet or hydration.",
                "next_steps": "If you have questions about this result, speak with a healthcare professional."
            },
            "normal": {
                "explanation": "Blood urea is within the typical healthy range. Urea is a waste product your kidneys filter from your blood.",
                "why_it_matters": "Normal urea suggests your kidneys are processing waste appropriately.",
                "next_steps": "No immediate action needed for this test."
            },
            "high": {
                "explanation": "Blood urea is higher than the typical range.",
                "why_it_matters": "Elevated urea may indicate kidney function changes, dehydration, or other factors requiring evaluation.",
                "next_steps": "Consult with a healthcare professional for further assessment."
            },
            "critical_low": {
                "explanation": "Blood urea is unusually low.",
                "why_it_matters": "This may warrant discussion with a healthcare provider.",
                "next_steps": "Speak with a healthcare professional if you have concerns."
            },
            "critical_high": {
                "explanation": "Blood urea is significantly above normal range.",
                "why_it_matters": "This requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    },
    
    # ========================================================================
    # LIVER
    # ========================================================================
    
    "ALT": {
        "name": "Alanine Aminotransferase (ALT)",
        "category": "Liver",
        "unit": "U/L",
        "sex_specific": False,
        "reference_ranges": {
            "default": {"low": 7.0, "high": 56.0}
        },
        "critical_thresholds": {
            "critical_low": None,  # Low ALT not concerning
            "critical_high": 1000.0  # Severe liver injury
        },
        "interpretations": {
            "low": {
                "explanation": "ALT is lower than the typical range. ALT is an enzyme found mainly in the liver.",
                "why_it_matters": "Low ALT is generally not concerning.",
                "next_steps": "No action typically needed for low ALT."
            },
            "normal": {
                "explanation": "ALT is within the typical healthy range. ALT is an enzyme that helps assess liver health.",
                "why_it_matters": "Normal ALT suggests your liver is functioning well.",
                "next_steps": "No immediate action needed for this test."
            },
            "high": {
                "explanation": "ALT is higher than the typical range.",
                "why_it_matters": "Elevated ALT may indicate liver inflammation or injury and requires evaluation.",
                "next_steps": "Consult with a healthcare professional for liver function assessment."
            },
            "critical_low": {
                "explanation": "ALT is unusually low.",
                "why_it_matters": "This is typically not concerning.",
                "next_steps": "No immediate action typically needed."
            },
            "critical_high": {
                "explanation": "ALT is significantly above normal range.",
                "why_it_matters": "This indicates significant liver stress and requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    },
    
    "AST": {
        "name": "Aspartate Aminotransferase (AST)",
        "category": "Liver",
        "unit": "U/L",
        "sex_specific": False,
        "reference_ranges": {
            "default": {"low": 10.0, "high": 40.0}
        },
        "critical_thresholds": {
            "critical_low": None,
            "critical_high": 1000.0
        },
        "interpretations": {
            "low": {
                "explanation": "AST is lower than the typical range. AST is an enzyme found in the liver and other tissues.",
                "why_it_matters": "Low AST is generally not concerning.",
                "next_steps": "No action typically needed for low AST."
            },
            "normal": {
                "explanation": "AST is within the typical healthy range. AST is an enzyme that helps assess liver and tissue health.",
                "why_it_matters": "Normal AST is a positive indicator of liver health.",
                "next_steps": "No immediate action needed for this test."
            },
            "high": {
                "explanation": "AST is higher than the typical range.",
                "why_it_matters": "Elevated AST may indicate liver or tissue stress and requires evaluation.",
                "next_steps": "Consult with a healthcare professional for further assessment."
            },
            "critical_low": {
                "explanation": "AST is unusually low.",
                "why_it_matters": "This is typically not concerning.",
                "next_steps": "No immediate action typically needed."
            },
            "critical_high": {
                "explanation": "AST is significantly above normal range.",
                "why_it_matters": "This requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    },
    
    "TBIL": {
        "name": "Total Bilirubin",
        "category": "Liver",
        "unit": "mg/dL",
        "sex_specific": False,
        "reference_ranges": {
            "default": {"low": 0.1, "high": 1.2}
        },
        "critical_thresholds": {
            "critical_low": None,
            "critical_high": 12.0  # Severe jaundice
        },
        "interpretations": {
            "low": {
                "explanation": "Total bilirubin is lower than the typical range. Bilirubin is a yellow pigment produced when red blood cells break down.",
                "why_it_matters": "Low bilirubin is generally not concerning.",
                "next_steps": "No action typically needed for low bilirubin."
            },
            "normal": {
                "explanation": "Total bilirubin is within the typical healthy range. Bilirubin is processed by your liver.",
                "why_it_matters": "Normal bilirubin suggests your liver is processing this substance appropriately.",
                "next_steps": "No immediate action needed for this test."
            },
            "high": {
                "explanation": "Total bilirubin is higher than the typical range.",
                "why_it_matters": "Elevated bilirubin may cause yellowing of skin or eyes and requires evaluation.",
                "next_steps": "Consult with a healthcare professional for liver function assessment."
            },
            "critical_low": {
                "explanation": "Total bilirubin is unusually low.",
                "why_it_matters": "This is typically not concerning.",
                "next_steps": "No immediate action typically needed."
            },
            "critical_high": {
                "explanation": "Total bilirubin is significantly above normal range.",
                "why_it_matters": "This requires prompt medical attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    },
    
    # ========================================================================
    # LIPIDS
    # ========================================================================
    
    "TCHOL": {
        "name": "Total Cholesterol",
        "category": "Lipids",
        "unit": "mg/dL",
        "sex_specific": False,
        "reference_ranges": {
            "default": {"low": 125.0, "high": 200.0}  # Desirable
        },
        "borderline_ranges": {
            "default": {"low": 200.0, "high": 239.0}  # Borderline high
        },
        "critical_thresholds": {
            "critical_low": None,
            "critical_high": 400.0  # Extremely high
        },
        "interpretations": {
            "low": {
                "explanation": "Total cholesterol is lower than the typical range. Cholesterol is a fatty substance in your blood.",
                "why_it_matters": "While high cholesterol is more commonly discussed, very low levels may warrant discussion.",
                "next_steps": "If you have questions about this result, speak with a healthcare professional."
            },
            "normal": {
                "explanation": "Total cholesterol is within the desirable range. Cholesterol is a fatty substance your body needs in healthy amounts.",
                "why_it_matters": "Desirable cholesterol levels support heart health.",
                "next_steps": "Maintain heart-healthy lifestyle habits. No immediate action needed for this test."
            },
            "borderline": {
                "explanation": "Total cholesterol is in the borderline high range (200-239 mg/dL).",
                "why_it_matters": "This level suggests increased cardiovascular risk and lifestyle changes may be beneficial.",
                "next_steps": "Discuss this result with a healthcare professional about heart health strategies."
            },
            "high": {
                "explanation": "Total cholesterol is higher than the desirable range.",
                "why_it_matters": "High cholesterol increases cardiovascular risk and requires professional evaluation.",
                "next_steps": "Consult with a healthcare professional about cholesterol management."
            },
            "critical_low": {
                "explanation": "Total cholesterol is unusually low.",
                "why_it_matters": "This may warrant discussion with a healthcare provider.",
                "next_steps": "Speak with a healthcare professional if you have concerns."
            },
            "critical_high": {
                "explanation": "Total cholesterol is significantly above normal range.",
                "why_it_matters": "This requires prompt medical attention for cardiovascular risk management.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    },
    
    "LDL": {
        "name": "LDL Cholesterol",
        "category": "Lipids",
        "unit": "mg/dL",
        "sex_specific": False,
        "reference_ranges": {
            "default": {"low": 0.0, "high": 100.0}  # Optimal
        },
        "borderline_ranges": {
            "default": {"low": 130.0, "high": 159.0}  # Borderline high
        },
        "critical_thresholds": {
            "critical_low": None,
            "critical_high": 250.0
        },
        "interpretations": {
            "low": {
                "explanation": "LDL cholesterol is low. LDL is often called 'bad cholesterol' because high levels can increase heart disease risk.",
                "why_it_matters": "Low LDL cholesterol is generally considered beneficial for heart health.",
                "next_steps": "Continue heart-healthy lifestyle habits."
            },
            "normal": {
                "explanation": "LDL cholesterol is at optimal levels. LDL is sometimes called 'bad cholesterol' when elevated.",
                "why_it_matters": "Optimal LDL cholesterol supports cardiovascular health.",
                "next_steps": "Maintain heart-healthy lifestyle habits. No immediate action needed for this test."
            },
            "borderline": {
                "explanation": "LDL cholesterol is in the borderline high range (130-159 mg/dL).",
                "why_it_matters": "This level suggests increased cardiovascular risk.",
                "next_steps": "Discuss this result with a healthcare professional about heart health strategies."
            },
            "high": {
                "explanation": "LDL cholesterol is higher than optimal levels.",
                "why_it_matters": "High LDL increases cardiovascular risk and may require intervention.",
                "next_steps": "Consult with a healthcare professional about LDL management strategies."
            },
            "critical_low": {
                "explanation": "LDL cholesterol is very low.",
                "why_it_matters": "Very low LDL is generally beneficial for heart health.",
                "next_steps": "Continue current health practices."
            },
            "critical_high": {
                "explanation": "LDL cholesterol is significantly above optimal range.",
                "why_it_matters": "This requires prompt medical attention for cardiovascular risk management.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    },
    
    "HDL": {
        "name": "HDL Cholesterol",
        "category": "Lipids",
        "unit": "mg/dL",
        "sex_specific": True,
        "reference_ranges": {
            "male": {"low": 40.0, "high": 200.0},  # >40 protective
            "female": {"low": 50.0, "high": 200.0}  # >50 protective
        },
        "critical_thresholds": {
            "critical_low": 20.0,  # Very high risk
            "critical_high": None   # High HDL is protective
        },
        "interpretations": {
            "low": {
                "explanation": "HDL cholesterol is lower than desired. HDL is often called 'good cholesterol' because it helps remove other cholesterol from your blood.",
                "why_it_matters": "Low HDL cholesterol increases cardiovascular risk.",
                "next_steps": "Consult with a healthcare professional about strategies to raise HDL cholesterol."
            },
            "normal": {
                "explanation": "HDL cholesterol is within the protective range. HDL is called 'good cholesterol' because it helps protect your heart.",
                "why_it_matters": "Adequate HDL cholesterol is protective for cardiovascular health.",
                "next_steps": "Maintain heart-healthy lifestyle habits. No immediate action needed for this test."
            },
            "high": {
                "explanation": "HDL cholesterol is higher than typical. HDL is the 'good cholesterol' that protects your heart.",
                "why_it_matters": "High HDL is generally considered protective for heart health.",
                "next_steps": "Continue heart-healthy lifestyle habits."
            },
            "critical_low": {
                "explanation": "HDL cholesterol is significantly below protective levels.",
                "why_it_matters": "This indicates very high cardiovascular risk and requires prompt attention.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            },
            "critical_high": {
                "explanation": "HDL cholesterol is very high.",
                "why_it_matters": "High HDL is typically protective for heart health.",
                "next_steps": "Continue current health practices."
            }
        }
    },
    
    "TRIG": {
        "name": "Triglycerides",
        "category": "Lipids",
        "unit": "mg/dL",
        "sex_specific": False,
        "reference_ranges": {
            "default": {"low": 0.0, "high": 150.0}  # Normal
        },
        "borderline_ranges": {
            "default": {"low": 150.0, "high": 199.0}  # Borderline high
        },
        "critical_thresholds": {
            "critical_low": None,
            "critical_high": 500.0  # Very high - pancreatitis risk
        },
        "interpretations": {
            "low": {
                "explanation": "Triglycerides are low. Triglycerides are a type of fat in your blood.",
                "why_it_matters": "Low triglycerides are generally not concerning and may be beneficial.",
                "next_steps": "Continue healthy lifestyle habits."
            },
            "normal": {
                "explanation": "Triglycerides are within the normal range. Triglycerides are a type of fat stored in your blood.",
                "why_it_matters": "Normal triglycerides support overall metabolic and heart health.",
                "next_steps": "Maintain heart-healthy lifestyle habits. No immediate action needed for this test."
            },
            "borderline": {
                "explanation": "Triglycerides are in the borderline high range (150-199 mg/dL).",
                "why_it_matters": "This level suggests increased cardiovascular risk and metabolic concerns.",
                "next_steps": "Discuss this result with a healthcare professional about lifestyle modifications."
            },
            "high": {
                "explanation": "Triglycerides are higher than the normal range.",
                "why_it_matters": "High triglycerides increase cardiovascular and metabolic risks.",
                "next_steps": "Consult with a healthcare professional about triglyceride management."
            },
            "critical_low": {
                "explanation": "Triglycerides are very low.",
                "why_it_matters": "Very low triglycerides are typically not concerning.",
                "next_steps": "Continue current health practices."
            },
            "critical_high": {
                "explanation": "Triglycerides are significantly above normal range.",
                "why_it_matters": "This requires prompt medical attention due to risk of pancreatitis and other complications.",
                "next_steps": "Seek medical attention promptly. Contact your healthcare provider."
            }
        }
    }
}
