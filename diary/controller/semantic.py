# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint
from flask_stormpath import StormpathError, StormpathManager, User, login_required, login_user, logout_user, user
from flask import flash, redirect, render_template, request, url_for
from diary.logger import Log

blueprint = Blueprint('semantic', __name__, static_folder='../static')

@blueprint.route('/semantic', methods=['GET'])
def timeline():
    return render_template('semantic/semantic.html')
