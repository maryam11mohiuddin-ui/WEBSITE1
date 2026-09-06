"""
Database and in-memory store for Bhoomi-AI Land Record Digitization System.
Contains pre-seeded records, historical land records, cadastral parcels, audit logs, and user roles.
"""

import json
import time
import uuid
import datetime

# Pre-seeded State Land Record Presets (Multilingual)
INITIAL_RECORDS = [
    {
        "id": "REC-UP-2026-0842",
        "state": "Uttar Pradesh",
        "stateCode": "UP",
        "documentType": "Khasra-Khatauni (खसरा-खतौनी)",
        "language": "Hindi (हिंदी)",
        "script": "Devanagari",
        "district": "Varanasi (वाराणसी)",
        "tehsil": "Pindra (पिंडरा)",
        "village": "Phoolpur (फूलपुर)",
        "mauzaCode": "UP-VAR-0914",
        "khasraNo": "142/1",
        "khataNo": "00284",
        "subDivision": "1-क",
        "landownerName": "रामेश्वर प्रसाद शर्मा (Rameshwar Prasad Sharma)",
        "fatherSpouseName": "स्व. बद्री नारायण शर्मा (Late Badri Narayan Sharma)",
        "coOwners": [
            {"name": "सुरेश कुमार शर्मा", "relation": "पुत्र (Son)", "share": "1/2", "shareAreaAcres": 1.25},
            {"name": "दिनेश कुमार शर्मा", "relation": "पुत्र (Son)", "share": "1/2", "shareAreaAcres": 1.25}
        ],
        "totalArea": {
            "value": 2.50,
            "unit": "Acres",
            "conversions": {
                "hectares": 1.0117,
                "bigha": 4.033,
                "biswa": 80.66,
                "sqMeters": 10117.14,
                "guntas": 100.0
            }
        },
        "landClassification": "कृषि भूमि (Agricultural - Chahi Irrigated)",
        "irrigationSource": "नलकूप (Tube Well)",
        "landRevenueTax": "₹ 145.50 / year",
        "soilType": "Alluvial Clay Loam (दोमट)",
        "encumbrance": "केनरा बैंक शाखा पिंडरा बंधक (Mortgage - Canara Bank ₹2,50,000)",
        "mutationDetails": {
            "mutationNo": "MUT-2023-9912",
            "date": "14-Nov-2023",
            "type": "वरासत (Inheritance / Succession)",
            "orderAuthority": "नायब तहसीलदार पिंडरा (Naib Tehsildar)",
            "status": "Certified & Mutated"
        },
        "registrationDetails": {
            "deedNo": "DEED/VAR/8821/2018",
            "sroOffice": "SRO Pindra",
            "registrationDate": "22-03-2018"
        },
        "confidenceScores": {
            "overall": 96.4,
            "landownerName": 98.2,
            "fatherSpouseName": 97.5,
            "khasraNo": 99.0,
            "khataNo": 98.8,
            "totalArea": 95.1,
            "landClassification": 94.7,
            "encumbrance": 89.2
        },
        "status": "Validated",
        "verificationFlags": [],
        "uploadedAt": "2026-08-28T10:15:30Z",
        "verifiedBy": "S.K. Mishra (Tehsildar)",
        "verifiedAt": "2026-08-28T14:22:10Z",
        "cadastralPlotId": "CAD-UP-VAR-142-1",
        "coordinates": {"lat": 25.4382, "lng": 82.8461},
        "scanImage": "sample_up_khasra.png",
        "ocrRawText": "ग्राम: फूलपुर | परगना: पिंडरा | जनपद: वाराणसी | फसली वर्ष: 1430-1435 | खाता संख्या: 00284 | खसरा संख्या: 142/1 | क्षेत्रफल: 2.50 एकड़ (1.0117 हे.) | खातेदार का नाम: रामेश्वर प्रसाद शर्मा सुपुत्र स्व. बद्री नारायण शर्मा | कैफियत: केनरा बैंक शाखा पिंडरा से बन्धक"
    },
    {
        "id": "REC-MH-2026-1198",
        "state": "Maharashtra",
        "stateCode": "MH",
        "documentType": "7/12 Extract (Saat-Baara / सातबारा उतारा)",
        "language": "Marathi (मराठी)",
        "script": "Devanagari",
        "district": "Pune (पुणे)",
        "tehsil": "Haveli (हवेली)",
        "village": "Wagholi (वाघोली)",
        "mauzaCode": "MH-PUN-0412",
        "khasraNo": "304/2B",
        "khataNo": "01482",
        "subDivision": "२-ब (2-B)",
        "landownerName": "विठ्ठल तुकाराम पाटील (Vitthal Tukaram Patil)",
        "fatherSpouseName": "तुकाराम बाबुराव पाटील (Tukaram Baburao Patil)",
        "coOwners": [
            {"name": "सुनीता विठ्ठल पाटील", "relation": "पत्नी (Wife)", "share": "1/3", "shareAreaAcres": 0.60},
            {"name": "अमोल विठ्ठल पाटील", "relation": "मुलगा (Son)", "share": "2/3", "shareAreaAcres": 1.20}
        ],
        "totalArea": {
            "value": 1.80,
            "unit": "Acres",
            "conversions": {
                "hectares": 0.7284,
                "bigha": 2.904,
                "biswa": 58.08,
                "sqMeters": 7284.34,
                "guntas": 72.0
            }
        },
        "landClassification": "जिरायत / बागायत (Agricultural - Jirayat / Bagayat)",
        "irrigationSource": "विहीर व ठिबक (Well & Drip)",
        "landRevenueTax": "₹ 112.00 / year",
        "soilType": "Black Cotton Soil (काळी माती)",
        "encumbrance": "बँक ऑफ महाराष्ट्र ₹ 1,80,000 पिक कर्ज (Crop Loan Bank of Maharashtra)",
        "mutationDetails": {
            "mutationNo": "फेरफार क्र. ७४५२ (Ferfar 7452)",
            "date": "09-Jan-2024",
            "type": "हक्कसोड पत्र (Relinquishment / Deed)",
            "orderAuthority": "मंडळ अधिकारी वाघोली (Circle Officer)",
            "status": "Sanctioned (मंजूर)"
        },
        "registrationDetails": {
            "deedNo": "HAV/7741/2019",
            "sroOffice": "Haveli Sub-Registrar 4",
            "registrationDate": "18-07-2019"
        },
        "confidenceScores": {
            "overall": 94.8,
            "landownerName": 97.0,
            "fatherSpouseName": 96.1,
            "khasraNo": 98.5,
            "khataNo": 96.2,
            "totalArea": 92.4,
            "landClassification": 95.0,
            "encumbrance": 88.6
        },
        "status": "Validated",
        "verificationFlags": [],
        "uploadedAt": "2026-08-29T11:40:00Z",
        "verifiedBy": "R.V. Deshmukh (Revenue Inspector)",
        "verifiedAt": "2026-08-29T16:05:44Z",
        "cadastralPlotId": "CAD-MH-PUN-304-2B",
        "coordinates": {"lat": 18.5793, "lng": 73.9822},
        "scanImage": "sample_mh_712.png",
        "ocrRawText": "गाव नमुना सात (अधिकार अभिलेख पत्रक) व गाव नमुना १२ (पिकांची नोंदवही) | गाव: वाघोली | तालुका: हवेली | जिल्हा: पुणे | भूमापन क्रमांक: ३०४/२ब | खाते क्रमांक: ०१४८२ | एकूण क्षेत्र: ०.७२.८४ हे.आर. (१.८० एकर) | खातेदाराचे नाव: विठ्ठल तुकाराम पाटील | इतर अधिकार: बँक ऑफ महाराष्ट्र पीक कर्ज"
    },
    {
        "id": "REC-TS-2026-3341",
        "state": "Telangana",
        "stateCode": "TS",
        "documentType": "Dharani Pattadar Passbook & Pahani (ధరణి పట్టాదారు పాస్ పుస్తకం)",
        "language": "Telugu (తెలుగు)",
        "script": "Telugu",
        "district": "Medchal-Malkajgiri (మేడ్చల్-మల్కాజిగిరి)",
        "tehsil": "Ghatkesar (ఘట్‌కేసర్)",
        "village": "Kondapur (కొండాపూర్)",
        "mauzaCode": "TS-MED-0211",
        "khasraNo": "218/A/1",
        "khataNo": "9054",
        "subDivision": "A-1",
        "landownerName": "గొల్లపూడి వెంకటేశ్వరరావు (Gollapudi Venkateswara Rao)",
        "fatherSpouseName": "జి. సత్యనారాయణ (G. Satyanarayana)",
        "coOwners": [
            {"name": "గొల్లపూడి లక్ష్మి", "relation": "భార్య (Wife)", "share": "1/1", "shareAreaAcres": 3.15}
        ],
        "totalArea": {
            "value": 3.15,
            "unit": "Acres",
            "conversions": {
                "hectares": 1.2748,
                "bigha": 5.082,
                "biswa": 101.64,
                "sqMeters": 12747.6,
                "guntas": 126.0
            }
        },
        "landClassification": "పట్టా భూమి - మెట్ట (Patta Dry Land - Metta)",
        "irrigationSource": "బోరు బావి (Borewell)",
        "landRevenueTax": "₹ 95.00 / year",
        "soilType": "Red Chalkas (ఎర్ర నేలలు)",
        "encumbrance": "నిల్ (Nil / No Encumbrance)",
        "mutationDetails": {
            "mutationNo": "DHARANI-MUT-2022-7712",
            "date": "20-Apr-2022",
            "type": "క్రయ విక్రయం (Sale Deed)",
            "orderAuthority": "తహసీల్దార్ ఘట్‌కేసర్ (Tahsildar)",
            "status": "Instant Dharani e-Mutation"
        },
        "registrationDetails": {
            "deedNo": "RO-GHAT/1104/2022",
            "sroOffice": "SRO Ghatkesar",
            "registrationDate": "20-04-2022"
        },
        "confidenceScores": {
            "overall": 98.1,
            "landownerName": 99.1,
            "fatherSpouseName": 98.4,
            "khasraNo": 99.5,
            "khataNo": 98.9,
            "totalArea": 97.6,
            "landClassification": 98.0,
            "encumbrance": 93.5
        },
        "status": "Validated",
        "verificationFlags": [],
        "uploadedAt": "2026-08-30T09:10:15Z",
        "verifiedBy": "B. Anand Kumar (Tahsildar)",
        "verifiedAt": "2026-08-30T10:45:00Z",
        "cadastralPlotId": "CAD-TS-MED-218-A1",
        "coordinates": {"lat": 17.4478, "lng": 78.6811},
        "scanImage": "sample_ts_dharani.png",
        "ocrRawText": "తెలంగాణ ప్రభుత్వం - భూ రికార్డుల యాజమాన్య వ్యవస్థ (ధరణి) | జిల్లా: మేడ్చల్-మల్కాజిగిరి | మండలం: ఘట్‌కేసర్ | గ్రామం: కొండాపూర్ | సర్వే నెం: 218/A/1 | ఖాతా నెం: 9054 | విస్తీర్ణం: 3.15 ఎకరాలు | పట్టాదారు పేరు: గొల్లపూడి వెంకటేశ్వరరావు | తండ్రి: జి. సత్యనారాయణ"
    },
    {
        "id": "REC-KA-2026-4402",
        "state": "Karnataka",
        "stateCode": "KA",
        "documentType": "Bhoomi RTC Extract (ಭೂಮಿ ಪಹಣಿ - Form 16)",
        "language": "Kannada (ಕನ್ನಡ)",
        "script": "Kannada",
        "district": "Mysuru (ಮೈಸೂರು)",
        "tehsil": "Hunsur (ಹುಣಸೂರು)",
        "village": "Biligere (ಬಿಳೆಗೆರೆ)",
        "mauzaCode": "KA-MYS-0774",
        "khasraNo": "89/3",
        "khataNo": "512",
        "subDivision": "Hissa 3",
        "landownerName": "ಮಂಜುನಾಥ್ ಬಿ. ಗೌಡ (Manjunath B. Gowda)",
        "fatherSpouseName": "ಬಸವೇಗೌಡ (Basavegowda)",
        "coOwners": [
            {"name": "ಪಾರ್ವತಮ್ಮ", "relation": "ತಾಯಿ (Mother)", "share": "1/2", "shareAreaAcres": 1.00},
            {"name": "ಮಂಜುನಾಥ್ ಗೌಡ", "relation": "ಸ್ವಂತ (Self)", "share": "1/2", "shareAreaAcres": 1.00}
        ],
        "totalArea": {
            "value": 2.00,
            "unit": "Acres",
            "conversions": {
                "hectares": 0.8094,
                "bigha": 3.226,
                "biswa": 64.52,
                "sqMeters": 8093.71,
                "guntas": 80.0
            }
        },
        "landClassification": "ಖುಷ್ಕಿ ಜಮೀನು (Agricultural - Rainfed / Khushki)",
        "irrigationSource": "ಮಳೆ ಆಶ್ರಿತ (Rainfed)",
        "landRevenueTax": "₹ 78.00 / year",
        "soilType": "Red Loam (ಕೆಂಪು ಮಣ್ಣು)",
        "encumbrance": "ಕರ್ನಾಟಕ ಗ್ರಾಮೀಣ ಬ್ಯಾಂಕ್ ಬೆಳೆ ಸಾಲ ₹ 1,20,000 (KGB Crop Loan)",
        "mutationDetails": {
            "mutationNo": "MR-T-142-2021",
            "date": "11-Nov-2021",
            "type": "ವಿಭಾಗ ಪತ್ರ (Partition Deed / Hissa)",
            "orderAuthority": "ಕಂದಾಯ ನಿರೀಕ್ಷಕರು ಹುಣಸೂರು (Revenue Inspector)",
            "status": "Accepted in Bhoomi Engine"
        },
        "registrationDetails": {
            "deedNo": "HNS/3389/2021",
            "sroOffice": "SRO Hunsur",
            "registrationDate": "15-10-2021"
        },
        "confidenceScores": {
            "overall": 95.7,
            "landownerName": 97.8,
            "fatherSpouseName": 98.0,
            "khasraNo": 99.2,
            "khataNo": 97.4,
            "totalArea": 94.8,
            "landClassification": 96.1,
            "encumbrance": 86.9
        },
        "status": "Validated",
        "verificationFlags": [],
        "uploadedAt": "2026-08-31T08:30:10Z",
        "verifiedBy": "K. Chandrashekar (Tahsildar)",
        "verifiedAt": "2026-08-31T12:00:00Z",
        "cadastralPlotId": "CAD-KA-MYS-89-3",
        "coordinates": {"lat": 12.3082, "lng": 76.2914},
        "scanImage": "sample_ka_bhoomi.png",
        "ocrRawText": "ಕರ್ನಾಟಕ ಸರ್ಕಾರ - ಕಂದಾಯ ಇಲಾಖೆ (ಭೂಮಿ ತಂತ್ರಾಂಶ) | ಜಿಲ್ಲೆ: ಮೈಸೂರು | ತಾಲೂಕು: ಹುಣಸೂರು | ಗ್ರಾಮ: ಬಿಳೆಗೆರೆ | ಸರ್ವೆ ನಂಬರ್: 89/3 | ಖಾತಾ ನಂಬರ್: 512 | ವಿಸ್ತೀರ್ಣ: 2.00 ಎಕರೆ (0.80.94 ಹೆಕ್ಟೇರ್) | ಖಾತೇದಾರರ ಹೆಸರು: ಮಂಜುನಾಥ್ ಬಿ. ಗೌಡ ತಂದೆ ಬಸವೇಗೌಡ | ಋಣಭಾರ: ಕೆಜಿಬಿ ಬ್ಯಾಂಕ್ ಸಾಲ"
    },
    {
        "id": "REC-TN-2026-5519",
        "state": "Tamil Nadu",
        "stateCode": "TN",
        "documentType": "Patta Chitta & FMB Extract (பட்டா சிட்டா / புல வரைபடம்)",
        "language": "Tamil (தமிழ்)",
        "script": "Tamil",
        "district": "Coimbatore (கோயம்புத்தூர்)",
        "tehsil": "Pollachi (பொள்ளாச்சி)",
        "village": "Anamalai (ஆனைமலை)",
        "mauzaCode": "TN-CBE-0118",
        "khasraNo": "156/4",
        "khataNo": "1082",
        "subDivision": "புல உட்பிரிவு 4",
        "landownerName": "மு. செந்தில்குமார் (M. Senthilkumar)",
        "fatherSpouseName": "முருகேசன் கவுண்டர் (Murugesan Gounder)",
        "coOwners": [],
        "totalArea": {
            "value": 1.50,
            "unit": "Acres",
            "conversions": {
                "hectares": 0.6070,
                "bigha": 2.42,
                "biswa": 48.4,
                "sqMeters": 6070.28,
                "guntas": 60.0,
                "cents": 150.0
            }
        },
        "landClassification": "நஞ்சை நிலம் (Wet Land / Nanjai)",
        "irrigationSource": "ஆழ்துளை கிணறு மற்றும் வாய்க்கால் (Canal & Tube Well)",
        "landRevenueTax": "₹ 160.00 / year",
        "soilType": "Clay Sandy Loam (களிமண்)",
        "encumbrance": "வில்லங்கம் ஏதுமில்லை (Nil Encumbrance Certificate)",
        "mutationDetails": {
            "mutationNo": "TN-ANYRO-MUT-8840",
            "date": "18-Dec-2023",
            "type": "தான செட்டில்மென்ட் (Gift Settlement)",
            "orderAuthority": "துணை வட்டாட்சியர் பொள்ளாச்சி (Deputy Tahsildar)",
            "status": "Patta Transfer Approved"
        },
        "registrationDetails": {
            "deedNo": "POL/5590/2023",
            "sroOffice": "SRO Pollachi Joint 1",
            "registrationDate": "05-12-2023"
        },
        "confidenceScores": {
            "overall": 97.2,
            "landownerName": 98.6,
            "fatherSpouseName": 97.9,
            "khasraNo": 99.4,
            "khataNo": 98.1,
            "totalArea": 96.5,
            "landClassification": 97.0,
            "encumbrance": 94.0
        },
        "status": "Validated",
        "verificationFlags": [],
        "uploadedAt": "2026-09-01T07:15:20Z",
        "verifiedBy": "P. Selvaraj (Revenue Officer)",
        "verifiedAt": "2026-09-01T11:20:00Z",
        "cadastralPlotId": "CAD-TN-CBE-156-4",
        "coordinates": {"lat": 10.5841, "lng": 76.9312},
        "scanImage": "sample_tn_patta.png",
        "ocrRawText": "தமிழ்நாடு அரசு - வருவாய்த்துறை (இ-சேவை நில உரிமை ஆவணம்) | மாவட்டம்: கோயம்புத்தூர் | வட்டம்: பொள்ளாச்சி | கிராமம்: ஆனைமலை | புல எண்: 156/4 | பட்டா எண்: 1082 | விஸ்தீர்ணம்: 0.60.70 ஹெக்டேர் (1.50 ஏக்கர் / 150 சென்ட்) | நில உரிமையாளர் பெயர்: மு. செந்தில்குமார் த/பெ முருகேசன் | தீர்வை: ₹ 160"
    },
    {
        "id": "REC-WB-2026-6810",
        "state": "West Bengal",
        "stateCode": "WB",
        "documentType": "Banglarbhumi Khatian & Plot Ledger (খতিয়ান ও দাগের তথ্য - ফর্ম খ)",
        "language": "Bengali (বাংলা)",
        "script": "Bengali",
        "district": "Purba Bardhaman (পূর্ব বর্ধমান)",
        "tehsil": "Kalna (কালনা)",
        "village": "Samudragarh (সমুদ্রগড়)",
        "mauzaCode": "WB-BRD-0044",
        "khasraNo": "512/9",
        "khataNo": "2310",
        "subDivision": "দাগ ৯",
        "landownerName": "অনিরুদ্ধ ব্যানার্জী (Aniruddha Banerjee)",
        "fatherSpouseName": "প্রণব ব্যানার্জী (Late Pranab Banerjee)",
        "coOwners": [
            {"name": "সুমনা ব্যানার্জী", "relation": "ভগিনী (Sister)", "share": "1/2", "shareAreaAcres": 0.85},
            {"name": "অনিরুদ্ধ ব্যানার্জী", "relation": "স্বয়ং (Self)", "share": "1/2", "shareAreaAcres": 0.85}
        ],
        "totalArea": {
            "value": 1.70,
            "unit": "Acres",
            "conversions": {
                "hectares": 0.6879,
                "bigha": 5.14,
                "biswa": 102.8,
                "sqMeters": 6879.65,
                "guntas": 68.0,
                "satak": 170.0
            }
        },
        "landClassification": "শালিবাদ / রূপিত কৃষি (Agricultural - Sali Bad)",
        "irrigationSource": "ভাগীরথী নদী সেচ ও ক্যানাল (River Lift Irrigation)",
        "landRevenueTax": "₹ 110.00 / year",
        "soilType": "Gangetic Alluvium (পলি মাটি)",
        "encumbrance": "ক্যানাল কর বকেয়া নাই (No Dues / Clear)",
        "mutationDetails": {
            "mutationNo": "MUT-KAL-WB-2024-118",
            "date": "14-Feb-2024",
            "type": "ওয়ারিশনামা (Succession / Warisan)",
            "orderAuthority": "BL & LRO Kalna II",
            "status": "Finalized in Banglarbhumi"
        },
        "registrationDetails": {
            "deedNo": "KAL/9901/2017",
            "sroOffice": "ADSR Kalna",
            "registrationDate": "12-08-2017"
        },
        "confidenceScores": {
            "overall": 93.9,
            "landownerName": 96.2,
            "fatherSpouseName": 95.4,
            "khasraNo": 98.7,
            "khataNo": 96.0,
            "totalArea": 91.5,
            "landClassification": 94.2,
            "encumbrance": 89.0
        },
        "status": "Validated",
        "verificationFlags": [],
        "uploadedAt": "2026-09-01T14:50:00Z",
        "verifiedBy": "S. Ghosh (Revenue Officer)",
        "verifiedAt": "2026-09-01T18:10:00Z",
        "cadastralPlotId": "CAD-WB-BRD-512-9",
        "coordinates": {"lat": 23.3644, "lng": 88.3562},
        "scanImage": "sample_wb_khatian.png",
        "ocrRawText": "পশ্চিমবঙ্গ সরকার - ভূমি ও ভূমি সংস্কার দপ্তর (বাংলারভূমি) | জেলা: পূর্ব বর্ধমান | ব্লক: কালনা | মৌজা: সমুদ্রগড় | জে.এল. নং: ৪৪ | খতিয়ান নং: ২৩১০ | দাগ নং: ৫১২/৯ | জমির শ্রেণি: শালি | মোট পরিমাণ: ১.৭০ একর (১৭০ শতক) | রায়তের নাম: অনিরুদ্ধ ব্যানার্জী পিতা প্রণব ব্যানার্জী"
    },
    {
        "id": "REC-PB-2026-7201",
        "state": "Punjab",
        "stateCode": "PB",
        "documentType": "Jamabandi Nakal (ਜਮਾਂਬੰਦੀ ਨਕਲ / Fard - ਫ਼ਰਦ)",
        "language": "Punjabi (ਪੰਜਾਬੀ)",
        "script": "Gurmukhi",
        "district": "Ludhiana (ਲੁਧਿਆਣਾ)",
        "tehsil": "Jagraon (ਜਗਰਾਉਂ)",
        "village": "Chowkiman (ਚੌਕੀਮਾਨ)",
        "mauzaCode": "PB-LDH-0089",
        "khasraNo": "65//12/2",
        "khataNo": "144/210",
        "subDivision": "12/2",
        "landownerName": "ਗੁਰਦੀਪ ਸਿੰਘ ਧਾਲੀਵਾਲ (Gurdeep Singh Dhaliwal)",
        "fatherSpouseName": "ਜਗਤਾਰ ਸਿੰਘ (Jagtarsingh)",
        "coOwners": [
            {"name": "ਹਰਪ੍ਰੀਤ ਕੌਰ", "relation": "ਪਤਨੀ (Wife)", "share": "1/2", "shareAreaAcres": 2.00},
            {"name": "ਗੁਰਦੀਪ ਸਿੰਘ", "relation": "ਖੁਦ (Self)", "share": "1/2", "shareAreaAcres": 2.00}
        ],
        "totalArea": {
            "value": 4.00,
            "unit": "Acres",
            "conversions": {
                "hectares": 1.6187,
                "bigha": 6.45,
                "biswa": 129.0,
                "sqMeters": 16187.4,
                "guntas": 160.0,
                "kanal": 32.0,
                "marla": 640.0
            }
        },
        "landClassification": "ਚਾਹੀ ਨਹਿਰੀ (Agricultural - Chahi Nehri)",
        "irrigationSource": "ਸਰਹਿੰਦ ਕੈਨਾਲ ਤੇ ਸੋਲਰ ਟਿਊਬਵੈੱਲ (Canal & Solar Tubewell)",
        "landRevenueTax": "₹ 210.00 / year",
        "soilType": "Alluvial Loam (ਜ਼ਰਖੇਜ਼ ਦੋਮਟ)",
        "encumbrance": "ਪੰਜਾਬ ਨੈਸ਼ਨਲ ਬੈਂਕ ਲਿਮਿਟ ₹ 3,00,000 (PNB Kisan Credit Limit)",
        "mutationDetails": {
            "mutationNo": "ਇੰਤਕਾਲ ਨੰ. ੪੩੨੧ (Intiqal 4321)",
            "date": "04-May-2023",
            "type": "ਬੈਅ ਨਾਮਾ (Registered Sale Deed)",
            "orderAuthority": "ਤਹਿਸੀਲਦਾਰ ਜਗਰਾਉਂ (Tehsildar)",
            "status": "Tasdeeq (Approved)"
        },
        "registrationDetails": {
            "deedNo": "JAG/4412/2023",
            "sroOffice": "SRO Jagraon",
            "registrationDate": "28-04-2023"
        },
        "confidenceScores": {
            "overall": 96.1,
            "landownerName": 98.4,
            "fatherSpouseName": 97.8,
            "khasraNo": 99.1,
            "khataNo": 97.2,
            "totalArea": 95.3,
            "landClassification": 96.8,
            "encumbrance": 90.1
        },
        "status": "Validated",
        "verificationFlags": [],
        "uploadedAt": "2026-09-02T06:10:00Z",
        "verifiedBy": "Harvinder Singh (Naib Tehsildar)",
        "verifiedAt": "2026-09-02T09:40:00Z",
        "cadastralPlotId": "CAD-PB-LDH-65-12",
        "coordinates": {"lat": 30.8312, "lng": 75.5218},
        "scanImage": "sample_pb_jamabandi.png",
        "ocrRawText": "ਮਾਲ ਵਿਭਾਗ ਪੰਜਾਬ (ਪੀ.ਐਲ.ਆਰ.ਐਮ.ਐਸ.) | ਜ਼ਿਲ੍ਹਾ: ਲੁਧਿਆਣਾ | ਤਹਿਸੀਲ: ਜਗਰਾਉਂ | ਪਿੰਡ: ਚੌਕੀਮਾਨ | ਹੱਦਬਸਤ ਨੰ: ੮੯ | ਜਮਾਂਬੰਦੀ ਸਾਲ: ੨੦੨੨-੨੩ | ਖੇਵਟ/ਖਤੌਨੀ: ੧੪੪/੨੧੦ | ਖਸਰਾ ਨੰ: ੬੫//੧੨/੨ | ਰਕਬਾ: ੪ ਏਕੜ (੩੨ ਕਨਾਲ ੦ ਮਰਲੇ) | ਮਾਲਕ ਦਾ ਨਾਮ: ਗੁਰਦੀਪ ਸਿੰਘ ਪੁੱਤਰ ਜਗਤਾਰ ਸਿੰਘ"
    },
    {
        "id": "REC-PENDING-001",
        "state": "Uttar Pradesh",
        "stateCode": "UP",
        "documentType": "Legacy Handwritten Shajra & Khasra Register (हस्तलिखित खसरा पंजी)",
        "language": "Hindi (हिंदी) with Urdu Revenue terms",
        "script": "Handwritten Devanagari / Shikasta",
        "district": "Gorakhpur (गोरखपुर)",
        "tehsil": "Sahjanwa (सहजनवा)",
        "village": "Bhiti Rawat (भीटी रावत)",
        "mauzaCode": "UP-GKP-1102",
        "khasraNo": "88/4-ख",
        "khataNo": "00119",
        "subDivision": "4-ख",
        "landownerName": "दीनानाथ मौर्य (Dinanath Maurya)",
        "fatherSpouseName": "मुंशी सुखदेव मौर्य (Munshi Sukhdev Maurya)",
        "coOwners": [
            {"name": "दीनानाथ मौर्य", "relation": "खातेदार", "share": "3/4", "shareAreaAcres": 1.20},
            {"name": "रामलखन मौर्य", "relation": "भाई (Brother)", "share": "1/4", "shareAreaAcres": 0.40}
        ],
        "totalArea": {
            "value": 1.60,
            "unit": "Acres",
            "conversions": {
                "hectares": 0.6475,
                "bigha": 2.58,
                "biswa": 51.6,
                "sqMeters": 6474.97,
                "guntas": 64.0
            }
        },
        "landClassification": "कृषि भूमि (Agricultural - Barani / Unirrigated)",
        "irrigationSource": "कच्चा कुआं (Unlined Well)",
        "landRevenueTax": "₹ 62.00 / year",
        "soilType": "Loam Sandy (बलुई दोमट)",
        "encumbrance": "अस्पष्ट हस्तलिखित टिप्पणी (Unclear Handwritten Endorsement - Review Needed)",
        "mutationDetails": {
            "mutationNo": "नामान्तरण मिसल संख्या 442 (1984)",
            "date": "10-Jul-1984",
            "type": "फर्द विभाजन (Partition)",
            "orderAuthority": "पेशकार तहसीलदार सहजनवा",
            "status": "Legacy Record - Manual Verification Needed"
        },
        "registrationDetails": {
            "deedNo": "BAHI/1/VOL/94/1979",
            "sroOffice": "SRO Sahjanwa",
            "registrationDate": "04-09-1979"
        },
        "confidenceScores": {
            "overall": 68.4,
            "landownerName": 74.0,
            "fatherSpouseName": 65.2,
            "khasraNo": 82.0,
            "khataNo": 79.5,
            "totalArea": 62.1,
            "landClassification": 71.0,
            "encumbrance": 44.8
        },
        "status": "Review Required",
        "verificationFlags": [
            "Low confidence on Father Name (Faded ink in scan line 4)",
            "Handwritten endorsement in Remarks column requires Tehsildar verification",
            "Co-owner sum validation passed, but boundary orientation ambiguous on cadastral sketch"
        ],
        "uploadedAt": "2026-09-02T11:05:00Z",
        "verifiedBy": None,
        "verifiedAt": None,
        "cadastralPlotId": "CAD-UP-GKP-88-4B",
        "coordinates": {"lat": 26.7588, "lng": 83.2144},
        "scanImage": "sample_handwritten_legacy.png",
        "ocrRawText": "तहसील सहजनवा मौजा भीटी रावत खसरा नं 88/4-ख रकबा 1-12-0 बीघा (1.60 एकड़) खातेदार दीनानाथ मौर्य वल्द मुंशी सुखदेव मौर्य कैफियत [स्याही धुंधली] रहन बतफ़सील दर्ज मिसल नं 442 सन् 1984"
    }
]

# Scope of Study Matrix (Comparative table for reference and documentation)
SCOPE_OF_STUDY_DATA = {
    "title": "Scope of Study & Modernization Benchmark Matrix",
    "description": "Comprehensive comparative evaluation of Traditional Manual Land Record Digitization vs. AI-Powered Bhoomi-AI System.",
    "columns": ["Dimension / Parameter", "Traditional Manual Digitization", "AI-Powered Bhoomi-AI Platform", "DILRMP / Governance Impact"],
    "rows": [
        [
            "Document Ingestion & Multi-Format Support",
            "Manual scanning at 150 DPI; manual sorting of damaged registers, maps, and Urdu/Modi script deeds.",
            "Automated multi-format pipeline (PDF, TIFF, JPEG); AI image enhancement (adaptive binarization, de-skew, denoising, stamp isolation).",
            "90% reduction in document prep time; preserves fragile 100+ year historical deeds digitally."
        ],
        [
            "Multilingual & Regional Script OCR",
            "High transcription error rate (20-35%) when transcribing Devanagari, Telugu, Tamil, Kannada, Bengali, Gurmukhi.",
            "Multi-engine deep learning OCR trained on 22 official Indian languages + historical revenue lexicons (Urdu, Shikasta, Modi).",
            "98.4% field-level accuracy; eliminates phonological transliteration discrepancies in citizen records."
        ],
        [
            "Intelligent Entity Extraction (NER)",
            "Manual typing of Khasra, Khata, Katedar, Father name, Sub-division, and Share into standalone spreadsheets.",
            "Context-aware Transformer & Vision-LLM models automatically segment and structure tabular & narrative land deeds.",
            "Standardizes 150+ regional terms (e.g. Patta, RTC, 7/12, Jamabandi, Khatian, Pahani) into unified national schema."
        ],
        [
            "Automated Business Rule Validation",
            "No real-time validation; arithmetic area errors and double allocations remain undetected for years.",
            "Automated 6-tier validation engine: Area cross-sum verification, Khasra syntax check, LRMS cross-db verification, duplicate detection.",
            "Prevents property fraud, double registration, and boundary dispute litigations at source."
        ],
        [
            "Confidence Scoring & HITL Workflow",
            "Every single document requires 100% human re-keying regardless of quality.",
            "Per-field confidence scoring (0-100%); auto-approves >90% confidence, queues 70-89% for quick review, flags <70% for Tehsildar.",
            "80% reduction in Patwari & Tehsildar verification backlog; average processing drops from 45 min to 18 seconds."
        ],
        [
            "Active Learning & Self-Improvement",
            "Errors repeated continuously; no institutional knowledge retention.",
            "Continuous active learning loop stores human corrections, updating regional vocabulary weights and confusion priors.",
            "Accuracy monotonically improves with each verified batch per district/tehsil."
        ],
        [
            "Cadastral GIS & Spatial Integration",
            "Paper cadastral maps (Shajra / FMB) stored in physical cloth bundles (Basta); no GPS linkage.",
            "GeoJSON Cadastral parcel visualizer with GPS centroids, polygon area calculation, and neighbor boundary cross-validation.",
            "Enables seamless linkage with BharatMaps, PM GatiShakti, SWAMITVA drone surveys, and DILRMP GIS portal."
        ],
        [
            "Audit Trail, Security & Tamper-Evidence",
            "Paper records vulnerable to unauthorized tampering, page tearing, and ink alterations.",
            "Immutable audit trail logging every OCR edit, Tehsildar digital signature, SHA-256 integrity hash, and QR-verified RoR certificates.",
            "Guarantees legal admissibility under Information Technology Act 2000 & Section 65B of Evidence Act."
        ]
    ]
}

# Cadastral GIS GeoJSON Parcels (Mapped to records)
CADASTRAL_PARCELS_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "CAD-UP-VAR-142-1",
            "properties": {
                "recordId": "REC-UP-2026-0842",
                "khasraNo": "142/1",
                "owner": "Rameshwar Prasad Sharma",
                "village": "Phoolpur",
                "district": "Varanasi",
                "state": "Uttar Pradesh",
                "areaAcres": 2.50,
                "classification": "Agricultural - Irrigated",
                "status": "Validated",
                "centroid": [25.4382, 82.8461],
                "color": "#10b981",
                "neighbors": {"North": "142/2", "South": "141", "East": "Village Road", "West": "143/1"}
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [82.8445, 25.4370],
                    [82.8475, 25.4372],
                    [82.8478, 25.4395],
                    [82.8448, 25.4393],
                    [82.8445, 25.4370]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "CAD-MH-PUN-304-2B",
            "properties": {
                "recordId": "REC-MH-2026-1198",
                "khasraNo": "304/2B",
                "owner": "Vitthal Tukaram Patil",
                "village": "Wagholi",
                "district": "Pune",
                "state": "Maharashtra",
                "areaAcres": 1.80,
                "classification": "Agricultural - Jirayat",
                "status": "Validated",
                "centroid": [18.5793, 73.9822],
                "color": "#10b981",
                "neighbors": {"North": "304/2A", "South": "305", "East": "304/3", "West": "Nala Canal"}
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [73.9805, 18.5780],
                    [73.9838, 18.5782],
                    [73.9840, 18.5804],
                    [73.9808, 18.5802],
                    [73.9805, 18.5780]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "CAD-TS-MED-218-A1",
            "properties": {
                "recordId": "REC-TS-2026-3341",
                "khasraNo": "218/A/1",
                "owner": "Gollapudi Venkateswara Rao",
                "village": "Kondapur",
                "district": "Medchal-Malkajgiri",
                "state": "Telangana",
                "areaAcres": 3.15,
                "classification": "Patta Dry Land",
                "status": "Validated",
                "centroid": [17.4478, 78.6811],
                "color": "#10b981",
                "neighbors": {"North": "218/A/2", "South": "217", "East": "219", "West": "Outer Ring Road Link"}
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [78.6790, 17.4460],
                    [78.6830, 17.4462],
                    [78.6832, 17.4495],
                    [78.6793, 17.4493],
                    [78.6790, 17.4460]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "CAD-KA-MYS-89-3",
            "properties": {
                "recordId": "REC-KA-2026-4402",
                "khasraNo": "89/3",
                "owner": "Manjunath B. Gowda",
                "village": "Biligere",
                "district": "Mysuru",
                "state": "Karnataka",
                "areaAcres": 2.00,
                "classification": "Khushki Rainfed",
                "status": "Validated",
                "centroid": [12.3082, 76.2914],
                "color": "#10b981",
                "neighbors": {"North": "89/2", "South": "90", "East": "89/4", "West": "Forest Buffer Zone"}
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [76.2895, 12.3068],
                    [76.2930, 12.3070],
                    [76.2932, 12.3095],
                    [76.2898, 12.3093],
                    [76.2895, 12.3068]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "CAD-UP-GKP-88-4B",
            "properties": {
                "recordId": "REC-PENDING-001",
                "khasraNo": "88/4-ख",
                "owner": "Dinanath Maurya",
                "village": "Bhiti Rawat",
                "district": "Gorakhpur",
                "state": "Uttar Pradesh",
                "areaAcres": 1.60,
                "classification": "Agricultural - Barani",
                "status": "Review Required",
                "centroid": [26.7588, 83.2144],
                "color": "#f59e0b",
                "neighbors": {"North": "88/4-क", "South": "87", "East": "88/5", "West": "Gram Sabha Talab"}
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [83.2128, 26.7575],
                    [83.2160, 26.7577],
                    [83.2162, 26.7600],
                    [83.2130, 26.7598],
                    [83.2128, 26.7575]
                ]]
            }
        }
    ]
}

# Audit Logs
AUDIT_LOGS = [
    {
        "id": "AUD-991",
        "timestamp": "2026-09-02T13:45:12Z",
        "user": "tehsildar_pindra",
        "role": "Tehsildar",
        "action": "DIGITAL_SIGN_ROR",
        "recordId": "REC-UP-2026-0842",
        "details": "Digitally certified RoR extract with QR Code hash 88f7c9e0",
        "ipAddress": "10.14.22.84"
    },
    {
        "id": "AUD-990",
        "timestamp": "2026-09-02T12:20:05Z",
        "user": "patwari_gorakhpur",
        "role": "Patwari",
        "action": "DOCUMENT_UPLOAD",
        "recordId": "REC-PENDING-001",
        "details": "Uploaded legacy handwritten scan 'sample_handwritten_legacy.png'",
        "ipAddress": "10.14.88.19"
    },
    {
        "id": "AUD-989",
        "timestamp": "2026-09-02T11:15:40Z",
        "user": "system_ai_engine",
        "role": "AI OCR & NLP",
        "action": "AUTO_EXTRACTION",
        "recordId": "REC-PENDING-001",
        "details": "Extracted 14 fields with 68.4% aggregate confidence. Flagged for HITL review.",
        "ipAddress": "127.0.0.1"
    },
    {
        "id": "AUD-988",
        "timestamp": "2026-09-01T18:10:00Z",
        "user": "revenue_officer_kalna",
        "role": "Tehsildar",
        "action": "VERIFY_RECORD",
        "recordId": "REC-WB-2026-6810",
        "details": "Verified Banglarbhumi Khatian 2310 and cross-validated with DILRMP",
        "ipAddress": "10.18.44.12"
    }
]

# Active Learning Corrections Store
ACTIVE_LEARNING_CORRECTIONS = [
    {
        "id": "AL-01",
        "recordId": "REC-UP-2026-0842",
        "field": "fatherSpouseName",
        "ocrOriginal": "बद्री नरायन शर्मा",
        "humanCorrected": "बद्री नारायण शर्मा",
        "correctionType": "Spelling / Dialect Normalization",
        "timestamp": "2026-08-28T14:20:00Z",
        "weightAdjusted": "+0.042 (Devanagari Ya/Ra glide prior)"
    },
    {
        "id": "AL-02",
        "recordId": "REC-MH-2026-1198",
        "field": "landClassification",
        "ocrOriginal": "जिरायन",
        "humanCorrected": "जिरायत",
        "correctionType": "OCR Character Confusion (त vs न)",
        "timestamp": "2026-08-29T16:00:00Z",
        "weightAdjusted": "+0.038 (Marathi Revenue Gazetteer boost)"
    }
]

# State-wise Modernization Statistics
STATE_STATS = [
    {"state": "Uttar Pradesh", "districts": 75, "totalRecords": 14200000, "digitized": 13490000, "accuracy": 97.8, "progress": 95.0, "status": "Advanced"},
    {"state": "Maharashtra", "districts": 36, "totalRecords": 9800000, "digitized": 9408000, "accuracy": 98.4, "progress": 96.0, "status": "Advanced"},
    {"state": "Karnataka", "districts": 31, "totalRecords": 6700000, "digitized": 6566000, "accuracy": 98.9, "progress": 98.0, "status": "Near Completion"},
    {"state": "Telangana", "districts": 33, "totalRecords": 4900000, "digitized": 4851000, "accuracy": 99.1, "progress": 99.0, "status": "Dharani Integrated"},
    {"state": "Tamil Nadu", "districts": 38, "totalRecords": 8200000, "digitized": 7954000, "accuracy": 98.2, "progress": 97.0, "status": "Advanced"},
    {"state": "West Bengal", "districts": 23, "totalRecords": 7500000, "digitized": 6900000, "accuracy": 96.5, "progress": 92.0, "status": "In Progress"},
    {"state": "Punjab & Haryana", "districts": 45, "totalRecords": 5800000, "digitized": 5568000, "accuracy": 98.1, "progress": 96.0, "status": "Advanced"},
    {"state": "Madhya Pradesh", "districts": 55, "totalRecords": 8900000, "digitized": 8455000, "accuracy": 97.4, "progress": 95.0, "status": "Advanced"},
    {"state": "Rajasthan", "districts": 50, "totalRecords": 7200000, "digitized": 6624000, "accuracy": 96.1, "progress": 92.0, "status": "In Progress"},
    {"state": "Bihar", "districts": 38, "totalRecords": 9100000, "digitized": 7826000, "accuracy": 94.8, "progress": 86.0, "status": "Special Intensive Drive"}
]

class Database:
    def __init__(self):
        self.records = list(INITIAL_RECORDS)
        self.cadastral = CADASTRAL_PARCELS_GEOJSON
        self.audit_logs = list(AUDIT_LOGS)
        self.active_learning = list(ACTIVE_LEARNING_CORRECTIONS)
        self.state_stats = list(STATE_STATS)

    def get_all_records(self):
        return self.records

    def get_record_by_id(self, record_id):
        for r in self.records:
            if r["id"] == record_id:
                return r
        return None

    def add_record(self, record):
        if not record.get("id"):
            record["id"] = f"REC-NEW-{uuid.uuid4().hex[:8].upper()}"
        self.records.insert(0, record)
        self.log_audit(
            user="patwari_user",
            role="Patwari",
            action="DOCUMENT_INGESTION",
            record_id=record["id"],
            details=f"New document ingested: {record.get('documentType', 'Land Record')}"
        )
        return record

    def update_record(self, record_id, updated_fields, user="tehsildar_user", role="Tehsildar"):
        for i, r in enumerate(self.records):
            if r["id"] == record_id:
                # Track corrections for active learning
                for k, v in updated_fields.items():
                    if k in r and r[k] != v and k not in ["verifiedAt", "verifiedBy", "status"]:
                        self.active_learning.insert(0, {
                            "id": f"AL-{uuid.uuid4().hex[:6].upper()}",
                            "recordId": record_id,
                            "field": k,
                            "ocrOriginal": str(r[k]),
                            "humanCorrected": str(v),
                            "correctionType": "Human Verification Correction",
                            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            "weightAdjusted": "+0.035 (Model Prior Recalibrated)"
                        })

                self.records[i].update(updated_fields)
                self.records[i]["verifiedBy"] = user
                self.records[i]["verifiedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
                
                self.log_audit(
                    user=user,
                    role=role,
                    action="RECORD_VERIFIED_UPDATE",
                    record_id=record_id,
                    details=f"Record updated and approved by {user}"
                )
                return self.records[i]
        return None

    def search_records(self, query=None, state=None, status=None, district=None):
        results = self.records
        if state and state != "All":
            results = [r for r in results if r.get("state") == state or r.get("stateCode") == state]
        if status and status != "All":
            results = [r for r in results if r.get("status") == status]
        if district and district != "All":
            results = [r for r in results if district.lower() in r.get("district", "").lower()]
        if query:
            q = query.lower().strip()
            results = [
                r for r in results
                if q in r.get("id", "").lower()
                or q in r.get("khasraNo", "").lower()
                or q in r.get("khataNo", "").lower()
                or q in r.get("landownerName", "").lower()
                or q in r.get("village", "").lower()
                or q in r.get("district", "").lower()
                or q in r.get("state", "").lower()
            ]
        return results

    def get_cadastral_geojson(self):
        return self.cadastral

    def get_audit_logs(self, limit=50):
        return self.audit_logs[:limit]

    def log_audit(self, user, role, action, record_id, details, ip="127.0.0.1"):
        log_entry = {
            "id": f"AUD-{uuid.uuid4().hex[:6].upper()}",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "user": user,
            "role": role,
            "action": action,
            "recordId": record_id,
            "details": details,
            "ipAddress": ip
        }
        self.audit_logs.insert(0, log_entry)
        return log_entry

    def get_active_learning_feed(self, limit=50):
        return self.active_learning[:limit]

    def get_kpis(self):
        total_docs = len(self.records)
        validated_docs = len([r for r in self.records if r.get("status") == "Validated"])
        review_docs = len([r for r in self.records if r.get("status") == "Review Required"])
        avg_confidence = round(sum(r.get("confidenceScores", {}).get("overall", 90) for r in self.records) / (total_docs or 1), 1)

        return {
            "totalDocuments": total_docs,
            "validatedDocuments": validated_docs,
            "reviewRequired": review_docs,
            "autoValidationPassRate": round((validated_docs / (total_docs or 1)) * 100, 1),
            "averageAccuracy": avg_confidence,
            "activeLearningCorrectionsCount": len(self.active_learning),
            "averageLatencySeconds": 14.8,
            "nationalDigitizationRate": 96.2,
            "stateBreakdown": self.state_stats
        }

db = Database()
