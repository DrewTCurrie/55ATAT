import os
import sys
import textwrap

#Import numpy for removing qr code background
import numpy as np

#QRcode library and package to make the QR code as an SVG
import qrcode
import qrcode.image.svg
#import QRcode styling packages
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

from PIL import Image, ImageDraw, ImageFont

from flask import render_template, jsonify, url_for

from APIFuncs import utils


#Goals:
#Create a better looking QR Code in python
#Create a badge that is not being cut off when printed on PVC
#Create a badge that has more readable fonts.

#Define PTC colors
PEACH = 212, 117, 84
SUNSHINE = 232, 186, 99
BACKGROUND = 0,0,0,0

#1. Create a better looking QR Code 
def generate_qr_code(userID, filename):
        #Setup custom QR code generation properties
        customQR = qrcode.QRCode(
                image_factory=StyledPilImage,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                border=0,
                box_size=30,            #Must be a factor of 10, larger takes longer to process. 30 Seems to be a good spot between time to complete and resolution when printed
                version=3,
                )

        customQR.add_data(userID)
        attendeeQR = customQR.make_image(
                module_drawer=RoundedModuleDrawer(), 
                eye_drawer=RoundedModuleDrawer(),
                color_mask=RadialGradiantColorMask(back_color=(255, 255, 255), 
                center_color=(SUNSHINE), 
                edge_color=(PEACH)),
                embeded_image_path=os.path.join('flaskServer', 'APIFuncs', 'PTClogo.png'))
        attendeeQR.save(filename)
        image=attendeeQR
        # transform image to RGBA
        image = image.convert('RGBA')
        newImage = []
        for item in image.getdata():
                if item[:3] == (255,255,255):
                        newImage.append((255,255,255,0))
                else:
                      newImage.append(item)
        image.putdata(newImage)
        image.save(filename)

# Function to add text to an image
def add_text_to_image(img_path, text, output_path, position, font_size=40, font_path=os.path.join('flaskServer', 'APIFuncs', 'OpenSans-Bold.ttf')):
        img = Image.open(img_path).convert("RGBA")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, font_size)
        draw.text((position[0], position[1]), text, fill="black", font=font)
        img.save(output_path)

def embed_user_image(base_img_path, user_img_path, output_path, user_img_size, user_img_position):
    base_img = Image.open(base_img_path).convert("RGBA")
    user_img = Image.open(user_img_path).resize(user_img_size).convert("RGBA")

    # Create a circular mask
    mask = Image.new("L", user_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + user_img.size, fill=255)

    user_img.putalpha(mask)

    # Paste the user's image onto the base image
    base_img.paste(user_img, user_img_position, user_img)
    base_img.save(output_path)


def generate_employee_badge(userID, Name):
        #PTC Basic Info
        address_firstline = "Address: 1091 Stoneridge Dr,"
        address_secondline = "Bozeman, MT 59718"
        phone = "Phone: (406)-624-6599"
        initials=Name

        #Load employee template
        front_img_path = os.path.join('flaskServer', 'static', 'BadgeTemplates', 'Template_EmployeeFront.png')
        front_output_path = os.path.join('flaskServer', 'static', 'EmployeeFrontWithDetails.png')
        
        #Format initials -> Replace with name for employees
        front_img = Image.open(front_img_path)
        template_width, template_height = front_img.size
        #load font to get sizes
        font_path = os.path.join('flaskServer', 'APIFuncs', 'OpenSans-Bold.ttf')
        font_size = 40
        font = ImageFont.truetype(font_path, font_size)
        #Add initials to the badge
        initials_length = font.getlength(initials)
        add_text_to_image(
                front_img_path,
                initials,
                front_output_path,
                (int((template_width/2)-(initials_length/2)), 650)
        )
        
        role_length = font.getlength("Employee")
        add_text_to_image(
                front_output_path,
                "Employee",
                front_output_path,
                (int((template_width/2)-(role_length/2)), 650+40+10)
        )

        # Embed user image into EmployeeFrontWithDetails
        #Check to see if an image exists, if not then use base ptclogo
        if os.path.isfile(os.path.join('flaskServer', 'profileImage', f'{userID}.png')):
            user_image_path = os.path.join('flaskServer', 'profileImage', f'{userID}.png')
        else:
            user_image_path = os.path.join('flaskServer', 'static', 'BadgeTemplates', 'Template_ptclogo.png')
        embed_user_image(front_output_path, user_image_path, front_output_path, user_img_size=(360, 360),
                         user_img_position=(114, 165))

        # Generate QR code for EmployeeBack
        qr_data = userID
        qr_filename = os.path.join('flaskServer', 'static', 'EmployeeBackQR.png')
        generate_qr_code(qr_data, qr_filename)

        #Load employee back template
        back_img_path = os.path.join('flaskServer', 'static', 'BadgeTemplates', 'Template_EmployeeBack.png')
        back_output_path = os.path.join('flaskServer', 'static', 'EmployeeBackWithQR.png')
        back_img = Image.open(back_img_path)

        qr_img = Image.open(qr_filename).resize((350, 350)).convert('RGBA')
        #Determine center of the template dynamically
        template_width, template_height = back_img.size
        qr_width, qr_height = qr_img.size
        back_img.paste(qr_img, box=(int((template_width/2)-(qr_width/2))+5, int((template_height/2)-(qr_height/2))+50), mask=qr_img)
        back_img.save(back_output_path)

        #Load the font at the desired size
        font_path = os.path.join('flaskServer', 'APIFuncs', 'OpenSans-Regular.ttf')
        font_size = 30
        font = ImageFont.truetype(font_path, font_size)

        #Calculate the size of each of the texts and template to center each string dynamically
        phone_width = font.getlength(phone)
        add_text_to_image(
                back_output_path,
                phone,
                back_output_path,
                (int((template_width/2)-(phone_width/2)), 800),
                font_size=font_size,
                font_path = font_path
        )

        address_firstline_width = font.getlength(address_firstline)
        add_text_to_image(
                back_output_path,
                address_firstline,
                back_output_path,
                (int((template_width/2)-(address_firstline_width/2)), 800+10+font_size),
                font_size=font_size,
                font_path = font_path
        )

        address_secondline_width = font.getlength(address_secondline)
        add_text_to_image(
                back_output_path,
                address_secondline,
                back_output_path,
                (int((template_width/2)-(address_secondline_width/2)), 800+20+font_size*2),
                font_size=font_size,
                font_path = font_path
        )

def generate_client_badge(userID, initials, service):
        #Load client template
        front_img_path = os.path.join('flaskServer', 'static', 'BadgeTemplates', 'Template_Client.png')
        #Using old name for the file output to maintain compatibility as that is another fix altogether
        front_output_path = os.path.join('flaskServer', 'static', 'NonEmployeeFrontWithDetails.png')
        
        #Open template and font
        front_img = Image.open(front_img_path)
        template_width, template_height = front_img.size

        #load font to get sizes
        font_path = os.path.join('flaskServer', 'APIFuncs', 'OpenSans-Bold.ttf')
        font_size = 35
        font = ImageFont.truetype(font_path, font_size)

        #Generate QR Code
        qr_data = userID
        qr_filename = os.path.join('flaskServer', 'static', 'NonEmployeeBack.png')
        generate_qr_code(qr_data, qr_filename)
        
        #Add QR code to the badge
        qr_img = Image.open(qr_filename).resize((350, 350)).convert('RGBA')
        #Determine center of the template dynamically
        template_width, template_height = front_img.size
        qr_width, qr_height = qr_img.size
        front_img.paste(qr_img, box=(int((template_width/2)-(qr_width/2))+5, int((template_height/2)-(qr_height/2))+175), mask=qr_img)
        front_img.save(front_output_path)


        #Add initials to the badge
        initials_length = font.getlength(initials)
        add_text_to_image(
                front_output_path,
                initials,
                front_output_path,
                (int((template_width/2)-(initials_length/2)), 675+int(qr_width/2))
        )
        
        service_length = font.getlength(service[0])
        add_text_to_image(
                front_output_path,
                service[0],
                front_output_path,
                (int((template_width/2)-(service_length/2)), 675+font_size+10+int(qr_width/2))
        )




def generate_badge(userID):

        attendeeInfo = utils.getAttendee(userID)
        employeeRoles = utils.getEmployeeRoles()
        if any(getattr(attendeeInfo, col, False) is True for col in employeeRoles) or attendeeInfo.Administrator:
                generate_employee_badge(userID, attendeeInfo.AttendeeInitials)
                front_url = url_for('static', filename='EmployeeFrontWithDetails.png', _external=True)
                back_url = url_for('static', filename='EmployeeBackWithQR.png', _external=True)
                return jsonify({'front': front_url,'back':back_url})
        else:
                generate_client_badge(userID, attendeeInfo.AttendeeInitials, utils.getAttendeeRole(userID))
                front_url = url_for('static', filename='NonEmployeeFrontWithDetails.png', _external=True)
                return jsonify({'front': front_url})
if __name__ == '__main__':
    generate_badge('PTCBZN-10099262496')
