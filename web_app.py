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
INSTAGRAM_VERSION = "3.7"  # Increment this when Instagram code changes
APP_VERSION = "2.5.7"  # Main app version
UPDATE_NOTES = "Updated Instagram file naming: 'Instagram - Sold/New/Under Contract - [Address].png' for better organization"  # Brief note about what was updated

# Version history for dropdown
VERSION_HISTORY = {
    "2.5.7": "Updated Instagram file naming: 'Instagram - Sold/New/Under Contract - [Address].png' for better organization",
    "2.5.6": "Added elegant font priority: Cambria, Georgia, Times New Roman, Lato, Open Sans + better serif options",
    "2.5.5": "Switched to DejaVu Sans as primary font - universally available on Streamlit Cloud",
    "2.5.4": "FIXED tiny font issue - added Liberation Sans backup and scaled up emergency default font",
    "2.5.3": "FIXED Liberation Serif loading with multiple paths to restore beautiful November font appearance",
    "2.5.2": "REMOVED DejaVu fonts completely - Liberation/Times/Helvetica/Default only",
    "2.5.1": "RESTORED: Back to original working Liberation Serif font that was working in Streamlit Cloud",
    "2.5.0": "MAJOR FIX: Web-first font loading to avoid DejaVu fonts entirely in cloud deployment",
    "2.4.5": "Improved font priority to avoid DejaVu and reduced text spacing to 75px for better layout",
    "2.4.4": "Prioritized Helvetica font over DejaVu and reduced sizes to 65pt/45pt for better visual appearance",
    "2.4.3": "Optimized Instagram font sizes - reduced to 70pt/50pt for better visual balance",
    "2.4.2": "Fixed Instagram font loading for cloud deployment - added web-friendly font fallbacks",
    "2.4.1": "Fixed Instagram post font sizes - increased to 80pt/60pt for proper social media visibility",
    "2.4.0": "Added refresh button for multiple properties and recent downloads section for quick file access",
    "2.3.0": "Fixed font consistency across all Instagram post types and reduced text spacing to prevent cutoff",
    "2.2.0": "Reverted to original font sizes (59pt/40pt) and added debugging to diagnose font loading issues",
    "2.1.6": "Increased Instagram post text size for better readability - street address now 80pt, city/state 60pt",
    "2.1.5": "Fixed photo upload conditional visibility - now properly hides when neither cover page nor Instagram posts are selected",
    "2.1.4": "Reorganized photo upload section - moved to top and made conditionally visible based on selected features",
    "2.1.3": "Moved Instagram-only button to packet settings for better workflow organization",
    "2.1.2": "Added '1)' prefix to packet filenames for better organization and sorting", 
    "2.1.1": "Fixed cover image scaling - Photos now maintain aspect ratio and fit properly",
    "2.1.0": "Added PDF compression and version tracking system", 
    "2.0.0": "Complete web application with    # Version information at bottomcover pages, and compression",
    "1.0.0": "Initial desktop application with basic PDF combining functionality"
}

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
            temp_cropped_photo = tempfile.mktemp(suffix='_cropped.jpg')
            try:
                with open(temp_photo, 'wb') as f:
                    f.write(photo_bytes)
                
                # Define target dimensions for photo area
                target_width = page_width  # Full page width
                target_height = 7.12 * inch  # Exactly 7.12 inches tall
                target_aspect = target_width / target_height
                
                # Load and process the image to maintain aspect ratio
                if PIL_AVAILABLE:
                    img = Image.open(temp_photo)
                    img_width, img_height = img.size
                    img_aspect = img_width / img_height
                    
                    # Determine how to crop the image to fit the target aspect ratio
                    if img_aspect > target_aspect:
                        # Image is wider than target - crop the width
                        new_height = img_height
                        new_width = int(new_height * target_aspect)
                        left = (img_width - new_width) // 2
                        crop_box = (left, 0, left + new_width, new_height)
                    else:
                        # Image is taller than target - crop the height
                        new_width = img_width
                        new_height = int(new_width / target_aspect)
                        top = (img_height - new_height) // 2
                        crop_box = (0, top, new_width, top + new_height)
                    
                    # Crop and save the processed image
                    cropped_img = img.crop(crop_box)
                    cropped_img.save(temp_cropped_photo, 'JPEG', quality=95)
                    
                    # Use the cropped image
                    final_photo_path = temp_cropped_photo
                else:
                    # Fallback to original image if PIL not available
                    final_photo_path = temp_photo
                
                # Position for photo area
                photo_x = 0  # Start at absolute left edge
                photo_y = page_height - target_height  # Position from top: 11" - 7.12" = 3.88" from bottom
                
                # Draw the properly cropped photo over the template
                c.drawImage(final_photo_path, photo_x, photo_y, width=target_width, height=target_height)
                
            except Exception as e:
                st.warning(f"Could not add photo overlay: {e}")
            finally:
                # Clean up temporary files
                for temp_file in [temp_photo, temp_cropped_photo]:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
        
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
        
        # Load fonts once at the beginning for consistency across all posts
        main_font = None
        small_font = None
        main_font_details = ""
        small_font_details = ""
        
        # Load main font (65pt) - Try prettier fonts first, then fall back to universals
        main_font_loaded = False
        
        # Try prettier, more elegant fonts first
        elegant_fonts = [
            # Microsoft fonts (if available)
            ("/usr/share/fonts/truetype/msttcorefonts/cambria.ttf", "Cambria"),
            ("/usr/share/fonts/truetype/msttcorefonts/georgia.ttf", "Georgia"),
            ("/usr/share/fonts/truetype/msttcorefonts/times.ttf", "Times New Roman"),
            # Google Fonts (sometimes available)
            ("/usr/share/fonts/truetype/lato/Lato-Regular.ttf", "Lato"),
            ("/usr/share/fonts/truetype/opensans/OpenSans-Regular.ttf", "Open Sans"),
            # Linux serif alternatives
            ("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", "Liberation Serif"),
            ("/usr/share/fonts/truetype/libertinus/LibertinusSerif-Regular.otf", "Libertinus Serif"),
            # Standard but clean fonts
            ("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", "DejaVu Serif"),
            ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVu Sans"),
        ]
        
        for font_path, font_name in elegant_fonts:
            try:
                main_font = ImageFont.truetype(font_path, 65)
                main_font_details = f"{font_name} at 65pt - FOUND at {font_path}"
                main_font_loaded = True
                break
            except Exception as e:
                continue
        
        if not main_font_loaded:
            try:
                # Try macOS fonts for local development (including Cambria if available)
                for font_path, font_name in [
                    ("/System/Library/Fonts/Cambria.ttc", "Cambria (macOS)"),
                    ("/System/Library/Fonts/Georgia.ttf", "Georgia (macOS)"),
                    ("/System/Library/Fonts/Times.ttc", "Times (macOS)"),
                    ("/System/Library/Fonts/Helvetica.ttc", "Helvetica (macOS)")
                ]:
                    try:
                        main_font = ImageFont.truetype(font_path, 65)
                        main_font_details = f"{font_name} at 65pt"
                        main_font_loaded = True
                        break
                    except:
                        continue
            except:
                pass
        
        if not main_font_loaded:
            # Last resort - default font
            main_font = ImageFont.load_default()
            main_font_details = "LAST RESORT: Basic default font - no system fonts found"
        
        # Load small font (45pt) - Match the elegant main font
        small_font_loaded = False
        
        # If we successfully loaded an elegant font for main font, use same for small font
        if main_font_loaded and not "default" in main_font_details.lower():
            for font_path, font_name in elegant_fonts:
                try:
                    small_font = ImageFont.truetype(font_path, 45)
                    small_font_details = f"{font_name} at 45pt - FOUND at {font_path}"
                    small_font_loaded = True
                    break
                except:
                    continue
        
        if not small_font_loaded:
            try:
                # Try macOS fonts for local development
                for font_path, font_name in [
                    ("/System/Library/Fonts/Cambria.ttc", "Cambria (macOS)"),
                    ("/System/Library/Fonts/Georgia.ttf", "Georgia (macOS)"),
                    ("/System/Library/Fonts/Times.ttc", "Times (macOS)"),
                    ("/System/Library/Fonts/Helvetica.ttc", "Helvetica (macOS)")
                ]:
                    try:
                        small_font = ImageFont.truetype(font_path, 45)
                        small_font_details = f"{font_name} at 45pt"
                        small_font_loaded = True
                        break
                    except:
                        continue
            except:
                pass
        
        if not small_font_loaded:
            # Use the main font as fallback
            small_font = main_font
            small_font_details = "Using main font as fallback"
        
        # Log font loading results with detailed debugging
        st.success(f"✅ Main font loaded: {main_font_details}")
        st.success(f"✅ Small font loaded: {small_font_details}")
        
        # Show font quality level
        if any(elegant in main_font_details for elegant in ["Cambria", "Georgia", "Times New Roman", "Lato", "Open Sans"]):
            st.success("🎨 PREMIUM FONT: Using elegant typography!")
        elif any(good in main_font_details for good in ["Liberation Serif", "Libertinus", "DejaVu Serif"]):
            st.info("✨ GOOD FONT: Using professional serif font")
        elif "DejaVu Sans" in main_font_details:
            st.info("📝 STANDARD FONT: Using clean sans-serif")
        elif "macOS" in main_font_details:
            st.info("🍎 Using macOS system font - testing locally")
        elif "default" in main_font_details.lower():
            st.error("⚠️ BASIC FONT: No system fonts available - text may be small")
        
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
                        
                        # Use pre-loaded font
                        font = main_font
                        st.info(f"🔍 {post_type} - Using font: {main_font_details}")
                        
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
                        text_bbox = draw.textbbox((0, 0), street_address_upper, font=font)
                        rendered_text_height = text_bbox[3] - text_bbox[1]
                        st.info(f"🔍 {post_type} - Street address height: {rendered_text_height}px (expected ~70px for 70pt font)")
                        draw.text(text_position, street_address_upper, fill=text_color, font=font)
                        
                        # Add city/state below street address if available
                        if city_state:
                            try:
                                # Use pre-loaded small font and reduce spacing
                                city_font = small_font
                                st.info(f"🔍 {post_type} - Using small font: {small_font_details}")
                                
                                # Convert city/state to uppercase for consistent branding
                                city_state_upper = city_state.upper()
                                
                                # Position city/state below street address with same alignment
                                if text_alignment == "centered_offset":
                                    city_text_width = draw.textbbox((0, 0), city_state_upper, font=city_font)[2]
                                    city_x_final = (post_width // 2) - (city_text_width // 2) + text_x
                                elif text_alignment == "centered":
                                    city_text_width = draw.textbbox((0, 0), city_state_upper, font=city_font)[2]
                                    city_x_final = (post_width - city_text_width) // 2  # Perfect center
                                else:
                                    city_x_final = text_x
                                
                                # Reduced spacing: 75px between lines (was 90px) to bring city/state closer
                                city_position = (city_x_final, text_y + 75)
                                draw.text(city_position, city_state_upper, fill=text_color, font=city_font)
                            except Exception as city_e:
                                st.warning(f"Could not add city/state text: {city_e}")
                        
                    except Exception as text_e:
                        st.warning(f"Could not add address text to {post_type}: {text_e}")
                
                # Convert to bytes for download
                output_buffer = BytesIO()
                instagram_post.save(output_buffer, format='PNG', quality=95)
                
                created_files.append({
                    'name': f"Instagram - {post_type} - {street_address}.png",
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

def compress_pdf(pdf_bytes, target_size_mb=20):
    """Compress PDF to reduce file size"""
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        # Read the PDF
        reader = PdfReader(BytesIO(pdf_bytes))
        writer = PdfWriter()
        
        # Add all pages with compression
        for page in reader.pages:
            # Compress page content
            page.compress_content_streams()
            writer.add_page(page)
        
        # Set compression level
        writer.add_metadata(reader.metadata)
        
        # Write compressed PDF
        output_buffer = BytesIO()
        writer.write(output_buffer)
        compressed_bytes = output_buffer.getvalue()
        
        # Check if we achieved target size
        original_size_mb = len(pdf_bytes) / (1024 * 1024)
        compressed_size_mb = len(compressed_bytes) / (1024 * 1024)
        
        st.info(f"📊 PDF Compression: {original_size_mb:.1f} MB → {compressed_size_mb:.1f} MB ({(1 - compressed_size_mb/original_size_mb)*100:.1f}% reduction)")
        
        return compressed_bytes
        
    except Exception as e:
        st.warning(f"Could not compress PDF: {e}. Using original file.")
        return pdf_bytes

def create_packet(pdf_files, street_address, city_state, cover_photo_bytes, include_cover, compress_pdf_option=True):
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
        
        pdf_bytes = output_buffer.getvalue()
        
        # Apply compression if requested
        if compress_pdf_option:
            pdf_bytes = compress_pdf(pdf_bytes)
        
        return pdf_bytes
        
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
    if 'instagram_version' not in st.session_state:
        st.session_state.instagram_version = ""
    
    # Check if Instagram code has been updated - force regeneration if so
    if st.session_state.instagram_version != INSTAGRAM_VERSION:
        if st.session_state.instagram_files:  # Only clear if there were Instagram files
            st.session_state.instagram_files = []
            st.session_state.processing_complete = False
            st.session_state.packet_summary = ""
        st.session_state.instagram_version = INSTAGRAM_VERSION
    
    # Custom CSS for Hall Collins branding
    st.markdown("""
    <style>
    .main-header {
        color: #E91E63;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
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
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown("### ✨ Features")
        
        st.markdown("**📄 PDF Combining**\nMerge multiple PDFs into one professional packet")
        st.markdown("**🗜️ PDF Compression**\nReduces file sizes under 20MB for easy sharing")
        st.markdown("**📁 ZIP Support**\nAutomatically extracts PDFs from ZIP files")
        st.markdown("**�️ JPG to PDF**\nConvert JPG images to PDF format")
        st.markdown("**🏠 Custom Covers**\nAdd branded cover pages with property photos")
        st.markdown("**📱 Instagram Posts**\nCreate 3 social media posts (New, Under Contract, Sold)")
        st.markdown("**🎨 Hall Collins Branding**\nProfessional templates with company colors")
        st.markdown("**☁️ Web Based**\nNo software installation required")
        
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
    st.markdown("### 📋 Step 1: Packet Settings")
    st.markdown("*Add just the address if you want a regular showing packet. Check the boxes if you want a branded packet for our listing.*")
    
    # Create columns for settings
    settings_col1, settings_col2 = st.columns([1, 1])
    
    with settings_col1:
        # Address input
        street_address = st.text_input("📍 Street Address", placeholder="123 Main Street")
        city_state = st.text_input("🏙️ City, State", placeholder="Woodstock, VT")
        
        # Cover page options
        include_cover = st.checkbox("📄 Include Custom Cover Page", value=False, disabled=not COVER_AVAILABLE)
        if not COVER_AVAILABLE:
            st.warning("⚠️ Cover page feature requires additional libraries. Install reportlab and Pillow.")
    
    with settings_col2:
        # Instagram posts option (defined first so it can be used in conditional logic)
        include_instagram = st.checkbox("📱 Create Instagram Posts", value=False, disabled=not PIL_AVAILABLE)
        if not PIL_AVAILABLE:
            st.warning("⚠️ Instagram posts require Pillow library.")
        elif include_instagram:
            st.info("📸 Will create 3 Instagram posts: New Listing, Under Contract, Sold")
        
        # Property photo upload - shown only when cover page or Instagram posts are needed
        cover_photo = None
        if (include_cover and COVER_AVAILABLE) or include_instagram:
            cover_photo = st.file_uploader("📸 Property Photo", type=['jpg', 'jpeg', 'png'], 
                                         help="Required for cover page and Instagram posts. Can create Instagram posts without uploading documents.")
        
        # PDF compression option
        compress_pdf_option = st.checkbox("🗜️ Compress PDF Files", value=True, 
                                         help="Reduces file size for easier sharing. Recommended for files over 20MB.")
        if compress_pdf_option:
            st.info("📉 Will compress PDFs to reduce file size")
    
    st.markdown("---")
    
    # File processing area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📁 Step 2: Upload Files")
        st.markdown("*When selecting files, click them in the order you want them to appear in the packet*")
        
        # Refresh button for new property
        if st.button("🔄 New Property", help="Clear all inputs and start fresh with a new property", use_container_width=True, type="secondary"):
            # Clear all session state
            st.session_state.packet_data = None
            st.session_state.instagram_files = []
            st.session_state.packet_filename = ""
            st.session_state.processing_complete = False
            st.session_state.packet_summary = ""
            st.success("✨ Ready for new property!")
            st.rerun()
        
        # File upload
        uploaded_files = st.file_uploader(
            "Select PDF, JPG, or ZIP files",
            type=['pdf', 'zip', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="Upload multiple PDF files, ZIP archives, or JPG images to combine into a listing packet"
        )
        
        # Recent downloads section (web equivalent)
        with st.expander("📥 Quick Upload Tips", expanded=False):
            st.markdown("""
            **💡 Pro Tips for File Organization:**
            • Upload files in the order you want them in the packet
            • Use descriptive filenames for better organization  
            • ZIP files will be automatically extracted
            • JPG images will be converted to PDF format
            • Multiple files can be selected at once
            
            **📂 Recommended File Order:**
            1. MLS listing sheet
            2. Property disclosures
            3. HOA documents (if applicable)
            4. Property photos/floor plans
            5. Additional documents
            """)
        
        if uploaded_files:
            st.markdown("#### 📋 Selected Files")
            for file in uploaded_files:
                file_size = len(file.getvalue()) / 1024  # KB
                st.write(f"• {file.name} ({file_size:.1f} KB)")
        
        # Instagram-only button (when photo and address are provided but no files uploaded)
        elif cover_photo and street_address and city_state and PIL_AVAILABLE:
            st.markdown("#### 📱 Create Instagram Posts Only")
            st.info("📸 Upload property photo and enter address to create social media posts without documents")
            if st.button("🎨 Create Instagram Posts", type="secondary", use_container_width=True):
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
    
    with col2:
        st.markdown("### 🔧 Processing")
        
        # Show persistent results if available
        if st.session_state.processing_complete:
            st.success("✅ Files ready for download!")
            
            # Show version update warning if applicable
            if st.session_state.instagram_files and st.session_state.instagram_version != INSTAGRAM_VERSION:
                st.warning("📱 Instagram posts updated! Click 'Create New Files' below to regenerate with improved fonts.")
            
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
                            include_cover,
                            compress_pdf_option
                        )
                        
                        # Create Instagram posts if requested
                        instagram_files = []
                        if include_instagram and cover_photo_bytes and PIL_AVAILABLE and street_address and city_state:
                            with st.spinner("Creating Instagram posts..."):
                                instagram_files = create_instagram_posts(cover_photo_bytes, street_address, city_state)
                        
                        if packet_bytes:
                            # Store results in session state
                            if street_address:
                                filename = f"1) {street_address} - Packet.pdf"
                            else:
                                filename = "1) Listing Packet.pdf"
                            
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
        
        elif not st.session_state.processing_complete:
            if cover_photo and PIL_AVAILABLE:
                st.info("📱 Enter address information above to create Instagram posts, or upload files to create a full listing packet")
            else:
                st.info("👆 Upload files to get started")
    
    # Footer
    st.markdown("---")
    
    # Version information at bottom
    st.markdown(f"""
    <div style="text-align: center; color: #999; font-size: 0.75rem; margin-bottom: 0.5rem;">
        Version {APP_VERSION} • {UPDATE_NOTES}
    </div>
    """, unsafe_allow_html=True)
    
    # Version history dropdown
    with st.expander("📋 Version History", expanded=False):
        st.markdown("### Release Notes")
        for version, notes in VERSION_HISTORY.items():
            if version == APP_VERSION:
                st.markdown(f"**{version}** (Current): {notes}")
            else:
                st.markdown(f"**{version}**: {notes}")
    
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
        "Hall Collins Real Estate Group • Professional Listing Packet Creator"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
