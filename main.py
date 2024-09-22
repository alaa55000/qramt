from pydoc import pager
import flet as ft
import cv2
from pyzbar.pyzbar import decode
import webbrowser
import re
import numpy as np

# Function to decode QR code from an image file
def decode_qr_code_from_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    decoded_objects = decode(img)
    for obj in decoded_objects:
        return obj.data.decode('utf-8')
    return None

# Function to decode QR code using the camera
def decode_qr_code():
    cap = cv2.VideoCapture(0)
    qr_data = None
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Decode QR codes in the frame
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            break
        
        cv2.imshow("QR Code Scanner", frame)
        if qr_data:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return qr_data

# Function to validate URL
def is_valid_url(url):
    # Regex to validate URL format
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

# Function to handle file selection
def file_picker_result(e: ft.FilePickerResultEvent, link_display):
    if e.files:
        # Decode QR code from the selected image file
        image_path = e.files[0].path
        qr_data = decode_qr_code_from_image(image_path)
        
        # Clear previous controls
        link_display.controls.clear()

        # Validate and open the URL directly
    if qr_data and is_valid_url(qr_data):
        webbrowser.open(qr_data)
        link_display.controls.append(ft.Container(content=ft.Text(f"Opening URL: {qr_data},",color="black",size=16),alignment=ft.alignment.center,padding=30))
    else:
        link_display.controls.append(
    ft.Container(
        content=ft.Text(
            "لا يوجد رابط الكتروني",
            color="black",
            size=16          
                       
        ),
        alignment=ft.alignment.center,  # وضع النص في منتصف الحاوية
        padding=30,    # إضافة مسافة حول النص
    )
)
        

    link_display.update()
        

# Function to handle scanning QR code via camera
def handle_scan_qr_code(e, link_display):
    qr_data = decode_qr_code()
    
    # Clear previous controls
    link_display.controls.clear()

    # Validate and open the URL directly
    if qr_data and is_valid_url(qr_data):
        webbrowser.open(qr_data)
        link_display.controls.append(ft.Container(content=ft.Text(f"Opening URL: {qr_data},",color="black",size=16),alignment=ft.alignment.center,padding=30))
    else:
        link_display.controls.append(
    ft.Container(
        content=ft.Text("لا يوجد رابط الكتروني",
            color="black",         # لون النص
            size=16
            
        ),
        alignment=ft.alignment.center,  # وضع النص في منتصف الحاوية
        padding=30,    # إضافة مسافة حول النص
    )
)
        

    link_display.update()
    

def main(page: ft.Page):
    
    
    
    page.title = "QR_AMT"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor=ft.colors.CYAN
    
    
    
   
   
    
    



    # Display elements where QR code URL will be shown
    link_display = ft.Column()
    
    #logo
    image1 = ft.Image(src="amt.png", width=400, height=80)
    # Button to trigger QR code scanning
    scan_button =ft.Container(ft.ElevatedButton("Scan QR Code", on_click=lambda e: handle_scan_qr_code(e, link_display), width=165),padding=40)
            
         
    
   


    
    
    

    # File picker for selecting an image
    file_picker = ft.FilePicker(on_result=lambda e: file_picker_result(e, link_display))
    
    
    
    # Add the file picker to the page overlay
    page.overlay.append(file_picker)
    
    
    # إنشاء ستاك فارغ مع بادينج
   
    # Upload button for uploading an image
    upload_button =ft.Container(ft.ElevatedButton("Upload QR Code ", on_click=lambda e: file_picker.pick_files(allow_multiple=False),width=165),padding=20)
         
    text = ft.Text(value="للدخول للرابط المراد (skip advertisement) اذا ظهرت لك هذه الصفحة اضغط على الزر المشار اليه فى الصورة", size=20, color="white")
    image = ft.Image(src="non.png", width=700, height=400)
    


    
    

    # Add elements to the page
    page.add(image1,scan_button, upload_button, link_display,text,image)
    


    
    
    
   

   
    

ft.app(target=main)
