from fpdf import FPDF
from PIL import Image
import matplotlib.pyplot as plt
import os

def save_patient_graphs(patient_data, diagnosis_probs, output_folder='temp_graphs'):
    os.makedirs(output_folder, exist_ok=True)
    graph_paths = []

    # Example graph: diagnosis probabilities
    plt.figure(figsize=(8, 4))
    disorders, probs = zip(*diagnosis_probs.items())
    plt.bar(disorders, probs)
    plt.ylabel('Probability')
    plt.title('Disorder Probability Distribution')
    plt.xticks(rotation=90)
    graph_path = os.path.join(output_folder, 'diagnosis_probs.png')
    plt.tight_layout()
    plt.savefig(graph_path)
    plt.close()
    graph_paths.append(graph_path)

    # Add more graphs as needed (e.g., vital stats, features)
    # ... (similar code for each)

    return graph_paths

def generate_pdf_report(patient_data, diagnosis, treatments, reasoning, graph_paths, output_pdf='patient_report.pdf'):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Patient Diagnosis Report', ln=True, align='C')

    # Patient Details
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Patient Details', ln=True)
    for key, value in patient_data.items():
        pdf.cell(0, 8, f'{key}: {value}', ln=True)

    pdf.ln(5)
    # Diagnosis & Confidence
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Diagnosis: {diagnosis}', ln=True)
    pdf.cell(0, 10, f'Confidence: {round(patient_data.get("confidence", 0), 2)}', ln=True)

    pdf.ln(5)
    # Treatments
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Recommended Treatments:', ln=True)
    for treat in treatments:
        pdf.cell(0, 8, f'- {treat}', ln=True)

    pdf.ln(5)
    # Reasoning (optional)
    pdf.cell(0, 10, 'Clinical Reasoning:', ln=True)
    for section, items in reasoning.items():
        pdf.cell(0, 8, f'{section.capitalize()}:', ln=True)
        for item in items:
            pdf.cell(0, 8, f'- {item}', ln=True)

    pdf.ln(5)
    # Graphs
    pdf.cell(0, 10, 'Diagnostic Graphs:', ln=True)
    for graph_path in graph_paths:
        pdf.image(graph_path, w=180)
        pdf.ln(8)

    pdf.output(output_pdf)
    return output_pdf
