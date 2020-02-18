import requests


json_headers = {
    "Accept": "application/json"
}


json_post_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


config = {
    "title": "Aminoglycoside dosing guidance",
    "piid": "pdspi-aminoglycoside-nomogram",
    "pluginType": "g",
    "pluginSelectors": [ {
        "title": "Drug",
        "id": "dosing.rxCUI",
        "selectorValue": {
            "value": "rxCUI:1596450",
            "title": "Gentamicin"
        }
    } ],
    "pluginParameterDefaults": [ {
        "id": "pdspi-guidance-example:1",
        "title": "Extended interval nomogram",
        "parameterDescription": "This calculator uses one of four extended-interval nomograms. Please choose one nomogram.",
        "parameterValue": { "value": "Hartford" },
        "legalValues": {
            "type": "string",
            "enum": [ "Hartford", "Urban-Craig", "Conventional A", "Conventional B" ] }
    } ],
    "requiredPatientVariables": [ {
        "id": "LOINC:30525-0",
        "title": "Age",
        "legalValues": { "type": "number", "minimum": "0" },
        "why": "Age is used to calculate the creatinine clearance. Dosing is lower for geriatric patient and contraindicated for pediatric patients"
    }, {
        "id": "LOINC:39156-5",
        "title": "BMI",
        "legalValues": { "type": "number", "minimum": "0" },
        "why": "BMI is used to calculate the creatinine clearance. Dosing is higher for patients with higher BMI"
    }]
}


guidance = {
    "piid": "pdspi-aminoglycoside-nomogram",
    "title": "Aminoglycoside dosing guidance",
    "txid": "38-1",
    "justification": [
        {
            "id": "LOINC:30525-0",
            "title": "Age",
            "how": "The value was specified by the end user.",
            "why": "Age is used to calculate the creatinine clearance. Dosing is lower for geriatric patient and contraindicated for pediatric patients",
            "variableValue": {
                "value": "0.5",
                "units": "years"
            },
            "legalValues": {
                "type": "number",
                "minimum": "0"
            },
            "timestamp": "2020-02-18T18:54:57.099Z"
        }
    ],
    "vizOutputs": [
        {
            "survival": "(x,y),...",
            "pkpd": "(x,y),..."
        }
    ],
    "cards": [
        {
            "id": "string",
            "title": "string",
            "summary": "some <140 char Summary Message",
            "detail": "some sort of optional GitHub Markdown details",
            "indicator": "info",
            "source": {
                "label": "Human-readable source label",
                "url": "https://example.com",
                "icon": "https://example.com/img/icon-100px.png"
            },
            "suggestions": [
                {
                    "uuid": "e1187895-ad57-4ff7-a1f1-ccf954b2fe46",
                    "label": "Human-readable suggestion label",
                    "actions": [
                        {
                            "title": "string",
                            "id": "string",
                            "type": "create",
                            "description": "Create a prescription for Acetaminophen 250 MG",
                            "resource": "MedicationRequest"
                        }
                    ]
                }
            ],
            "selectionBehavior": "string",
            "links": [
                {
                    "label": "SMART Example App",
                    "url": "string",
                    "type": "string",
                    "appContext": "string"
                }
            ]
        }
    ]
}


guidance_input = {
    "piid": "pdspi-guidance-example",
    "ptid": "38",
    "timestamp": "2019-12-03T13:41:09.942+00:00",
    "pluginParameterValues": [ {
        "id": "pdspi-guidance-example:1",
        "title": "Extended interval nomogram",
        "parameterDescription": "This calculator uses one of four extended-interval nomograms. Please choose one nomogram.",
        "parameterValue": { "value": "Hartford" }
    } ],
    "userSuppliedPatientVariables": [ {
        "id": "LOINC:30525-0",
        "title": "Age",
        "variableValue": {
            "value": "0.5",
            "units": "years"
        },
        "how": "The value was specified by the end user.",
        "timestamp": "2019-12-03T13:41:09.942+00:00"
    } ]
}


def test_guidance():
    resp = requests.post("http://pdspi-guidance-example:8080/guidance", headers=json_post_headers, json=guidance_input)

    assert resp.status_code == 200
    assert resp.json() == guidance
    

def test_config():
    resp = requests.get("http://pdspi-guidance-example:8080/config", headers=json_headers)

    assert resp.status_code == 200
    assert resp.json() == config

    
def test_ui():
    resp = requests.get("http://pdspi-guidance-example:8080/ui")

    assert resp.status_code == 200
