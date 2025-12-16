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
    """Create custom cover page matching the original desktop app design"""
    if not COVER_AVAILABLE:
        return False
    
    try:
        # Use standard letter size - 8.5" x 11"
        page_width = 8.5 * inch
        page_height = 11 * inch
        
        # Create the PDF
        c = canvas.Canvas(output_path, pagesize=(page_width, page_height))
        
        # First, draw the Hall Collins template as the base (full page)
        template_image_path = "templates/1) HC -  Template Bottom Photo.png"
        if os.path.exists(template_image_path):
            try:
                # Draw the complete template first - covers entire page
                c.drawImage(template_image_path, 0, 0, width=page_width, height=page_height)
            except Exception as e:
                st.warning(f"Could not add template base: {e}")
        else:
            st.warning(f"Template file not found: {template_image_path}")
        
        # Add property photo overlay (covers the photo area of the template)
        if photo_bytes:
            temp_photo = tempfile.mktemp(suffix='.jpg')
            try:
                with open(temp_photo, 'wb') as f:
                    f.write(photo_bytes)
                
                # Cover exactly 7.12" from the top of the page (photo area only)
                photo_width = page_width  # Full page width
                photo_height = 7.12 * inch  # Exactly 7.12 inches tall
                photo_x = 0  # Start at absolute left edge
                photo_y = page_height - photo_height  # Position from top: 11" - 7.12" = 3.88" from bottom
                
                # Draw photo over the template - covers exactly 7.12" from top
                c.drawImage(temp_photo, photo_x, photo_y, width=photo_width, height=photo_height)
                
            except Exception as e:
                st.warning(f"Could not add photo overlay: {e}")
            finally:
                if os.path.exists(temp_photo):
                    os.unlink(temp_photo)
        
        # Add Hall Collins white logo overlay on the photo
        logo_overlay_path = "templates/HC_Solid White Logo_Transparent Back.png"
        if os.path.exists(logo_overlay_path):
            try:
                # Size the logo 50% larger (5.75" * 1.5 = 8.625" wide)
                logo_width = 8.625 * inch
                logo_img = PIL_AVAILABLE and Image.open(logo_overlay_path)
                if logo_img:
                    logo_height = logo_img.height * (logo_width / logo_img.width)
                    
                    # Position logo centered horizontally, with CENTER 1" from top
                    logo_x = (page_width - logo_width) / 2
                    logo_y = page_height - (1.0 * inch) - (logo_height / 2)
                    
                    c.drawImage(logo_overlay_path, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')
                
            except Exception as logo_e:
                st.warning(f"Could not add logo overlay: {logo_e}")
        
        # Add address text overlays on the photo
        if street_address:
            try:
                # Try fonts in order of preference - using regular (non-bold) fonts
                font_name = "Times-Roman"
                for font_option in ["PlayfairDisplay-Regular", "EBGaramond-Regular", "Times-Roman"]:
                    try:
                        c.setFont(font_option, 36)
                        font_name = font_option
                        break
                    except:
                        continue
                
                c.setFillColor(colors.white)
                # Position street address text on the photo - convert to uppercase
                street_address_upper = street_address.upper()
                text_width = c.stringWidth(street_address_upper, font_name, 36)
                x_position = (page_width - text_width) / 2
                c.drawString(x_position, 3.21 * inch, street_address_upper)
            except Exception as text_e:
                st.warning(f"Could not add street address: {text_e}")
        
        if city_state:
            try:
                # Try fonts in order of preference - using regular (non-bold) fonts  
                font_name = "Times-Roman"
                for font_option in ["PlayfairDisplay-Regular", "EBGaramond-Regular", "Times-Roman"]:
                    try:
                        c.setFont(font_option, 24)
                        font_name = font_option
                        break
                    except:
                        continue
                
                c.setFillColor(colors.white)
                # Position city/state text on the photo - convert to uppercase
                city_state_upper = city_state.upper()
                text_width = c.stringWidth(city_state_upper, font_name, 24)
                x_position = (page_width - text_width) / 2
                c.drawString(x_position, 2.58 * inch, city_state_upper)
            except Exception as text_e:
                st.warning(f"Could not add city/state: {text_e}")
        
        # Save the PDF
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

def create_instagram_posts(photo_bytes, street_address, city_state):
    """Create 3 Instagram posts using template PNG files and property photo"""
    if not PIL_AVAILABLE:
        return []
        
    created_files = []
    
    # Instagram post specifications
    post_width = 1080  # pixels
    post_height = 1350  # pixels
    photo_width = 1080  # Match post width for proper aspect ratio
    photo_height = int(1085.2)  # pixels - reduced by 5 pixels to avoid covering colored banner
    
    # Template files with specific positioning and colors for each type
    templates = [
        ("templates/Instagram New Post Template.png", "New Listing", "centered_offset", 100, 1206, "white"),
        ("templates/Instagram Under Contract Post Template.png", "Under Contract", "centered_offset", 100, 1206, "#173348"),
        ("templates/Instagram Sold Post Template.png", "Sold", "centered_offset", 100, 1206, "#173348")
    ]
    
    try:
        from PIL import ImageDraw, ImageFont
        
        for template_file, post_type, text_alignment, text_x, text_y, text_color in templates:
            if not os.path.exists(template_file):
                st.warning(f"Template not found: {template_file}")
                continue
                
            try:
                # Create new image with Instagram dimensions
                instagram_post = Image.new('RGB', (post_width, post_height), 'white')
                
                # Load and apply template as background
                template_img = Image.open(template_file)
                template_img = template_img.resize((post_width, post_height), Image.Resampling.LANCZOS)
                
                if template_img.mode == 'RGBA':
                    instagram_post.paste(template_img, (0, 0), template_img)
                else:
                    instagram_post.paste(template_img, (0, 0))
                
                # Overlay property photo
                if photo_bytes:
                    property_photo = Image.open(BytesIO(photo_bytes))
                    
                    # Calculate proper cropping to maintain aspect ratio
                    original_width, original_height = property_photo.size
                    target_aspect = photo_width / photo_height
                    original_aspect = original_width / original_height
                    
                    if original_aspect > target_aspect:
                        # Photo is wider than needed, crop width
                        new_height = original_height
                        new_width = int(new_height * target_aspect)
                        left = (original_width - new_width) // 2
                        crop_box = (left, 0, left + new_width, new_height)
                    else:
                        # Photo is taller than needed, crop height
                        new_width = original_width
                        new_height = int(new_width / target_aspect)
                        top = (original_height - new_height) // 2
                        crop_box = (0, top, new_width, top + new_height)
                    
                    # Crop and resize to exact specifications
                    property_photo = property_photo.crop(crop_box)
                    property_photo = property_photo.resize((photo_width, photo_height), Image.Resampling.LANCZOS)
                    
                    # Paste photo at top center
                    photo_x = (post_width - photo_width) // 2
                    photo_y = 0
                    instagram_post.paste(property_photo, (photo_x, photo_y))
                
                # Add address text overlay
                if street_address:
                    try:
                        draw = ImageDraw.Draw(instagram_post)
                        
                        # Try to load a font - size 59 to match original app
                        try:
                            # Try to use a system font - size 59 matches original desktop app
                            font = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 59)
                        except:
                            try:
                                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 59)
                            except:
                                # Fall back to default font
                                font = ImageFont.load_default()
                        
                        # Convert street address to uppercase for consistent branding
                        street_address_upper = street_address.upper()
                        
                        # Calculate text positioning based on post type - exact logic from original
                        if text_alignment == "centered_offset":
                            # For Under Contract: center text with offset
                            text_width = draw.textbbox((0, 0), street_address_upper, font=font)[2]
                            text_x_final = (post_width // 2) - (text_width // 2) + text_x  # Center and offset by text_x
                        elif text_alignment == "centered":
                            # For New Listing and Sold: center text perfectly
                            text_width = draw.textbbox((0, 0), street_address_upper, font=font)[2]
                            text_x_final = (post_width - text_width) // 2  # Perfect center
                        else:
                            # For other cases: use absolute positioning
                            text_x_final = text_x
                        
                        text_position = (text_x_final, text_y)
                        
                        # Add street address text with specified color
                        draw.text(text_position, street_address_upper, fill=text_color, font=font)
                        
                        # Add city/state below street address if available
                        if city_state:
                            try:
                                # Use font size 40 to match original app
                                try:
                                    small_font = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 40)  # Matches original desktop app
                                except:
                                    try:
                                        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)  # Matches original desktop app
                                    except:
                                        small_font = font  # Use same font if others fail
                                
                                # Convert city/state to uppercase for consistent branding
                                city_state_upper = city_state.upper()
                                
                                # Position city/state below street address with same alignment
                                if text_alignment == "centered_offset":
                                    city_text_width = draw.textbbox((0, 0), city_state_upper, font=small_font)[2]
                                    city_x_final = (post_width // 2) - (city_text_width // 2) + text_x
                                elif text_alignment == "centered":
                                    city_text_width = draw.textbbox((0, 0), city_state_upper, font=small_font)[2]
                                    city_x_final = (post_width - city_text_width) // 2  # Perfect center
                                else:
                                    city_x_final = text_x
                                
                                city_position = (city_x_final, text_y + 100)  # Adjusted spacing for proportional fonts
                                draw.text(city_position, city_state_upper, fill=text_color, font=small_font)
                            except Exception as city_e:
                                st.warning(f"Could not add city/state text: {city_e}")
                        
                    except Exception as text_e:
                        st.warning(f"Could not add address text to {post_type}: {text_e}")
                
                # Convert to bytes for download
                output_buffer = BytesIO()
                instagram_post.save(output_buffer, format='PNG', quality=95)
                
                created_files.append({
                    'name': f"{street_address} - {post_type} - Instagram.png",
                    'data': output_buffer.getvalue(),
                    'type': post_type
                })
                
            except Exception as e:
                st.warning(f"Could not create {post_type} Instagram post: {e}")
                continue
                
    except Exception as e:
        st.error(f"Error creating Instagram posts: {e}")
    
    return created_files

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
            try:
                # Create a BytesIO object from the PDF content
                pdf_stream = BytesIO(pdf_file['content'])
                merger.append(pdf_stream)
            except Exception as e:
                st.warning(f"Could not process {pdf_file['name']}: {e}")
                continue
        
        # Create output
        output_buffer = BytesIO()
        merger.write(output_buffer)
        merger.close()
        
        return output_buffer.getvalue()
        
    except Exception as e:
        st.error(f"Error creating packet: {e}")
        return None

def get_hall_collins_logo():
    """Get Hall Collins logo as base64 for display in web app"""
    try:
        # Try templates folder first, then root directory
        for logo_path in ["templates/hall_collins_logo.png", "hall_collins_logo.png"]:
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                if len(logo_data) > 0:  # Make sure file isn't empty
                    return base64.b64encode(logo_data).decode()
    except Exception:
        pass
    return None

def main():
    # Page configuration
    st.set_page_config(
        page_title="Hall Collins Listing Packet Combiner",
        page_icon="🏡",
        layout="wide"
    )
    
    # Initialize session state
    if 'packet_data' not in st.session_state:
        st.session_state.packet_data = None
    if 'instagram_files' not in st.session_state:
        st.session_state.instagram_files = []
    if 'packet_filename' not in st.session_state:
        st.session_state.packet_filename = ""
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    if 'packet_summary' not in st.session_state:
        st.session_state.packet_summary = ""
    
    # Custom CSS for Hall Collins branding
    st.markdown("""
    <style>
    .main-header {
        color: #2C3E50;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        margin-top: 0;
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
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    # Get Hall Collins logo
    logo_base64 = get_hall_collins_logo()
    
    if logo_base64:
        # Display logo and title together
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Center the logo
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <img src="data:image/png;base64,{logo_base64}" style="width: 300px; max-width: 100%; height: auto;">
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<h1 class="main-header">Listing Packet Combiner</h1>', unsafe_allow_html=True)
    else:
        # Fallback to text-only header
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
        
        # Instagram posts option
        include_instagram = st.checkbox("📱 Create Instagram Posts", value=False, disabled=not PIL_AVAILABLE)
        if not PIL_AVAILABLE:
            st.warning("⚠️ Instagram posts require Pillow library.")
        elif include_instagram:
            st.info("📸 Will create 3 Instagram posts: New Listing, Under Contract, Sold")
        
        # Property photo upload
        cover_photo = None
        if (include_cover and COVER_AVAILABLE) or (include_instagram and PIL_AVAILABLE) or PIL_AVAILABLE:
            cover_photo = st.file_uploader("📸 Property Photo", type=['jpg', 'jpeg', 'png'], 
                                         help="Required for cover page and Instagram posts. Can create Instagram posts without uploading documents.")
        
        # Reset button
        st.markdown("---")
        if st.button("🔄 Reset All", help="Clear all generated files and start fresh"):
            st.session_state.packet_data = None
            st.session_state.instagram_files = []
            st.session_state.packet_filename = ""
            st.session_state.processing_complete = False
            st.session_state.packet_summary = ""
            st.rerun()
    
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
        
        # Show persistent results if available
        if st.session_state.processing_complete:
            st.success("✅ Files ready for download!")
            
            # Create columns for download buttons
            download_col1, download_col2 = st.columns(2)
            
            # PDF download button
            if st.session_state.packet_data:
                with download_col1:
                    st.download_button(
                        label="📥 Download Listing Packet",
                        data=st.session_state.packet_data,
                        file_name=st.session_state.packet_filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
            
            # Instagram posts download buttons
            if st.session_state.instagram_files:
                with download_col2:
                    st.success(f"📱 {len(st.session_state.instagram_files)} Instagram posts ready!")
                
                for instagram_file in st.session_state.instagram_files:
                    st.download_button(
                        label=f"📱 Download {instagram_file['type']} Post",
                        data=instagram_file['data'],
                        file_name=instagram_file['name'],
                        mime="image/png",
                        key=f"persistent_download_{instagram_file['type']}",
                        use_container_width=True
                    )
            
            # Show summary
            if st.session_state.packet_summary:
                st.info(st.session_state.packet_summary)
            
            # Add reprocess button for users who want to make changes
            if st.button("🔄 Create New Files", help="Clear results and start over with new files or settings"):
                st.session_state.packet_data = None
                st.session_state.instagram_files = []
                st.session_state.packet_filename = ""
                st.session_state.processing_complete = False
                st.session_state.packet_summary = ""
                st.rerun()
            
            st.markdown("---")
        
        # PDF Packet Creation
        if uploaded_files and not st.session_state.processing_complete:
            st.markdown("#### 📄 Create Full Listing Packet")
            if st.button("�🔗 Create Listing Packet", type="primary", use_container_width=True):
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
                        
                        # Check if address is required for cover page or Instagram posts
                        if (include_cover or include_instagram) and cover_photo_bytes:
                            if not street_address or not city_state:
                                st.error("⚠️ Please enter both street address and city/state for cover page and Instagram posts!")
                                st.stop()
                        
                        # Create packet
                        packet_bytes = create_packet(
                            pdf_files, 
                            street_address, 
                            city_state, 
                            cover_photo_bytes, 
                            include_cover
                        )
                        
                        # Create Instagram posts if requested
                        instagram_files = []
                        if include_instagram and cover_photo_bytes and PIL_AVAILABLE and street_address and city_state:
                            with st.spinner("Creating Instagram posts..."):
                                instagram_files = create_instagram_posts(cover_photo_bytes, street_address, city_state)
                        
                        if packet_bytes:
                            # Store results in session state
                            if street_address:
                                filename = f"{street_address} - Packet.pdf"
                            else:
                                filename = "Listing Packet.pdf"
                            
                            st.session_state.packet_data = packet_bytes
                            st.session_state.packet_filename = filename
                            st.session_state.instagram_files = instagram_files
                            
                            # Create summary
                            summary = f"""
                            **Packet Summary:**
                            • Combined {len(pdf_files)} files
                            • Cover page: {'✅ Included' if include_cover and cover_photo_bytes else '❌ Not included'}
                            • Instagram posts: {'✅ Created ' + str(len(instagram_files)) + ' posts' if instagram_files else '❌ Not created'}
                            • Property: {street_address or 'No address specified'}
                            • Location: {city_state or 'No location specified'}
                            """
                            st.session_state.packet_summary = summary
                            st.session_state.processing_complete = True
                            
                            # Rerun to show persistent download buttons
                            st.rerun()
                    else:
                        st.error("No valid PDF files found to process")
        
        # Standalone Instagram Posts option
        elif cover_photo and street_address and city_state and PIL_AVAILABLE:
            st.markdown("#### 📱 Create Instagram Posts Only")
            if st.button("🎨 Create Instagram Posts", type="secondary"):
                with st.spinner("Creating Instagram posts..."):
                    cover_photo_bytes = cover_photo.getvalue()
                    instagram_files = create_instagram_posts(cover_photo_bytes, street_address, city_state)
                    
                    if instagram_files:
                        # Store only Instagram results in session state
                        st.session_state.packet_data = None
                        st.session_state.packet_filename = ""
                        st.session_state.instagram_files = instagram_files
                        
                        # Create summary for Instagram only
                        summary = f"""
                        **Instagram Posts Created:**
                        • Created {len(instagram_files)} social media posts
                        • Property: {street_address}
                        • Location: {city_state}
                        • Posts: New Listing, Under Contract, Sold
                        """
                        st.session_state.packet_summary = summary
                        st.session_state.processing_complete = True
                        
                        # Rerun to show download buttons
                        st.rerun()
                    else:
                        st.error("Could not create Instagram posts")
        
        elif not st.session_state.processing_complete:
            if cover_photo and PIL_AVAILABLE:
                st.info("📱 Enter address information above to create Instagram posts, or upload files to create a full listing packet")
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
    
    # Second row of features
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**📱 Instagram Posts**\nCreate 3 social media posts (New, Under Contract, Sold)")
    with col2:
        st.markdown("**🎨 Hall Collins Branding**\nProfessional templates with company colors")
    with col3:
        st.markdown("**☁️ Web Based**\nNo software installation required")
    with col4:
        st.markdown("**📱 Mobile Ready**\nWorks on phones, tablets, and computers")
    
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
