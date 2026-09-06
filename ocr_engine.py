"""
OCR & Multilingual Named Entity Recognition (NER) Engine for Bhoomi-AI.
Processes scanned land records, generates bounding boxes, simulates computer vision pre-processing,
and extracts structured land administration fields across 22+ Indian languages.
"""

import re
import random
import uuid

# Multilingual State Templates & Vocabulary Maps
STATE_TEMPLATES = {
    "UP": {
        "name": "Uttar Pradesh",
        "docType": "Khasra-Khatauni (खसरा-खतौनी)",
        "language": "Hindi (हिंदी)",
        "script": "Devanagari",
        "keywords": ["खसरा", "खतौनी", "खाता", "फसली", "गाटा", "खातेदार", "क्षेत्रफल", "तहसील", "परगना", "कैफियत", "हिस्सा"],
        "units": ["एकड़", "हेक्टेयर", "बीघा", "बिस्वा", "वर्ग मीटर"],
        "sampleSurnames": ["शर्मा", "यादव", "मौर्य", "सिंह", "वर्मा", "पांडेय", "शुक्ला", "पटेल", "गुप्ता", "त्रिपाठी"]
    },
    "MH": {
        "name": "Maharashtra",
        "docType": "7/12 Extract (सातबारा उतारा)",
        "language": "Marathi (मराठी)",
        "script": "Devanagari",
        "keywords": ["गाव नमुना", "अधिकार अभिलेख", "भूमापन क्रमांक", "हिस्सा", "खाते क्रमांक", "खातेदाराचे नाव", "जिरायत", "बागायत", "फेरफार", "इतर अधिकार"],
        "units": ["हे.आर.", "एकर", "गुंठे", "चौ.मी."],
        "sampleSurnames": ["पाटील", "देशमुख", "गायकवाड", "पवार", "शिंदे", "जाधव", "कांबळे", "कदम", "मोरे", "भोसले"]
    },
    "TS": {
        "name": "Telangana",
        "docType": "Dharani Pattadar Passbook & Pahani (ధరణి పట్టాదారు పాస్ పుస్తకం)",
        "language": "Telugu (తెలుగు)",
        "script": "Telugu",
        "keywords": ["ధరణి", "పట్టాదారు", "సర్వే నెం", "ఖాతా నెం", "విస్తీర్ణం", "భూమి రకం", "మెట్ట", "తరి", "మండలం", "గ్రామం", "ఋణభారం"],
        "units": ["ఎకరాలు", "గుంటలు", "హెక్టార్లు", "చ.మీ."],
        "sampleSurnames": ["రావు", "రెడ్డి", "చౌదరి", "శర్మ", "గుప్తా", "యాదవ్", "నాయుడు", "వర్మ", "గౌడ్"]
    },
    "KA": {
        "name": "Karnataka",
        "docType": "Bhoomi RTC Extract (ಭೂಮಿ ಪಹಣಿ)",
        "language": "Kannada (ಕನ್ನಡ)",
        "script": "Kannada",
        "keywords": ["ಭೂಮಿ", "ಪಹಣಿ", "ಸರ್ವೆ ನಂಬರ್", "ಖಾತಾ", "ಹಿಸ್ಸಾ", "ಖಾತೇದಾರರ ಹೆಸರು", "ವಿಸ್ತೀರ್ಣ", "ಖುಷ್ಕಿ", "ತರಿ", "ಬಾಗಾಯ್ತು", "ಋಣಭಾರ"],
        "units": ["ಎಕರೆ", "ಗುಂಟೆ", "ಹೆಕ್ಟೇರ್", "ಚ.ಮೀ."],
        "sampleSurnames": ["ಗೌಡ", "ಶೆಟ್ಟಿ", "ರಾವ್", "ಹೆಗಡೆ", "ನಾಯಕ್", "ಭಟ್", "ಕುಮಾರ್", "ರೆಡ್ಡಿ"]
    },
    "TN": {
        "name": "Tamil Nadu",
        "docType": "Patta Chitta & FMB Extract (பட்டா சிட்டா)",
        "language": "Tamil (தமிழ்)",
        "script": "Tamil",
        "keywords": ["பட்டா", "சிட்டா", "புல எண்", "உட்பிரிவு", "விஸ்தீர்ணம்", "நஞ்சை", "புஞ்சை", "உரிமையாளர் பெயர்", "தீர்வை", "மாவட்டம்"],
        "units": ["ஹெக்டேர்", "ஏக்கர்", "சென்ட்", "குழி"],
        "sampleSurnames": ["கவுண்டர்", "செட்டியார்", "நாயக்கர்", "தேவர்", "முதலியார்", "பிள்ளை", "சுப்பிரமணியன்"]
    },
    "WB": {
        "name": "West Bengal",
        "docType": "Banglarbhumi Khatian & Plot Ledger (বাংলারভূমি খতিয়ান)",
        "language": "Bengali (বাংলা)",
        "script": "Bengali",
        "keywords": ["খতিয়ান", "দাগ নং", "মৌজা", "জে.এল. নং", "জমির শ্রেণি", "শালি", "বাস্তু", "রায়তের নাম", "অংশ", "মন্তব্য"],
        "units": ["একর", "শতক", "হেক্টর", "কাঠা", "বিঘা"],
        "sampleSurnames": ["ব্যানার্জী", "মুখার্জী", "চ্যাটার্জী", "ঘোষ", "বসু", "সেন", "দাস", "রায়", "মজুমদার"]
    },
    "PB": {
        "name": "Punjab",
        "docType": "Jamabandi Nakal / Fard (ਜਮਾਂਬੰਦੀ ਨਕਲ)",
        "language": "Punjabi (ਪੰਜਾਬੀ)",
        "script": "Gurmukhi",
        "keywords": ["ਜਮਾਂਬੰਦੀ", "ਫ਼ਰਦ", "ਖੇਵਟ", "ਖਤੌਨੀ", "ਖਸਰਾ", "ਰਕਬਾ", "ਚਾਹੀ", "ਨਹਿਰੀ", "ਗੈਰ ਮੁਮਕਿਨ", "ਮਾਲਕ", "ਕਾਸ਼ਤਕਾਰ", "ਇੰਤਕਾਲ"],
        "units": ["ਏਕੜ", "ਕਨਾਲ", "ਮਰਲੇ", "ਬਿੱਘਾ", "ਬਿਸਵਾ"],
        "sampleSurnames": ["ਸਿੰਘ", "ਧਾਲੀਵਾਲ", "ਗਿੱਲ", "ਸੰਧੂ", "ਢਿੱਲੋਂ", "ਬਰਾੜ", "ਗਰੇਵਾਲ", "ਔਲਖ", "ਚੀਮਾ"]
    }
}

class OCREngine:
    def __init__(self):
        pass

    def generate_bounding_boxes(self, record_data):
        """
        Generates realistic document coordinates and bounding box metadata for the interactive canvas.
        Each box is tagged with field key, label, confidence score, and normalized coordinate percentages.
        """
        conf = record_data.get("confidenceScores", {})
        
        boxes = [
            {
                "id": "box-header",
                "field": "documentType",
                "label": "Document Type / Title",
                "value": record_data.get("documentType", "Land Record Extract"),
                "confidence": 99.0,
                "x": 15, "y": 6, "w": 70, "h": 6,
                "status": "high"
            },
            {
                "id": "box-district-village",
                "field": "location",
                "label": "Village, Tehsil, District",
                "value": f"{record_data.get('village', '')}, {record_data.get('tehsil', '')}, {record_data.get('district', '')}",
                "confidence": 98.2,
                "x": 10, "y": 14, "w": 80, "h": 7,
                "status": "high"
            },
            {
                "id": "box-khasra",
                "field": "khasraNo",
                "label": "Survey / Khasra No.",
                "value": str(record_data.get("khasraNo", "142/1")),
                "confidence": conf.get("khasraNo", 98.5),
                "x": 12, "y": 24, "w": 22, "h": 6,
                "status": "high" if conf.get("khasraNo", 98.5) >= 90 else "medium"
            },
            {
                "id": "box-khata",
                "field": "khataNo",
                "label": "Khata / Khatauni No.",
                "value": str(record_data.get("khataNo", "00284")),
                "confidence": conf.get("khataNo", 97.4),
                "x": 37, "y": 24, "w": 22, "h": 6,
                "status": "high" if conf.get("khataNo", 97.4) >= 90 else "medium"
            },
            {
                "id": "box-subdiv",
                "field": "subDivision",
                "label": "Sub-Division / Hissa",
                "value": str(record_data.get("subDivision", "1-क")),
                "confidence": 95.0,
                "x": 62, "y": 24, "w": 26, "h": 6,
                "status": "high"
            },
            {
                "id": "box-owner",
                "field": "landownerName",
                "label": "Landowner / Katedar Name",
                "value": record_data.get("landownerName", "Landowner"),
                "confidence": conf.get("landownerName", 96.0),
                "x": 10, "y": 33, "w": 45, "h": 8,
                "status": "high" if conf.get("landownerName", 96.0) >= 90 else ("medium" if conf.get("landownerName", 96.0) >= 70 else "low")
            },
            {
                "id": "box-father",
                "field": "fatherSpouseName",
                "label": "Father / Spouse Name",
                "value": record_data.get("fatherSpouseName", "Father"),
                "confidence": conf.get("fatherSpouseName", 95.0),
                "x": 58, "y": 33, "w": 32, "h": 8,
                "status": "high" if conf.get("fatherSpouseName", 95.0) >= 90 else ("medium" if conf.get("fatherSpouseName", 95.0) >= 70 else "low")
            },
            {
                "id": "box-area",
                "field": "totalArea",
                "label": "Plot Extent / Area",
                "value": f"{record_data.get('totalArea', {}).get('value', 2.0)} {record_data.get('totalArea', {}).get('unit', 'Acres')}",
                "confidence": conf.get("totalArea", 94.0),
                "x": 10, "y": 44, "w": 38, "h": 7,
                "status": "high" if conf.get("totalArea", 94.0) >= 90 else ("medium" if conf.get("totalArea", 94.0) >= 70 else "low")
            },
            {
                "id": "box-classification",
                "field": "landClassification",
                "label": "Land Classification",
                "value": record_data.get("landClassification", "Agricultural"),
                "confidence": conf.get("landClassification", 95.5),
                "x": 52, "y": 44, "w": 38, "h": 7,
                "status": "high" if conf.get("landClassification", 95.5) >= 90 else "medium"
            },
            {
                "id": "box-encumbrance",
                "field": "encumbrance",
                "label": "Encumbrance / Liabilities",
                "value": record_data.get("encumbrance", "Nil"),
                "confidence": conf.get("encumbrance", 88.0),
                "x": 10, "y": 54, "w": 80, "h": 8,
                "status": "high" if conf.get("encumbrance", 88.0) >= 90 else ("medium" if conf.get("encumbrance", 88.0) >= 70 else "low")
            },
            {
                "id": "box-mutation",
                "field": "mutationDetails",
                "label": "Mutation (Namantaran) Order",
                "value": f"{record_data.get('mutationDetails', {}).get('mutationNo', '')} ({record_data.get('mutationDetails', {}).get('type', '')})",
                "confidence": 92.0,
                "x": 10, "y": 65, "w": 80, "h": 8,
                "status": "high"
            },
            {
                "id": "box-seal-stamp",
                "field": "officialSeal",
                "label": "Official Revenue Seal & Signature",
                "value": "Certified Digital Stamp & Signature",
                "confidence": 98.9,
                "x": 62, "y": 78, "w": 28, "h": 16,
                "status": "high"
            }
        ]

        return boxes

    def process_raw_document(self, filename, raw_text=None, state_hint="UP"):
        """
        Simulates multilingual OCR extraction & NER entity classification pipeline.
        Parses Khasra, Khata, Owner names, Areas, and calculates unit conversions and confidence.
        """
        state_code = state_hint.upper() if state_hint in STATE_TEMPLATES else "UP"
        template = STATE_TEMPLATES.get(state_code, STATE_TEMPLATES["UP"])

        # If raw text is provided by user, perform heuristic NER parsing
        if raw_text:
            text = raw_text
        else:
            text = f"खसरा संख्या: {random.randint(100, 999)}/{random.randint(1, 4)} | खाता संख्या: {random.randint(1000, 9999)} | खातेदार: {random.choice(template['sampleSurnames'])} | क्षेत्रफल: {round(random.uniform(0.5, 5.0), 2)} एकड़"

        # Heuristic extraction
        khasra_match = re.search(r'(?:खसरा|सर्वे|survey|khasra|ভূমাपन|புல)\s*(?:संख्या|नंबर|no|नं|নং)?[:\s]*([0-9]+(?:\/[0-9]+[A-Za-z\u0900-\u097F]*)?)', text, re.IGNORECASE)
        khata_match = re.search(r'(?:खाता|khata|খতিয়ান|பட்டா|ಖಾತಾ|ఖాతా)\s*(?:संख्या|नंबर|no|नं)?[:\s]*([0-9]+)', text, re.IGNORECASE)
        area_match = re.search(r'(?:क्षेत्रफल|area|विस्तీర్ణం|రకబా|విస్తీర్ణం|ਵਿਸਥਾਰ|পরিমাণ)\s*[:\s]*([0-9]+(?:\.[0-9]+)?)\s*([a-zA-Z\u0900-\u0DFF]+)?', text, re.IGNORECASE)

        khasra_no = khasra_match.group(1) if khasra_match else f"{random.randint(100, 450)}/{random.randint(1, 3)}"
        khata_no = khata_match.group(1) if khata_match else f"0{random.randint(1000, 8999)}"
        area_val = float(area_match.group(1)) if area_match else round(random.uniform(1.2, 4.8), 2)
        unit = area_match.group(2) if (area_match and area_match.group(2)) else "Acres"

        owner_name = f"राजेश {random.choice(template['sampleSurnames'])} (Rajesh {template['sampleSurnames'][0]})"
        father_name = f"स्व. रामनाथ {random.choice(template['sampleSurnames'])}"

        # Compute standard unit conversions
        acres = area_val if "acre" in unit.lower() or "एकड़" in unit else round(area_val * 2.471, 2)
        hectares = round(acres * 0.404686, 4)
        bigha = round(acres * 1.613, 2)
        biswa = round(bigha * 20, 1)
        sq_meters = round(acres * 4046.86, 2)
        guntas = round(acres * 40, 1)

        conf_khasra = round(random.uniform(92.0, 99.5), 1)
        conf_owner = round(random.uniform(88.0, 98.5), 1)
        conf_father = round(random.uniform(85.0, 97.0), 1)
        conf_area = round(random.uniform(90.0, 99.0), 1)
        conf_khata = round(random.uniform(91.0, 98.8), 1)
        conf_overall = round((conf_khasra + conf_owner + conf_father + conf_area + conf_khata) / 5, 1)

        record_id = f"REC-{state_code}-2026-{random.randint(1000, 9999)}"

        new_record = {
            "id": record_id,
            "state": template["name"],
            "stateCode": state_code,
            "documentType": template["docType"],
            "language": template["language"],
            "script": template["script"],
            "district": "Model Central District",
            "tehsil": "Model Revenue Circle",
            "village": "Rampur Khurd",
            "mauzaCode": f"{state_code}-MOD-0199",
            "khasraNo": khasra_no,
            "khataNo": khata_no,
            "subDivision": "1-क",
            "landownerName": owner_name,
            "fatherSpouseName": father_name,
            "coOwners": [
                {"name": owner_name.split()[0], "relation": "खातेदार (Self)", "share": "1/1", "shareAreaAcres": acres}
            ],
            "totalArea": {
                "value": acres,
                "unit": "Acres",
                "conversions": {
                    "hectares": hectares,
                    "bigha": bigha,
                    "biswa": biswa,
                    "sqMeters": sq_meters,
                    "guntas": guntas
                }
            },
            "landClassification": "कृषि भूमि (Agricultural - Irrigated)",
            "irrigationSource": "नलकूप / Canal",
            "landRevenueTax": f"₹ {round(acres * 60, 2)} / year",
            "soilType": "Fertile Alluvial Loam",
            "encumbrance": "Nil (Encumbrance Free)",
            "mutationDetails": {
                "mutationNo": f"MUT-{state_code}-2024-{random.randint(1000, 9999)}",
                "date": "15-May-2024",
                "type": "रजिस्टर्ड बैनामा (Registered Sale Deed)",
                "orderAuthority": "नायब तहसीलदार / Revenue Officer",
                "status": "Certified in State LRMS"
            },
            "registrationDetails": {
                "deedNo": f"DEED/{state_code}/{random.randint(1000, 9999)}/2024",
                "sroOffice": "Central Sub-Registrar Office",
                "registrationDate": "10-05-2024"
            },
            "confidenceScores": {
                "overall": conf_overall,
                "landownerName": conf_owner,
                "fatherSpouseName": conf_father,
                "khasraNo": conf_khasra,
                "khataNo": conf_khata,
                "totalArea": conf_area,
                "landClassification": 95.0,
                "encumbrance": 92.0
            },
            "status": "Validated" if conf_overall >= 90.0 else "Review Required",
            "verificationFlags": [] if conf_overall >= 90.0 else ["Low confidence on handwritten entries; Human verification recommended."],
            "uploadedAt": "2026-09-02T14:30:00Z",
            "verifiedBy": None,
            "verifiedAt": None,
            "cadastralPlotId": f"CAD-{state_code}-{khasra_no.replace('/', '-')}",
            "coordinates": {"lat": 26.5 + random.uniform(-5, 5), "lng": 80.5 + random.uniform(-5, 5)},
            "scanImage": filename,
            "ocrRawText": text
        }

        return new_record

ocr_engine = OCREngine()
