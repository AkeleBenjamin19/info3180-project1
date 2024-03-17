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


@app.route('/properties/create')
def createProperty():
    """Render the website's property create page."""
    propertyForm = PropertyForm()
    
    if request.method == 'POST':
        if propertyForm.validate_on_submit():
            
            title = propertyForm.title.data
            numberOfBedrooms = propertyForm.numberOfBedrooms.data
            numberOfBathrooms = propertyForm.numberOfBathrooms.data
            location = propertyForm.location.data
            price = propertyForm.price.data
            type= propertyForm.type.data
            description = propertyForm.description.data
            filename = propertyForm.filename.data # we could also use request.files['photo']
            filenameFolder = secure_filename(filename.filenameFolder)

            property=Property(title,numberOfBedrooms,numberOfBathrooms,location,price,type,description,filenameFolder)
            db.session.add(property)
            db.session.commit()


            filename.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filenameFolder
            ))

            return render_template('properties.html')

        flash_errors(propertyForm)
    return render_template('create.html',form=propertyForm)

@app.route('/properties')
def properties():
    """Render the website's properties page."""
    return render_template('properties.html')

@app.route('/properties/<propertyid>')
def findProperty(id):
    """Render the a specific property on the website."""
    return render_template('property.html', id=id)
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
