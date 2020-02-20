config = {
    "title": "Aminoglycoside dosing guidance",
    "piid": "pdspi-guidance-example",
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
    "piid": "pdspi-guidance-example",
    "title": "Aminoglycoside dosing guidance",
    "txid": "38-1",
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


def get_config():
    return config

def get_guidance(body):
    def extract(var, attr):
        return var.get(attr, next(filter(lambda rpv: rpv["id"] == var["id"], config["requiredPatientVariables"]))[attr])
    return {
        **guidance,
        "justification": [
            {
                "id": var["id"],
                "title": extract(var, "title"),
                "how": var["how"],
                "why": extract(var, "why"),
                "variableValue": var["variableValue"],
                "legalValues": extract(var, "legalValues"),
                "timestamp": var.get("timestamp", "2020-02-18T18:54:57.099Z")
            } for var in body["userSuppliedPatientVariables"]
        ]
    }
