#!/usr/bin/env python3
"""
Ultra Simple PDF Combiner - No complex GUI updates
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import zipfile
import tempfile
import shutil
from PyPDF2 import PdfMerger
import PyPDF2

# Additional imports for cover page with enhanced error handling
COVER_AVAILABLE = False
PIL_AVAILABLE = False
REPORTLAB_AVAILABLE = False

# Test ReportLab
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    
    # Test functionality
    import tempfile
    test_path = tempfile.mktemp(suffix='.pdf')
    test_canvas = canvas.Canvas(test_path)
    test_canvas.save()
    os.unlink(test_path)
    
    REPORTLAB_AVAILABLE = True
    print("DEBUG: ReportLab loaded and tested successfully")
    
except Exception as e:
    print(f"DEBUG: ReportLab failed: {e}")
    REPORTLAB_AVAILABLE = False

# Test PIL/Pillow
try:
    from PIL import Image, ImageTk
    
    # Test functionality
    test_img = Image.new('RGB', (1, 1))
    
    PIL_AVAILABLE = True
    print("DEBUG: PIL/Pillow loaded and tested successfully")
    
except Exception as e:
    print(f"DEBUG: PIL/Pillow failed: {e}")
    PIL_AVAILABLE = False

# Final determination
COVER_AVAILABLE = REPORTLAB_AVAILABLE and PIL_AVAILABLE
print(f"DEBUG: Final status - ReportLab: {REPORTLAB_AVAILABLE}, PIL: {PIL_AVAILABLE}, Cover Available: {COVER_AVAILABLE}")

# Force the variables to be available globally
globals()['COVER_AVAILABLE'] = COVER_AVAILABLE
globals()['PIL_AVAILABLE'] = PIL_AVAILABLE
globals()['REPORTLAB_AVAILABLE'] = REPORTLAB_AVAILABLE

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

def create_cover_page(template_path, photo_path, street_address, city_state, output_path):
    """Create custom cover page by drawing everything from scratch - no template merging"""
    if not COVER_AVAILABLE:
        return False
        
    try:
        # Use standard letter size - 8.5" x 11"
        page_width = 8.5 * inch
        page_height = 11 * inch
        
        # Create the PDF directly without template merging
        c = canvas.Canvas(output_path, pagesize=(page_width, page_height))
        
        # First, draw the Hall Collins template as the base (full page)
        template_image_path = "templates/1) HC -  Template Bottom Photo.png"
        if os.path.exists(template_image_path):
            try:
                # Draw the complete template first - covers entire page
                c.drawImage(template_image_path, 0, 0, width=page_width, height=page_height)
                print(f"DEBUG: Template base drawn - {page_width/inch:.2f}\" x {page_height/inch:.2f}\"")
            except Exception as e:
                print(f"Warning: Could not add template base: {e}")
        else:
            print(f"Warning: Template file not found: {template_image_path}")
        
        # Add property photo overlay (covers the photo area of the template)
        if photo_path and os.path.exists(photo_path):
            try:
                # Cover exactly 7.12" from the top of the page (photo area only)
                photo_width = page_width  # Full page width
                photo_height = 7.12 * inch  # Exactly 7.12 inches tall
                photo_x = 0  # Start at absolute left edge
                photo_y = page_height - photo_height  # Position from top: 11" - 7.12" = 3.88" from bottom
                
                # Draw photo over the template - covers exactly 7.12" from top
                c.drawImage(photo_path, photo_x, photo_y, width=photo_width, height=photo_height)
                print(f"DEBUG: Photo overlay drawn at ({photo_x}, {photo_y}) - {photo_width/inch:.2f}\" x {photo_height/inch:.2f}\" (exactly 7.12\" tall)")
                
            except Exception as e:
                print(f"Warning: Could not add photo overlay: {e}")
        
        # Add Hall Collins white logo overlay on the photo
        logo_overlay_path = "templates/HC_Solid White Logo_Transparent Back.png"
        if os.path.exists(logo_overlay_path):
            try:
                # Size the logo 50% larger (5.75" * 1.5 = 8.625" wide)
                logo_width = 8.625 * inch
                logo_img = Image.open(logo_overlay_path)
                logo_height = logo_img.height * (logo_width / logo_img.width)
                
                # Position logo centered horizontally, with CENTER 1" from top
                logo_x = (page_width - logo_width) / 2
                logo_y = page_height - (1.0 * inch) - (logo_height / 2)
                
                c.drawImage(logo_overlay_path, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')
                print(f"DEBUG: Logo added at ({logo_x}, {logo_y}) - {logo_width/inch:.2f}\" wide, center 1\" from top")
                
            except Exception as logo_e:
                print(f"Warning: Could not add logo overlay: {logo_e}")
        
        # Add address text overlays on the photo
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
                print(f"DEBUG: Street address added with {font_name}")
            except Exception as text_e:
                print(f"Warning: Could not add street address: {text_e}")
        
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
                print(f"DEBUG: City/State added with {font_name}")
            except Exception as text_e:
                print(f"Warning: Could not add city/state: {text_e}")
        
        # Save the PDF directly - no template merging needed
        c.save()
        print("DEBUG: Cover page created directly without template merging")
        return True
            
    except Exception as e:
        print(f"Error creating cover page: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_instagram_posts(photo_path, street_address, city_state, output_dir):
    """Create 3 Instagram posts using template PNG files and property photo"""
    if not COVER_AVAILABLE:
        return []
        
    created_files = []
    
    # Instagram post specifications
    post_width = 1080  # pixels
    post_height = 1350  # pixels
    photo_width = 1080  # Match post width for proper aspect ratio
    photo_height = int(1085.2)  # pixels - reduced by 5 pixels to avoid covering colored banner
    
    # Template files with specific positioning and colors for each type
    templates = [
        ("templates/Instagram New Post Template.png", "New Listing", "centered_offset", 100, 1206, "white"),  # Centered with 100px right offset, Y=1206 (1" from bottom), white text
        ("templates/Instagram Under Contract Post Template.png", "Under Contract", "centered_offset", 100, 1206, "#173348"),  # Centered with 100px offset, Y=1206 (same as New Listing), navy text
        ("templates/Instagram Sold Post Template.png", "Sold", "centered_offset", 100, 1206, "#173348")  # Centered with 100px offset, Y=1206 (same as others), navy text
    ]
    
    try:
        # Import ImageDraw and ImageFont for text overlay
        from PIL import ImageDraw, ImageFont
        
        for template_file, post_type, text_alignment, text_x, text_y, text_color in templates:
            if not os.path.exists(template_file):
                print(f"Warning: Template not found: {template_file}")
                continue
                
            try:
                # Create new image with Instagram dimensions
                instagram_post = Image.new('RGB', (post_width, post_height), 'white')
                print(f"DEBUG: Created base Instagram post {post_width}x{post_height} for {post_type}")
                
                # Load and apply template as BACKGROUND FIRST
                if os.path.exists(template_file):
                    template_img = Image.open(template_file)
                    print(f"DEBUG: Loaded template {template_file}, original size: {template_img.size}, mode: {template_img.mode}")
                    
                    # Resize template to Instagram dimensions if needed
                    template_img = template_img.resize((post_width, post_height), Image.Resampling.LANCZOS)
                    print(f"DEBUG: Resized template to: {template_img.size}")
                    
                    # Apply template as the base background
                    if template_img.mode == 'RGBA':
                        instagram_post.paste(template_img, (0, 0), template_img)
                    else:
                        instagram_post.paste(template_img, (0, 0))
                    print(f"DEBUG: Template applied as background for {post_type}")
                    
                    # Save a debug version of the template background
                    debug_template_filename = f"DEBUG_TEMPLATE_BACKGROUND_{post_type}.png"
                    debug_template_path = os.path.join(output_dir, debug_template_filename)
                    instagram_post.save(debug_template_path, 'PNG')
                    print(f"DEBUG: Saved template background: {debug_template_filename}")
                else:
                    print(f"DEBUG: Template file not found: {template_file}")
                
                # NOW overlay property photo on top of template
                if photo_path and os.path.exists(photo_path):
                    print(f"DEBUG: Loading property photo from: {photo_path}")
                    property_photo = Image.open(photo_path)
                    print(f"DEBUG: Original property photo size: {property_photo.size}")
                    
                    # Calculate proper cropping to maintain aspect ratio and fit dimensions
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
                    print(f"DEBUG: Cropped and resized property photo to: {property_photo.size}")
                    
                    # Paste photo at top-left (now it should fit perfectly)
                    photo_x = (post_width - photo_width) // 2  # Center horizontally
                    photo_y = 0  # Start at top of post
                    
                    instagram_post.paste(property_photo, (photo_x, photo_y))
                    print(f"DEBUG: Property photo overlaid on template at ({photo_x}, {photo_y}) - final size {property_photo.size}")
                    
                    # Save a debug version to see the photo over template
                    debug_filename = f"DEBUG_PHOTO_OVER_TEMPLATE_{post_type}.png"
                    debug_path = os.path.join(output_dir, debug_filename)
                    instagram_post.save(debug_path, 'PNG')
                    print(f"DEBUG: Saved photo-over-template image: {debug_filename}")
                    
                else:
                    print(f"DEBUG: No property photo found or path invalid: {photo_path}")
                    print(f"DEBUG: Photo exists: {os.path.exists(photo_path) if photo_path else 'No path provided'}")
                
                # Add address text overlay with specific positioning and colors
                if street_address:
                    try:
                        draw = ImageDraw.Draw(instagram_post)
                        
                        # Try to load a font - fall back to default if needed
                        try:
                            # Try to use a system font - size 59 (51 * 1.15) for additional 15% increase
                            font = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 59)
                        except:
                            try:
                                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 59)
                            except:
                                # Fall back to default font
                                font = ImageFont.load_default()
                        
                        # Convert street address to uppercase for consistent branding
                        street_address_upper = street_address.upper()
                        
                        # Calculate text positioning based on post type
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
                        print(f"DEBUG: Added street address '{street_address_upper}' at {text_position} for {post_type} in color {text_color}")
                        
                        # Add city/state below street address if available
                        if city_state:
                            try:
                                # Use smaller font for city/state
                                try:
                                    small_font = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 40)  # 35 * 1.15 for additional 15% increase
                                except:
                                    try:
                                        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)  # 35 * 1.15 for additional 15% increase
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
                                
                                city_position = (city_x_final, text_y + 60)
                                draw.text(city_position, city_state_upper, fill=text_color, font=small_font)
                                print(f"DEBUG: Added city/state '{city_state_upper}' at {city_position} for {post_type} in color {text_color}")
                            except Exception as city_e:
                                print(f"Warning: Could not add city/state text: {city_e}")
                        
                    except Exception as text_e:
                        print(f"Warning: Could not add address text to {post_type}: {text_e}")
                
                # Create filename
                safe_street = "".join(c for c in street_address if c.isalnum() or c in (' ', '-', '_')).strip()
                filename = f"{safe_street} - {post_type} - Instagram.png"
                output_path = os.path.join(output_dir, filename)
                
                # Save Instagram post
                instagram_post.save(output_path, 'PNG', quality=95)
                created_files.append(output_path)
                print(f"DEBUG: Created Instagram post: {filename}")
                
            except Exception as e:
                print(f"Warning: Could not create {post_type} Instagram post: {e}")
                continue
                
    except Exception as e:
        print(f"Error creating Instagram posts: {e}")
        import traceback
        traceback.print_exc()
    
    return created_files

def select_cover_photo():
    """Select a photo for the cover page"""
    if not COVER_AVAILABLE:
        messagebox.showwarning("Libraries Required", 
                             "Cover page features require additional libraries.\n\n" + 
                             "To enable these features:\n" +
                             "1. Double-click 'INSTALL_REQUIREMENTS.command'\n" +
                             "2. Or manually run: pip3 install reportlab pillow\n\n" +
                             "Basic PDF combining is still available without libraries.")
        return
    
    # Update button to show we're opening dialog
    cover_photo_btn.config(text="Opening...")
    root.update_idletasks()
        
    file_path = filedialog.askopenfilename(
        title="Select Property Photo for Cover Page",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ],
        parent=root  # Ensure dialog is attached to main window
    )
    if file_path:
        global cover_photo_path
        cover_photo_path = file_path
        filename = os.path.basename(file_path)
        if len(filename) > 25:
            filename = filename[:22] + "..."
        cover_photo_btn.config(text=f"📸 {filename}")
        
        # Automatically check the cover page checkbox when photo is selected
        if COVER_AVAILABLE and cover_var is not None:
            cover_var.set(True)
            print("DEBUG: Auto-enabled cover page checkbox")
            
        # Automatically check the Instagram posts checkbox when photo is selected
        if COVER_AVAILABLE and instagram_var is not None:
            instagram_var.set(True)
            print("DEBUG: Auto-enabled Instagram posts checkbox")
        
        print(f"DEBUG: Cover photo selected: {file_path}")
    else:
        # Reset button text based on availability
        if COVER_AVAILABLE:
            cover_photo_btn.config(text="📸 Select Property Photo")
        else:
            cover_photo_btn.config(text="📸 Select Property Photo (install libraries first)")

def convert_jpg_to_pdf(jpg_path, output_path):
    """Convert JPG file to PDF"""
    if not PIL_AVAILABLE:
        return False
        
    try:
        from PIL import Image
        
        # Open and convert JPG to PDF
        img = Image.open(jpg_path)
        
        # Convert RGBA to RGB if necessary (PDF doesn't support transparency)
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Save as PDF
        img.save(output_path, 'PDF', quality=95)
        return True
        
    except Exception as e:
        print(f"Error converting JPG to PDF: {e}")
        return False

def select_and_process_files():
    """Select and immediately process files without complex GUI updates"""
    print("DEBUG: Starting file selection...")
    
    # Update UI to show we're starting
    status_label.config(text="Opening file dialog...", fg="blue")
    root.update_idletasks()  # Force UI update before dialog
    
    try:
        files = filedialog.askopenfilenames(
            title="Select PDF, JPG, or ZIP Files",
            filetypes=[
                ("All supported files", "*.pdf *.zip *.jpg *.jpeg"),
                ("PDF files", "*.pdf"), 
                ("JPG files", "*.jpg *.jpeg"),
                ("ZIP files", "*.zip"),
                ("All files", "*.*")
            ],
            parent=root  # Ensure dialog is attached to main window
        )
        
        print(f"DEBUG: Selected {len(files) if files else 0} files")
        
        if not files:
            status_label.config(text="No files selected", fg="red")
            return
            
        # Show processing status
        status_label.config(text="Processing files...", fg="blue")
        root.update_idletasks()
        
        # Clear and process files immediately
        file_listbox.delete(0, tk.END)
        
        global all_pdf_paths, temp_dir
        all_pdf_paths = []
        
        # Create temp directory if needed
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        temp_dir = tempfile.mkdtemp(prefix="listing_packet_")
        
        print("DEBUG: Processing files...")
        
        for file_path in files:
            file_name = os.path.basename(file_path)
            print(f"DEBUG: Processing: {file_name}")
            
            # Update UI periodically to prevent freezing
            root.update_idletasks()
            
            if not os.path.exists(file_path):
                file_listbox.insert(tk.END, f"❌ {file_name} (not found)")
                continue
            
            if file_path.lower().endswith('.zip'):
                # Process ZIP file
                try:
                    extracted_pdfs = simple_extract_zip(file_path, temp_dir)
                    if extracted_pdfs:
                        file_listbox.insert(tk.END, f"📁 {file_name} ({len(extracted_pdfs)} PDFs)")
                        all_pdf_paths.extend(extracted_pdfs)
                        for pdf_path in extracted_pdfs:
                            pdf_name = os.path.basename(pdf_path)
                            file_listbox.insert(tk.END, f"   📄 {pdf_name}")
                    else:
                        file_listbox.insert(tk.END, f"⚠️ {file_name} (no PDFs)")
                except Exception as e:
                    print(f"DEBUG: ZIP error: {str(e)}")
                    file_listbox.insert(tk.END, f"❌ {file_name} (ZIP error)")
                    
            elif file_path.lower().endswith('.pdf'):
                # Regular PDF
                file_listbox.insert(tk.END, f"📄 {file_name}")
                all_pdf_paths.append(file_path)
                
            elif file_path.lower().endswith(('.jpg', '.jpeg')):
                # Convert JPG to PDF
                try:
                    if PIL_AVAILABLE:
                        # Create temp PDF from JPG
                        jpg_pdf_path = os.path.join(temp_dir, f"{os.path.splitext(file_name)[0]}.pdf")
                        if convert_jpg_to_pdf(file_path, jpg_pdf_path):
                            file_listbox.insert(tk.END, f"📷➡️📄 {file_name} (converted)")
                            all_pdf_paths.append(jpg_pdf_path)
                        else:
                            file_listbox.insert(tk.END, f"❌ {file_name} (conversion failed)")
                    else:
                        file_listbox.insert(tk.END, f"❌ {file_name} (PIL required for JPG)")
                except Exception as e:
                    print(f"DEBUG: JPG conversion error: {str(e)}")
                    file_listbox.insert(tk.END, f"❌ {file_name} (JPG error)")
                    
            else:
                file_listbox.insert(tk.END, f"❌ {file_name} (unsupported)")
        
        # Update status
        if all_pdf_paths:
            status_label.config(text=f"Ready! {len(all_pdf_paths)} PDFs loaded", fg="green")
        else:
            status_label.config(text="No PDFs found", fg="red")
            
        print(f"DEBUG: Processing complete. {len(all_pdf_paths)} PDFs ready")
        
    except Exception as e:
        print(f"DEBUG: Error in file selection: {str(e)}")
        status_label.config(text=f"Error: {str(e)}", fg="red")

def simple_extract_zip(zip_path, temp_dir):
    """Simple ZIP extraction without complex logging"""
    pdf_files = []
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                if (file_name.lower().endswith('.pdf') and 
                    not file_name.startswith('__MACOSX/') and
                    not file_name.startswith('.')):
                    
                    zip_ref.extract(file_name, temp_dir)
                    extracted_path = os.path.join(temp_dir, file_name)
                    if os.path.exists(extracted_path):
                        pdf_files.append(extracted_path)
    except:
        pass  # Silently fail for now
        
    return pdf_files

def create_packet():
    """Create the final PDF packet with optional cover page and Instagram posts"""
    if not all_pdf_paths:
        messagebox.showerror("Error", "Please select PDF or ZIP files first!")
        return
    
    street_address = street_entry.get().strip()
    city_state = city_state_entry.get().strip()
    
    # Check if cover page is requested (handle case where cover_var might be None)
    include_cover = (cover_var.get() if cover_var and COVER_AVAILABLE else False)
    
    # Check if Instagram posts are requested (handle case where instagram_var might be None)
    include_instagram = (instagram_var.get() if instagram_var and COVER_AVAILABLE else False)
    
    # Only require street address and city/state if cover page or Instagram posts are requested
    if (include_cover or include_instagram) and cover_photo_path:
        if not street_address or not city_state:
            messagebox.showerror("Error", "Please enter both street address and city/state for cover page and Instagram posts!")
            return
    
    # For filename, use street address if available, otherwise create a generic name
    if street_address:
        if city_state:
            full_address = f"{street_address}, {city_state}"
        else:
            full_address = street_address
    else:
        full_address = "Listing Packet"
    
    try:
        # Use street address for filename if available, otherwise use generic name
        if street_address:
            output_filename = f"{street_address} - Packet.pdf"
        else:
            output_filename = "Listing Packet.pdf"
        output_path = os.path.join(os.path.expanduser("~/Downloads"), output_filename)
        
        # Create PDF merger
        merger = PdfMerger()
        combined_count = 0
        
        # Add cover page if requested
        if include_cover and cover_photo_path and COVER_AVAILABLE:
            print("DEBUG: Creating cover page...")
            print(f"DEBUG: Cover photo path: {cover_photo_path}")
            print(f"DEBUG: Street: {street_address}")
            print(f"DEBUG: City/State: {city_state}")
            
            # The create_cover_page function creates the PDF directly from PNG templates
            # No PDF template file is needed - it uses the PNG templates in the templates folder
            cover_path = tempfile.mktemp(suffix='_cover.pdf')
            print(f"DEBUG: Creating cover page at: {cover_path}")
            
            # Pass None as template_path since create_cover_page uses PNG templates directly
            if create_cover_page(None, cover_photo_path, street_address, city_state, cover_path):
                try:
                    with open(cover_path, 'rb') as f:
                        merger.append(f)
                    combined_count += 1
                    print("DEBUG: Cover page added successfully to merger")
                    os.unlink(cover_path)
                except Exception as e:
                    print(f"DEBUG: Error adding cover page to merger: {e}")
            else:
                print("DEBUG: Cover page creation failed")
        
        # Add listing PDFs
        for pdf_path in all_pdf_paths:
            try:
                print(f"DEBUG: Attempting to add PDF: {os.path.basename(pdf_path)}")
                with open(pdf_path, 'rb') as f:
                    merger.append(f)
                    combined_count += 1
                    print(f"DEBUG: Successfully added: {os.path.basename(pdf_path)}")
            except Exception as e:
                print(f"DEBUG: Failed to add {os.path.basename(pdf_path)}: {e}")
                continue  # Skip problematic files
        
        if combined_count == 0:
            messagebox.showerror("Error", "No PDF files could be processed!")
            return
        
        print(f"DEBUG: Attempting to write final PDF with {combined_count} pages/files")
        try:
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)
            print("DEBUG: PDF write successful")
        except Exception as write_error:
            print(f"DEBUG: PDF write failed: {write_error}")
            # Try alternative approach with PdfWriter
            try:
                print("DEBUG: Attempting alternative PDF creation method...")
                from PyPDF2 import PdfWriter, PdfReader
                writer = PdfWriter()
                
                # Re-add cover page if it exists
                if include_cover and cover_photo_path and COVER_AVAILABLE:
                    cover_path = tempfile.mktemp(suffix='_cover.pdf')
                    if create_cover_page(None, cover_photo_path, street_address, city_state, cover_path):
                        cover_reader = PdfReader(cover_path)
                        for page in cover_reader.pages:
                            writer.add_page(page)
                        os.unlink(cover_path)
                
                # Re-add PDF files one by one
                for pdf_path in all_pdf_paths:
                    try:
                        reader = PdfReader(pdf_path)
                        for page in reader.pages:
                            writer.add_page(page)
                    except Exception as pdf_error:
                        print(f"DEBUG: Skipping problematic PDF {os.path.basename(pdf_path)}: {pdf_error}")
                        continue
                
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                print("DEBUG: Alternative PDF creation successful")
                
            except Exception as alt_error:
                raise Exception(f"Both PDF creation methods failed. Original error: {write_error}. Alternative error: {alt_error}")
        
        merger.close()
        
        # Create Instagram posts if requested
        instagram_files = []
        if include_instagram and cover_photo_path and COVER_AVAILABLE:
            print("DEBUG: Creating Instagram posts...")
            print(f"DEBUG: Instagram photo path: {cover_photo_path}")
            print(f"DEBUG: Instagram street: {street_address}")
            print(f"DEBUG: Instagram city/state: {city_state}")
            print(f"DEBUG: Photo exists: {os.path.exists(cover_photo_path) if cover_photo_path else 'No path'}")
            downloads_dir = os.path.expanduser("~/Downloads")
            print(f"DEBUG: Downloads directory: {downloads_dir}")
            instagram_files = create_instagram_posts(cover_photo_path, street_address, city_state, downloads_dir)
            print(f"DEBUG: Instagram posts created: {len(instagram_files)} files")
        elif include_instagram:
            print(f"DEBUG: Instagram requested but requirements not met:")
            print(f"DEBUG: include_instagram: {include_instagram}")
            print(f"DEBUG: cover_photo_path: {cover_photo_path}")
            print(f"DEBUG: COVER_AVAILABLE: {COVER_AVAILABLE}")
        
        # Cleanup
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        
        # Success message
        success_msg = f"Created: {output_filename}\nCombined {combined_count} PDFs\nSaved to Downloads folder"
        if include_cover and cover_photo_path and street_address:
            success_msg += f"\n\nIncludes custom cover page:\n• {street_address}"
            if city_state:
                success_msg += f"\n• {city_state}"
        
        if include_instagram and instagram_files:
            success_msg += f"\n\nCreated {len(instagram_files)} Instagram posts:\n"
            for file_path in instagram_files:
                filename = os.path.basename(file_path)
                success_msg += f"• {filename}\n"
        
        messagebox.showinfo("Success!", success_msg)
        status_label.config(text=f"Success! Created {output_filename}" + (f" + {len(instagram_files)} Instagram posts" if instagram_files else ""), fg="green")
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"DEBUG: Full error traceback:\n{error_details}")
        
        # More user-friendly error message
        error_msg = f"Failed to create packet.\n\nTechnical details:\n{str(e)}"
        if "Multiple definitions in dictionary" in str(e) or "Object" in str(e) and "not defined" in str(e):
            error_msg += "\n\nThis appears to be caused by a corrupted or problematic PDF file. Try:\n1. Use fewer PDF files\n2. Check if any PDFs are password-protected\n3. Recreate any problematic PDFs"
        
        messagebox.showerror("Error", error_msg)
        print(f"DEBUG: Error in create_packet: {str(e)}")

# Initialize
all_pdf_paths = []
temp_dir = None
cover_photo_path = None

# Create simple window
root = tk.Tk()
root.title("Hall Collins Listing Packet Combiner")
root.geometry("600x600")  # Made taller for logo
root.configure(bg='#f0f0f0')

# Create main frame with scrollbar
main_canvas = tk.Canvas(root, bg='#f0f0f0')
scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = tk.Frame(main_canvas, bg='#f0f0f0')

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=scrollbar.set)

# Pack the canvas and scrollbar
main_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Bind mousewheel to canvas for smooth scrolling with macOS native support
def _on_mousewheel(event):
    # Handle different platforms and scroll directions properly
    if event.delta:
        # Windows and macOS - use delta value directly
        delta = event.delta
        # Normalize delta for consistent scrolling speed
        if abs(delta) > 100:
            delta = delta // abs(delta) * 3  # Reduce sensitivity for large deltas
        else:
            delta = delta // 40  # Standard sensitivity
        main_canvas.yview_scroll(-delta, "units")
    else:
        # Linux - use event.num
        if event.num == 4:
            main_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            main_canvas.yview_scroll(1, "units")

# Bind scrolling events for all platforms with native behavior
main_canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows & macOS
main_canvas.bind_all("<Button-4>", _on_mousewheel)    # Linux scroll up
main_canvas.bind_all("<Button-5>", _on_mousewheel)    # Linux scroll down

# Also bind to the scrollable frame for better coverage
scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)
scrollable_frame.bind_all("<Button-4>", _on_mousewheel)
scrollable_frame.bind_all("<Button-5>", _on_mousewheel)

# Hall Collins Logo - Enhanced loading with fallback
logo_loaded = False
print(f"DEBUG: Starting logo loading - PIL_AVAILABLE: {PIL_AVAILABLE}")

try:
    if PIL_AVAILABLE:  # Only try if PIL is available
        logo_path = "templates/hall_collins_logo.png"
        logo_full_path = os.path.join(os.getcwd(), logo_path)
        
        print(f"DEBUG: Looking for logo at: {logo_full_path}")
        print(f"DEBUG: Logo exists: {os.path.exists(logo_full_path)}")
        
        if os.path.exists(logo_full_path):
            print("DEBUG: Attempting to load logo image...")
            # Load and resize logo
            logo_image = Image.open(logo_full_path)
            print("DEBUG: Logo image opened successfully")
            
            # Resize to fit nicely (width=200, maintain aspect ratio)
            logo_width = 200
            logo_height = int(logo_image.height * (logo_width / logo_image.width))
            logo_image = logo_image.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            print("DEBUG: Logo image resized successfully")
            
            logo_photo = ImageTk.PhotoImage(logo_image)
            print("DEBUG: Logo converted to PhotoImage successfully")
            
            # Create logo label
            logo_label = tk.Label(scrollable_frame, image=logo_photo, bg='#f0f0f0')
            logo_label.image = logo_photo  # Keep a reference
            logo_label.pack(pady=(20, 10))
            logo_loaded = True
            print("DEBUG: Hall Collins logo loaded and displayed successfully")
        else:
            print("DEBUG: Logo file not found")
    else:
        print("DEBUG: PIL not available for logo loading")
        
except Exception as e:
    print(f"DEBUG: Logo loading failed with exception: {e}")
    import traceback
    traceback.print_exc()
    logo_loaded = False

print(f"DEBUG: Logo loading result: {logo_loaded}")

# Always show title - either logo failed or PIL not available
if not logo_loaded:
    print("DEBUG: Creating fallback title")
    tk.Label(scrollable_frame, text="📄 Hall Collins Listing Packet Combiner",
             font=('System', 18, 'bold'), bg='#f0f0f0', fg='#2C3E50').pack(pady=20)

# Subtitle
tk.Label(scrollable_frame, text="Professional Real Estate Listing Packet Creator",
         font=('System', 12), bg='#f0f0f0', fg='#666').pack(pady=(0, 20))

# Select button
tk.Button(scrollable_frame, text="📁 Select PDF, JPG or ZIP Files", command=select_and_process_files,
         font=('System', 14), bg='#2C3E50', fg='black', width=25, height=2,
         relief='flat', bd=0).pack(pady=10)

# File list - ALWAYS SHOWN
tk.Label(scrollable_frame, text="Selected Files:", font=('System', 12, 'bold'), bg='#f0f0f0').pack(pady=(20, 5))
file_listbox = tk.Listbox(scrollable_frame, height=8, width=70, font=('System', 10), 
                         bg='white', relief='solid', bd=1)
file_listbox.pack(pady=5, padx=20, fill='x')

# Address fields - ALWAYS SHOWN (needed for basic functionality)
tk.Label(scrollable_frame, text="Street Address (optional for basic PDF combining):", 
         font=('System', 12, 'bold'), bg='#f0f0f0', fg='#2C3E50').pack(pady=(20, 5))
street_entry = tk.Entry(scrollable_frame, font=('System', 12), width=50, relief='solid', bd=1, 
                       highlightthickness=1, highlightcolor='#E91E63', bg='white')
street_entry.pack(pady=5)

tk.Label(scrollable_frame, text="City, State (optional for basic PDF combining):", 
         font=('System', 12, 'bold'), bg='#f0f0f0', fg='#2C3E50').pack(pady=(10, 5))
city_state_entry = tk.Entry(scrollable_frame, font=('System', 12), width=50, relief='solid', bd=1,
                           highlightthickness=1, highlightcolor='#E91E63', bg='white')
city_state_entry.pack(pady=5)

# Cover page section - ALWAYS SHOWN with full interface
print(f"DEBUG: About to create GUI section - COVER_AVAILABLE: {COVER_AVAILABLE}")

cover_frame = tk.Frame(scrollable_frame, bg='#f0f0f0', relief='solid', bd=1)
cover_frame.pack(pady=15, fill='x', padx=20)

# ALWAYS create the full interface - just change colors/text based on availability
print("DEBUG: Creating full cover page section - interface always visible")

# Cover page checkbox with Hall Collins styling - ALWAYS SHOWN
cover_var = tk.BooleanVar()
if COVER_AVAILABLE:
    checkbox_text = "📄 Include Hall Collins Cover Page"
    checkbox_color = '#2C3E50'
else:
    checkbox_text = "📄 Include Hall Collins Cover Page (requires library installation)"
    checkbox_color = '#999999'

cover_checkbox = tk.Checkbutton(cover_frame, text=checkbox_text, 
                               variable=cover_var, font=('System', 12, 'bold'), 
                               bg='#f0f0f0', fg=checkbox_color, selectcolor='#f0f0f0',
                               activebackground='#f0f0f0', activeforeground='#E91E63')
cover_checkbox.pack(side='left', padx=10, pady=10)

# Cover photo button with Hall Collins styling - ALWAYS SHOWN
if COVER_AVAILABLE:
    button_text = "📸 Select Property Photo"
    button_bg = '#E91E63'
else:
    button_text = "📸 Select Property Photo (install libraries first)"
    button_bg = '#CCCCCC'

cover_photo_btn = tk.Button(cover_frame, text=button_text, 
                           command=select_cover_photo, bg=button_bg, fg='black', 
                           font=('System', 10, 'bold'), relief='raised', bd=2)
cover_photo_btn.pack(side='right', padx=10, pady=10)

# Instagram posts section - ALWAYS SHOWN
instagram_frame = tk.Frame(scrollable_frame, bg='#f0f0f0', relief='solid', bd=1)
instagram_frame.pack(pady=10, fill='x', padx=20)

# Instagram posts checkbox with Hall Collins styling - ALWAYS SHOWN
instagram_var = tk.BooleanVar()
if COVER_AVAILABLE:
    instagram_text = "📱 Create Instagram Posts (New Listing, Under Contract, Sold)"
    instagram_color = '#2C3E50'
else:
    instagram_text = "📱 Create Instagram Posts (requires library installation)"
    instagram_color = '#999999'

instagram_checkbox = tk.Checkbutton(instagram_frame, text=instagram_text, 
                                   variable=instagram_var, font=('System', 12, 'bold'), 
                                   bg='#f0f0f0', fg=instagram_color, selectcolor='#f0f0f0',
                                   activebackground='#f0f0f0', activeforeground='#E91E63')
instagram_checkbox.pack(padx=10, pady=10)

# Show library status message if needed
if not COVER_AVAILABLE:
    status_frame = tk.Frame(scrollable_frame, bg='#FFF3CD', relief='solid', bd=1)
    status_frame.pack(pady=10, fill='x', padx=20)
    
    status_label = tk.Label(status_frame, text="💡 To enable cover page features, run: INSTALL_REQUIREMENTS.command", 
             font=('System', 11, 'bold'), bg='#FFF3CD', fg='#856404')
    status_label.pack(pady=10)

print("DEBUG: Full GUI interface created - all elements always visible")

# Create button with Hall Collins styling
tk.Button(scrollable_frame, text="🔗 Create Listing Packet", command=create_packet,
         font=('System', 14, 'bold'), bg='#E91E63', fg='black', width=25, height=2,
         relief='flat', bd=0).pack(pady=20)

# Status
status_label = tk.Label(scrollable_frame, text="Ready to select files", 
                       font=('System', 11), bg='#f0f0f0', fg='blue')
status_label.pack(pady=10)

print("Ultra Simple PDF Combiner ready")
root.mainloop()
