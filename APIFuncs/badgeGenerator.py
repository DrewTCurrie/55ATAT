import os
import sys
import textwrap

import qrcode
from PIL import Image, ImageDraw, ImageFont
from flask import render_template, jsonify, url_for

from APIFuncs import utils


# Helper function to generate a QR code, generates QR code based on ID so that it remains the same if needing to be regenerated.
def generate_qr_code(userID, filename):
    ptclogo = Image.open(
        os.path.join('flaskServer', 'static', 'ptclogo.png'))  #TODO: add ptclogo to center of QR code.
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(userID)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)


# Function to add text to an image
def add_text_to_image(img_path, text, output_path, position, font_size=50):
    img = Image.open(img_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("APIFuncs/Arial.ttf", font_size)
    # Split the text into multiple lines
    lines = text.split('\n')
    y = position[1]
    for line in lines:
        draw.text((position[0], y), line, fill="black", font=font)
        y += font_size + 10  # Move to the next line (adjust spacing as needed)

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


def generate_badge(userID):
    #Query User Details:
    attendeeInfo = utils.getAttendee(userID)
    if attendeeInfo.Employee | attendeeInfo.Administrator:
        address = "1091 Stoneridge Dr, Bozeman, MT 59718"
        phone = "(406)-624-6599"
        initials = attendeeInfo.AttendeeInitials

        # Format the address and phone number
        address_lines = textwrap.wrap(f"Address:{address}", width=20)
        formatted_address = "\n".join(address_lines)
        formatted_phone = f"Phone: {phone}"

        # Add name, "Employee", phone, and address to EmployeeFront
        front_img_path = os.path.join('flaskServer', 'static', 'EmployeeFront.png')
        front_output_path = os.path.join('flaskServer', 'static', 'EmployeeFrontWithDetails.png')
        add_text_to_image(
            front_img_path,
            f"{initials}\nEmployee\n\n{formatted_phone}\n{formatted_address}",
            front_output_path,
            (50, 570),
            font_size=30
        )
        # Embed user image into EmployeeFrontWithDetails
        #Check to see if an image exists, if not then use base ptclogo
        if os.path.isfile(os.path.join('flaskServer', 'profileImage', f'{userID}.png')):
            user_image_path = os.path.join('flaskServer', 'profileImage', f'{userID}.png')
        else:
            user_image_path = os.path.join('flaskServer', 'static', 'ptclogo.png')
        embed_user_image(front_output_path, user_image_path, front_output_path, user_img_size=(360, 360),
                         user_img_position=(114, 165))

        # Generate QR code for EmployeeBack
        qr_data = userID
        qr_filename = os.path.join('flaskServer', 'static', 'EmployeeBackQR.png')
        generate_qr_code(qr_data, qr_filename)

        # Combine QR code with EmployeeBack and add details
        back_img_path = os.path.join('flaskServer', 'static', 'EmployeeBack.png')
        back_output_path = os.path.join('flaskServer', 'static', 'EmployeeBackWithQR.png')
        back_img = Image.open(back_img_path).convert("RGBA")
        qr_img = Image.open(qr_filename).resize((400, 400))
        back_img.paste(qr_img, (110, 400))
        back_img.save(back_output_path)

        front_url = url_for('static', filename='EmployeeFrontWithDetails.png', _external=True)
        back_url = url_for('static', filename='EmployeeBackWithQR.png', _external=True)
        return jsonify({'front': front_url,'back':back_url})

    else:
        service = utils.getAttendeeRole(userID)
        initials = attendeeInfo.AttendeeInitials

        # Format the service text
        service_lines = textwrap.wrap(f"Service: {service[0]}", width=20)
        formatted_service = "\n".join(service_lines)

        # Add initials and service details to NonEmployeeFront
        front_img_path = os.path.join('flaskServer', 'static', 'NonEmployeeFront.png')
        front_output_path = os.path.join('flaskServer', 'static', 'NonEmployeeFrontWithDetails.png')

        add_text_to_image(
            front_img_path,
            f"{initials}\n{formatted_service}",
            front_output_path,
            (60, 850), # Adjust as needed to fit text and QR code
            font_size=30
        )

        # Generate QR code and place it on the front image
        qr_data = userID
        qr_filename = os.path.join('flaskServer', 'static', 'NonEmployeeBack.png')
        generate_qr_code(qr_data, qr_filename)

        # Combine QR code with the front image
        front_img = Image.open(front_output_path).convert("RGBA")
        qr_img = Image.open(qr_filename).resize((350, 350))  # Resize as needed to fit the layout
        front_img.paste(qr_img, (110, 480))  # Adjust position to fit text and QR
        front_img.save(front_output_path)
        # Create a URL for the image, to service the webpage.
        front_url = url_for('static', filename='NonEmployeeFrontWithDetails.png', _external=True)
        return jsonify({'front': front_url})


if __name__ == '__main__':
    generate_badge('PTCBZN-14740603386')
