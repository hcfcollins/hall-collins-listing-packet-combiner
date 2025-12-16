#!/usr/bin/env python3
"""
Hall Collins Listing Packet Combiner - Web Application
Streamlit version for web browser access
"""

import streamlit as st
import os
import tempfile
import zipfile
import shutil
from io import BytesIO
import base64
from PyPDF2 import PdfMerger
import PyPDF2

# Enhanced error handling for optional libraries
COVER_AVAILABLE = False
PIL_AVAILABLE = False
REPORTLAB_AVAILABLE = False

# Test ReportLab
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

# Test PIL/Pillow
try:
    from PIL import Image
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# Final determination
COVER_AVAILABLE = REPORTLAB_AVAILABLE and PIL_AVAILABLE

def parse_address(full_address):
    """Parse full address into street address and city/state"""
    parts = [part.strip() for part in full_address.split(',')]
    
    if len(parts) >= 3:
        street = parts[0]
        city_state = f"{parts[1]}, {parts[2]}"
    elif len(parts) == 2:
        street = parts[0]
        city_state = parts[1]
    else:
        words = full_address.split()
        if len(words) >= 2:
            street = ' '.join(words[:-1])
            city_state = words[-1]
        else:
            street = full_address
            city_state = ""
    
    return street, city_state

def create_cover_page(photo_bytes, street_address, city_state, output_path):
    """Create custom cover page using uploaded photo"""
    if not COVER_AVAILABLE:
        return False
    
    try:
        # Use standard letter size
        page_width = 8.5 * inch
        page_height = 11 * inch
        
        c = canvas.Canvas(output_path, pagesize=(page_width, page_height))
        
        # Add property photo
        if photo_bytes:
            temp_photo = tempfile.mktemp(suffix='.jpg')
            with open(temp_photo, 'wb') as f:
                f.write(photo_bytes)
            
            # Calculate photo dimensions (maintain aspect ratio)
            photo_width = 6 * inch
            photo_height = 4 * inch
            photo_x = (page_width - photo_width) / 2
            photo_y = page_height - photo_height - 2 * inch
            
            c.drawImage(temp_photo, photo_x, photo_y, photo_width, photo_height)
            os.unlink(temp_photo)
        
        # Add Hall Collins branding
        c.setFillColor(colors.HexColor('#2C3E50'))
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(page_width / 2, 1.5 * inch, "HALL COLLINS")
        
        c.setFillColor(colors.HexColor('#E91E63'))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(page_width / 2, 1.2 * inch, "REAL ESTATE GROUP")
        
        # Add property address
        if street_address:
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(page_width / 2, 0.8 * inch, street_address)
        
        if city_state:
            c.setFont("Helvetica", 14)
            c.drawCentredString(page_width / 2, 0.5 * inch, city_state)
        
        c.save()
        return True
        
    except Exception as e:
        st.error(f"Error creating cover page: {e}")
        return False

def extract_pdfs_from_zip(zip_bytes):
    """Extract PDF files from ZIP archive"""
    pdf_files = []
    
    try:
        with zipfile.ZipFile(BytesIO(zip_bytes), 'r') as zip_ref:
            for file_info in zip_ref.filelist:
                if file_info.filename.lower().endswith('.pdf'):
                    pdf_content = zip_ref.read(file_info.filename)
                    pdf_files.append({
                        'name': file_info.filename,
                        'content': pdf_content
                    })
        return pdf_files
    except Exception as e:
        st.error(f"Error extracting ZIP: {e}")
        return []

def convert_jpg_to_pdf(jpg_bytes, filename):
    """Convert JPG to PDF"""
    if not PIL_AVAILABLE:
        return None
    
    try:
        # Create PDF from JPG
        img = Image.open(BytesIO(jpg_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pdf_bytes = BytesIO()
        img.save(pdf_bytes, format='PDF')
        
        return {
            'name': filename.replace('.jpg', '.pdf').replace('.jpeg', '.pdf'),
            'content': pdf_bytes.getvalue()
        }
    except Exception as e:
        st.error(f"Error converting JPG to PDF: {e}")
        return None

def create_packet(pdf_files, street_address, city_state, cover_photo_bytes, include_cover):
    """Create the final PDF packet"""
    try:
        merger = PdfMerger()
        
        # Add cover page if requested
        if include_cover and cover_photo_bytes and COVER_AVAILABLE:
            cover_path = tempfile.mktemp(suffix='_cover.pdf')
            if create_cover_page(cover_photo_bytes, street_address, city_state, cover_path):
                with open(cover_path, 'rb') as f:
                    merger.append(f)
                os.unlink(cover_path)
        
        # Add all PDFs
        for pdf_file in pdf_files:
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file['content']))
            for page in pdf_reader.pages:
                merger.append(page)
        
        # Create output
        output_buffer = BytesIO()
        merger.write(output_buffer)
        merger.close()
        
        return output_buffer.getvalue()
        
    except Exception as e:
        st.error(f"Error creating packet: {e}")
        return None

def main():
    # Page configuration
    st.set_page_config(
        page_title="Hall Collins Listing Packet Combiner",
        page_icon="🏡",
        layout="wide"
    )
    
    # Custom CSS for Hall Collins branding
    st.markdown("""
    <style>
    .main-header {
        color: #2C3E50;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #E91E63;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background-color: #E91E63;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #C2185B;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🏡 Hall Collins Listing Packet Combiner</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Professional Real Estate Listing Packet Creator</p>', unsafe_allow_html=True)
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown("### 📋 Packet Settings")
        
        # Address input
        street_address = st.text_input("📍 Street Address", placeholder="123 Main Street")
        city_state = st.text_input("🏙️ City, State", placeholder="Woodstock, VT")
        
        # Cover page options
        include_cover = st.checkbox("📄 Include Custom Cover Page", value=False, disabled=not COVER_AVAILABLE)
        if not COVER_AVAILABLE:
            st.warning("⚠️ Cover page feature requires additional libraries. Install reportlab and Pillow.")
        
        # Property photo upload
        cover_photo = None
        if include_cover and COVER_AVAILABLE:
            cover_photo = st.file_uploader("📸 Property Photo", type=['jpg', 'jpeg', 'png'])
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📁 Upload Files")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Select PDF, JPG, or ZIP files",
            type=['pdf', 'zip', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="Upload multiple PDF files, ZIP archives, or JPG images to combine into a listing packet"
        )
        
        if uploaded_files:
            st.markdown("#### 📋 Selected Files")
            for file in uploaded_files:
                file_size = len(file.getvalue()) / 1024  # KB
                st.write(f"• {file.name} ({file_size:.1f} KB)")
    
    with col2:
        st.markdown("### 🔧 Processing")
        
        if uploaded_files:
            if st.button("🔗 Create Listing Packet", type="primary"):
                with st.spinner("Processing files..."):
                    # Process uploaded files
                    pdf_files = []
                    
                    for uploaded_file in uploaded_files:
                        file_bytes = uploaded_file.getvalue()
                        file_name = uploaded_file.name.lower()
                        
                        if file_name.endswith('.pdf'):
                            pdf_files.append({
                                'name': uploaded_file.name,
                                'content': file_bytes
                            })
                        elif file_name.endswith('.zip'):
                            extracted_pdfs = extract_pdfs_from_zip(file_bytes)
                            pdf_files.extend(extracted_pdfs)
                            st.success(f"Extracted {len(extracted_pdfs)} PDFs from {uploaded_file.name}")
                        elif file_name.endswith(('.jpg', '.jpeg')):
                            converted_pdf = convert_jpg_to_pdf(file_bytes, uploaded_file.name)
                            if converted_pdf:
                                pdf_files.append(converted_pdf)
                                st.success(f"Converted {uploaded_file.name} to PDF")
                    
                    if pdf_files:
                        # Get cover photo bytes
                        cover_photo_bytes = cover_photo.getvalue() if cover_photo else None
                        
                        # Create packet
                        packet_bytes = create_packet(
                            pdf_files, 
                            street_address, 
                            city_state, 
                            cover_photo_bytes, 
                            include_cover
                        )
                        
                        if packet_bytes:
                            # Create filename
                            if street_address:
                                filename = f"{street_address} - Packet.pdf"
                            else:
                                filename = "Listing Packet.pdf"
                            
                            # Provide download button
                            st.success("✅ Packet created successfully!")
                            st.download_button(
                                label="📥 Download Listing Packet",
                                data=packet_bytes,
                                file_name=filename,
                                mime="application/pdf"
                            )
                            
                            # Show summary
                            st.info(f"""
                            **Packet Summary:**
                            • Combined {len(pdf_files)} files
                            • Cover page: {'✅ Included' if include_cover and cover_photo_bytes else '❌ Not included'}
                            • Property: {street_address or 'No address specified'}
                            • Location: {city_state or 'No location specified'}
                            """)
                    else:
                        st.error("No valid PDF files found to process")
        else:
            st.info("👆 Upload files to get started")
    
    # Features section
    st.markdown("---")
    st.markdown("### ✨ Features")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**📄 PDF Combining**\nMerge multiple PDFs into one professional packet")
    with col2:
        st.markdown("**📁 ZIP Support**\nAutomatically extracts PDFs from ZIP files")
    with col3:
        st.markdown("**🖼️ JPG to PDF**\nConvert JPG images to PDF format")
    with col4:
        st.markdown("**🏠 Custom Covers**\nAdd branded cover pages with property photos")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
        "Hall Collins Real Estate Group • Professional Listing Packet Creator"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
