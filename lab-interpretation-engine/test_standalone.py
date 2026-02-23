"""
Standalone Test - No Server Required
=====================================
Tests the core interpretation logic without running FastAPI.
"""

import sys
import json
from test_registry import TEST_REGISTRY
from interpretation_engine import LabInterpretationEngine


def test_interpretation_logic():
    """Test the interpretation engine with various scenarios."""
    
    print("=" * 80)
    print("LAB INTERPRETATION ENGINE - CORE LOGIC TEST")
    print("=" * 80)
    print()
    
    # Initialize engine
    engine = LabInterpretationEngine(TEST_REGISTRY)
    
    # Test cases
    test_cases = [
        {
            "name": "Normal Hemoglobin (Female)",
            "test_code": "HB",
            "value": 13.5,
            "sex": "female",
            "age": 35,
            "expected_status": "NORMAL",
            "expected_severity": "NORMAL"
        },
        {
            "name": "Low Hemoglobin (Female) - Abnormal",
            "test_code": "HB",
            "value": 10.8,
            "sex": "female",
            "age": 45,
            "expected_status": "LOW",
            "expected_severity": "ABNORMAL"
        },
        {
            "name": "Critical Low Hemoglobin",
            "test_code": "HB",
            "value": 6.5,
            "sex": "male",
            "age": 60,
            "expected_status": "LOW",
            "expected_severity": "CRITICAL"
        },
        {
            "name": "Borderline Fasting Glucose (Prediabetes)",
            "test_code": "FBG",
            "value": 115,
            "sex": "male",
            "age": 52,
            "expected_status": "HIGH",
            "expected_severity": "BORDERLINE"
        },
        {
            "name": "High Fasting Glucose (Diabetes range)",
            "test_code": "FBG",
            "value": 128,
            "sex": "female",
            "age": 45,
            "expected_status": "HIGH",
            "expected_severity": "ABNORMAL"
        },
        {
            "name": "Critical High Glucose",
            "test_code": "FBG",
            "value": 420,
            "sex": "male",
            "age": 60,
            "expected_status": "HIGH",
            "expected_severity": "CRITICAL"
        },
        {
            "name": "Borderline High Cholesterol",
            "test_code": "TCHOL",
            "value": 215,
            "sex": "male",
            "age": 52,
            "expected_status": "HIGH",
            "expected_severity": "BORDERLINE"
        },
        {
            "name": "Low HDL (Male) - High risk",
            "test_code": "HDL",
            "value": 38,
            "sex": "male",
            "age": 30,
            "expected_status": "LOW",
            "expected_severity": "ABNORMAL"
        },
        {
            "name": "Critical High Creatinine (Kidney failure)",
            "test_code": "CREAT",
            "value": 5.8,
            "sex": "male",
            "age": 60,
            "expected_status": "HIGH",
            "expected_severity": "CRITICAL"
        },
        {
            "name": "Sex-Specific: Male Hemoglobin in Female Range",
            "test_code": "HB",
            "value": 13.0,
            "sex": "male",
            "age": 30,
            "expected_status": "LOW",
            "expected_severity": "ABNORMAL"
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print("-" * 80)
        
        try:
            # Run interpretation
            result = engine.interpret_result(
                test_code=test['test_code'],
                value=test['value'],
                patient_sex=test['sex'],
                patient_age=test['age']
            )
            
            # Check results
            status_match = result['status'] == test['expected_status']
            severity_match = result['severity'] == test['expected_severity']
            
            if status_match and severity_match:
                print(f"✅ PASS")
                passed += 1
            else:
                print(f"❌ FAIL")
                failed += 1
                if not status_match:
                    print(f"   Expected status: {test['expected_status']}, Got: {result['status']}")
                if not severity_match:
                    print(f"   Expected severity: {test['expected_severity']}, Got: {result['severity']}")
            
            # Display interpretation
            print(f"   Test: {result['test_name']}")
            print(f"   Value: {result['value']} {result['unit']}")
            print(f"   Reference Range: {result['reference_range']}")
            print(f"   Status: {result['status']} | Severity: {result['severity']}")
            print(f"   Explanation: {result['explanation'][:80]}...")
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            failed += 1
    
    # Test summary generation
    print("\n" + "=" * 80)
    print("Testing Summary Generation")
    print("=" * 80)
    
    sample_interpretations = [
        {
            "test_code": "HB",
            "severity": "NORMAL",
            "value": 13.5,
            "unit": "g/dL"
        },
        {
            "test_code": "FBG",
            "severity": "BORDERLINE",
            "value": 115,
            "unit": "mg/dL"
        },
        {
            "test_code": "LDL",
            "severity": "ABNORMAL",
            "value": 165,
            "unit": "mg/dL"
        }
    ]
    
    summary = engine.generate_summary(sample_interpretations)
    print(f"\nSummary Test:")
    print(f"  Overall Flag: {summary['overall_flag']} (Expected: ABNORMAL)")
    print(f"  Critical Alert: {summary['critical_alert']} (Expected: False)")
    print(f"  Normal: {summary['normal_count']} (Expected: 1)")
    print(f"  Borderline: {summary['borderline_count']} (Expected: 1)")
    print(f"  Abnormal: {summary['abnormal_count']} (Expected: 1)")
    print(f"  Critical: {summary['critical_count']} (Expected: 0)")
    
    if (summary['overall_flag'] == 'ABNORMAL' and 
        summary['critical_alert'] == False and
        summary['normal_count'] == 1 and
        summary['borderline_count'] == 1 and
        summary['abnormal_count'] == 1):
        print("✅ Summary generation: PASS")
        passed += 1
    else:
        print("❌ Summary generation: FAIL")
        failed += 1
    
    # Final results
    print("\n" + "=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    print(f"Total Tests: {passed + failed}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/(passed+failed)*100):.1f}%")
    print("=" * 80)
    
    return failed == 0


def test_all_supported_tests():
    """Verify all 15 tests are properly configured."""
    
    print("\n" + "=" * 80)
    print("TESTING ALL 15 SUPPORTED TESTS")
    print("=" * 80)
    
    expected_tests = {
        "HB": "Hemoglobin",
        "PCV": "Packed Cell Volume",
        "WBC": "White Blood Cell Count",
        "PLT": "Platelet Count",
        "FBG": "Fasting Blood Glucose",
        "HBA1C": "Hemoglobin A1c",
        "CREAT": "Creatinine",
        "UREA": "Blood Urea Nitrogen",
        "ALT": "Alanine Aminotransferase",
        "AST": "Aspartate Aminotransferase",
        "TBIL": "Total Bilirubin",
        "TCHOL": "Total Cholesterol",
        "LDL": "LDL Cholesterol",
        "HDL": "HDL Cholesterol",
        "TRIG": "Triglycerides"
    }
    
    print(f"\nExpected: {len(expected_tests)} tests")
    print(f"Found: {len(TEST_REGISTRY)} tests")
    
    all_present = True
    
    for code, name in expected_tests.items():
        if code in TEST_REGISTRY:
            test_def = TEST_REGISTRY[code]
            print(f"✅ {code:8s} - {test_def['name']:40s} [{test_def['category']}]")
            
            # Verify required fields
            required_fields = ['name', 'category', 'unit', 'reference_ranges', 
                             'critical_thresholds', 'interpretations']
            for field in required_fields:
                if field not in test_def:
                    print(f"   ⚠️  Missing field: {field}")
                    all_present = False
        else:
            print(f"❌ {code:8s} - MISSING")
            all_present = False
    
    if all_present and len(TEST_REGISTRY) == len(expected_tests):
        print("\n✅ All 15 tests properly configured!")
        return True
    else:
        print("\n❌ Configuration incomplete")
        return False


if __name__ == "__main__":
    print("Lab Result Interpretation Engine - Standalone Test")
    print("No server required - testing core logic only\n")
    
    # Test 1: All tests configured
    config_ok = test_all_supported_tests()
    
    # Test 2: Interpretation logic
    logic_ok = test_interpretation_logic()
    
    # Final status
    print("\n" + "=" * 80)
    print("FINAL STATUS")
    print("=" * 80)
    if config_ok and logic_ok:
        print("✅ ALL TESTS PASSED - System is working correctly")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - Review output above")
        sys.exit(1)
