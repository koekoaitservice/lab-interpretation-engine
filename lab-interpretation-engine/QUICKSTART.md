# Quick Start Guide

## Installation & Running

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python main.py
```

The server will start on `http://localhost:8000`

### 3. Test the API

**Check health:**
```bash
curl http://localhost:8000
```

**List supported tests:**
```bash
curl http://localhost:8000/tests
```

**Interpret results:**
```bash
curl -X POST http://localhost:8000/interpret \
  -H "Content-Type: application/json" \
  -d @example_request.json
```

## Testing Without Running Server

If you want to test the core logic without installing FastAPI:

```bash
python test_standalone.py
```

This will run all unit tests and verify the system is working correctly.

## Generate Example Files

```bash
python generate_example.py
```

This creates example JSON request/response files for reference.

## File Structure

```
├── main.py                    # FastAPI application
├── test_registry.py           # All 15 lab tests with ranges
├── interpretation_engine.py   # Core interpretation logic
├── test_standalone.py         # Unit tests (no server needed)
├── test_examples.py           # API integration tests
├── generate_example.py        # Generate example JSON files
├── requirements.txt           # Python dependencies
├── README.md                  # Full documentation
└── QUICKSTART.md             # This file
```

## Next Steps

1. ✅ Review the full README.md for detailed documentation
2. ✅ Run test_standalone.py to verify the system
3. ✅ Start the server with python main.py
4. ✅ Test with example_request.json
5. ✅ Integrate into your diagnostic lab workflow

## Production Deployment Checklist

- [ ] Review all reference ranges with medical team
- [ ] Customize patient-facing text for your region
- [ ] Add logging and monitoring
- [ ] Implement rate limiting
- [ ] Add authentication if needed
- [ ] Set up SSL/TLS
- [ ] Configure CORS for your frontend
- [ ] Add database for audit trails
- [ ] Legal review of all disclaimers
- [ ] Test with real lab data

## Support

This is a reference implementation. For production use, please:
- Consult with healthcare professionals
- Review with legal/compliance team
- Validate against local laboratory standards
