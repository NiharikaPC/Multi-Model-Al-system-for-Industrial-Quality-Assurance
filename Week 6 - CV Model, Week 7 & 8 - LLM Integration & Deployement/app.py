# Run using:
# streamlit run app.py

import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import ollama
import pandas as pd
import time
import io
import cv2

from collections import Counter
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


# PAGE CONFIGURATION

st.set_page_config(
    page_title="AI Industrial Quality Assurance",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 AI-Powered Industrial Quality Assurance System")
st.caption(
    "YOLOv8 + Llama 3.2 | Automated Steel Surface Inspection"
)

# SIDEBAR

st.sidebar.title("Model Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=1.00,
    value=0.50,
    step=0.05
)

st.sidebar.markdown("---")
st.sidebar.write("**YOLO Model:** best.pt")
st.sidebar.write("**LLM:** Llama 3.2")
st.sidebar.write("**Framework:** Streamlit")

# LOAD MODEL

@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# FILE UPLOAD

uploaded_file = st.file_uploader(
    "Upload a steel surface image",
    type=["jpg", "jpeg", "png"]
)

# MAIN APP

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as tmp_file:

        image.save(tmp_file.name)
        image_path = tmp_file.name

    # YOLO INFERENCE

    start_time = time.time()

    results = model(
        image_path,
        conf=confidence
    )

    end_time = time.time()

    inference_time = end_time - start_time

    boxes = results[0].boxes
    annotated_image = results[0].plot()

    # KPI METRICS

    total_defects = len(boxes)

    highest_conf = 0

    if total_defects > 0:
        highest_conf = max(
            float(box.conf[0])
            for box in boxes
        )

    if total_defects == 0:
        status = "PASS ✅"

    elif total_defects <= 2:
        status = "NEEDS REVIEW 🟡"

    else:
        status = "REJECT 🔴"

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Total Defects",
        total_defects
    )

    metric2.metric(
        "Highest Confidence",
        f"{highest_conf:.1%}"
    )

    metric3.metric(
        "Overall Status",
        status
    )

    # DISPLAY IMAGES

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Uploaded Image")
        st.image(
            image,
            use_container_width=True
        )

    with col2:
        st.subheader("Detection Result")
        st.image(
            annotated_image,
            use_container_width=True
        )

    st.sidebar.success(
        "Model Loaded Successfully"
    )

    st.sidebar.write(
        f"Inference Time: **{inference_time:.2f} sec**"
    )

    # NO DEFECTS

    if len(boxes) == 0:

        st.warning(
            "No defects detected."
        )

    else:

        st.success(
            f"Detected {len(boxes)} defect(s)."
        )

        detected_defects = []
        table = []

        defect_names = []

        for box in boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            defect_name = model.names[cls]

            defect_names.append(defect_name)

            detected_defects.append(
                f"{defect_name} ({conf:.2%})"
            )

            table.append(
                {
                    "Defect": defect_name,
                    "Confidence": f"{conf:.2%}"
                }
            )

        # DETECTION TABLE

        st.subheader(
            "📋 Detection Summary"
        )
        st.dataframe(
            pd.DataFrame(table),
            use_container_width=True,
            hide_index=True)
       
        # COUNT DEFECTS BY TYPE

        st.subheader(
            "⭐ Count Defects by Type"
        )

        defect_counter = Counter(
            defect_names
        )

        for defect, count in defect_counter.items():

            st.write(
                f"**{defect.title()} : {count}**"
            )

        # IMAGE STATISTICS

        st.subheader(
            "⭐ Image Statistics"
        )

        width, height = image.size

        st.write(
            f"**Image Size:** {width} x {height}"
        )

        st.write(
            f"**Format:** {image.format}"
        )

        # AI REPORT PROMPT

        prompt = f"""
You are an experienced industrial quality inspector.

A steel surface image has been inspected.

Detected defects:

{chr(10).join(detected_defects)}

Generate a professional inspection report.

Include the following sections:

1. Inspection Date
2. Detected Defects
3. Summary
4. Severity (Low / Medium / High)
5. Recommended Actions
6. Overall Quality Status (Pass / Needs Review / Reject)

Keep the report concise, professional and suitable for an industrial quality assurance report.
"""

        # LLM REPORT GENERATION

        with st.spinner("Generating AI Inspection Report..."):

            response = ollama.chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

        report = response["message"]["content"]

        # SHOW REPORT

        with st.expander(
            "📄 AI Inspection Report",
            expanded=True
        ):

            st.markdown(report)

        # DOWNLOAD TXT REPORT

        st.download_button(
            label="📥 Download TXT Report",
            data=report,
            file_name="Inspection_Report.txt",
            mime="text/plain"
        )

        # GENERATE PDF REPORT

        pdf_buffer = io.BytesIO()

        doc = SimpleDocTemplate(pdf_buffer)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b>AI Industrial Quality Assurance Report</b>",
                styles["Title"]
            )
        )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                f"<b>Inspection Date:</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 10))

        story.append(
            Paragraph(
                "<b>Detection Summary</b>",
                styles["Heading2"]
            )
        )

        for defect in detected_defects:

            story.append(
                Paragraph(
                    f"• {defect}",
                    styles["BodyText"]
                )
            )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "<b>AI Inspection Report</b>",
                styles["Heading2"]
            )
        )

        for line in report.split("\n"):

            if line.strip() != "":

                story.append(
                    Paragraph(
                        line,
                        styles["BodyText"]
                    )
                )

        doc.build(story)

        pdf_buffer.seek(0)

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_buffer,
            file_name="Inspection_Report.pdf",
            mime="application/pdf"
        )

        # DOWNLOAD DETECTION IMAGE

        annotated_rgb = cv2.cvtColor(
            annotated_image,
            cv2.COLOR_BGR2RGB
)

        annotated_pil = Image.fromarray(
            annotated_rgb
)
        img_buffer = io.BytesIO()

        annotated_pil.save(
            img_buffer,
            format="PNG"
        )

        img_buffer.seek(0)

        st.download_button(
            label="🖼️ Download Detection Image",
            data=img_buffer,
            file_name="Detection_Result.png",
            mime="image/png"
        )

# FOOTER

st.markdown("---")

st.markdown(
    """
<div style='text-align:center;'>

### 🏭 AI Industrial Quality Assurance System

Developed by **Niharika Chandak**

YOLOv8 • Llama 3.2 • Streamlit

</div>
""",
    unsafe_allow_html=True
)