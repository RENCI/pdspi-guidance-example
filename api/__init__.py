import os
import requests

from api.utils import generate_time_series_data, generate_multi_time_series_data, generate_scatter_plot_data, \
    generate_multi_scatter_plot_data, generate_histogram_data, generate_dosing_data


pds_host = os.getenv("PDS_HOST", "localhost")
pds_port = os.getenv("PDS_PORT", "8080")
pds_version = os.getenv("PDS_VERSION", "v1")

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
        "id": "LOINC:29463-7",
        "title": "Weight",
        "legalValues": { "type": "number", "minimum": "0" },
        "why": "Weight is used to calculate the creatinine clearance. Dosing is higher for patients with higher weight"
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


def generate_vis_spec(typeid, x_axis_title, y_axis_title, chart_title, chart_desc):
    json_post_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    vega_spec_input = {
        "typeid": typeid,
        "x_axis_title": x_axis_title,
        "y_axis_title": y_axis_title,
        "chart_title": chart_title,
        "chart_description": chart_desc
    }
    url_str = "http://{}:{}/{}/plugin/tx-vis/vega_spec".format(pds_host, pds_port, pds_version)
    resp = requests.post(url_str, headers=json_post_headers, json=vega_spec_input)
    # resp = requests.post("http://tx-vis:8080/vega_spec", headers=json_post_headers, json=vega_spec_input)
    if resp.status_code == 200:
        return resp.json()
    else:
        return {}


def generate_vis_outputs(age=None, weight=None, bmi=None):
    outputs = [
        {
            "id": "oid-1",
            "name": "Time-series data",
            "description": "Information about time-series data",
            "data": generate_time_series_data(50),
            "specs": [
                generate_vis_spec("line_chart", "X Axis", "Y Axis", "Line chart", "Time-series line chart"),
                generate_vis_spec("area_chart", "X Axis", "Y Axis", "Area chart", "Time-series area chart")
            ]
        },
        {
            "id": "oid-2",
            "name": "Multiple time-series data",
            "description": "Information about multiple time-series data",
            "data": generate_multi_time_series_data(50, 3),
            "specs": [
                generate_vis_spec("multiple_line_chart", "X Axis", "Y Axis", "Multiple line chart",
                                  "Multiple time-series line chart")
            ]
        },
        {
            "id": "oid-3",
            "name": "Scatter plot data",
            "description": "Information about scatter plot data",
            "data": generate_scatter_plot_data(100),
            "specs": [
                generate_vis_spec("scatter_plot", "X Axis", "Y Axis", "Scatter plot", "Two dimensional scatter plot")
            ]
        },
        {
            "id": "oid-4",
            "name": "Multiple class scatter plot data",
            "description": "Information about multiple class scatter plot data",
            "data": generate_multi_scatter_plot_data(100, 2),
            "specs": [
                generate_vis_spec("multiple_scatter_plot", "X Axis", "Y Axis", "Multi-class scatter plot",
                                  "Two dimensional scatter plot with multiple classes")
            ]
        },
        {
            "id": "oid-5",
            "name": "Histogram data",
            "description": "Information about histogram data",
            "data": generate_histogram_data(100),
            "specs": [
                generate_vis_spec("histogram", "X Axis", "Y Axis", "Histogram", "Histogram of counts")
            ]
        },
        {
            "id": "oid-6",
            "name": "Dosing data",
            "description": "Information about dosing data",
            "data": generate_dosing_data(p_age=age, p_weight=weight, p_bmi=bmi),
            "specs": [
                generate_vis_spec("dosing_plot", "Time (hours)", "Concentration (mcg/mL)", "Plot of dosing data",
                                  "Plot of Aminoglycoside concentration graph over time")
            ]
        }
    ]
    return outputs


def get_config():
    return config


def get_guidance(body):
    def extract(var, attr):
        return var.get(attr, next(filter(lambda rpv: rpv["id"] == var["id"], config["requiredPatientVariables"]))[attr])

    inputs = []
    age = None
    weight = None
    bmi = None
    for var in body["userSuppliedPatientVariables"]:
        if var['id'] == 'LOINC:30525-0':
            age = var["variableValue"]['value']
        elif var['id'] == 'LOINC:29463-7':
            weight = var["variableValue"]['value']
        elif var['id'] == 'LOINC:39156-5':
            bmi = var["variableValue"]['value']
        inputs.append({
            "id": var["id"],
            "title": extract(var, "title"),
            "how": var["how"],
            "why": extract(var, "why"),
            "variableValue": var["variableValue"],
            "legalValues": extract(var, "legalValues"),
            "timestamp": var.get("timestamp", "2020-02-18T18:54:57.099Z")
        })
    return {
        **guidance,
        "justification": {
            "inputs": inputs,
            "outputs": generate_vis_outputs(age=age, weight=weight, bmi=bmi)
        }
    }
