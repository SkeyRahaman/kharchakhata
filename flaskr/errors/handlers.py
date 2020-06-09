from http.client import HTTPException

from flask import Blueprint, render_template, redirect
import itsdangerous.exc
import sqlalchemy.exc
import mysql.connector.errors

errors = Blueprint('errors', __name__,
                   template_folder='templates', )


@errors.app_errorhandler(404)
def error_404(error):
    return render_template("error_404.html"), 404


@errors.app_errorhandler(500)
def error_500(error):
    return """<!DOCTYPE html>
        <html>
        <head>
                <title>KharchaKhata - error</title>
                <link rel="icon" href="https://pngimg.com/uploads/letter_k/letter_k_PNG69.png" type="image/png">
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        
        
                <style>
                    .heading {
                        background-image: linear-gradient(to right , #1FBFCA , #E8C718);
                        padding-bottom: 10px;
                        margin-bottom: 10px;
                        font-size: 40px;
                    }
                    .heading a{
                        color: #DC004B;
                    }
                    .heading a:hover{
                        color: #DC004B;
                    }
                    .footer{
                         background-image: linear-gradient(to right , #1FBFCA , #E8C718);
                         margin-top: 10px;
                         padding-bottom: 10px;
                         padding-top: 10px;
                         position: relative;
                         bottom: 0;
                         margin-bottom: 0px;
                         width: 100%;
                    }
                    .heading #name_app{
                        text-align: right;
                    }
                    body {
                        padding-bottom: 5%;
                        margin-bottom: 5%;
                    }
                </style>
        </head>
        <body>
            <nav class="navbar heading">
                <strong id="name_app"><a href="/">KHARCHAKHATA</a></strong>
            </nav>
        
            <div class="card bg-light m-auto">
                <div class="card-body text-center">
                    <h1>Server side error.</h1>
                    <h2>500 error.</h2>
                    <p>We are currently working on this issue.</p>
                    <p>Please wait for 2 second it should resolve by it self..</p>
                    <p>If not, Please check after some time. Or go back...</p>
                </div>
            </div>
            <div class="text-center">
                <button class="btn btn-outline-success" onclick="history.back();">BACK</button>
            </div>
        
            <div class="footer text-center">
                <a href="http://shakib-portfolio-app.herokuapp.com/">
                    <div class="btn">
                    A Complete Project By Md Shakib Mondal
                    </div>
                </a>
            </div>
            <script type="text/javascript">
                setTimeout(function(){location.reload()}, 1000);
                if (window.screen.height <= document.body.clientHeight){
                    document.getElementsByClassName("footer")[0].style.position = "relative";
                } else {
                    document.getElementsByClassName("footer")[0].style.position = "fixed";
                }
            </script>
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
        </body>
        </html>""", 500


@errors.app_errorhandler(itsdangerous.exc.BadSignature)
def error_500(error):
    return render_template("error_mail_url.html"), 500


@errors.app_errorhandler(sqlalchemy.exc.OperationalError)
def error_db(error):
    return render_template("error_db_connection.html"), 500


@errors.app_errorhandler(sqlalchemy.exc.StatementError)
def error_db(error):
    return render_template("error_db_connection.html"), 500


@errors.app_errorhandler(sqlalchemy.exc.InterfaceError)
def error_db(error):
    return render_template("error_db_connection.html"), 500


@errors.app_errorhandler(sqlalchemy.exc.InvalidRequestError)
def error_db(error):
    return render_template("error_db_connection.html"), 500


@errors.app_errorhandler(mysql.connector.errors.OperationalError)
def error_db(error):
    return render_template("error_db_connection.html"), 500


@errors.errorhandler(HTTPException)
def http_error_handler(error):
    return render_template("error_db_connection.html"), 500
