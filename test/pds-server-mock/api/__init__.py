clinical_feature_variables = [
    {
        "id": "v0",
        "title": "t0",
        "why": "w0",
        "legalValues": {
            "type": "i0"
        }
    }, {
        "id": "v1",
        "title": "t1",
        "why": "w1",
        "legalValues": {
            "type": "i1"
        }
    }, {
        "id": "v2",
        "title": "t2",
        "why": "w2",
        "legalValues": {
            "type": "i2"
        }
    }
]

config = [{
    "piid": "pdspi-guidance-example",
    "pluginType": "g",
    "requiredPatientVariables": clinical_feature_variables,
    "enabled": True
}, {
    "piid": "pdspi-guidance-example2",
    "pluginType": "g",
    "requiredPatientVariables": clinical_feature_variables,
    "enabled": False
}, {
    "piid": "pdspi-mapper-example",
    "pluginType": "m",
    "enabled": True
}, {
    "piid": "pdspi-fhir-example",
    "pluginType": "f",
    "enabled": True
}]

custom_units = []

selectors = []

vega_spec_output = {
    "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
    "title": "Line chart",
    "description": "Time-series line chart",
    "width": "container",
    "height": "container",
    "autosize": { "resize": True },
    "data": { "name": "data" },
    "mark": "line",
    "encoding": {
        "x": {
            "field": "x",
            "type": "quantitative",
            "axis": { "title": "Time" }
        },
        "y": {
            "field": "y",
            "type": "quantitative",
            "axis": { "title": "Drug Dosage" }
        }
    }
}

guidance = {
    "title" : "guidance title",
    "id": "guidance id",
    "justification": {},
    "cards": [
    ],
    "vizOutputs": [
    ]
}

phenotypes = {
    "1000": [{
        "id": "v0",
        "title": "t0",
        "variableValue": {
            "value": "a0",
            "units": "u0"
        },
        "certitude": 0,
        "how": "c0",
        "timestamp": "s0"
    }, {
        "id": "v1",
        "title": "t1",
        "variableValue": {
            "value": "a1",
            "units": "u1"
        },
        "certitude": 1,
        "how": "c1",
        "timestamp": "s1"
    }, {
        "id": "v2",
        "title": "t2",
        "variableValue": {
            "value": "a2",
            "units": "u2"
        },
        "certitude": 2,
        "how": "c2",
        "timestamp": "s2"
    }]
}

patients = {
    "1000": {}
}

conditions = {
    "1000": {
        "resourceType": "Bundle",
        "entry": []
    }
}

observations = {
    "1000": {
        "resourceType": "Bundle",
        "entry": []
    }
}

def get_config():
    return [config[0], config[2], config[3]]

def get_custom_units():
    return custom_units

def get_selectors():
    return selectors

def post_guidance(body):
    return guidance

def post_vega_spec(body):
    return vega_spec_output

def post_log(body):
    return None

def get_guidance_example_config():
    return config[0]

def get_guidance_example2_config():
    return config[1]

def get_mapper_config():
    return config[2]

def get_fhir_config():
    return config[3]

def get_patient(ptid):
    return patients.get(ptid, ("not found", 404))

def get_condition(patient):
    return conditions.get(patient, {
        "resourceType": "Bundle",
        "entry": []
    }) 

def get_observation(patient):
    return observations.get(patient, {
        "resourceType": "Bundle",
        "entry": []
    })

def get_phenotype(patient_id, timestamp, body):
    ps = phenotypes.get(patient_id)
    if ps is None:
        return ("Not Found", 404)
    else:
        for p, cfv in zip(ps, clinical_feature_variables):
            cus = [a for a in body["variableTypes"] if a["id"] == cfv["id"]]
            if len(cus) > 0:
                q = cus[0]
                unit = q.get("units")
                if unit is not None:
                    p["units"] = unit
        return ps





