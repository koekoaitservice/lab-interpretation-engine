# Lab Result Interpretation Engine

A **compliance-safe, rules-based** lab result interpretation system designed for patient-facing explanations. This is **NOT a diagnostic system** and provides educational information only.

## 🎯 Purpose

This engine helps diagnostic laboratories provide clear, understandable explanations of lab results to patients while maintaining strict healthcare compliance and safety standards.

## 📋 Phase 1 Updates

**Recent corrections implemented:**
1. ✅ **Critical result restriction** - CRITICAL results now use minimal, action-oriented messaging only
2. ✅ **Unsupported test handling** - Unknown test codes are tracked and returned in warnings (not silently ignored)
3. ✅ **Age safety guardrail** - Adults only (age >= 18); pediatric patients rejected with clear error
4. ✅ **Unit conversion** - Support for common alternative units (mmol/L, µmol/L) with deterministic conversion

See [PHASE1_CORRECTIONS.md](PHASE1_CORRECTIONS.md) for detailed documentation.

## ⚠️ Critical Compliance Features

- **No AI/ML Models**: Uses only deterministic, rules-based logic
- **No Diagnosis**: Does not diagnose diseases or conditions
- **No Treatment Advice**: Does not recommend medications or treatments
- **Auditable**: All logic is transparent and traceable
- **Safety-First**: Conservative classification with critical threshold monitoring
- **Structured Output**: JSON-formatted responses for downstream integration

## 🏥 Supported Lab Tests (15)

### Hematology
- **HB** - Hemoglobin
- **PCV** - Packed Cell Volume (Hematocrit)
- **WBC** - White Blood Cell Count
- **PLT** - Platelet Count

### Metabolic
- **FBG** - Fasting Blood Glucose
- **HBA1C** - Hemoglobin A1c

### Renal (Kidney)
- **CREAT** - Creatinine
- **UREA** - Blood Urea Nitrogen (BUN)

### Liver
- **ALT** - Alanine Aminotransferase
- **AST** - Aspartate Aminotransferase
- **TBIL** - Total Bilirubin

### Lipids
- **TCHOL** - Total Cholesterol
- **LDL** - LDL Cholesterol
- **HDL** - HDL Cholesterol
- **TRIG** - Triglycerides

## 🔒 Safety Classification System

Each test result is classified into **four severity tiers**:

1. **NORMAL** - Within healthy reference range
2. **BORDERLINE** - In a cautionary zone (for applicable tests)
3. **ABNORMAL** - Outside normal range but not immediately dangerous
4. **CRITICAL** - Requires urgent medical attention

### Critical Threshold Logic

**Critical thresholds are checked FIRST** before normal ranges to ensure urgent situations are immediately flagged.

Examples:
- Hemoglobin ≤ 7.0 g/dL → CRITICAL (severe anemia)
- Glucose ≥ 400 mg/dL → CRITICAL (severe hyperglycemia)
- Creatinine ≥ 5.0 mg/dL → CRITICAL (severe kidney impairment)

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```

4. **Verify the server is running:**
   ```bash
   curl http://localhost:8000
   ```

   You should see:
   ```json
   {
     "service": "Lab Result Interpretation Engine",
     "status": "operational",
     "version": "1.0.0",
     "compliance": "Educational use only - not for diagnosis"
   }
   ```

## 📡 API Usage

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```bash
GET /
```

#### 2. List Supported Tests
```bash
GET /tests
```

#### 3. Interpret Lab Results
```bash
POST /interpret
```

### Request Format

```json
{
  "patient": {
    "age": 45,
    "sex": "female"
  },
  "results": [
    {
      "test_code": "HB",
      "value": 10.8,
      "unit": "g/dL"
    },
    {
      "test_code": "FBG",
      "value": 128,
      "unit": "mg/dL"
    }
  ]
}
```

**Field Validation:**
- `age`: Integer, 0-120
- `sex`: Either "male" or "female"
- `test_code`: Must be one of the 15 supported codes (case-insensitive)
- `value`: Numeric test result
- `unit`: Must match expected unit for the test

### Response Format

```json
{
  "summary": {
    "overall_flag": "ABNORMAL",
    "critical_alert": false,
    "critical_count": 0,
    "abnormal_count": 2,
    "borderline_count": 0,
    "normal_count": 0
  },
  "interpretations": [
    {
      "test_code": "HB",
      "test_name": "Hemoglobin",
      "value": 10.8,
      "unit": "g/dL",
      "status": "LOW",
      "severity": "ABNORMAL",
      "reference_range": "12.0 - 15.5 g/dL",
      "explanation": "Hemoglobin is lower than the typical range. Hemoglobin is the protein in red blood cells that carries oxygen throughout your body.",
      "why_it_matters": "Lower levels may be associated with tiredness, weakness, or shortness of breath.",
      "next_steps": "Consider discussing this result with a healthcare professional to understand possible causes."
    },
    {
      "test_code": "FBG",
      "test_name": "Fasting Blood Glucose",
      "value": 128,
      "unit": "mg/dL",
      "status": "HIGH",
      "severity": "ABNORMAL",
      "reference_range": "70 - 99 mg/dL",
      "explanation": "Fasting blood glucose is higher than the typical range.",
      "why_it_matters": "Elevated fasting glucose may indicate diabetes and requires professional evaluation.",
      "next_steps": "Consult with a healthcare professional for further assessment and guidance."
    }
  ],
  "disclaimer": "This information is for educational purposes only and does not replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider with questions about your health or lab results."
}
```

## 🧪 Testing

### Run Test Suite

```bash
python test_examples.py
```

This will test all example scenarios:
1. Normal results
2. Abnormal results
3. Borderline results
4. Critical results
5. Comprehensive metabolic panel
6. Sex-specific reference ranges

### Generate Example JSON Files

```bash
python test_examples.py save
```

This creates example request files you can use with curl or Postman:
- `example_1_normal.json`
- `example_2_abnormal.json`
- `example_3_borderline.json`
- `example_4_critical.json`
- `example_5_comprehensive.json`
- `example_6_sex_specific.json`

### Manual Testing with curl

```bash
curl -X POST http://localhost:8000/interpret \
  -H "Content-Type: application/json" \
  -d @example_2_abnormal.json
```

## 📋 Example Use Cases

### Example 1: Normal Results
**Input:**
- Female, age 35
- Hemoglobin: 13.5 g/dL
- Fasting glucose: 92 mg/dL

**Output:** All tests NORMAL, no alerts

---

### Example 2: Borderline Prediabetes
**Input:**
- Male, age 52
- Fasting glucose: 115 mg/dL (borderline)
- HbA1c: 6.0% (borderline)

**Output:** BORDERLINE severity, recommendation to discuss with healthcare provider

---

### Example 3: Critical Anemia
**Input:**
- Male, age 60
- Hemoglobin: 6.5 g/dL (critical)

**Output:**
- CRITICAL severity
- critical_alert: true
- Next steps: "Seek medical attention promptly"

## 🏗️ Architecture

### File Structure

```
├── main.py                    # FastAPI application & endpoints
├── test_registry.py           # Test definitions, ranges, templates
├── interpretation_engine.py   # Core interpretation logic
├── test_examples.py           # Test cases & examples
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### Core Components

1. **main.py**: FastAPI application with request/response models and validation
2. **test_registry.py**: Centralized registry of all 15 lab tests with:
   - Reference ranges (sex-specific where applicable)
   - Critical thresholds
   - Borderline ranges (for applicable tests)
   - Patient-friendly explanation templates

3. **interpretation_engine.py**: Rules-based logic engine that:
   - Classifies results (LOW/NORMAL/HIGH)
   - Determines severity (NORMAL/BORDERLINE/ABNORMAL/CRITICAL)
   - Selects appropriate explanations
   - Generates summary statistics

### Safety Logic Flow

```
1. Receive lab result
2. Validate input (test code, unit, value range)
3. Get appropriate reference range (sex-specific if needed)
4. ⚠️  CHECK CRITICAL THRESHOLDS FIRST (highest priority)
5. Check borderline ranges (if applicable)
6. Check normal reference ranges
7. Classify severity conservatively
8. Select appropriate explanation template
9. Return structured, auditable output
```

## 🌍 Regional Considerations

The system is designed for **Nigeria/Africa** but is globally extensible:

- Reference ranges follow international clinical standards
- Units are standard (mg/dL, g/dL, U/L, etc.)
- Sex-specific ranges are implemented where clinically relevant
- Conservative critical thresholds ensure safety across populations

**To adapt for different regions:**
1. Review reference ranges in `test_registry.py`
2. Adjust critical thresholds if local guidelines differ
3. Translate explanation templates as needed
4. Maintain same safety classification logic

## 🔐 Compliance & Legal

### Medical Disclaimer

**IMPORTANT:** This system provides educational information only and:
- Does NOT diagnose diseases
- Does NOT recommend treatments or medications
- Does NOT replace professional medical advice
- Should ALWAYS include the mandatory disclaimer

### Audit Trail

All interpretations are:
- **Deterministic**: Same input always produces same output
- **Traceable**: Logic is explicit and documented
- **Explainable**: Clear rules, no "black box" AI
- **Structured**: JSON output enables compliance logging

### Production Deployment Recommendations

1. **Logging**: Implement comprehensive audit logging
2. **Monitoring**: Track critical alerts and API usage
3. **Validation**: Add laboratory certification checks
4. **Versioning**: Version the test registry for traceability
5. **Legal Review**: Have legal team review all patient-facing text
6. **Testing**: Comprehensive testing with real lab data
7. **Backup**: Ensure reference ranges are backed up
8. **Updates**: Process for updating ranges when guidelines change

## 🔧 Customization

### Adding New Tests

To add a new lab test:

1. Add test definition to `test_registry.py`:
   ```python
   "NEW_TEST": {
       "name": "Full Test Name",
       "category": "Category",
       "unit": "unit",
       "sex_specific": False,  # or True
       "reference_ranges": {
           "default": {"low": X, "high": Y}
       },
       "critical_thresholds": {
           "critical_low": A,
           "critical_high": B
       },
       "interpretations": {
           "low": {...},
           "normal": {...},
           "high": {...},
           "critical_low": {...},
           "critical_high": {...}
       }
   }
   ```

2. Test the new definition thoroughly
3. Update documentation

### Modifying Reference Ranges

**⚠️ IMPORTANT:** Only modify reference ranges based on:
- Updated clinical guidelines
- Regional laboratory standards
- Medical professional review

Never modify ranges without proper clinical justification.

## 📞 Support & Feedback

This is a reference implementation for educational purposes. For production use:

1. Consult with healthcare professionals
2. Review with legal/compliance team
3. Validate with local laboratory standards
4. Implement comprehensive testing
5. Add proper monitoring and logging

## 📄 License

This is a reference implementation. Adapt as needed for your use case while maintaining healthcare compliance standards.

## ✅ Quality Checklist

- [x] No AI/ML probabilistic models
- [x] Deterministic, rules-based logic only
- [x] No disease diagnosis
- [x] No treatment recommendations
- [x] Medical disclaimer included
- [x] Critical thresholds implemented
- [x] Sex-specific ranges where applicable
- [x] Structured, auditable output
- [x] Input validation
- [x] Error handling
- [x] Comprehensive documentation
- [x] Test cases provided

---

**Version:** 1.0.0  
**Target Region:** Nigeria / Africa (globally extensible)  
**Compliance:** Educational use only - not for diagnosis
