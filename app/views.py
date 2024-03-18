"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, session, abort,send_from_directory
from werkzeug.utils import secure_filename
from app.models import Property
from .forms import PropertyForm
###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/properties/create', methods=['POST', 'GET'])
def createProperty():
    """Render the website's property create page."""
    propertyForm = PropertyForm()
    #print("line 31")
    if request.method == 'POST':
        #print("line 33")
        if propertyForm.validate_on_submit():
            #print("line 35")
            title = propertyForm.title.data
            numberOfBedrooms = propertyForm.numberOfBedrooms.data
            numberOfBathrooms = propertyForm.numberOfBathrooms.data
            location = propertyForm.location.data
            price = propertyForm.price.data
            type= propertyForm.type.data
            description = propertyForm.description.data
            filename = propertyForm.filename.data # we could also use request.files['photo']
            #print("line 43")
            filenameFolder = secure_filename(filename.filename)
            filenamePath=os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']), filename

            #print("line 45")

            property=Property(title,numberOfBedrooms,numberOfBathrooms,location,price,type,description,filenamePath)
            #print("line 48")
            db.session.add(property)
            db.session.commit()
            #print("line 51")


            filename.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filenameFolder
            ))
            #print("line 57")

            flash('Property added!!!', 'success')
            return render_template('properties.html',title=title,description=description,numberOfBedrooms=numberOfBedrooms,numberOfBathrooms=numberOfBathrooms,price=price,type=type,location=location,filename=filename)

        flash_errors(propertyForm)
    return render_template('create.html',form=propertyForm)

@app.route('/properties',methods=['GET'])
def properties():
    """Render the website's properties page."""
    allProperties=Property.query.all()
    return render_template('properties.html',allProperties=allProperties)

@app.route('/properties/<propertyid>', methods=['GET','POST'])
def findProperty(propertyid):
    """Render the a specific property on the website."""
    print(f"Property ID={propertyid}")
    print("Line 78")
    queryProperty = db.get_or_404(Property, propertyid)
    return render_template('property.html',queryProperty=queryProperty)

@app.route('/property/<filename>', methods=['GET'])
def get_image(filename):
    rootdir=os.getcwd()
    b=f"\\uploads\\{filename}"
    print(os.path.join(os.getcwd(),b))
    return send_from_directory(os.path.join(rootdir,app.config['UPLOAD_FOLDER']), filename)

def get_uploaded_images():
    rootdir = os.getcwd()
    uploaded_images = []
    #print ("Line 1",rootdir)

    for subdir, dirs, files in os.walk(rootdir + '/uploads'):
        for file in files:
            uploaded_images.append(os.path.join(subdir, file).split("\\")[-1])
    return uploaded_images[1:]
###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
